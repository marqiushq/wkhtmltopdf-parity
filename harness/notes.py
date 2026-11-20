"""Why a document differs: the notes in corpus/notes.tsv, each tied to the result it explains.

    set  name  checked  score  overlay  note

A person writes a note for one result: the document's score and overlay in a run of the
marqius-wkhtmltopdf version named in `checked`. A run shows the note only while the document's
result is still that one, the score within 0.002 and the overlay within 0.005 (between versions,
documents that did not change move by less). Otherwise the run shows what compare found, and lists
the note as one to check again. So no note names a version (the run beside it does), and a new
version never leaves a note beside a result it does not explain. A note with no score and overlay
holds for every result; a document may have several, for different results.

Used by score.py and publish.py. Only the standard library is used.
"""
from pathlib import Path

SCORE_NEAR = 0.002
OVERLAY_NEAR = 0.005


def read(path):
    """{(set, name): [note, ...]}; a file with only set, name and note is read too"""
    path = Path(path)
    if not path.exists():
        return {}
    lines = [line.split("\t") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return {}
    head, out = lines[0], {}
    for row in lines[1:]:
        x = dict(zip(head, row + [""] * (len(head) - len(row))))
        n = {"checked": x.get("checked", ""), "note": x.get("note", "")}
        for k in ("score", "overlay"):
            try:
                n[k] = float(x[k]) if x.get(k) else None
            except ValueError:
                n[k] = None
        out.setdefault((x.get("set", ""), x.get("name", "")), []).append(n)
    return out


def holds(n, d):
    """does note n still explain document d's result?"""
    return ((n["score"] is None or abs(d["score"] - n["score"]) <= SCORE_NEAR)
            and (n["overlay"] is None or abs(d.get("overlay", 0) - n["overlay"]) <= OVERLAY_NEAR))


def pick(notes, d):
    """(the note that explains document d's result, or "" and the notes written for other results)"""
    mine = notes.get((d["set"], d["name"]), [])
    for n in mine:
        if holds(n, d):
            return n["note"], []
    return "", mine


def due_text(d, others):
    """one line for a run's log: a note that no longer explains its document"""
    was = "; ".join(f"{n['checked'] or 'an earlier run'}: {n['score']:.4f}, overlay {n['overlay']:.3f}"
                    for n in others if n["score"] is not None and n["overlay"] is not None)
    return f"{d['set']}/{d['name']} is {d['score']:.4f}, overlay {d.get('overlay', 0):.3f}" + (f" (the note was written for {was})" if was else "")
