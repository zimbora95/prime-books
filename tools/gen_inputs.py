"""Generate the missing per-book input spreadsheets.

Source order (decided 2026-09-14):
  1. the BOOK's own contents page (sections parsed from book.pdf) — the repo
     doctrine: the book is the only source of truth, so an input derived from it
     cannot drift from what the pupil sees; page numbers come with it;
  2. the Edu360 syllabus in Odoo (fallback for books with no contents page, e.g.
     the 4-page shells) — units from sections, subunits from chapters/topics,
     no page numbers.

Writes the site's Contents format: sheet 'Contents', Section type | Title | Page.

    .venv/bin/python /tmp/gen_inputs.py --dry-run
    .venv/bin/python /tmp/gen_inputs.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, "/root/.config/odoo")

REPO = Path("/root/prime-books")
INPUTS = REPO / "public" / "inputs"
LIB = REPO / "public" / "library"

SUBRE = re.compile(r"^(\d+)\.(\d+)\b")
UNUM = re.compile(r"^Unit\s*(\d+)\b", re.I)
MAPPING = Path(__file__).resolve().parent / "syllabus_mapping.json"
# A book must be built from the CURRENT syllabus, not the first name match: the
# matcher scores names, and those ties fall to whichever syllabus came first
# (ENGLISH [Y03] 2021 beat English (Y03) 2026). These are the titles where the
# current-year syllabus is known from the Edu360 list; everything else picks by
# the currency rule in current_first() below.
OVERRIDES = {
    "y01-global-perspectives": 939,   # Global Perspectives KS1 - 2026 (62 topics)
    "y02-science": 943,               # Science (Y02) - 2026 (60 topics)
    "y03-english": 947,               # English (Y03) - 2026 (78 topics)
    "y05-science": 279,               # SCIENCE - Y05 - 2026 (42 topics)
    "y06-science": 280,               # SCIENCE-Y06 - 2026 (39 topics)
}
CURRENT = re.compile(r"(20[2-9]\d|\b\d\d\s*[-/]\s*\d\d\b)")
PREFIX = re.compile(r"^(Y\d{2}|KS\d|K)\s+", re.I)
# "Unit 2 Materials: properties and changes" and "Unit 2: Materials" must both
# keep their whole title — only the "Unit <n>" prefix and the separator that
# follows it may be stripped, never a colon inside the title itself.
UPREFIX = re.compile(r"^Unit\s*\d+\s*[:.\-·]?\s*", re.I)


def unit_title(name: str) -> str:
    return UPREFIX.sub("", (name or "").strip()).strip() or (name or "").strip()


def skey(label):
    m = SUBRE.match(label or "")
    return (int(m.group(1)), int(m.group(2)), label) if m else (9999, 9999, label or "")


def ukey(label):
    m = UNUM.match(label or "")
    return int(m.group(1)) if m else 9999


def book_rows(slug: str):
    """-> rows or None. rows: [(type, title, page)] from the book's contents page."""
    import book_sections as ps

    pdf = LIB / slug / "book.pdf"
    if not pdf.exists():
        return None
    units = ps.group(ps.sections(pdf))
    if not units:
        return None
    rows = []
    for i in sorted(range(len(units)), key=lambda i: ukey(units[i][0])):
        label, subs = units[i]
        rows.append(("Unit", label, ""))
        for title, page in sorted(subs, key=lambda t: skey(t[0])):
            rows.append(("Subunit", title, str(page) if page else ""))
    return rows or None


def odoo_rows(syl_id: int):
    import odoo_web as o

    secs = o.search_read("edu360.section", [("syllabus_id", "=", syl_id)], ["id", "name", "sequence"], order="id")
    chaps = o.search_read("edu360.chapter", [("syllabus_id", "=", syl_id)],
                          ["id", "name", "section_id", "sequence"], order="id")
    tops = o.search_read("edu360.topic", [("syllabus_id", "=", syl_id)],
                         ["id", "name", "chapter_id", "section_id", "sequence"], order="id")
    by_sec = {}
    for c in chaps:
        by_sec.setdefault(c["section_id"][0] if c["section_id"] else 0, []).append(c)
    tops_by_chap = {}
    for t in tops:
        tops_by_chap.setdefault(t["chapter_id"][0] if t["chapter_id"] else 0, []).append(t)

    def key(name):
        m = UNUM.match(name or "")
        return (int(m.group(1)) if m else 9999, name or "")

    rows = []
    extra = []                                          # sections that are not units
    cands = {}                                          # unit number -> competing sections
    for s in sorted(secs, key=lambda s: key(s["name"])):
        sname = (s["name"] or "").strip()
        m = UNUM.match(sname)
        if not m or not sname:
            if sname:
                extra.append(sname)
            continue
        cands.setdefault(int(m.group(1)), []).append(s)

    for n in sorted(cands):
        # a syllabus can carry several sections numbered "Unit 1": the real unit
        # is the one holding the numbered topics, the others (e.g. a
        # "Unit 1 Humanities" strand with one stub topic) ship as Section rows
        # rather than claiming a unit number.
        ranked = sorted(
            cands[n],
            key=lambda s: (-len(by_sec.get(s["id"], [])), 0 if ":" in (s["name"] or "") else 1, s["id"]),
        )
        s, losers = ranked[0], ranked[1:]
        sname = (s["name"] or "").strip()
        if not by_sec.get(s["id"]):
            extra.extend([(x["name"] or "").strip() for x in ranked if (x["name"] or "").strip()])
            continue
        extra.extend([(x["name"] or "").strip() for x in losers if (x["name"] or "").strip()])
        rows.append(("Unit", f"Unit {n} · {unit_title(sname)}", ""))
        for c in sorted(by_sec.get(s["id"], []), key=lambda c: skey(c["name"])):
            cname = (c["name"] or "").strip()
            if SUBRE.match(cname):
                rows.append(("Subunit", cname, ""))
            else:
                tops = sorted(
                    tops_by_chap.get(c["id"], []),
                    key=lambda t: (skey(PREFIX.sub("", (t["name"] or "").strip()))[:2], t.get("sequence") or 0),
                )
                for t in tops:
                    tname = PREFIX.sub("", (t["name"] or "").strip())
                    if tname:
                        rows.append(("Subunit", tname, ""))

    def xkey(name):
        m = re.match(r"^Term\s*(\d)", name, re.I)
        kind = 0 if re.search(r"revision", name, re.I) else 1 if re.search(r"assess", name, re.I) else 2
        return (0, int(m.group(1)), kind, name) if m else (1, 0, 0, name)

    for name in sorted(extra, key=xkey):
        rows.append(("Section", name, ""))
    return rows or None


def clean_title(t: str) -> str:
    """Tidy a heading for the Contents sheet: no doubled unit prefix, no folio
    references, no dangling separators ('Unit 1 · – Values' / 'Unit 1: X' /
    'Unidade 1 · TEXTOS DOS MEDIA (pág. 3)')."""
    t = re.sub(r"\s*\((?:pág|pg|p)\.?\s*\d+\)\s*$", "", t).strip()
    m = re.match(r"^((?:unit|unidade|unidad|module|modulo)\s*\d+)\s*·\s*(.+)$", t, re.I)
    if m:
        head, tail = m.group(1), m.group(2).strip()
        tail = re.sub(r"^(?:unit|unidade|unidad|module|modulo)\s*\d+\s*[:.\-–]\s*", "", tail, flags=re.I)
        tail = tail.lstrip("–-—:·, ").strip()
        return f"{head} · {tail}" if tail else head
    return t


def write(slug: str, rows, dry: bool):
    if dry:
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contents"
    ws.append(["Section type", "Title", "Page"])
    for typ, t, p in rows:
        ws.append([typ, clean_title(t), p])
    wb.save(INPUTS / f"{slug} - input.xlsx")


def validate(rows):
    """Problems that make a generated input unfit to ship (garbage rows, disorder)."""
    probs = []
    units = [(t, p) for typ, t, p in rows if typ == "Unit"]
    if not units:
        return ["no unit rows"]
    titles = [t for t, _ in units]
    if len(set(titles)) != len(titles):
        probs.append("duplicate unit rows")
    nums = [re.match(r"^(\w+)\s*(\d+)", t) for t in titles]
    seen_nums = {}
    for m in nums:
        if m and m.group(1).lower() == "unit":
            seen_nums[m.group(2)] = seen_nums.get(m.group(2), 0) + 1
    dupes = [n for n, c in seen_nums.items() if c > 1]
    if dupes:
        probs.append(f"unit number(s) used twice: {dupes[:6]}")
    # unit numbers must run 1,2,3…: a contents page that prints only page
    # numbers beside each heading parses as units 5,12,22,32 (german B1/B2) or
    # 2,8,14,20 (portuguese) — gaps like that mean the numbers are folios.
    seq = [int(m.group(2)) for m in nums if m and m.group(1).lower() in ("unit", "unidade", "unidad")]
    if seq and seq != list(range(1, len(seq) + 1)):
        probs.append(f"unit numbers are not 1..{len(seq)}: {seq[:8]}")
    # and their names must not be the book's generic end-matter headings
    GENERIC = {"assessment", "assessments", "revision", "test", "tests", "exercise",
               "exercícios de revisão", "índice", "indice", "inhalt", "index", "contents"}
    generic = sum(1 for t in titles
                  if (t.split("·", 1)[1].strip().lower() if "·" in t else t.strip().lower()) in GENERIC)
    if generic and generic >= max(1, len(titles) // 2):
        probs.append("unit rows are end-matter headings, not units")
    UNITWORD = re.compile(r"^(unit|unidade|unidad|module|modulo|theme|topic|part|stop|section|chapter|term|termo)\b", re.I)
    for t in titles:
        if not UNITWORD.match(t):
            probs.append(f"unit row without a unit word: {t[:34]!r}")
        tail = t.split("·", 1)[1].strip() if "·" in t else ""
        if not tail:
            probs.append(f"unit row with no name: {t[:34]!r}")
        if re.match(r"^TOPIC\s*\d", tail, re.I) or re.match(r"^\d+\.\d+\.\d+", tail):
            probs.append(f"unit row built from a subunit/page number: {t[:40]!r}")
    # subunits under their own unit, in order
    cur, groups = None, {}
    for typ, t, _ in rows:
        if typ == "Unit":
            cur = t
            groups.setdefault(cur, [])
        elif typ == "Subunit":
            if cur is None:
                probs.append(f"subunit before any unit: {t[:30]!r}")
            else:
                groups[cur].append(t)
    for u, ss in groups.items():
        if any(not s.strip() for s in ss):
            probs.append(f"empty subunit under {u[:26]!r}")
        keys = [skey(s)[:2] for s in ss]
        if keys != sorted(keys):
            probs.append(f"subunits out of order under {u[:26]!r}")
    return probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="write even when validation complains")
    ap.add_argument("--overwrite", action="store_true", help="re-generate books that already have an input")
    ap.add_argument("slugs", nargs="*")
    args = ap.parse_args()

    lib = json.load(open(REPO / "public" / "library.json"))
    have = {p.name.split(" - input.")[0] for p in INPUTS.glob("* - input.*")} if not args.overwrite else set()
    mapping = json.load(open(MAPPING)) if MAPPING.exists() else {}

    plan, skipped = [], []
    for r in lib:
        slug = r["slug"]
        if slug in have or (args.slugs and slug not in args.slugs):
            continue
        cands = (mapping.get(slug) or {}).get("cands") or []
        sid = OVERRIDES.get(slug)
        if not sid:
            # currency first: a syllabus naming the current school year wins over
            # any name-score tie (see OVERRIDES above)
            usable = [c for c in cands if c.get("score", 0) >= 1.0]
            current = [c for c in usable if CURRENT.search(c["name"] or "")]
            sid = (current or usable)[0]["id"] if (current or usable) else None
        attempts = [("book", lambda s=slug: book_rows(s)),
                    ("odoo", (lambda s=sid: odoo_rows(s)) if sid else None)]
        chosen, why = None, []
        for name, fn in attempts:
            if fn is None:
                continue
            try:
                rows = fn()
            except Exception as e:                                    # noqa: BLE001
                why.append(f"{name}: {e}")
                continue
            if not rows:
                why.append(f"{name}: nothing parsed")
                continue
            probs = validate(rows)
            if probs and not args.force:
                why.append(f"{name}: " + "; ".join(probs[:3]))
                continue
            chosen = (slug, f"{name}{':%d' % sid if name == 'odoo' else ''}", rows)
            break
        if chosen:
            plan.append(chosen)
        else:
            skipped.append((slug, " | ".join(why) or "no source"))

    for slug, src, rows in plan:
        u = sum(1 for r in rows if r[0] == "Unit")
        s = sum(1 for r in rows if r[0] == "Subunit")
        print(f"{slug:34} {src:12} units={u:3} subunits={s:3}")
        write(slug, rows, args.dry_run)
    print(f"\ngenerated: {len(plan)}   skipped: {len(skipped)}")
    for slug, why in skipped:
        print(f"   SKIP {slug:32} {why}")
    print("(dry run — nothing written)" if args.dry_run else "written")


if __name__ == "__main__":
    main()