#!/usr/bin/env python3
"""Scores one run of the parity suite: each document's PDF from wkhtmltopdf beside the one from
marqius-wkhtmltopdf, made on the same system with the same fonts (convert.sh).

The parity measure is the marqius engine's own (its parity.py, copied below unchanged), so that
the figures published for marqius-wkhtmltopdf can be checked. For each document:

    score = 0.5 x text + 0.3 x word positions + 0.2 x page count          (each from 0 to 1)

  text            how much of the text agrees, in reading order: difflib's ratio between the
                  two texts poppler's pdftotext finds, with all runs of white space made one space
  word positions  the words are paired in order (difflib again) and each pair scores 1 when the
                  two words' centres coincide, falling to 0 when they are 60 points apart; the sum
                  is divided by the number of words in the longer document, so a missing word
                  counts as 0
  page count      1 when both have as many pages, otherwise 1 - difference / larger count

A set's parity is the mean of its documents' scores. Beside the measure, the report gives the
program's own document-by-document comparison (marqius-wkhtmltopdf compare), the fonts each PDF
names, file sizes, exit statuses and times.

    python3 score.py WORK CORPUS META      (in the scorer container; no network is needed)

WORK is the folder convert.sh filled, CORPUS the folder of sets, META a file of what run.sh knows
(images, digests, tag, platform), one fact a line: key, a tab, value. Writes WORK/report.json, report.md, report.html and
scores.csv, and prints a summary.
"""
import csv
import difflib
import html
import json
import os
import re
import statistics
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# ---------------------------------------------------------------------------------------------
# The engine's measure: parity.py (marqius, tests' parity harness), unchanged. WEIGHTS, run,
# pdftotext, pages, words and geom_score are copied from it; score_pair is how the published
# figures were scored (tools/download-tests/judge.py and tools/wkparity.py).
WEIGHTS = {"text": 0.5, "geom": 0.3, "pages": 0.2}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def pdftotext(p):
    r = run(["pdftotext", str(p), "-"])
    return re.sub(r"\s+", " ", r.stdout).strip()


def pages(p):
    r = run(["pdfinfo", str(p)])
    m = re.search(r"Pages:\s+(\d+)", r.stdout)
    return int(m.group(1)) if m else 0


WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')


def words(p):
    """All words with positions (pt), page order preserved."""
    r = run(["pdftotext", "-bbox", str(p), "-"])
    out = []
    for m in WORD_RE.finditer(r.stdout):
        x1, y1, x2, y2 = (float(m.group(i)) for i in range(1, 5))
        out.append((x1, y1, x2, y2, m.group(5)))
    return out


def geom_score(p_pdf, m_pdf):
    """Match words pairwise by (text, order); reward close positions (pt)."""
    wp, wm = words(p_pdf), words(m_pdf)
    if not wp or not wm:
        return 0.0
    sm = difflib.SequenceMatcher(None, [w[4] for w in wp], [w[4] for w in wm])
    score_sum, matched = 0.0, 0
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            x1p, y1p, x2p, y2p, _ = wp[a + k]
            x1m, y1m, x2m, y2m, _ = wm[b + k]
            # position error: center-point distance, normalized (>=60pt off = 0)
            cxd = abs((x1m + x2m) / 2 - (x1p + x2p) / 2)
            cyd = abs((y1m + y2m) / 2 - (y1p + y2p) / 2)
            d = (cxd * cxd + cyd * cyd) ** 0.5
            score_sum += max(0.0, 1.0 - d / 60.0)
            matched += 1
    return score_sum / max(len(wp), len(wm))


def pdf_ok(p):
    p = Path(p)
    return p.is_file() and p.stat().st_size > 0 and p.read_bytes()[:5] == b"%PDF-"


def score_pair(rp, mp):
    """(score, text, geom, pages of wkhtmltopdf's, pages of marqius-wkhtmltopdf's)"""
    if not pdf_ok(rp) or not pdf_ok(mp):
        return 0.0, 0.0, 0.0, pages(rp) if pdf_ok(rp) else 0, pages(mp) if pdf_ok(mp) else 0
    tr, tm = pdftotext(rp), pdftotext(mp)
    text = difflib.SequenceMatcher(None, tr, tm).ratio() if tr or tm else 1.0
    geom = geom_score(rp, mp) if tr else 1.0
    pr, pm = pages(rp), pages(mp)
    pg = 1.0 if pr == pm else max(0.0, 1.0 - abs(pr - pm) / max(pr, pm, 1))
    return WEIGHTS["text"] * text + WEIGHTS["geom"] * geom + WEIGHTS["pages"] * pg, text, geom, pr, pm
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# How the pages look, apart from what their text says: each page drawn in grey at 72 dpi (a dot is
# a point), every dot darker than INK is ink, and a dot of ink is matched when the other PDF has
# ink within NEAR points of it. looks = matched ink of both / all ink of both; a page only one PDF
# has counts as unmatched. Words that moved by a point or two still match; reversed or missing
# letters, missing pictures and text set elsewhere do not.
DPI, INK, NEAR = 72, 160, 2
INK_BITS = bytes.maketrans(bytes(range(256)), bytes(ord("1") if v < INK else ord("0") for v in range(256)))


def bitmaps(pdf, tmp):
    """each page as a list of rows, each row an integer whose set bits are the ink"""
    base = Path(tmp) / Path(pdf).stem
    subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", str(pdf), str(base)], capture_output=True, timeout=300)
    pages_ = []
    for f in sorted(Path(tmp).glob(base.name + "-*.pgm"), key=lambda x: int(x.stem.rsplit("-", 1)[1])):
        data = f.read_bytes()
        # P5 header: magic, width, height, maxval, each separated by white space
        fields, i = [], 0
        while len(fields) < 4:
            while data[i:i + 1].isspace():
                i += 1
            j = i
            while not data[j:j + 1].isspace():
                j += 1
            fields.append(data[i:j])
            i = j
        w, h = int(fields[1]), int(fields[2])
        px = data[i + 1:]
        pages_.append([int(px[y * w:(y + 1) * w].translate(INK_BITS), 2) for y in range(h)])
        f.unlink()
    return pages_


def grow(rows):
    """ink spread by NEAR dots in every direction"""
    wide = []
    for r in rows:
        x = r
        for k in range(1, NEAR + 1):
            x |= (r << k) | (r >> k)
        wide.append(x)
    out = []
    for y in range(len(wide)):
        x = 0
        for yy in range(max(0, y - NEAR), min(len(wide), y + NEAR + 1)):
            x |= wide[yy]
        out.append(x)
    return out


def looks_alike(rp, mp):
    import tempfile
    if not pdf_ok(rp) or not pdf_ok(mp):
        return 0.0
    with tempfile.TemporaryDirectory() as t:
        ta, tb = Path(t) / "a", Path(t) / "b"
        ta.mkdir()
        tb.mkdir()
        A, B = bitmaps(rp, ta), bitmaps(mp, tb)
    ink = matched = 0
    for k in range(max(len(A), len(B))):
        a = A[k] if k < len(A) else []
        b = B[k] if k < len(B) else []
        ia = sum(r.bit_count() for r in a)
        ib = sum(r.bit_count() for r in b)
        ink += ia + ib
        if a and b:
            ga, gb = grow(a), grow(b)
            n = min(len(a), len(b))
            matched += sum((a[y] & gb[y]).bit_count() for y in range(n)) + sum((b[y] & ga[y]).bit_count() for y in range(n))
    return 1.0 if ink == 0 else matched / ink


def fonts_of(p):
    """The fonts a PDF names, without the six-letter prefix of a subset (as the harness lists them)."""
    if not pdf_ok(p):
        return []
    names = []
    for line in run(["pdffonts", str(p)]).stdout.splitlines()[2:]:
        if line.strip():
            names.append(re.sub(r"^[A-Z]{6}\+", "", line.split()[0]))
    return sorted(set(names))


def one(job):
    s, n, rp, mp = job
    sc, text, geom, pr, pm = score_pair(rp, mp)
    return dict(set=s, name=n, score=sc, text=text, geom=geom, pages_wk=pr, pages_mq=pm, looks=looks_alike(rp, mp),
                fonts_wk=fonts_of(rp), fonts_mq=fonts_of(mp),
                size_wk=Path(rp).stat().st_size if pdf_ok(rp) else 0,
                size_mq=Path(mp).stat().st_size if pdf_ok(mp) else 0,
                made_wk=pdf_ok(rp), made_mq=pdf_ok(mp))


def read_meta(p):
    """run.sh's facts, one a line (key, a tab, value; dots in a key make nested objects)"""
    meta = {}
    for line in Path(p).read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        k, v = line.split("\t", 1)
        o = meta
        *path, last = k.split(".")
        for part in path:
            o = o.setdefault(part, {})
        if last in ("size_mb",):
            v = float(v or 0)
        o[last] = v
    meta["sets"] = meta.get("sets_list", "").split()
    meta["label_of"] = {s: meta.get("label", {}).get(s, "main") for s in meta["sets"]}
    meta["first_label"] = meta["label_of"][meta["sets"][0]] if meta["sets"] else "main"
    return meta


def read_tsv(p):
    if not Path(p).exists():
        return []
    return [line.rstrip("\n").split("\t") for line in Path(p).read_text(encoding="utf-8").splitlines() if line.strip()]


def median(xs):
    return statistics.median(xs) if xs else None


def kb(n):
    return f"{n / 1024:.0f} KB" if n >= 10240 else f"{n / 1024:.1f} KB"


def ms_text(ms):
    if ms is None:
        return ""
    return "<10 ms" if ms < 10 else f"{ms:.0f} ms" if ms < 10000 else f"{ms / 1000:.1f} s"


def verdict_word(v):
    """compare's verdicts, as the report counts them: 'file differs' means the pages are the same"""
    return {"same": "same pages", "file differs": "same pages", "appearance only": "appearance only",
            "content differs": "content differs", "cannot tell": "cannot tell"}.get(v, v or "not compared")


def main():
    work, corpus, meta_file = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    meta = read_meta(meta_file)
    sets_info = {r[0]: dict(image=r[1], published=r[2] == "yes", title=r[3], about=r[4])
                 for r in read_tsv(corpus / "sets.tsv")[1:]} if (corpus / "sets.tsv").exists() else {}
    notes = {(r[0], r[1]): r[2] for r in read_tsv(corpus / "notes.tsv")[1:]} if (corpus / "notes.tsv").exists() else {}
    sets = meta["sets"]

    # every pair, scored on every core
    jobs = []
    for s in sets:
        d_wk, d_mq = work / "pdf" / "wk" / s, work / "pdf" / "mq" / s
        names = sorted({p.stem for p in d_wk.glob("*.pdf")} | {p.stem for p in d_mq.glob("*.pdf")})
        # documents neither program made: from the times of the first run
        for row in read_tsv(work / "times" / f"{meta['label_of'][s]}.tsv"):
            if row[1] == "1" and row[2] == s and row[3] not in names:
                names.append(row[3])
        for n in sorted(set(names)):
            jobs.append((s, n, str(d_wk / f"{n}.pdf"), str(d_mq / f"{n}.pdf")))
    with ProcessPoolExecutor() as ex:
        docs = list(ex.map(one, jobs))

    # exit statuses and times of each document (the first run's status; the median time of the runs)
    status, times = {}, {}
    for label in sorted(set(meta["label_of"].values())):
        for who, run_, s, n, st, ms in read_tsv(work / "times" / f"{label}.tsv"):
            if run_ == "1":
                status[(who, s, n)] = int(st)
            if run_.isdigit():
                times.setdefault((who, s, n), []).append(int(ms))
    # compare's verdict for each pair
    verdicts = {}
    for s in sets:
        p = work / "compare" / s / "summary.csv"
        if p.exists():
            with p.open(encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    verdicts[(s, r["pair"])] = r
    for d in docs:
        k = (d["set"], d["name"])
        d["status_wk"], d["status_mq"] = status.get(("wk",) + k), status.get(("mq",) + k)
        d["ms_wk"], d["ms_mq"] = median(times.get(("wk",) + k, [])), median(times.get(("mq",) + k, []))
        v = verdicts.get(k, {})
        d["verdict"] = v.get("verdict", "")
        d["level"] = v.get("level", "")
        d["first"] = v.get("first", "")
        d["differences"] = int(v["differences"]) if v.get("differences", "").isdigit() else None
        d["fonts_same"] = d["fonts_wk"] == d["fonts_mq"]
        d["note"] = notes.get(k, "")
        # every difference compare found, the content ones first, then appearance, then the file's
        pj = work / "compare" / d["set"] / "pairs" / f"{d['name']}.json"
        diffs = []
        if pj.exists():
            try:
                diffs = json.loads(pj.read_text(encoding="utf-8")).get("differences", [])
            except ValueError:
                diffs = []
        order = {"content": 0, "appearance": 1, "file": 2}
        diffs.sort(key=lambda x: order.get(x.get("of"), 3))
        d["notes"] = [dict(of=x.get("of", ""), kind=x.get("kind", ""), level=x.get("level", ""), note=x.get("note", "")) for x in diffs]
        d["pictures"] = sorted((p.name for p in (work / "compare" / d["set"] / "pairs").glob(f"{d['name']}.page-*.png")),
                               key=lambda x: int(re.sub(r"\D", "", x.rsplit(".page-", 1)[-1]) or 0))
        for key in ("score", "text", "geom", "looks"):
            d[key] = round(d[key], 6)

    # each set: its parity, its spread, compare's verdicts, its time through each program
    set_times = {}
    for label in sorted(set(meta["label_of"].values())):
        for who, run_, s, us in read_tsv(work / "times" / f"{label}-sets.tsv"):
            set_times.setdefault((s, run_), {})[who] = int(us)
    summary = {}
    for s in sets:
        ds = [d for d in docs if d["set"] == s]
        if not ds:
            continue
        sc = [d["score"] for d in ds]
        vc = {}
        for d in ds:
            w = verdict_word(d["verdict"])
            vc[w] = vc.get(w, 0) + 1
        runs = [(r, t) for (s2, r), t in set_times.items() if s2 == s and r.isdigit() and "wk" in t and "mq" in t]
        ratios = [t["wk"] / t["mq"] for _, t in runs if t["mq"] > 0]
        summary[s] = dict(
            title=sets_info.get(s, {}).get("title", s), published=sets_info.get(s, {}).get("published", False),
            image=sets_info.get(s, {}).get("image", "reference"),
            documents=len(ds), parity=round(sum(sc) / len(sc), 6), lowest=round(min(sc), 6),
            looks=round(sum(d["looks"] for d in ds) / len(ds), 6), looks_lowest=round(min(d["looks"] for d in ds), 6),
            at_least_099=sum(1 for x in sc if x >= 0.99), below_090=sum(1 for x in sc if x < 0.9),
            verdicts=vc, pdfs_wk=sum(1 for d in ds if d["made_wk"]), pdfs_mq=sum(1 for d in ds if d["made_mq"]),
            fonts_differ=sum(1 for d in ds if not d["fonts_same"]),
            bytes_wk=sum(d["size_wk"] for d in ds), bytes_mq=sum(d["size_mq"] for d in ds),
            seconds_wk=[round(t["wk"] / 1e6, 3) for _, t in sorted(runs)], seconds_mq=[round(t["mq"] / 1e6, 3) for _, t in sorted(runs)],
            speed=round(median(ratios), 2) if ratios else None,
        )
        nw = set_times.get((s, "nowait"), {})
        if "wk" in nw and "mq" in nw and nw["mq"] > 0:
            summary[s]["nowait"] = dict(seconds_wk=round(nw["wk"] / 1e6, 3), seconds_mq=round(nw["mq"] / 1e6, 3), speed=round(nw["wk"] / nw["mq"], 2))

    # the published documents together (print and everyday): the figures marqius.com states
    pub = [s for s in sets if summary.get(s, {}).get("published")]
    headline = None
    if pub:
        ds = [d for d in docs if d["set"] in pub]
        sc = [d["score"] for d in ds]
        per_run = {}
        for (s, r), t in set_times.items():
            if s in pub and r.isdigit() and "wk" in t and "mq" in t:
                a = per_run.setdefault(r, [0, 0, 0])
                a[0] += t["wk"]
                a[1] += t["mq"]
                a[2] += 1
        ratios = [a[0] / a[1] for a in per_run.values() if a[2] == len(pub) and a[1] > 0]
        nwk = sum(summary[s].get("nowait", {}).get("seconds_wk", 0) for s in pub)
        nmq = sum(summary[s].get("nowait", {}).get("seconds_mq", 0) for s in pub)
        headline = dict(sets=pub, documents=len(ds), parity=round(sum(sc) / len(sc), 6), looks=round(sum(d["looks"] for d in ds) / len(ds), 6),
                        by_set={s: summary[s]["parity"] for s in pub},
                        speed=round(median(ratios), 2) if ratios else None, speed_runs=[round(x, 2) for x in sorted(ratios)],
                        seconds_wk=round(median([a[0] / 1e6 for a in per_run.values() if a[2] == len(pub)]) or 0, 3) if ratios else None,
                        seconds_mq=round(median([a[1] / 1e6 for a in per_run.values() if a[2] == len(pub)]) or 0, 3) if ratios else None,
                        nowait_speed=round(nwk / nmq, 2) if nmq else None)

    env = {}
    for p in sorted((work / "env").glob("*.tsv")):
        env[p.stem] = {r[0]: (r[1] if len(r) > 1 else "") for r in read_tsv(p)}
    families = {}
    for p in sorted((work / "env").glob("*-families.txt")):
        families[p.name[: -len("-families.txt")]] = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    tools = {"pdftotext": (run(["pdftotext", "-v"]).stderr.splitlines() or [""])[0], "python": sys.version.split()[0]}
    # the version the program gives (marqius-wkhtmltopdf 0.12.3), not the tag it came under
    v = env.get(meta["first_label"], {}).get("mq_version", "")
    if v:
        meta["marqius"]["version"] = v.split()[-1]

    report = dict(suite=meta.get("suite", {}), when=meta.get("when"), meta=meta, tools=tools, env=env, families=families,
                  headline=headline, sets=summary, documents=docs)
    (work / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    with (work / "scores.csv").open("w", newline="", encoding="utf-8") as f:
        cols = ["set", "name", "score", "text", "geom", "pages_wk", "pages_mq", "looks", "verdict", "level", "first", "fonts_same",
                "size_wk", "size_mq", "status_wk", "status_mq", "ms_wk", "ms_mq"]
        w = csv.writer(f)
        w.writerow(cols)
        for d in docs:
            w.writerow([d[c] for c in cols])
    (work / "report.md").write_text(markdown(report), encoding="utf-8")
    (work / "report.html").write_text(html_report(report), encoding="utf-8")
    print(console(report))


# ---------------------------------------------------------------------------------------------
# what a reader sees

def fmt(x, n=4):
    return "" if x is None else f"{x:.{n}f}"


def doc_rows(report, s, limit=None):
    ds = [d for d in report["documents"] if d["set"] == s]
    ds.sort(key=lambda d: (d["score"], d["name"]))
    return ds[:limit] if limit else ds


def why(d):
    """compare's first difference, or what is wrong with the files"""
    if not d["made_wk"] and not d["made_mq"]:
        return "neither program made a PDF"
    if not d["made_mq"]:
        return "marqius-wkhtmltopdf made no PDF"
    if not d["made_wk"]:
        return "wkhtmltopdf made no PDF"
    if d["verdict"] in ("same", "file differs"):
        files = [x["note"] for x in d.get("notes", []) if x["of"] == "file"]
        return "the pages are the same" + (f" (the files differ: {'; '.join(files[:2])})" if files else "")
    seen = [x["note"] for x in d.get("notes", []) if x["of"] in ("content", "appearance")]
    if seen:
        return "; ".join(seen[:3]) + (f"; and {len(seen) - 3} more" if len(seen) > 3 else "")
    return d["first"]


def console(r):
    out = []
    m = r["meta"]
    out.append(f"marqius-wkhtmltopdf {m['marqius']['version']} ({m['marqius']['image']}) beside {r['env'].get(m['first_label'], {}).get('wk_version', 'wkhtmltopdf')}")
    out.append(f"{m['platform']}, {r['env'].get(m['first_label'], {}).get('cpus', '?')} cpus; scored with {r['tools']['pdftotext']}, Python {r['tools']['python']}")
    out.append("")
    out.append(f"  {'set':14s} {'docs':>4s} {'parity':>7s} {'lowest':>7s} {'looks':>6s}  {'same pages':>10s} {'appearance':>10s} {'content':>8s}  speed")
    for s, x in r["sets"].items():
        v = x["verdicts"]
        sp = f"{x['speed']:.0f}x" if x.get("speed") else ""
        out.append(f"  {s:14s} {x['documents']:4d} {x['parity']:7.4f} {x['lowest']:7.4f} {x['looks']:6.3f}  {v.get('same pages', 0):10d} {v.get('appearance only', 0):10d} {v.get('content differs', 0):8d}  {sp}")
    h = r.get("headline")
    if h:
        out.append("")
        out.append(f"  published documents ({' + '.join(h['sets'])}, {h['documents']}): parity {h['parity']:.4f}"
                   + (f"; {h['speed']:.0f}x faster (median of {len(h['speed_runs'])} runs)" if h.get("speed") else ""))
    low = sorted(r["documents"], key=lambda d: d["score"])[:5]
    if low and low[0]["score"] < 0.99:
        out.append("")
        out.append("  lowest scores:")
        for d in low:
            if d["score"] >= 0.99:
                break
            out.append(f"    {d['set']}/{d['name']}: {d['score']:.4f} (looks alike {d['looks']:.3f})  {why(d)[:80]}")
    return "\n".join(out)


def markdown(r):
    m = r["meta"]
    e = r["env"].get(m["first_label"], {})
    L = [f"# wkhtmltopdf parity report", "",
         f"marqius-wkhtmltopdf **{m['marqius']['version']}** beside **{e.get('wk_version', 'wkhtmltopdf 0.12.6')}**, "
         f"{m['when']}, on {m['platform']} ({e.get('cpus', '?')} cpus).", ""]
    h = r.get("headline")
    if h:
        L += [f"**The published documents ({' and '.join(h['sets'])}, {h['documents']} in all): parity {h['parity']:.4f}**"
              + (f", converted {h['speed']:.0f} times faster than wkhtmltopdf (median of {len(h['speed_runs'])} runs)." if h.get("speed") else "."), ""]
    L += ["| Set | Documents | Parity | Lowest | Looks alike | Same pages | Appearance only | Content differs | Fonts differ | Speed |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for s, x in r["sets"].items():
        v = x["verdicts"]
        L.append(f"| {x['title']} (`{s}`) | {x['documents']} | {x['parity']:.4f} | {x['lowest']:.4f} | {x['looks']:.3f} | {v.get('same pages', 0)} | "
                 f"{v.get('appearance only', 0)} | {v.get('content differs', 0)} | {x['fonts_differ']} | {(str(round(x['speed'])) + '×') if x.get('speed') else ''} |")
    L += ["", "Parity is the marqius engine's measure: 50% text, 30% word positions, 20% page count, from 0 to 1, read from the text in the PDFs. "
          "*Looks alike* is drawn from the pages themselves: the share of ink, at 72 dpi, that has ink from the other PDF within 2 points. "
          "The verdicts are `marqius-wkhtmltopdf compare`'s: *same pages* counts the pairs whose pages are the same "
          "(the files themselves may differ, as PDF 1.4 against 1.7 does), *appearance only* those where something moved "
          "or changed size or colour, *content differs* those where words, numbers or pictures differ.", ""]
    for s, x in r["sets"].items():
        L += [f"## {x['title']} (`{s}`)", "",
              "| Document | Score | Text | Positions | Pages | Looks alike | compare | First difference | Fonts | Size wk / mq | Time wk / mq |",
              "|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|"]
        for d in doc_rows(r, s):
            fonts = "same" if d["fonts_same"] else "differ"
            first = why(d).replace("|", "\\|")
            if d["note"]:
                first += f" — *{d['note']}*"
            L.append(f"| {d['name']} | {d['score']:.4f} | {d['text']:.3f} | {d['geom']:.3f} | {d['pages_wk']}/{d['pages_mq']} | {d['looks']:.3f} | "
                     f"{verdict_word(d['verdict'])} | {first} | {fonts} | {kb(d['size_wk'])} / {kb(d['size_mq'])} | "
                     f"{ms_text(d['ms_wk'])} / {ms_text(d['ms_mq'])} |")
        L.append("")
    L += ["## Speed", ""]
    for s, x in r["sets"].items():
        if x.get("seconds_wk"):
            L.append(f"- {s}: wkhtmltopdf {', '.join(f'{t:.2f}' for t in x['seconds_wk'])} s; marqius-wkhtmltopdf "
                     f"{', '.join(f'{t:.3f}' for t in x['seconds_mq'])} s" + (f"; {x['speed']:.1f}× (median)" if x.get("speed") else ""))
            if x.get("nowait"):
                n = x["nowait"]
                L.append(f"  - with wkhtmltopdf's 200 ms script wait off (`--javascript-delay 0`, for both): {n['seconds_wk']:.2f} s and {n['seconds_mq']:.3f} s, {n['speed']:.1f}×")
    L += ["", "Each set's wall time, one document after another, each program warmed up first. A document's time is the median of its runs, "
          "read from /proc/uptime (10 ms steps), as the published figures were.", "", "## What ran", ""]
    L += system_lines(r)
    return "\n".join(L) + "\n"


def system_lines(r):
    m = r["meta"]
    L = []
    for label, e in r["env"].items():
        L.append(f"- **{label}** pass: {e.get('wk_version', '')}; {e.get('mq_as_wkhtmltopdf', '')}; Alpine {e.get('alpine', '')}, {e.get('machine', '')}, "
                 f"{e.get('cpus', '')} cpus ({e.get('cpu', '') or 'model not given'}), {e.get('memory', '')}; "
                 f"{e.get('font_files', '')} font files, {len(r['families'].get(label, []))} families")
    for k, i in m["images"].items():
        L.append(f"- image `{k}`: `{i.get('name', '')}`" + (f", digest `{i['digest']}`" if i.get("digest") else "")
                 + (f", {i['size_mb']:.0f} MB unpacked" if i.get("size_mb") else ""))
    L.append(f"- marqius-wkhtmltopdf program: sha256 `{m['marqius'].get('sha256', '')}`, {m['marqius'].get('size_mb', 0):.1f} MB")
    L.append(f"- scorer: {r['tools']['pdftotext']}, Python {r['tools']['python']}")
    L.append(f"- suite: {m.get('suite', {}).get('commit', 'not a git checkout')}")
    if m.get("run_url"):
        L.append(f"- run: {m['run_url']}")
    return L


def html_report(r):
    m = r["meta"]
    e = r["env"].get(m["first_label"], {})
    esc = html.escape
    h = r.get("headline")
    rows = []
    for s, x in r["sets"].items():
        v = x["verdicts"]
        rows.append(f"<tr><td>{esc(x['title'])} <code>{esc(s)}</code></td><td>{x['documents']}</td><td><b>{x['parity']:.4f}</b></td><td>{x['lowest']:.4f}</td><td>{x['looks']:.3f}</td>"
                    f"<td>{v.get('same pages', 0)}</td><td>{v.get('appearance only', 0)}</td><td>{v.get('content differs', 0)}</td><td>{x['fonts_differ']}</td>"
                    f"<td>{(str(round(x['speed'])) + '×') if x.get('speed') else ''}</td></tr>")
    parts = []
    for s, x in r["sets"].items():
        trs = []
        for d in doc_rows(r, s):
            first = esc(why(d))
            if d["note"]:
                first += f"<br><i>{esc(d['note'])}</i>"
            pic_links = [f'<a href="compare/{esc(s)}/pairs/{esc(p)}">page {esc(p.rsplit(".page-", 1)[-1].replace(".png", ""))}</a>'
                         for p in d.get("pictures", [])]
            cls = "bad" if d["score"] < 0.9 else "warn" if d["score"] < 0.98 else ""
            trs.append(f"<tr class='{cls}'><td>{esc(d['name'])}</td><td><b>{d['score']:.4f}</b></td><td>{d['text']:.3f}</td><td>{d['geom']:.3f}</td>"
                       f"<td>{d['pages_wk']}/{d['pages_mq']}</td><td>{d['looks']:.3f}</td><td>{esc(verdict_word(d['verdict']))}</td><td>{first}</td>"
                       f"<td>{'same' if d['fonts_same'] else 'differ: ' + esc(', '.join(sorted(set(d['fonts_wk']) ^ set(d['fonts_mq']))))}</td>"
                       f"<td>{kb(d['size_wk'])} / {kb(d['size_mq'])}</td><td>{ms_text(d['ms_wk'])} / {ms_text(d['ms_mq'])}</td>"
                       f"<td>{' '.join(pic_links)}</td>"
                       f"<td><a href='pdf/wk/{esc(s)}/{esc(d['name'])}.pdf'>wk</a> <a href='pdf/mq/{esc(s)}/{esc(d['name'])}.pdf'>mq</a></td></tr>")
        parts.append(f"<h2>{esc(x['title'])} <code>{esc(s)}</code></h2><p>{x['documents']} documents, parity <b>{x['parity']:.4f}</b>, lowest {x['lowest']:.4f}.</p>"
                     "<table><tr><th>Document</th><th>Score</th><th>Text</th><th>Positions</th><th>Pages wk/mq</th><th>Looks alike</th><th>compare</th><th>First difference</th>"
                     "<th>Fonts</th><th>Size wk / mq</th><th>Time wk / mq</th><th>Pages that differ</th><th>PDFs</th></tr>" + "".join(trs) + "</table>")
    sysl = "".join(f"<li>{esc(re.sub(r'[*`]', '', x))}</li>" for x in system_lines(r))
    head = ""
    if h:
        head = (f"<p class='big'>Published documents ({esc(' and '.join(h['sets']))}, {h['documents']}): parity <b>{h['parity']:.4f}</b>"
                + (f", {h['speed']:.0f}× faster than wkhtmltopdf" if h.get("speed") else "") + "</p>")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>wkhtmltopdf parity report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ --fg: #1c2430; --muted: #5b6676; --line: #d9dee5; --bg: #fff; --head: #f3f5f8; --bad: #fde8e8; --warn: #fff6dc; --link: #1f5fbf }}
@media (prefers-color-scheme: dark) {{ :root {{ --fg: #e6e9ee; --muted: #9aa4b2; --line: #333b47; --bg: #14181e; --head: #1d232b; --bad: #3a1f22; --warn: #34301d; --link: #7fb0ff }} }}
body {{ font: 14px/1.45 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: var(--fg); background: var(--bg); margin: 24px auto; max-width: 1400px; padding: 0 16px }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 24px; font-size: 13px }} th, td {{ border-bottom: 1px solid var(--line); padding: 5px 8px; text-align: left; vertical-align: top }}
th {{ background: var(--head); position: sticky; top: 0 }} tr.bad td {{ background: var(--bad) }} tr.warn td {{ background: var(--warn) }}
.big {{ font-size: 18px }} .muted {{ color: var(--muted) }} a {{ color: var(--link) }} code {{ font-size: 12px }}
</style></head><body>
<h1>wkhtmltopdf parity report</h1>
<p>marqius-wkhtmltopdf <b>{esc(m['marqius']['version'])}</b> beside <b>{esc(e.get('wk_version', ''))}</b>, {esc(m['when'])}, on {esc(m['platform'])}.</p>
{head}
<table><tr><th>Set</th><th>Documents</th><th>Parity</th><th>Lowest</th><th>Looks alike</th><th>Same pages</th><th>Appearance only</th><th>Content differs</th><th>Fonts differ</th><th>Speed</th></tr>{''.join(rows)}</table>
<p class="muted">Parity: 50% text, 30% word positions, 20% page count (the marqius engine's measure, read from the text in the PDFs). Looks alike: the share of ink, at 72 dpi, with ink from the other PDF within 2 points. Verdicts: <code>marqius-wkhtmltopdf compare</code>; its full report, with both PDFs marked where they differ, is in <a href="compare/">compare/</a>. Rows in yellow score below 0.98, in red below 0.90.</p>
{''.join(parts)}
<h2>What ran</h2><ul>{sysl}</ul>
</body></html>
"""


if __name__ == "__main__":
    main()
