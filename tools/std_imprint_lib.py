#!/usr/bin/env python3
"""Build a Prime Books STANDARD imprint page (physical page 2) as a one-page PDF.

This is the design rolled out across Years 1-4 on 2026-09-12 (see
prime-books-book-builder/references/imprint-standard-rollout-y1-4.md). The
geometry below was MEASURED off the shipped reference pages
(public/library/y01-art-and-design/book.pdf page 2, 612x792), not invented:

    eyebrow cap-line        Poppins SemiBold 8.6  base 64.0   x 56   +0.27 tracking
    school mark             (522,38)-(556,72)    the real logo, never generated
    header rule             (56,76)-(556,77.4)   the YEAR stripe colour
    display title           Poppins ExtraBold 30 base 126.0  x 56   ink #1a1a1a
    year / student line     Poppins SemiBold 10.4 base 148.0 x 56   #6e7a88
    accent bar              (56,161)-(188,166.4) the year stripe colour
    hook line               Andika 12.2          base 196.0  x 56   accent text
    INSIDE THIS BOOK        Poppins SemiBold 9.6 base 226.4  x 56
    bullets                 2 cols, x 72 / x 335, square 2.6pt at x 56 / x 319
    IMPRINT card            (56,315.4)-(556,...) white fill, 0.9pt ink border
      tab                   (56,315.4)-(184,337.4) stripe, label base 330.4 x 68
      rows                  label Poppins SB 8.2 x 74 #6e7a88, value Andika 9.4
                            x 196; first base = card top + 48.0; each row starts
                            22.2 below the previous row's LAST line; wrapped
                            lines step 13.2; dotted leader to x 186
    footer rule             (56,682)-(556,682) 0.6pt #d8d2c6
    footer left             Andika 8.4 #6e7a88  base 700.0 step 11.6 maxw 348
    footer right            Poppins SemiBold 8.4 tracked, right-aligned to 556,
                            base 700.0; the web line 9.4 accent text, base 716.0
    folio badge             (538,746)-(562,770) stripe, white Fredoka 11 base 762.3

Year colour: `tools/cover_assets/cover_meta.json -> stripes` (sampled from the
catalogue covers) for the rules, fills, tab, bullets and badge; a darker tone of
the same hue for small type on white (white on amber/sky blue is only ~3:1).

Usage:
    python tools/std_imprint_lib.py <slug> --out /tmp/p2.pdf
    python tools/std_imprint_lib.py <slug> --out /tmp/p2.pdf --blurb '...'

The content for a book comes from --spec JSON (see BOOKS below for the shape) or
from the book's own page 2 plus tools/cover_assets/back_copy.json.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(HERE, "cover_assets")
FONTS = "/root/pbfonts"


def _font(name, fallback_dir=FONTS):
    for d in (fallback_dir, ASSETS):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


F_TITLE = _font("Poppins-ExtraBold.ttf")
F_TITLE_MED = _font("Poppins-SemiBold.ttf")
F_BODY = _font("Andika-Regular.ttf")
F_FOLIO = _font("Fredoka-SemiBold.ttf")
LOGO = os.path.join(ASSETS, "logo_prime_school.png")

WHITE = (1.0, 1.0, 1.0)
INK = (0x1A / 255,) * 3
MUTED = (0x6E / 255, 0x7A / 255, 0x88 / 255)
DOTS = (0xD8 / 255, 0xD2 / 255, 0xC6 / 255)

# measured geometry, PDF points, top-left origin
W, H = 612.0, 792.0
ML, MR = 56.0, 556.0
BASE_EYEBROW, BASE_TITLE, BASE_SUB = 64.0, 126.0, 148.0
RULE = (56.0, 76.0, 556.0, 77.4)
ACCENT = (56.0, 161.0, 188.0, 166.4)
BASE_HOOK, BASE_INSIDE = 196.0, 226.4
BULLET_X = (72.0, 335.0)
BULLET_SQ_X = (56.0, 319.0)
CARD_X0, CARD_X1 = 56.0, 556.0
TAB = (56.0, 315.4, 184.0, 337.4)
ROW_LABEL_X, ROW_VALUE_X, ROW_LEADER_X1 = 74.0, 196.0, 186.0
FOOTER_RULE_Y = 682.0
FOOTER_BASE, FOOTER_STEP = 700.0, 11.6
FOOTER_MAXW = 280.0        # keeps the reference's four-line break AND leaves the
                           # right-hand block room for a word-spaced ages line:
                           # at 312 its longest line reached x 366 and collided
                           # with 'Ages 11 to 12 · Lower Secondary'
BADGE = (538.0, 746.0, 562.0, 770.0)

INDEPENDENCE = (
    "Independent publication. This is an independent publication produced by "
    "Prime School for use within its own programmes of study. It is not "
    "affiliated with, licensed by, endorsed by or approved by any examination "
    "board, or by any other publisher."
)

KNOWN_YEARS = {
    1: ("f1b300", "7a5a00"), 2: ("7fc3e8", "15658c"), 3: ("ef7522", "a5460b"),
    4: ("60bb46", "2d7a21"), 5: ("c32480", "7d1a52"), 6: ("835fc1", "4b2f7d"),
}


def rgb(hexstr):
    return tuple(int(hexstr[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _lum(c):
    """Relative luminance of a 0-1 colour tuple."""
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def on_accent(stripe):
    """Type colour for text sitting ON the year stripe fill.

    Ink on a light accent (amber, sky) reads; white on amber is ~1.7:1. The
    darkest secondary stripes (Y7 teal, Y8 slate) are the other way round, so
    the choice is made on measured contrast, never by rule of thumb.
    """
    return WHITE if _contrast(WHITE, stripe) >= _contrast(INK, stripe) else INK


def year_colours(year, meta_path=None):
    """(stripe, accent_text) for a year: sampled stripe + a darker type tone."""
    stripe = None
    m = meta_path or os.path.join(ASSETS, "cover_meta.json")
    try:
        meta = json.load(open(m))
        s = meta.get("stripes", {}).get(str(int(year)))
        if s:
            stripe = tuple(c / 255 for c in s)
    except Exception:
        pass
    if stripe is None:
        stripe = rgb(KNOWN_YEARS[int(year)][0])
    if int(year) in KNOWN_YEARS:
        return stripe, rgb(KNOWN_YEARS[int(year)][1])
    # darken the stripe toward black for small type on white
    return stripe, tuple(c * 0.42 for c in stripe)


def wrap(text, fontfile, size, maxw):
    f = pymupdf.Font(fontfile=fontfile)
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.text_length(t, fontsize=size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spread(text):
    """'INSIDE THIS BOOK' -> 'I N S I D E  T H I S  B O O K'.

    Letters take a single space; a WORD boundary takes two, so `tracked` can
    give the word gap an extra advance. With one space everywhere (the old
    behaviour) every gap is identical and the line reads 'INSIDETHISBOOK'.
    """
    return "  ".join(" ".join(w) for w in str(text).split())


def tracked(page, text, x, base, fontfile, size, color, tracking=0.0, align_right=None,
            word_gap=None):
    """Glyph-by-glyph placement so the letterspacing is exact.

    A letter-spaced line must still show its WORD breaks: the advance at a word
    boundary is a second space plus `word_gap`, so the gap reads as about four
    times a letter gap. Word gap default is 0.45 of the type size: at 8.4pt the
    footer's right-hand block (ages, band, site) then still clears the
    independence notice's longest line by about 10pt, on the reference's own
    numbers.
    """
    text = spread(text)
    f = pymupdf.Font(fontfile=fontfile)
    if word_gap is None:
        word_gap = 0.45 * size
    advs, prev_space = [], False
    for ch in text:
        a = f.text_length(ch, fontsize=size) + tracking
        if ch == " ":
            if prev_space:            # the second space of a word boundary
                a += word_gap
            prev_space = True
        else:
            prev_space = False
        advs.append(a)
    total = sum(advs) - (tracking if advs else 0)
    if align_right is not None:
        x = align_right - total
    tw = pymupdf.TextWriter(page.rect)
    cx = x
    for ch, a in zip(text, advs):
        tw.append((cx, base), ch, font=f, fontsize=size)
        cx += a
    tw.write_text(page, color=color)          # float tuple: an int is IGNORED
    return x, x + total


def build_page(spec, stripe, accent):
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    page.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=WHITE)

    year = int(spec["year"])
    title = spec["title"]
    sub = spec.get("sub") or "Year %d · Student Book" % year

    # --- cap-line, mark, rule -------------------------------------------------
    tracked(page, "PRIME SCHOOL PRESS", ML, BASE_EYEBROW, F_TITLE_MED, 8.6,
            accent, tracking=0.27)
    page.insert_image(pymupdf.Rect(522, 38, 556, 72), filename=LOGO)
    page.draw_rect(pymupdf.Rect(*RULE), color=None, fill=stripe)

    # --- title / sub / accent bar / hook --------------------------------------
    size = 30.0
    while size > 20 and pymupdf.Font(fontfile=F_TITLE).text_length(title, fontsize=size) > MR - ML:
        size -= 0.5
    page.insert_text((ML, BASE_TITLE), title, fontsize=size, fontname="ttl",
                     fontfile=F_TITLE, color=INK)
    page.insert_text((ML, BASE_SUB), sub, fontsize=10.4, fontname="med",
                     fontfile=F_TITLE_MED, color=MUTED)
    page.draw_rect(pymupdf.Rect(*ACCENT), color=None, fill=stripe)
    page.insert_text((ML, BASE_HOOK), spec["hook"], fontsize=12.2, fontname="body",
                     fontfile=F_BODY, color=accent)

    # --- lead paragraph (the book's own about-this-book sentence) -------------
    y = BASE_HOOK + 20.5
    for line in wrap(spec.get("lead", ""), F_BODY, 10.0, MR - ML):
        page.insert_text((ML, y), line, fontsize=10.0, fontname="body",
                         fontfile=F_BODY, color=INK)
        y += 13.5
    if spec.get("lead"):
        y += 10.0

    # --- INSIDE THIS BOOK -----------------------------------------------------
    base_inside = y if y > BASE_HOOK + 20 else BASE_INSIDE
    base_inside = max(base_inside, BASE_INSIDE)
    tracked(page, "INSIDE THIS BOOK", ML, base_inside, F_TITLE_MED, 9.6, INK,
            tracking=0.0)

    bullets = list(spec.get("bullets") or [])
    half = (len(bullets) + 1) // 2
    cols = (bullets[:half], bullets[half:])
    col_bottom = base_inside + 20.0
    for ci, col in enumerate(cols):
        x, sqx = BULLET_X[ci], BULLET_SQ_X[ci]
        maxw = (MR if ci else BULLET_SQ_X[1] - 8) - x
        b = base_inside + 20.0          # every column starts at the same top
        for item in col:
            page.draw_rect(pymupdf.Rect(sqx, b - 2.6, sqx + 2.6, b),
                           color=None, fill=stripe)
            for line in wrap(item, F_BODY, 10.0, maxw):
                page.insert_text((x, b), line, fontsize=10.0, fontname="body",
                                 fontfile=F_BODY, color=INK)
                b += 14.0
            b += 5.0
        col_bottom = max(col_bottom, b - 5.0)

    # --- the IMPRINT card -----------------------------------------------------
    rows = spec["rows"]
    top = max(TAB[1] + 22.0, col_bottom + 31.0)
    lines_per_row = [wrap(v, F_BODY, 9.4, MR - ROW_VALUE_X) for _, v in rows]
    card_h = 48.0 + sum(22.2 + 13.2 * (len(l) - 1) for l in lines_per_row) - 22.2 + 14.2
    bottom = top + card_h
    if bottom > FOOTER_RULE_Y - 12:
        raise SystemExit(
            "card does not fit: bottom %.1f (footer rule %.1f). Drop optional "
            "rows or shorten CREDITS." % (bottom, FOOTER_RULE_Y))
    page.draw_rect(pymupdf.Rect(CARD_X0, top, CARD_X1, bottom), color=INK,
                   fill=WHITE, width=0.9)
    page.draw_rect(pymupdf.Rect(CARD_X0, top, TAB[2], top + 22.0), color=None,
                   fill=stripe)
    tracked(page, "IMPRINT", 68.0, top + 15.0, F_TITLE_MED, 9.0,
            on_accent(stripe), tracking=0.0)

    b = top + 48.0
    f_lab = pymupdf.Font(fontfile=F_TITLE_MED)
    for (label, _), lines in zip(rows, lines_per_row):
        page.insert_text((ROW_LABEL_X, b), label, fontsize=8.2, fontname="med",
                         fontfile=F_TITLE_MED, color=MUTED)
        lw = f_lab.text_length(label, fontsize=8.2)
        dx = ROW_LABEL_X + lw + 5.0
        while dx < ROW_LEADER_X1:
            page.draw_rect(pymupdf.Rect(dx, b - 1.2, dx + 1.4, b - 0.4),
                           color=None, fill=DOTS)
            dx += 3.4
        for line in lines:
            page.insert_text((ROW_VALUE_X, b), line, fontsize=9.4, fontname="body",
                             fontfile=F_BODY, color=INK)
            b += 13.2
        b += 22.2 - 13.2      # next row's baseline is 22.2 below this row's last
    assert abs((b - 22.2 + 14.2) - bottom) < 0.6, (
        b, bottom, top, [len(l) for l in lines_per_row], card_h)

    # --- footer ---------------------------------------------------------------
    page.draw_line(pymupdf.Point(ML, FOOTER_RULE_Y), pymupdf.Point(MR, FOOTER_RULE_Y),
                   color=DOTS, width=0.6)
    fy = FOOTER_BASE
    for line in wrap(INDEPENDENCE, F_BODY, 8.4, FOOTER_MAXW):
        page.insert_text((ML, fy), line, fontsize=8.4, fontname="body",
                         fontfile=F_BODY, color=MUTED)
        fy += FOOTER_STEP
    ages = spec.get("ages") or "Ages 9 to 10"
    band = spec.get("band") or "Upper Primary"
    tracked(page, "%s · %s" % (ages, band), 0, FOOTER_BASE, F_TITLE_MED, 8.4,
            MUTED, tracking=0.17, align_right=MR)
    tracked(page, "www.primeschool.pt", 0, FOOTER_BASE + 16.0, F_TITLE_MED, 9.4,
            accent, tracking=0.0, align_right=MR)

    # --- folio badge ----------------------------------------------------------
    page.draw_rect(pymupdf.Rect(*BADGE), color=None, fill=stripe, radius=0.5)
    tw = pymupdf.TextWriter(page.rect)
    fnum = pymupdf.Font(fontfile=F_FOLIO)
    num = str(spec.get("folio", 2))
    tw.append((550.0 - fnum.text_length(num, fontsize=11.0) / 2, 762.3), num,
              font=fnum, fontsize=11.0)
    tw.write_text(page, color=on_accent(stripe))
    return doc


def to_page(design, spec_size):
    """Place the 612x792 design, scaled and centred, on another trim size.

    Some titles trim at 210x270mm (595x765.12pt), not US Letter: a book of two
    page sizes is a printing fault, so the design is scaled UNIFORMLY (never
    stretched) and centred. The white margin that leaves is invisible on a white
    page, and every proportion and margin of the design is kept.
    """
    w, h = (float(v) for v in re.split(r"[x,]", spec_size))
    s = min(w / W, h / H)
    out = pymupdf.open()
    page = out.new_page(width=w, height=h)
    page.draw_rect(pymupdf.Rect(0, 0, w, h), color=None, fill=WHITE)
    x0, y0 = (w - W * s) / 2.0, (h - H * s) / 2.0
    page.show_pdf_page(pymupdf.Rect(x0, y0, x0 + W * s, y0 + H * s), design, 0)
    return out


def audit(doc):
    """Line-bbox collision + margin scan. Returns a list of complaints."""
    page = doc[0]
    pw = page.rect.width
    lines = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            if l["spans"]:
                lines.append(l["bbox"])
    lines.sort(key=lambda r: (round(r[1], 1), r[0]))
    bad = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, c = lines[i], lines[j]
            if c[1] - a[3] < -4 and min(a[2], c[2]) - max(a[0], c[0]) > 12:
                bad.append(("overlap", [round(v, 1) for v in a],
                            [round(v, 1) for v in c]))
    for r in lines:
        if r[0] < 28 or r[2] > pw - 28:
            bad.append(("margin", [round(v, 1) for v in r]))
    return bad


# ------------------------------------------------------------------ per book --
def spec_from_book(slug):
    """Read the book's own page 2 and the back-cover copy, and build the spec."""
    root = ROOT
    lib = json.load(open(os.path.join(root, "public", "library.json")))
    row = [r for r in lib if r["slug"] == slug][0]
    meta = json.load(open(os.path.join(ASSETS, "cover_meta.json")))
    year = int(row["year"])
    levels = meta["levels"][str(year)]
    copy = json.load(open(os.path.join(ASSETS, "back_copy.json")))["copy"].get(slug, {})

    doc = pymupdf.open(os.path.join(root, "public", "library", slug, "book.pdf"))
    old = doc[1].get_text()
    return {
        "slug": slug,
        "year": year,
        "title": meta["subjects"][slug]["title"],
        "sub": "Year %d · Student Book" % year,
        "hook": copy.get("hook", ""),
        "bullets": copy.get("bullets", []),
        "ages": levels["ages"].replace("–", " to "),
        "band": levels["band"],
        "old_page_2": old,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--out", required=True)
    ap.add_argument("--spec", help="JSON file with the page's content")
    ap.add_argument("--year", type=int)
    ap.add_argument("--page", help="build onto a page of this size, e.g. 595x765.12; "
                                   "default the 612x792 the design was measured on")
    args = ap.parse_args(argv)

    spec = json.load(open(args.spec)) if args.spec else spec_from_book(args.slug)
    stripe, accent = year_colours(spec.get("year") or args.year)
    doc = build_page(spec, stripe, accent)
    if args.page:
        doc = to_page(doc, args.page)
    problems = audit(doc)
    doc.save(args.out)
    print("wrote %s  stripe #%02x%02x%02x" % (args.out, *(int(c * 255) for c in stripe)))
    print("audit:", problems if problems else "clean")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())