#!/usr/bin/env python3
"""Build the whole Year 1 Physical Education book in the Prime Books house style.

Pages 1 (cover), 2 (imprint) and 3 (Welcome, the teacher's chosen design) are
kept from the master, and so is the back cover. Every page between them is
rebuilt from tools/y01pe_book_content.py, each page carrying its unit colour.
"""
import os, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
WORK = os.path.join(REPO, "work", "y01pe")
sys.path.insert(0, HERE)

import pb_engine as E            # noqa: E402
import y01pe_book_content as C   # noqa: E402

E.IMG_DIR = os.environ.get("PB_IMG_DIR") or os.path.join(WORK, "img")
MASTER = os.path.join(REPO, "public", "library", "y01-physical-education", "book.pdf")
OUT = os.path.join(WORK, "book_new.pdf")
TOC_LEAD = "Six units, one after another. Every unit has its own colour."


def restyle_folio(pg, label, num, badge, rule=True, clear=None):
    """Replace an inherited page-number badge with the standard house badge."""
    E.set_theme(E.UNIT_THEMES[0])
    pg.draw_rect(clear or pymupdf.Rect(526, 726, 578, 778), color=None,
                 fill=(1, 1, 1))
    if rule:
        pg.draw_line(pymupdf.Point(E.ML, E.FOOT_Y), pymupdf.Point(E.MR, E.FOOT_Y),
                     color=E.TH["line"], width=0.6)
    pg.draw_circle(E.FOLIO_C, E.FOLIO_R, color=None, fill=badge)
    E.draw_c(pg, E.FOLIO_C[0], E.FOLIO_C[1] + 3.9, str(num), "F", 11, (1, 1, 1))


def main():
    pages, groups = C.build_pages()
    for p in pages:
        if p["kind"] == "toc":
            p["spec"] = dict(hl="Prime School Press",
                             hr="Physical Education · Year 1",
                             kick="PHYSICAL EDUCATION · YEAR 1",
                             title="What is inside?",
                             blocks=[E.B.toc(groups, lead=TOC_LEAD)])

    doc = pymupdf.open()
    over, sparse, outofbox = [], [], []
    for p in pages:
        spec = p["spec"]
        if p["kind"] == "opener":
            _pg, bottom = E.render_opener(doc, spec, p["num"])
            lim = (20.0, 580.0)
        else:
            _pg, bottom, bad = E.render_page(doc, spec, p["folio"], p["num"],
                                             unit=p["unit"])
            lim = (E.ML - 1.5, E.MR + 1.5)
            text_len = len(_pg.get_text().strip())
            if bad:
                over.append((p["num"], round(bottom, 1)))
            if text_len < 140 and not any(n == "plate" for n, _ in spec["blocks"]):
                sparse.append((p["num"], text_len))
        for b in _pg.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            if x1 > lim[1] or x0 < lim[0] or y1 > 776:
                outofbox.append((p["num"], round(x0, 1), round(x1, 1), round(y1, 1)))
    print("interior pages built:", doc.page_count)

    old = pymupdf.open(MASTER)
    assert old.page_count == 72, old.page_count
    out = pymupdf.open()
    out.insert_pdf(old, from_page=0, to_page=2)      # cover, imprint, Welcome
    out.insert_pdf(doc)                              # rebuilt interior
    out.insert_pdf(old, from_page=71, to_page=71)    # back cover

    # pages 2 and 3 inherit an older number badge; put the house badge on them
    E.set_theme(E.UNIT_THEMES[0])
    for i in (1, 2):
        restyle_folio(out[i], None, i + 1, E.TH["mid"], rule=False)

    out.set_metadata(old.metadata)
    out.save(OUT, deflate=True, garbage=3, clean=True)

    total = out.page_count
    print("total pages:", total)
    print("overflowing pages:", over)
    print("sparse pages:", sparse)
    print("out-of-margin text:", outofbox)
    chk = pymupdf.open(OUT)
    for i in (0, 1, 2, 3, 4):
        print(" p%-3d %s" % (i + 1, chk[i].get_text().strip().replace("\n", " | ")[:88]))
    print(" last  %s" % chk[total - 1].get_text().strip().replace("\n", " | ")[:88])
    if over or sparse:
        print("!! review before committing")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
