#!/usr/bin/env python3
"""Rebuild the Year 1 Physical Education interior on Prime Books Standard A 2.0.

Runs on top of the current house engine (tools/pb_engine.py), which already
carries one colour per unit and the card-style contents page. What this builder
adds:

* STANDARD A 2.0 TYPE. The engine's A2 ladder is live: 16 pt reading text on
  21 pt leading, 15 pt panels and step lists, larger captions and table cells.
* REPAGINATION. Bigger type moves the page boundaries, so every content page is
  measured block by block and split into continuation pages, then folios and the
  card contents page are regenerated from the finished list (so the contents can
  never drift from the book).
* SCAN AND SHOW. Link-checked educational QR codes are attributed to the unit
  that carries them, tinted in that unit's colour, and scattered over an
  irregular subset of topic pages - never every page.
* PICTURE GLOSSARY. The picture-glossary cards for the fourteen words.
* PARITY. The flipbook needs an even page count; if the rebuilt interior lands
  on an odd number, a teacher's "scan and show" index page is added rather than
  leaving the back cover alone on a spread.

Cover, imprint and the Welcome page (1-3) and the back cover are spliced in from
the master, so nothing outside the interior changes here.
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
TOC_LEAD = "Six units, one after another. Every unit has its own colour."
# unit -> the link-checked addresses that unit may carry
UNIT_LINKS = {
    1: ["supermovers", "shakeup", "nature", "gonoodle"],
    2: ["supermovers_all", "rspb", "gonoodle"],
    3: ["cosmic", "supermovers", "gonoodle"],
    4: ["gonoodle", "yst", "supermovers_all"],
    5: ["yst", "rspb", "bhf"],
    6: ["nhs_active", "bhf", "nhs_five", "nhs_exercise"],
}


# ------------------------------------------------------------- pagination ---
def page_top(title):
    """Reproduces content_page()'s first-content y, so packing matches drawing."""
    ts = E.fit_size(title, "F", 24.5, E.CW, floor=17.0)
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
    """Attach a link-checked QR to an irregular subset of the unit topic pages."""
    placed, by_unit = [], {}
    for p in pages:
        spec = p.get("spec") or {}
        unit = p.get("unit") or 0
        if p["kind"] == "content" and unit in UNIT_LINKS \
                and "TOPIC" in (spec.get("kick") or "").upper():
            by_unit.setdefault(unit, []).append(p)
    for unit, plist in sorted(by_unit.items()):
        pool = UNIT_LINKS[unit]
        picks = sorted(rng.sample(range(len(plist)), min(QR_PER_UNIT, len(plist))))
        for i, idx in enumerate(picks):
            page, key = plist[idx], pool[i % len(pool)]
            page["spec"]["blocks"] = list(page["spec"]["blocks"]) + [
                C.qr(key, blurb=C.LINKS[key][2] + "  " + C.LINKS[key][3])]
            placed.append((key, page["spec"]["title"]))
    for key, want in (("rspb", "meadow"), ("supermovers_all", "Look back")):
        for p in pages:
            spec = p.get("spec") or {}
            if p["kind"] == "content" and want.lower() in (spec.get("title") or "").lower():
                spec["blocks"] = list(spec["blocks"]) + [C.qr(key)]
                placed.append((key, spec["title"]))
                break
    return placed


def remap_groups(groups, first_new):
    """Rewrite every contents-card page number against the rebuilt numbering.

    A contents row is any two-item list/tuple of (label, page). Anything else is
    walked into: the cards nest rows inside dicts and lists.
    """
    def row(x):
        return (isinstance(x, (list, tuple)) and len(x) == 2
                and isinstance(x[0], str) and isinstance(x[1], int))

    def walk(node):
        if row(node):
            num = first_new.get(node[1], node[1])
            return [node[0], num] if isinstance(node, list) else (node[0], num)
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, (list, tuple)):
            out = [walk(x) for x in node]
            return out if isinstance(node, list) else tuple(out)
        return node

    return walk(groups)


def teacher_page():
    """The teacher's one-page index of every address used in the book."""
    links = sorted({k for ks in UNIT_LINKS.values() for k in ks})
    return dict(kind="content", unit=0,
                spec=dict(hl="Prime School Press",
                          hr="Physical Education · Year 1",
                          kick="SCAN AND SHOW · FOR THE TEACHER",
                          title="Scan and show",
                          blocks=[
                              E.B.lead("Every address in this book, in one "
                                       "place, so an adult can check one before "
                                       "the lesson and open it on a screen."),
                              C.qr("supermovers",
                                   "The routine we use most",
                                   "BBC Teach Super Movers: songs and movement "
                                   "for Key Stage 1.  about 5 minutes each"),
                              E.B.reflist([(C.LINKS[k][1], C.LINKS[k][0],
                                            C.LINKS[k][3]) for k in links])]),
                folio="SCAN AND SHOW", num=0)


def assemble(gap=26.0, teacher_index=None):
    """The whole page plan as the book will render it.

    Page count has to come out even (the flipbook shows two pages at a time), so
    when the rebuilt interior is odd the teacher's index page is added just
    before the sources, which also keeps the 'Watch and learn' link page inside
    the last three pages of the book.
    """
    pages, groups = C.build_pages()
    rng = random.Random(SEED)
    placed = plan_qr(pages, rng)
    if teacher_index:
        pages.append(teacher_page())

    # flatten, repaginating content pages; folios are assigned after the split
    flat = []
    for p in pages:
        old = p["num"]
        if p["kind"] == "content":
            for spec in pack(p["spec"], gap):
                flat.append(dict(p, spec=spec, _old=old))
        else:
            flat.append(dict(p, _old=old))

    if teacher_index is None and (3 + len(flat) + 1) % 2:
        idx = next((i for i, p in enumerate(flat)
                    if (p.get("spec") or {}).get("kick", "").startswith("OUR SOURCES")),
                   len(flat))
        flat.insert(idx, dict(teacher_page(), _old=None))

    first_new = {}
    for i, p in enumerate(flat):
        p["num"] = 4 + i
        if p["_old"] is not None:
            first_new.setdefault(p["_old"], p["num"])

    groups = remap_groups(groups, first_new)
    toc_page = [p for p in flat if p["kind"] == "toc"][0]
    toc_page["spec"] = dict(hl="Prime School Press",
                            hr="Physical Education · Year 1",
                            kick="PHYSICAL EDUCATION · YEAR 1",
                            title="What is inside?",
                            blocks=[E.B.toc(groups, lead=TOC_LEAD)])
    return flat, groups, placed


def render(flat, out_path):
    doc = pymupdf.open()
    over, sparse, outofbox = [], [], []
    for p in flat:
        spec = p["spec"]
        if p["kind"] == "opener":
            pg, bottom = E.render_opener(doc, spec, p["num"])
            lim = (20.0, 580.0)
        else:
            pg, bottom, bad = E.render_page(doc, spec, p["folio"], p["num"],
                                            unit=p.get("unit") or 0)
            lim = (E.ML - 1.5, E.MR + 1.5)
            text_len = len(pg.get_text().strip())
            if bad:
                over.append((p["num"], round(bottom, 1)))
            if text_len < 140 and not any(n == "plate" for n, _ in spec["blocks"]):
                sparse.append((p["num"], text_len))
        for b in pg.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            if x1 > lim[1] or x0 < lim[0] or y1 > 776:
                outofbox.append((p["num"], round(x0, 1), round(x1, 1), round(y1, 1)))

    # The outside pages are not rebuilt: cover, imprint and the Welcome page come
    # from the published master, and so does the back cover. The master may
    # already be a previous Standard A 2.0 build, so identify those pages by what
    # is on them rather than by a fixed page count.
    old = pymupdf.open(MASTER)
    assert old.page_count >= 8 and old.page_count % 2 == 0, old.page_count
    assert "Physical Education" in old[0].get_text(), "master p1 is not the cover"
    assert "IMPRINT" in old[1].get_text().upper().replace(" ", ""), "master p2"
    assert "WELCOME" in old[2].get_text().upper(), "master p3 is not the Welcome"
    back = old.page_count - 1
    assert "PRIME" in old[back].get_text().upper().replace(" ", ""), "back cover"
    out = pymupdf.open()
    out.insert_pdf(old, from_page=0, to_page=2)       # cover, imprint, Welcome
    out.insert_pdf(doc)                              # rebuilt interior
    out.insert_pdf(old, from_page=back, to_page=back)  # back cover
    # pages 2 and 3 inherit an older number badge; give them the house badge
    E.set_theme(E.UNIT_THEMES[0])
    for i in (1, 2):
        pg = out[i]
        pg.draw_rect(pymupdf.Rect(526, 726, 578, 778), color=None, fill=(1, 1, 1))
        pg.draw_circle(E.FOLIO_C, E.FOLIO_R, color=None, fill=E.TH["mid"])
        E.draw_c(pg, E.FOLIO_C[0], E.FOLIO_C[1] + 3.9, str(i + 1), "F", 11, (1, 1, 1))
    out.set_metadata(old.metadata)
    out.save(out_path, deflate=True, garbage=3, clean=True)
    return out.page_count, over, sparse, outofbox


def main():
    os.makedirs(WORK, exist_ok=True)
    flat, groups, placed = assemble()
    interior = len(flat)
    total = 3 + interior + 1
    if (interior + 4) % 2 == 0 and any(
            (p.get("spec") or {}).get("title") == "Scan and show" for p in flat):
        print("odd interior: the teacher index page was added before the sources")

    total, over, sparse, outofbox = render(flat, OUT)
    unit_counts = {}
    for p in flat:
        if p["kind"] == "content" and (p.get("unit") or 0):
            unit_counts[p["unit"]] = unit_counts.get(p["unit"], 0) + 1
    report = dict(interior=interior, total=total, even=total % 2 == 0,
                  qr=[k for k, _ in placed],
                  qr_pages=[t for _k, t in placed],
                  overflow=over, sparse=sparse, out_of_margin=outofbox,
                  unit_pages=unit_counts,
                  themes={u: ("#" + "".join("%02x" % round(c * 255)
                                            for c in t["mid"]))
                          for u, t in E.UNIT_THEMES.items() if u})
    with open(os.path.join(WORK, "report.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print("interior pages :", interior, " total:", total, "even:", total % 2 == 0)
    print("QR codes       :", len(placed), "on", len(set(report["qr_pages"])), "pages")
    for k, t in placed:
        print("   %-16s %s" % (k, t[:56]))
    print("unit pages     :", unit_counts)
    print("overflow       :", over)
    print("sparse         :", sparse)
    print("out of margin  :", outofbox)
    return 0


if __name__ == "__main__":
    sys.exit(main())
