"""Builds the test pages: every page in features/ once for each stylesheet in SETS.

    python3 harness/build.py SITE

SITE gets pages/<set>/<page>.html and pages.json; the stylesheets themselves are put in SITE by
fetch.sh (Bootstrap, from Odoo's own source tree) and odoo.sh (Odoo's compiled report CSS)."""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# The stylesheets a report can get. Bootstrap alone, at the two versions Odoo ships, and Odoo's own
# report CSS as each Odoo server compiles it for PDFs (web.report_assets_pdf, then
# web.report_assets_common), inside the page structure of Odoo's PDF layout (web.minimal_layout and
# the standard external layout).
SETS = {
    "bootstrap-5.1.3": dict(bootstrap="5.1.3", label="Bootstrap 5.1.3 alone", note="the Bootstrap of Odoo 16 and 17"),
    "bootstrap-5.3.3": dict(bootstrap="5.3.3", label="Bootstrap 5.3.3 alone", note="the Bootstrap of Odoo 18, 19 and 20"),
    "odoo-17.0": dict(bootstrap="5.1.3", odoo="17.0", label="Odoo 17 report CSS"),
    "odoo-18.0": dict(bootstrap="5.3.3", odoo="18.0", label="Odoo 18 report CSS"),
    "odoo-19.0": dict(bootstrap="5.3.3", odoo="19.0", label="Odoo 19 report CSS"),
    "odoo-20.0": dict(bootstrap="5.3.3", odoo="20.0", label="Odoo 20 report CSS"),
}

BOOTSTRAP_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../../css/bootstrap-{bootstrap}.css">
{base}<link rel="stylesheet" href="../../harness/markers.css">
</head>
<body>
<div id="frame" style="padding: 0 40px">
{fragment}
</div>
{checks}
<script src="../../harness/probe.js"></script>
</body>
</html>
"""

# web.minimal_layout: Odoo 17 gives the body class "container"; 18 and later "o_body_pdf o_css_margins
# container overflow-hidden". The article carries the standard layout's classes.
BARE_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../../harness/markers.css">
</head>
<body>
<div id="frame" style="padding: 0 40px">
{fragment}
</div>
{checks}
<script src="../../harness/probe.js"></script>
</body>
</html>
"""

# Where wkhtmltopdf puts three words, in CSS pixels, to measure the scale it prints at.
CALIBRATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>calibrate</title>
<link rel="stylesheet" href="harness/markers.css"></head><body>
<div style="position: absolute; left: 0; top: 0">CALA</div>
<div style="position: absolute; left: 600px; top: 0">CALB</div>
<div style="position: absolute; left: 0; top: 600px">CALC</div>
</body></html>
"""

ODOO_PAGE = """<!DOCTYPE html>
<html style="height: 0;">
<head>
<link rel="stylesheet" href="../../odoo/{odoo}/report_assets_pdf.css">
<link rel="stylesheet" href="../../odoo/{odoo}/report_assets_common.css">
<link rel="stylesheet" href="../../harness/markers.css">
<meta charset="utf-8">
<title>{title}</title>
</head>
<body class="{body_class}"{body_style}>
<div class="{article_class}"><div class="page"><div id="frame">
{fragment}
</div></div></div>
{checks}
<script src="../../harness/probe.js"></script>
</body>
</html>
"""


def read_feature(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"<!--\s*(\{.*?\})\s*-->\s*", text, re.S)
    meta = json.loads(m.group(1))
    rest = text[m.end():]
    c = re.search(r'<script type="text/x-checks" id="checks">(.*?)</script>', rest, re.S)
    checks = json.loads(c.group(1))
    fragment = (rest[:c.start()] + rest[c.end():]).strip()
    return meta, fragment, checks, c.group(0)


def main(site):
    site = pathlib.Path(site)
    pages = []
    found = [p for p in (ROOT / "features").glob("*.html") if not p.name.startswith(".")]
    for path in sorted(found, key=lambda p: int(p.stem.split("-")[0])):
        meta, fragment, checks, checks_html = read_feature(path)
        pages.append(dict(slug=path.stem, group=meta["group"], title=meta["title"], checks=checks,
                          bare=bool(meta.get("bare")), since=meta.get("since"), judge=meta.get("judge", "compare")))
        for name, s in SETS.items():
            out = site / "pages" / name / (path.stem + ".html")
            out.parent.mkdir(parents=True, exist_ok=True)
            title = html.escape(meta["title"])
            if meta.get("bare"):
                text = BARE_PAGE.format(title=title, fragment=fragment, checks=checks_html)
            elif "odoo" in s:
                v = s["odoo"]
                old = v == "17.0"
                text = ODOO_PAGE.format(
                    odoo=v, title=title, fragment=fragment, checks=checks_html,
                    body_class="container" if old else "o_body_pdf o_css_margins container overflow-hidden",
                    body_style=' style="overflow:hidden"' if old else "",
                    article_class="article o_report_layout_standard o_company_1_layout" if old
                    else "article o_report_layout_standard o_table_standard o_company_1_layout")
            else:
                base = '' if meta.get("base") is False else '<link rel="stylesheet" href="../../harness/base.css">\n'
                text = BOOTSTRAP_PAGE.format(bootstrap=s["bootstrap"], base=base, title=title, fragment=fragment, checks=checks_html)
            out.write_text(text, encoding="utf-8")
    (site / "calibrate.html").write_text(CALIBRATE, encoding="utf-8")
    (site / "pages.json").write_text(json.dumps(dict(sets=SETS, pages=pages), indent=1), encoding="utf-8")
    print("%d pages x %d stylesheets, %d checks each set" % (len(pages), len(SETS), sum(len(p["checks"]) for p in pages)))


if __name__ == "__main__":
    main(sys.argv[1])
