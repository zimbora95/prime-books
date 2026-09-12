#!/usr/bin/env python3
"""Build the ten redesigned Unit 1 pages of the Year 1 Physical Education book.

Writes work/y01pe_u1/unit1.pdf (10 pages, indexes 12..21 of the master).
"""
import os, sys, shutil
import pymupdf
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y01pe_u1_kit import *  # noqa

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "work", "y01pe_u1", "img")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "work", "y01pe_u1", "unit1.pdf")


# --------------------------------------------------------------------------
def prep_busts():
    """Trim each character cut-out to its artwork and normalise the height."""
    for n in ("ch_pip", "ch_bramble", "ch_sorrel", "ch_tuft", "ch_willow", "ch_rowan"):
        p = os.path.join(IMG, n + ".png")
        src = Image.open(p).convert("RGBA")
        bb = src.getchannel("A").getbbox()
        if not bb:
            continue
        pad = 6
        bb = (max(0, bb[0] - pad), max(0, bb[1] - pad),
              min(src.width, bb[2] + pad), min(src.height, bb[3] + pad))
        cut = src.crop(bb)
        if cut.height > 520:
            cut = cut.resize((int(cut.width * 520 / cut.height), 520), Image.LANCZOS)
        cut.save(os.path.join(IMG, n + "_t.png"), optimize=True)


def bust_h(name):
    im = Image.open(os.path.join(IMG, name + "_t.png"))
    return im.width / im.height


class Flow:
    """Draws blocks top-down and spreads the leftover air between them."""

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


def para(pg, y, runs, size=13.5, pitch=18.7, width=CW, x=ML, colour=None, after=8.0):
    colour = colour or INK
    lines, tr = autowrap(runs, width, size)
    for ln in lines:
        y += pitch
        draw_line_words(pg, x, y, ln, size, colour, tr)
    return y + after


def para_h(runs, size=13.5, pitch=18.7, width=CW, after=8.0):
    return len(autowrap(runs, width, size)[0]) * pitch + after


def PB(kind, title, lines, **kw):
    return panel_box(kind, title, lines, **kw)[0]


def lead(pg, y, runs, after=9.0):
    """Slightly larger opening line under the H1."""
    return para(pg, y, runs, size=15.0, pitch=20.5, colour=hx("3A3226"), after=after)


def lead_h(runs, after=9.0):
    return para_h(runs, size=15.0, pitch=20.5, after=after)


# ==========================================================================
def build():
    prep_busts()
    doc = pymupdf.open()
    log = []

    # ------------------------------------------------------------ page 13 --
    pg = new_page(doc)
    bg(pg, DEEP)
    draw(pg, 36.8, 52, "U N I T  O N E", "F", 12, AMBER, track=2.0)
    rrect(pg, pymupdf.Rect(36.8, 64, 98.8, 126), 16, fill=AMBER)
    draw_c(pg, 67.8, 108.5, "1", "F", 30, DEEP)
    draw(pg, 124.7, 113.6, "Moving well", "F", 44, WHITE)
    draw(pg, 36.8, 158, "The Open Meadow", "F", 17, AMBER)
    y = para(pg, 168,
             [("This ground is about using a space, then using a body: walk, run, stop, "
               "hop, skip, and kit that changes the floor.", "A")],
             size=14.0, pitch=19.6, width=538, x=36.8, colour=hx("F3E4C6"), after=6)
    draw(pg, 36.8, y + 16, "Pip runs. Bramble leaves a space. Willow watches the stop.",
         "G", 14, hx("EFD49A"))
    pytop = y + 44
    pills = [("1.1", "Space, walk, run, stop"), ("1.2", "Hop, skip, join"),
             ("1.3", "Fast, slow, high, low"), ("1.4", "Hoops, benches, mats")]
    px, prow, inrow = 36.8, 0, 0
    for num, label in pills:
        wtxt = tw(num + "  " + label, "F", 13)
        pw = wtxt + 34
        if inrow == 2:
            prow += 1
            px, inrow = 36.8, 0
        r = pymupdf.Rect(px, pytop + prow * 41, px + pw, pytop + prow * 41 + 31.5)
        rrect(pg, r, 15.75, fill=WHITE)
        draw(pg, px + 15, r.y0 + 21.2, num, "F", 13, MID)
        draw(pg, px + 15 + tw(num + "  ", "F", 13), r.y0 + 21.2, label, "F", 13, DEEP)
        px += pw + 11
        inrow += 1
    at = pytop + (prow + 1) * 41 + 8
    ah = max(250.0, 690.0 - at)
    r = pymupdf.Rect(60, at, 552, at + ah)
    cream = hx("FDFAF3")
    rrect(pg, r, 96, fill=cream)
    pg.draw_rect(pymupdf.Rect(60, r.y1 - 96, 552, r.y1), color=None, fill=cream)
    plate_in(pg, r, os.path.join(IMG, "u1_opener.png"), 96.0, 0.0, tuple(round(c*255) for c in DEEP))
    cap = ("Picture 1.0", "The Open Meadow at the start of the year. Six friends, six "
                          "bodies, plenty of grass.")
    lines = wrap([(cap[1], "A")], CW, 11.5)
    cy = r.y1 + 24
    first = " ".join(w for w, _ in lines[0])
    fw = tw(cap[0] + " " + first, "A", 11.5)
    x0 = W / 2 - fw / 2
    draw(pg, x0, cy, cap[0], "AB", 11.5, AMBER)
    draw(pg, x0 + tw(cap[0] + " ", "AB", 11.5), cy, first, "A", 11.5, hx("F6EEDC"))
    for extra in lines[1:]:
        cy += 15.0
        draw_c(pg, W / 2, cy, " ".join(w for w, _ in extra), "A", 11.5, hx("F6EEDC"))
    pg.draw_circle(FOLIO_C, FOLIO_R, color=None, fill=WHITE)
    draw_c(pg, FOLIO_C[0], FOLIO_C[1] + 3.9, "13", "F", 11, MID)
    log.append(("13", round(cy, 1)))

    hdr = ("Unit 1 · Moving Well", "The Open Meadow")

    # ------------------------------------------------------------ page 14 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.1", "Space, walk, run, stop")
    f = Flow(pg, y)
    tw_ = ["leave a space and stop when asked",
           "hop, skip and join two movements",
           "change speed and level on purpose",
           "move on, over and through simple apparatus"]
    th = PB("today", "Today you will", tw_)
    kh = PB("plain", "The kit you need",
                   [("Four cones, a clear floor, and a teacher with a bell or a clear "
                     "word for stop.", False)])
    cap = ("Picture 1.1", "Pip and Bramble walk with a wide space between them. Sorrel "
                          "waits further back. Look how nobody is touching.")
    caph = 17 + 14.2 * (len(wrap([(cap[1], "A")], CW - 70, 11.0)) - 1) + 12
    ph = min(341.0, BOT - y - th - kh - caph - 22)
    f.add(ph + caph, lambda yy, ph=ph: plate(pg, yy, os.path.join(IMG, "u1_p11_space.png"),
                                             ph, cap))
    f.add(th, lambda yy: today(pg, yy, "Today you will", tw_))
    f.add(kh, lambda yy: panel(pg, yy, "plain", "The kit you need",
                               [("Four cones, a clear floor, and a teacher with a bell "
                                 "or a clear word for stop.", False)], icon="kit"))
    log.append(("14", round(f.run(), 1)))
    folio(pg, "1.1  SPACE, WALK, RUN, STOP", 14)

    # ------------------------------------------------------------ page 15 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.1 · WALK, RUN AND STOP",
                         "Walk, run and stop")
    f = Flow(pg, y)
    p1 = [("A ", "A"), ("space", "AB"), (" is a gap you can see. In Year 1, a good space "
          "is one you could lie down in without touching anyone.", "A")]
    p2 = [("Walk uses both feet, one after the other. Run uses both feet too, but there is "
           "a moment when both are off the floor. ", "A"), ("Stop", "AB"),
          (" means freeze: feet still, eyes on the teacher.", "A")]
    mvt = [("Walk anywhere for one minute. Change direction when you meet somebody. Do not "
            "touch. Then stand still.", False)]
    wmt = [("Pip runs. Bramble calls stop. Pip's feet finish the step they started, then "
            "they stay. He does not skid into Sorrel.", False)]
    sfy = [("Look where you are going. Leave a lie-down space. Stop means stop, even if the "
            "game is exciting.", False)]
    tri = ["Walk the space. Count how many children you can see without turning your head.",
           "Run to a cone and stop before you touch it. Do this four times.",
           "When the teacher says stop, freeze. Tick if your feet were still."]
    tks = ["I left a space.", "I stopped when I was asked."]
    f.add(para_h(p1) + para_h(p2) + 6,
          lambda yy: para(pg, para(pg, yy, p1), p2, after=0))
    f.add(PB("tint", "Move it", mvt) + 10,
          lambda yy: panel(pg, yy, "tint", "Move it", mvt, icon="move"))
    f.add(PB("plain", "Watch me try", wmt) + 10,
          lambda yy: watch(pg, yy, wmt, "ch_pip_t", 54))
    f.add(PB("green", "Safety first", sfy) + 10,
          lambda yy: panel(pg, yy, "green", "Safety first", sfy, icon="safety"))
    f.add(steps_box(tri) + 10,
          lambda yy: steps(pg, yy, "Try it", tri))
    f.add(ticks_box(tks), lambda yy: ticks(pg, yy, "Look what I can do", tks))
    log.append(("15", round(f.run(), 1)))
    folio(pg, "1.1  WALK, RUN AND STOP", 15)

    # ------------------------------------------------------------ page 16 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.2", "Hop, skip, join")
    f = Flow(pg, y)
    plt = [("Traffic. Green means walk. Yellow means slow. Red means stop. Play for two "
            "minutes. Nobody is out. If you bump, you just start again with a bigger "
            "space.", False)]
    kh = PB("plain", "The kit you need",
                   [("Skipping ropes if you have them, or just a clear floor. Work in "
                     "pairs.", False)])
    mvt = [("Ten heel raises. Ten gentle jumps on the spot. Shake your feet.", False)]
    cap = ("Picture 1.2", "Pip hops on one foot. Bramble skips with a rope. Two different "
                          "movements, both using a spring.")
    caph = 17 + 14.2 * (len(wrap([(cap[1], "A")], CW - 70, 11.0)) - 1) + 12
    ph = min(341.0, BOT - y - PB("tint", "Play together", plt) - kh
             - PB("tint", "Move it", mvt) - caph - 40)
    f.add(ph + caph, lambda yy, ph=ph: plate(pg, yy, os.path.join(IMG, "u1_p12_hopskip.png"),
                                             ph, cap))
    f.add(PB("tint", "Play together", plt) + 10,
          lambda yy: panel(pg, yy, "tint", "Play together", plt, icon="play"))
    f.add(kh + 10, lambda yy: panel(pg, yy, "plain", "The kit you need",
                                    [("Skipping ropes if you have them, or just a clear "
                                      "floor. Work in pairs.", False)], icon="kit"))
    f.add(PB("tint", "Move it", mvt),
          lambda yy: panel(pg, yy, "tint", "Move it", mvt, icon="move"))
    log.append(("16", round(f.run(), 1)))
    folio(pg, "1.2  HOP, SKIP, JOIN", 16)

    # ------------------------------------------------------------ page 17 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.2 · THE JOIN", "The join")
    f = Flow(pg, y)
    p1 = [("A ", "A"), ("hop", "AB"), (" is a spring on one foot, landing on the same foot. "
          "A ", "A"), ("skip", "AB"), (" is a step and a hop, repeating. To join them, you "
          "finish the hop and start the skip with no long pause in the middle.", "A")]
    wmt = [("Tuft hops three times on his right foot. Then he skips to the cone. The join "
            "is the third landing, which becomes the first skip.", False)]
    sfy = [("Land softly, with a little bend in the knee. If you wobble, put the other foot "
            "down. That is still good work.", False)]
    tri = ["Hop four times on each foot. Hold a wall if you need to.",
           "Skip to a cone and skip back.",
           "Join them: hop, hop, skip, skip. Draw the order."]
    chl = [("Do hop-hop-skip across the meadow without stopping in the middle. A partner "
            "watches the join.", False)]
    f.add(para_h(p1) + 6, lambda yy: para(pg, yy, p1, after=0))
    f.add(PB("plain", "Watch me try", wmt) + 10,
          lambda yy: watch(pg, yy, wmt, "ch_tuft_t", 54))
    f.add(PB("green", "Safety first", sfy) + 10,
          lambda yy: panel(pg, yy, "green", "Safety first", sfy, icon="safety"))
    f.add(steps_box(tri, extra="MY SEQUENCE") + 10,
          lambda yy: steps(pg, yy, "Try it", tri, extra="MY SEQUENCE"))
    f.add(PB("warn", "Challenge", chl),
          lambda yy: panel(pg, yy, "warn", "Challenge", chl, icon="challenge"))
    log.append(("17", round(f.run(), 1)))
    folio(pg, "1.2  THE JOIN", 17)

    # ------------------------------------------------------------ page 18 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.3", "Fast, slow, high, low")
    f = Flow(pg, y)
    p1 = [("Speed", "AB"), (" is how quickly a movement happens. ", "A"), ("Level", "AB"),
          (" is how high or low the body is. You can change one of them on purpose.", "A")]
    p2 = [("Fast is not better than slow. Slow is often harder to hold.", "A")]
    kh = PB("plain", "The kit you need",
                   [("Two cones about eight metres apart, and a partner who watches.",
                     False)])
    mvt = [("Walk, then jog, then walk. Thirty seconds each.", False)]
    cap = ("Picture 1.3", "Sorrel sprints. Tuft creeps. Same meadow, two speeds. Look at "
                          "how high each body is.")
    caph = 17 + 14.2 * (len(wrap([(cap[1], "A")], CW - 70, 11.0)) - 1) + 12
    ph = min(341.0, BOT - y - para_h(p1) - para_h(p2) - kh
             - PB("tint", "Move it", mvt) - caph - 40)
    f.add(ph + caph, lambda yy, ph=ph: plate(pg, yy, os.path.join(IMG, "u1_p13_speed.png"),
                                             ph, cap))
    f.add(para_h(p1) + para_h(p2) + 6,
          lambda yy: para(pg, para(pg, yy, p1), p2, after=0))
    f.add(kh + 10, lambda yy: panel(pg, yy, "plain", "The kit you need",
                                    [("Two cones about eight metres apart, and a partner "
                                      "who watches.", False)], icon="kit"))
    f.add(PB("tint", "Move it", mvt),
          lambda yy: panel(pg, yy, "tint", "Move it", mvt, icon="move"))
    log.append(("18", round(f.run(), 1)))
    folio(pg, "1.3  FAST, SLOW, HIGH, LOW", 18)

    # ------------------------------------------------------------ page 19 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.3 · FAST AND SLOW", "Fast and slow")
    f = Flow(pg, y)
    wmt = [("Sorrel runs the eight metres as fast as she can. Then she crosses again as "
            "slowly as she can without stopping. Willow times both with a count of "
            "\u201cone-elephant, two-elephant\u201d.", False)]
    sfy = [("Fast needs a long space behind the finish cone so you can slow down. Do not "
            "run at a wall.", False)]
    tri = ["Cross fast. Cross slow. Tell your partner which felt harder.",
           "Walk on tiptoes (high). Walk in a small squat (low).",
           "Tick the sentence that is true for you."]
    tks = ["Slow was harder than fast.", "High made me wobble.",
           "I could change speed when asked."]
    f.add(PB("plain", "Watch me try", wmt) + 10,
          lambda yy: watch(pg, yy, wmt, "ch_sorrel_t", 54))
    f.add(PB("green", "Safety first", sfy) + 10,
          lambda yy: panel(pg, yy, "green", "Safety first", sfy, icon="safety"))
    f.add(steps_box(tri, tail=tks) + 10,
          lambda yy: steps(pg, yy, "Try it", tri, tail=tks))
    f.add(96, lambda yy: speed_strip(pg, yy))
    log.append(("19", round(f.run(), 1)))
    folio(pg, "1.3  FAST AND SLOW", 19)

    # ------------------------------------------------------------ page 20 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.4", "Hoops, benches, mats")
    f = Flow(pg, y)
    p1 = [("Apparatus", "AB"), (" is kit you move on, over or through. The movement you "
          "already know must still work when the floor changes.", "A")]
    kh = PB("plain", "The kit you need",
                   [("Hoops, a low bench or a line of mats, and a teacher who has tested "
                     "the bench.", False)])
    mvt = [("Bear walk to a hoop and stand inside it.", False)]
    cap = ("Picture 1.4", "Pip crawls through a hoop. A bench and a mat wait behind. The "
                          "whole hoop is in the picture, and so are Pip's feet.")
    caph = 17 + 14.2 * (len(wrap([(cap[1], "A")], CW - 70, 11.0)) - 1) + 12
    ph = min(341.0, BOT - y - para_h(p1) - kh - PB("tint", "Move it", mvt)
             - caph - 30)
    f.add(ph + caph, lambda yy, ph=ph: plate(pg, yy,
                                             os.path.join(IMG, "u1_p14_apparatus.png"),
                                             ph, cap))
    f.add(para_h(p1) + 6, lambda yy: para(pg, yy, p1, after=0))
    f.add(kh + 10, lambda yy: panel(pg, yy, "plain", "The kit you need",
                                    [("Hoops, a low bench or a line of mats, and a teacher "
                                      "who has tested the bench.", False)], icon="kit"))
    f.add(PB("tint", "Move it", mvt),
          lambda yy: panel(pg, yy, "tint", "Move it", mvt, icon="move"))
    log.append(("20", round(f.run(), 1)))
    folio(pg, "1.4  HOOPS, BENCHES, MATS", 20)

    # ------------------------------------------------------------ page 21 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · TOPIC 1.4 · THE MEADOW GAMES",
                         "The meadow games")
    f = Flow(pg, y)
    ld = [("Play three stations. Spend four minutes at each.", "A")]
    wmt = [("Pip steps into the hoop, crawls through, then walks along the bench with his "
            "eyes on the far end. He does not rush the bench.", False)]
    sfy = [("Only one child on a bench. An adult stands at the side. Mats stay flat. Never "
            "jump off a bench in this topic: step down.", False)]
    tri = ["Through a hoop, then along a line of mats.",
           "Change the order: mats first, hoop second.",
           "Tell Willow one thing that changed when the kit was there."]
    stn = [("Space tag", "Walk only. If you are tagged, freeze until someone gives you a "
                         "thumbs-up from a lie-down space away."),
           ("Join the hop", "Hop to a cone, skip home."),
           ("Hoop path", "Three hoops in a line. In, through, out.")]
    tks = ["I can stop when I am asked.", "I can hop and skip.", "I can change speed.",
           "I can use a hoop or a mat without rushing."]
    f.add(lead_h(ld) + 6, lambda yy: lead(pg, yy, ld))
    f.add(PB("plain", "Watch me try", wmt) + 10,
          lambda yy: watch(pg, yy, wmt, "ch_pip_t", 54))
    f.add(PB("green", "Safety first", sfy) + 10,
          lambda yy: panel(pg, yy, "green", "Safety first", sfy, icon="safety"))
    f.add(steps_box(tri) + 10, lambda yy: steps(pg, yy, "Try it", tri))
    f.add(cards_box(stn), lambda yy: cards(pg, yy, stn))
    f.add(ticks_box(tks), lambda yy: ticks(pg, yy, "Look what I can do", tks))
    log.append(("21", round(f.run(), 1)))
    folio(pg, "1.4  THE MEADOW GAMES", 21)

    # ------------------------------------------------------------ page 22 --
    pg, y = content_page(doc, *hdr, "UNIT 1 · HOW DID IT GO?", "How did it go?")
    f = Flow(pg, y)
    intro = [("Colour ", "A"), ("one", "AB"), (" circle in each row. Green means yes, "
             "yellow means nearly, and red means not yet. Not yet is a fine answer: it "
             "just means you have more to do.", "A")]
    rows = ["I can stop when I am asked.", "I can hop and skip.", "I can change speed.",
            "I can use a hoop or a mat without rushing."]
    closing = [("Which page in this unit did you enjoy most? Turn back to it and show "
                "someone why.", "A")]
    ih = lead_h(intro) - 2
    rh = 4 * (34.5 + 6.4) + 4
    ch = para_h(closing, size=11.0, pitch=14.6, after=0) + 4
    ph = min(341.0, BOT - y - ih - rh - ch - 34)
    f.add(ih, lambda yy: lead(pg, yy, intro))
    f.add(rh, lambda yy: traffic(pg, yy, rows))
    f.add(ph + 18, lambda yy, ph=ph: plate(pg, yy, os.path.join(IMG, "u1_close.png"), ph))
    f.add(ch, lambda yy: para(pg, yy, closing, size=11.0, pitch=14.6, colour=hx("4A4234"),
                              after=0))
    log.append(("22", round(f.run(), 1)))
    folio(pg, "UNIT 1 · HOW DID IT GO?", 22)

    doc.save(OUT, deflate=True, garbage=3)
    for name, bottom in log:
        flag = "OVER" if bottom > BOT + 0.5 else "ok"
        print("page %s bottom %.1f  %s" % (name, bottom, flag))
    print("saved", OUT, doc.page_count, "pages")


# ------------------------------------------------------------------ add-ons --
def plate_in(pg, r, path, rtop=96.0, rbot=0.0, corner=None):
    tmp = "/tmp/_in_%s.jpg" % os.path.basename(path).replace(".png", "")
    plate_png(path, tmp, r.width, r.height, rtop, rbot, corner)
    pg.insert_image(r, filename=tmp)


def watch(pg, y, lines, bust, bsize=54):
    """'Watch me try' card with the character's portrait in the top-left corner."""
    pad = 13.0
    ts = 11.5
    body_w = CW - 2 * pad - bsize - 12
    wrapped = [wrap([(t, "AB" if b else "A")], body_w, 13.0) for t, b in lines]
    bh = sum(len(l) * 17.4 + 4 for l in wrapped)
    bsize = min(bsize, bh + 4)
    total = max(pad + ts + 8 + bh + pad - 2, bsize + 2 * pad)
    r = pymupdf.Rect(ML, y, MR, y + total)
    rrect(pg, r, 9, fill=WHITE, stroke=LINE, width=0.75)
    ic_square(pg, ML + pad + 6.6, y + pad + ts * 0.36, 4.6, MID)
    draw(pg, ML + pad + 17.5, y + pad + ts * 0.80, "WATCH ME TRY", "F", ts, MID, track=0.45)
    bx, by = MR - pad - bsize, y + total - pad - bsize
    p = os.path.join(IMG, bust + ".png")
    im = Image.open(p)
    pg.insert_image(pymupdf.Rect(bx, by, bx + bsize, by + bsize), filename=p)
    yy = y + pad + ts + 8
    for ls in wrapped:
        for ln in ls:
            yy += 17.4
            draw(pg, ML + pad + 2, yy, " ".join(w for w, _ in ln), "A", 13.0, INK)
        yy += 4
    return r.y1 + 10


def speed_strip(pg, y):
    """Two-character comparison strip: the same idea at two speeds."""
    h = 96.0
    r = pymupdf.Rect(ML, y, MR, y + h)
    rrect(pg, r, 9, fill=CREAM, stroke=LINE, width=0.75)
    half = CW / 2
    pg.draw_line(pymupdf.Point(ML + half, y + 12), pymupdf.Point(ML + half, y + h - 12),
                 color=LINE, width=0.7)
    for i, (bust, top, sub) in enumerate((
            ("ch_sorrel_t", "FAST", "a long low run, arms working"),
            ("ch_tuft_t", "SLOW", "a small careful creep, body low"))):
        cx = ML + i * half
        p = os.path.join(IMG, bust + ".png")
        im = Image.open(p)
        bw = 62.0
        bh = bw * im.height / im.width
        bh = min(bh, h - 34)
        bw = bh * im.width / im.height
        pg.insert_image(pymupdf.Rect(cx + 18, y + h - 12 - bh, cx + 18 + bw,
                                     y + h - 12), filename=p)
        tx = cx + 18 + bw + 16
        twid = cx + half - 14 - tx
        draw(pg, tx, y + 34, top, "F", 13, MID, track=1.1)
        sub_lines, _ = autowrap([(sub, "A")], twid, 12.0)
        sy = y + 54
        for ln in sub_lines:
            draw(pg, tx, sy, " ".join(w for w, _ in ln), "A", 12.0, MUTED)
            sy += 15.0
    return r.y1 + 10


if __name__ == "__main__":
    build()
