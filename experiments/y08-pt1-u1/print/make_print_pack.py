#!/usr/bin/env python3
"""BookVault print pack for y08-portuguese-1st-anthropic (A4 master -> US Letter print), VECTOR.

The house builder (tools/make_bookvault_files.py) expects a master on BookVault's
216 x 279 mm trim. This book is A4 (210 x 297 mm). y05 solved that by rasterising every
page at 300 dpi; here that gives a 170 MB text file (the riso paper grain defeats JPEG) --
over GitHub's 100 MB limit. So the print master is built in VECTOR instead:

  * every page (covers included) is scaled to the trim height (x 0.9393) and placed with
    show_pdf_page -- fonts and vectors stay live, the file stays small;
  * it sits flush to its OUTER edge; the ~18.8 mm left at the binding edge is filled with
    the page's own binding-edge column (a 1 pt strip rendered at 300 dpi and stretched),
    inside BookVault's 20 mm binding zone -- on the covers that strip lands on the spine side
    (a width crop would cut the cover's bottom line);
  * one blank leaf goes in front of p. 2, so odd folios print on rectos as designed and the
    block becomes 4n-1 pages (the master must have 4n pages).

Live-text clearance after the transform is checked first (>= 20 mm gutter, >= 5 mm elsewhere).
Run from the experiment dir, in the background (PDF/X conversion takes minutes):
    .venv/bin/python print/make_print_pack.py
"""
import importlib, pathlib, shutil, sys

import pymupdf

REPO = pathlib.Path("/root/prime-books")
SLUG = "y08-portuguese-1st-anthropic"
MASTER = REPO / "public" / "library" / SLUG / "book.pdf"
STAGE = pathlib.Path(__file__).resolve().parent / "stage"
MM = 72 / 25.4
W, H = 216.0 * MM, 279.0 * MM          # BookVault US Letter trim, points
DPI = 300


def edge_strip(src, i, side):
    """PNG of the page's 1 pt edge column on `side` ('left'|'right'), rendered at DPI."""
    r = src[i].rect
    clip = pymupdf.Rect(0, 0, 1, r.height) if side == "left" else pymupdf.Rect(r.width - 1, 0, r.width, r.height)
    pix = src[i].get_pixmap(matrix=pymupdf.Matrix(DPI / 72, DPI / 72), clip=clip, alpha=False)
    return pix.tobytes("png")


def raster_page(src, i):
    """A 300 dpi JPEG of page i, as a one-page PDF (flattens its transparency)."""
    r = src[i].rect
    pix = src[i].get_pixmap(matrix=pymupdf.Matrix(DPI / 72, DPI / 72), alpha=False)
    one = pymupdf.open()
    pg = one.new_page(width=r.width, height=r.height)
    pg.insert_image(pg.rect, stream=pix.tobytes("jpeg", jpg_quality=90))
    return one


def place(dst, src, i, binding_left, flat=False):
    """Scale to trim height, flush to the outer edge, continue the binding edge.
    flat=True places a 300 dpi raster of the page instead of the vector page."""
    r = src[i].rect
    k = H / r.height
    pw = r.width * k
    gap = W - pw
    p = dst.new_page(width=W, height=H)
    if flat:
        src, i = raster_page(src, i), 0
    if binding_left:                       # recto / front cover: binding on the LEFT
        p.insert_image(pymupdf.Rect(0, 0, gap + 0.6, H), stream=edge_strip(src, i, "left"), keep_proportion=False)
        p.show_pdf_page(pymupdf.Rect(gap, 0, W, H), src, i)
    else:                                  # verso / back cover: binding on the RIGHT
        p.insert_image(pymupdf.Rect(pw - 0.6, 0, W, H), stream=edge_strip(src, i, "right"), keep_proportion=False)
        p.show_pdf_page(pymupdf.Rect(0, 0, pw, H), src, i)


def margins():
    """Live-text clearance on the PRINTED page: the master's text boxes mapped through
    the same scale + outer-edge placement, against BookVault's 20 mm gutter and 5 mm
    trim rules. Returns the worst value per edge with its book page."""
    src = pymupdf.open(MASTER)
    worst = {"gutter": (999, 0), "outer": (999, 0), "top": (999, 0), "bottom": (999, 0)}
    for i in range(1, src.page_count - 1):
        r = src[i].rect
        k = H / r.height
        gap = 216.0 - r.width * k / MM
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


BUILT = pathlib.Path(__file__).resolve().parent.parent / "src" / "_book.built.html"
COVER_IDS = ("s1", "s28")
HERE_COVERS = pathlib.Path(__file__).resolve().parent.parent / "covers"


def covers_native() -> pymupdf.Document:
    """Front and back cover re-rendered by Chromium directly at the 216 x 279 mm trim.
    Scaling A4 covers would either crop them (the front's bottom line falls on the cut)
    or need a smeared strip that shows on cover art. Both covers are full-bleed designs
    anchored to the top and bottom, so they reflow to the new box cleanly."""
    from playwright.sync_api import sync_playwright
    std = HERE_COVERS / "std-covers-letter.pdf"
    if std.exists():                    # house-standard covers, built natively at the trim
        d = pymupdf.open(std)
        assert d.page_count == 2 and abs(d[0].rect.width - W) < 1 and abs(d[0].rect.height - H) < 1
        return d
    out = STAGE / "covers.pdf"
    STAGE.mkdir(parents=True, exist_ok=True)
    keep = ",".join("#" + i for i in COVER_IDS)
    css = ("@page { size: 216mm 279mm; margin: 0; } .page { width: 216mm !important; height: 279mm !important; } "
           f"section.page:not({keep}) {{ display: none !important; }}")
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(BUILT.as_uri(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.emulate_media(media="print")
        pg.add_style_tag(content=css)
        pg.wait_for_timeout(500)
        pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
        b.close()
    d = pymupdf.open(out)
    assert d.page_count == 2, f"cover render gave {d.page_count} pages"
    return d


def place_native(dst, cov, i, flat):
    """A cover page already on the trim: 1:1. Flattened pages keep an invisible text layer,
    so the wrap builder still recognises the back cover (it looks for text markers)."""
    p = dst.new_page(width=W, height=H)
    if flat:
        text = cov[i].get_text()
        p.show_pdf_page(p.rect, raster_page(cov, i), 0)
        p.insert_textbox(pymupdf.Rect(10, 10, W - 10, H - 10), text, fontsize=4, render_mode=3)
    else:
        p.show_pdf_page(p.rect, cov, i)


def stage() -> pathlib.Path:
    src = pymupdf.open(MASTER)
    n = src.page_count
    assert n % 4 == 0, f"master has {n} pages; BookVault's 4n-1 block needs a multiple of 4"
    sys.path.insert(0, str(REPO / "tools"))
    mb = importlib.import_module("make_bookvault_files")
    flat = set()
    for label in mb.transparency_pages(src):       # e.g. "page 3: transparency group"
        flat.add(int(str(label).split()[1].rstrip(":")) - 1)
    print(f"transparency on {len(flat)} master pages -> placed as 300 dpi rasters:", sorted(x + 1 for x in flat))
    cov = covers_native()
    cflat = {int(str(l).split()[1].rstrip(":")) - 1 for l in mb.transparency_pages(cov)}
    out = pymupdf.open()
    place_native(out, cov, 0, flat=0 in cflat)                     # front cover, native trim
    out.new_page(width=W, height=H)                                # blank flyleaf (recto)
    for i in range(1, n - 1):                                      # book p.2 .. p.n-1
        place(out, src, i, binding_left=(i + 1) % 2 == 1, flat=i in flat)
    place_native(out, cov, 1, flat=1 in cflat)                     # back cover, native trim
    d = STAGE / SLUG
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    path = d / "book.pdf"
    out.save(path, garbage=4, deflate=True)
    print(f"staged {out.page_count} pages ({n} in the master + 1 flyleaf) -> {path} ({path.stat().st_size/1e6:.1f} MB)")
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
    shutil.copytree(STAGE / SLUG / "bookvault", dst, ignore=shutil.ignore_patterns(".*"))
    for f in sorted(dst.iterdir()):
        print(f"  {f.name}: {f.stat().st_size/1e6:.1f} MB")
    big = [f.name for f in dst.iterdir() if f.stat().st_size > 95e6]
    if big:
        raise SystemExit(f"files too large for GitHub: {big}")
    print("pack ->", dst)


if __name__ == "__main__":
    w = margins()
    print("printed live-text clearance (mm, book page):", w)
    ok = w["gutter"][0] >= 20 and min(w[e][0] for e in ("outer", "top", "bottom")) >= 5
    print("BookVault margins:", "PASS" if ok else "FAIL")
    if not ok:
        raise SystemExit(1)
    stage()
    build()
