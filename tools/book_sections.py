"""Mirror of buildSections() in index.html (pymupdf) — sections from the BOOK's own PDF.

Dry-run before generating any input file: run over every book in public/library.json
and print GOOD/WEAK/NONE tallies plus a sample, and check y01-art-and-design against
the endorsed input spreadsheet.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pymupdf

pymupdf.TOOLS.mupdf_display_errors(False)

REPO = Path("/root/prime-books")
LIB = REPO / "public" / "library"

SQUEEZE = re.compile(r"([A-Za-z]) (?=[A-Za-z](?:\s|$))")
HEAD = re.compile(
    r"^(unit|unidade|unidad|stop|topic|theme|term|termo|modulo|module|part|section)\s*(\d+(?:\.\d+)?)"
    r"\s*(?:(?:\s*[·:\u2013\u2014-]\s*|\s+)(\S.*))?$"
    r"|^(unit|unidade|unidad|stop|topic|theme|term|termo|modulo|module|part|section)\s*(\d+(?:\.\d+)?)$",
    re.I,
)
SUB = re.compile(r"^(\d+\.\d+)\s+(.+)$")
SUB2 = re.compile(r"^\d{1,2}\.\s+(\d+\.\d+)\s+(.+)$")
BARE = re.compile(r"^(\d{1,3})$")
TOCWORD = re.compile(r"contents|table of contents|what is inside|what is in this book|\u00edndice|indice", re.I)
TOCUNIT = re.compile(r"\b(unit|unidade|unidad|stop|topic|theme|term|modulo|module|part|section)\s*\d", re.I)
BARENUM = re.compile(r"^\d+\s*\n\S", re.M)


def squeeze(t: str) -> str:
    return SQUEEZE.sub(r"\1", t)


def page_lines(page) -> list[str]:
    return [l.strip() for l in page.get_text().splitlines() if l.strip()]


def folio_of(lines: list[str]):
    for ln in reversed(lines[-3:]):
        toks = ln.split()
        if toks and re.fullmatch(r"\d{1,3}", toks[-1]):
            return int(toks[-1])
    return None


def sections(path: Path):
    doc = pymupdf.open(path)
    try:
        texts, folios = [], []
        for i in range(doc.page_count):
            lines = page_lines(doc[i])
            texts.append("\n".join(lines))
            folios.append(folio_of(lines))

        toc_text, toc_idx = None, -1
        for i in range(min(14, doc.page_count)):
            sq = squeeze(texts[i])
            if TOCWORD.search(sq) and (TOCUNIT.search(sq) or BARENUM.search(sq)):
                toc_text, toc_idx = texts[i], i
                break

        idx_of_folio = {}
        for i, f in enumerate(folios):
            if f is not None and f not in idx_of_folio:
                idx_of_folio[f] = i

        def to_idx(folio):
            if folio in idx_of_folio:
                return idx_of_folio[folio]
            for f in range(folio - 1, -1, -1):
                if f in idx_of_folio:
                    return idx_of_folio[f]
            return 0

        if toc_text is None:                                   # unit-opener fallback
            secs = []
            for i in range(1, doc.page_count):
                if len(secs) >= 40:
                    break
                first = [squeeze(l) for l in page_lines(doc[i])[:6]]
                m = HEAD.match(first[0]) if first else None
                if m:
                    word, num, title = (m.group(1) or m.group(4)), (m.group(2) or m.group(5)), m.group(3)
                    kind = word.capitalize()
                    secs.append({"label": f"{kind} {num} · {title}" if title else f"{kind} {num}",
                                 "unit": True, "page": i + 1, "folio": folios[i]})
                    continue
                m2 = SUB.match(first[0]) if first else None
                if m2 and secs and secs[-1]["label"].startswith("Unit"):
                    secs.append({"label": f"{m2.group(1)} {m2.group(2)}", "unit": False,
                                 "page": i + 1, "folio": folios[i]})
            return secs

        lines = [squeeze(l.strip()) for l in toc_text.splitlines() if l.strip()]
        secs, pending = [], None
        # A bare "16" line is a PAGE number when the page also carries real
        # "Unit N" headings; only the bare-number contents style (Y2/Y3 Maths:
        # "1 / Numbers to 100") uses it as the unit number. The JS mirror in
        # index.html does not carry this guard, so do not treat the two as
        # byte-identical any more.
        numeric_style = not any(HEAD.match(l) for l in lines)

        def flush():
            nonlocal pending
            if pending and pending["labelParts"]:
                secs.append({"label": " · ".join(pending["labelParts"]), "unit": pending["unit"],
                             "page": pending["page"], "folio": None})
            pending = None

        for raw in lines:
            if re.match(r"^contents|table of contents|what is inside|what is in this book", raw, re.I):
                continue
            n = BARE.match(raw)
            if n:
                if pending:
                    pending["page"] = to_idx(int(n.group(1)))
                    pending["folio"] = int(n.group(1))
                    flush()
                elif numeric_style and int(n.group(1)) <= 40:
                    pending = {"labelParts": [n.group(1)], "unit": True, "page": 0, "numeric": True}
                continue
            m = HEAD.match(raw)
            if m:
                flush()
                word = (m.group(1) or m.group(4)).capitalize()
                num = m.group(2) or m.group(5)
                title = m.group(3)
                pending = {"labelParts": [f"{word} {num}"], "unit": True, "page": 0}
                if title and len(title) <= 80:
                    pending["labelParts"].append(title)
                continue
            m = SUB2.match(raw)
            if m:
                flush()
                pending = {"labelParts": [f"{m.group(1)} {m.group(2)}"], "unit": False, "page": 0}
                continue
            m = SUB.match(raw)
            if m:
                flush()
                pending = {"labelParts": [f"{m.group(1)} {m.group(2)}"], "unit": False, "page": 0}
                continue
            if pending and len(pending["labelParts"]) < 2 and 1 < len(raw) < 60 and not re.search(r"[.:]$", raw):
                if pending.get("numeric"):
                    pending["labelParts"][0] = "Unit " + pending["labelParts"][0]
                    pending["numeric"] = False
                pending["labelParts"].append(raw)
                continue
        flush()

        start = toc_idx + 1 if toc_idx >= 0 else 1
        for s in secs:
            if s["page"] > 0:
                continue
            probe = s["label"].split(" · ")[-1].lower()
            if len(probe) < 5:
                continue
            for i in range(start, len(texts)):
                if probe in texts[i].lower():
                    s["page"] = i
                    s["folio"] = folios[i]
                    break
        return [s for s in secs if s["page"] > 0]
    finally:
        doc.close()


def group(secs):
    """-> [(unit_label, [(sub_label, page), ...]), ...] with pages (folio or print index)."""
    out, cur = [], None
    for s in secs:
        pg = s.get("folio") or (s["page"] + 1)
        if s["unit"]:
            cur = [s["label"], []]
            out.append(cur)
        elif cur is not None:
            cur[1].append((s["label"], pg))
    return out


def main():
    lib = json.load(open(REPO / "public" / "library.json"))
    only = sys.argv[1:] or None
    rows, tally = [], {"GOOD": 0, "WEAK": 0, "NONE": 0}
    for r in lib:
        slug = r["slug"]
        if only and slug not in only:
            continue
        p = LIB / slug / "book.pdf"
        if not p.exists():
            tally["NONE"] += 1
            rows.append((slug, "NO PDF", 0, 0))
            continue
        try:
            secs = sections(p)
        except Exception as e:                                       # noqa: BLE001
            rows.append((slug, f"ERROR {e}", 0, 0))
            tally["NONE"] += 1
            continue
        units = group(secs)
        nu = len(units)
        ns = sum(len(u[1]) for u in units)
        verdict = "GOOD" if nu >= 3 else ("WEAK" if nu >= 1 else "NONE")
        tally[verdict] += 1
        rows.append((slug, verdict, nu, ns))
    print(f"{'slug':34} {'verdict':6} {'units':>5} {'subs':>5}")
    for slug, v, nu, ns in rows:
        print(f"{slug:34} {v:6} {nu:5} {ns:5}")
    print(f"\n{tally}   of {len(rows)} books")
    if only:
        slug = only[0]
        p = LIB / slug / "book.pdf"
        if p.exists():
            print(f"\n--- {slug} ---")
            for u, subs in group(sections(p)):
                print(f"Unit {u}")
                for s, pg in subs:
                    print(f"   {s}   [{pg}]")


if __name__ == "__main__":
    main()