#!/usr/bin/env python3
"""Publish the rebuilt Year 1 Physical Education book into the master."""
import os, shutil, sys
import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(REPO, "public", "library", "y01-physical-education", "book.pdf")
NEW = os.path.join(REPO, "work", "y01pe", "book_new.pdf")
OUT = "/tmp/y01pe_publish.pdf"

new = pymupdf.open(NEW)
old = pymupdf.open(MASTER)
assert new.page_count == 71 + 1, new.page_count
assert old.page_count == 68, old.page_count

# cover untouched, imprint untouched, back cover untouched
assert "Physical Education" in new[0].get_text()
assert "I M P R I N T" in new[1].get_text().upper() or "IMPRINT" in new[1].get_text().upper()
assert "P R I M E  S C H O O L  P R E S S" in new[new.page_count - 1].get_text()

for i in range(2, new.page_count - 1):
    t = new[i].get_text().strip()
    assert len(t) > 60, (i + 1, len(t))

# folio check: every interior page carries its own number
import re
bad = []
for i in range(2, new.page_count - 1):
    nums = re.findall(r"^\s*(\d{1,3})\s*$", new[i].get_text(), re.M)
    if str(i + 1) not in nums:
        bad.append(i + 1)
assert not bad, bad

out = pymupdf.open()
out.insert_pdf(new)
out.set_metadata(old.metadata)
out.save(OUT, deflate=True, garbage=3, clean=True)

chk = pymupdf.open(OUT)
print("pages:", chk.page_count, "size MB:", round(os.path.getsize(OUT) / 1e6, 2))
print("p1 :", chk[0].get_text().strip().replace("\n", " | ")[:70])
print("p2 :", chk[1].get_text().strip().replace("\n", " | ")[:70])
print("p71:", chk[70].get_text().strip().replace("\n", " | ")[:70])
print("p72:", chk[71].get_text().strip().replace("\n", " | ")[:70])
if "--commit" in sys.argv:
    shutil.copy(OUT, MASTER)
    print("master replaced:", MASTER)
