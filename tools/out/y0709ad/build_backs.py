#!/usr/bin/env python3
"""Rebuild the BACK COVER of the Year 7 / 8 / 9 Art & Design books onto the
Prime School Press back-cover standard (reference = the y07-humanities and
y07-spanish backs, which the gate passes).

What was wrong (identical damage on all three, same as the y05/y06 art books):

  * the 2026-09-09 "remove the Cambridge level line" sweep redacted cover lines
    with the default WHITE fill on a page whose background is ONE full-page
    image, so it baked opaque white knockout bars into the artwork (raster rows
    162-305 = page y 139-261: the subtitle / hook / blurb band);
  * the same redaction swallowed the whole subtitle line "Year N · Cambridge
    Lower Secondary · Student Manual", the hook and both blurb lines, leaving
    only the orphan tail " thinking: drawing, colour," at x 354.9;
  * a stray "Student Manual" span was re-seated inside the title's own block;
  * the old template survived: "P R I M E  B O O K S" imprint and
    "Prime Books · Art & Design" footer instead of Prime School Press, and the
    INSIDE THIS BOOK card sat at y 332.6 with its label/bullets 31.7 pt high
    (standard: card 364.3, label 378.8, bullets 395.7 + 19n).

Fix, per book:
  * the page is rebuilt from scratch, so no redaction residue can survive;
  * the artwork is restored 1:1 from the pre-damage revision of the same
    master (git d86000f^) - byte-identical outside the baked bars, no
    inpainting and no re-wash; the three rasters are bit-identical;
  * the standard template is drawn at the measured coordinates of the
    reference backs, and the book's OWN copy (hook, blurb, bullets) is
    re-typeset verbatim from the pre-damage master - never reworded, and the
    Cambridge line is replaced by the house subtitle per the Aug-2026 branding
    rule (covers carry no third-party programme branding).

Run:  .venv/bin/python tools/out/y0709ad/build_backs.py [slug ...]
"""
import hashlib
import io
import pathlib
import shutil
import subprocess
import sys

import pymupdf
from PIL import Image

REPO = pathlib.Path('/root/prime-books')
WORK = REPO / 'tools' / 'out' / 'y0709ad'
ASSETS = REPO / 'tools' / 'cover_assets'
REV = 'd86000f^'

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

SUBJECT = 'Art & Design'
BULLETS = [
    'Skills: drawing, paint, print, 3D',
    'Artists and movements in context',
    'Sketchbook habit and portfolio building',
    'Critique language and reflection',
    'Final project per unit',
]

BOOKS = [
    dict(slug='y07-art-and-design', year=7, ages='Ages 11–12 · Lower Secondary'),
    dict(slug='y08-art-and-design', year=8, ages='Ages 12–13 · Lower Secondary'),
    dict(slug='y09-art-and-design', year=9, ages='Ages 13–14 · Lower Secondary'),
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


def pre_damage(slug):
    """The master as it stood before the sweep: art + the book's own back copy."""
    blob = subprocess.run(['git', 'show', f'{REV}:public/library/{slug}/book.pdf'],
                          cwd=REPO, capture_output=True, check=True).stdout
    doc = pymupdf.open(stream=blob, filetype='pdf')
    art = WORK / 'back_art_pristine.png'
    if not art.exists():
        info = doc.extract_image(doc[-1].get_images(full=True)[0][0])
        Image.open(io.BytesIO(info['image'])).convert('RGB').save(art)
    p = doc[-1]
    spans = [s for b in p.get_text('dict')['blocks'] if b['type'] == 0
             for l in b['lines'] for s in l['spans']]
    txt = [s['text'].strip() for s in spans]
    hook = next(t for t in txt if t.startswith('Every child'))
    lead = next(t for t in txt if 'art and design develops' in t)
    tail = next(t for t in txt if t.startswith('print, 3D and the artists'))
    blurb = lead + ' ' + tail
    stripes = [tuple(round(c, 5) for c in dr['fill'])
               for dr in p.get_drawings() if dr.get('fill')
               and abs(dr['rect'].x0) < 1 and dr['rect'].width < 40]
    doc.close()
    return art, hook, blurb, stripes[0]


def render_hashes(path):
    d = pymupdf.open(path)
    out = [hashlib.md5(d[i].get_pixmap(dpi=50).samples).hexdigest()
           for i in range(d.page_count)]
    d.close()
    return out


def render_page(path, index, dst, zoom=720 / 612.0):
    d = pymupdf.open(path)
    pix = d[index].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(dst)
    d.close()


def build(cfg):
    slug, year, ages = cfg['slug'], cfg['year'], cfg['ages']
    book = REPO / 'public' / 'library' / slug / 'book.pdf'
    art, hook, blurb, stripe = pre_damage(slug)
    print(f"  {slug}: stripe {stripe}  hook {hook!r}")
    print(f"  {slug}: blurb {blurb!r}")
    assert 'Cambridge' not in blurb, blurb

    backup = WORK / f'{slug}-DAMAGED-backup.pdf'
    if not backup.exists():
        shutil.copyfile(book, backup)

    before = render_hashes(book)
    n_before = len(before)
    render_page(str(book), -1, str(WORK / f'{slug}-before.png'))

    doc = pymupdf.open(book)
    n = doc.page_count
    assert n % 2 == 0, n
    doc.delete_page(n - 1)
    page = doc.new_page(pno=doc.page_count, width=612, height=792)
    page.set_mediabox(pymupdf.Rect(0, 0, 612, 792))

    # ---- artwork, full bleed, 1:1 (this book's own back art) ----
    page.insert_image(pymupdf.Rect(0, 0, 612, 792), filename=str(art),
                      keep_proportion=False)

    # ---- spine stripe + accent rule, in the book's own year colour ----
    page.draw_rect(pymupdf.Rect(0, 0, 34, 792), color=None, fill=stripe)
    page.draw_rect(pymupdf.Rect(85, 166, 107, 169), color=None, fill=stripe)

    x0 = 85.0
    page.insert_text((x0, 78), 'P R I M E  S C H O O L  P R E S S', fontsize=9.6,
                     fontname='med', fontfile=F_MED, color=GREY)
    page.insert_text((x0, 128), SUBJECT, fontsize=33.0,
                     fontname='ttl', fontfile=F_TTL, color=INK)
    page.insert_text((x0, 188), f'Year {year} · Prime School Press · Student Manual',
                     fontsize=11.0, fontname='body', fontfile=F_BODY, color=SUBTLE)
    page.insert_text((x0, 214), hook, fontsize=11.4, fontname='body',
                     fontfile=F_BODY, color=INKISH)
    y = 238.2
    for ln in wrap(blurb, f_body, 11.4, 438):
        page.insert_text((x0, y), ln, fontsize=11.4, fontname='body',
                         fontfile=F_BODY, color=INKISH)
        y += 17.2

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
    page.insert_text((x0, 727), f'Prime School Press · {SUBJECT}', fontsize=9.0,
                     fontname='med', fontfile=F_MED, color=INK)
    page.insert_text((x0, 743), ages, fontsize=9.0, fontname='body',
                     fontfile=F_BODY, color=GREY)
    page.insert_text((x0, 759), 'primeschool.pt', fontsize=9.0, fontname='med',
                     fontfile=F_MED, color=TERRA)

    doc.subset_fonts()
    out = WORK / f'{slug}-book_new.pdf'
    doc.save(str(out), deflate=True, garbage=4)
    doc.close()

    # ---------------- verification ----------------
    chk = pymupdf.open(str(out))
    back = chk[-1]
    txt = back.get_text()
    joined = ' '.join(txt.split())
    flat = joined.replace(' ', '')          # wrapping- and spacing-insensitive

    def has(s):
        return s.replace(' ', '') in flat

    for must in ['P R I M E  S C H O O L  P R E S S', SUBJECT,
                 f'Year {year} · Prime School Press · Student Manual', hook,
                 blurb, BULLETS[0], BULLETS[-1], 'INSIDE THIS BOOK',
                 f'Prime School Press · {SUBJECT}', ages, 'primeschool.pt']:
        assert has(must), f'{slug} MISSING {must!r}'
    assert not has('P R I M E  B O O K S') or has('P R I M E  S C H O O L  P R E S S'), slug
    assert not has('P R I M E B O O K S'), slug
    assert 'Cambridge' not in txt, slug
    assert '\x00' not in txt, slug
    assert txt.count('Student Manual') == 1, f"{slug}: stray Student Manual"
    spans = [s for b in back.get_text('dict')['blocks'] if b['type'] == 0
             for l in b['lines'] for s in l['spans']]
    fams = sorted({s['font'] for s in spans})
    print(f'  {slug}: back fonts {fams}')
    assert len(fams) == 3, fams
    type3 = [f for f in back.get_fonts(full=True) if f[2] == 'Type3']
    assert not type3, type3
    # geometry: the standard coordinates of the reference backs
    WANT = [('P R I M E', 67.9), ('Art & Design', 93.4),
            (f'Year {year} · Prime School Press', 174.6), (hook, 200.1),
            ('INSIDE THIS BOOK', 378.8)]
    for needle, top in WANT:
        s = next(s for s in spans if s['text'].startswith(needle))
        assert abs(s['bbox'][1] - top) <= 0.6, (needle, s['bbox'][1], top)
    bars = [round(d['rect'].y0) for d in back.get_drawings() if d.get('fill')
            and d['rect'].width < 60 and 1.5 < d['rect'].height < 5]
    cards = [round(d['rect'].y0) for d in back.get_drawings() if d.get('fill')
             and d['rect'].width > 250 and d['rect'].height > 100]
    assert 166 in bars, bars
    assert cards and abs(cards[0] - 364) <= 1, cards
    pages = chk.page_count
    after = render_hashes(str(out))
    chk.close()
    assert pages == n_before, (pages, n_before)
    changed = [i + 1 for i, (a, b) in enumerate(zip(before, after)) if a != b]
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
