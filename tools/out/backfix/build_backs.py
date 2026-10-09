#!/usr/bin/env python3
"""Rebuild the back cover of three damaged Y5/Y6 titles onto the Prime School
Press back-cover standard (the reference is the Year 1 Art & Design back).

The three shipped backs (y05-art-and-design, y05-global-perspectives,
y06-global-perspectives) were mangled by the 2026-09-09 "remove the Cambridge
level line" sweep: a redaction with the default white fill, applied to a page
whose background is ONE full-page image, baked opaque white knockout bars into
the art, swallowed whole lines of the blurb, deleted the subtitle (leaving a
stray "Student Manual" span inside the title on y05-ad, and a tofu run on the
two Global Perspectives backs), and left the old template behind (PRIME BOOKS
imprint, footer at y 690.5 instead of the standard 717.5, card 430 wide
instead of 470).

Fix, per book:
  * art restored 1:1 from the pre-damage revision of the same master (byte
    identical outside the baked bars -- verified, no inpainting, no re-wash);
  * the page rebuilt from scratch, so no redaction residue can survive;
  * the standard template drawn as vectors at the measured coordinates of the
    Year 1 Art & Design back;
  * the book's OWN back copy (hook / blurb / bullets) restored from
    tools/cover_assets/back_copy.json -- re-typeset, never reworded.

Run:  .venv/bin/python tools/out/backfix/build_backs.py [slug ...]
"""
import hashlib
import io
import json
import pathlib
import shutil
import subprocess
import sys

import pymupdf
from PIL import Image

REPO = pathlib.Path('/root/prime-books')
WORK = REPO / 'tools' / 'out' / 'backfix'
ASSETS = REPO / 'tools' / 'cover_assets'
COPY = json.loads((ASSETS / 'back_copy.json').read_text())['copy']

F_TTL = str(ASSETS / 'Poppins-ExtraBold.ttf')
F_MED = str(ASSETS / 'Poppins-SemiBold.ttf')
F_BODY = str(ASSETS / 'Andika-Regular.ttf')

SAND = (0xF2 / 255, 0xEB / 255, 0xDC / 255)
INK = (0x1A / 255,) * 3
GREY = (0x6B / 255, 0x6B / 255, 0x5E / 255)
SUBTLE = (0x6B / 255, 0x7D / 255, 0x72 / 255)
BROWN = (0x5A / 255, 0x24 / 255, 0x09 / 255)
TERRA = (0x7C / 255, 0x40 / 255, 0x22 / 255)
INKISH = (0x2E / 255, 0x2A / 255, 0x24 / 255)

# stripe colours come from cover_meta.json (the year colour); the page's own
# stripe fill was read back and matches in every case.
STRIPE_Y5 = (0xC3 / 255, 0x24 / 255, 0x80 / 255)     # #C32480
STRIPE_Y6 = (0x83 / 255, 0x5F / 255, 0xC1 / 255)     # #835FC1

BOOKS = [
    dict(slug='y05-art-and-design', year=5, subject='Art & Design',
         ages='Ages 9–10 · Upper Primary', stripe=STRIPE_Y5, rev='1231bbd'),
    dict(slug='y05-global-perspectives', year=5, subject='Global Perspectives',
         ages='Ages 9–10 · Upper Primary', stripe=STRIPE_Y5, rev='1231bbd'),
    dict(slug='y06-global-perspectives', year=6, subject='Global Perspectives',
         ages='Ages 10–11 · Upper Primary', stripe=STRIPE_Y6, rev='d920f88'),
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


def pristine_art(slug, rev):
    """The back-page image of this master as it stood before the damage."""
    out = WORK / f'{slug}-art.png'
    if not out.exists():
        blob = subprocess.run(['git', 'show', f'{rev}:public/library/{slug}/book.pdf'],
                              cwd=REPO, capture_output=True, check=True).stdout
        pre = pymupdf.open(stream=blob, filetype='pdf')
        info = pre.extract_image(pre[-1].get_images(full=True)[0][0])
        Image.open(io.BytesIO(info['image'])).convert('RGB').save(out)
        pre.close()
    return out


def render_hashes(path):
    d = pymupdf.open(path)
    out = [hashlib.md5(d[i].get_pixmap(dpi=50).samples).hexdigest()
           for i in range(d.page_count)]
    d.close()
    return out


def render_page(path, index, dst, zoom=720 / 612.0):
    d = pymupdf.open(path)
    p = d[index]
    pix = p.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(dst)
    d.close()


def build(cfg):
    slug = cfg['slug']
    book = REPO / 'public' / 'library' / slug / 'book.pdf'
    cp = COPY[slug]
    art = pristine_art(slug, cfg['rev'])
    before_hashes = render_hashes(book)
    n_before = len(before_hashes)
    render_page(str(book), -1, str(WORK / f'{slug}-before.png'))

    doc = pymupdf.open(book)
    n = doc.page_count
    assert n % 2 == 0, n
    doc.delete_page(n - 1)
    page = doc.new_page(pno=doc.page_count, width=612, height=792)
    page.set_mediabox(pymupdf.Rect(0, 0, 612, 792))

    # ---- art, full bleed, 1:1 (the book keeps its own watermark) ----
    page.insert_image(pymupdf.Rect(0, 0, 612, 792), filename=str(art),
                      keep_proportion=False)

    # ---- spine stripe + accent bar, in the year colour ----
    page.draw_rect(pymupdf.Rect(0, 0, 34, 792), color=None, fill=cfg['stripe'])
    page.draw_rect(pymupdf.Rect(85, 166, 107, 169), color=None, fill=cfg['stripe'])

    x0 = 85.0
    # ---- imprint + title ----
    page.insert_text((x0, 78), 'P R I M E  S C H O O L  P R E S S', fontsize=9.6,
                     fontname='med', fontfile=F_MED, color=GREY)
    page.insert_text((x0, 128), cfg['subject'], fontsize=33.0,
                     fontname='ttl', fontfile=F_TTL, color=INK)
    # ---- subtitle ----
    page.insert_text((x0, 188), f"Year {cfg['year']} · Prime School Press · Student Manual",
                     fontsize=11.0, fontname='body', fontfile=F_BODY, color=SUBTLE)
    # ---- hook + blurb ----
    page.insert_text((x0, 214), cp['hook'], fontsize=11.4, fontname='body',
                     fontfile=F_BODY, color=INKISH)
    y = 238.2
    lines = wrap(cp['blurb'], f_body, 11.4, 438)
    for ln in lines:
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
    for bl in cp['bullets']:
        page.insert_text((87, yy), '•', fontsize=10.6, fontname='body',
                         fontfile=F_BODY, color=INKISH)
        first = True
        for ln in wrap(bl, f_body, 10.6, 353):
            page.insert_text((101, yy), ln, fontsize=10.6, fontname='body',
                             fontfile=F_BODY, color=INKISH)
            yy += 19 if first else 15
            first = False
    # ---- footer, at the standard baselines ----
    page.insert_text((x0, 727), f"Prime School Press · {cfg['subject']}", fontsize=9.0,
                     fontname='med', fontfile=F_MED, color=INK)
    page.insert_text((x0, 743), cfg['ages'], fontsize=9.0, fontname='body',
                     fontfile=F_BODY, color=GREY)
    page.insert_text((x0, 759), 'primeschool.pt', fontsize=9.0, fontname='med',
                     fontfile=F_MED, color=TERRA)

    out = WORK / f'{slug}-book_new.pdf'
    doc.save(str(out), deflate=True, garbage=4)
    doc.close()

    # ---------- verification ----------
    chk = pymupdf.open(str(out))
    back = chk[-1]
    txt = back.get_text()
    for must in ['P R I M E  S C H O O L  P R E S S', cfg['subject'],
                 f"Year {cfg['year']} · Prime School Press · Student Manual",
                 cp['hook'], cp['bullets'][0], cp['bullets'][-1],
                 'INSIDE THIS BOOK', f"Prime School Press · {cfg['subject']}",
                 cfg['ages'], 'primeschool.pt']:
        assert must in txt, f'{slug} MISSING: {must}'
    assert 'P R I M E  B O O K S' not in txt, slug
    assert 'Cambridge' not in txt, slug
    assert '\x00' not in txt, slug
    # the whole blurb, wrapped as the pre-damage master wrapped it
    joined = ' '.join(txt.split())
    assert cp['blurb'].replace('  ', ' ') in joined, slug
    spans = [s for b in back.get_text('dict')['blocks'] if b['type'] == 0
             for l in b['lines'] for s in l['spans']]
    fams = sorted({s['font'] for s in spans})
    print(f'  {slug}: back fonts {fams}')
    assert len(fams) == 3, fams
    assert all(any(k in f for k in ('Poppins SemiBold', 'Poppins ExtraBold',
                                   'Andika Regular', 'Poppins-SemiBold',
                                   'Poppins-ExtraBold', 'Andika')) for f in fams)
    pages = chk.page_count
    after_hashes = render_hashes(str(out))
    chk.close()
    assert pages == n_before, (pages, n_before)
    changed = [i + 1 for i, (a, b) in enumerate(zip(before_hashes, after_hashes)) if a != b]
    print(f'  {slug}: {pages} pages, renders changed: {changed}')
    assert changed == [pages], changed

    shutil.copyfile(out, book)
    render_page(str(book), -1, str(WORK / f'{slug}-after.png'))
    print(f'  {slug}: WROTE {book} ({book.stat().st_size} bytes)')


def main(argv):
    WORK.mkdir(parents=True, exist_ok=True)
    only = [a for a in argv[1:] if not a.startswith('-')]
    for cfg in BOOKS:
        if only and cfg['slug'] not in only:
            continue
        print('==', cfg['slug'])
        build(cfg)


if __name__ == '__main__':
    main(sys.argv)
