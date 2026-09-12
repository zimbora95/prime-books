#!/usr/bin/env python3
"""Rebuild Unit 1 of the Year 1 Physical Education book in the Art & Design
Year 1 visual language (Pack A "storybook" design system, 02-design-system.md).

Replaces PDF pages 13-22 (0-based 12..21) with ten freshly composed pages:

  13  Unit 1 opener, full-bleed, arched plate
  14  Topic 1.1  Space, walk, run, stop
  15  Topic 1.1  Walk, run and stop
  16  Topic 1.2  Hop, skip, join
  17  Topic 1.2  The join
  18  Topic 1.3  Fast, slow, high, low
  19  Topic 1.3  Fast and slow
  20  Topic 1.4  Hoops, benches, mats
  21  Topic 1.4  The meadow games
  22  Unit 1     How did it go?

All original wording is preserved. Run with .venv/bin/python.
"""
import os, sys, shutil
import pymupdf
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(REPO, "work", "y01pe_u1", "img")
FONTDIR = "/root/pbfonts"

# ---------------------------------------------------------------- geometry --
W, H = 612.0, 792.0
ML, MR = 50.2, 561.8
CW = MR - ML                     # 511.6 content width
TOP = 66.0
BOT = 734.2
BAND_H = 47.0
RULE_H = 1.8
FOOT_Y = 742.0
FOLIO_C = (550.0, 758.0)
FOLIO_R = 12.0


def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ------------------------------------------------------------------ palette --
DEEP = hx("5A3A0E")      # deep umber-ochre: headings, rules, accents
MID = hx("9A6A12")       # ochre: kicker, folio badge, panel bars
TINT = hx("F6EEDC")      # header band / tinted panel wash
CREAM = hx("FFFBF3")     # figure panel paper
LINE = hx("EBDFC7")      # hairlines and panel borders
AMBER = hx("F1B300")     # bright accent (unit badge)
GREEN = hx("4E6B45")     # safety and success
GTINT = hx("EDF3E6")
WARN = hx("B4442A")      # challenge
WTINT = hx("FAEDE4")
INK = hx("2B2721")       # body text
MUTED = hx("6E6759")     # captions, running text
WHITE = (1, 1, 1)
G_ON, G_ED = hx("CFEBC7"), hx("4FA845")
Y_ON, Y_ED = hx("FDECB8"), hx("FFC233")
R_ON, R_ED = hx("F9CFC4"), hx("E4572E")
PAPER = hx("FBF6EC")

# -------------------------------------------------------------------- fonts --
FONTS = {
    "F":  "Fredoka-SemiBold.ttf",
    "A":  "Andika-Regular.ttf",
    "AB": "Andika-Bold.ttf",
    "P":  "Poppins-SemiBold.ttf",
    "PM": "Poppins-Medium.ttf",
    "PR": "Poppins-Regular.ttf",
    "C":  "Caveat-Regular.ttf",
    "G":  "Gelasio-Bold.ttf",
}
FPATH = {k: os.path.join(FONTDIR, v) for k, v in FONTS.items()}
FOBJ = {k: pymupdf.Font(fontfile=v) for k, v in FPATH.items()}


def tw(s, key, size):
    return FOBJ[key].text_length(s, size)


def draw(pg, x, y, s, key, size, colour, track=0.0):
    """Baseline text at (x, y); track adds letter-spacing in points."""
    if track:
        cx = x
        for ch in s:
            pg.insert_text((cx, y), ch, fontname=key, fontfile=FPATH[key],
                           fontsize=size, color=colour)
            cx += tw(ch, key, size) + track
        return
    pg.insert_text((x, y), s, fontname=key, fontfile=FPATH[key],
                   fontsize=size, color=colour)


def draw_c(pg, cx, y, s, key, size, colour, track=0.0):
    w = tw(s, key, size) + track * max(0, len(s) - 1)
    draw(pg, cx - w / 2.0, y, s, key, size, colour, track)


def draw_r(pg, rx, y, s, key, size, colour, track=0.0):
    w = tw(s, key, size) + track * max(0, len(s) - 1)
    draw(pg, rx - w, y, s, key, size, colour, track)


def wrap(runs, width, size, track=0.0):
    """runs = [(text, fontkey), ...] -> list of lines, each a list of (word, key)."""
    words = []
    for text, key in runs:
        for w in text.split():
            words.append((w, key))
    sw = tw(" ", "A", size) + track
    lines, cur, curw = [], [], 0.0
    for w, key in words:
        ww = tw(w, key, size) + track * max(0, len(w) - 1)
        add = ww if not cur else sw + ww
        if cur and curw + add > width:
            lines.append(cur)
            cur, curw = [(w, key)], ww
        else:
            cur.append((w, key))
            curw += add
    if cur:
        lines.append(cur)
    return lines


def autowrap(runs, width, size):
    """Wrap, then tighten the tracking a little if a single word is left alone."""
    lines = wrap(runs, width, size, 0.0)
    if len(lines) > 1 and len(lines[-1]) == 1:
        for t in (-0.06, -0.12, -0.19, -0.26):
            alt = wrap(runs, width, size, t)
            if len(alt) < len(lines):
                return alt, t
    return lines, 0.0


def draw_line_words(pg, x, y, ln, size, colour, track):
    cx = x
    for i, (w, key) in enumerate(ln):
        if i:
            cx += tw(" ", "A", size) + track
        pg.insert_text((cx, y), w, fontname=key, fontfile=FPATH[key],
                       fontsize=size, color=colour)
        cx += tw(w, key, size) + track * max(0, len(w) - 1)


class Cursor:
    """Tracks the vertical position on one page and knows when space has run out."""

    def __init__(self, pg, y=TOP):
        self.pg, self.y = pg, y

    def need(self, h, min_start=BOT):
        return self.y + h <= min_start

    def end(self):
        return self.y


# -------------------------------------------------------------- page pieces --
def bg(pg, colour):
    pg.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=colour)


def band(pg, left, right):
    pg.draw_rect(pymupdf.Rect(0, 0, W, BAND_H), color=None, fill=TINT)
    pg.draw_rect(pymupdf.Rect(0, BAND_H - 1, W, BAND_H - 1 + RULE_H), color=None, fill=MID)
    draw(pg, ML, 24.4, left, "F", 10.5, DEEP)
    draw_r(pg, MR, 25.0, right, "A", 10.0, MUTED)


def folio(pg, label, num, badge=MID, num_col=WHITE):
    pg.draw_line(pymupdf.Point(ML, FOOT_Y), pymupdf.Point(MR, FOOT_Y), color=LINE, width=0.6)
    draw(pg, ML, 752.5, label, "A", 9.4, MUTED, track=0.55)
    pg.draw_circle(FOLIO_C, FOLIO_R, color=None, fill=badge)
    draw_c(pg, FOLIO_C[0], FOLIO_C[1] + 3.9, str(num), "F", 11, num_col)


def kicker(pg, y, text):
    draw(pg, ML, y + 7.6, text, "F", 9.5, MID, track=0.5)
    return y + 7.6


def h1(pg, y, text, size=24.5, colour=DEEP):
    draw(pg, ML, y + size * 0.80, text, "F", size, colour)
    return y + size * 0.80


# ------------------------------------------------------------------- shapes --
def rrect(pg, r, rad, fill=None, stroke=None, width=0.75, dashes=None):
    """rad is given in POINTS; PyMuPDF wants a fraction of the shorter side."""
    frac = min(0.5, max(0.0, rad / max(1.0, min(r.width, r.height))))
    pg.draw_rect(r, color=stroke, fill=fill, width=width, radius=frac, dashes=dashes)


def dashed(pg, r, rad, stroke=LINE, width=0.9):
    frac = min(0.5, max(0.0, rad / max(1.0, min(r.width, r.height))))
    pg.draw_rect(r, color=stroke, fill=None, width=width, radius=frac,
                 dashes="[4 3] 0")


def cream_fill(path):
    """Corner colour of a plate, so the figure panel merges with the artwork."""
    im = Image.open(path).convert("RGB")
    px = im.getpixel((4, 4))
    return tuple(c / 255 for c in px)


def _crop_to(path, want):
    src = Image.open(path).convert("RGB")
    w0, h0 = src.size
    have = w0 / h0
    if have > want:
        nw = int(h0 * want)
        box = ((w0 - nw) // 2, 0, (w0 - nw) // 2 + nw, h0)
    else:
        nh = int(w0 / want)
        box = (0, (h0 - nh) // 2, w0, (h0 - nh) // 2 + nh)
    return src.crop(box)


def plate_png(path, out, w_pt, h_pt, r_top_pt, r_bot_pt, corner=None):
    """Aspect-crop a plate and round its frame corners, filling the cut-away
    with `corner` (default: the plate's own paper tone, so it sits seamlessly
    on the matching cream panel)."""
    img = _crop_to(path, w_pt / h_pt)
    if img.width > 1240:                      # ~180 dpi at final size: enough
        nh = int(img.height * 1240 / img.width)   # for print, far less file bulk
        img = img.resize((1240, nh), Image.LANCZOS)
    w, h = img.size
    fill = corner or img.getpixel((2, 2))
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    rt = int(r_top_pt * w / w_pt)
    rb = int(r_bot_pt * w / w_pt)
    if rt:
        d.rectangle([0, rt, w - 1, h - 1], fill=255)
        d.rectangle([rt, 0, w - 1 - rt, h - 1], fill=255)
        d.pieslice([0, 0, 2 * rt, 2 * rt], 180, 270, fill=255)
        d.pieslice([w - 1 - 2 * rt, 0, w - 1, 2 * rt], 270, 360, fill=255)
    else:
        d.rectangle([0, 0, w - 1, h - 1], fill=255)
    if rb:
        d.rectangle([0, h - 1 - rb, w - 1, h - 1], fill=255)
        d.pieslice([0, h - 1 - 2 * rb, 2 * rb, h - 1], 90, 180, fill=255)
        d.pieslice([w - 1 - 2 * rb, h - 1 - 2 * rb, w - 1, h - 1], 0, 90, fill=255)
    base = Image.new("RGB", (w, h), fill)
    base.paste(img, (0, 0), m)
    base.save(out, quality=92)
    return out


def plate(pg, y, path, height, caption=None, arch=0, width=CW, x=ML):
    """Cream figure panel with the plate inside; returns the y below the caption."""
    fill = cream_fill(path)
    r = pymupdf.Rect(x, y, x + width, y + height)
    if arch:
        rrect(pg, r, arch, fill=fill)
        pg.draw_rect(pymupdf.Rect(x, r.y1 - arch, r.x1, r.y1), color=None, fill=fill)
    else:
        rrect(pg, r, 9, fill=fill)
    tmp = "/tmp/_plate_%s.jpg" % os.path.basename(path).replace(".png", "")
    corner = None
    if not arch:                       # round the plate corners to paper white
        corner = (255, 255, 255)       # so the cream block reads as a soft plate
    plate_png(path, tmp, width, height, arch if arch else 9, 0 if arch else 9, corner)
    pg.insert_image(r, filename=tmp)
    out = r.y1
    if caption:
        out += 17
        lab, txt = caption
        draw(pg, ML, out, lab, "AB", 11.0, DEEP)
        cw = tw(lab, "AB", 11.0) + tw(" ", "A", 11.0)
        lines = wrap([(txt, "A")], CW - cw, 11.0)
        draw(pg, ML + cw, out, " ".join(w for w, _ in lines[0]), "A", 11.0, MUTED)
        for extra in lines[1:]:
            out += 14.2
            draw(pg, ML, out, " ".join(w for w, _ in extra), "A", 11.0, MUTED)
    return out + 12


# -------------------------------------------------------------------- icons --
def _icon_base(pg, fill, stroke=None):
    return fill, stroke


def ic_diamond(pg, cx, cy, s, col):
    r = pymupdf.Rect(cx - s, cy - s, cx + s, cy + s)
    pg.draw_polyline([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy), (cx, cy - s)],
                     color=None, fill=col)


def ic_triangle(pg, cx, cy, s, col):
    pg.draw_polyline([(cx, cy - s), (cx + s, cy + s), (cx - s, cy + s), (cx, cy - s)],
                     color=None, fill=col)


def ic_square(pg, cx, cy, s, col):
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=None, fill=col)


def ic_dot(pg, cx, cy, s, col):
    pg.draw_circle((cx, cy), s, color=None, fill=col)


def ic_star(pg, cx, cy, s, col):
    pg.draw_polyline([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy), (cx, cy - s)],
                     color=col, fill=None, width=1.6)


def ic_flag(pg, cx, cy, s, col):
    pg.draw_line(pymupdf.Point(cx - s * 0.6, cy - s), pymupdf.Point(cx - s * 0.6, cy + s),
                 color=col, width=1.7)
    pg.draw_polyline([(cx - s * 0.6, cy - s), (cx + s, cy - s * 0.45),
                      (cx - s * 0.6, cy + s * 0.1)], color=None, fill=col)


def ic_kit(pg, cx, cy, s, col):
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=col, width=1.5, radius=0.16)
    pg.draw_rect(pymupdf.Rect(cx - s * 0.42, cy - s * 0.42, cx + s * 0.42, cy + s * 0.42),
                 color=col, width=1.2, radius=0.14)


def ic_tick(pg, cx, cy, s, col):
    pg.draw_polyline([(cx - s, cy), (cx - s * 0.25, cy + s * 0.7), (cx + s, cy - s * 0.8)],
                     color=col, width=1.9, lineCap=1)


def ic_checkbox(pg, cx, cy, s, col):
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=col, width=0.9, radius=0.18)


PANEL_ICON = {"kit": ic_kit, "move": ic_star, "watch": ic_square, "try": ic_dot,
              "play": ic_diamond, "safety": ic_flag, "look": ic_checkbox,
              "challenge": ic_triangle}


# ------------------------------------------------------------------ panels --
def panel_box(kind, title, lines, width=CW, ts=11.5, bs=13.0, pitch=17.4):
    """Height of a call-out box (and its wrapped body), without drawing it."""
    pad = 13.0
    if kind == "today":
        return pad + ts + 9 + len(lines) * 19.5 + pad - 4, []
    head_h = ts + 6
    body_h = 0
    wrapped = []
    for text, bold in lines:
        ls, tr = autowrap([(text, "AB" if bold else "A")], width - 2 * pad - 4, bs)
        wrapped.append((ls, tr))
        body_h += len(ls) * pitch + 4
    return pad + head_h + body_h - 2 + pad, wrapped


def steps_box(items, width=CW, bs=13.0, pitch=17.4, extra=None, tail=None):
    pad = 13.0
    ts = 11.5
    box_w = width - 2 * pad - 26
    wrapped = [autowrap([(t, "A")], box_w, bs) for t in items]
    body_h = sum(len(l[0]) * pitch + 6 for l in wrapped)
    body_h += 56 if extra else 0
    body_h += len(tail or []) * 20.0 + (8 if tail else 0)
    return pad + ts + 7 + body_h + pad - 2


def ticks_box(items, width=CW):
    pad = 13.0
    ts = 11.5
    return pad + ts + 8 + len(items) * 20.0 + pad - 4


def today(pg, y, title, items, width=CW, x=ML):
    """'Today you will' tick panel."""
    pad = 13.0
    ts = 11.5
    total, _ = panel_box("today", title, items, width=width, ts=ts)
    r = pymupdf.Rect(x, y, x + width, y + total)
    rrect(pg, r, 9, fill=TINT)
    pg.draw_rect(pymupdf.Rect(x, y + 5, x + 4.2, r.y1 - 5), color=None, fill=MID)
    ic_tick(pg, x + pad + 7.4, y + pad + ts * 0.36, 5.0, MID)
    draw(pg, x + pad + 18.5, y + pad + ts * 0.80, title.upper(), "F", ts, MID, track=0.45)
    ry = y + pad + ts + 9
    for it in items:
        ry += 19.5
        ic_tick(pg, x + pad + 9.0, ry - 4.6, 6.0, MID)
        draw(pg, x + pad + 24, ry, it, "A", 13.0, INK)
    return r.y1 + 10


def panel(pg, y, kind, title, lines, icon=None, width=CW, x=ML,
          accent=None, ts=11.5, bs=13.0, pitch=17.4):
    """One call-out box. lines = [(text, bold?), ...] paragraphs."""
    pad = 13.0
    accent = accent or MID
    total, wrapped = panel_box(kind, title, lines, width=width, ts=ts, bs=bs, pitch=pitch)

    r = pymupdf.Rect(x, y, x + width, y + total)
    if kind == "plain":
        rrect(pg, r, 9, fill=WHITE, stroke=LINE, width=0.75)
    elif kind == "tint":
        rrect(pg, r, 9, fill=TINT)
        pg.draw_rect(pymupdf.Rect(x, y + 5, x + 4.2, r.y1 - 5), color=None, fill=accent)
    elif kind == "green":
        rrect(pg, r, 9, fill=GTINT)
        pg.draw_rect(pymupdf.Rect(x, y + 5, x + 4.2, r.y1 - 5), color=None, fill=GREEN)
    elif kind == "warn":
        rrect(pg, r, 9, fill=WTINT)
        pg.draw_rect(pymupdf.Rect(x, y + 5, x + 4.2, r.y1 - 5), color=None, fill=WARN)

    ty = y + pad + ts * 0.80
    tx = x + pad + 2
    if icon:
        PANEL_ICON[icon](pg, tx + 4.6, y + pad + ts * 0.36, 4.6,
                         GREEN if kind == "green" else (WARN if kind == "warn" else accent))
        tx += 15.5
    draw(pg, tx, ty, title.upper(), "F", ts, accent, track=0.45)

    by = ty + 8.5
    for ls, tr in wrapped:
        for ln in ls:
            by += pitch
            draw_line_words(pg, x + pad + 2, by, ln, bs, INK, tr)
        by += 4
    return r.y1 + 10


def steps(pg, y, title, items, icon="try", width=CW, x=ML, bs=13.0, pitch=17.4,
          extra=None, tail=None):
    """Numbered 'Try it' panel: ochre numeral discs on a white card."""
    pad = 13.0
    ts = 11.5
    box_w = width - 2 * pad - 26
    wrapped = [autowrap([(t, "A")], box_w, bs) for t in items]
    total = steps_box(items, width=width, bs=bs, pitch=pitch, extra=extra, tail=tail)
    r = pymupdf.Rect(x, y, x + width, y + total)
    rrect(pg, r, 9, fill=WHITE, stroke=LINE, width=0.75)
    ty = y + pad + ts * 0.80
    PANEL_ICON[icon](pg, x + pad + 6.6, y + pad + ts * 0.36, 4.6, MID)
    draw(pg, x + pad + 17.5, ty, title.upper(), "F", ts, MID, track=0.45)
    by = ty + 10.5
    for i, (ls, tr) in enumerate(wrapped):
        pg.draw_circle((x + pad + 10.5, by + 5.0), 8.0, color=None, fill=MID)
        draw_c(pg, x + pad + 10.5, by + 8.6, str(i + 1), "F", 9.5, WHITE)
        for ln in ls:
            by += pitch
            draw_line_words(pg, x + pad + 26, by, ln, bs, INK, tr)
        by += 6
    if extra:
        draw(pg, x + pad + 26, by + 14, extra, "F", 9.5, MUTED, track=0.45)
        dashed(pg, pymupdf.Rect(x + pad + 26, by + 22, r.x1 - pad, r.y1 - pad), 7)
        by += 56
    if tail:
        by += 8
        for it in tail:
            by += 20.0
            ic_checkbox(pg, x + pad + 32, by - 4.4, 6.2, MID)
            draw(pg, x + pad + 48, by, it, "A", bs, INK)
    return r.y1 + 10


def ticks(pg, y, title, items, width=CW, x=ML):
    """'Look what I can do' tick list on a white card."""
    pad = 13.0
    ts = 11.5
    total = ticks_box(items, width=width)
    r = pymupdf.Rect(x, y, x + width, y + total)
    rrect(pg, r, 9, fill=WHITE, stroke=LINE, width=0.75)
    ic_checkbox(pg, x + pad + 6.4, y + pad + ts * 0.36, 5.2, MID)
    draw(pg, x + pad + 17.5, y + pad + ts * 0.80, title.upper(), "F", ts, MID, track=0.45)
    ry = y + pad + ts + 8
    for it in items:
        ry += 20.0
        ic_checkbox(pg, x + pad + 7.4, ry - 4.4, 6.2, MID)
        draw(pg, x + pad + 24, ry, it, "A", 13.0, INK)
    return r.y1 + 10


def traffic(pg, y, rows, width=CW, x=ML):
    """Self-assessment rows: statement left, three traffic-light circles right."""
    h = 34.5
    for text in rows:
        r = pymupdf.Rect(x, y, x + width, y + h)
        rrect(pg, r, 8, fill=WHITE, stroke=LINE, width=0.75)
        draw(pg, x + 14, y + h * 0.5 + 4.6, text, "A", 14.0, INK)
        pg.draw_line(pymupdf.Point(x + width - 118, y + 6),
                     pymupdf.Point(x + width - 118, y + h - 6), color=LINE, width=0.7)
        for i, (on, ed) in enumerate(((G_ON, G_ED), (Y_ON, Y_ED), (R_ON, R_ED))):
            pg.draw_circle((x + width - 90 + i * 28, y + h * 0.5), 9.0, color=ed,
                           fill=on, width=0.75)
        y += h + 6.4
    return y + 4


def cards_box(cols, width=CW):
    gap = 11.0
    cw = (width - 2 * gap) / 3.0
    maxlines = 0
    for t, b in cols:
        ls, _ = autowrap([(b, "A")], cw - 40, 11.5)
        maxlines = max(maxlines, len(ls))
    return 32 + maxlines * 14.6 + 16 + 10


def cards(pg, y, cols, width=CW, x=ML, h=None):
    """Small numbered station cards side by side (the meadow games)."""
    gap = 11.0
    cw = (width - 2 * gap) / 3.0
    wrapped = []
    maxlines = 0
    for title, body in cols:
        ls, tr = autowrap([(body, "A")], cw - 40, 11.5)
        wrapped.append((ls, tr))
        maxlines = max(maxlines, len(ls))
    h = h or (32 + maxlines * 14.6 + 16)
    for i, (title, body) in enumerate(cols):
        cx = x + i * (cw + gap)
        r = pymupdf.Rect(cx, y, cx + cw, y + h)
        rrect(pg, r, 8, fill=CREAM, stroke=LINE, width=0.75)
        pg.draw_circle((cx + 20, y + 22), 9.5, color=None, fill=MID)
        draw_c(pg, cx + 20, y + 25.6, str(i + 1), "F", 10, WHITE)
        draw(pg, cx + 36, y + 26, title, "F", 12.0, DEEP)
        by = y + 32
        for ln in wrapped[i][0]:
            by += 14.6
            draw_line_words(pg, cx + 14, by, ln, 11.5, MUTED, wrapped[i][1])
    return y + h + 10


def portrait(pg, x, y, name, size):
    """Small transparent character bust drawn straight on the page."""
    pg.insert_image(pymupdf.Rect(x, y, x + size, y + size),
                    filename=os.path.join(IMG, name + ".png"))


# ============================================================ page furniture ==
def new_page(doc):
    return doc.new_page(width=W, height=H)


def content_page(doc, header_left, header_right, kick, title):
    pg = new_page(doc)
    bg(pg, WHITE)
    band(pg, header_left, header_right)
    y = kicker(pg, TOP + 1.0, kick)
    y = h1(pg, y + 6.0, title)
    return pg, y + 8


FOOT_1_1 = "1.1  Walk, run and stop"
FOOT_1_2 = "1.2  Hop, skip, join"
FOOT_1_3 = "1.3  Fast and slow"
FOOT_1_4 = "1.4  The meadow games"
