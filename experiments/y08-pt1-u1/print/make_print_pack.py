#!/usr/bin/env python3
"""BookVault print pack for y08-portuguese-1st-anthropic (A4 master -> US Letter print).

The house pack builder (tools/make_bookvault_files.py) is written for masters that
already sit on BookVault's 216 x 279 mm trim. This book is A4 (210 x 297 mm), so a
1:1 placement cuts 9 mm off the top and bottom: the running header and the folio
badges land on the cut. And the reader's page parity is not the press's: in the
flipbook the cover stands alone and p. 2 is a LEFT page, but in the printed block
(covers stripped) p. 2 would be the first RIGHT page, so every outer-edge thumb tab
would land in the gutter.

This script stages a PRINT MASTER and runs the unchanged house builder on it:

  * every interior page is scaled to the trim height (x 0.9393) and set flush to
    its OUTER edge; the 18.8 mm left at the binding edge continues the page's own
    gutter-edge colour (a 1 pt column stretched across it, vector), inside
    BookVault's 20 mm binding zone;
  * one blank leaf goes in front of p. 2, so odd folios print on rectos exactly as
    designed (outer tabs on the outside, gutter margins at the spine) -- and the
    block becomes 159 pages = 4n-1, BookVault's rule for trims above US Royal;
  * the covers are fitted to the trim by the width (centred crop top and bottom).

Run: .venv/bin/python print/make_print_pack.py   (from the experiment dir)
"""
import importlib, pathlib, shutil, sys

import io

import pymupdf
from PIL import Image

REPO = pathlib.Path("/root/prime-books")
SLUG = "y08-portuguese-1st-anthropic"
MASTER = REPO / "public" / "library" / SLUG / "book.pdf"
STAGE = pathlib.Path(__file__).resolve().parent / "stage"
MM = 72 / 25.4
W, H = 216.0 * MM, 279.0 * MM          # BookVault US Letter trim, points
DPI = 300                              # BookVault's image floor; the page is printed from this raster
PX_W, PX_H = round(216.0 / 25.4 * DPI), round(279.0 / 25.4 * DPI)
JPEG_Q = 92


def render(src, i, scale_px):
    pix = src[i].get_pixmap(matrix=pymupdf.Matrix(scale_px, scale_px), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def put(dst, im):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, subsampling=0, dpi=(DPI, DPI))
    p = dst.new_page(width=W, height=H)
    p.insert_image(p.rect, stream=buf.getvalue())


def fill(dst, src, i):
    """Cover pages: scale to cover the trim, centred crop."""
    r = src[i].rect
    k = max(PX_W / r.width, PX_H / r.height)
    im = render(src, i, k)
    x, y = (im.width - PX_W) // 2, (im.height - PX_H) // 2
    put(dst, im.crop((x, y, x + PX_W, y + PX_H)))


def interior(dst, src, i, recto):
    """Scale to the trim height, set flush to the OUTER edge, continue the gutter edge."""
    r = src[i].rect
    im = render(src, i, PX_H / r.height)
    im = im.resize((im.width, PX_H)) if im.height != PX_H else im
    gap = PX_W - im.width
    canvas = Image.new("RGB", (PX_W, PX_H))
    if recto:                                   # binding edge on the LEFT
        canvas.paste(im.crop((0, 0, 2, PX_H)).resize((gap, PX_H)), (0, 0))
        canvas.paste(im, (gap, 0))
    else:                                       # binding edge on the RIGHT
        canvas.paste(im, (0, 0))
        canvas.paste(im.crop((im.width - 2, 0, im.width, PX_H)).resize((gap, PX_H)), (im.width, 0))
    put(dst, canvas)


def margins():
    """Live-text clearance on the PRINTED page (the raster carries no text, so the
    pack builder cannot measure it): the master's text boxes mapped through the
    same scale + outer-edge placement, against BookVault's 20 mm gutter and 5 mm
    trim rules. Returns the worst value per edge with its book page."""
    src = pymupdf.open(MASTER)
    n = src.page_count
    worst = {"gutter": (999, 0), "outer": (999, 0), "top": (999, 0), "bottom": (999, 0)}
    for i in range(1, n - 1):
        r = src[i].rect
        k = (279.0 / 25.4 * 72) / r.height
        pw = r.width * k / MM                       # printed width of the page, mm
        gap = 216.0 - pw
        recto = (i + 1) % 2 == 1
        for b in src[i].get_text("blocks"):
            if not b[4].strip():
                continue
            x0, y0, x1, y1 = (v * k / MM for v in b[:4])
            if recto:
                x0, x1 = x0 + gap, x1 + gap
                g, o = x0, 216.0 - x1
            else:
                g, o = 216.0 - x1, x0
            for edge, v in (("gutter", g), ("outer", o), ("top", y0), ("bottom", 279.0 - y1)):
                if v < worst[edge][0]:
                    worst[edge] = (round(v, 1), i + 1)
    return worst


def stage() -> pathlib.Path:
    src = pymupdf.open(MASTER)
    n = src.page_count
    out = pymupdf.open()
    fill(out, src, 0)                           # staged idx 0: front cover
    put(out, Image.new("RGB", (PX_W, PX_H), (255, 255, 255)))   # staged idx 1: blank flyleaf (recto)
    for i in range(1, n - 1):                   # book p.2 .. p.n-1 -> staged idx i+1
        interior(out, src, i, recto=(i + 1) % 2 == 1)
    fill(out, src, n - 1)                       # back cover
    d = STAGE / SLUG
    d.mkdir(parents=True, exist_ok=True)
    path = d / "book.pdf"
    out.save(path, garbage=4, deflate=True)
    print(f"staged {out.page_count} pages ({n} in the master + 1 flyleaf) -> {path}")
    return path


def build(spine_mm=None):
    sys.path.insert(0, str(REPO / "tools"))
    mb = importlib.import_module("make_bookvault_files")
    mb.LIBRARY = STAGE                          # read the print master, write the pack beside it
    r = mb.build(SLUG, force=True, do_pdfx=True, spine_per_page_mm=None, spine_mm=spine_mm,
                 pad_12n=False, cover_only=False)
    fails = [c["name"] for c in r["checks"] if not c["pass"] and c["level"] == "fail"]
    opens = [c["name"] for c in r["checks"] if not c["pass"] and c["level"] == "warn"]
    print("FAIL:", fails or "none")
    print("OPEN:", opens or "none")
    for c in r["checks"]:
        if not c["pass"]:
            print(f"  [{c['level']}] {c['name']}: {str(c.get('detail', ''))[:400]}")
    dst = REPO / "public" / "library" / SLUG / "bookvault"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(STAGE / SLUG / "bookvault", dst)
    print("pack ->", dst)


if __name__ == "__main__":
    w = margins()
    print("printed live-text clearance (mm, book page):", w)
    ok = w["gutter"][0] >= 20 and min(w[e][0] for e in ("outer", "top", "bottom")) >= 5
    print("BookVault margins:", "PASS" if ok else "FAIL")
    stage()
    build()
