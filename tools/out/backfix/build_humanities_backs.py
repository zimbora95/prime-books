#!/usr/bin/env python3
"""Rebuild the Year 7/8/9 Humanities back covers onto the current house
back-cover standard (the Year 1 Art & Design back: PRIME SCHOOL PRESS
imprint, measured geometry) while keeping each book's own back copy.

Verified reference (y01-art-and-design, page coords, bbox tops):
  imprint   x85 top  67.9  Poppins-SemiBold 9.6  #6B6B5E
  title     x85 top  93.4  Poppins-ExtraBold 33  #1A1A1A
  accent    (85,166)-(107,169)                   stripe colour
  subtitle  x85 top 174.6  Andika 11             #6B7D72
  hook      x85 top 200.1  Andika 11.4           #2E2A24
  blurb     x85 top 224.3, +17.2 per line        wrap 438
  card      (71,364.3)-(470,512.3) fill #F2EBDC  radius 0.06
  INSIDE    x87 top 378.8  Poppins-SemiBold 9.4  #5A2409
  bullets   bul x87 / text x101, top 395.7 +19   Andika 10.6 wrap 353
  footer    x85 tops H-74.5 / H-60 / H-42.5, 9pt
On the primary (US Letter, H=792) books those footer tops are 717.5/732.0/
749.5; the footer is bottom-anchored, so on these A4-height (H=765) books it
lands at 690.5 / 705.0 / 722.5 - which is exactly where their old template
already put it.

Art: the back art raster is reused at 1:1 (no re-wash) from the pre-sweep
revision (d86000f^) where the Cambridge sweep left white knockout bars baked
into the raster. y07/y09 pre-sweep rasters are bit-identical; y08's differs
only inside the sweep damage band (page y 138-262), so the same clean raster
restores it.
"""
import io
import shutil
import sys

import numpy as np
import pymupdf
from PIL import Image

HERE = '/root/prime-books'
ASSETS = HERE + '/tools/cover_assets'
F_TITLE = ASSETS + '/Poppins-ExtraBold.ttf'
F_MED = ASSETS + '/Poppins-SemiBold.ttf'
F_BODY = ASSETS + '/Andika-Regular.ttf'

GREY = (0x6B / 255, 0x6B / 255, 0x5E / 255)
INK = (0x1A / 255,) * 3
INKISH = (0x2E / 255, 0x2A / 255, 0x24 / 255)
BROWN = (0x5A / 255, 0x24 / 255, 0x09 / 255)
SUB = (0x6B / 255, 0x7D / 255, 0x72 / 255)
TERRA = (0x7C / 255, 0x3F / 255, 0x22 / 255)
SAND = (0xF2 / 255, 0xEB / 255, 0xDC / 255)

f_title = pymupdf.Font(fontfile=F_TITLE)
f_med = pymupdf.Font(fontfile=F_MED)
f_body = pymupdf.Font(fontfile=F_BODY)

PRESWEEP = '/root/backwork/%s-presweep.pdf'
CLEAN_ART = '/root/backwork/clean-humanities-back-art.png'

BULLETS = [
    'History: sources and enquiry',
    'Geography: maps, place and process',
    'Citizenship and global issues',
    'Skills practice: sources, data, essays',
    'Unit reviews with model answers',
]

BOOKS = [
    dict(slug='y07-humanities', year=7, ages='Ages 11\u201312', level='Lower Secondary',
         stripe=(26, 94, 104)),
    dict(slug='y08-humanities', year=8, ages='Ages 12\u201313', level='Lower Secondary',
         stripe=(84, 110, 158)),
    dict(slug='y09-humanities', year=9, ages='Ages 13\u201314', level='Lower Secondary',
         stripe=(196, 148, 58)),
]


def wrap(font, text, size, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if font.text_length(t, fontsize=size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def baseline(font, size, top):
    """bbox top -> baseline, using the font's own ascender."""
    return top + font.ascender * size


def clean_art():
    """Persist the clean (pre-sweep) back art once."""
    d = pymupdf.open(PRESWEEP % 'y07-humanities')
    p = d[-1]
    info = d.extract_image(p.get_images(full=True)[0][0])
    im = Image.open(io.BytesIO(info['image'])).convert('RGB')
    im.save(CLEAN_ART)
    d.close()
    return im


def build(spec, art_im):
    slug = spec['slug']
    src = 'public/library/%s/book.pdf' % slug
    doc = pymupdf.open(src)
    last = doc.page_count - 1
    rect = doc[last].rect
    W, H = rect.width, rect.height

    # --- the page that is replaced must be the LAST one (back cover) ---
    doc.delete_page(last)
    doc.new_page()
    pno = doc.page_count - 1
    page = doc[pno]
    page.set_mediabox(rect)
    page = doc[pno]  # re-fetch after mediabox change

    # --- art, full bleed, 1:1 (already aspect-matched: 714 x 1.2*H) ---
    art = art_im.resize((714, int(round(714 * H / W))), Image.LANCZOS)
    art.save('/root/backwork/_art_%s.png' % slug)
    page.insert_image(pymupdf.Rect(0, 0, W, H),
                      filename='/root/backwork/_art_%s.png' % slug,
                      keep_proportion=False)

    stripe = tuple(c / 255 for c in spec['stripe'])

    # --- spine stripe + accent bar ---
    page.draw_rect(pymupdf.Rect(0, 0, 34.0, H), color=None, fill=stripe)
    page.draw_rect(pymupdf.Rect(85.0, 166.0, 107.0, 169.0), color=None, fill=stripe)

    # --- imprint / title / subtitle ---
    page.insert_text((85.0, baseline(f_med, 9.6, 67.9)),
                     'P R I M E  S C H O O L  P R E S S',
                     fontsize=9.6, fontname='Poppins-SemiBold', fontfile=F_MED,
                     color=GREY)
    page.insert_text((85.0, baseline(f_title, 33.0, 93.4)), 'Humanities',
                     fontsize=33.0, fontname='Poppins-ExtraBold', fontfile=F_TITLE,
                     color=INK)
    page.insert_text((85.0, baseline(f_body, 11.0, 174.6)),
                     'Year %d \u00b7 Prime School Press \u00b7 Student Manual' % spec['year'],
                     fontsize=11.0, fontname='Andika', fontfile=F_BODY, color=SUB)

    # --- hook + blurb (the book's own back copy, recovered from pre-sweep) ---
    hook = 'Learn to read the world.'
    blurb = ('Year %d humanities weaves history, geography and citizenship into one '
             'course: sources, maps, case studies and big questions about people and '
             'place.' % spec['year'])
    by = baseline(f_body, 11.4, 200.1)
    page.insert_text((85.0, by), hook, fontsize=11.4, fontname='Andika',
                     fontfile=F_BODY, color=INKISH)
    by = baseline(f_body, 11.4, 224.3)
    for ln in wrap(f_body, blurb, 11.4, 438):
        page.insert_text((85.0, by), ln, fontsize=11.4, fontname='Andika',
                         fontfile=F_BODY, color=INKISH)
        by += 17.2

    # --- INSIDE THIS BOOK card (standard rect) ---
    card = pymupdf.Rect(71.0, 364.3, 470.0, 512.3)
    sh = page.new_shape()
    sh.draw_rect(card, radius=0.06)
    sh.finish(color=None, fill=SAND)
    sh.commit()
    page.insert_text((87.0, baseline(f_med, 9.4, 378.8)), 'INSIDE THIS BOOK',
                     fontsize=9.4, fontname='Poppins-SemiBold', fontfile=F_MED,
                     color=BROWN)
    yy = baseline(f_body, 10.6, 395.7)
    for b in BULLETS:
        page.insert_text((87.0, yy), '\u2022', fontsize=10.6, fontname='Andika',
                         fontfile=F_BODY, color=INKISH)
        first = True
        for ln in wrap(f_body, b, 10.6, 353):
            page.insert_text((101.0, yy), ln, fontsize=10.6, fontname='Andika',
                             fontfile=F_BODY, color=INKISH)
            yy += 19 if first else 15
            first = False
        if first:  # nothing drawn (impossible) - keep the ladder aligned
            yy += 19

    # --- footer, bottom-anchored at the standard's distances (Letter: 74.5/60/42.5) ---
    page.insert_text((85.0, baseline(f_med, 9.0, H - 74.5)),
                     'Prime School Press \u00b7 Humanities',
                     fontsize=9.0, fontname='Poppins-SemiBold', fontfile=F_MED,
                     color=INK)
    page.insert_text((85.0, baseline(f_body, 9.0, H - 60.0)),
                     '%s \u00b7 %s' % (spec['ages'], spec['level']),
                     fontsize=9.0, fontname='Andika', fontfile=F_BODY, color=GREY)
    page.insert_text((85.0, baseline(f_med, 9.0, H - 42.5)), 'primeschool.pt',
                     fontsize=9.0, fontname='Poppins-SemiBold', fontfile=F_MED,
                     color=TERRA)

    out = '/root/backwork/%s-book-NEW.pdf' % slug
    doc.save(out, deflate=True, garbage=4)
    n = doc.page_count
    doc.close()
    return out, n, H


def main():
    art = clean_art()
    for spec in BOOKS:
        out, n, H = build(spec, art)
        print('built %-18s pages=%d H=%.1f -> %s' % (spec['slug'], n, H, out))


if __name__ == '__main__':
    main()
