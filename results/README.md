# Results

Written by the workflow after each run on GitHub; [`harness/publish.py`](../harness/publish.py) files them.

- **`VERSION/PLATFORM/`** holds the latest run of one version of marqius-wkhtmltopdf on one platform (`linux-amd64`, `linux-arm64`):
  - `report.md` gives every document's scores and what differs;
  - `report.json` holds all of it, with the images' digests, the program's checksum, the system and its fonts;
  - `scores.csv` has one line a document;
  - `compare-SET.txt` is `marqius-wkhtmltopdf compare`'s summary of each set;
  - `pictures/` shows the pages that differ, wkhtmltopdf's beside marqius-wkhtmltopdf's, marked where they differ.
- **`history.tsv`** has one line for every run: when, the version, the image digest, each set's parity, the speed and the link to the run's log.

Earlier runs of a version are in the repository's history. To make any of these again on your own machine, run `./run.sh --tag VERSION`.
