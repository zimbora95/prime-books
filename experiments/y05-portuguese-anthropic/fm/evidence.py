"""Before/after PNGs of every page this job changed (fm/qa-evidence/). Read-only on the published edition.

before = /root/prime-books/public/library/y05-portuguese-anthropic/book.pdf (the previous assembled edition) and the
master's covers; after = fm/build/book.pdf.
"""
import json
import os

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "qa-evidence")
os.makedirs(EV, exist_ok=True)
M = json.load(open(os.path.join(HERE, "build", "model.json")))
after = pymupdf.open(os.path.join(HERE, "build", "book.pdf"))
before = pymupdf.open("/root/prime-books/public/library/y05-portuguese-anthropic/book.pdf")
master = pymupdf.open("/root/prime-books/public/library/y05-portuguese/book.pdf")
bp = M["bp"]
F = 8


def save(doc, pno, name, dpi=110):
    doc[pno - 1].get_pixmap(dpi=dpi).save(os.path.join(EV, name))


# (name, before (doc, page) or None, after page)
old_bp = {"Glossário": 145, "Recursos digitais": 147, "Referências e créditos": 148, "Planificação anual": 149,
          "O meu 5.º ano — antes de fechar o livro": 150, "Colofão": 151}
pairs = [("p001-capa", (master, 1), 1), ("p002-ficha-tecnica", (before, 2), 2), ("p003-como-usar", (before, 3), 3),
         ("p004-mapa", (before, 4), 4), ("p005-indice", (before, 5), 5), ("p006-indice-cont", (before, 6), 6),
         ("p007-diario-leitura", (before, 7), 7)]
for k, (t, p) in enumerate(sorted(old_bp.items(), key=lambda x: x[1])):
    pairs.append((f"fim-{p}-{t.split(' ')[0].lower()}", (before, p + F), bp[t] + F))
pairs.append(("contracapa", (master, master.page_count), after.page_count))
for name, b, a in pairs:
    if b:
        save(b[0], b[1], f"{name}-before.png")
    save(after, a, f"{name}-after.png")
for p, t in M["back"]:
    if t.startswith("Soluções") or t.startswith("Textos"):
        save(after, p + F, f"new-{p}-{'solucoes' if t.startswith('Soluções') else 'textos-professor'}.png")
print(len(pairs), "pairs +", sum(1 for p, t in M["back"] if t.startswith(("Soluções", "Textos"))), "new pages ->", EV)
