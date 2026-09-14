#!/usr/bin/env python3
"""Rebuild Year 1 Physical Education onto Prime Books Standard A 2.0.

Deltas against the master now on disk:

* SIX UNIT THEMES. The previous build never called set_theme(), so every
  interior page kept the module-global ochre theme and the whole book read as
  one colour. Each unit now carries its own named theme (band tint, rule,
  kicker, headings, badges, opener flood), and the contents page is colour-keyed
  to the units it lists.
* STANDARD A 2.0 TYPE. 16 pt reading text on 21 pt leading, 24 pt page titles,
  larger step lists, panels and captions, measured with the same profile the
  pages are drawn with.
* REPAGINATION. Bigger type moves the page boundaries, so content pages are
  packed block by block and split into continuation pages before folios and the
  contents page are generated.
* SCAN AND SHOW. Link-checked educational QR codes on an irregular subset of
  topic pages - never every page - in the unit's own colour, and every rendered
  code is decoded back to its URL as a gate.

Cover (page 1), imprint (page 2) and back cover are spliced from the master, so
nothing outside the interior changes here.
"""
import json
import os
import random
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WORK = os.path.join(REPO, "work", "y01pe_a2")
sys.path.insert(0, HERE)

import pb_engine as E            # noqa: E402
import y01pe_book_content as C   # noqa: E402

E.IMG_DIR = os.environ.get("PB_IMG_DIR") or os.path.join(REPO, "work", "y01pe", "img")
MASTER = os.path.join(REPO, "public", "library", "y01-physical-education", "book.pdf")
OUT = os.path.join(WORK, "book_new.pdf")
SEED = 20260914
QR_PER_UNIT = 3


def theme(deep, mid, tint, line):
    return dict(deep=E.hx(deep), mid=E.hx(mid), tint=E.hx(tint), line=E.hx(line),
                cream=E.hx("fffbf3"), amber=E.hx("f1b300"), green=E.hx("4e6b45"),
                gtint=E.hx("edf3e6"), warn=E.hx("b4442a"), wtint=E.hx("faede4"),
                ink=E.hx("2b2721"), muted=E.hx("6e6759"),
                band_text=E.hx("ffffff"), sub=E.hx("3a3226"))


HOUSE = E.PE                      # ochre: cover, imprint, front and back matter
UNIT_THEMES = {
    1: (theme("#2c4127", "#4e6b45", "#edf3e6", "#d5e0cb"), "Meadow green"),
    2: (theme("#1e4e6b", "#3c7ca6", "#eaf3f9", "#cfe0eb"), "Watching blue"),
    3: (theme("#6e2a25", "#b4564e", "#fbedec", "#edd6d3"), "Dancing rose"),
    4: (theme("#6b4a0c", "#c08a1e", "#fdf3dc", "#f0e0bb"), "Team amber"),
    5: (theme("#442f63", "#7a5fa0", "#f4eff9", "#e2d9ee"), "Responsibility violet"),
    6: (theme("#6b3410", "#b4622a", "#faede2", "#eed9c8"), "Healthy terracotta"),
}
# which link-checked addresses belong to which unit; the seeded scatter decides
# which pages of that unit actually carry one (roughly one page in three)
UNIT_LINKS = {
    1: ["supermovers", "shakeup", "nature", "gonoodle"],
    2: ["supermovers_all", "rspb", "gonoodle"],
    3: ["cosmic", "supermovers", "gonoodle"],
    4: ["gonoodle", "yst", "supermovers_all"],
    5: ["yst", "rspb", "bhf"],
    6: ["nhs_active", "bhf", "nhs_five", "nhs_exercise"],
}
WORD_UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}


def unit_of(spec):
    """Read the unit number out of a page's running head, if it has one."""
    spec = spec or {}
    for key in ("kick", "hl", "hr"):
        text = (spec.get(key) or "").replace("·", " ").replace("|", " ")
        for i, word in enumerate(text.split()):
            if word.lower() in ("unit", "units"):
                parts = text.split()
                if i + 1 < len(parts):
                    nxt = parts[i + 1].strip(".,:").lower()
                    if nxt.isdigit():
                        return int(nxt)
                    if nxt in WORD_UNITS:
                        return WORD_UNITS[nxt]
    return None


def theme_for(spec):
    n = unit_of(spec)
    return UNIT_THEMES[n][0] if n in UNIT_THEMES else HOUSE


# ------------------------------------------------------------- pagination ---
def page_top(title):
    """Reproduces content_page()'s first-content y, so packing matches drawing."""
    ts = E.fit_size(title, "F", 24.0, E.CW, floor=17.0)
    return E.TOP + 1.0 + 7.6 + 6.0 + ts * 0.80 + 8


def pack(spec, gap=26.0):
    """Split one page spec into as many pages as the measure requires."""
    title = spec["title"]
    room = E.BOT - page_top(title)
    chunks, cur, used = [], [], 0.0
    for name, payload in spec["blocks"]:
        p = dict(payload)
        h = p["minh"] if (name == "plate" and p.get("flex")) else E.BLOCKS[name][0](p)
        if not cur:
            cur, used = [(name, p)], h
        elif used + h + gap > room:
            chunks.append(cur)
            cur, used = [(name, p)], h
        else:
            cur.append((name, p))
            used += h + gap
    if cur:
        chunks.append(cur)

    out = []
    for i, blocks in enumerate(chunks):
        flexes = [p for n, p in blocks if n == "plate" and p.get("flex")]
        if len(chunks) > 1:
            for n, p in blocks:
                if n == "plate" and p.get("flex"):
                    p["flex"] = (i == len(chunks) - 1) and len(flexes) == 1
                    if not p["flex"]:
                        p["height"] = p["minh"]
        if len([n for n, _ in blocks if n == "plate"]) > 1:
            for n, p in blocks:
                if n == "plate":
                    p["flex"] = False
        out.append(dict(spec, title=title if not i else title + " (continued)",
                        blocks=blocks))
    return out


def plan_qr(pages, rng):
    """Attach a link-checked QR to an irregular subset of the topic pages."""
    placed = []
    by_unit = {}
    for p in pages:
        spec = p.get("spec") or {}
        u = unit_of(spec)
        if p["kind"] == "content" and u in UNIT_THEMES \
                and "TOPIC" in (spec.get("kick") or "").upper():
            by_unit.setdefault(u, []).append(p)
    for u, plist in sorted(by_unit.items()):
        pool = UNIT_LINKS[u]
        picks = sorted(rng.sample(range(len(plist)), min(QR_PER_UNIT, len(plist))))
        for i, idx in enumerate(picks):
            page, key = plist[idx], pool[i % len(pool)]
            page["spec"]["blocks"] = list(page["spec"]["blocks"]) + [
                C.qr(key, blurb=C.LINKS[key][2] + "  " + C.LINKS[key][3])]
            placed.append((page["num"], key, page["spec"]["title"]))
    for key, want in (("rspb", "meadow"), ("supermovers_all", "Look back")):
        for p in pages:
            spec = p.get("spec") or {}
            if p["kind"] == "content" and want.lower() in (spec.get("title") or "").lower():
                spec["blocks"] = list(spec["blocks"]) + [C.qr(key)]
                placed.append((p["num"], key, spec["title"]))
                break
    return placed


def assemble():
    """The whole page plan, exactly as the book renders it: themes applied, QR
    codes placed, overflowing content pages split, folios renumbered and the
    contents page generated from the finished list. Returns (flat, entries)."""
    pages, toc = C.build_pages()
    rng = random.Random(SEED)
    for p in pages:
        p["theme"] = theme_for(p.get("spec"))
    placed = plan_qr(pages, rng)

    flat, first_new = [], {}
    for p in pages:
        old = p["num"]
        if p["kind"] == "content":
            for spec in pack(p["spec"]):
                flat.append(dict(p, spec=spec, _old=old))
        else:
            flat.append(dict(p, _old=old))
    for i, p in enumerate(flat):
        p["num"] = 3 + i
        first_new.setdefault(p["_old"], p["num"])

    by_num = {p["num"]: p for p in flat}

    def colour_of(num):
        p = by_num.get(num)
        if not p:
            return None
        t = p["theme"]
        return None if t is HOUSE else (t["deep"] if p["kind"] == "opener" else t["mid"])

    entries = []
    for label, oldnum, lvl in toc:
        entries.append((label, first_new.get(oldnum, oldnum), lvl,
                        colour_of(first_new.get(oldnum, oldnum))))

    toc_page = [p for p in flat if p["kind"] == "toc"][0]
    toc_page["spec"] = dict(
        hl="Prime School Press", hr="Physical Education · Year 1",
        kick="PHYSICAL EDUCATION · YEAR 1", title="What is inside?",
        blocks=[E.B.toc(entries)])
    return flat, entries, placed


def main():
    os.makedirs(WORK, exist_ok=True)
    flat, entries, placed = assemble()

    # ---- render -----------------------------------------------------------
    doc = pymupdf.open()
    over, sparse, outofbox, bands, qr_pages = [], [], [], [], []
    for p in flat:
        E.set_theme(p["theme"])
        spec = p["spec"]
        if p["kind"] == "opener":
            pg, bottom = E.render_opener(doc, spec, p["num"])
            lim = (20.0, 580.0)
        else:
            pg, bottom, bad = E.render_page(doc, spec, p["folio"], p["num"])
            lim = (E.ML - 1.5, E.MR + 1.5)
            text_len = len(pg.get_text().strip())
            if bad:
                over.append((p["num"], round(bottom, 1)))
            if text_len < 140 and not any(n == "plate" for n, _ in spec["blocks"]):
                sparse.append((p["num"], text_len))
            if any(n == "qr" for n, _ in spec["blocks"]):
                qr_pages.append(p)
        for b in pg.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            if x1 > lim[1] or x0 < lim[0] or y1 > 776:
                outofbox.append((p["num"], round(x0, 1), round(x1, 1), round(y1, 1)))
        pix = pg.get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False)
        samples = pix.pixel(int(E.W / 2), int(E.BAND_H - 0.5))
        band = "#%02x%02x%02x" % samples[:3]
        bands.append((p["num"], unit_of(spec) or 0, band))

    # ---- decode every rendered QR back to its URL -------------------------
    det = cv2 = None
    try:
        import cv2
        det = cv2.QRCodeDetector()
    except Exception as exc:                    # pragma: no cover
        print("!! no cv2, cannot decode QRs:", exc)
    decoded, failed = [], []
    if det is not None:
        import numpy as np
        for p in qr_pages:
            page = doc[p["num"] - 3]
            pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), alpha=False)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n)[:, :, :3]
            ok, texts, _pts, _ = det.detectAndDecodeMulti(img)
            seen = {t.strip() for t in (texts or []) if t}
            want = [b[1]["url"].strip() for b in p["spec"]["blocks"] if b[0] == "qr"]
            missing = [u for u in want if u not in seen]
            if missing:
                failed.append((p["num"], sorted(seen), missing))
            else:
                decoded.extend((p["num"], u) for u in want)

    # ---- splice outside pages from the master -----------------------------
    old = pymupdf.open(MASTER)
    assert old.page_count == 72, old.page_count
    out = pymupdf.open()
    out.insert_pdf(old, from_page=0, to_page=1)
    out.insert_pdf(doc)
    out.insert_pdf(old, from_page=71, to_page=71)
    out.set_metadata(old.metadata)
    out.save(OUT, deflate=True, garbage=3, clean=True)

    unit_bands = {}
    for num, u, band in bands:
        unit_bands.setdefault(u, set()).add(band)
    report = dict(interior=doc.page_count, total=out.page_count,
                  qr_pages=[(n, k) for n, k, _t in placed],
                  qr_decoded=len(decoded), qr_failed=failed,
                  overflow=over, sparse=sparse, out_of_margin=outofbox,
                  unit_bands={u: sorted(v) for u, v in unit_bands.items()},
                  themes={u: name for u, (_t, name) in UNIT_THEMES.items()})
    with open(os.path.join(WORK, "report.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print("interior pages      :", doc.page_count, "(master interior was 69)")
    print("total pages         :", out.page_count)
    print("QR codes placed     :", len(placed), "decoded:", len(decoded))
    for n, k, t in placed:
        print("   p%-3d %-16s %s" % (n, k, t[:52]))
    print("QR failures         :", failed)
    print("unit band colours   :", {u: sorted(v)[0] for u, v in unit_bands.items()})
    print("overflowing pages   :", over)
    print("sparse pages        :", sparse)
    print("out-of-margin text  :", outofbox)
    return 0


if __name__ == "__main__":
    sys.exit(main())
