"""Publish the experiment into public/library/<slug>/ and the library.json manifest."""
import json, shutil, pathlib, pymupdf
from PIL import Image

ROOT = pathlib.Path(__file__).parent
REPO = ROOT.parents[1]
SLUG = "y08-portuguese-1st-anthropic"
OUT = REPO / "public" / "library" / SLUG
PDF = ROOT / "build" / "book.pdf"

ROW = {
    "slug": SLUG,
    "year": 8,
    "subject": "Portuguese 1st",
    "band": "Cambridge Lower Secondary",
    "family": "experiment",
    "level": "Lower Secondary",
    "pages": None,
    "done": False,
    "pdf": f"/library/{SLUG}/book.pdf",
    "cover": f"/library/{SLUG}/cover.webp",
    "mb": None,
    "buildable": False,
    "editable": False,
    "edition": None,
    "display_name": "Português · 8.º ano — Promessa & Veredicto",
    "finished_full": True,
    "preview": [f"/library/{SLUG}/preview/01.webp", f"/library/{SLUG}/preview/02.webp", f"/library/{SLUG}/preview/last.webp"],
}


def page_webp(doc, i, dest, width=900):
    pix = doc[i].get_pixmap(dpi=150)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(dest, "WEBP", quality=84, method=6)


def upsert_text(text, row):
    """Textual upsert so the rest of the (hand-formatted) manifest is untouched."""
    import re
    block = json.dumps(row, ensure_ascii=False, indent=2)
    block = "\n".join("  " + l for l in block.splitlines())
    pat = re.compile(r',?\n  \{\n    "slug": "' + re.escape(row["slug"]) + r'".*?\n  \}(?=,?\n)', re.S)
    text = pat.sub("", text)
    body = text.rstrip()
    assert body.endswith("]")
    return body[:-1].rstrip() + ",\n" + block + "\n]" + ("\n" if text.endswith("\n") else "")


def main(edition):
    (OUT / "preview").mkdir(parents=True, exist_ok=True)
    (OUT / "audio").mkdir(exist_ok=True)
    shutil.copy(PDF, OUT / "book.pdf")
    for mp3 in (ROOT / "audio").glob("*.mp3"):
        shutil.copy(mp3, OUT / "audio" / mp3.name)
    doc = pymupdf.open(PDF)
    page_webp(doc, 0, OUT / "cover.webp")
    page_webp(doc, 0, OUT / "preview" / "01.webp")
    page_webp(doc, 1, OUT / "preview" / "02.webp")
    page_webp(doc, len(doc) - 1, OUT / "preview" / "last.webp")
    row = dict(ROW, pages=len(doc), mb=round(PDF.stat().st_size / 1e6, 2), edition=edition)
    import subprocess
    lib = REPO / "public" / "library.json"
    new = upsert_text(lib.read_text(), row)
    json.loads(new)
    lib.write_text(new)
    # stage ONLY this row: HEAD's manifest + our row (other agents' unstaged edits stay unstaged)
    head = subprocess.run(["git", "show", "HEAD:public/library.json"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    staged = upsert_text(head, row); json.loads(staged)
    sha = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=REPO, input=staged, capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "update-index", "--cacheinfo", f"100644,{sha},public/library.json"], cwd=REPO, check=True)
    print(json.dumps(row, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
