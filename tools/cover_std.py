#!/usr/bin/env python3
"""Standardized Prime Books covers for Years 1-6 (Beatrix Potter styling).

Front template: y01-computing-and-robotics (cream bg, left stripe, Prime Books
logo, Arial-Bold title block top-left, watercolour art lower ~59%).
Back template: y02-computing-and-robotics (sepia bg art, left stripe, PRIME
BOOKS + title, blurb, INSIDE THIS BOOK sand card, footer, barcode).

All text is live (Poppins/Andika embedded), positioned identically on every
book so future standardization is byte-consistent.
"""
import json, math, os, sys
import pymupdf
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'cover_assets')
FONT_TITLE = os.path.join(ASSETS, 'Poppins-ExtraBold.ttf')
FONT_TITLE_MED = os.path.join(ASSETS, 'Poppins-SemiBold.ttf')
FONT_LOGO = os.path.join(ASSETS, 'Poppins-ExtraBold.ttf')
FONT_BODY = os.path.join(ASSETS, 'Andika-Regular.ttf')
FONT_BODY_B = os.path.join(ASSETS, 'Andika-Bold.ttf')

PAGE_W, PAGE_H = 594.96, 765.12
CREAM = (249/255, 245/255, 234/255)
SAND = (0xF2/255, 0xEB/255, 0xDC/255)
INK = (0x1A/255, 0x1A/255, 0x1A/255)
GREY = (0x6B/255, 0x6B/255, 0x5E/255)
BROWN = (0x5A/255, 0x24/255, 0x09/255)
TERRA = (0x7C/255, 0x40/255, 0x22/255)
SEPIA_BG = (0xF7/255, 0xF3/255, 0xE9/255)
NAVY = (0x0A/255, 0x38/255, 0x71/255)
RED = (0xD3/255, 0x2F/255, 0x2F/255)

META = json.load(open(os.path.join(ASSETS, 'cover_meta.json')))
COPY = json.load(open(os.path.join(ASSETS, 'back_copy.json')))['copy']

f_title = pymupdf.Font(fontfile=FONT_TITLE)
f_med = pymupdf.Font(fontfile=FONT_TITLE_MED)
f_body = pymupdf.Font(fontfile=FONT_BODY)
f_bodyb = pymupdf.Font(fontfile=FONT_BODY_B)


def tw(font, text, size):
    return font.text_length(text, fontsize=size)


def wrap(text, font, size, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if tw(f if False else font, t, size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


LOGO_PNG = os.path.join(ASSETS, 'logo_prime_school.png')


def draw_logo(page, x, y, height=52.0):
    """Official Prime School logo (arch, star, PRIME SCHOOL) placed so its
    top-left is (x, y) and its height is `height` pt. Transparent PNG."""
    im = Image.open(LOGO_PNG)
    ratio = im.width / im.height
    w = height * ratio
    page.insert_image(pymupdf.Rect(x, y, x + w, y + height), filename=LOGO_PNG)


def content_bbox(im, bg=(249, 245, 234), tol=18):
    """Bounding box of non-background content in the image."""
    g = im.convert('RGB')
    w, h = g.size
    px = g.load()
    def isbg(p):
        return (abs(p[0]-bg[0]) <= tol and abs(p[1]-bg[1]) <= tol
                and abs(p[2]-bg[2]) <= tol)
    left, right, top, bot = w, 0, h, 0
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            if not isbg(px[x, y]):
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bot: bot = y
    if right <= left or bot <= top:
        return (0, 0, w, h)
    return (left, top, min(w, right+3), min(h, bot+3))


def prep_art(path, mode='fit', target_ratio=561/450, canvas=(1121, 919)):
    """Prepare front-cover art on a cream landscape canvas, always showing the
    full content bounding box (never clips heads)."""
    im = Image.open(path).convert('RGB')
    w, h = im.size
    # crop to content bbox so letterboxing is minimal and content is maximal
    bb = content_bbox(im)
    im = im.crop(bb)
    w, h = im.size
    cw, ch = canvas
    scale = min(cw / w, ch / h)
    nw, nh = int(w * scale), int(h * scale)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    out = Image.new('RGB', canvas, (249, 245, 234))
    out.paste(im2, ((cw - nw) // 2, (ch - nh) // 2))
    return out


def build_front(page, year, subject_title, level, art_path, stripe_rgb):
    """Draw standardized front cover onto a blank page."""
    W, H = page.rect.width, page.rect.height
    stripe_w = 34.0
    page.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=CREAM)
    page.draw_rect(pymupdf.Rect(0, 0, stripe_w, H), color=None,
                   fill=tuple(c/255 for c in stripe_rgb))
    # logo — 64pt tall, left edge aligned with the title text (x=85).
    # Bumped from 52pt (Aug 2026, teacher request); title block still starts
    # at baseline 140 so the larger logo sits comfortably above it.
    draw_logo(page, 85, 42, height=64.0)
    # title block — SINGLE uniform size (33pt) on every book; long titles
    # wrap to a second line instead of shrinking, so the series reads
    # identically across subjects
    x0 = 85.0
    size = 33.0
    lines = wrap(subject_title, f_title, size, 470)
    for i, line in enumerate(lines):
        page.insert_text((x0, 140 + i*38), line, fontsize=size,
                         fontname='ttl', fontfile=FONT_TITLE, color=INK)
    ymeta = 140 + len(lines)*38 + 26
    page.insert_text((x0, ymeta), f'Year {year}', fontsize=17,
                     fontname='med', fontfile=FONT_TITLE_MED, color=INK)
    page.insert_text((x0, ymeta + 24), level, fontsize=11,
                     fontname='body', fontfile=FONT_BODY, color=GREY)
    page.insert_text((x0, ymeta + 40), 'Student Manual', fontsize=11,
                     fontname='body', fontfile=FONT_BODY, color=GREY)
    ry = ymeta + 52
    page.draw_rect(pymupdf.Rect(x0, ry, x0+46, ry+2.6), color=None,
                   fill=tuple(c/255 for c in stripe_rgb))
    # artwork: full-bleed — fills the zone edge to edge (top 315pt to bottom,
    # stripe edge to right edge), as on the original covers
    art_top = 315.0
    page.insert_image(pymupdf.Rect(stripe_w, art_top, W, H), filename=art_path,
                      keep_proportion=False)


def sepia(img):
    g = ImageOps.grayscale(img).convert('L')
    r = g.point([min(255, int(p*1.02 + 18)) for p in range(256)])
    gr = g.point([min(255, int(p*0.95 + 10)) for p in range(256)])
    b = g.point([min(255, int(p*0.78 + 4)) for p in range(256)])
    return Image.merge('RGB', (r, gr, b))


def desat_neutral(img):
    """Neutral (non-yellow) wash: desaturate, then re-tint to a near-neutral
    warm white instead of sepia brown. Board prefers white/neutral backs."""
    g = ImageOps.grayscale(img).convert('L')
    # slight lift; R/G/B nearly equal -> neutral grey, no yellow cast
    r = g.point([min(255, int(p*0.97 + 16)) for p in range(256)])
    gr = g.point([min(255, int(p*0.97 + 16)) for p in range(256)])
    b = g.point([min(255, int(p*0.96 + 15)) for p in range(256)])
    return Image.merge('RGB', (r, gr, b))


def build_back(page, year, subject_title, level, ages, band, copy, art_path,
               stripe_rgb, isbn=None):
    W, H = page.rect.width, page.rect.height
    # background: distinct back-cover artwork, washed toward neutral warm-white
    # for text legibility (board feedback Aug 2026: less yellow, more
    # white/neutral; template look: pale desaturated wash, art reads ~25%)
    im = Image.open(art_path).convert('RGB')
    im = im.resize((714, 919), Image.LANCZOS)
    im = desat_neutral(im)
    white = Image.new('RGB', im.size, (250, 249, 246))
    im = Image.blend(im, white, 0.62)
    tmp = '/tmp/_backbg.png'
    im.save(tmp)
    page.insert_image(pymupdf.Rect(0, 0, W, H), filename=tmp, keep_proportion=False)
    stripe_w = 34.0
    page.draw_rect(pymupdf.Rect(0, 0, stripe_w, H), color=None,
                   fill=tuple(c/255 for c in stripe_rgb))
    x0 = 85.0
    # PRIME BOOKS label
    lab = 'P R I M E  B O O K S'
    page.insert_text((x0, 78), lab, fontsize=9.6, fontname='med',
                     fontfile=FONT_TITLE_MED, color=GREY)
    # title — same uniform 33pt as the front
    size = 33.0
    y = 96
    lines = wrap(subject_title, f_title, size, 460)
    for i, line in enumerate(lines):
        page.insert_text((x0, y + 32 + i*36), line, fontsize=size,
                         fontname='ttl', fontfile=FONT_TITLE, color=INK)
    ty = y + 32 + len(lines)*36 + 2
    # accent bar
    page.draw_rect(pymupdf.Rect(x0, ty, x0+22, ty+3), color=None,
                   fill=tuple(c/255 for c in stripe_rgb))
    # metadata line
    page.insert_text((x0, ty + 22), f'Year {year} · {level} · Student Manual',
                     fontsize=11, fontname='body', fontfile=FONT_BODY, color=GREY)
    # blurb
    by = ty + 48
    paras = [copy['hook']]
    paras.append(copy.get('blurb', ''))
    if copy.get('blurb2'):
        paras.append(copy['blurb2'])
    for p in paras:
        for ln in wrap(p, f_body, 11.4, 438):
            page.insert_text((x0, by), ln, fontsize=11.4, fontname='body',
                             fontfile=FONT_BODY, color=(0x2E/255, 0x2A/255, 0x24/255))
            by += 17.2
        by += 7
    # INSIDE THIS BOOK card
    card_x0, card_x1 = x0 - 14, 430
    card_y0 = max(by + 6, 0.46*H)
    bullets = copy['bullets']
    card_h = 30 + 9 + len(bullets)*19 + 14
    card_y1 = card_y0 + card_h
    card = page.new_shape()
    card.draw_rect(pymupdf.Rect(card_x0, card_y0, card_x1, card_y1), radius=0.06)
    card.finish(color=None, fill=SAND)
    card.commit()
    page.insert_text((card_x0 + 16, card_y0 + 24), 'INSIDE THIS BOOK',
                     fontsize=9.4, fontname='med', fontfile=FONT_TITLE_MED, color=BROWN)
    yy = card_y0 + 44
    for b in bullets:
        page.insert_text((card_x0 + 16, yy), '•', fontsize=10.6, fontname='body',
                         fontfile=FONT_BODY, color=(0x2E/255, 0x2A/255, 0x24/255))
        first = True
        for ln in wrap(b, f_body, 10.6, card_x1 - card_x0 - 46):
            page.insert_text((card_x0 + 30, yy), ln, fontsize=10.6, fontname='body',
                             fontfile=FONT_BODY, color=(0x2E/255, 0x2A/255, 0x24/255))
            yy += 19 if first else 15
            first = False
    # footer
    fy = 700
    page.insert_text((x0, fy), f'Prime Books · {subject_title}', fontsize=9,
                     fontname='med', fontfile=FONT_TITLE_MED, color=INK)
    page.insert_text((x0, fy + 16), f'{ages} · {band}', fontsize=9,
                     fontname='body', fontfile=FONT_BODY, color=GREY)
    page.insert_text((x0, fy + 32), 'primeschool.pt', fontsize=9,
                     fontname='med', fontfile=FONT_TITLE_MED, color=TERRA)
    # barcode + number bottom right (white knockout box for scanner legibility)
    if isbn:
        page.draw_rect(pymupdf.Rect(394, fy - 22, 512, fy + 52), color=None,
                       fill=(1, 1, 1))
        draw_barcode(page, 404, fy - 14, isbn)
        page.insert_text((404, fy + 42), isbn, fontsize=12,
                         fontname='body', fontfile=FONT_BODY, color=(0x2E/255,0x2A/255,0x24/255))


def draw_barcode(page, x, y, digits):
    """Minimal EAN-13-looking barcode (visual only) from digit string."""
    digits = digits.replace(' ', '')
    bars = []
    # guard
    bars += [(1, 2.2), (0, 2.2), (1, 2.2)]
    # left group digits 1-6, right group 7-12 (simplified widths from digit parity)
    L = {0:'0001101',1:'0011001',2:'0010011',3:'0111101',4:'0100011',
         5:'0110001',6:'0101111',7:'0111011',8:'0110111',9:'0001011'}
    R = {d: ''.join('1' if c=='0' else '0' for c in L[d]) for d in range(10)}
    seq = ''.join(L[int(d)] for d in digits[:6]) + ''.join(R[int(d)] for d in digits[6:13])
    for ch in seq:
        if ch == '1': bars.append((1, 1.7))
        else: bars.append((0, 1.7))
    bars += [(1, 2.2), (0, 2.2), (1, 2.2)]
    shape = page.new_shape()
    cx = x
    for black, w in bars:
        if black:
            shape.draw_rect(pymupdf.Rect(cx, y, cx + w, y + 44))
        cx += w
    shape.finish(color=(0.1, 0.1, 0.1), fill=(0.1, 0.1, 0.1))
    shape.commit()


def main():
    art_dir = sys.argv[1] if len(sys.argv) > 1 else '/tmp/newart'
    back_dir = sys.argv[2] if len(sys.argv) > 2 else '/tmp/backart'
    rows = [r for r in json.load(open('public/library.json')) if r['year'] <= 6]
    report = []
    for r in rows:
        slug = r['slug']
        year = str(r['year'])
        meta = META['subjects'][slug]
        copy = COPY[slug]
        level = META['levels'][year]['level']
        ages = META['levels'][year]['ages']
        band = META['levels'][year]['band']
        stripe = META['stripes'][year]
        art = os.path.join(art_dir, slug + '.png')
        back_art = os.path.join(back_dir, slug + '.png')
        if not os.path.exists(art):
            report.append((slug, 'NO FRONT ART'))
            continue
        if not os.path.exists(back_art):
            report.append((slug, 'NO BACK ART'))
            continue
        doc = pymupdf.open(f'public/library/{slug}/book.pdf')
        # FRONT
        fp = doc[0]
        fp.add_redact_annot(fp.rect)
        fp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE)
        build_front(fp, year, meta['title'], level, art, stripe)
        # BACK
        bp = doc[doc.page_count - 1]
        bp.add_redact_annot(bp.rect)
        bp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE)
        build_back(bp, year, meta['title'], level, ages, band, copy, back_art, stripe)
        out = '/tmp/out_' + slug + '.pdf'
        doc.save(out, deflate=True, garbage=3)
        report.append((slug, 'ok'))
    for s, m in report:
        print(s, m)


if __name__ == '__main__':
    main()
