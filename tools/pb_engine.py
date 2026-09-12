#!/usr/bin/env python3
"""Block-driven page engine for Prime Books (Pack A "storybook", Years 1-6).

One shared layout skeleton, one subject theme colour. Pages are pure DATA:

    page = dict(label="1.1  WALK, RUN AND STOP", num=15,
                hl="Unit 1 · Moving Well", hr="The Open Meadow",
                kick="UNIT 1 · TOPIC 1.1 · WALK, RUN AND STOP",
                title="Walk, run and stop",
                blocks=[B.lead("..."), B.plate("u1_p11_space", ("Picture 1.1", "...")),
                        B.panel("tint", "Move it", ["..."], icon="move"), ...])

Blocks are (name, payload) tuples; every block has a height function and a
draw function, so a page can measure itself before it draws (which is what
stops half-empty and overflowing pages).

Geometry and type sizes are lifted from the y01 Art & Design master.
"""
import os
import pymupdf
from PIL import Image, ImageDraw

# ---------------------------------------------------------------- geometry --
W, H = 612.0, 792.0
ML, MR = 50.2, 561.8
CW = MR - ML
TOP, BOT = 66.0, 734.2
BAND_H, RULE_H = 47.0, 1.8
FOOT_Y = 742.0
FOLIO_C = (550.0, 758.0)
FOLIO_R = 12.0

FONTDIR = "/root/pbfonts"
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


def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))


def tw(s, key, size):
    return FOBJ[key].text_length(s, size)


# ------------------------------------------------------------------ themes --
PE = dict(
    deep=hx("5A3A0E"), mid=hx("9A6A12"), tint=hx("F6EEDC"), cream=hx("FFFBF3"),
    line=hx("EBDFC7"), amber=hx("F1B300"), green=hx("4E6B45"), gtint=hx("EDF3E6"),
    warn=hx("B4442A"), wtint=hx("FAEDE4"), ink=hx("2B2721"), muted=hx("6E6759"),
    band_text=hx("FFFFFF"), sub=hx("3A3226"),
)

TH = PE  # active theme, rebound by set_theme()


def set_theme(t):
    global TH
    TH = t


# --------------------------------------------------------------- text utils --
def draw(pg, x, y, s, key, size, colour, track=0.0):
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


def fit_size(text, key, size, maxw, floor=13.0):
    """Shrink a display face until the line fits the measure."""
    while size > floor and tw(text, key, size) > maxw:
        size -= 0.5
    return size


def wrap(runs, width, size, track=0.0):
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


# ------------------------------------------------------------------ shapes --
def rrect(pg, r, rad, fill=None, stroke=None, width=0.75, dashes=None):
    frac = min(0.5, max(0.0, rad / max(1.0, min(r.width, r.height))))
    pg.draw_rect(r, color=stroke, fill=fill, width=width, radius=frac, dashes=dashes)


def dashed(pg, r, rad, stroke=None, width=0.9):
    stroke = stroke or TH["line"]
    frac = min(0.5, max(0.0, rad / max(1.0, min(r.width, r.height))))
    pg.draw_rect(r, color=stroke, fill=None, width=width, radius=frac, dashes="[4 3] 0")


def bg(pg, colour):
    pg.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=colour)


# -------------------------------------------------------------------- icons --
def ic_diamond(pg, cx, cy, s, col):
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
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=col, width=1.5,
                 radius=0.16)
    pg.draw_rect(pymupdf.Rect(cx - s * 0.42, cy - s * 0.42, cx + s * 0.42, cy + s * 0.42),
                 color=col, width=1.2, radius=0.14)


def ic_tick(pg, cx, cy, s, col):
    pg.draw_polyline([(cx - s, cy), (cx - s * 0.25, cy + s * 0.7), (cx + s, cy - s * 0.8)],
                     color=col, width=1.9, lineCap=1)


def ic_checkbox(pg, cx, cy, s, col):
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=col, width=0.9,
                 radius=0.18)


def ic_qr(pg, cx, cy, s, col):
    """Small vector 'scan me' mark."""
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=col, width=1.4,
                 radius=0.1)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1)):
        pg.draw_rect(pymupdf.Rect(cx + dx * s * 0.52 - s * 0.3,
                                  cy + dy * s * 0.52 - s * 0.3,
                                  cx + dx * s * 0.52 + s * 0.3,
                                  cy + dy * s * 0.52 + s * 0.3),
                     color=None, fill=col)
    pg.draw_rect(pymupdf.Rect(cx + s * 0.14, cy + s * 0.14, cx + s * 0.72, cy + s * 0.72),
                 color=None, fill=col)


def ic_book(pg, cx, cy, s, col):
    pg.draw_rect(pymupdf.Rect(cx - s, cy - s, cx + s, cy + s), color=col, width=1.4,
                 radius=0.12)
    pg.draw_line(pymupdf.Point(cx, cy - s), pymupdf.Point(cx, cy + s), color=col, width=1.0)


PANEL_ICON = {"kit": ic_kit, "move": ic_star, "watch": ic_square, "try": ic_dot,
              "play": ic_diamond, "safety": ic_flag, "look": ic_checkbox,
              "challenge": ic_triangle, "qr": ic_qr, "didyou": ic_star,
              "think": ic_diamond, "note": ic_book}


# ------------------------------------------------------------- plate helper --
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


def plate_png(path, out, w_pt, h_pt, r_top_pt, r_bot_pt, corner=None, maxpx=980):
    img = _crop_to(path, w_pt / h_pt)
    if img.width > maxpx:
        img = img.resize((maxpx, int(img.height * maxpx / img.width)), Image.LANCZOS)
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
    base.save(out, quality=84)
    return out


def cream_fill(path):
    im = Image.open(path).convert("RGB")
    return tuple(c / 255 for c in im.getpixel((4, 4)))


# --------------------------------------------------------------- page parts --
def content_page(doc, hl, hr, kick, title):
    pg = doc.new_page(width=W, height=H)
    bg(pg, TH["band_text"])          # white paper
    pg.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=(1, 1, 1))
    pg.draw_rect(pymupdf.Rect(0, 0, W, BAND_H), color=None, fill=TH["tint"])
    pg.draw_rect(pymupdf.Rect(0, BAND_H - 1, W, BAND_H - 1 + RULE_H), color=None,
                 fill=TH["mid"])
    draw(pg, ML, 24.4, hl, "F", 10.5, TH["deep"])
    draw_r(pg, MR, 25.0, hr, "A", 10.0, TH["muted"])
    y = TOP + 1.0 + 7.6
    draw(pg, ML, y, kick, "F", 9.5, TH["mid"], track=0.5)
    y += 6.0
    ts = fit_size(title, "F", 24.5, CW, floor=17.0)
    y += ts * 0.80
    draw(pg, ML, y, title, "F", ts, TH["deep"])
    return pg, y + 8


def folio(pg, label, num, badge=None):
    pg.draw_line(pymupdf.Point(ML, FOOT_Y), pymupdf.Point(MR, FOOT_Y), color=TH["line"],
                 width=0.6)
    draw(pg, ML, 752.5, label, "A", 9.4, TH["muted"], track=0.55)
    pg.draw_circle(FOLIO_C, FOLIO_R, color=None, fill=badge or TH["mid"])
    draw_c(pg, FOLIO_C[0], FOLIO_C[1] + 3.9, str(num), "F", 11, (1, 1, 1))


class Flow:
    """Draws blocks top-down and spreads leftover air between them."""

    def __init__(self, pg, y):
        self.pg, self.y, self.blocks = pg, y, []

    def add(self, height, fn):
        self.blocks.append((height, fn))
        return self

    def total(self):
        return sum(h for h, _ in self.blocks)

    def run(self, bottom=BOT, max_gap=30.0):
        n = len(self.blocks)
        extra = 0.0
        if n > 1:
            extra = min(max_gap, max(0.0, (bottom - self.y - self.total()) / (n - 1)))
        y = self.y
        for i, (h, fn) in enumerate(self.blocks):
            fn(y)
            y += h
            if i < n - 1:
                y += extra
        return y


# =============================================================== the blocks ==
# every block: B.<name>(...) -> ("name", payload)
class B:
    @staticmethod
    def lead(text, after=9.0):
        return ("lead", dict(text=text, after=after))

    @staticmethod
    def para(text, size=13.5, pitch=18.7, after=8.0):
        return ("para", dict(text=text, size=size, pitch=pitch, after=after))

    @staticmethod
    def panel(kind, title, paras, icon=None, bs=13.0, pitch=17.4):
        return ("panel", dict(kind=kind, title=title, paras=paras, icon=icon,
                              bs=bs, pitch=pitch))

    @staticmethod
    def today(title, items):
        return ("today", dict(title=title, items=items))

    @staticmethod
    def steps(title, items, extra=None, tail=None, icon="try"):
        return ("steps", dict(title=title, items=items, extra=extra, tail=tail, icon=icon))

    @staticmethod
    def ticks(title, items):
        return ("ticks", dict(title=title, items=items))

    @staticmethod
    def traffic(rows):
        return ("traffic", dict(rows=rows))

    @staticmethod
    def cards(cols, numbered=True):
        return ("cards", dict(cols=cols, numbered=numbered))

    @staticmethod
    def plate(img, caption=None, height=300, flex=False, arch=0, minh=180, maxh=341,
              corner=None):
        return ("plate", dict(img=img, caption=caption, height=height, flex=flex,
                              arch=arch, minh=minh, maxh=maxh, corner=corner))

    @staticmethod
    def qr(url, title, blurb, minutes="", note=""):
        return ("qr", dict(url=url, title=title, blurb=blurb, minutes=minutes, note=note))

    @staticmethod
    def duo(items, height=96):
        return ("duo", dict(items=items, height=height))

    @staticmethod
    def drawbox(label, lines=1, height=44):
        return ("drawbox", dict(label=label, lines=lines, height=height))

    @staticmethod
    def table(cols, rows, widths=None, head=True):
        return ("table", dict(cols=cols, rows=rows, widths=widths, head=head))

    @staticmethod
    def subhead(text):
        return ("subhead", dict(text=text))

    @staticmethod
    def watch(paras, bust, title=None):
        return ("watch", dict(paras=paras, bust=bust, title=title))

    @staticmethod
    def chips(items):
        return ("chips", dict(items=items))

    @staticmethod
    def drawrow(labels, height=44):
        return ("drawrow", dict(labels=labels, height=height))

    @staticmethod
    def spot(img, height=150, caption=None):
        return ("spot", dict(img=img, height=height, caption=caption))

    @staticmethod
    def toc(entries):
        return ("toc", dict(entries=entries))

    @staticmethod
    def qrgrid(items, cols=4):
        return ("qrgrid", dict(items=items, cols=cols))

    @staticmethod
    def reflist(items):
        return ("reflist", dict(items=items))

    @staticmethod
    def note(text, who=None):
        return ("note", dict(text=text, who=who))

    @staticmethod
    def gap(pts):
        return ("gap", dict(pts=pts))


PAD = 13.0
TS = 11.5


def _panel_wrapped(b):
    return [(autowrap([(t, "AB" if bold(text) else "A")], CW - 2 * PAD - 4, b["bs"]))
            for text, bold in b["paras"]]


def bold(x):
    return False


def h_lead(b):
    return len(autowrap([(b["text"], "A")], CW, 15.0)[0]) * 20.5 + b["after"]


def d_lead(pg, y, b):
    return _para(pg, y, [("", "A")], b["text"], 15.0, 20.5, TH["sub"], b["after"])


def h_para(b):
    return len(autowrap([(b["text"], "A")], CW, b["size"])[0]) * b["pitch"] + b["after"]


def d_para(pg, y, b):
    return _para(pg, y, None, b["text"], b["size"], b["pitch"], TH["ink"], b["after"])


def _para(pg, y, _runs, text, size, pitch, colour, after):
    lines, tr = autowrap([(text, "A")], CW, size)
    for ln in lines:
        y += pitch
        draw_line_words(pg, ML, y, ln, size, colour, tr)
    return y + after


def h_today(b):
    return PAD + TS + 9 + len(b["items"]) * 19.5 + PAD - 4 + 10


def d_today(pg, y, b):
    total = PAD + TS + 9 + len(b["items"]) * 19.5 + PAD - 4
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=TH["tint"])
    pg.draw_rect(pymupdf.Rect(ML, y + 5, ML + 4.2, r.y1 - 5), color=None, fill=TH["mid"])
    ic_tick(pg, ML + PAD + 7.4, y + PAD + TS * 0.36, 5.0, TH["mid"])
    draw(pg, ML + PAD + 18.5, y + PAD + TS * 0.80, b["title"].upper(), "F", TS, TH["mid"],
         track=0.45)
    ry = y + PAD + TS + 9
    for it in b["items"]:
        ry += 19.5
        ic_tick(pg, ML + PAD + 9.0, ry - 4.6, 6.0, TH["mid"])
        draw(pg, ML + PAD + 24, ry, it, "A", 13.0, TH["ink"])
    return r.y1 + 10


def h_panel(b):
    kind = b["kind"]
    if kind == "didyou":
        head_h = TS + 6
        body = sum(len(autowrap([(t, "A")], CW - 2 * PAD - 4, b["bs"])[0]) * b["pitch"] + 4
                   for t in b["paras"])
        return PAD + head_h + body - 2 + PAD + 10
    head_h = TS + 6
    body = sum(len(autowrap([(t, "A")], CW - 2 * PAD - 4, b["bs"])[0]) * b["pitch"] + 4
               for t in b["paras"])
    return PAD + head_h + body - 2 + PAD + 10


def d_panel(pg, y, b):
    kind = b["kind"]
    wrapd = [autowrap([(t, "A")], CW - 2 * PAD - 4, b["bs"]) for t in b["paras"]]
    body = sum(len(l) * b["pitch"] + 4 for l, _ in wrapd)
    total = PAD + (TS + 6) + body - 2 + PAD
    r = pymupdf.Rect(ML, y, MR, y + total)
    accent = TH["mid"]
    if kind == "plain":
        rrect(pg, r, 9, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
    elif kind == "tint":
        rrect(pg, r, 9, fill=TH["tint"])
        pg.draw_rect(pymupdf.Rect(ML, y + 5, ML + 4.2, r.y1 - 5), color=None, fill=accent)
    elif kind == "green":
        rrect(pg, r, 9, fill=TH["gtint"])
        pg.draw_rect(pymupdf.Rect(ML, y + 5, ML + 4.2, r.y1 - 5), color=None,
                     fill=TH["green"])
        accent = TH["green"]
    elif kind == "warn":
        rrect(pg, r, 9, fill=TH["wtint"])
        pg.draw_rect(pymupdf.Rect(ML, y + 5, ML + 4.2, r.y1 - 5), color=None,
                     fill=TH["warn"])
        accent = TH["warn"]
    elif kind == "didyou":
        rrect(pg, r, 9, fill=TH["tint"])
        pg.draw_rect(pymupdf.Rect(ML, y + 5, ML + 4.2, r.y1 - 5), color=None, fill=accent)
    ty = y + PAD + TS * 0.80
    tx = ML + PAD + 2
    icon = b.get("icon")
    if icon:
        PANEL_ICON[icon](pg, tx + 4.6, y + PAD + TS * 0.36, 4.6, accent)
        tx += 15.5
    draw(pg, tx, ty, b["title"].upper(), "F", TS, accent, track=0.45)
    by = ty + 8.5
    for ls, tr in wrapd:
        for ln in ls:
            by += b["pitch"]
            draw_line_words(pg, ML + PAD + 2, by, ln, b["bs"], TH["ink"], tr)
        by += 4
    return r.y1 + 10


def h_steps(b):
    bw = CW - 2 * PAD - 26
    wrapped = [autowrap([(t, "A")], bw, 13.0) for t in b["items"]]
    body = sum(len(l) * 17.4 + 6 for l, _ in wrapped)
    body += 56 if b["extra"] else 0
    body += len(b["tail"] or []) * 20.0 + (8 if b["tail"] else 0)
    return PAD + TS + 7 + body + PAD - 2 + 10


def d_steps(pg, y, b):
    bw = CW - 2 * PAD - 26
    wrapped = [autowrap([(t, "A")], bw, 13.0) for t in b["items"]]
    body = sum(len(l) * 17.4 + 6 for l, _ in wrapped)
    body += 56 if b["extra"] else 0
    body += len(b["tail"] or []) * 20.0 + (8 if b["tail"] else 0)
    total = PAD + TS + 7 + body + PAD - 2
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
    ty = y + PAD + TS * 0.80
    PANEL_ICON[b.get("icon") or "try"](pg, ML + PAD + 6.6, y + PAD + TS * 0.36, 4.6,
                                       TH["mid"])
    draw(pg, ML + PAD + 17.5, ty, b["title"].upper(), "F", TS, TH["mid"], track=0.45)
    by = ty + 10.5
    for i, (ls, tr) in enumerate(wrapped):
        pg.draw_circle((ML + PAD + 10.5, by + 5.0), 8.0, color=None, fill=TH["mid"])
        draw_c(pg, ML + PAD + 10.5, by + 8.6, str(i + 1), "F", 9.5, (1, 1, 1))
        for ln in ls:
            by += 17.4
            draw_line_words(pg, ML + PAD + 26, by, ln, 13.0, TH["ink"], tr)
        by += 6
    if b["extra"]:
        draw(pg, ML + PAD + 26, by + 14, b["extra"], "F", 9.5, TH["muted"], track=0.45)
        bx = pymupdf.Rect(ML + PAD + 26, by + 22, r.x1 - PAD, r.y1 - PAD)
        dashed(pg, bx, 7)
        d_drawbox_lines(pg, bx, label_pt=6.0, gap=17.0)
        by += 56
    if b["tail"]:
        by += 8
        for it in b["tail"]:
            by += 20.0
            ic_checkbox(pg, ML + PAD + 32, by - 4.4, 6.2, TH["mid"])
            draw(pg, ML + PAD + 48, by, it, "A", 13.0, TH["ink"])
    return r.y1 + 10


def h_ticks(b):
    return PAD + TS + 8 + len(b["items"]) * 20.0 + PAD - 4 + 10


def d_ticks(pg, y, b):
    total = PAD + TS + 8 + len(b["items"]) * 20.0 + PAD - 4
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
    ic_checkbox(pg, ML + PAD + 6.4, y + PAD + TS * 0.36, 5.2, TH["mid"])
    draw(pg, ML + PAD + 17.5, y + PAD + TS * 0.80, b["title"].upper(), "F", TS, TH["mid"],
         track=0.45)
    ry = y + PAD + TS + 8
    for it in b["items"]:
        ry += 20.0
        ic_checkbox(pg, ML + PAD + 7.4, ry - 4.4, 6.2, TH["mid"])
        draw(pg, ML + PAD + 24, ry, it, "A", 13.0, TH["ink"])
    return r.y1 + 10


def h_traffic(b):
    return len(b["rows"]) * (34.5 + 6.4) + 4 + 10


def d_traffic(pg, y, b):
    for text in b["rows"]:
        r = pymupdf.Rect(ML, y, MR, y + 34.5)
        rrect(pg, r, 8, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
        draw(pg, ML + 14, y + 34.5 * 0.5 + 4.6, text, "A", 14.0, TH["ink"])
        pg.draw_line(pymupdf.Point(MR - 118, y + 6), pymupdf.Point(MR - 118, y + 28.5),
                     color=TH["line"], width=0.7)
        for i, (on, ed) in enumerate(((hx("CFEBC7"), hx("4FA845")),
                                      (hx("FDECB8"), hx("FFC233")),
                                      (hx("F9CFC4"), hx("E4572E")))):
            pg.draw_circle((MR - 90 + i * 28, y + 17.25), 9.0, color=ed, fill=on, width=0.75)
        y += 40.9
    return y + 4 + 10


def _card_lines(cols, ncols):
    gap = 11.0
    cw = (CW - (ncols - 1) * gap) / ncols
    wrapped, maxl = [], 0
    for title, body in cols:
        ls, tr = autowrap([(body, "A")], cw - 40, 11.5)
        wrapped.append((ls, tr))
        maxl = max(maxl, len(ls))
    return cw, gap, wrapped, maxl


def h_cards(b):
    n = len(b["cols"])
    _, _, _, maxl = _card_lines(b["cols"], n)
    return 32 + maxl * 14.6 + 16 + 10


def d_cards(pg, y, b):
    n = len(b["cols"])
    cw, gap, wrapped, maxl = _card_lines(b["cols"], n)
    h = 32 + maxl * 14.6 + 16
    for i, (title, body) in enumerate(b["cols"]):
        cx = ML + i * (cw + gap)
        r = pymupdf.Rect(cx, y, cx + cw, y + h)
        rrect(pg, r, 8, fill=TH["cream"], stroke=TH["line"], width=0.75)
        if b["numbered"]:
            pg.draw_circle((cx + 20, y + 22), 9.5, color=None, fill=TH["mid"])
            draw_c(pg, cx + 20, y + 25.6, str(i + 1), "F", 10, (1, 1, 1))
            tx = cx + 36
        else:
            tx = cx + 14
        draw(pg, tx, y + 26, title, "F", 12.0, TH["deep"])
        by = y + 32
        for ln in wrapped[i][0]:
            by += 14.6
            draw_line_words(pg, cx + 14, by, ln, 11.5, TH["muted"], wrapped[i][1])
    return y + h + 10


def h_subhead(b):
    return 14 * 0.8 + 12 + 8


def d_subhead(pg, y, b):
    draw(pg, ML, y + 12, b["text"], "F", 14.0, TH["deep"])
    return y + 12 + 8


def h_note(b):
    size = 15.0 if b.get("who") else 14.0
    return 18 + len(autowrap([(b["text"], "C")], CW - 90, size)[0]) * 17.0 + 8


def d_note(pg, y, b):
    """Handwritten teacher aside, the Art & Design 'studio note' voice."""
    size = 15.0 if b.get("who") else 14.0
    lines, _ = autowrap([(b["text"], "C")], CW - 90, size)
    yy = y + 6
    if b.get("who"):
        draw(pg, ML, yy + 12, b["who"], "F", 10.0, TH["mid"], track=0.45)
        yy += 12 + 4
    for ln in lines:
        yy += 17.0
        draw(pg, ML + 22, yy, " ".join(w for w, _ in ln), "C", size, TH["muted"])
    return yy + 8


def _table_rows(b):
    """Wrap every cell; return per-row heights so a 2-line cell never collides."""
    widths = b["widths"] or [0.42, 0.58]
    xs, x = [], ML + 14
    for frac in widths:
        xs.append(x)
        x += CW * frac - 28
    xs.append(MR - 14)
    out = []
    for row in b["rows"]:
        cells = []
        for i, cell in enumerate(row):
            w = (xs[i + 1] - xs[i]) - 8
            ls = autowrap([(cell, "A")], w, 12.0)[0] if cell.strip() else []
            cells.append(ls)
        lines = max([len(c) for c in cells] or [1])
        out.append((cells, 10 + lines * 13.5))
    return xs, out


def h_table(b):
    _xs, rows = _table_rows(b)
    return (24 if b["head"] else 2) + sum(h for _c, h in rows) + 10 + 10


def d_table(pg, y, b):
    cols = b["cols"]
    xs, rows = _table_rows(b)
    total = (24 if b["head"] else 2) + sum(h for _c, h in rows) + 10
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
    if b["head"]:
        pg.draw_rect(pymupdf.Rect(ML, y + 1, MR, y + 24), color=None, fill=TH["tint"])
        for i, cname in enumerate(cols):
            draw(pg, xs[i], y + 17, cname.upper(), "F", 9.5, TH["mid"], track=0.45)
    yy = y + (24 if b["head"] else 1)
    for j, (cells, h) in enumerate(rows):
        for i, lines in enumerate(cells):
            for k, ln in enumerate(lines):
                draw_line_words(pg, xs[i], yy + 14 + k * 13.5, ln, 12.0,
                                TH["ink"] if i == 0 else TH["muted"], 0.0)
        yy += h
        if j < len(rows) - 1:
            pg.draw_line(pymupdf.Point(ML + 10, yy - 3), pymupdf.Point(MR - 10, yy - 3),
                         color=TH["line"], width=0.5)
    return y + total + 10


def h_qr(b):
    return 92 + 10


def d_qr(pg, y, b):
    """A 'scan and show' panel: vector QR tile + what it is + adult note."""
    total = 92
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=TH["cream"], stroke=TH["line"], width=0.75)
    tile = pymupdf.Rect(ML + 12, y + 12, ML + 80, y + 80)
    rrect(pg, tile, 7, fill=(1, 1, 1), stroke=TH["line"], width=0.6)
    pg.insert_image(pymupdf.Rect(tile.x0 + 4, tile.y0 + 4, tile.x1 - 4, tile.y1 - 4),
                    filename=_qr_png(b["url"]))
    tx = ML + 94
    ic_qr(pg, tx + 4.0, y + 22.5, 4.0, TH["mid"])
    draw(pg, tx + 14, y + 26, b["title"].upper(), "F", 10.5, TH["mid"], track=0.45)
    by = y + 30
    for ln in autowrap([(b["blurb"], "A")], MR - tx - 14, 12.5)[0]:
        by += 15.6
        draw(pg, tx, by, " ".join(w for w, _ in ln), "A", 12.5, TH["ink"])
    foot = b["url"].replace("https://", "").replace("www.", "")
    draw(pg, tx, y + 78, foot, "A", 9.0, TH["muted"])
    if b["minutes"]:
        draw_r(pg, MR - 14, y + 78, b["minutes"], "A", 9.0, TH["mid"])
    return r.y1 + 10


_QR_CACHE = {}


def _qr_png(url):
    if url in _QR_CACHE:
        return _QR_CACHE[url]
    import segno
    path = "/tmp/_qr_%d.png" % (abs(hash(url)) % 10 ** 9)
    segno.make(url, error="m").save(path, scale=8, border=2, dark="#2b2721")
    _QR_CACHE[url] = path
    return path


def h_duo(b):
    return b["height"] + 10


def d_duo(pg, y, b):
    h = b["height"]
    r = pymupdf.Rect(ML, y, MR, y + h)
    rrect(pg, r, 9, fill=TH["cream"], stroke=TH["line"], width=0.75)
    n = len(b["items"])
    cw = CW / n
    for i in range(1, n):
        pg.draw_line(pymupdf.Point(ML + i * cw, y + 12), pymupdf.Point(ML + i * cw, y + h - 12),
                     color=TH["line"], width=0.7)
    for i, (bust, top, sub) in enumerate(b["items"]):
        cx = ML + i * cw
        p = _spot_jpg(bust, 300)
        im = Image.open(p)
        bw = 62.0
        bh = min(bw * im.height / im.width, h - 34)
        bw = bh * im.width / im.height
        pg.insert_image(pymupdf.Rect(cx + 18, y + h - 12 - bh, cx + 18 + bw, y + h - 12),
                        filename=p)
        tx = cx + 18 + bw + 16
        twid = cx + cw - 14 - tx
        draw(pg, tx, y + 34, top, "F", 13, TH["mid"], track=1.1)
        sy = y + 54
        for ln in autowrap([(sub, "A")], twid, 12.0)[0]:
            draw(pg, tx, sy, " ".join(w for w, _ in ln), "A", 12.0, TH["muted"])
            sy += 15.0
    return r.y1 + 10


def h_drawbox(b):
    return b["height"] + 10


def d_drawbox(pg, y, b):
    h = b["height"]
    r = pymupdf.Rect(ML, y, MR, y + h)
    dashed(pg, r, 9)
    draw(pg, ML + 12, y + 15, b["label"].upper(), "F", 9.5, TH["muted"], track=0.45)
    d_drawbox_lines(pg, r)
    return r.y1 + 10


def h_gap(b):
    return b["pts"]


def d_gap(pg, y, b):
    return y + b["pts"]


IMG_DIR = ""


def _img(name):
    return os.path.join(IMG_DIR, name + ".png")


def h_plate(b):
    h = b["height"]
    if b["caption"]:
        lab, txt = b["caption"]
        n = len(autowrap([(txt, "A")], CW - tw(lab + " ", "AB", 11.0), 11.0)[0])
        h += 17 + 14.2 * (n - 1) + 12
    else:
        h += 12
    return h


def d_plate(pg, y, b):
    path = _img(b["img"])
    h = b["height"]
    fill = cream_fill(path)
    r = pymupdf.Rect(ML, y, MR, y + h)
    arch = b["arch"]
    if arch:
        rrect(pg, r, arch, fill=fill)
        pg.draw_rect(pymupdf.Rect(ML, r.y1 - arch, MR, r.y1), color=None, fill=fill)
    else:
        rrect(pg, r, 9, fill=fill)
    tmp = "/tmp/_pl_%s.jpg" % b["img"]
    corner = b["corner"]
    if corner == "white" and not arch:
        corner = (255, 255, 255)
    plate_png(path, tmp, CW, h, arch if arch else 9, 0 if arch else 9, corner)
    pg.insert_image(r, filename=tmp)
    out = r.y1
    if b["caption"]:
        out += 17
        lab, txt = b["caption"]
        draw(pg, ML, out, lab, "AB", 11.0, TH["deep"])
        cw = tw(lab, "AB", 11.0) + tw(" ", "A", 11.0)
        lines = wrap([(txt, "A")], CW - cw, 11.0)
        draw(pg, ML + cw, out, " ".join(w for w, _ in lines[0]), "A", 11.0, TH["muted"])
        for extra in lines[1:]:
            out += 14.2
            draw(pg, ML, out, " ".join(w for w, _ in extra), "A", 11.0, TH["muted"])
    return out + 12


def h_watch(b):
    bust = 54.0
    bw = CW - 2 * PAD - bust - 12
    lines = sum(len(autowrap([(t, "A")], bw, 13.0)[0]) for t in b["paras"])
    return max(PAD + TS + 8 + lines * 17.4 + 4 * len(b["paras"]) + PAD - 2,
               bust + 2 * PAD) + 10


def d_watch(pg, y, b):
    """'Watch me try' card with one of the six drawn in the corner."""
    bust = 54.0
    bw = CW - 2 * PAD - bust - 12
    wrapped = [autowrap([(t, "A")], bw, 13.0) for t in b["paras"]]
    bh = sum(len(l) * 17.4 + 4 for l, _ in wrapped)
    total = max(PAD + TS + 8 + bh + PAD - 2, bust + 2 * PAD)
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
    ic_square(pg, ML + PAD + 6.6, y + PAD + TS * 0.36, 4.6, TH["mid"])
    draw(pg, ML + PAD + 17.5, y + PAD + TS * 0.80, (b.get("title") or "Watch me try").upper(),
         "F", TS, TH["mid"], track=0.45)
    p = _spot_jpg(b["bust"], 300, bg=(255, 255, 255))
    bx, by = MR - PAD - bust, y + total - PAD - bust
    pg.insert_image(pymupdf.Rect(bx, by, bx + bust, by + bust), filename=p)
    yy = y + PAD + TS + 8
    for ls, tr in wrapped:
        for ln in ls:
            yy += 17.4
            draw_line_words(pg, ML + PAD + 2, yy, ln, 13.0, TH["ink"], tr)
        yy += 4
    return r.y1 + 10


def h_chips(b):
    return 30.0 + 10


def d_chips(pg, y, b):
    """A row of small tick chips: short options a child circles or ticks."""
    gap = 8.0
    n = len(b["items"])
    cw = (CW - (n - 1) * gap) / n
    for i, label in enumerate(b["items"]):
        cx = ML + i * (cw + gap)
        r = pymupdf.Rect(cx, y, cx + cw, y + 30)
        rrect(pg, r, 7, fill=(1, 1, 1), stroke=TH["line"], width=0.75)
        ic_checkbox(pg, cx + 14, y + 15, 5.6, TH["mid"])
        draw(pg, cx + 26, y + 19.4, label, "A", 12.0, TH["ink"])
    return y + 40


def h_drawrow(b):
    return b["height"] + 10


def d_drawrow(pg, y, b):
    """Side-by-side labelled drawing boxes (draw here / then here)."""
    gap = 11.0
    n = len(b["labels"])
    cw = (CW - (n - 1) * gap) / n
    h = b["height"]
    for i, lab in enumerate(b["labels"]):
        cx = ML + i * (cw + gap)
        r = pymupdf.Rect(cx, y, cx + cw, y + h)
        dashed(pg, r, 8)
        draw(pg, cx + 12, y + 15, lab.upper(), "F", 9.5, TH["muted"], track=0.45)
    return y + h + 10


def h_spot(b):
    return b["height"] + (20 if b.get("caption") else 0) + 10


def d_spot(pg, y, b):
    """A small transparent vignette centred on a cream card."""
    h = b["height"]
    cap = b.get("caption")
    total = h + (20 if cap else 0)
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=TH["cream"], stroke=TH["line"], width=0.75)
    p = _spot_jpg(b["img"])
    im = Image.open(p)
    ih = h - 16
    iw = min(ih * im.width / im.height, CW - 40)
    ih = iw * im.height / im.width
    pg.insert_image(pymupdf.Rect(W / 2 - iw / 2, y + 8, W / 2 + iw / 2, y + 8 + ih),
                    filename=p)
    if cap:
        draw_c(pg, W / 2, r.y1 - 8, cap, "A", 11.0, TH["muted"])
    return r.y1 + 10


_SPOT_CACHE = {}


def _spot_jpg(name, maxpx=560, bg=None):
    """Flatten a transparent vignette onto the panel colour and keep it small."""
    key = (name, bg, maxpx)
    if key in _SPOT_CACHE:
        return _SPOT_CACHE[key]
    src = Image.open(_img(name)).convert("RGBA")
    bb = src.getchannel("A").getbbox()
    if bb:
        pad = 4
        bb = (max(0, bb[0] - pad), max(0, bb[1] - pad),
              min(src.width, bb[2] + pad), min(src.height, bb[3] + pad))
        src = src.crop(bb)
    if src.width > maxpx:
        src = src.resize((maxpx, int(src.height * maxpx / src.width)), Image.LANCZOS)
    col = bg or tuple(round(c * 255) for c in TH["cream"])
    base = Image.new("RGB", src.size, col)
    base.paste(src, (0, 0), src)
    path = "/tmp/_spot_%s_%d.jpg" % (name, maxpx)
    base.save(path, quality=84)
    _SPOT_CACHE[key] = path
    return path


def d_drawbox_lines(pg, r, label_pt=22.0, gap=18.0, colour=None):
    """Faint ruled writing lines inside a practice box."""
    col = colour or hx("DCD3C0")
    y = r.y0 + label_pt
    while y < r.y1 - 8:
        pg.draw_line(pymupdf.Point(r.x0 + 14, y), pymupdf.Point(r.x1 - 14, y),
                     color=col, width=0.5, dashes="[1.5 3] 0")
        y += gap


BLOCKS = {
    "lead": (h_lead, d_lead), "para": (h_para, d_para), "panel": (h_panel, d_panel),
    "today": (h_today, d_today), "steps": (h_steps, d_steps), "ticks": (h_ticks, d_ticks),
    "traffic": (h_traffic, d_traffic), "cards": (h_cards, d_cards),
    "plate": (h_plate, d_plate), "qr": (h_qr, d_qr), "duo": (h_duo, d_duo),
    "drawbox": (h_drawbox, d_drawbox), "table": (h_table, d_table),
    "subhead": (h_subhead, d_subhead), "note": (h_note, d_note), "gap": (h_gap, d_gap),
    "watch": (h_watch, d_watch), "chips": (h_chips, d_chips),
    "drawrow": (h_drawrow, d_drawrow), "spot": (h_spot, d_spot),
    "toc": None, "qrgrid": None, "reflist": None,
}


# ------------------------------------------------------------ toc / listings --
def d_toc(pg, y, b):
    """Two-column contents list with dot leaders."""
    entries = b["entries"]
    col_w = (CW - 24) / 2
    half = (len(entries) + 1) // 2
    biggest = y
    for c in range(2):
        yy = y
        for label, num, lvl in entries[c * half:(c + 1) * half]:
            if label is None:
                yy += 8
                continue
            x = ML + c * (col_w + 24) + (14 if lvl == 2 else 0)
            size = 13.0 if lvl == 1 else 11.5
            key = "F" if lvl == 1 else "A"
            col = TH["deep"] if lvl == 1 else TH["ink"]
            draw(pg, x, yy + 13, label, key, size, col)
            draw_r(pg, ML + c * (col_w + 24) + col_w, yy + 13, str(num), "F", 11.5,
                   TH["mid"] if lvl == 1 else TH["muted"])
            lw = tw(label, key, size)
            ns = str(num)
            nw = tw(ns, "F", 11.5)
            dot_start = x + lw + 5
            dot_end = ML + c * (col_w + 24) + col_w - nw - 5
            if lvl == 2 and dot_end - dot_start > 8:
                d = dot_start
                while d < dot_end:
                    pg.draw_circle((d, yy + 9.6), 0.5, color=TH["line"], fill=TH["line"])
                    d += 4.4
            yy += 19.0 if lvl == 2 else 24.0
        biggest = max(biggest, yy)
    return biggest + 12


def h_qrgrid(b):
    rows = (len(b["items"]) + b["cols"] - 1) // b["cols"]
    return rows * 118 + 10


def d_qrgrid(pg, y, b):
    items, cols = b["items"], b["cols"]
    gap = 10.0
    cw = (CW - (cols - 1) * gap) / cols
    ch = 118.0
    for i, (title, url) in enumerate(items):
        cx = ML + (i % cols) * (cw + gap)
        cy = y + (i // cols) * ch
        r = pymupdf.Rect(cx, cy, cx + cw, cy + ch - 10)
        rrect(pg, r, 8, fill=TH["cream"], stroke=TH["line"], width=0.75)
        t = pymupdf.Rect(cx + (cw - 74) / 2, cy + 10, cx + (cw + 74) / 2, cy + 84)
        rrect(pg, t, 6, fill=(1, 1, 1), stroke=TH["line"], width=0.6)
        pg.insert_image(pymupdf.Rect(t.x0 + 4, t.y0 + 4, t.x1 - 4, t.y1 - 4),
                        filename=_qr_png(url))
        for ln in autowrap([(title, "A")], cw - 18, 10.5)[0][:2]:
            draw_c(pg, cx + cw / 2, cy + 98, " ".join(w for w, _ in ln), "A", 10.5, TH["ink"])
            break
    return y + ((len(items) + cols - 1) // cols) * ch + 10


def h_reflist(b):
    return len(b["items"]) * 30.0 + 10


def d_reflist(pg, y, b):
    """Numbered source list: label, publisher and the full address."""
    for i, (label, url, note) in enumerate(b["items"]):
        yy = y + i * 30.0
        pg.draw_circle((ML + 8, yy + 12), 8.0, color=None, fill=TH["mid"])
        draw_c(pg, ML + 8, yy + 15.4, str(i + 1), "F", 9.0, (1, 1, 1))
        draw(pg, ML + 24, yy + 16, label, "F", 11.5, TH["deep"])
        draw(pg, ML + 24, yy + 27, url, "A", 9.5, TH["muted"])
        if note:
            draw_r(pg, MR, yy + 16, note, "A", 9.5, TH["mid"])
        if i < len(b["items"]) - 1:
            pg.draw_line(pymupdf.Point(ML, yy + 30), pymupdf.Point(MR, yy + 30),
                         color=TH["line"], width=0.5)
    return y + len(b["items"]) * 30.0 + 10


BLOCKS["toc"] = (lambda b: 30 + sum(19.0 for e in b["entries"]) / 2, d_toc)
BLOCKS["qrgrid"] = (h_qrgrid, d_qrgrid)
BLOCKS["reflist"] = (h_reflist, d_reflist)


# ---------------------------------------------------------------- opener ----
def render_opener(doc, spec, num):
    """Full-bleed unit opener: flood colour, squircle numeral, topic pills,
    arched plate, caption. Returns (page, bottom)."""
    pg = doc.new_page(width=W, height=H)
    deep = TH["deep"]
    pg.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=deep)
    amber, cream = TH["amber"], hx("F6EEDC")
    draw(pg, 36.8, 52, spec["kicker"], "F", 12, amber, track=2.0)
    rrect(pg, pymupdf.Rect(36.8, 64, 98.8, 126), 16, fill=amber)
    draw_c(pg, 67.8, 108.5, str(spec["num"]), "F", 30, deep)
    draw(pg, 124.7, 113.6, spec["title"], "F",
         fit_size(spec["title"], "F", 44, 575.0 - 124.7, floor=26.0), (1, 1, 1))
    draw(pg, 36.8, 158, spec["ground"], "F", 17, hx("F5B82A"))
    y = 168.0
    for ln in autowrap([(spec["blurb"], "A")], 470, 14.0)[0]:
        y += 19.6
        draw(pg, 36.8, y, " ".join(w for w, _ in ln), "A", 14.0, hx("F3E4C6"))
    y += 6
    draw(pg, 36.8, y + 16, spec["narrative"], "G", 14, hx("EFD49A"))
    pytop = y + 44
    px, prow, inrow = 36.8, 0, 0
    for pnum, label in spec["topics"]:
        pw = tw(pnum + "  " + label, "F", 13) + 34
        if inrow == 2:
            prow += 1
            px, inrow = 36.8, 0
        r = pymupdf.Rect(px, pytop + prow * 41, px + pw, pytop + prow * 41 + 31.5)
        rrect(pg, r, 15.75, fill=(1, 1, 1))
        draw(pg, px + 15, r.y0 + 21.2, pnum, "F", 13, TH["mid"])
        draw(pg, px + 15 + tw(pnum + "  ", "F", 13), r.y0 + 21.2, label, "F", 13, deep)
        px += pw + 11
        inrow += 1
    at = pytop + (prow + 1) * 41 + 8
    ah = max(250.0, 690.0 - at)
    r = pymupdf.Rect(60, at, 552, at + ah)
    cf = base_fill = cream
    rrect(pg, r, 96, fill=cf)
    pg.draw_rect(pymupdf.Rect(60, r.y1 - 96, 552, r.y1), color=None, fill=cf)
    tmp = "/tmp/_op_%s.jpg" % spec["img"]
    plate_png(_img(spec["img"]), tmp, r.width, r.height, 96.0, 0.0,
              tuple(round(c * 255) for c in deep))
    pg.insert_image(r, filename=tmp)
    lab, txt = spec["caption"]
    labw = tw(lab + " ", "AB", 11.5)
    lines = wrap([(txt, "A")], CW - labw, 11.5)
    cy = r.y1 + 24
    first = " ".join(w for w, _ in lines[0])
    fw = tw(lab + " " + first, "A", 11.5)
    draw(pg, W / 2 - fw / 2, cy, lab, "AB", 11.5, amber)
    draw(pg, W / 2 - fw / 2 + tw(lab + " ", "AB", 11.5), cy, first, "A", 11.5, hx("F6EEDC"))
    for extra in lines[1:]:
        cy += 15.0
        draw_c(pg, W / 2, cy, " ".join(w for w, _ in extra), "A", 11.5, hx("F6EEDC"))
    pg.draw_circle(FOLIO_C, FOLIO_R, color=None, fill=(1, 1, 1))
    draw_c(pg, FOLIO_C[0], FOLIO_C[1] + 3.9, str(num), "F", 11, TH["mid"])
    return pg, cy


def render_page(doc, spec, folio_label, num):
    """Draw one content page from a spec dict; returns (page, bottom_y, over)."""
    pg, y = content_page(doc, spec["hl"], spec["hr"], spec["kick"], spec["title"])
    blocks = list(spec["blocks"])
    flex = [i for i, (n, p) in enumerate(blocks) if n == "plate" and p.get("flex")]
    if flex:
        i = flex[0]
        rest = 0.0
        for j, (n, p) in enumerate(blocks):
            if j == i:
                continue
            rest += BLOCKS[n][0](p)
        gaps = 26.0 * (len(blocks) - 1)
        avail = BOT - y - rest - gaps
        p = blocks[i][1]
        p["height"] = max(p["minh"], min(p["maxh"], avail))
    flow = Flow(pg, y)
    for n, p in blocks:
        hh, dd = BLOCKS[n]
        flow.add(hh(p), (lambda pp, fn: (lambda yy: fn(pg, yy, pp)))(p, dd))
    bottom = flow.run()
    folio(pg, folio_label, num)
    return pg, bottom, bottom > BOT + 0.5
