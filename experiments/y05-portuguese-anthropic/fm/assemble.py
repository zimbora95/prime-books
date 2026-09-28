#!/usr/bin/env python3
"""Assemble «Português · Year 5 — Manual do aluno» into fm/build/book.pdf.

    /root/.hermes/cache/scratch/exp-venv/bin/python assemble.py [--allow-missing]

front.pdf (i–viii) + ./build/unit.pdf (1–24) + u2..u7/build/unit.pdf (25–144) + back.pdf (145–151 + back cover)

Checks: every part exists and has its planned page count; the printed folio of every page matches the plan
(read from the text layer, bottom 22 mm); total = 160; fonts subset (pymupdf subset_fonts) and then no Type3 or
base-14 (non-embedded) font anywhere. Writes build/assembly-report.md and build/assembly-report.json.
Never publishes: no writes outside fm/build/.
"""
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
sys.path.insert(0, HERE)
from plan import FRONT, TOTAL, UNITS  # noqa: E402

BASE14 = {"Courier", "Helvetica", "Times-Roman", "Times", "Symbol", "ZapfDingbats", "Arial"}
ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]


def parts():
    out = [dict(name="Abertura (front matter)", path=os.path.join(BUILD, "front.pdf"), pages=8,
                folios=ROMAN, unnumbered={"i", "ii"})]
    for u in UNITS:
        out.append(dict(name=f"Unidade {u['n']}", path=os.path.join(ROOT, u["folder"], "build", "unit.pdf"),
                        pages=u["pages"], folios=[str(n) for n in range(u["first"], u["last"] + 1)],
                        unnumbered={str(u["first"])}))  # unit openers are full-bleed art pages without a folio
    out.append(dict(name="Fim do livro (back matter)", path=os.path.join(BUILD, "back.pdf"), pages=8,
                    folios=[str(n) for n in range(145, 152)] + ["contracapa"], unnumbered={"contracapa"}))
    return out


def printed_folio(pg, expect):
    """True if `expect` is printed as a stand-alone word in the bottom 22 mm of the page"""
    H = pg.rect.height
    zone = pymupdf.Rect(0, H - 22 * 72 / 25.4, pg.rect.width, H)
    words = [w[4].strip() for w in pg.get_text("words", clip=zone)]
    return expect in words, words[-4:]


def main():
    allow_missing = "--allow-missing" in sys.argv
    rep = dict(parts=[], problems=[], missing=[])
    book = pymupdf.open()
    for part in parts():
        info = dict(name=part["name"], path=part["path"], planned=part["pages"])
        if not os.path.exists(part["path"]):
            info["status"] = "MISSING"
            rep["missing"].append(part["name"])
            rep["parts"].append(info)
            if not allow_missing:
                sys.exit(f"missing {part['path']} (use --allow-missing to assemble what exists)")
            continue
        d = pymupdf.open(part["path"])
        info["pages"] = d.page_count
        info["mtime"] = os.path.getmtime(part["path"])
        if d.page_count != part["pages"]:
            rep["problems"].append(f"{part['name']}: {d.page_count} pages, plan says {part['pages']}")
        bad = []
        for k, pg in enumerate(d):
            if k >= len(part["folios"]):
                break
            f = part["folios"][k]
            if f in part["unnumbered"]:
                continue
            ok, seen = printed_folio(pg, f)
            if not ok:
                bad.append(f"pdf p.{k+1}: expected folio {f}, bottom words {seen}")
        info["folio_errors"] = bad
        rep["problems"] += [f"{part['name']}: {b}" for b in bad]
        blank = [k + 1 for k, pg in enumerate(d) if not pg.get_text().strip() and not pg.get_images() and not pg.get_drawings()]
        if blank:
            rep["problems"].append(f"{part['name']}: blank pages {blank}")
        info["status"] = "ok" if not bad and d.page_count == part["pages"] else "CHECK"
        book.insert_pdf(d)
        rep["parts"].append(info)
    rep["total"] = book.page_count
    if book.page_count != TOTAL:
        rep["problems"].append(f"total {book.page_count} pages, plan says {TOTAL}")
    if book.page_count % 2:
        rep["problems"].append("odd page count")
    # page labels: roman for front matter, arabic from Unidade 1
    try:
        book.set_page_labels([{"startpage": 0, "prefix": "", "style": "r", "firstpagenum": 1},
                              {"startpage": 8, "prefix": "", "style": "D", "firstpagenum": 1}])
    except Exception as e:  # noqa: BLE001
        rep["problems"].append(f"page labels not set: {e}")
    # outline (bookmarks)
    toc = [[1, "Capa", 1], [1, "Ficha técnica", 2], [1, "Como usar este livro", 3], [1, "Mapa do ano", 4], [1, "Índice", 5],
           [1, "O meu ano de leitura", 7], [1, "Quem sou eu como leitor", 8]]
    model = json.load(open(os.path.join(BUILD, "model.json"))) if os.path.exists(os.path.join(BUILD, "model.json")) else {}
    for u in model.get("units", UNITS):
        if u["first"] + 8 <= book.page_count:
            toc.append([1, f"Unidade {u['n']} · {u['title']}", u["first"] + 8])
    for p, t in [(145, "Glossário"), (147, "Recursos digitais"), (148, "Referências e créditos"), (149, "Planificação anual"),
                 (150, "O meu 5.º ano — antes de fechar o livro"), (151, "Colofão"), (152, "Contracapa")]:
        if p + 8 <= book.page_count:
            toc.append([1, t, p + 8])
    book.set_toc(toc)
    book.set_metadata({"title": "Português · Year 5 — Manual do aluno", "author": "Prime School Press",
                       "subject": "Português Língua Materna, 5.º ano", "creator": "Prime School Press",
                       "producer": "Prime School Press (Chromium + PyMuPDF)"})
    # fonts: subset, then verify nothing is Type3 or a non-embedded base-14 font
    try:
        book.subset_fonts()
        rep["subset"] = "ok"
    except Exception as e:  # noqa: BLE001
        rep["subset"] = f"failed: {e}"
    out = os.path.join(BUILD, "book.pdf")
    book.save(out, garbage=3, deflate=True)
    d = pymupdf.open(out)
    type3_pages, base14, fonts = [], set(), set()
    for i, pg in enumerate(d):
        for f in pg.get_fonts(full=True):
            ext, typ, name = f[1], f[2], f[3]
            fonts.add((typ, re.sub(r"^[A-Z]{6}\+", "", name)))
            if typ == "Type3":
                type3_pages.append(i + 1)
            if re.sub(r"^[A-Z]{6}\+", "", name).split(",")[0].split("-")[0] in BASE14 and ext in ("", "n/a"):
                base14.add(name)
    t3 = sorted(set(type3_pages))
    rep["fonts"] = sorted(fonts)
    rep["type3_pages"] = t3
    rep["base14"] = sorted(base14)
    if t3:
        rep["problems"].append(f"Type3 fonts on {len(t3)} pages (book pp. {compress(t3)})")
    if base14:
        rep["problems"].append(f"non-embedded base-14 fonts: {sorted(base14)}")
    rep["size_mb"] = round(os.path.getsize(out) / 1e6, 2)
    rep["out"] = out
    json.dump(rep, open(os.path.join(BUILD, "assembly-report.json"), "w"), ensure_ascii=False, indent=1)
    write_md(rep)
    print(f"book.pdf: {rep['total']} pages, {rep['size_mb']} MB -> {out}")
    for p in rep["problems"]:
        print("  PROBLEM:", p)
    if not rep["problems"]:
        print("  all checks passed")


def compress(nums):
    """[1,2,3,7,8] -> '1–3, 7–8' (book page numbers, 1-based physical)"""
    out, s = [], None
    for i, n in enumerate(nums):
        if s is None:
            s = n
        if i == len(nums) - 1 or nums[i + 1] != n + 1:
            out.append(f"{s}–{n}" if s != n else f"{s}")
            s = None
    return ", ".join(out)


def write_md(rep):
    L = ["# Assembly report — Português · Year 5 — Manual do aluno", "",
         f"Output: `{rep['out']}` — **{rep['total']} pages** (plan {TOTAL}), {rep['size_mb']} MB", "",
         "| Part | Planned | Found | Status | Folio errors |", "|---|---|---|---|---|"]
    for p in rep["parts"]:
        L.append(f"| {p['name']} | {p['planned']} | {p.get('pages', '—')} | {p['status']} | {len(p.get('folio_errors', []))} |")
    L += ["", f"Font subsetting: {rep['subset']}", "", "Fonts in the book: " + ", ".join(f"{t} {n}" for t, n in rep["fonts"]), ""]
    L += ["## Problems", ""] + ([f"- {p}" for p in rep["problems"]] or ["- none"])
    if rep["missing"]:
        L += ["", "## Missing parts", ""] + [f"- {m}" for m in rep["missing"]]
    open(os.path.join(BUILD, "assembly-report.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
