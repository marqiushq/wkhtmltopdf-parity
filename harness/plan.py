#!/usr/bin/env python3
"""Which tags of marqius/wkhtmltopdf a CI run tests. Prints `tags=[...]` for $GITHUB_OUTPUT.

  schedule            every version tag (and latest) whose image digest no run on GitHub has tested
                      (results/history.tsv): a new release is tested within a day. On Mondays latest is
                      tested again even when nothing changed, so the proof is never older than a week.
  workflow_dispatch   the tags typed in (spaces between them), or what the schedule would pick
  push, pull_request  latest: the suite itself changed

Docker Hub is read anonymously (hub.docker.com's public tag list); nothing is sent but the request.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "marqius/wkhtmltopdf"
TAG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def hub_tags():
    url = f"https://hub.docker.com/v2/repositories/{REPO}/tags?page_size=100"
    out = {}
    while url:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "wkhtmltopdf-parity"}), timeout=30) as r:
            d = json.load(r)
        for t in d.get("results", []):
            out[t["name"]] = t.get("digest") or ""
        url = d.get("next")
    return out


def tested_digests(history):
    """digests a run on GitHub has tested (a local run, with no link to a log, does not count)"""
    seen = set()
    if history.exists():
        lines = history.read_text(encoding="utf-8").splitlines()
        cols = lines[0].split("\t") if lines else []
        for line in lines[1:]:
            row = dict(zip(cols, line.split("\t")))
            if row.get("digest") and row.get("run", "").startswith("https://"):
                seen.add(row["digest"])
    return seen


def main():
    event = os.environ.get("EVENT", "schedule")
    typed = os.environ.get("INPUT_TAGS", "").split()
    if event in ("push", "pull_request"):
        tags = ["latest"]
    elif typed:
        bad = [t for t in typed if not TAG.match(t)]
        if bad:
            sys.exit(f"not a Docker tag: {' '.join(bad)}")
        tags = typed
    else:
        hub = hub_tags()
        seen = tested_digests(Path(__file__).resolve().parents[1] / "results" / "history.tsv")
        versions = sorted((t for t in hub if VERSION.match(t)), key=lambda t: [int(x) for x in t.split(".")])
        tags, digests = [], set()
        for t in versions:
            if hub[t] and hub[t] not in seen:
                tags.append(t)
                digests.add(hub[t])
        monday = datetime.now(timezone.utc).weekday() == 0
        latest = hub.get("latest", "")
        if latest and latest not in digests and (latest not in seen or monday or event == "workflow_dispatch"):
            tags.append("latest")
    print("tags=" + json.dumps(tags))
    print(f"testing: {' '.join(tags) or 'nothing new'}", file=sys.stderr)


if __name__ == "__main__":
    main()
