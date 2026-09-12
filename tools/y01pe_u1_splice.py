#!/usr/bin/env python3
"""Splice the rebuilt Unit 1 pages into the Year 1 Physical Education master."""
import os, shutil, sys
import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(REPO, "public", "library", "y01-physical-education", "book.pdf")
NEW = os.path.join(REPO, "work", "y01pe_u1", "unit1.pdf")
OUT = "/tmp/y01pe_master_new.pdf"

old = pymupdf.open(MASTER)
new = pymupdf.open(NEW)
assert old.page_count == 68, old.page_count
assert new.page_count == 10, new.page_count

# sanity: the pages we are replacing really are Unit 1
assert "U N I T 1" in old[12].get_text(), old[12].get_text()[:80]
assert "UNIT 1  MOVING WELL" in old[21].get_text() or "MOVING WELL" in old[21].get_text()

out = pymupdf.open()
out.insert_pdf(old, from_page=0, to_page=11)     # pages 1-12  (front matter)
out.insert_pdf(new)                              # pages 13-22 (new Unit 1)
out.insert_pdf(old, from_page=22)                # pages 23-68 (rest of the book)
assert out.page_count == 68, out.page_count

# verify the seam: last front-matter page, first page after Unit 1
assert "GETTING SET UP" in out[11].get_text().upper() or "SAFETY FIRST" in out[11].get_text()
assert "WATCHING" in out[22].get_text().upper().replace(" ", ""), out[22].get_text()[:120]
for i in range(12, 22):
    assert len(out[i].get_text().strip()) > 200, (i + 1, len(out[i].get_text()))
    assert out[i].get_images(), i + 1

out.set_metadata(old.metadata)
out.save(OUT, deflate=True, garbage=3, clean=True)
chk = pymupdf.open(OUT)
print("pages:", chk.page_count, "size MB:", round(os.path.getsize(OUT) / 1e6, 2))
print("p13 :", chk[12].get_text().strip().replace("\n", " | ")[:90])
print("p22 :", chk[21].get_text().strip().replace("\n", " | ")[:90])
print("p23 :", chk[22].get_text().strip().replace("\n", " | ")[:90])
if "--commit" in sys.argv:
    shutil.copy(OUT, MASTER)
    print("master replaced:", MASTER)
