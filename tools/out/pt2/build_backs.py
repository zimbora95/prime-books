#!/usr/bin/env python3
"""Rebuild the Year 7/8/9 Portuguese 2nd Language back covers onto the current
house back-cover standard (the Year 1/7 Art & Design back: PRIME SCHOOL PRESS
imprint, measured geometry), keeping each book's own back copy.

Why: the Cambridge-line sweep (d86000f) redacted the level line on these backs
with white fills and left the tail of the hook and blurb behind as stray text
("...nicação do dia a dia, textos"), and the same sweep baked four white
knockout bars into the art raster (rows 166-314 of 918, 4.2% of the image).
The pre-sweep revision (1231bbd) has both clean: the art is the series still
life (sailboat, azulejo, pastel de nata, cypress arch), 0.1% white, no text.

Standard geometry (bbox tops, from y07-art-and-design p74 and the verified
y07/8/9-humanities rebuild):
  imprint   x85 top  67.9  Poppins-SemiBold 9.6  #6B6B5E
  title     x85 top  93.4  Poppins-ExtraBold 33  #1A1A1A
  accent    (85,166)-(107,169)                   stripe colour
  subtitle  x85 top 174.6  Andika 11             #6B7D72
  hook      x85 top 200.1  Andika 11.4           #2E2A24
  blurb     x85 top 224.3, +17.2 per line        wrap 438
  card      (71,364.3)-(470,512.3) fill #F2EBDC  radius 0.06
  INSIDE    x87 top 378.8  Poppins-SemiBold 9.4  #5A2409
  bullets   bul x87 / text x101, top 395.7 +19   Andika 10.6 wrap 353
  footer    x85 tops H-74.5 / H-60 / H-42.5, 9pt (bottom-anchored)

    .venv/bin/python tools/out/pt2/build_backs.py <slug>... [--dry-run]
"""
import io
import os
import subprocess
import sys

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

CLEAN_REV = '1231bbd'                      # d86000f^ = before the sweep
WORK = '/root/backwork/pt2'
ART = WORK + '/clean-pt2-back-art.png'

f_title = pymupdf.Font(fontfile=F_TITLE)
f_med = pymupdf.Font(fontfile=F_MED)
f_body = pymupdf.Font(fontfile=F_BODY)

BOOKS = {
    'y07-portuguese-2nd': dict(year=7, ages='Ages 11\u201312', stripe=(26, 94, 104)),
    'y08-portuguese-2nd': dict(year=8, ages='Ages 12\u201313', stripe=(84, 110, 158)),
    'y09-portuguese-2nd': dict(year=9, ages='Ages 13\u201314', stripe=(196, 148, 58)),
}
TITLE = 'Portuguese 2nd'
LEVEL = 'Lower Secondary'


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


def clean_art(slug):
    """Persist the pre-sweep back art once (it is the same raster for all three)."""
    if os.path.exists(ART):
        return Image.open(ART).convert('RGB')
    data = subprocess.run(['git', 'show', '%s:public/library/%s/book.pdf' % (CLEAN_REV, slug)],
                          capture_output=True, cwd=HERE).stdout
    d = pymupdf.open(stream=data, filetype='pdf')
    p = d[-1]
    info = d.extract_image(p.get_images(full=True)[0][0])
    d.close()
    im = Image.open(io.BytesIO(info['image'])).convert('RGB')
    os.makedirs(WORK, exist_ok=True)
    im.save(ART)
    return im


def old_copy(slug):
    """Read the book's own back copy out of the pre-sweep revision."""
    data = subprocess.run(['git', 'show', '%s:public/library/%s/book.pdf' % (CLEAN_REV, slug)],
                          capture_output=True, cwd=HERE).stdout
    d = pymupdf.open(stream=data, filetype='pdf')
    p = d[-1]
    sp = [s for b in p.get_text('dict')['blocks'] if not b['type']
          for l in b['lines'] for s in l['spans'] if s['text'].strip()]
    d.close()
    hook = [s['text'] for s in sp if abs(s['bbox'][1] - 200.1) < 1.5]
    blurb = [s['text'] for s in sp if abs(s['bbox'][0] - 85.0) < 1.5
             and s['bbox'][1] > 220 and s['bbox'][1] < 280]
    bullets = [s['text'] for s in sp if abs(s['bbox'][0] - 101.0) < 1.5]
    if len(hook) != 1 or not 1 <= len(blurb) <= 4 or len(bullets) != 5:
        raise SystemExit('%s: pre-sweep copy does not parse (hook %d blurb %d bullets %d)'
                         % (slug, len(hook), len(blurb), len(bullets)))
    return hook[0], ' '.join(blurb), bullets


def build(slug, spec, art_im, dry_run=False):
    src = os.path.join(HERE, 'public/library/%s/book.pdf' % slug)
    doc = pymupdf.open(src)
    last = doc.page_count - 1
    rect = doc[last].rect
    W, H = rect.width, rect.height
    hook, blurb, bullets = old_copy(slug)
    print('%s: %d pages, %s' % (slug, doc.page_count, '%gx%g' % (W, H)))
    print('   hook    %r' % hook)
    print('   blurb   %r' % blurb)
    print('   bullets %s' % bullets)
    if dry_run:
        doc.close()
        return None

    doc.delete_page(last)
    doc.new_page()
    pno = doc.page_count - 1
    doc[pno].set_mediabox(rect)
    page = doc[pno]                       # re-fetch after the mediabox change

    # --- art, full bleed, aspect preserved (cover fit) ---
    scale = max(W / art_im.width, H / art_im.height)
    aw, ah = art_im.width * scale, art_im.height * scale
    ax, ay = (W - aw) / 2, (H - ah) / 2
    tmp = WORK + '/_art_%s.png' % slug
    art_im.resize((max(1, int(round(aw))), max(1, int(round(ah)))), Image.LANCZOS).save(tmp)
    page.insert_image(pymupdf.Rect(ax, ay, ax + aw, ay + ah), filename=tmp,
                      keep_proportion=True)

    stripe = tuple(c / 255 for c in spec['stripe'])

    # --- spine stripe + accent bar ---
    page.draw_rect(pymupdf.Rect(0, 0, 34.0, H), color=None, fill=stripe)
    page.draw_rect(pymupdf.Rect(85.0, 166.0, 107.0, 169.0), color=None, fill=stripe)

    # --- imprint / title / subtitle ---
    page.insert_text((85.0, baseline(f_med, 9.6, 67.9)), 'P R I M E  S C H O O L  P R E S S',
                     fontsize=9.6, fontname='Poppins-SemiBold', fontfile=F_MED, color=GREY)
    page.insert_text((85.0, baseline(f_title, 33.0, 93.4)), TITLE,
                     fontsize=33.0, fontname='Poppins-ExtraBold', fontfile=F_TITLE, color=INK)
    page.insert_text((85.0, baseline(f_body, 11.0, 174.6)),
                     'Year %d \u00b7 Prime School Press \u00b7 Student Manual' % spec['year'],
                     fontsize=11.0, fontname='Andika', fontfile=F_BODY, color=SUB)

    # --- hook + blurb (the book's own back copy, recovered from the pre-sweep revision) ---
    page.insert_text((85.0, baseline(f_body, 11.4, 200.1)), hook,
                     fontsize=11.4, fontname='Andika', fontfile=F_BODY, color=INKISH)
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
                     fontsize=9.4, fontname='Poppins-SemiBold', fontfile=F_MED, color=BROWN)
    yy = baseline(f_body, 10.6, 395.7)
    for b in bullets:
        page.insert_text((87.0, yy), '\u2022', fontsize=10.6, fontname='Andika',
                         fontfile=F_BODY, color=INKISH)
        first = True
        for ln in wrap(f_body, b, 10.6, 353):
            page.insert_text((101.0, yy), ln, fontsize=10.6, fontname='Andika',
                             fontfile=F_BODY, color=INKISH)
            yy += 19 if first else 15
            first = False

    # --- footer, bottom-anchored at the standard's distances ---
    page.insert_text((85.0, baseline(f_med, 9.0, H - 74.5)), 'Prime School Press \u00b7 ' + TITLE,
                     fontsize=9.0, fontname='Poppins-SemiBold', fontfile=F_MED, color=INK)
    page.insert_text((85.0, baseline(f_body, 9.0, H - 60.0)),
                     '%s \u00b7 %s' % (spec['ages'], LEVEL),
                     fontsize=9.0, fontname='Andika', fontfile=F_BODY, color=GREY)
    page.insert_text((85.0, baseline(f_med, 9.0, H - 42.5)), 'primeschool.pt',
                     fontsize=9.0, fontname='Poppins-SemiBold', fontfile=F_MED, color=TERRA)

    doc.save(src + '.tmp', deflate=True, garbage=4)
    n = doc.page_count
    doc.close()
    os.replace(src + '.tmp', src)
    return n, H


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    slugs = args or list(BOOKS)
    art = clean_art(slugs[0])
    for slug in slugs:
        out = build(slug, BOOKS[slug], art, dry)
        if out:
            print('   rebuilt back: pages=%d H=%.1f' % out)


if __name__ == '__main__':
    main()
