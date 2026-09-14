#!/usr/bin/env python3
"""Independent check of a built BookVault pack, read from the files.

Deliberately duplicates no code from tools/make_bookvault_files.py logic it is
verifying (only the geometry constants, which come from the guide): it opens the
finished PDFs, measures them and compares sampled interior pages against the
master they came from. Run it after any change to the builder:

    .venv/bin/python tools/verify_bookvault_pack.py y01-physical-education
"""
import json
import pathlib
import sys

import pymupdf

REPO = pathlib.Path(__file__).resolve().parent.parent
TRIM_W, TRIM_H, BLEED = 216.0, 279.0, 3.0
MM = 72.0 / 25.4


def mm(v):
    return round(v / MM, 2)


def ink(page, dpi=36):
    """Share of pixels that are not the page's own background colour.

    A fixed "is it white?" test is not safe here: converting to CMYK moves a pale
    tint like the lavender header band from (238,230,249) to (239,229,241), which
    steps across a fixed threshold and reports a page as having lost a third of
    its ink when it is pixel-for-pixel the same page. Comparing against the
    page's modal colour instead measures ink as the eye sees it.
    """
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB)
    s = pix.samples
    step = pix.n
    n = pix.width * pix.height
    hist = {}
    for i in range(0, len(s), step):
        hist[s[i:i + 3]] = hist.get(s[i:i + 3], 0) + 1
    bg = max(hist, key=hist.get)
    ink = sum(1 for i in range(0, len(s), step)
              if max(abs(s[i] - bg[0]), abs(s[i + 1] - bg[1]), abs(s[i + 2] - bg[2])) > 16)
    return ink / max(1, n)


def ink_share(page, dpi=36, thresh=45):
    """Share of near-black pixels -- a masked plate composited on black shows up
    here as a jump against the same page of the master."""
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB)
    s = pix.samples
    n = pix.width * pix.height
    dark = sum(1 for i in range(0, len(s), 3)
               if max(s[i], s[i + 1], s[i + 2]) < thresh)
    return dark / max(1, n)


def masked_images(doc):
    out = []
    for pno in range(doc.page_count):
        for img in doc[pno].get_images(full=True):
            if img[1]:
                out.append((pno + 1, img[0]))
    return out


def marker(path):
    d = pymupdf.open(path)
    ver, intent = "", False
    ref = d.xref_get_key(-1, "Info")
    if ref[0] != "null":
        n = ref[1].split()[0]
        v = d.xref_get_key(int(n), "GTS_PDFXVersion")
        if v[0] != "null":
            ver = v[1].strip("()")
    intent = d.xref_get_key(d.pdf_catalog(), "OutputIntents")[0] != "null"
    d.close()
    return ver, intent


def main(slug):
    od = REPO / "public/library" / slug / "bookvault"
    text = od / f"{slug}-text-file.pdf"
    cover = od / f"{slug}-cover-file.pdf"
    master = REPO / "public/library" / slug / "book.pdf"
    fails = []

    d = pymupdf.open(text)
    n, w, h = d.page_count, mm(d[0].rect.width), mm(d[0].rect.height)
    print(f"text   {n} pages  {w} x {h} mm")
    # 0.2 mm of slack: the cover's size is fixed by whole pixels at 300 DPI, and
    # the interior's by the point grid, so exact equality is not meaningful.
    if abs(w - (TRIM_W + 2 * BLEED)) > 0.2 or abs(h - (TRIM_H + 2 * BLEED)) > 0.2:
        fails.append(f"text media is {w} x {h} mm, want 222.0 x 285.0")
    # The page count is checked against what this pack says it is: the owner asked
    # for no blank pages at the rear, so 12n-1 is only required when it was asked for.
    declared = {}
    bj = od / "build.json"
    if bj.is_file():
        declared = (json.loads(bj.read_text()).get("text") or {})
    content = declared.get("content_pages")
    if declared.get("pad_12n"):
        if n % 12 != 11:
            fails.append(f"{n} pages is not 12n-1, but the pack declares padding")
    elif content is not None and n != content:
        fails.append(f"{n} pages but the pack says {content} content pages and no padding")
    else:
        print(f"       {n} pages, no blank padding: guide p.5 would suggest "
              f"{declared.get('guide_suggested_pages', '?')} for their barcode page")
    if not d[n - 1].get_text().strip():
        print("       last page blank (their barcode lands there)")
    else:
        print("       NOTE: last page carries content; their barcode goes on it")

    masks = masked_images(d)
    if masks:
        fails.append(f"{len(masks)} image(s) still carry a soft mask, e.g. page "
                     f"{masks[0][0]} xref {masks[0][1]} -- flatten them before "
                     f"converting (PDF/X-1a allows no transparency)")
    else:
        print("       no soft-masked images left (artwork pre-composited)")

    # BookVault draws their safety margins over the preview: 20 mm on the gutter
    # (guide p.3, interior files) and 5 mm from the trim on the other three edges
    # (their text template). Read the clearances off the packed pages.
    trim, edge, gutter = 3.0, 999.0, 999.0
    where_e = where_g = ""
    for i in range(n):
        blocks = d[i].get_text("blocks")
        if not blocks:
            continue
        lft = min(x[0] for x in blocks) / MM - trim
        rgt = (d[i].rect.width / MM - trim) - max(x[2] for x in blocks) / MM
        top = min(x[1] for x in blocks) / MM - trim
        bot = (d[i].rect.height / MM - trim) - max(x[3] for x in blocks) / MM
        g = lft if (i + 1) % 2 else rgt          # odd packed pages are right-hand
        if g < gutter:
            gutter, where_g = g, f"page {i + 1}"
        for side, v in (("left", lft), ("right", rgt), ("top", top), ("bottom", bot)):
            if v < edge:
                edge, where_e = v, f"{side} of page {i + 1}"
    print(f"       closest text {gutter:.1f} mm off the gutter ({where_g}), "
          f"{edge:.1f} mm from the trim ({where_e})")
    if gutter < 20.0:
        fails.append(f"text {gutter:.1f} mm off the gutter on {where_g}: their "
                     f"guide asks for 20 mm (guide p.3, interior files)")
    if edge < 5.0:
        fails.append(f"text {edge:.1f} mm from the {where_e}: their template "
                     f"draws a 5 mm trim safety line")

    md = pymupdf.open(master)
    step = max(1, (n - 12) // 8)
    for i in range(0, min(n - 12, md.page_count - 2), step):
        a, b = ink(d[i]), ink(md[i + 1])
        flag = "" if (b < 0.02 and a < 0.05) or a >= b * 0.8 else "  <-- LOST"
        if flag:
            fails.append(f"page {i + 1}: {a:.1%} ink vs master {b:.1%}{flag}")
        da, db = ink_share(d[i]), ink_share(md[i + 1])
        dflag = ""
        if da - db > 0.03:
            dflag = "  <-- DARK BLOCK"
            fails.append(f"page {i + 1}: {da:.1%} near-black vs master {db:.1%}"
                         f"{dflag} (a masked plate printed on its black base?)")
        print(f"       p{i + 1:>3} ink {a:6.1%}  master p{i + 2} ink {b:6.1%}"
              f"  dark {da:5.1%}/{db:5.1%}{flag}{dflag}")
    md.close()
    ver, intent = marker(text)
    print(f"       PDF/X: {ver or '(none - RGB)'}  output intent: {intent}")
    d.close()

    c = pymupdf.open(cover)
    cw, ch = mm(c[0].rect.width), mm(c[0].rect.height)
    spine = round(cw - 2 * TRIM_W - 2 * BLEED, 1)
    print(f"cover  {cw} x {ch} mm  -> implied spine {spine} mm")
    if abs(ch - (TRIM_H + 2 * BLEED)) > 0.2:
        fails.append(f"cover height is {ch} mm, want 285.0")
    if spine < 1 or spine > 40:
        fails.append(f"cover width {cw} mm implies a spine of {spine} mm")
    c.close()

    print("\n" + ("FAIL: " + "; ".join(fails) if fails else "OK: all independent checks passed"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "y01-physical-education"))
