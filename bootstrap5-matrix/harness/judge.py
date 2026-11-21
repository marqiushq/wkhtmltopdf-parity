"""The matrix: for each page and stylesheet, compare's verdict on wkhtmltopdf's PDF against Chrome's
(same, appearance only, content differs), the kinds of difference it found and its first note;
beside it, the computed styles each program read (why a page differs). Keeps compare's picture
of each page (Chrome left, wkhtmltopdf right, differences marked).

    python3 harness/judge.py SITE OUT RESULTS"""
import csv
import json
import pathlib
import re
import shutil
import sys

from PIL import Image

SITE, OUT, RES = (pathlib.Path(a) for a in sys.argv[1:4])
KINDS = ["text", "number", "date", "written", "missing", "added", "picture-missing", "picture-added", "picture-changed",
         "unreadable", "reflow", "spacing", "moved", "page-break", "pages", "page-size", "font", "size", "colour",
         "picture-moved", "picture-size", "picture-dots", "drawing", "pdf-type"]
def norm(v):
    return re.sub(r"\s+", " ", str(v).strip().lower())


def close(a, b, tol=1.0):
    """two computed lengths within tol px of each other (4px and 4.8px are the same corner), or equal text"""
    na, nb = re.findall(r"-?\d*\.?\d+", str(a)), re.findall(r"-?\d*\.?\d+", str(b))
    if na and nb and len(na) == len(nb):
        return all(abs(float(x) - float(y)) <= tol for x, y in zip(na, nb))
    return norm(a) == norm(b)


SHORT = {"same": "same", "appearance only": "appearance", "content differs": "content", "file differs": "same",
         "cannot tell": "cannot tell"}


def older(have, since):
    return tuple(int(x) for x in have.split(".")) < tuple(int(x) for x in since.split("."))


def main():
    meta = json.loads((SITE / "pages.json").read_text())
    rend = json.loads((OUT / "render.json").read_text())
    sets, pages = meta["sets"], meta["pages"]
    rows = {}
    for s in sets:
        p = OUT / "compare" / s / "summary.csv"
        if p.exists():
            with p.open(encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    rows[(s, r["pair"])] = r
    if RES.exists():
        shutil.rmtree(RES / "pictures", ignore_errors=True)
    RES.mkdir(parents=True, exist_ok=True)
    out = []
    for pg in pages:
        slug = pg["slug"]
        per = {}
        for s, sm in sets.items():
            r = rend["results"]["%s/%s" % (s, slug)]
            c = rows.get((s, slug), {})
            kinds = {k: int(c[k]) for k in KINDS if c.get(k, "0").isdigit() and int(c[k])}
            why = []
            for i, chk in enumerate(pg["checks"]):
                v = {e: ((r[e].get("probe") or {}).get("js") or {}).get(str(i)) for e in ("wkhtmltopdf", "chromium")}
                why.append(dict(n=chk["n"], wk=v["wkhtmltopdf"], ch=v["chromium"]))
            e = dict(verdict=c.get("verdict", "not compared"), level=c.get("level", ""), first=c.get("first", ""),
                     differences=int(c["differences"]) if c.get("differences", "").isdigit() else None, kinds=kinds,
                     pages=dict(wk=r["wkhtmltopdf"]["pages"], ch=r["chromium"]["pages"]), why=why,
                     notes=[x for x in (r["wkhtmltopdf"].get("note"), r["chromium"].get("note")) if x])
            if pg.get("judge") == "computed":
                # compare sets where rules, frames and tints stand, not the roundness of their corners:
                # on these pages the computed corner radius decides, and the matrix says so
                off = [w for w in why if not close(w["wk"], w["ch"])]
                e["compare"] = e["verdict"]
                e["verdict"] = "appearance only" if off else "same"
                e["kinds"] = {"corners": len(off)} if off else {}
                e["first"] = ("%s: %s in wkhtmltopdf, %s in Chrome (computed style; compare does not compare corner shapes)"
                              % (off[0]["n"], off[0]["wk"], off[0]["ch"])) if off else ""
            if pg.get("since") and older(sm["bootstrap"], pg["since"]):
                e["na"] = "not in Bootstrap %s" % sm["bootstrap"]
            pj = OUT / "compare" / s / "pairs" / (slug + ".json")
            if pj.exists():
                try:
                    e["first_notes"] = [d.get("note", "") for d in json.loads(pj.read_text(encoding="utf-8")).get("differences", [])][:6]
                except ValueError:
                    pass
            pic = OUT / "compare" / s / "pairs" / (slug + ".page-1.png")
            if pic.exists():
                dest = RES / "pictures" / s / (slug + ".png")
                dest.parent.mkdir(parents=True, exist_ok=True)
                Image.open(pic).convert("RGB").quantize(colors=48).save(dest, optimize=True)
                e["picture"] = "pictures/%s/%s.png" % (s, slug)
            per[s] = e
        out.append(dict(slug=slug, group=pg["group"], title=pg["title"], bare=pg.get("bare", False), results=per))
    (RES / "results.json").write_text(json.dumps(dict(tools=rend["tools"], scale=rend["scale"], wkhtmltopdf_args=rend["wkhtmltopdf_args"],
                                                      sets=sets, pages=out), indent=1))
    write_md(rend, sets, out)


def md(s):
    """text for a Markdown table: tags shown as text, pipes kept inside the cell"""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")


def cell(e):
    if e.get("na"):
        return "–"
    v = SHORT.get(e["verdict"], e["verdict"])
    if v == "same":
        txt = "✓ same"
    else:
        ks = sorted(e["kinds"], key=lambda k: -e["kinds"][k])
        txt = "✗ %s: %s" % (v, ", ".join(ks[:3]) or "?")
    if e.get("picture"):
        txt = "[%s](%s)" % (txt, e["picture"])
    return txt


def write_md(rend, sets, pages):
    names = list(sets)
    L = ["# Bootstrap 5 in wkhtmltopdf 0.12.6.1, page by page", "",
         "Each page uses one Bootstrap 5 feature as an Odoo report would. wkhtmltopdf prints it as Odoo calls it; Chrome prints it "
         "as the reference, at the scale wkhtmltopdf prints a CSS pixel (%.4f), so the same CSS gives the same page. "
         "`marqius-wkhtmltopdf compare` sets wkhtmltopdf's PDF against Chrome's: ✓ same; ✗ appearance (the same words, laid out "
         "or drawn differently) or ✗ content (words missing, added or changed), with the kinds of difference it found. – : not in "
         "that Bootstrap. Each verdict links compare's picture: Chrome left, wkhtmltopdf right, each difference marked. "
         "compare does not compare the roundness of corners: on the two corner pages, the corner radius each program computed decides."
         % rend["scale"]["chrome"], "",
         "Programs: " + "; ".join(rend["tools"].values()) + ".", "",
         "| Feature | " + " | ".join(sets[s]["label"] for s in names) + " |", "|---|" + "---|" * len(names)]
    group = None
    for pg in pages:
        if pg["group"] != group:
            group = pg["group"]
            L.append("| **%s** |%s" % (group, " |" * len(names)))
        L.append("| %s | %s |" % (md(pg["title"]), " | ".join(cell(pg["results"][s]) for s in names)))
    L += ["", "## Why: what each program read", ""]
    for pg in pages:
        lines = []
        for s in names:
            e = pg["results"][s]
            if e.get("na") or SHORT.get(e["verdict"]) == "same":
                continue
            diffs = ["%s %s / %s" % (w["n"], w["wk"], w["ch"]) for w in e["why"] if w["wk"] != w["ch"]]
            lines.append("- %s: %s%s" % (sets[s]["label"], e["first"] or e["verdict"],
                                         ("; computed (wkhtmltopdf / Chrome): " + "; ".join(diffs)) if diffs else ""))
        if lines:
            L += ["**%s**" % md(pg["title"]), ""] + [md(x) for x in lines] + [""]
    (RES / "RESULTS.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote", RES / "RESULTS.md")


if __name__ == "__main__":
    main()
