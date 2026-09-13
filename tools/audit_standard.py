#!/usr/bin/env python3
"""Audit a Prime Books master against the Y1-Y4 house standard.

The standard is not described here, it is *measured* from the y01 Physical
Education master and codified as the constants below. Run it on any book:

    .venv/bin/python tools/audit_standard.py                 # every Y1-Y4 book
    .venv/bin/python tools/audit_standard.py y02-science     # one book
    .venv/bin/python tools/audit_standard.py --json out.json

Exit code is the number of books that FAIL a hard check (0 = all clean), so it
can gate a build or a commit.
"""
import json, os, re, sys
import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(REPO, "public", "library")

# --------------------------------------------------------------- the standard --
STD = {
    "page": (612.0, 792.0),          # US Letter, portrait
    "band_h": 47.0,                  # running-header band height
    "rule_h": 1.8,                   # ochre rule under the band
    "rule_hex": "#9a6a12",
    "badge_d": 24.0,                 # folio circle diameter
    "badge_centre": (550.0, 758.0),  # folio circle centre
    "footer_y": 741.0,               # footer label baseline
    "band_text_y": 14.2,             # "Prime School Press" baseline
    "kicker_y": 65.3,                # kicker baseline
    "display_y": 76.3,               # display heading baseline
    "house_tint": "#f6eedc",         # front matter / contents / back matter band
    "fonts_ok": ("Andika", "Fredoka", "Poppins", "Gelasio", "Caveat"),
    "unit_tints": {"1": "#eaf3f9", "2": "#edf3e6", "3": "#fbedec",
                   "4": "#fdf3dc", "5": "#f4eff9", "6": "#faede2"},
    # the six-segment colour bar on the contents page uses the unit MIDs
    "unit_mids": {"1": "#3c7ca6", "2": "#4e6b45", "3": "#b4564e",
                  "4": "#c08a1e", "5": "#7a5fa0", "6": "#b4622a"},
    "unit_deeps": {"1": "#1e4e6b", "2": "#2c4127", "3": "#6e2a25",
                   "4": "#6b4a0c", "5": "#442f63", "6": "#6b3410"},
    # pages 2 and 3 are the "outside" pages: Poppins family, no band, no folio
    "outside_pages": {2, 3},
}


def is_flood(p):
    """A full-bleed unit opener: one saturated rect covering the whole page.

    The engines paint a full-page WHITE rect first on every page, so the flood
    test must exclude paper: a flood is a full-page fill that is not near-white.
    """
    for d in p.get_drawings():
        r = d["rect"]
        if not (d.get("fill") and r.width > 600 and r.height > 780
                and r.x0 < 5 and r.y0 < 5):
            continue
        if max(d["fill"]) < 0.9:            # saturated: a real flood, not paper
            return hx(d["fill"])
    return None


def hx(c):
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)


def spans(p):
    out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                out.append(s)
    return out


def band(p):
    """The full-width tinted band at the top of an interior page."""
    best = None
    for d in p.get_drawings():
        r = d["rect"]
        if d.get("fill") and r.x0 < 5 and r.x1 > 600 and r.y0 < 5 and 20 < r.height < 60:
            if best is None or r.height > best[0].height:
                best = (r, hx(d["fill"]))
    return best


def badge(p):
    for d in p.get_drawings():
        r = d["rect"]
        if d.get("fill") and r.y0 > 720 and 8 < r.width < 40 and abs(r.width - r.height) < 3:
            return r, hx(d["fill"])
    return None, None


def audit(path, slug):
    doc = pymupdf.open(path)
    n = doc.page_count
    f = []                                   # failures
    w = []                                   # warnings
    std = {}

    std["pages"] = n
    std["even_pages"] = n % 2 == 0
    if n % 2:
        f.append("page count %d is ODD - the flipbook shows the back cover alone only when it is even" % n)

    pg = doc[0].rect
    if (round(pg.width, 1), round(pg.height, 1)) != STD["page"]:
        f.append("page size %sx%s, expected %sx%s" % (pg.width, pg.height, *STD["page"]))

    # fonts: no Type3, nothing outside the house families
    fams, bad_fonts = set(), []
    for p in doc:
        for fo in p.get_fonts(full=True):
            name = fo[3]
            if fo[2] == "Type3" or name.lower().startswith(("type3", "helv", "times")):
                bad_fonts.append(name)
            fams.add(name.split("-")[0].split("+")[-1])
    outside = sorted(x for x in fams if not any(x.startswith(k) for k in STD["fonts_ok"]))
    std["font_families"] = sorted(fams)
    if bad_fonts:
        f.append("non-embeddable/base14 fonts present: %s" % sorted(set(bad_fonts))[:4])
    if outside:
        w.append("font families outside the house set: %s" % outside)

    # cover: art, subject, year, and no folio badge. The institutional label
    # lives on the imprint and the back cover, not on the front.
    ctxt = doc[0].get_text()
    if doc[0].get_images(full=True):
        std["cover_has_art"] = True
    else:
        f.append("page 1: no cover art")
    if not re.search(r"Year\s+[1-6]", ctxt):
        f.append("page 1: no 'Year N' line")
    if "Student Manual" not in ctxt and "Student Book" not in ctxt:
        w.append("page 1: no 'Student Manual' / 'Student Book' line")
    if badge(doc[0])[0] is not None:
        f.append("page 1: front cover carries a folio badge")
    std["cover_text"] = ctxt.strip().split("\n")

    # imprint + welcome
    p2 = doc[1].get_text().upper() if n > 1 else ""
    std["imprint_page"] = "IMPRINT" in p2
    if not std["imprint_page"]:
        f.append("page 2: no IMPRINT block")
    for key in ("EDITION", "PUBLISHER", "RIGHTS", "CREDITS"):
        if key not in p2:
            w.append("page 2: imprint is missing the %s row" % key)

    # contents: the six-segment bar and one card per unit
    toc_i = None
    for i in range(min(8, n)):
        t = doc[i].get_text().upper()
        if "CONTENTS" in t and ("UNIT 1" in t or "UNIT  I" in t):
            toc_i = i
            break
    std["contents_page"] = toc_i + 1 if toc_i is not None else None
    if toc_i is None:
        f.append("no contents page in the first 8 pages (needs 'CONTENTS' + 'UNIT 1' cards)")
    else:
        tp = doc[toc_i]
        bands = {hx(d["fill"]) for d in tp.get_drawings()
                 if d.get("fill") and d["rect"].y0 < 220 and 2 < d["rect"].height < 10}
        seg = bands & set(STD["unit_mids"].values())
        std["contents_colour_bar"] = len(seg)
        if len(seg) < 6:
            f.append("contents page %d: colour bar shows %d of 6 unit colours"
                     % (toc_i + 1, len(seg)))
        tt = tp.get_text()
        missing = [u for u in range(1, 7) if "UNIT %d" % u not in tt]
        if missing:
            f.append("contents page: no card for unit(s) %s" % missing)
        if "How did it go?" not in tt:
            w.append("contents page: no 'Unit n - How did it go?' row")

    # running header band, rule and folio badge on every interior page, except
    # the two "outside" pages (2, 3) and the full-bleed unit openers.
    off, openers, bad_flood = [], [], []
    tints_seen = {}
    for i in range(1, n - 1):
        p = doc[i]
        if (i + 1) in STD["outside_pages"]:
            continue
        flood = is_flood(p)
        if flood is not None:                       # unit opener
            openers.append(i + 1)
            if flood not in STD["unit_deeps"].values():
                bad_flood.append((i + 1, flood))
            bd, _ = badge(p)
            if bd is None or abs(bd.width - STD["badge_d"]) > 1.5:
                off.append(i + 1)
            continue
        b = band(p)
        bd, _ = badge(p)
        if not b or bd is None or abs(bd.width - STD["badge_d"]) > 1.5:
            off.append(i + 1)
            continue
        tints_seen[b[1]] = tints_seen.get(b[1], 0) + 1
    std["unit_openers"] = openers
    std["band_and_badge_pages"] = n - 2 - len(off) - len(openers)
    if bad_flood:
        f.append("unit opener(s) not flooded in a unit deep colour: %s" % bad_flood[:4])
    if not openers:
        f.append("no full-bleed unit opener found (a unit must open on its own colour)")
    if off:
        f.append("pages missing the standard band/badge (%d): %s%s"
                 % (len(off), off[:8], " ..." if len(off) > 8 else ""))
    std["band_tints"] = dict(sorted(tints_seen.items(), key=lambda kv: -kv[1]))
    if STD["house_tint"] not in tints_seen:
        w.append("no page uses the house ochre band %s" % STD["house_tint"])

    # house furniture on the first body page: kicker + 24.5pt display heading
    body = None
    for i in range(1, min(12, n - 1)):
        ss = [s for s in spans(doc[i]) if abs(s["size"] - 24.5) < 0.6]
        if ss and band(doc[i]):
            body = i
            break
    if body is None:
        w.append("no interior page carries the 24.5pt Fredoka display heading")
    else:
        std["display_heading_page"] = body + 1
        kick = [s for s in spans(doc[body]) if abs(s["size"] - 9.5) < 0.6 and s["bbox"][1] < 70]
        std["kicker"] = bool(kick)
        if not kick:
            w.append("page %d: no 9.5pt kicker above the display heading" % (body + 1))

    # back cover: label, no folio badge
    last = doc[n - 1]
    lt = last.get_text().upper().replace("  ", " ")
    std["back_cover_label"] = "P R I M E" in last.get_text().upper()
    if not std["back_cover_label"]:
        f.append("last page: no 'P R I M E  S C H O O L  P R E S S' label")
    if badge(last)[0] is not None:
        f.append("last page: back cover carries a folio badge (house rule: none)")
    if "INSIDE THIS BOOK" not in lt:
        w.append("back cover: no INSIDE THIS BOOK card")
    if not re.search(r"pri\s*m\s*e\s*school\.pt|primeschool\.pt", last.get_text().lower()):
        w.append("back cover: no primeschool.pt line")

    # last three pages = the reference apparatus
    std["last_three"] = [doc[i].get_text().strip().split("\n")[0][:30] for i in range(n - 3, n)]
    tail = " ".join(doc[i].get_text().upper() for i in range(n - 3, n))
    if "SOURCES" not in tail:
        w.append("last three pages: no sources page ('Our sources')")
    if "QR" in tail or "WATCH" not in tail:
        w.append("last three pages: no 'Watch and learn' link page")

    ok = not f
    return {"slug": slug, "pages": n, "ok": ok, "failures": f, "warnings": w, "standard": std}


def main():
    argv = sys.argv[1:]
    out = None
    if "--json" in argv:
        i = argv.index("--json")
        out = argv[i + 1]
        del argv[i:i + 2]
    slugs = [a for a in argv if not a.startswith("--")]
    manifest = json.load(open(os.path.join(REPO, "public", "library.json")))
    slugs = slugs or [r["slug"] for r in manifest
                      if r.get("slug", "").startswith(("y01", "y02", "y03", "y04"))]
    results = []
    for slug in slugs:
        path = os.path.join(LIB, slug, "book.pdf")
        if not os.path.exists(path):
            results.append({"slug": slug, "ok": False, "failures": ["no book.pdf"], "warnings": []})
            continue
        try:
            results.append(audit(path, slug))
        except Exception as e:                                  # noqa: BLE001
            results.append({"slug": slug, "ok": False,
                            "failures": ["audit error: %s" % e], "warnings": []})

    print("%-34s %5s %6s %6s  %s" % ("book", "pp", "fail", "warn", "verdict"))
    for r in results:
        print("%-34s %5s %6d %6d  %s" % (r["slug"], r.get("pages", "-"),
                                         len(r["failures"]), len(r["warnings"]),
                                         "PASS" if r["ok"] else "FAIL"))
    nfail = sum(1 for r in results if not r["ok"])
    print("\n%d/%d books pass every hard check" % (len(results) - nfail, len(results)))
    if out:
        json.dump(results, open(out, "w"), indent=1)
        print("written:", out)
    return nfail


if __name__ == "__main__":
    sys.exit(min(120, main()))
