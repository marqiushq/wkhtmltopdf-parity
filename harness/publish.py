#!/usr/bin/env python3
"""Files the reports of finished runs under results/ and rewrites the README's scoreboard.

    python3 harness/publish.py REPORTS... [--results results] [--readme README.md] [--tag TAG] [--issues FILE]

Each REPORTS folder holds a run's report.json (out/corpus after ./run.sh, or the artifacts CI
downloads: one folder for each run). For each run:

  results/VERSION/PLATFORM/      report.md, report.json, scores.csv, compare's summary of each
                                 set, and the pictures of the pages that differ most
  results/history.tsv            one line: when, the version, the tag, the image digest, the
                                 parity of each set, the speed, the run's log

Then the part of README.md between the scoreboard markers is written again from results/:
the latest version's scores, every version's, and every document below 0.99 with the reason,
marked where it comes out better from marqius-wkhtmltopdf (score.py decides that). A reason is a
note from corpus/notes.tsv while the document's result is the one the note was written for
(notes.py), else what compare found.

The part between the gaps markers lists the open tracking issues (label "known gap") with the
document each tracks. --issues is the GitHub API's list of those issues (the workflow downloads it);
they are kept in results/known-gaps.tsv, which is read when --issues is not given.
No version is written by hand: the latest run's is filled in. Only the standard library is used.
"""
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import notes as notes_file

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- scoreboard:start"
END = "<!-- scoreboard:end -->"
GAPS_START = "<!-- gaps:start"
GAPS_END = "<!-- gaps:end -->"
GAPS_COLS = ["number", "state", "document", "title", "url"]
HISTORY_COLS = ["when", "version", "tag", "platform", "digest", "print", "everyday", "published", "options",
                "international", "speed", "nowait_speed", "suite", "run"]
CANONICAL = "linux-amd64"  # the platform the scoreboard leads with: most servers, and the published figures'
MISS = 0.99  # documents below this are listed one by one, with the reason
# the mark beside a document that comes out better from marqius-wkhtmltopdf (score.py, better_than_wk), linked
# to how it is decided; nothing is shown beside the others
BADGE = "[![marqius better](.github/better.svg)](#the-measures)"
BADGE_ABOUT = ("marks a document where every difference goes marqius-wkhtmltopdf's way: its PDF has the page's own words where "
               "wkhtmltopdf's has garbled letters, look-alike characters, words split into letters or a picture of the words, and nothing "
               "else on the page looks different. Its score is lower only because the score measures how alike the two PDFs are. Each run decides it again, "
               "from the page itself.")
NOTES_ABOUT = ("Each reason was written for the result beside it, and each run checks that the result is still the same; where it is not, "
               "the reason given is what `compare` found.")


def platform_dir(p):
    return p.replace("/", "-")


def version_key(v):
    return [int(x) if x.isdigit() else x for x in re.split(r"[.-]", v)]


def file_run(folder, results, tag=None):
    r = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    m = r["meta"]
    version = m["marqius"]["version"]
    plat = platform_dir(m["platform"])
    dest = results / version / plat
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "pictures").mkdir(parents=True)
    for name in ("report.md", "report.json", "scores.csv"):
        shutil.copy2(folder / name, dest / name)
    for s in r["sets"]:
        summ = folder / "compare" / s / "summary.txt"
        if summ.exists():
            text = summ.read_text(encoding="utf-8").replace("/parity/work/", "")
            (dest / f"compare-{s}.txt").write_text(text, encoding="utf-8")
    # the pages that differ, for each document below the line or with content that differs: the
    # small copies score.py made, else compare's own
    for d in r["documents"]:
        if d.get("miss", d["score"] < MISS or d["verdict"] == "content differs"):
            for p in d.get("pictures", []):
                small = folder / "pictures" / f"{d['set']}--{p}"
                src = small if small.exists() else folder / "compare" / d["set"] / "pairs" / p
                if src.exists():
                    shutil.copy2(src, dest / "pictures" / f"{d['set']}--{p}")
    h = r.get("headline") or {}
    sets = r["sets"]
    row = {
        "when": m["when"], "version": version, "tag": tag or m["marqius"].get("tag", ""), "platform": m["platform"],
        "digest": m.get("images", {}).get("marqius", {}).get("digest", ""),
        "print": f"{sets['print']['parity']:.4f}" if "print" in sets else "",
        "everyday": f"{sets['everyday']['parity']:.4f}" if "everyday" in sets else "",
        "published": f"{h['parity']:.4f}" if h.get("parity") is not None else "",
        "options": f"{sets['options']['parity']:.4f}" if "options" in sets else "",
        "international": f"{sets['international']['parity']:.4f}" if "international" in sets else "",
        "speed": f"{h['speed']:.1f}" if h.get("speed") else "", "nowait_speed": f"{h['nowait_speed']:.1f}" if h.get("nowait_speed") else "",
        "suite": m.get("suite", {}).get("commit", ""), "run": m.get("run_url", ""),
    }
    hist = results / "history.tsv"
    if not hist.exists():
        hist.write_text("\t".join(HISTORY_COLS) + "\n", encoding="utf-8")
    with hist.open("a", encoding="utf-8") as f:
        f.write("\t".join(row[c] for c in HISTORY_COLS) + "\n")
    return version, plat


def latest_runs(results):
    """{version: {platform: report}} from the folders under results/"""
    out = {}
    for p in sorted(results.glob("*/*/report.json")):
        out.setdefault(p.parent.parent.name, {})[p.parent.name] = json.loads(p.read_text(encoding="utf-8"))
    return out


def when_text(iso):
    try:
        t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
        return f"{t.day} {t.strftime('%B %Y')}, {t.strftime('%H:%M')} UTC"
    except (TypeError, ValueError):
        return iso or ""


def where_text(r):
    m = r["meta"]
    e = r["env"].get(m.get("first_label", "main"), {})
    arch = {"linux/amd64": "x86-64", "linux/arm64": "ARM64"}.get(m["platform"], m["platform"])
    host = "GitHub Actions" if m.get("run_url") else "a local machine"
    return f"{host}, {arch}, {e.get('cpus', '?')} CPUs"


def wk_version(r):
    """wkhtmltopdf's version, as the run found it ('wkhtmltopdf 0.12.6 (with patched qt)' gives 0.12.6)"""
    e = r["env"].get(r["meta"].get("first_label", "main"), {})
    m = re.search(r"wkhtmltopdf (\S+)", e.get("wk_version", ""))
    return m.group(1) if m else "0.12.6"


def latest(runs):
    """the latest version and its run on the canonical platform"""
    v = sorted(runs, key=version_key, reverse=True)[0]
    plat = CANONICAL if CANONICAL in runs[v] else sorted(runs[v])[0]
    return v, plat, runs[v][plat]


def read_issues(path):
    """the tracking issues from the GitHub API's list: [{number, state, document, title, url}]"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("not a list")
    out = []
    for i in data:
        if not isinstance(i, dict) or "pull_request" in i or not i.get("number"):
            continue
        m = re.search(r"`corpus/([^`/\s]+/[^`/\s]+)`", i.get("body") or "")
        out.append({"number": str(i["number"]), "state": i.get("state", ""), "document": m.group(1) if m else "",
                    "title": " ".join((i.get("title") or "").split()), "url": i.get("html_url", "")})
    return sorted(out, key=lambda x: int(x["number"]))


def keep_issues(issues, path):
    path.write_text("\n".join(["\t".join(GAPS_COLS)] + ["\t".join(x[c] for c in GAPS_COLS) for x in issues]) + "\n", encoding="utf-8")


def kept_issues(path):
    if not path.exists():
        return None
    rows = [line.split("\t") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [dict(zip(GAPS_COLS, r)) for r in rows[1:]]


def md_text(t):
    """an issue's title as Markdown link text: code spans as they are, < > [ ] outside them escaped"""
    parts = t.split("`")
    for k in range(0, len(parts), 2):
        parts[k] = parts[k].replace("<", "&lt;").replace(">", "&gt;").replace("[", "\\[").replace("]", "\\]")
    return "`".join(parts)


def gaps(results, notes, issues):
    """the open tracking issues, each with the document it tracks; one whose document's result has changed
    since its note was written is marked to be checked again"""
    runs = latest_runs(results)
    if not runs:
        return "No results yet."
    v, _, r = latest(runs)
    docs = {f"{d['set']}/{d['name']}": d for d in r["documents"]}
    open_ = [x for x in issues if x["state"] == "open"]
    if not open_:
        L = [f"marqius-wkhtmltopdf **{v}**, the version on the scoreboard, has no difference with an open tracking issue."]
    else:
        L = [f"What marqius-wkhtmltopdf **{v}**, the version on the scoreboard, has yet to match. Each difference has a tracking issue, "
             "closed once the difference is gone: watch the one you care about.", ""]
        for x in open_:
            doc, d = x["document"], docs.get(x["document"])
            said = ""
            if d:
                note, others = notes_file.pick(notes, d)
                if not note and others:
                    checked = [n["checked"] for n in others if n["checked"]]
                    since = max(checked, key=version_key) if checked else ""
                    said = f": changed since {since}, to be checked again" if since else ": changed, to be checked again"
            L.append(f"- [{md_text(x['title'])}]({x['url']})" + (f" (`{doc}`{said})" if doc else ""))
    closed = [x for x in issues if x["state"] == "closed"]
    if closed:
        base = closed[0]["url"].rsplit("/issues/", 1)[0]
        L += ["", f"[Closed tracking issues]({base}/issues?q=label%3A%22known%20gap%22%20is%3Aclosed) are differences a later version removed."]
    return "\n".join(L)


def speed_cell(x):
    return f"{x:.0f}×" if x else "–"


def scoreboard(results, readme_dir, notes, issues):
    runs = latest_runs(results)
    if not runs:
        return "No results yet: the first run of the workflow writes them here."
    versions = sorted(runs, key=version_key, reverse=True)
    v, plat, r = latest(runs)
    m = r["meta"]
    rel = lambda p: p.relative_to(readme_dir).as_posix()
    folder = results / v / plat
    L = [f"**marqius-wkhtmltopdf {v}** beside **wkhtmltopdf {wk_version(r)}**, checked {when_text(m['when'])} on {where_text(r)}"
         + (f": [the run's log]({m['run_url']})" if m.get("run_url") else "")
         + f" · [full report]({rel(folder / 'report.md')}) · [every document]({rel(folder / 'scores.csv')})", ""]
    L += ["| What was converted | Documents | Parity | Overlay | Same pages | Appearance only | Content differs | Speed |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    sets = r["sets"]
    order = [s for s in ("everyday", "print") if s in sets] + [s for s in sets if s not in ("everyday", "print")]
    h = r.get("headline")
    for s in order:
        x = sets[s]
        vc = x["verdicts"]
        L.append(f"| {x['title']} (`{s}`) | {x['documents']} | {x['parity']:.4f} | {x.get('overlay', 0):.3f} | {vc.get('same pages', 0)} | {vc.get('appearance only', 0)} | "
                 f"{vc.get('content differs', 0)} | {speed_cell(x.get('speed'))} |")
        if h and s == order[1] and set(h["sets"]) == {"everyday", "print"}:
            tot = {k: sum(sets[t]["verdicts"].get(k, 0) for t in h["sets"]) for k in ("same pages", "appearance only", "content differs")}
            L.append(f"| **The {h['documents']} published documents together** | **{h['documents']}** | **{h['parity']:.4f}** | {h.get('overlay', 0):.3f} | {tot['same pages']} | "
                     f"{tot['appearance only']} | {tot['content differs']} | **{speed_cell(h.get('speed'))}** |")
    L.append("")
    if h and h.get("speed"):
        L.append(f"Speed is the time to convert the published documents one after another, wkhtmltopdf's divided by marqius-wkhtmltopdf's: "
                 f"{h['seconds_wk']:.1f} s against {h['seconds_mq']:.2f} s (median of {len(h['speed_runs'])} runs)"
                 + (f"; {h['nowait_speed']:.0f}× with wkhtmltopdf's 200 ms script wait turned off for both." if h.get("nowait_speed") else "."))
        L.append("")
    if h and h.get("bytes_wk"):
        imgs = m.get("images", {})
        L.append(f"Sizes: the {h['documents']} PDFs come to {h['bytes_wk'] / 1048576:.1f} MB from wkhtmltopdf and {h['bytes_mq'] / 1048576:.1f} MB from marqius-wkhtmltopdf."
                 + (f" The `{imgs['marqius']['name'].split(':')[0]}` image is {imgs['marqius']['size_mb']:.0f} MB unpacked; the image wkhtmltopdf runs in here, with its fonts, {imgs['reference']['size_mb']:.0f} MB."
                    if imgs.get("marqius", {}).get("size_mb") and imgs.get("reference", {}).get("size_mb") else ""))
        L.append("")
    others = [p for p in sorted(runs[v]) if p != plat]
    for p in others:
        o = runs[v][p]
        oh = o.get("headline") or {}
        same = all(abs(o["sets"].get(s, {}).get("parity", -1) - sets[s]["parity"]) < 0.00005 for s in sets)
        L.append(f"On {where_text(o)}: " + ("the same parity in every set" if same else
                 ", ".join(f"{s} {o['sets'][s]['parity']:.4f}" for s in order if s in o["sets"]))
                 + (f", {oh['speed']:.0f}× faster" if oh.get("speed") else "") + f" ([report]({rel(results / v / p / 'report.md')})).")
        L.append("")
    # every version
    L += ["#### Every version", "", "| Version | Checked | Business documents | CSS features | Published 86 | Options | Languages | Speed |",
          "|---|---|---:|---:|---:|---:|---:|---:|"]
    for ver in versions:
        pl = CANONICAL if CANONICAL in runs[ver] else sorted(runs[ver])[0]
        rr = runs[ver][pl]
        ss, hh = rr["sets"], rr.get("headline") or {}
        cell = lambda s: f"{ss[s]['parity']:.4f}" if s in ss else "–"
        L.append(f"| [{ver}]({rel(results / ver / pl / 'report.md')}) | {rr['meta']['when'][:10]} | {cell('everyday')} | {cell('print')} | "
                 f"{(format(hh['parity'], '.4f') if hh.get('parity') is not None else '–')} | {cell('options')} | {cell('international')} | {speed_cell(hh.get('speed'))} |")
    L.append("")
    # the misses, one by one: the reason a person checked, else what compare found
    misses = sorted((d for d in r["documents"] if d["score"] < MISS or d["verdict"] == "content differs"), key=lambda d: d["score"])
    if not misses:
        L.append(f"Every document scores {MISS} or more, and none differs in content.")
    else:
        better = sum(1 for d in misses if d.get("better"))
        L += ["<details>", f"<summary><b>The {len(misses)} documents below {MISS} or with different content, and why"
              + (f"; {better} of them come out better from marqius-wkhtmltopdf" if better else "") + "</b></summary>", ""]
        if better:
            L += [f"{BADGE} {BADGE_ABOUT}", ""]
        L += [NOTES_ABOUT, ""]
        tracked = {x["document"]: x for x in issues if x["state"] == "open" and x["document"]}
        L += ["| Document | Parity | Overlay | Why | Pages |", "|---|---:|---:|---|---|"]
        for d in misses:
            pics = " ".join(f"[{p.rsplit('.page-', 1)[-1].replace('.png', '')}]({rel(folder / 'pictures' / (d['set'] + '--' + p))})"
                            for p in d.get("pictures", []) if (folder / "pictures" / f"{d['set']}--{p}").exists())
            why, _ = notes_file.pick(notes, d)
            if not why:
                found = [x["note"] for x in d.get("notes", []) if x["of"] in ("content", "appearance")][:2]
                why = "compare: " + ("; ".join(found) or d.get("first", ""))
                if len(why) > 160:
                    why = why[:157].rstrip() + "…"
            why = why.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")  # (<script src>) is text, not a tag
            mark = f"<br>{BADGE}" if d.get("better") else ""
            gap = tracked.get(f"{d['set']}/{d['name']}")
            if gap:
                mark += f"<br>[tracking issue]({gap['url']})"
            L.append(f"| `{d['set']}/{d['name']}`{mark} | {d['score']:.4f} | {d.get('overlay', 0):.3f} | {why} | {pics} |")
        L += ["", "</details>"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reports", nargs="*", type=Path)
    ap.add_argument("--results", type=Path, default=ROOT / "results")
    ap.add_argument("--readme", type=Path, default=ROOT / "README.md")
    ap.add_argument("--tag", default=None)
    ap.add_argument("--notes", type=Path, default=ROOT / "corpus" / "notes.tsv")
    ap.add_argument("--issues", type=Path, default=None, help="the GitHub API's list of the tracking issues")
    a = ap.parse_args()
    a.results.mkdir(parents=True, exist_ok=True)
    found = []
    for folder in a.reports:
        # a run's folder holds meta.tsv beside report.json (compare's own files may be called report.json too)
        found += [p.parent for p in sorted(folder.glob("**/meta.tsv")) if (p.parent / "report.json").exists()]
    for f in found:
        v, p = file_run(f, a.results, a.tag)
        print(f"filed {f} as results/{v}/{p}")
    notes = notes_file.read(a.notes)
    kept = a.results / "known-gaps.tsv"
    issues = None
    if a.issues and a.issues.exists():
        try:
            issues = read_issues(a.issues)
        except (ValueError, TypeError, KeyError) as e:
            print(f"{a.issues} is not a list of issues ({e}); using {kept}")
    if issues is not None:
        keep_issues(issues, kept)
    else:
        issues = kept_issues(kept) or []
    text = a.readme.read_text(encoding="utf-8")
    text = between(text, START, END, scoreboard(a.results, a.readme.parent, notes, issues), a.readme)
    if GAPS_START in text:
        text = between(text, GAPS_START, GAPS_END, gaps(a.results, notes, issues), a.readme)
    a.readme.write_text(text, encoding="utf-8")
    print(f"scoreboard written to {a.readme}")
    runs = latest_runs(a.results)
    if runs:
        _, _, r = latest(runs)
        due = [notes_file.due_text(d, others) for d in r["documents"] for note, others in [notes_file.pick(notes, d)] if not note and others]
        if due:
            print("notes to check again (compare's finding is shown instead):\n  " + "\n  ".join(due))


def between(text, start, end, body, where):
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0:
        raise SystemExit(f"{where} has no {start} ... {end} markers")
    return text[: text.index("-->", i) + 3] + "\n" + body + "\n" + text[j:]


if __name__ == "__main__":
    main()
