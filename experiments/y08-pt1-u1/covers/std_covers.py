"""Front and back cover of «Promessa & Veredicto» on the house cover standard (the Y5/Y6
Portuguese collection), in the Year 8 colour.

    ../../.venv/bin/python covers/std_covers.py      -> covers/std-covers-a4.pdf, std-covers-letter.pdf

Front = tools/std_front_lib geometry as in experiments/y06-pt-u1/build/std_pages.py: cream page,
        year stripe, official logo, Poppins title «Português 1.ª Língua», «8.º Ano»,
        «Manual do Aluno», and a new still-life (covers/front_b.png: travertine plinths, flat
        slate-blue circle, guitarra portuguesa, azulejos, armillary sphere on books, Bordallo
        swallow, cypress), cut out of its cream ground and set in the art's own proportions.
Back  = the Prime School Press back standard (as y06): washed pencil-and-watercolour art
        (covers/back_art.png: a Lisbon writer's desk), stripe, imprint label, title, meta line,
        this book's own hook and blurb, a «Neste livro» card, footer, and the paper panel for
        BookVault's barcode box.
Two trims: A4 (the book master) and US Letter 216 x 279 mm (the BookVault print master; the
pack places these pages 1:1 instead of scaling the A4 ones).
"""
import os, pathlib, sys

import numpy as np
import pymupdf
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools"))
import std_front_lib as F          # noqa: E402
import std_imprint_lib as I        # noqa: E402

MM = 72 / 25.4
YEAR = 8
STRIPE = tuple(c / 255 for c in F.META["stripes"][str(YEAR)])      # (84, 110, 158) slate
_, ACCENT = I.year_colours(YEAR)
FRONT_SRC, BACK_SRC = HERE / "front_b.png", HERE / "back_art.png"
FRONT_ART, BACK_ART = HERE / "front-art-cut.png", HERE / "back-art-washed.jpg"
TRIMS = {"a4": (210 * MM, 297 * MM), "letter": (216 * MM, 279 * MM),
         "shell": (594.96, 765.12)}   # the y08-portuguese-1st catalogue shell keeps its own page size

TITLE = "Português 1.ª Língua"
HOOK = "«Um anúncio promete. Um crítico julga. Tu decides.»"
BLURB = ("Numa vila da costa, um cinema reabre com a estreia de um filme sobre uma baleia e um farol. "
         "Ao longo de sete sessões, vais desmontar cartazes, anúncios de rádio e campanhas; ler críticas "
         "que se contradizem; descobrir o que Fernando Pessoa e um pacote de sal têm em comum; e aprender "
         "a escrever um slogan que fica no ouvido e uma crítica em que se pode confiar. Depois, sete "
         "narrativas — de Herculano a Oscar Wilde — mostram-te como se constrói uma história e como uma "
         "história nos constrói; nove poemas ensinam-te a ouvir o verso; o teatro leva tudo isto para o "
         "palco; e, no fim, dois testes e um veredicto que dás a ti próprio. E, porque só se aprende a "
         "julgar livros lendo-os, assinas um contrato de leitura contigo próprio.")
BULLETS = ["Publicidade, crítica de cinema e de livro",
           "Sete narrativas de formação",
           "Nove poemas, oito poetas",
           "Teatro: da página ao palco",
           "Rádio ao vivo, revisões e dois testes com critérios",
           "Contrato e diário de leitura"]


def prepare_art():
    """Front: crop to the house art proportion (1090:1024) and cut the cream ground away
    (flood fill from the border, feathered) so the still-life sits on the page's own cream.
    Back: wash 62 % toward cream, as the back standard does."""
    im = Image.open(FRONT_SRC).convert("RGB")
    w, h = im.size
    ch = round(w * 1024 / 1090)
    im = im.crop((0, h - ch, w, h))                    # drop the empty top strip, keep the floor
    a = np.asarray(im).astype(np.int16)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, axis=0)
    near = (np.abs(a - bg).max(axis=2) <= 20)
    # flood fill from the border through near-background pixels
    mask = np.zeros(near.shape, bool)
    stack = [(y, x) for y in (0, near.shape[0] - 1) for x in range(near.shape[1]) if near[y, x]]
    stack += [(y, x) for x in (0, near.shape[1] - 1) for y in range(near.shape[0]) if near[y, x]]
    while stack:
        y, x = stack.pop()
        if mask[y, x] or not near[y, x]:
            continue
        mask[y, x] = True
        if y > 0: stack.append((y - 1, x))
        if y < near.shape[0] - 1: stack.append((y + 1, x))
        if x > 0: stack.append((y, x - 1))
        if x < near.shape[1] - 1: stack.append((y, x + 1))
    alpha = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
    rgba = im.convert("RGBA"); rgba.putalpha(alpha)
    rgba.save(FRONT_ART)
    b = Image.open(BACK_SRC).convert("RGB")
    cream = Image.new("RGB", b.size, tuple(round(c * 255) for c in F.CREAM))
    Image.blend(b, cream, 0.62).save(BACK_ART, quality=90)
    print(f"front art {rgba.size}, ground removed {mask.mean():.0%}; back washed")


def front(doc, W, H):
    p = doc.new_page(width=W, height=H)
    stripe_w = 34.0
    p.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=F.CREAM)
    p.draw_rect(pymupdf.Rect(0, 0, stripe_w, H), color=None, fill=STRIPE)
    F.draw_logo(p, 85, 42, height=64.0)
    size = 33.0
    lines = F.wrap(TITLE, F.f_title, size, W - 125)
    for i, line in enumerate(lines):
        p.insert_text((85.0, 140 + i * 38), line, fontsize=size, fontname="ttl", fontfile=F.FONT_TITLE, color=F.INK)
    ymeta = 140 + len(lines) * 38 + 26
    p.insert_text((85.0, ymeta), f"{YEAR}.º Ano", fontsize=17, fontname="med", fontfile=F.FONT_TITLE_MED, color=F.INK)
    p.insert_text((85.0, ymeta + 24), "Manual do Aluno", fontsize=11, fontname="body", fontfile=F.FONT_BODY, color=F.GREY)
    art_w = W - stripe_w
    art_h = art_w * 1024 / 1090                        # the art's own proportions, never stretched
    top = H - art_h + 14.0                             # 14 pt into the art's empty floor
    p.insert_image(pymupdf.Rect(stripe_w, top, W, top + art_h), filename=str(FRONT_ART))


def back(doc, W, H):
    p = doc.new_page(width=W, height=H)
    p.draw_rect(p.rect, color=None, fill=F.CREAM)
    # washed art fills the page in its own proportion (cover-crop, centred)
    aw, ah = Image.open(BACK_ART).size
    k = max(W / aw, H / ah)
    dw, dh = aw * k, ah * k
    p.insert_image(pymupdf.Rect((W - dw) / 2, (H - dh) / 2, (W + dw) / 2, (H + dh) / 2), filename=str(BACK_ART))
    p.draw_rect(pymupdf.Rect(0, 0, 34, H), color=None, fill=STRIPE)
    rgb = lambda h: tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    semi, xbold, body = F.FONT_TITLE_MED, F.FONT_TITLE, F.FONT_BODY

    def t(x, top, text, font, size, col):
        f = pymupdf.Font(fontfile=font)
        p.insert_text((x, top + f.ascender * size), text, fontsize=size, fontfile=font,
                      fontname="f" + os.path.basename(font).split(".")[0].replace("-", "")[:14], color=col)

    ink, soft = rgb("#1a1a1a"), rgb("#2e2a24")
    t(85, 67.9, "P R I M E  S C H O O L  P R E S S", semi, 9.6, rgb("#6b6b5e"))
    t(85, 93.4, TITLE, xbold, 33.0, ink)
    p.draw_rect(pymupdf.Rect(85, 166, 107, 169), color=None, fill=STRIPE)
    t(85, 174.6, f"{YEAR}.º Ano · Prime School Press · Manual do Aluno", body, 11.0, rgb("#6b7d72"))
    t(85, 200.1, HOOK, semi, 11.4, soft)
    fb = pymupdf.Font(fontfile=body)
    y = 224.3
    for line in F.wrap(BLURB, fb, 10.6, W - 85 - 70):
        t(85, y, line, body, 10.6, soft)
        y += 15.6
    card_top = y + 16
    card_h = 34 + 19 * len(BULLETS)
    p.draw_rect(pymupdf.Rect(71, card_top, 470, card_top + card_h), color=None, fill=rgb("#f2ebdc"), radius=0.06)
    t(87, card_top + 14.5, "NESTE LIVRO", semi, 9.4, rgb("#5a2409"))
    for i, b in enumerate(BULLETS):
        t(87, card_top + 31.4 + 19 * i, "•", body, 10.6, soft)
        t(101, card_top + 31.4 + 19 * i, b, body, 10.6, soft)
    t(85, H - 73.4, f"Prime School Press · {TITLE}", semi, 9.0, ink)
    t(85, H - 58.9, "12–13 anos · 3.º Ciclo do Ensino Básico", body, 9.0, rgb("#6b6b5e"))
    t(85, H - 41.4, "primeschool.pt", semi, 9.0, ACCENT)
    # BookVault's barcode box (38 x 25 mm, 6.4 mm in from the spine-side trim, 3.3 mm up) on a paper panel
    x1, y1 = W - 6.4 * MM, H - 3.3 * MM
    p.draw_rect(pymupdf.Rect(x1 - 40 * MM, y1 - 27 * MM, x1 + 1 * MM, y1 + 1 * MM), color=None, fill=F.CREAM, radius=0.08)
    return card_top + card_h


if __name__ == "__main__":
    prepare_art()
    for name, (W, H) in TRIMS.items():
        doc = pymupdf.open()
        front(doc, W, H)
        card_bottom = back(doc, W, H)
        assert card_bottom < H - 90, f"{name}: back card runs into the footer ({card_bottom:.0f} pt)"
        out = HERE / f"std-covers-{name}.pdf"
        doc.save(out, garbage=4, deflate=True)
        fonts = sorted({f[3].split("+")[-1] for pg in doc for f in pg.get_fonts()})
        print(out.name, [round(v / MM, 1) for v in doc[0].rect[2:]], "card bottom", round(card_bottom), "fonts", fonts)
