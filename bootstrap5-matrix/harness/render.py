"""Prints every test page with wkhtmltopdf as Odoo calls it, and with Chrome at the same page scale;
then compare (marqius-wkhtmltopdf's PDF comparison) sets each wkhtmltopdf PDF against Chrome's.

    python3 harness/render.py SITE OUT COMPARE_BINARY

Pages are served from SITE on 127.0.0.1 only: nothing is fetched from the network."""
import concurrent.futures as cf
import functools
import http.server
import json
import os
import pathlib
import subprocess
import sys
import threading
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from chrome import Chrome  # noqa: E402

SITE, OUT, COMPARE = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
PORT = 8123
BASE = "http://127.0.0.1:%d/" % PORT
CHROME_EXE = "/usr/bin/google-chrome"
WORKERS = max(2, os.cpu_count() or 2)

# Odoo's own command line (ir.actions.report._build_wkhtmltopdf_args) for its default A4 paper
# format: --dpi 90 and --zoom 96/90, margins left and right 0. Top and bottom are 10 mm instead
# of the room Odoo keeps for its header and footer, as these pages have neither.
WKHTMLTOPDF = ["wkhtmltopdf", "--disable-local-file-access", "--quiet", "--page-size", "A4",
               "--margin-top", "10", "--dpi", "90", "--zoom", str(96.0 / 90), "--margin-left", "0",
               "--margin-bottom", "10", "--margin-right", "0", "--orientation", "Portrait",
               "--javascript-delay", "1000"]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run(cmd, timeout=180):
    t = time.time()
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), round(time.time() - t, 2)
    except subprocess.TimeoutExpired:
        return "timeout", "", "", round(time.time() - t, 2)


def pdfinfo(pdf):
    info = {}
    if pdf.exists() and pdf.stat().st_size:
        out = subprocess.run(["pdfinfo", "-enc", "UTF-8", str(pdf)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
        for line in out.decode("utf-8", "replace").splitlines():
            k, _, v = line.partition(":")
            info[k.strip()] = v.strip()
    return info


def probe_of(title):
    if title.startswith("PROBE "):
        try:
            return json.loads(title[6:]), ""
        except ValueError as e:
            return None, "measurements not readable: %s" % e
    return None, "no measurements in the title: %r" % title[:100]


def wk(job):
    s, slug = job
    pdf = OUT / "pdf" / s / "wkhtmltopdf" / (slug + ".pdf")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    rc, _, err, secs = run(WKHTMLTOPDF + [BASE + "pages/%s/%s.html" % (s, slug), str(pdf)])
    info = pdfinfo(pdf)
    probe, note = probe_of(info.get("Title", ""))
    return job, dict(status=rc, seconds=secs, stderr=err.strip()[-600:], pages=int(info.get("Pages", 0) or 0), probe=probe, note=note)


def scale_of(pdf):
    """the scale wkhtmltopdf printed calibrate.html at: CALB stands 600 CSS px right of CALA, CALC 600 below"""
    rc, out, err, _ = run([COMPARE, "compare", "--words", str(pdf)])
    pos = {}
    for line in out.splitlines():
        f = line.split("\t")
        if len(f) == 6 and f[5] in ("CALA", "CALB", "CALC"):
            pos[f[5]] = (float(f[1]), float(f[2]))
    across = (pos["CALB"][0] - pos["CALA"][0]) / 450.0  # 600 CSS px are 450 pt at scale 1
    down = (pos["CALC"][1] - pos["CALA"][1]) / 450.0
    return across, down


def chrome_share(jobs, scale, n):
    # the window as wide as the printed page's layout, so scripts and media queries see what print sees
    c = Chrome(CHROME_EXE, "/tmp/chrome-profile-%d" % n, width=int(round(210 / 25.4 * 96 / scale)))
    done = {}
    try:
        for s, slug in jobs:
            pdf = OUT / "pdf" / s / "chromium" / (slug + ".pdf")
            pdf.parent.mkdir(parents=True, exist_ok=True)
            t = time.time()
            try:
                title = c.pdf(BASE + "pages/%s/%s.html" % (s, slug), str(pdf), scale)
                probe, note = probe_of(title)
                status = 0
            except Exception as e:  # noqa: the page is reported, the run goes on
                probe, note, status = None, "chrome: %s" % e, 1
            done[(s, slug)] = dict(status=status, seconds=round(time.time() - t, 2), pages=int(pdfinfo(pdf).get("Pages", 0) or 0),
                                   probe=probe, note=note)
    finally:
        c.close()
    return done


def version(cmd):
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode().strip().splitlines()[0]
    except Exception as e:  # noqa
        return "unknown (%s)" % e


def main():
    meta = json.loads((SITE / "pages.json").read_text())
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Quiet, directory=str(SITE)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    cal = OUT / "calibrate.pdf"
    OUT.mkdir(parents=True, exist_ok=True)
    run(WKHTMLTOPDF + [BASE + "calibrate.html", str(cal)])
    across, down = scale_of(cal)
    scale = round(across, 5)
    print("wkhtmltopdf prints a CSS pixel at %.5f of Chrome's size across, %.5f down: Chrome prints at %.5f" % (across, down, scale))

    jobs = [(s, p["slug"]) for s in meta["sets"] for p in meta["pages"]]
    results = {"%s/%s" % j: {} for j in jobs}
    t = time.time()
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for (s, slug), r in ex.map(wk, jobs):
            results["%s/%s" % (s, slug)]["wkhtmltopdf"] = r
    print("wkhtmltopdf: %d pages in %.0f s" % (len(jobs), time.time() - t))

    t = time.time()
    shares = [jobs[i::WORKERS] for i in range(WORKERS)]
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for done in ex.map(chrome_share, shares, [scale] * WORKERS, range(WORKERS)):
            for (s, slug), r in done.items():
                results["%s/%s" % (s, slug)]["chromium"] = r
    print("Chrome: %d pages in %.0f s" % (len(jobs), time.time() - t))

    compared = {}
    for s in meta["sets"]:
        d = OUT / "compare" / s
        rc, _, err, secs = run([COMPARE, "compare", str(OUT / "pdf" / s / "chromium"), str(OUT / "pdf" / s / "wkhtmltopdf"),
                                "-o", str(d), "--ignore-kind", "metadata", "--ignore-kind", "pdf-type", "--move", "2", "--pictures", "all", "--marked", "differing",
                                "--quiet"], timeout=1800)
        compared[s] = dict(status=rc, seconds=secs, stderr=err.strip()[-600:])
        print("compare %s: status %s, %s s" % (s, rc, secs))
    tools = dict(wkhtmltopdf=version(["wkhtmltopdf", "--version"]), chrome=version([CHROME_EXE, "--version"]),
                 compare=version([COMPARE, "--version"]), poppler=version(["pdfinfo", "-v"]))
    (OUT / "render.json").write_text(json.dumps(dict(tools=tools, scale=dict(across=across, down=down, chrome=scale),
                                                     wkhtmltopdf_args=WKHTMLTOPDF, results=results, compare=compared), indent=1))
    for k, v in tools.items():
        print("%s: %s" % (k, v))


if __name__ == "__main__":
    main()
