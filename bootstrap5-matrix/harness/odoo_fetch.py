"""Fetches Odoo's report CSS for PDFs from a running Odoo server, as web.minimal_layout links it,
with the files its url() rules name (fonts) kept beside it so the pages work without the server.

    python3 harness/odoo_fetch.py BASE_URL SUFFIX OUTDIR

SUFFIX is "" for Odoo 17 and 18 (which always add -webkit- prefixes) and ".autoprefixed" for 19
and later (where web.minimal_layout asks for them with t-autoprefix)."""
import pathlib, re, sys, time, urllib.request

base, sfx, out = sys.argv[1].rstrip("/"), sys.argv[2], pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)


def get(url, tries=90, wait=2):
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=600) as r:
                return r.read()
        except Exception as e:  # the server may still be starting
            last = e
            time.sleep(wait)
    raise SystemExit("could not fetch %s: %s" % (url, last))


get(base + "/web/login")
URL = re.compile(r"""url\(\s*(['"]?)(/[^/'")][^'")]*)\1\s*\)""")
for bundle in ("report_assets_pdf", "report_assets_common"):
    css = get("%s/web/assets/any/web.%s%s.min.css" % (base, bundle, sfx)).decode("utf-8")
    kept = {}

    def local(m):
        q, path = m.group(1), m.group(2)
        clean = re.split(r"[?#]", path)[0]
        if clean not in kept:
            dest = out / "assets" / clean.lstrip("/")
            try:
                if not dest.exists():
                    data = get(base + clean, tries=3)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
                kept[clean] = True
            except SystemExit:
                kept[clean] = False
        if not kept[clean]:
            return m.group(0)
        return "url(%sassets%s%s)" % (q, path, q)

    css = URL.sub(local, css)
    (out / (bundle + ".css")).write_text(css, encoding="utf-8")
    print("%s%s: %d bytes, %d files kept beside it, %d not found" % (
        bundle, sfx, len(css), sum(kept.values()), sum(1 for v in kept.values() if not v)))
