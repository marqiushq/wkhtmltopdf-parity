#!/usr/bin/env python3
"""./run.sh share: send the summary of a run of your own templates to marqius, only if you say so.

What is sent is printed in full first, and nothing leaves the machine unless you type "yes" (or
give --yes). It holds the versions, the platform, how many documents there were, the scores of
each (in order of score, without names) and the kinds of difference compare found, such as
"moved" or "font". It never holds a document, a file name, a path, any text from the
documents or the values of your options (only their names, such as --margin-top). An e-mail
address and a note go with it only if you give them.

    python3 share.py WORK              (in the scorer container, with network only for this)

Settings: PARITY_SHARE_URL (where it goes), PARITY_SHARE_EMAIL, PARITY_SHARE_NOTE, PARITY_SHARE_YES=1,
PARITY_SUITE_REPO (owner/name, for the public alternative: a GitHub issue you open yourself).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = os.environ.get("PARITY_SHARE_URL") or "https://marqius.com/api/parity/share"
SCHEMA = "wkhtmltopdf-parity-share/1"


def option_names(work):
    """the names of the options the run used (convert.sh lists them), never their values"""
    names = set()
    opts = work / "options-used.txt"
    if opts.exists():
        for line in opts.read_text(encoding="utf-8").splitlines():
            if re.fullmatch(r"--?[A-Za-z][A-Za-z0-9-]*|cover|toc", line.strip()):
                names.add(line.strip())
    return sorted(names)


def payload(work):
    r = json.loads((work / "report.json").read_text(encoding="utf-8"))
    m, sets = r["meta"], r["sets"]
    e = r["env"].get(m.get("first_label", "main"), {})
    docs = sorted(r["documents"], key=lambda d: d["score"])
    allv = {}
    for x in sets.values():
        for k, v in x["verdicts"].items():
            allv[k] = allv.get(k, 0) + v
    n = len(docs)
    p = {
        "schema": SCHEMA,
        "suite": m.get("suite", {}).get("commit", ""),
        "marqius_wkhtmltopdf": m["marqius"]["version"],
        "image_digest": m.get("images", {}).get("marqius", {}).get("digest", ""),
        "wkhtmltopdf": e.get("wk_version", ""),
        "platform": m.get("platform", ""),
        "network": m.get("network", "none"),
        "cjk_fonts": any(k != "main" for k in r["env"]),
        "documents": n,
        "parity": round(sum(d["score"] for d in docs) / n, 4) if n else None,
        "overlay": round(sum(d["overlay"] for d in docs) / n, 3) if n else None,
        "lowest": round(docs[0]["score"], 4) if n else None,
        "verdicts": allv,
        "speed": next((x.get("speed") for x in sets.values() if x.get("speed")), None),
        "options": option_names(work),
        "each": [dict(score=round(d["score"], 4), overlay=round(d["overlay"], 3), verdict=d["verdict"],
                      pages=[d["pages_wk"], d["pages_mq"]], fonts_differ=not d["fonts_same"],
                      kinds=sorted({x["kind"] for x in d.get("notes", []) if x.get("kind") and x.get("of") != "file"}),
                      made=[d["made_wk"], d["made_mq"]])
                 for d in docs],
    }
    email = os.environ.get("PARITY_SHARE_EMAIL", "").strip()
    note = os.environ.get("PARITY_SHARE_NOTE", "").strip()
    if email:
        p["contact"] = email
    if note:
        p["note"] = note[:2000]
    return p


def main():
    work = Path(sys.argv[1])
    if not (work / "report.json").exists():
        sys.exit("share: no report here; run ./run.sh mine first")
    p = payload(work)
    body = json.dumps(p, indent=1, ensure_ascii=False)
    print("Everything that would be sent, and nothing else:\n")
    print(body)
    print(f"\nTo: {URL}")
    if os.environ.get("PARITY_SHARE_YES") != "1":
        if not sys.stdin.isatty():
            print("\nNothing was sent. To send it, run ./run.sh share --yes (or run it in a terminal and answer yes).")
            return 0
        try:
            answer = input("\nSend it? Type yes to send, anything else to stop: ")
        except (EOFError, KeyboardInterrupt):  # Ctrl-D or Ctrl-C at the prompt: a no
            answer = ""
            print()
        if answer.strip().lower() != "yes":
            print("Nothing was sent.")
            return 0
    req = urllib.request.Request(URL, data=body.encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "wkhtmltopdf-parity-suite"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            answer = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as ex:
        print(f"\nIt could not be sent ({ex}). Nothing was sent.")
        repo = os.environ.get("PARITY_SUITE_REPO", "")
        if repo:
            # an issue is public: it carries the summary only, never the contact or the note
            public = json.dumps({k: v for k, v in p.items() if k not in ("contact", "note")}, indent=1, ensure_ascii=False)
            q = urllib.parse.urlencode({"title": "Parity run: questions about the differences",
                                        "body": "```json\n" + public + "\n```\n"})
            print(f"You can share it in public instead, as a GitHub issue you open yourself (without your address):\nhttps://github.com/{repo}/issues/new?{q}")
        return 1
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (work / f"shared-{stamp}.json").write_text(json.dumps({"sent": p, "to": URL, "answer": answer}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    try:
        ref = json.loads(answer).get("reference", "")
    except ValueError:
        ref = ""
    print(f"\nSent{' (reference ' + ref + ')' if ref else ''}. A copy of what was sent is in shared-{stamp}.json beside the report.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
