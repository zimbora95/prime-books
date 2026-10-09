#!/usr/bin/env python3
"""y05-portuguese — remove every "Cambridge" reference from the book's BACK COVER.

Four surfaces carry this book's back cover:

  page 2    the reader's back cover (standalone page 2 of the flipbook). The
            2026-09-09 d86000f sweep removed the level line here but baked four
            opaque white knockout bars into its full-page raster (rows 172-324
            of the 714x1026 art), re-seated a stray "Student Manual" span on top
            of the title, and left the blurb as the orphan tail
            "tura, escrita, gramática e oralidade".
  pages 3,4 two legacy A4 back-cover pages still carrying the whole
            "Year 5 · Cambridge Primary · Student Manual" line.
  page 134  the designed back cover: a single 880x1265 raster with the text
            baked in as pixels (no text layer). Erased by column interpolation
            and re-set as live Andika. This is the page the wrap cover is
            rendered from, so the wrap derives from the fixed art.

Method for pages 2-4: text is rebuilt from the PRE-SWEEP revision of the same
master (git 1231bbd), whose page art is pixel-identical to today's outside the
sweep damage (verified: page 2 differs only in rows 172-324, pages 3/4 and the
interior differ nowhere). The page text is wiped wholesale and re-typeset from
the pre-sweep span list with the level line replaced by the house standard
"Year 5 · Student Manual". The art itself is restored from the same revision, so
the baked white knockout bars disappear without inpainting.

Run:  .venv/bin/python tools/out/y05pt/fix_back_cambridge.py [--commit]
"""
import argparse
import pathlib
import shutil
import sys
from io import BytesIO

import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = pathlib.Path('/root/prime-books')
WORK = REPO / 'tools' / 'out' / 'y05pt'
DONOR = WORK / 'donor'
OUT = WORK / 'out'
MASTER = REPO / 'public' / 'library' / 'y05-portuguese' / 'book.pdf'
PRE_SWEEP = DONOR / 'y05-portuguese-pre-sweep.pdf'
ASSETS = REPO / 'tools' / 'cover_assets'

FONTS = {
    'Andika': ASSETS / 'Andika-Regular.ttf',
    'Andika-Bold': ASSETS / 'Andika-Bold.ttf',
    'Poppins-SemiBold': ASSETS / 'Poppins-SemiBold.ttf',
    'Poppins-ExtraBold': ASSETS / 'Poppins-ExtraBold.ttf',
    'Poppins-Medium': ASSETS / 'Poppins-Medium.ttf',
    'Poppins-Regular': ASSETS / 'Poppins-Regular.ttf',
}
ALIAS = {name: f'f{name.replace("-", "").lower()}' for name in FONTS}
ANDIKA = FONTS['Andika']

LEVEL = 'Year 5 \u00b7 Student Manual'
# the pre-sweep level line; everything after it in a span is replaced by LEVEL
LEVEL_OLD = 'Year 5 \u00b7 Cambridge Primary \u00b7 Student Manual'


def page_raster(doc, page):
    """The page's first image as a writable HxWx3 numpy array + its xref."""
    xref = page.get_images(full=True)[0][0]
    pix = pymupdf.Pixmap(doc, xref)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return xref, arr[:, :, :3].copy()


def put_raster(page, xref, arr):
    """Replace an image in place with new pixels (PNG, lossless)."""
    buf = BytesIO()
    Image.fromarray(arr).save(buf, 'PNG')
    page.replace_image(xref, stream=buf.getvalue())


def spans_of(page):
    out = []
    for blk in page.get_text('dict')['blocks']:
        if blk['type'] != 0:
            continue
        for line in blk['lines']:
            for span in line['spans']:
                out.append(span)
    return out


def retype(page, span, text):
    font = FONTS[span['font']]
    col = span['color']
    colour = tuple(((col >> s) & 0xFF) / 255 for s in (16, 8, 0))
    page.insert_text((span['origin'][0], span['origin'][1]), text,
                     fontsize=span['size'], fontfile=str(font),
                     fontname=ALIAS[span['font']], color=colour)


def rebuild_from_donor(doc, donor, idx):
    """Wipe page text, restore its art, re-typeset the pre-sweep copy."""
    page, dpage = doc[idx], donor[idx]
    xref, _ = page_raster(doc, page)
    dxref, darr = page_raster(donor, dpage)
    page.add_redact_annot(page.rect)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    put_raster(page, xref, darr)
    n = 0
    for span in spans_of(dpage):
        text = LEVEL if span['text'].startswith('Year 5 \u00b7') else span['text']
        retype(page, span, text)
        n += 1
    return n


def erase_band(arr, y0, y1, x0, x1):
    """Rebuild rows y0..y1 by per-column lerp between the neighbouring rows."""
    top = arr[y0 - 9:y0 - 1, x0:x1].astype(np.float64).mean(0)
    bot = arr[y1 + 2:y1 + 10, x0:x1].astype(np.float64).mean(0)
    for y in range(y0, y1 + 1):
        t = (y - (y0 - 1)) / float((y1 + 1) - (y0 - 1))
        arr[y, x0:x1] = (top * (1 - t) + bot * t).round().astype(np.uint8)
    patch = Image.fromarray(arr[y0 - 4:y1 + 5, x0 - 4:x1 + 4])
    blurred = patch.filter(ImageFilter.GaussianBlur(1.1))
    ring = Image.new('L', patch.size, 0)
    w, h = patch.size
    ring.paste(Image.new('L', (w - 8, h - 8), 255), (4, 4))
    mask = ring.point(lambda v: 0 if v else 255)     # blur only the 4px rim
    arr[y0 - 4:y1 + 5, x0 - 4:x1 + 4] = np.asarray(Image.composite(blurred, patch, mask))
    return arr


def draw_line_pixels(arr, x, baseline, size_pt, text, colour, y0=240, y1=330):
    """Draw a line into the raster itself, supersampled 4x.

    Page 134 is one raster with no text layer, and the wrap-cover builder
    recognises it as the designed back because it is TEXTLESS — so the new line
    has to be pixels, not a live span.
    """
    scale = arr.shape[0] / 828.0            # raster pixels per page point
    big = 4
    font = ImageFont.truetype(str(ANDIKA), int(round(size_pt * scale * big)))
    layer = Image.new('RGBA', (arr.shape[1] * big, (y1 - y0) * big), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((x * big, (baseline - y0) * big), text, font=font,
                               fill=tuple(colour) + (255,), anchor='ls')
    layer = layer.resize((arr.shape[1], y1 - y0), Image.LANCZOS)
    band = Image.fromarray(arr[y0:y1, :, :]).convert('RGBA')
    band.alpha_composite(layer)
    arr[y0:y1, :, :] = np.asarray(band.convert('RGB'))
    return arr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--commit', action='store_true')
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    if not PRE_SWEEP.exists():
        sys.exit(f'missing pre-sweep donor {PRE_SWEEP}')

    doc = pymupdf.open(MASTER)
    donor = pymupdf.open(PRE_SWEEP)
    before = {i: doc[i].get_pixmap(dpi=110).tobytes('png') for i in (1, 2, 3, 133)}

    for idx in (1, 2, 3):
        print(f'  page {idx + 1}: {rebuild_from_donor(doc, donor, idx)} spans re-set')

    # -------------------------------------------------------------- page 134
    # designed back cover: one raster, the level line baked into its pixels.
    # Kept textless on purpose — the wrap builder finds the designed back by
    # being the last TEXTLESS art page of the master.
    page = doc[133]
    xref, arr = page_raster(doc, page)
    erase_band(arr, 268, 298, 120, 494)          # ink was rows 274-290, x 131-480
    draw_line_pixels(arr, 131, 287, 11.0, LEVEL, (107, 107, 94))
    put_raster(page, xref, arr)

    dst = OUT / 'book.pdf'
    doc.subset_fonts()          # keeps the full families from bloating the master
    doc.save(dst, garbage=3, deflate=True)
    doc.close()
    donor.close()

    # ----------------------------------------------------------- verification
    chk = pymupdf.open(dst)
    text = '\n'.join(chk[i].get_text() for i in range(chk.page_count))
    assert 'ambridge' not in text, 'Cambridge still in the text layer'
    assert chk.page_count == 134, chk.page_count
    for idx in (1, 2, 3):
        _, arr = page_raster(chk, chk[idx])
        print(f'  page {idx + 1}: pure-white pixels {int((arr >= 252).all(-1).sum())}'
              f' | text {len(chk[idx].get_text().strip())} chars')
    print(f'  page 134 text: {chk[133].get_text().strip()!r}')
    print(f'  page count {chk.page_count}')
    for idx in (1, 2, 3, 133):
        (WORK / f'after_p{idx + 1}.png').write_bytes(
            chk[idx].get_pixmap(dpi=110).tobytes('png'))
        (WORK / f'before_p{idx + 1}.png').write_bytes(before[idx])
    os_check = [name for name in chk[1].get_fonts() if name[3].startswith('f')]
    print(f'  fonts on page 2: {[f[3] for f in chk[1].get_fonts()]}')
    chk.close()

    if args.commit:
        shutil.move(str(dst), str(MASTER))
        print(f'committed -> {MASTER}')
    else:
        print(f'dry run -> {dst}')


if __name__ == '__main__':
    main()