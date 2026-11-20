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
names, file sizes, exit statuses and times, and marks the documents that come out better from
marqius-wkhtmltopdf than from wkhtmltopdf (better_than_wk, below).

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
import unicodedata
from concurrent.futures import ProcessPoolExecutor
from html.parser import HTMLParser
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
# The overlay: how the pages look, apart from what their text says: each page drawn in grey at 72 dpi (a dot is
# a point), every dot darker than INK is ink, and a dot of ink is matched when the other PDF has
# ink within NEAR points of it. overlay = matched ink of both / all ink of both; a page only one PDF
# has counts as unmatched. Words that moved by a point or two still match; reversed or missing
# letters, missing pictures and text set elsewhere do not.
DPI, INK, NEAR = 72, 160, 2
INK_BITS = bytes.maketrans(bytes(range(256)), bytes(ord("1") if v < INK else ord("0") for v in range(256)))


def bitmaps(pdf, tmp):
    """each page as a list of rows, each row an integer whose set bits are the ink (the leftmost dot
    the highest bit), and each page's width in dots"""
    base = Path(tmp) / Path(pdf).stem
    subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", str(pdf), str(base)], capture_output=True, timeout=300)
    pages_, widths = [], []
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
        widths.append(w)
        f.unlink()
    return pages_, widths


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


def drawn(rp, mp):
    """both PDFs' pages as ink, each with its pages' widths (bitmaps); None when a PDF is missing"""
    import tempfile
    if not pdf_ok(rp) or not pdf_ok(mp):
        return None
    with tempfile.TemporaryDirectory() as t:
        ta, tb = Path(t) / "a", Path(t) / "b"
        ta.mkdir()
        tb.mkdir()
        return bitmaps(rp, ta), bitmaps(mp, tb)


def overlay_of(both):
    """the overlay of the two PDFs' pages, as drawn() gives them"""
    if not both:
        return 0.0
    (A, _), (B, _) = both
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


# ---------------------------------------------------------------------------------------------
# marqius better: a document where every difference compare finds goes marqius-wkhtmltopdf's
# way, judged against the page itself, and nothing else on the page looks different. It is decided
# again on every run, so the mark goes as soon as it stops being true. A difference goes
# marqius-wkhtmltopdf's way when it is one of these:
#
#   text             marqius-wkhtmltopdf's words are the page's own and wkhtmltopdf's are not, and
#                    either the two look the same there (wkhtmltopdf's text behind the letters is
#                    wrong: look-alike characters, marks split off) or wkhtmltopdf's are the page's
#                    own words misread as Windows-1252 (a page that names no character set)
#   added            words that only marqius-wkhtmltopdf's PDF holds as text, which are the page's
#                    own and which wkhtmltopdf drew in the same place all the same (as a picture)
#   picture-missing  a picture of wkhtmltopdf's that marqius-wkhtmltopdf draws the same, as text or
#                    shapes
#   unreadable       letters drawn with no text behind them, in wkhtmltopdf's PDF only, which
#                    marqius-wkhtmltopdf draws the same
#
# compare's findings about the files (PDF 1.7, the page's language) are left aside. Of its findings
# about the look, only words divided differently, and lines that stand where they stood (within
# NEAR points), may stand. Anything else (a word missing, a font, a size, a colour, a page break, a
# picture added, letters with no text behind them in marqius-wkhtmltopdf's PDF, a warning from
# marqius-wkhtmltopdf) means no mark. "The page's own words" are the text of the HTML files the
# document's command line names, read as a browser reads them, compared without white space or case,
# with a few letters of the words around them, as the PDF has them. "The same there" means that,
# inside the boxes compare gives for the difference, the ink of each page lies within NEAR points of
# the other's, and the two pages, drawn in colour, hold as much ink there, of the same colour (so a
# gradient painted grey, a bold word set regular or a half-transparent line set solid is not the same).
SAME_THERE = 0.98  # share of the ink there with ink from the other page within NEAR points
SAME_INK = 0.85  # the lesser page's ink there (the sum of each dot's darkness) against the greater's
SAME_COLOUR = 24  # largest difference, in any of red, green and blue (0 to 255), between the ink's mean colours there
CONTEXT = 6  # letters either side of a word that must be the page's own too
FINE_LOOK = {"moved", "reflow"}  # compare's findings about the look that may stand if the two are the same there


class PageText(HTMLParser):
    """the text an HTML file shows: its text, and the values of its fields, without scripts and style sheets"""
    SKIP = {"script", "style", "noscript", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag == "input":
            self.parts += [v for k, v in attrs if k in ("value", "placeholder") and v]

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


WINDOWS_1252 = {"iso-8859-1", "iso8859-1", "latin1", "latin-1", "l1", "us-ascii", "ascii", "windows-1252", "cp1252"}


def page_text(raw, encoding=None):
    """an HTML file's text, read as a browser reads it: by its byte-order mark, else the character set it
    names, else the one given on the command line (--encoding), else UTF-8 when the bytes are UTF-8,
    else Windows-1252"""
    if raw.startswith(b"\xef\xbb\xbf"):
        enc = "utf-8-sig"
    elif raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        enc = "utf-16"
    else:
        m = re.search(rb"""<meta[^>]*?charset\s*=\s*["']?\s*([A-Za-z0-9._:-]+)""", raw[:4096], re.I) or \
            re.search(rb"""<\?xml[^>]*?encoding\s*=\s*["']([A-Za-z0-9._:-]+)""", raw[:4096], re.I)
        enc = (m.group(1).decode("ascii") if m else encoding or "").lower()
        if enc in WINDOWS_1252:
            enc = "cp1252"
        if not enc:
            try:
                raw.decode("utf-8")
                enc = "utf-8"
            except UnicodeDecodeError:
                enc = "cp1252"
    try:
        text = raw.decode(enc, errors="replace")
    except LookupError:
        text = raw.decode("utf-8", errors="replace")
    p = PageText()
    p.feed(text)
    p.close()
    return " ".join(p.parts)


def plain(s):
    """text to compare: canonical Unicode, case folded, without white space, controls or invisible marks"""
    s = unicodedata.normalize("NFC", unicodedata.normalize("NFC", s).casefold())
    return "".join(c for c in s if unicodedata.category(c) not in ("Zs", "Zl", "Zp", "Cc", "Cf"))


def own_text(corpus, s, n):
    """the page's own text, plain: the HTML files the document's command line names (the page, its
    header and footer, a cover), or the set's page of that name; '' when there is none"""
    d = corpus / s
    cmd = d / f"{n}.cmd"
    if cmd.exists():
        # one argument a line; lines starting with # are notes (as convert.sh reads them)
        args = [a.strip() for a in cmd.read_text(encoding="utf-8").splitlines() if a.strip() and not a.startswith("#")]
    else:
        args = []
        opts = d / "options.txt"  # mine/options.txt: options for every document of the set
        if opts.exists():
            import shlex
            try:
                args = shlex.split("\n".join(x for x in opts.read_text(encoding="utf-8").splitlines() if not x.startswith("#")))
            except ValueError:
                args = []
        args += [f"{n}{e}" for e in (".html", ".htm") if (d / f"{n}{e}").exists()][:1]
    enc = args[args.index("--encoding") + 1] if "--encoding" in args[:-1] else None
    files = [d / a for a in args if re.search(r"\.(x?html?|xml)$", a, re.I) and (d / a).is_file()]
    return plain(" ".join(page_text(f.read_bytes(), enc) for f in files))


def cut(s):
    """compare's text without its note that it shortened it ('… (20 words)')"""
    return re.sub(r"\s*…\s*\(\d+ words?\)\s*$", "", re.sub(r"^\s*…\s*", "", s or ""))


def misread(s):
    """s as a program shows it that takes UTF-8 for Windows-1252: é as Ã©"""
    out = []
    for b in s.encode("utf-8"):
        try:
            out.append(bytes([b]).decode("cp1252"))
        except UnicodeDecodeError:
            out.append(chr(b))
    return "".join(out)


def page_own(piece, pdf_text, own):
    """True when piece is the page's own words: with CONTEXT letters before or after it, as the PDF's
    text has them, it is in the page's own text (a piece of 12 letters or more may stand alone when
    the PDF's text does not have it as compare read it)"""
    p = plain(cut(piece))
    if not p or not own:
        return False
    i = pdf_text.find(p)
    if i < 0:
        return len(p) >= 12 and p in own
    while i >= 0:
        j = i + len(p)
        if any(c in own for c in (pdf_text[max(0, i - CONTEXT):j + CONTEXT], pdf_text[max(0, i - CONTEXT):j], pdf_text[i:j + CONTEXT])
               if len(c) > len(p) or len(p) >= 12):
            return True
        i = pdf_text.find(p, i + 1)
    return False


def look_there(ink, places, pad=2):
    """inside the boxes compare gives (page, box in points from the top left), the share of ink with
    ink from the other PDF within NEAR points, and how much ink each PDF has there"""
    (A, wa), (B, wb) = ink
    ia = ib = ma = mb = 0
    for pl in places:
        k = int(pl.get("page", 0)) - 1
        if k < 0 or k >= len(A) or k >= len(B) or wa[k] != wb[k]:
            return 0.0, 0, 0
        a, b, w = A[k], B[k], wa[k]
        x0, y0, x1, y1 = pl["box"]
        X0, X1 = max(0, int(x0) - pad), min(w - 1, int(x1) + pad)
        Y0, Y1 = max(0, int(y0) - pad), min(len(a), len(b), int(y1) + pad + 1)
        if X1 < X0 or Y1 <= Y0:
            continue
        mask = ((1 << (X1 - X0 + 1)) - 1) << (w - 1 - X1)
        lo, hi = max(0, Y0 - NEAR), min(len(a), len(b), Y1 + NEAR)
        ga, gb = grow(a[lo:hi]), grow(b[lo:hi])
        for y in range(Y0, Y1):
            ra, rb = a[y] & mask, b[y] & mask
            ia += ra.bit_count()
            ib += rb.bit_count()
            ma += (ra & gb[y - lo]).bit_count()
            mb += (rb & ga[y - lo]).bit_count()
    return ((ma + mb) / (ia + ib) if ia + ib else 1.0), ia, ib


def in_colour(pdf, page):
    """one page of a PDF drawn in colour at DPI: (width, height, red-green-blue bytes), or None"""
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), str(pdf), str(Path(t) / "p")],
                       capture_output=True, timeout=120)
        f = next(Path(t).glob("p-*.ppm"), None)
        if not f:
            return None
        data = f.read_bytes()
    # P6 header: magic, width, height, maxval, each separated by white space
    fields, i = [], 0
    while len(fields) < 4:
        while data[i:i + 1].isspace():
            i += 1
        j = i
        while not data[j:j + 1].isspace():
            j += 1
        fields.append(data[i:j])
        i = j
    return int(fields[1]), int(fields[2]), data[i + 1:]


def tone_there(pdf, places, cache, pad=2):
    """inside the boxes, on a PDF's pages drawn in colour: how much ink there is (the sum of each dot's
    darkness, 0 to 255) and the ink's mean colour, each dot weighed by its darkness; None when a page
    cannot be drawn"""
    dark = red = green = blue = 0
    for pl in places:
        key = (pdf, int(pl.get("page", 0)))
        if key not in cache:
            cache[key] = in_colour(*key) if key[1] > 0 else None
        if not cache[key]:
            return None
        w, h, px = cache[key]
        x0, y0, x1, y1 = pl["box"]
        X0, X1 = max(0, int(x0) - pad), min(w - 1, int(x1) + pad)
        for y in range(max(0, int(y0) - pad), min(h - 1, int(y1) + pad) + 1):
            row = px[(y * w + X0) * 3:(y * w + X1 + 1) * 3]
            for k in range(0, len(row) - 2, 3):
                r, g, b = row[k], row[k + 1], row[k + 2]
                d = 255 - (299 * r + 587 * g + 114 * b) // 1000
                if d > 0:
                    dark += d
                    red += d * r
                    green += d * g
                    blue += d * b
    return dark, ((red / dark, green / dark, blue / dark) if dark else (255.0, 255.0, 255.0))


def better_than_wk(diffs, own, text_wk, text_mq, ink, rp, mp):
    """True when every difference compare found (diffs, from its pair file) goes marqius-wkhtmltopdf's
    way and nothing else looks different (see above); text_wk and text_mq are the PDFs' text, plain;
    ink is both PDFs' pages as drawn() gives them, rp and mp the PDFs"""
    cache = {}

    def same_there(places, wk_drew=False, mq_drew=False):
        share, ia, ib = look_there(ink, places)
        if not places or share < SAME_THERE or (wk_drew and not ia) or (mq_drew and not ib):
            return False
        tw, tm = tone_there(rp, places, cache), tone_there(mp, places, cache)
        if not tw or not tm:
            return False
        (dw, cw), (dm, cm) = tw, tm
        if not max(dw, dm):
            return True
        return min(dw, dm) / max(dw, dm) >= SAME_INK and max(abs(a - b) for a, b in zip(cw, cm)) <= SAME_COLOUR

    wins = 0
    for x in diffs:
        of, kind = x.get("of"), x.get("kind")
        old, new = x.get("old") or [], x.get("new") or []
        if of == "file":
            continue
        if of == "appearance":
            if kind == "spacing" or (kind in FINE_LOOK and same_there(old + new)):
                continue
            return False
        if kind == "text":
            was, now = cut(x.get("was")), cut(x.get("now"))
            if not page_own(now, text_mq, own):
                return False
            if plain(was) and plain(was) == plain(misread(now)) != plain(now):
                pass  # wkhtmltopdf read the page's UTF-8 as Windows-1252
            elif not plain(was) or plain(was) in own or not same_there(old + new, wk_drew=True, mq_drew=True):
                return False
        elif kind == "added":
            if not page_own(x.get("now"), text_mq, own) or not same_there(new, wk_drew=True, mq_drew=True):
                return False
        elif kind == "picture-missing":
            if not same_there(old, wk_drew=True, mq_drew=True):
                return False
        elif kind == "unreadable":
            if new or not same_there(old, wk_drew=True, mq_drew=True):
                return False
        else:
            return False
        wins += 1
    return wins > 0


def judge(rp, mp, pages_wk, pages_mq, ink, pair, own, err_mq):
    """the mark for one document: better_than_wk, once both PDFs are there with as many pages,
    compare has listed every difference, and marqius-wkhtmltopdf gave no warning"""
    if not ink or not own or pages_wk != pages_mq:
        return False
    if Path(err_mq).exists() and Path(err_mq).read_text(errors="replace").strip():
        return False
    try:
        j = json.loads(Path(pair).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if j.get("verdict") != "content differs" or any((j.get("left_out") or {}).values()):
        return False
    return better_than_wk(j.get("differences", []), own, plain(pdftotext(rp)), plain(pdftotext(mp)), ink, rp, mp)


MISS = 0.99  # a document below this, or with content that differs, is listed with its pictures


def small_pictures(work, docs):
    """compare's pictures of the pages that differ, for the listed documents, in 32 colours
    (a tenth of the size, as legible) in WORK/pictures, named SET--PICTURE"""
    out = work / "pictures"
    out.mkdir(exist_ok=True)
    try:
        from PIL import Image
    except ImportError:
        Image = None
    for d in docs:
        if not d["miss"]:
            continue
        for p in d.get("pictures", []):
            src = work / "compare" / d["set"] / "pairs" / p
            dst = out / f"{d['set']}--{p}"
            if not src.exists():
                continue
            if Image is None:
                dst.write_bytes(src.read_bytes())
                continue
            im = Image.open(src).convert("RGB")
            im.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)


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
    s, n, rp, mp, pair, own, err_mq = job
    sc, text, geom, pr, pm = score_pair(rp, mp)
    ink = drawn(rp, mp)
    return dict(set=s, name=n, score=sc, text=text, geom=geom, pages_wk=pr, pages_mq=pm, overlay=overlay_of(ink),
                fonts_wk=fonts_of(rp), fonts_mq=fonts_of(mp),
                size_wk=Path(rp).stat().st_size if pdf_ok(rp) else 0,
                size_mq=Path(mp).stat().st_size if pdf_ok(mp) else 0,
                made_wk=pdf_ok(rp), made_mq=pdf_ok(mp),
                better=judge(rp, mp, pr, pm, ink, pair, own, err_mq))


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
            jobs.append((s, n, str(d_wk / f"{n}.pdf"), str(d_mq / f"{n}.pdf"), str(work / "compare" / s / "pairs" / f"{n}.json"),
                         own_text(corpus, s, n), str(work / "logs" / "mq" / s / f"{n}.err")))
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
        d["miss"] = d["score"] < MISS or d["verdict"] == "content differs"
        for key in ("score", "text", "geom", "overlay"):
            d[key] = round(d[key], 6)

    small_pictures(work, docs)

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
            overlay=round(sum(d["overlay"] for d in ds) / len(ds), 6), overlay_lowest=round(min(d["overlay"] for d in ds), 6),
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
        headline = dict(sets=pub, documents=len(ds), parity=round(sum(sc) / len(sc), 6), overlay=round(sum(d["overlay"] for d in ds) / len(ds), 6),
                        bytes_wk=sum(d["size_wk"] for d in ds), bytes_mq=sum(d["size_mq"] for d in ds),
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
        cols = ["set", "name", "score", "text", "geom", "pages_wk", "pages_mq", "overlay", "verdict", "level", "first", "fonts_same",
                "size_wk", "size_mq", "status_wk", "status_mq", "ms_wk", "ms_mq", "better"]
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
    out.append(f"  {'set':14s} {'docs':>4s} {'parity':>7s} {'lowest':>7s} {'overlay':>7s}  {'same pages':>10s} {'appearance':>10s} {'content':>8s}  speed")
    for s, x in r["sets"].items():
        v = x["verdicts"]
        sp = f"{x['speed']:.0f}x" if x.get("speed") else ""
        out.append(f"  {s:14s} {x['documents']:4d} {x['parity']:7.4f} {x['lowest']:7.4f} {x['overlay']:7.3f}  {v.get('same pages', 0):10d} {v.get('appearance only', 0):10d} {v.get('content differs', 0):8d}  {sp}")
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
            out.append(f"    {d['set']}/{d['name']}: {d['score']:.4f} (overlay {d['overlay']:.3f})" + (f", {BETTER.lower()}" if d.get("better") else "")
                       + f"  {why(d)[:80]}")
    nb = sum(1 for d in r["documents"] if d.get("better"))
    if nb:
        out.append("")
        out.append(f"  {BETTER}: {nb} document{'s' if nb > 1 else ''} ({', '.join(d['set'] + '/' + d['name'] for d in r['documents'] if d.get('better'))})")
    return "\n".join(out)


BETTER = "marqius better"
BETTER_ABOUT = ("*marqius better* marks a document where every difference goes marqius-wkhtmltopdf's way: its PDF has the page's own words "
                "where wkhtmltopdf's has garbled letters, look-alike characters or a picture of the words, and nothing else on the page looks different. "
                "Its score is lower only because the score measures how alike the two PDFs are.")


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
    L += ["| Set | Documents | Parity | Lowest | Overlay | Same pages | Appearance only | Content differs | Fonts differ | Speed |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for s, x in r["sets"].items():
        v = x["verdicts"]
        L.append(f"| {x['title']} (`{s}`) | {x['documents']} | {x['parity']:.4f} | {x['lowest']:.4f} | {x['overlay']:.3f} | {v.get('same pages', 0)} | "
                 f"{v.get('appearance only', 0)} | {v.get('content differs', 0)} | {x['fonts_differ']} | {(str(round(x['speed'])) + '×') if x.get('speed') else ''} |")
    L += ["", "Parity is the marqius engine's measure: 50% text, 30% word positions, 20% page count, from 0 to 1, read from the text in the PDFs. "
          "*Overlay* lays one page on the other: the share of ink, at 72 dots an inch, with ink from the other page within 2 points. "
          "The verdicts are `marqius-wkhtmltopdf compare`'s: *same pages* counts the pairs whose pages are the same "
          "(the files themselves may differ, as PDF 1.4 against 1.7 does), *appearance only* those where something moved "
          "or changed size or colour, *content differs* those where words, numbers or pictures differ.", ""]
    if any(d.get("better") for d in r["documents"]):
        L += [BETTER_ABOUT, ""]
    for s, x in r["sets"].items():
        L += [f"## {x['title']} (`{s}`)", "",
              "| Document | Score | Text | Positions | Pages | Overlay | compare | First difference | Fonts | Size wk / mq | Time wk / mq |",
              "|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|"]
        for d in doc_rows(r, s):
            fonts = "same" if d["fonts_same"] else "differ"
            first = why(d).replace("|", "\\|")
            if d["note"]:
                first += f" — *{d['note']}*"
            name = d["name"] + (f"<br>🏅 **{BETTER}**" if d.get("better") else "")
            L.append(f"| {name} | {d['score']:.4f} | {d['text']:.3f} | {d['geom']:.3f} | {d['pages_wk']}/{d['pages_mq']} | {d['overlay']:.3f} | "
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
    L += ["", "## Sizes", ""]
    for s_, x in r["sets"].items():
        L.append(f"- {s_}: the PDFs come to {kb(x['bytes_wk'])} from wkhtmltopdf and {kb(x['bytes_mq'])} from marqius-wkhtmltopdf")
    imgs = r["meta"].get("images", {})
    if imgs.get("marqius", {}).get("size_mb") and imgs.get("reference", {}).get("size_mb"):
        L.append(f"- images, unpacked: `{imgs['marqius']['name']}` {imgs['marqius']['size_mb']:.0f} MB; the reference system with wkhtmltopdf and its fonts {imgs['reference']['size_mb']:.0f} MB")
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
        rows.append(f"<tr><td>{esc(x['title'])} <code>{esc(s)}</code></td><td>{x['documents']}</td><td><b>{x['parity']:.4f}</b></td><td>{x['lowest']:.4f}</td><td>{x['overlay']:.3f}</td>"
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
            cls = "good" if d.get("better") else "bad" if d["score"] < 0.9 else "warn" if d["score"] < 0.98 else ""
            badge = f"<br><span class='better'>{BETTER}</span>" if d.get("better") else ""
            trs.append(f"<tr class='{cls}'><td>{esc(d['name'])}{badge}</td><td><b>{d['score']:.4f}</b></td><td>{d['text']:.3f}</td><td>{d['geom']:.3f}</td>"
                       f"<td>{d['pages_wk']}/{d['pages_mq']}</td><td>{d['overlay']:.3f}</td><td>{esc(verdict_word(d['verdict']))}</td><td>{first}</td>"
                       f"<td>{'same' if d['fonts_same'] else 'differ: ' + esc(', '.join(sorted(set(d['fonts_wk']) ^ set(d['fonts_mq']))))}</td>"
                       f"<td>{kb(d['size_wk'])} / {kb(d['size_mq'])}</td><td>{ms_text(d['ms_wk'])} / {ms_text(d['ms_mq'])}</td>"
                       f"<td>{' '.join(pic_links)}</td>"
                       f"<td><a href='pdf/wk/{esc(s)}/{esc(d['name'])}.pdf'>wk</a> <a href='pdf/mq/{esc(s)}/{esc(d['name'])}.pdf'>mq</a></td></tr>")
        parts.append(f"<h2>{esc(x['title'])} <code>{esc(s)}</code></h2><p>{x['documents']} documents, parity <b>{x['parity']:.4f}</b>, lowest {x['lowest']:.4f}.</p>"
                     "<table><tr><th>Document</th><th>Score</th><th>Text</th><th>Positions</th><th>Pages wk/mq</th><th>Overlay</th><th>compare</th><th>First difference</th>"
                     "<th>Fonts</th><th>Size wk / mq</th><th>Time wk / mq</th><th>Pages that differ</th><th>PDFs</th></tr>" + "".join(trs) + "</table>")
    sysl = "".join(f"<li>{esc(re.sub(r'[*`]', '', x))}</li>" for x in system_lines(r))
    better_about = (f"<p class='muted'><span class='better'>{BETTER}</span> {esc(BETTER_ABOUT.replace('*' + BETTER + '*', '').strip())} "
                    "Its row is green.</p>") if any(d.get("better") for d in r["documents"]) else ""
    head = ""
    if h:
        head = (f"<p class='big'>Published documents ({esc(' and '.join(h['sets']))}, {h['documents']}): parity <b>{h['parity']:.4f}</b>"
                + (f", {h['speed']:.0f}× faster than wkhtmltopdf" if h.get("speed") else "") + "</p>")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>wkhtmltopdf parity report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ --fg: #1c2430; --muted: #5b6676; --line: #d9dee5; --bg: #fff; --head: #f3f5f8; --bad: #fde8e8; --warn: #fff6dc; --good: #e9f6ec; --better: #1a7f37; --link: #1f5fbf }}
@media (prefers-color-scheme: dark) {{ :root {{ --fg: #e6e9ee; --muted: #9aa4b2; --line: #333b47; --bg: #14181e; --head: #1d232b; --bad: #3a1f22; --warn: #34301d; --good: #17301f; --better: #238636; --link: #7fb0ff }} }}
body {{ font: 14px/1.45 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: var(--fg); background: var(--bg); margin: 24px auto; max-width: 1400px; padding: 0 16px }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 24px; font-size: 13px }} th, td {{ border-bottom: 1px solid var(--line); padding: 5px 8px; text-align: left; vertical-align: top }}
th {{ background: var(--head); position: sticky; top: 0 }} tr.bad td {{ background: var(--bad) }} tr.warn td {{ background: var(--warn) }} tr.good td {{ background: var(--good) }}
.better {{ display: inline-block; margin-top: 3px; padding: 1px 8px 1px 7px; border-radius: 4px; background: var(--better); color: #fff; font-size: 11px; font-weight: 600; white-space: nowrap }}
.better::before {{ content: "🏅 " }}
.big {{ font-size: 18px }} .muted {{ color: var(--muted) }} a {{ color: var(--link) }} code {{ font-size: 12px }}
</style></head><body>
<h1>wkhtmltopdf parity report</h1>
<p>marqius-wkhtmltopdf <b>{esc(m['marqius']['version'])}</b> beside <b>{esc(e.get('wk_version', ''))}</b>, {esc(m['when'])}, on {esc(m['platform'])}.</p>
{head}
<table><tr><th>Set</th><th>Documents</th><th>Parity</th><th>Lowest</th><th>Overlay</th><th>Same pages</th><th>Appearance only</th><th>Content differs</th><th>Fonts differ</th><th>Speed</th></tr>{''.join(rows)}</table>
<p class="muted">Parity: 50% text, 30% word positions, 20% page count (the marqius engine's measure, read from the text in the PDFs). Overlay: one page laid on the other; the share of ink, at 72 dots an inch, with ink from the other page within 2 points. Verdicts: <code>marqius-wkhtmltopdf compare</code>; its full report, with both PDFs marked where they differ, is in <a href="compare/">compare/</a>. Rows in yellow score below 0.98, in red below 0.90.</p>
{better_about}
{''.join(parts)}
<h2>What ran</h2><ul>{sysl}</ul>
</body></html>
"""


if __name__ == "__main__":
    main()
