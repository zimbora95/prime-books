#!/usr/bin/env python3
"""Inventory the master: what is on every one of its 98 pages.

The standardised edition is a NEW book built to the standard, but nothing the
teacher placed may be lost, so the new build starts from a complete inventory of
the master - page type, unit, headings, body text, activity boxes and the art
each page carries. That inventory is what the new pages are composed from.

    .venv/bin/python book_plan.py            # writes book-plan.json + a summary
"""
import json
import os
import re

import pymupdf

REPO = "/root/prime-books"
MASTER = os.path.join(REPO, "public/library/y01-physical-education/book.pdf")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "book-plan.json")


def blocks(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") == 0:
            txt = "\n".join("".join(s["text"] for s in ln["spans"])
                            for ln in b.get("lines", [])).strip()
            if not txt:
                continue
            sizes = [round(s["size"], 1) for ln in b.get("lines", [])
                     for s in ln["spans"] if s["text"].strip()]
            fonts = sorted({"".join(ch for ch in s["font"] if ch.isalpha())
                            for ln in b.get("lines", []) for s in ln["spans"]})
            out.append({"kind": "text", "text": txt,
                        "bbox": [round(v, 1) for v in b["bbox"]],
                        "size": max(sizes) if sizes else None,
                        "fonts": fonts})
        else:
            out.append({"kind": "image", "bbox": [round(v, 1) for v in b["bbox"]],
                        "size": [b.get("width"), b.get("height")]})
    return sorted(out, key=lambda b: (round(b["bbox"][1]), round(b["bbox"][0])))


def classify(txt_all, n):
    t = txt_all.lower()
    if n == 1:
        return "cover"
    if n == 2:
        return "imprint"
    if "what is inside" in t or "contents" == txt_all.strip().lower()[:8]:
        return "contents"
    if n == 4 or "welcome to the meadow" in t and n <= 8:
        return "welcome"
    m = re.search(r"unit\s+([1-6])\b", t)
    if m and re.search(r"\bwhat you will (learn|do)\b", t):
        return "unit-opener"
    if re.search(r"how did it go", t):
        return "check"
    if "look back" in t:
        return "review"
    if "words we used" in t:
        return "glossary"
    if "answers for every unit" in t:
        return "answers"
    if "where the facts came from" in t or "our sources" in t:
        return "sources"
    if "watch and learn" in t:
        return "teacher"
    if n == 98:
        return "back-cover"
    return "topic"


def main():
    doc = pymupdf.open(MASTER)
    pages = []
    for i, page in enumerate(doc):
        n = i + 1
        bs = blocks(page)
        txt_all = "\n".join(b["text"] for b in bs if b["kind"] == "text")
        imgs = [b for b in bs if b["kind"] == "image"]
        imgs += [{"kind": "image", "bbox": None, "size": None}
                 for _ in range(len(page.get_images(full=True)) - len(imgs))]
        pages.append({
            "page": n,
            "type": classify(txt_all, n),
            "headings": [b["text"][:90] for b in bs
                         if b["kind"] == "text" and b["size"] and b["size"] >= 15],
            "blocks": [b for b in bs if b["kind"] == "text"],
            "images": len(page.get_images(full=True)),
            "drawings": len(page.get_drawings()),
            "chars": len(page.get_text().strip()),
        })
    kinds = {}
    for p in pages:
        kinds[p["type"]] = kinds.get(p["type"], 0) + 1
    json.dump({"master": MASTER, "pages": pages}, open(OUT, "w"), indent=1)
    print("page types:", json.dumps(kinds, indent=1))
    for p in pages:
        print(f"  p{p['page']:>3} {p['type']:<12} imgs {p['images']} "
              f"chars {p['chars']:>4}  {p['headings'][:1]}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()