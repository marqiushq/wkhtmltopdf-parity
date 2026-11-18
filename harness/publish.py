#!/usr/bin/env python3
"""Files the reports of finished runs under results/ and rewrites the README's scoreboard.

    python3 harness/publish.py REPORTS... [--results results] [--readme README.md] [--tag TAG]

Each REPORTS folder holds a run's report.json (out/corpus after ./run.sh, or the artifacts CI
downloads: one folder for each run). For each run:

  results/VERSION/PLATFORM/      report.md, report.json, scores.csv, compare's summary of each
                                 set, and the pictures of the pages that differ most
  results/history.tsv            one line: when, the version, the tag, the image digest, the
                                 parity of each set, the speed, the run's log

Then the part of README.md between the scoreboard markers is written again from results/:
the latest version's scores, every version's, and every document below 0.99 with the reason.
Only the standard library is used.
"""
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- scoreboard:start"
END = "<!-- scoreboard:end -->"
HISTORY_COLS = ["when", "version", "tag", "platform", "digest", "print", "everyday", "published", "options",
                "international", "speed", "nowait_speed", "suite", "run"]
CANONICAL = "linux-amd64"  # the platform the scoreboard leads with: most servers, and the published figures'
MISS = 0.99  # documents below this are listed one by one, with the reason


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


def speed_cell(x):
    return f"{x:.0f}×" if x else "–"


def scoreboard(results, readme_dir):
    runs = latest_runs(results)
    if not runs:
        return "No results yet: the first run of the workflow writes them here."
    versions = sorted(runs, key=version_key, reverse=True)
    v = versions[0]
    plat = CANONICAL if CANONICAL in runs[v] else sorted(runs[v])[0]
    r = runs[v][plat]
    m = r["meta"]
    rel = lambda p: p.relative_to(readme_dir).as_posix()
    folder = results / v / plat
    L = [f"**marqius-wkhtmltopdf {v}** beside **wkhtmltopdf 0.12.6**, checked {when_text(m['when'])} on {where_text(r)}"
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
        L += ["<details>", f"<summary><b>The {len(misses)} documents below {MISS} or with different content, and why</b></summary>", "",
              "| Document | Parity | Overlay | Why | Pages |", "|---|---:|---:|---|---|"]
        for d in misses:
            pics = " ".join(f"[{p.rsplit('.page-', 1)[-1].replace('.png', '')}]({rel(folder / 'pictures' / (d['set'] + '--' + p))})"
                            for p in d.get("pictures", []) if (folder / "pictures" / f"{d['set']}--{p}").exists())
            why = d.get("note", "")
            if not why:
                found = [x["note"] for x in d.get("notes", []) if x["of"] in ("content", "appearance")][:2]
                why = "compare: " + ("; ".join(found) or d.get("first", ""))
                if len(why) > 160:
                    why = why[:157].rstrip() + "…"
            why = why.replace("|", "\\|")
            L.append(f"| `{d['set']}/{d['name']}` | {d['score']:.4f} | {d.get('overlay', 0):.3f} | {why} | {pics} |")
        L += ["", "</details>"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reports", nargs="*", type=Path)
    ap.add_argument("--results", type=Path, default=ROOT / "results")
    ap.add_argument("--readme", type=Path, default=ROOT / "README.md")
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()
    a.results.mkdir(parents=True, exist_ok=True)
    found = []
    for folder in a.reports:
        # a run's folder holds meta.tsv beside report.json (compare's own files may be called report.json too)
        found += [p.parent for p in sorted(folder.glob("**/meta.tsv")) if (p.parent / "report.json").exists()]
    for f in found:
        v, p = file_run(f, a.results, a.tag)
        print(f"filed {f} as results/{v}/{p}")
    text = a.readme.read_text(encoding="utf-8")
    i, j = text.find(START), text.find(END)
    if i < 0 or j < 0:
        raise SystemExit(f"{a.readme} has no scoreboard markers")
    head = text[: text.index("-->", i) + 3]
    new = head + "\n" + scoreboard(a.results, a.readme.parent) + "\n" + text[j:]
    a.readme.write_text(new, encoding="utf-8")
    print(f"scoreboard written to {a.readme}")


if __name__ == "__main__":
    main()
