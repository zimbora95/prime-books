#!/usr/bin/env python3
"""Independent check of a built BookVault pack, read from the files.

Deliberately duplicates no code from tools/make_bookvault_files.py logic it is
verifying (only the geometry constants, which come from the guide): it opens the
finished PDFs, measures them and compares sampled interior pages against the
master they came from. Run it after any change to the builder:

    .venv/bin/python tools/verify_bookvault_pack.py y01-physical-education
"""
import pathlib
import sys

import pymupdf

REPO = pathlib.Path(__file__).resolve().parent.parent
TRIM_W, TRIM_H, BLEED = 216.0, 279.0, 3.0
MM = 72.0 / 25.4


def mm(v):
    return round(v / MM, 2)


def ink(page, dpi=36):
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB)
    s = pix.samples
    n = pix.width * pix.height
    white = sum(1 for i in range(0, len(s), 3)
                if s[i] > 245 and s[i + 1] > 245 and s[i + 2] > 245)
    return 1.0 - white / max(1, n)


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
    if n % 12 != 11:
        fails.append(f"{n} pages is not 12n-1")
    if not d[n - 1].get_text().strip():
        print("       last page blank (their barcode lands there)")
    else:
        print("       NOTE: last page carries content; their barcode goes on it")

    md = pymupdf.open(master)
    step = max(1, (n - 12) // 8)
    for i in range(0, min(n - 12, md.page_count - 2), step):
        a, b = ink(d[i]), ink(md[i + 1])
        flag = "" if (b < 0.02 and a < 0.05) or a >= b * 0.8 else "  <-- LOST"
        if flag:
            fails.append(f"page {i + 1}: {a:.1%} ink vs master {b:.1%}{flag}")
        print(f"       p{i + 1:>3} ink {a:6.1%}  master p{i + 2} ink {b:6.1%}{flag}")
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
