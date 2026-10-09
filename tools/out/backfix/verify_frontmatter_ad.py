#!/usr/bin/env python3
"""Read-only checks on a rebuilt Y7-9 Art & Design front matter.

  * even page count, no blank page anywhere;
  * page 2 house imprint page, page 3 welcome page, page 4 Contents;
  * every printed folio matches its physical page;
  * every Contents entry still names the same section and reads exactly the
    number the insert added (one page, or two where the book numbered its folios
    one behind its physical pages);
  * old page p is new page p+1, text for text (page numbers excepted).

Usage: .venv/bin/python tools/out/backfix/verify_frontmatter_ad.py <slug> [<original.pdf>]
"""
import os
import re
import sys

import pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
NUM = re.compile(r"^\d+$")
COMB = re.compile(r"^Page\s+(\d+)$")
FURN = re.compile(r"^(Year \d+ Art & Design|Prime Books|Page|P\s?R\s?I\s?M\s?E)")


def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for line in b["lines"]:
            for sp in line["spans"]:
                if sp["text"].strip():
                    out.append(sp)
    return out


def rows(page):
    return [(s["bbox"][1], s["bbox"][0], s["text"].strip(), s["size"])
            for s in spans(page)]


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def clean_label(t):
    t = re.sub(r"([ .]\.[ .])+\s*$", "", norm(t))
    return re.sub(r"[\s.]+$", "", t)


def strip_furniture(txt):
    lines = [l for l in txt.splitlines()
             if not FURN.match(l.strip()) and not NUM.match(l.strip())]
    return norm(" ".join(lines))


def folio_of(page):
    h = page.rect.height
    for sp in spans(page):
        t = sp["text"].strip()
        m = COMB.match(t)
        if m and sp["bbox"][1] > h - 90:
            return int(m.group(1))
        if NUM.match(t) and sp["size"] >= 10.5 and sp["bbox"][1] > h - 90 \
                and sp["bbox"][0] > 480:
            return int(t)
    return None


def folio_offset(doc):
    """1 when the book printed folio = physical - 1, else 0."""
    for i in range(3, doc.page_count - 3):
        f = folio_of(doc[i])
        if f is not None:
            return 1 if f == i else 0
    return 0


def toc_pairs(page):
    rs = rows(page)
    labels = [r for r in rs if r[1] < 480 and len(r[2]) > 3 and not FURN.match(r[2])]
    nums = [r for r in rs if r[1] > 480 and NUM.match(r[2])]
    out = []
    for y, x, t, sz in labels:
        cand = [n for n in nums if abs(n[0] - y) < 3.0 and abs(n[3] - sz) < 1.2]
        if len(cand) == 1:
            out.append((t, int(cand[0][2])))
    return out


def check(slug, original=None):
    path = os.path.join(ROOT, "public", "library", slug, "book.pdf")
    d = pymupdf.open(path)
    n = d.page_count
    bad = []
    print("== %s: %d pages (even: %s)" % (slug, n, n % 2 == 0))
    if n % 2:
        bad.append("odd page count")

    blanks = [i + 1 for i, p in enumerate(d)
              if not p.get_text().strip() and not p.get_images() and not p.get_drawings()]
    print("   blank pages:", blanks or "none")
    if blanks:
        bad.append("blank pages %s" % blanks)

    flat = re.sub(r"\s+", "", d[1].get_text()).upper()
    ok2 = "PRIMESCHOOLPRESS" in flat and "IMPRINT" in flat
    ok3 = "welcome" in norm(d[2].get_text())
    ok4 = "Contents" in d[3].get_text()
    print("   p2 imprint: %s | p3 welcome: %s | p4 contents: %s" % (ok2, ok3, ok4))
    if not ok2:
        bad.append("page 2 is not the standard imprint page")
    if not ok3:
        bad.append("page 3 is not the welcome page")
    if not ok4:
        bad.append("page 4 is not the Contents page")
    if "Independent publication for Prime School" in d[2].get_text():
        bad.append("page 3 still carries the old imprint section")

    wrong, seen = [], 0
    for i, p in enumerate(d):
        f = folio_of(p)
        if f is not None:
            seen += 1
            if f != i + 1:
                wrong.append((i + 1, f))
    print("   folios found: %d, wrong: %s" % (seen, wrong[:12] or "none"))
    if wrong:
        bad.append("%d wrong folios" % len(wrong))

    entries = toc_pairs(d[3])
    bump = 1
    mism = []
    if original and os.path.exists(original):
        o = pymupdf.open(original)
        bump += folio_offset(o)
        old_pairs = toc_pairs(o[2])
        if len(old_pairs) != len(entries):
            bad.append("contents has %d entries, before %d"
                       % (len(entries), len(old_pairs)))
        for (lt, ln), (ot, on) in zip(entries, old_pairs):
            if clean_label(lt) != clean_label(ot) or ln != on + bump:
                mism.append((clean_label(lt)[:42], on, ln))
    print("   contents entries: %d, unchanged except +%d: %s"
          % (len(entries), bump, mism[:6] or "none"))
    if mism:
        bad.append("%d contents entries wrong" % len(mism))

    # a section really does start on the page the list claims
    probes = [(l, v) for l, v in entries
              if len(re.sub(r"^(chapter|unit)\s*[\d.]+\s*", "", clean_label(l))) > 12]
    off = []
    for label, num in probes:
        key = re.sub(r"^(chapter|unit)\s*[\d.]+\s*", "", clean_label(label))[:34]
        hit = None
        for i in range(4, n - 1):
            if key in norm(d[i].get_text()):
                hit = i + 1
                break
        if hit and hit != num:
            off.append((label[:40], num, hit))
    print("   section spot checks: %d, off: %s" % (len(probes), off[:6] or "none"))

    if original and os.path.exists(original):
        o = pymupdf.open(original)
        lost = [i for i in range(4, n - 1)
                if strip_furniture(o[i - 1].get_text()) != strip_furniture(d[i].get_text())]
        print("   body pages whose text moved/changed: %s" % (lost[:8] or "none"))
        if lost:
            bad.append("%d body pages differ" % len(lost))
        old2 = strip_furniture(o[1].get_text())
        new3 = strip_furniture(d[2].get_text())
        keep = old2.split("welcome", 1)[1] if "welcome" in old2 else old2
        if keep and keep[:60] not in new3:
            bad.append("welcome copy not carried over to page 3")

    print("   VERDICT:", "clean" if not bad else bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
