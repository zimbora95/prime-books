"""Assemble the whole volume: front matter + units 0-7 + back matter.

Each unit is rebuilt with OFF = (its first page in the book) - 1, so folios and
the internal "p. N" cross-references are the book's own numbers. The front
matter module (fm.py) computes the same starts from the same modules, so the
contents, glossary and sources pages agree with the folios by construction.

    ../.venv/bin/python assemble.py            # build everything, write farol-book.pdf
    ../.venv/bin/python assemble.py --no-build # only re-join existing parts
"""
import os, subprocess, sys, importlib, pathlib
import pymupdf

HERE = pathlib.Path(__file__).parent
PY = str(HERE.parent / ".venv" / "bin" / "python")
UNITS = [(0, ("u0_a",)), (1, ("pages_a", "pages_b", "pages_c")), (2, ("u2_a", "u2_b")),
         (3, ("u3_a", "u3_b")), (4, ("u4_a", "u4_b")), (5, ("u5_a",)), (6, ("u6_a",)), (7, ("u7_a",))]
FRONT = 6

sys.path.insert(0, str(HERE))
os.chdir(HERE)
import parts  # noqa: E402

plan, start = [], FRONT + 1
for n, mods in UNITS:
    pages = {}
    for m in mods:
        if importlib.util.find_spec(m):
            pages.update(importlib.import_module(m).P)
    if not pages:
        print(f"unit {n}: missing, skipped"); continue
    total = max(pages)
    assert sorted(pages) == list(range(1, total + 1)), f"unit {n}: pages {sorted(pages)}"
    assert start % 2 == 1, f"unit {n} would open on a left page ({start})"
    plan.append((n, mods, start, total)); start += total
last_unit = start - 1

if "--no-build" not in sys.argv:
    for n, mods, s, total in plan:
        env = dict(os.environ, UNIT=str(n), MODS=",".join(mods), TAG=f"bk-u{n}", OFF=str(s - 1))
        out = subprocess.run([PY, "build.py"], env=env, capture_output=True, text=True)
        bad = [l for l in (out.stdout + out.stderr).splitlines() if "OVERFLOW" in l or "!!" in l or "Error" in l]
        print(f"unit {n}: pp. {s}-{s + total - 1}", "OK" if out.returncode == 0 and not bad else
              "PROBLEM rc=%d pages %s" % (out.returncode, sorted({l.split(":")[0].replace("OVERFLOW ", "") for l in bad if l.startswith("OVERFLOW")})))
    out = subprocess.run([PY, "build.py"], env=dict(os.environ, UNIT="fm", TAG="fm"), capture_output=True, text=True)
    bad = [l.split(":")[0] for l in (out.stdout + out.stderr).splitlines() if l.startswith("OVERFLOW")]
    print("front/back matter:", "OK" if out.returncode == 0 and not bad else f"PROBLEM rc={out.returncode} {bad} {out.stderr[-300:]}")

book = pymupdf.open()
fm = pymupdf.open(HERE / "farol-fm.pdf")
assert fm.page_count == FRONT + 3, fm.page_count
book.insert_pdf(fm, from_page=0, to_page=FRONT - 1)
toc = [[1, "Capa", 1], [1, "Ficha técnica", 2], [1, "Como usar o Farol", 3], [1, "Índice", 4], [1, "A escada de leitura", 6]]
import fm as FM  # noqa: E402  (titles, same computation as the contents page)
for n, mods, s, total in plan:
    d = pymupdf.open(HERE / f"farol-bk-u{n}.pdf")
    assert d.page_count == total, (n, d.page_count, total)
    assert len(book) + 1 == s, (n, len(book) + 1, s)
    book.insert_pdf(d)
    toc.append([1, f"Unidade {n} · {FM.INFO[n]['title']}", s])
    for st, title, p in FM.INFO[n]["stations"]:
        toc.append([2, f"{st}" + (f" — {title}" if title and title != st else ""), p])
book.insert_pdf(fm, from_page=FRONT, to_page=FRONT + 2)
toc += [[1, "Glossário", last_unit + 1], [1, "Fontes e créditos", last_unit + 2], [1, "Contracapa", last_unit + 3]]
# The house-standard front cover, imprint and back cover (std_pages.py) replace fm.py's own.
STD = [HERE / f"std-{k}.pdf" for k in ("front", "imprint", "back")]
if all(p.exists() for p in STD):
    fin = pymupdf.open()
    fin.insert_pdf(pymupdf.open(STD[0])); fin.insert_pdf(pymupdf.open(STD[1]))
    fin.insert_pdf(book, from_page=2, to_page=len(book) - 2)
    fin.insert_pdf(pymupdf.open(STD[2]))
    assert len(fin) == len(book), (len(fin), len(book))
    book = fin
    toc[1][1] = "Imprint"
book.set_toc(toc)
book.set_metadata({"title": "Farol · Português 6", "author": "Prime School Press", "subject": "Português · 6.º ano · Manual do aluno",
                   "keywords": "Prime School; Português; 6.º ano", "creator": "Prime Books", "producer": "Prime Books · Farol pipeline"})
book.save(HERE / "farol-book.pdf", garbage=4, deflate=True)

n = len(book)
non_ttf = sorted({f[3] for p in book for f in p.get_fonts() if f[1] not in ("TrueType", "Type0", "CIDFontType2") and f[1] != "ttf"})
fonts_all = sorted({(f[1], f[3].split("+")[-1]) for p in book for f in p.get_fonts()})
blank = [i + 1 for i, p in enumerate(book) if not p.get_text().strip() and not p.get_images() and not p.get_drawings()]
sizes = {(round(p.rect.width / 72 * 25.4), round(p.rect.height / 72 * 25.4)) for p in book}
print(f"book: {n} pp, even={n % 2 == 0}, sizes={sizes}, blank={blank}")
print("unit openers:", [(u, s) for u, _, s, _ in plan])
print("font types:", sorted({t for t, _ in fonts_all}))
