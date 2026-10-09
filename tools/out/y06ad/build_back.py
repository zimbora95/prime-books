"""Rebuild the back cover of y06-art-and-design onto the Prime Books house
standard (Standard A 2.0, back-cover reference = the Year 3 / Year 4 Art & Design
backs), and restore the back copy that the 2026-09-09 "remove Cambridge line"
sweep destroyed.

What was wrong with the shipped page 98:
  * a redaction with the default white fill, applied to a page whose background
    is ONE full-page image, baked four opaque white knockout bars into the art
    (page y 138-260) and deleted the subtitle, the hook and both blurb lines --
    only the orphan tail "topics across" was left behind;
  * a stray "Student Manual" span re-seated inside the title's own bbox;
  * the old template: PRIME BOOKS imprint, no "Prime School Press" subtitle,
    footer at y 690.5 instead of the standard 717.5, card 430 wide instead of 470.

Art is restored from the pre-damage revision of the same master (git d920f88),
byte-identical to the shipped raster everywhere outside the baked bars -- no
inpainting and no re-wash, the book keeps its own art at 1:1.

Run:  .venv/bin/python tools/out/y06ad/build_back.py
"""
import hashlib
import io
import pathlib
import shutil
import sys

import pymupdf
from PIL import Image

REPO = pathlib.Path('/root/prime-books')
sys.path.insert(0, str(REPO))
WORK = REPO / 'tools' / 'out' / 'y06ad'
ASSETS = REPO / 'tools' / 'cover_assets'
BOOK = REPO / 'public' / 'library' / 'y06-art-and-design' / 'book.pdf'
PRISTINE = WORK / 'back_art_pristine.png'

F_TTL = str(ASSETS / 'Poppins-ExtraBold.ttf')
F_MED = str(ASSETS / 'Poppins-SemiBold.ttf')
F_BODY = str(ASSETS / 'Andika-Regular.ttf')

CREAM = (249 / 255, 245 / 255, 234 / 255)
SAND = (0xF2 / 255, 0xEB / 255, 0xDC / 255)
INK = (0x1A / 255,) * 3
GREY = (0x6B / 255, 0x6B / 255, 0x5E / 255)
SUBTLE = (0x6B / 255, 0x7D / 255, 0x72 / 255)
BROWN = (0x5A / 255, 0x24 / 255, 0x09 / 255)
TERRA = (0x7C / 255, 0x40 / 255, 0x22 / 255)
INKISH = (0x2E / 255, 0x2A / 255, 0x24 / 255)
STRIPE = (0x83 / 255, 0x5F / 255, 0xC1 / 255)      # Year 6 stripe #835FC1

YEAR = 6
SUBJECT = 'Art & Design'
AGES = 'Ages 10–11 · Upper Primary'
HOOK = 'Welcome to the Loft Studio.'
BLURB = ('The last studio of primary school, and the most independent. Twenty '
         'topics across four units, a portfolio that is yours alone, and an '
         'exhibition to finish.')
BULLETS = [
    'Twenty topics across four units',
    'The most independent making yet',
    'A modelled making in every topic',
    'A portfolio that is yours alone',
    'An exhibition of your own to finish',
]

f_title = pymupdf.Font(fontfile=F_TTL)
f_med = pymupdf.Font(fontfile=F_MED)
f_body = pymupdf.Font(fontfile=F_BODY)


def tw(font, text, size):
    return font.text_length(text, fontsize=size)


def wrap(text, font, size, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if tw(font, t, size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def recover_art():
    """The pristine raster: extract the back-page image from the pre-damage
    revision of this same master (git d920f88)."""
    import subprocess
    if not PRISTINE.exists():
        blob = subprocess.run(['git', 'show', 'd920f88:public/library/y06-art-and-design/book.pdf'],
                              cwd=REPO, capture_output=True, check=True).stdout
        pre = pymupdf.open(stream=blob, filetype='pdf')
        info = pre.extract_image(pre[-1].get_images(full=True)[0][0])
        Image.open(io.BytesIO(info['image'])).convert('RGB').save(PRISTINE)
        pre.close()
    return PRISTINE


def render_hashes(path):
    d = pymupdf.open(path)
    out = []
    for i in range(d.page_count):
        pix = d[i].get_pixmap(dpi=50)
        out.append(hashlib.md5(pix.samples).hexdigest())
    d.close()
    return out


def main():
    art = recover_art()
    before = render_hashes(BOOK)

    doc = pymupdf.open(BOOK)
    n = doc.page_count
    assert n == 98 and n % 2 == 0, n
    doc.delete_page(n - 1)
    page = doc.new_page(pno=doc.page_count, width=612, height=792)
    page.set_mediabox(pymupdf.Rect(0, 0, 612, 792))

    # ---- art, full bleed, 1:1 (no wash: this is the book's own watermark) ----
    page.insert_image(pymupdf.Rect(0, 0, 612, 792), filename=str(art),
                      keep_proportion=False)

    # ---- spine stripe + accent bar in the Year 6 colour ----
    page.draw_rect(pymupdf.Rect(0, 0, 34, 792), color=None, fill=STRIPE)
    page.draw_rect(pymupdf.Rect(85, 166, 107, 169), color=None, fill=STRIPE)

    x0 = 85.0
    # ---- imprint, title ----
    page.insert_text((x0, 78), 'P R I M E  S C H O O L  P R E S S', fontsize=9.6,
                     fontname='med', fontfile=F_MED, color=GREY)
    page.insert_text((x0, 128), SUBJECT, fontsize=33.0,
                     fontname='ttl', fontfile=F_TTL, color=INK)
    # ---- subtitle ----
    page.insert_text((x0, 188), f'Year {YEAR} · Prime School Press · Student Manual',
                     fontsize=11.0, fontname='body', fontfile=F_BODY, color=SUBTLE)
    # ---- hook + blurb ----
    page.insert_text((x0, 214), HOOK, fontsize=11.4, fontname='body',
                     fontfile=F_BODY, color=INKISH)
    y = 238.2
    for ln in wrap(BLURB, f_body, 11.4, 438):
        page.insert_text((x0, y), ln, fontsize=11.4, fontname='body',
                         fontfile=F_BODY, color=INKISH)
        y += 17.2

    # ---- INSIDE THIS BOOK card (standard 71,364.3 - 470,512.3) ----
    card = page.new_shape()
    card.draw_rect(pymupdf.Rect(71, 364.3, 470, 512.3), radius=0.06)
    card.finish(color=None, fill=SAND)
    card.commit()
    page.insert_text((87, 388.3), 'INSIDE THIS BOOK', fontsize=9.4, fontname='med',
                     fontfile=F_MED, color=BROWN)
    yy = 408.3
    for bl in BULLETS:
        page.insert_text((87, yy), '•', fontsize=10.6, fontname='body',
                         fontfile=F_BODY, color=INKISH)
        first = True
        for ln in wrap(bl, f_body, 10.6, 353):
            page.insert_text((101, yy), ln, fontsize=10.6, fontname='body',
                             fontfile=F_BODY, color=INKISH)
            yy += 19 if first else 15
            first = False
    # ---- footer ----
    page.insert_text((x0, 727), 'Prime School Press · Art & Design', fontsize=9.0,
                     fontname='med', fontfile=F_MED, color=INK)
    page.insert_text((x0, 743), AGES, fontsize=9.0, fontname='body',
                     fontfile=F_BODY, color=GREY)
    page.insert_text((x0, 759), 'primeschool.pt', fontsize=9.0, fontname='med',
                     fontfile=F_MED, color=TERRA)

    doc.subset_fonts()
    out = WORK / 'book_new.pdf'
    doc.save(str(out), deflate=True, garbage=4)
    doc.close()

    # ---- verification ----
    chk = pymupdf.open(out)
    txt = chk[-1].get_text()
    for must in ['P R I M E  S C H O O L  P R E S S', 'Art & Design',
                 'Year 6 · Prime School Press · Student Manual', HOOK,
                 'Twenty topics across four units', 'four units, a portfolio',
                 'INSIDE THIS BOOK', 'Prime School Press · Art & Design',
                 'Ages 10–11 · Upper Primary', 'primeschool.pt']:
        assert must in txt, 'MISSING: ' + must
    assert 'P R I M E  B O O K S' not in txt
    assert 'Cambridge' not in txt
    # the blurb must be whole again, wrapping exactly as the pre-damage master did
    assert ('The last studio of primary school, and the most independent. Twenty topics across\n'
            'four units, a portfolio that is yours alone, and an exhibition to finish.' in txt)
    pages = chk.page_count
    after = render_hashes(out)
    chk.close()
    assert pages == len(before), (pages, len(before))
    changed = [i + 1 for i, (a, b) in enumerate(zip(before, after)) if a != b]
    print('page count', pages)
    print('pages whose render changed:', changed, '(expected [98])')
    assert changed == [98], changed

    lw = pymupdf.open(out)[-1]
    fonts = lw.get_fonts(full=True)
    fams = sorted({f[3] for f in fonts})
    print('back-page fonts:', fams)
    print('type3 on back:', [f for f in fonts if f[2] == 'Type3'])
    for f in ('Poppins ExtraBold', 'Poppins SemiBold', 'Andika Regular'):
        assert any(f in x for x in fams), f
    print('blurb wraps as:')
    for ln in wrap(BLURB, f_body, 11.4, 438):
        print('   ', repr(ln))

    shutil.copyfile(WORK / 'book_new.pdf', BOOK)
    print('WROTE', BOOK, BOOK.stat().st_size)


if __name__ == '__main__':
    main()
