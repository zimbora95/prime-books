#!/usr/bin/env python3
"""Standards checker for the locked Years 1-4 standard (edition A-2.1).

This is the machine half of the standard. It measures the published master of a
book against the locked tokens in `public/standards/years-1-4.json` and reports:

    HARD   a structural or technical truth that is wrong (page size, Type3 font,
           a missing folio on a cover, text outside the content box, a contents
           bar that does not match the book's own unit count, no unit opener)
    SOFT   design conformance that needs a human eye (extent in the 12n-1 print
           series, folio coverage, the reading size against the year ladder)

What it CANNOT check, and therefore never certifies: teacher content
preservation, image rights, illustration quality, colour contrast, QR targets,
and the physical print proof. Those stay in the manual checklist, so a green
machine result is "ready for sign-off", never "standardised".

Usage
    .venv/bin/python tools/standards_check.py                    # every book
    .venv/bin/python tools/standards_check.py y01-art-and-design
    .venv/bin/python tools/standards_check.py --json out.json
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone

import pymupdf

pymupdf.TOOLS.mupdf_display_errors(False)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(REPO, "public", "library")
LOCK = os.path.join(REPO, "public", "standards", "years-1-4.json")

# The authoring page is US Letter; the printer's trim is 216 x 279 mm. They are
# the same physical book to within 0.4 mm, so both are accepted.
LETTER = (612.0, 792.0)
PRINT_TRIM = (612.28, 790.87)
MEDIA = (629.28, 807.87)          # trim + 3 mm bleed each side, if a pack is checked
CONTENT_BOX = (50.25, 66.0, 561.75, 734.25)   # the historic PE content box
SAFE_X = (42.0, 570.0)            # 15 mm outer margin mirrored; 56.7 pt on the binding edge
FOOT_ZONE = 741.0                 # the footer rule: nothing but the label and folio below it
BADGE_SIZE = 24.0
BADGE_CENTRE = (550.0, 758.0)
HOUSE_FONTS = ("Andika", "Fredoka", "Poppins", "Gelasio", "Caveat")
BAD_BASE14 = ("helv", "times", "cour", "symb", "zapf", "arial", "verdana")


def lock() -> dict:
    try:
        return json.loads(open(LOCK, encoding="utf-8").read())
    except Exception:                                        # noqa: BLE001
        return {}


def hx(c) -> str:
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)


def spans(p):
    out = []
    for b in p.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                out.append(s)
    return out


def badge(p):
    for d in p.get_drawings():
        r = d["rect"]
        if d.get("fill") and r.y0 > 720 and 8 < r.width < 40 and abs(r.width - r.height) < 3:
            return r, hx(d["fill"])
    return None, None


def band(p):
    for d in p.get_drawings():
        r = d["rect"]
        if d.get("fill") and r.x0 < 5 and r.x1 > 600 and r.y0 < 5 and 20 < r.height < 60:
            return r, hx(d["fill"])
    return None, None


def is_flood(p):
    """A full-bleed opener: a saturated full-page fill. The engines paint a white
    page rect first, so the not-near-white test is load-bearing."""
    for d in p.get_drawings():
        r = d["rect"]
        if (d.get("fill") and r.width > 600 and r.height > 780 and r.x0 < 5 and r.y0 < 5
                and max(d["fill"]) < 0.9):
            return hx(d["fill"])
    return None


def legal_counts(lo_pp=11, hi_pp=None, step=12):
    """Every legal BookVault extent: one less than a multiple of 12."""
    counts, v = [], 11
    while v <= (hi_pp or 12 * 40 - 1):
        counts.append(v)
        v += step
    return counts


def nearest_legal(n):
    c = legal_counts()
    below = max([x for x in c if x <= n], default=None)
    above = min([x for x in c if x >= n], default=None)
    return [x for x in (below, above) if x is not None]


def check(path: str, slug: str, lk: dict, year=None) -> dict:
    doc = pymupdf.open(path)
    try:
        return _check(doc, slug, lk, year)
    finally:
        doc.close()


def _check(doc, slug, lk, year=None) -> dict:
    n = doc.page_count
    f, w = [], []
    facts = {}
    r0 = doc[0].rect
    size = (round(r0.width, 2), round(r0.height, 2))
    facts["page_size"] = size

    # 1. the file itself ----------------------------------------------------
    ok_sizes = [LETTER, PRINT_TRIM, MEDIA]
    if not any(abs(size[0] - a) < 0.6 and abs(size[1] - b) < 0.6 for a, b in ok_sizes):
        f.append("page size %gx%g is not US Letter 612x792 (or the 216x279 mm print trim)" % size)

    # 2. fonts --------------------------------------------------------------
    fams, bad = set(), []
    for p in doc:
        for fo in p.get_fonts(full=True):
            name = fo[3]
            low = name.lower()
            if fo[2] == "Type3" or low.startswith("type3") or any(low.startswith(b) for b in BAD_BASE14):
                bad.append(name)
            fams.add(name.split("-")[0].split("+")[-1].replace("MT", ""))
    facts["font_families"] = sorted(fams)
    if bad:
        f.append("non-embeddable or base-14 fonts present: %s" % sorted(set(bad))[:4])
    outside = sorted(x for x in fams if not any(x.startswith(k) for k in HOUSE_FONTS))
    if outside:
        w.append("font families outside the house set: %s" % outside)

    # 3. covers -------------------------------------------------------------
    if badge(doc[0])[0] is not None:
        f.append("page 1: front cover carries a folio badge")
    last = doc[n - 1]
    if badge(last)[0] is not None:
        f.append("last page: back cover carries a folio badge")
    if "P R I M E" not in last.get_text().upper():
        f.append("last page: no 'P R I M E  S C H O O L  P R E S S' label")

    # 4. contents: the bar has one segment per unit, and a card per unit ----
    toc_i, unit_nums = None, set()
    for i in range(min(8, n)):
        t = doc[i].get_text().upper()
        if "CONTENTS" in t:
            toc_i = i
            unit_nums = {int(m) for m in re.findall(r"\bUNIT\s+([1-9])\b", t)}
            unit_nums |= {len(m) for m in re.findall(r"\bUNIT\s+(I|II|III|IV|V|VI|VII|VIII|IX|X)\b", t)
                          for m in [m.replace("IV", "IIII").replace("IX", "VIIII")]}
            if unit_nums:
                break
    facts["contents_page"] = (toc_i + 1) if toc_i is not None else None
    unit_count = max(unit_nums) if unit_nums else None
    facts["unit_count"] = unit_count
    if toc_i is None:
        f.append("no contents page found in the first 8 pages")
    else:
        tp = doc[toc_i]
        # the bar and the per-unit cards both carry the unit colour, so every
        # distinct palette colour on the page counts as one unit's presence
        draws = {hx(d["fill"]).lower() for d in tp.get_drawings() if d.get("fill")}
        ladder = {r["mid"].lower() for r in lk.get("unit_palette", {}).get("rungs", [])}
        ladder |= {r["deep"].lower() for r in lk.get("unit_palette", {}).get("rungs", [])}
        ladder |= {"#3c7ca6", "#4e6b45", "#b4564e", "#c08a1e", "#7a5fa0", "#b4622a",
                   "#1e4e6b", "#2c4127", "#6e2a25", "#6b4a0c", "#442f63", "#6b3410"}
        seg = sorted(draws & ladder)
        facts["contents_segments"] = len(seg)
        if unit_count:
            if len(seg) < unit_count:
                f.append("contents page shows %d of %d unit colours: the standard wants one "
                         "bar segment and one card per unit" % (len(seg), unit_count))
            missing = [u for u in range(1, unit_count + 1)
                       if not re.search(r"\bUNIT\s+%d\b" % u, tp.get_text().upper())]
            if missing:
                f.append("contents page: no card for unit(s) %s" % missing)
        elif len(seg) < 2:
            w.append("contents colour bar: fewer than two unit colours detected")

    # 5. unit openers -------------------------------------------------------
    openers, bad_flood, off_band, off_badge = [], [], [], []
    tint_any = {r["tint"].lower() for r in lk.get("unit_palette", {}).get("rungs", [])}
    tint_any |= {"#f6eedc", "#eaf3f9", "#edf3e6", "#fbedec", "#fdf3dc", "#f4eff9", "#faede2"}
    deep_any = {r["deep"].lower() for r in lk.get("unit_palette", {}).get("rungs", [])}
    deep_any |= {r["mid"].lower() for r in lk.get("unit_palette", {}).get("rungs", [])}
    deep_any |= {"#1e4e6b", "#2c4127", "#6e2a25", "#6b4a0c", "#442f63", "#6b3410",
                 "#3c7ca6", "#4e6b45", "#b4564e", "#c08a1e", "#7a5fa0", "#b4622a"}
    for i in range(1, n - 1):
        p = doc[i]
        flood = is_flood(p)
        if flood is not None:
            openers.append(i + 1)
            if flood.lower() not in deep_any:
                bad_flood.append((i + 1, flood))
            continue
        b, bd = band(p), badge(p)[0]
        if b is None:
            off_band.append(i + 1)
        if bd is None or abs(bd.width - BADGE_SIZE) > 1.5:
            off_badge.append(i + 1)
    facts["unit_openers"] = openers
    facts["pages_without_band"] = len(off_band)
    facts["pages_without_folio"] = len(off_badge)
    if not openers:
        f.append("no full-bleed unit opener found")
    if bad_flood:
        f.append("opener(s) not flooded in a unit deep colour: %s" % bad_flood[:4])
    interior = max(1, n - 2)
    if len(off_badge) > 0.10 * interior:
        f.append("%d of %d interior pages have no folio badge" % (len(off_badge), interior))
    elif off_badge:
        w.append("%d interior page(s) without a folio badge: %s"
                 % (len(off_badge), off_badge[:8]))
    if len(off_band) > 0.10 * interior:
        w.append("%d of %d interior pages have no running-header band"
                 % (len(off_band), interior))

    # 6. text inside the box, and the reading size --------------------------
    escaped, sizes = [], {}
    left, top, right, bottom = CONTENT_BOX
    floods = set(openers)
    for i, p in enumerate(doc):
        pg = i + 1
        for s in spans(p):
            x0, y0, x1, y1 = s["bbox"]
            if i in (0, n - 1) or pg in floods:
                continue                       # covers and openers are full bleed
            if y0 > 725:
                continue                       # footer label and folio badge zone
            if (y1 > FOOT_ZONE or x0 < SAFE_X[0] or x1 > SAFE_X[1]
                    or y0 < 12.0):
                escaped.append(pg)
            sz = round(s["size"], 1)
            sizes[sz] = sizes.get(sz, 0) + len(s["text"])
    facts["text_outside_box_pages"] = sorted(set(escaped))[:10]
    if escaped:
        f.append("text outside the content box on page(s) %s"
                 % sorted(set(escaped))[:8])
    # the year's reading size is the largest size that carries a real body of text
    body = max(((sz, ch) for sz, ch in sizes.items() if ch >= 300), key=lambda kv: kv[1],
               default=(None, 0))
    facts["modal_text_size_pt"] = body[0]
    ymap = {k: v["size_pt"] for k, v in lk.get("typography", {}).get("reading_ladder", {}).items()}
    facts["reading_ladder_pt"] = ymap
    want = ymap.get(str(year)) if year else None
    facts["year"] = year
    if want and body[0] and abs(body[0] - want) > 0.6:
        w.append("modal reading size %.1f pt, the Year %s ladder says %.1f pt"
                 % (body[0], year, want))

    # 7. extent -------------------------------------------------------------
    legal = legal_counts()
    facts["extent_legal"] = n in legal
    if n not in legal:
        w.append("extent %d is not a legal BookVault count; nearest are %s"
                 % (n, nearest_legal(n)))

    # 8. no half-blank pages ------------------------------------------------
    # The teacher's rule: a page that stops two thirds of the way down reads as
    # an unfinished print file. Measured from the RENDERED page, never from the
    # elements that claim to have drawn it - an empty box drawn the width of the
    # page is still a half-blank page, and a folio badge is text at the foot.
    S = 0.5
    skip = {0, n - 1} | {p - 1 for p in openers}
    slack, blank = [], []
    for i in range(n):
        if i in skip:
            continue
        p = doc[i]
        if is_flood(p) is not None:          # a full-bleed page IS its picture
            continue
        pix = p.get_pixmap(matrix=pymupdf.Matrix(S, S))
        pw, ph, pn = pix.width, pix.height, pix.n
        buf = pix.samples
        counts = {}
        for y in range(0, ph, 2):
            row = y * pw * pn
            for x in range(0, pw, 2):
                k = buf[row + x * pn:row + x * pn + 3]
                counts[k] = counts.get(k, 0) + 1
        paper = max(counts.items(), key=lambda kv: kv[1])[0]
        foot = min(int(CONTENT_BOX[3] * S), ph)
        low, high = 0, 0
        bleed = False
        edges = [False, False]
        for y in range(foot):
            row = y * pw * pn
            # any ink at all, against the page's own paper: a page whose last
            # fifth carries nothing but paper is half blank whatever the layout
            # claims to have drawn there. (A tint or a picture that reaches the
            # foot IS ink, and a page built that way is not half blank.)
            run = 0
            for x in range(pw):
                o = row + x * pn
                if max(abs(buf[o] - paper[0]), abs(buf[o + 1] - paper[1]),
                       abs(buf[o + 2] - paper[2])) > 24:
                    run += 1
                    right = x
                    if run >= 2:             # ink, not noise
                        low = max(low, y)
                        high = max(high, right)
                        if x <= 2:
                            edges[0] = True
                        if x >= pw - 3:
                            edges[1] = True
                else:
                    run = 0
            if edges[0] and edges[1] and (y < 3 or y > foot - 3):
                bleed = True
        if bleed:                            # a full-bleed page IS its picture
            continue
        gap = CONTENT_BOX[3] - low / S
        gap_r = CONTENT_BOX[2] - high / S
        if gap > 60 or gap_r > 62:
            row = (i + 1, round(gap), round(gap_r))
            (blank if gap > 200 or gap_r > 202 else slack).append(row)
    facts["half_blank_pages"] = [b[0] for b in blank][:12]
    facts["pages_ending_short"] = [s[0] for s in slack][:12]
    # The fill rule is the standard's, so it is a verdict on a standardised
    # edition and a record only on a master - a master was not built to it, and
    # failing every old book would drown the sweep in noise that means nothing.
    strict = str(slug).endswith("-standard")
    if blank and strict:
        f.append("%d page(s) stop two thirds of the way down - the teacher's rule is "
                 "that no page is left half blank: %s (empty paper at the foot in pt: %s)"
                 % (len(blank), [b[0] for b in blank][:8], [(b[0], b[1]) for b in blank][:8]))
    if slack and strict:
        w.append("%d page(s) end a little short of the foot: %s"
                 % (len(slack), [(s[0], s[1]) for s in slack][:8]))
    if (blank or slack) and not strict:
        w.append("fill recorded only (this is a master, not a standardised edition): "
                 "%d page(s) end short of the foot, %d stop two thirds down"
                 % (len(slack), len(blank)))

    # 9. items that carry a picture and items that do not ---------------------
    # Reported, never failed. The engine has two legitimate forms of a step: one
    # with a plate in the column beside it, and one that is words and the child's
    # own ticks and runs the full width of the column (`if not art_w` in
    # page_task). A page with four items and three plates is therefore normal,
    # and calling it a defect was wrong - it is listed here only so a reviewer
    # can see the shape of a page at a glance.
    item_pages = []
    for i in range(n):
        items = doc[i].get_text().count("Tries")
        if not items:
            continue
        plates = len(doc[i].get_images(full=True))
        if items != plates:
            item_pages.append({"page": i + 1, "items": items, "plates": plates})
    facts["task_pages_items_and_plates_differ"] = item_pages[:12]

    facts["manual_checks_still_required"] = [
        "teacher content preserved on its page",
        "reading size approved for the year",
        "illustration quality, rights and credits",
        "contrast and no colour-only coding",
        "every QR code decoded and every URL opened",
        "one physical print proof held in the hand",
    ]
    return {
        "slug": slug,
        "pages": n,
        "spec": lk.get("id", "A-2.1-Y1-4"),
        "ok": not f,
        "failures": f,
        "warnings": w,
        "facts": facts,
    }


def main() -> int:
    argv = sys.argv[1:]
    out = None
    if "--json" in argv:
        i = argv.index("--json")
        out = argv[i + 1]
        del argv[i:i + 2]
    slugs = [a for a in argv if not a.startswith("--")]
    manifest = json.load(open(os.path.join(REPO, "public", "library.json"), encoding="utf-8"))
    known = {r.get("slug") for r in manifest}
    bad = [s for s in slugs if s not in known]
    if bad:
        sys.exit("not a book slug in public/library.json: %s" % ", ".join(bad))
    slugs = slugs or [r["slug"] for r in manifest]
    global YEARS
    YEARS = {}
    for r in manifest:
        y = str(r.get("year") or "").strip()
        m = re.match(r"(?:Year\s*)?(\d+)", y)
        if m:
            YEARS[r["slug"]] = int(m.group(1))
    lk = lock()
    results = []
    for slug in slugs:
        path = os.path.join(LIB, slug, "book.pdf")
        if not os.path.exists(path):
            results.append({"slug": slug, "ok": False, "failures": ["no book.pdf"],
                            "warnings": [], "facts": {}})
            continue
        try:
            results.append(check(path, slug, lk, YEARS.get(slug)))
        except Exception as e:                                # noqa: BLE001
            results.append({"slug": slug, "ok": False,
                            "failures": ["check error: %s" % e], "warnings": [], "facts": {}})
    print("%-34s %5s %5s %5s  %s" % ("book", "pp", "fail", "warn", "verdict"))
    for r in results:
        print("%-34s %5s %5d %5d  %s" % (r["slug"], r.get("pages", "-"),
                                         len(r["failures"]), len(r["warnings"]),
                                         "CLEAN" if r["ok"] else "FAIL"))
    nf = sum(1 for r in results if not r["ok"])
    print("\n%d/%d books pass every machine check" % (len(results) - nf, len(results)))
    print("machine-clean is not standardised: the manual checklist still applies")
    if out:
        json.dump({"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                   "spec": lk.get("id"), "books": results},
                  open(out, "w"), indent=1)
        print("written:", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
