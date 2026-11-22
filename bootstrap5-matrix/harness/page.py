#!/usr/bin/env python3
"""Writes the judge's matrix onto this folder's README, between its results markers, so the page
shows the results it links.

    python3 harness/page.py [RESULTS [README]]

RESULTS is the folder judge.py filled (results/: results.json and RESULTS.md, and run.txt once
the publish job has filed it); README is the page to write (README.md). The run's address comes
from run.txt, or else from RUN_URL. The publish job runs this after filing each matrix; the
measure job runs it on a copy of the page, to check it before anything is filed.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RES = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "results"
README = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "README.md"
START = "<!-- results:start (written by harness/page.py from results/; edits here are overwritten) -->"
END = "<!-- results:end -->"
ROWS = [("same", "✓ As in Chrome"),
        ("appearance only", "✗ The same words, laid out or drawn differently"),
        ("content differs", "✗ Words missing, added or out of place")]


def main():
    data = json.loads((RES / "results.json").read_text(encoding="utf-8"))
    sets = data["sets"]
    names = list(sets)
    pages = data["pages"]

    # each set's verdicts, as the matrix shows them: a feature not in that Bootstrap is left out,
    # and a file that differs only as a file counts as the same (judge.py's SHORT)
    counts = {s: {v: 0 for v, _ in ROWS} for s in names}
    for pg in pages:
        for s in names:
            e = pg["results"][s]
            if e.get("na"):
                continue
            v = "same" if e["verdict"] == "file differs" else e["verdict"]
            counts[s][v] = counts[s].get(v, 0) + 1

    # the control page (plain CSS, no Bootstrap) must print the same everywhere for the rest to count
    off = [sets[s]["label"] for pg in pages if pg.get("bare") for s in names
           if not pg["results"][s].get("na") and pg["results"][s]["verdict"] not in ("same", "file differs")]

    # the matrix itself, as judge.py wrote it, with its pictures linked from this folder
    md = (RES / "RESULTS.md").read_text(encoding="utf-8").splitlines()
    at = next(i for i, line in enumerate(md) if line.startswith("| Feature |"))
    matrix = []
    for line in md[at:]:
        if not line.startswith("|"):
            break
        matrix.append(line.replace("](pictures/", "](results/pictures/"))

    run = ""
    if (RES / "run.txt").is_file():
        run = (RES / "run.txt").read_text(encoding="utf-8").strip()
    run = run or os.environ.get("RUN_URL", "")
    tools = data["tools"]
    where = "Measured on GitHub's machines (%s)" % ("[the run](%s)" % run if run else "this run")

    L = [START,
         "**%s beside %s, one Bootstrap 5 feature to a page.** %s, judged by `marqius-wkhtmltopdf compare` "
         "(%s)." % (tools["wkhtmltopdf"].split(" (")[0], tools["chrome"], where, tools["compare"]),
         "",
         "| How the pages print | " + " | ".join(sets[s]["label"] for s in names) + " |",
         "|---|" + "---:|" * len(names)]
    for v, label in ROWS:
        L.append("| %s | %s |" % (label, " | ".join(str(counts[s][v]) for s in names)))
    L.append("")
    if off:
        L.append("The control page, an invoice block in plain CSS with no Bootstrap, does not print the same in: "
                 "%s. Read those columns with care." % ", ".join(off))
    else:
        many = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}.get(len(names), str(len(names)))
        L.append("The control page, an invoice block in plain CSS with no Bootstrap, prints the same in all %s, "
                 "so each difference below comes from the CSS its page tests." % many)
    L += ["",
          "Each verdict links compare's picture of the page: Chrome on the left, wkhtmltopdf on the right, each "
          "difference marked. – means the feature is not in that Bootstrap. "
          "[Why each page differs](results/RESULTS.md#why-what-each-program-read): what each program computed.",
          ""]
    L += matrix
    L.append(END)
    block = "\n".join(L)

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit("%s has no %s ... %s" % (README, START, END))
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(head + block + tail, encoding="utf-8")
    print("wrote the matrix onto", README, "(%d features)" % len(pages))


if __name__ == "__main__":
    main()
