#!/usr/bin/env python3
"""Publish the Standard A 2.0 rebuild of Year 1 Physical Education.

Checks the finished file, then (only with --commit) replaces the master PDF,
refreshes the manifest entry and leaves the cover alone: page 1 is spliced
byte-for-byte from the old master, so cover.webp still describes it.

  ./.venv/bin/python tools/y01pe_a2_publish.py            # dry run
  ./.venv/bin/python tools/y01pe_a2_publish.py --commit   # publish
"""
import json
import os
import re
import shutil
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SLUG = "y01-physical-education"
MASTER = os.path.join(REPO, "public", "library", SLUG, "book.pdf")
NEW = os.path.join(REPO, "work", "y01pe_a2", "book_new.pdf")
MANIFEST = os.path.join(REPO, "public", "library.json")
BACKUP = os.path.join(REPO, "work", "y01pe_a2", "book_master_before.pdf")


def main(commit):
    new = pymupdf.open(NEW)
    total = new.page_count
    print("new file      :", NEW, total, "pages")

    # ---- guards -----------------------------------------------------------
    assert "Physical Education" in new[0].get_text(), "page 1 is not the cover"
    assert "IMPRINT" in new[1].get_text().replace(" ", "").upper(), "page 2 imprint"
    assert "PRIMESCHOOLPRESS" in new[total - 1].get_text().replace(" ", "").upper(), \
        "last page is not the back cover"
    for i in range(2, total - 1):
        t = new[i].get_text().strip()
        assert len(t) > 60, ("thin interior page", i + 1, len(t))
        nums = re.findall(r"^\s*(\d{1,3})\s*$", new[i].get_text(), re.M)
        assert str(i + 1) in nums, ("missing folio", i + 1)
    print("guards        : cover, imprint, back cover, folios all present")

    size_mb = round(os.path.getsize(NEW) / 1e6, 2)
    print("size          :", size_mb, "MB")

    if not os.path.exists(BACKUP):
        shutil.copy(MASTER, BACKUP)
        print("backup        :", BACKUP)

    if not commit:
        print("dry run - nothing written. Re-run with --commit to publish.")
        return 0

    shutil.copy(NEW, MASTER)
    print("master        : replaced", MASTER)

    rows = json.load(open(MANIFEST))
    for r in rows:
        if r.get("slug") == SLUG:
            r["pages"] = total
            r["mb"] = size_mb
            print("manifest      : pages=%d mb=%s" % (total, size_mb))
            break
    json.dump(rows, open(MANIFEST, "w"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main("--commit" in sys.argv))
