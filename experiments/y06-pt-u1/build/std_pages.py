"""The three STANDARD pages of Farol, built on the house templates at Farol's trim.

    ../.venv/bin/python std_pages.py      -> std-front.pdf, std-imprint.pdf, std-back.pdf

1  Front cover  = the catalogue cover of the standard Year 6 Portuguese title
                  (public/library/y06-portuguese, page 1: title, Year 6, Student Manual,
                  year stripe, logo, the same cutout art), recomposed with the geometry of
                  tools/std_front_lib.build_front at 216 x 279 mm. The art keeps its
                  proportions (build_front stretches it) and is set 14 pt lower, into the art's own
                  empty foot, so the cypress clears "Student Manual" and the pedestal stays whole.
2  Imprint      = tools/std_imprint_lib.py (the house page 2), content in std_imprint.json.
3  Back cover   = the back of the standard Year 6 Portuguese title as it was before the
                  2026-09-09 redaction left white bars over its blurb (git 8817b5c): the same
                  washed art, title, hook, blurb and INSIDE THIS BOOK list, verbatim, set on
                  the current back standard (y01-art-and-design: PRIME SCHOOL PRESS imprint,
                  "Year N · Prime School Press · Student Manual", Prime School Press footer).
"""
import os, subprocess, sys, pathlib
import pymupdf

HERE = pathlib.Path(__file__).parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools"))
import std_front_lib as F          # noqa: E402
import std_imprint_lib as I        # noqa: E402

W, H = 216 / 25.4 * 72, 279 / 25.4 * 72           # Farol's trim: 612.28 x 790.87 pt
ART = HERE / "img" / "std-front-art.png"
BACK_ART = HERE / "img" / "std-back-art.png"
STRIPE = tuple(c / 255 for c in F.META["stripes"]["6"])         # (131, 95, 193)
_, ACCENT = I.year_colours(6)                                   # dark tone for small type


def extract_art():
    """Pull the two artworks out of the standard title (current front; pre-redaction back)."""
    if not ART.exists():
        d = pymupdf.open(REPO / "public/library/y06-portuguese/book.pdf")
        xref, _ = F.find_front_art(d[0])
        smask = [im for im in d[0].get_images(full=True) if im[0] == xref][0][1]
        pix = pymupdf.Pixmap(pymupdf.Pixmap(d, xref), pymupdf.Pixmap(d, smask)) if smask else pymupdf.Pixmap(d, xref)
        pix.save(str(ART))
    if not BACK_ART.exists():
        blob = subprocess.run(["git", "show", "8817b5c:public/library/y06-portuguese/book.pdf"],
                              cwd=REPO, capture_output=True, check=True).stdout
        d = pymupdf.open("pdf", blob)
        pymupdf.Pixmap(d, d[-1].get_images(full=True)[0][0]).save(str(BACK_ART))


def front():
    doc = pymupdf.open(); p = doc.new_page(width=W, height=H)
    stripe_w = 34.0
    p.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=F.CREAM)
    p.draw_rect(pymupdf.Rect(0, 0, stripe_w, H), color=None, fill=STRIPE)
    F.draw_logo(p, 85, 42, height=64.0)
    size = 33.0
    lines = F.wrap("Português 1.ª Língua", F.f_title, size, W - 125)
    for i, line in enumerate(lines):
        p.insert_text((85.0, 140 + i * 38), line, fontsize=size, fontname="ttl", fontfile=F.FONT_TITLE, color=F.INK)
    ymeta = 140 + len(lines) * 38 + 26
    p.insert_text((85.0, ymeta), "6.º Ano", fontsize=17, fontname="med", fontfile=F.FONT_TITLE_MED, color=F.INK)
    p.insert_text((85.0, ymeta + 24), "Manual do Aluno", fontsize=11, fontname="body", fontfile=F.FONT_BODY, color=F.GREY)
    art_w = W - stripe_w
    art_h = art_w * 1024 / 1090                       # the art's own proportions
    top = H - art_h + 14.0                            # 14 pt into the art's own empty foot: base whole, cypress clear
    p.insert_image(pymupdf.Rect(stripe_w, top, W, top + art_h), filename=str(ART))
    return doc


def back():
    doc = pymupdf.open(); p = doc.new_page(width=W, height=H)
    p.insert_image(pymupdf.Rect(0, 0, W, H), filename=str(BACK_ART), keep_proportion=False)
    p.draw_rect(pymupdf.Rect(0, 0, 34, H), color=None, fill=STRIPE)
    rgb = lambda h: tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    semi, xbold, body = F.FONT_TITLE_MED, F.FONT_TITLE, F.FONT_BODY

    def t(x, top, text, font, size, col):
        f = pymupdf.Font(fontfile=font)
        base = top + f.ascender * size                 # bbox top -> baseline, as measured
        p.insert_text((x, base), text, fontsize=size, fontfile=font, fontname="f" + os.path.basename(font).split(".")[0].replace("-", "")[:14], color=col)

    t(85, 67.9, "P R I M E  S C H O O L  P R E S S", semi, 9.6, rgb("#6b6b5e"))
    t(85, 93.4, "Português 1.ª Língua", xbold, 33.0, rgb("#1a1a1a"))
    p.draw_rect(pymupdf.Rect(85, 166, 107, 169), color=None, fill=STRIPE)
    t(85, 174.6, "6.º Ano · Prime School Press · Manual do Aluno", body, 11.0, rgb("#6b7d72"))
    t(85, 200.1, "O último ano do ensino primário, em português.", body, 11.4, rgb("#2e2a24"))
    blurb = ("Leitura, escrita e fala em nível de exame. Textos longos, escrita com intenção, "
             "apresentações orais, e a gramática e a ortografia sempre em contexto.")
    fb = pymupdf.Font(fontfile=body)
    for i, line in enumerate(F.wrap(blurb, fb, 11.4, 438)):
        t(85, 224.3 + 17.2 * i, line, body, 11.4, rgb("#2e2a24"))
    p.draw_rect(pymupdf.Rect(71, 364.3, 470, 512.3), color=None, fill=rgb("#f2ebdc"), radius=0.06)
    t(87, 378.8, "INSIDE THIS BOOK", semi, 9.4, rgb("#5a2409"))
    bullets = ["Leitura, escrita e fala em nível de exame", "Textos longos e oficinas de escrita",
               "Gramática e ortografia em contexto", "Apresentações orais guiadas", "Ilustração original em aguarela"]
    for i, b in enumerate(bullets):
        t(87, 395.7 + 19 * i, "•", body, 10.6, rgb("#2e2a24"))
        t(101, 395.7 + 19 * i, b, body, 10.6, rgb("#2e2a24"))
    t(85, 717.5, "Prime School Press · Português 1.ª Língua", semi, 9.0, rgb("#1a1a1a"))
    t(85, 732.0, "Ages 10–11 · Upper Primary", body, 9.0, rgb("#6b6b5e"))
    t(85, 749.5, "primeschool.pt", semi, 9.0, ACCENT)
    # BookVault's reserved barcode box (38 x 25 mm, 6.4 mm in from the right trim, 3.3 mm up):
    # the washed art runs through it, so it gets a paper-toned panel for their barcode.
    mm = 72 / 25.4
    x1, y1 = W - 6.4 * mm, H - 3.3 * mm
    p.draw_rect(pymupdf.Rect(x1 - 40 * mm, y1 - 27 * mm, x1 + 1 * mm, y1 + 1 * mm), color=None, fill=F.CREAM, radius=0.08)
    return doc


def imprint():
    out = HERE / "std-imprint.pdf"
    r = subprocess.run([sys.executable, str(REPO / "tools/std_imprint_lib.py"), "y06-portuguese-anthropic",
                        "--spec", str(HERE / "std_imprint.json"), "--out", str(out), "--page", f"{W:.2f}x{H:.2f}"],
                       capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[-400:])
    if r.returncode:
        raise SystemExit("imprint audit failed")
    # Page 2 is a LEFT page: its gutter is the right edge. The house design is symmetric
    # (56 pt = 19.8 mm margins), a hair inside BookVault's 20 mm gutter, so the whole
    # design is placed 3 pt towards the outer edge (outer margin 18.7 mm, gutter 20.8 mm).
    src = pymupdf.open(out)
    dst = pymupdf.open(); p = dst.new_page(width=W, height=H)
    p.draw_rect(p.rect, color=None, fill=(1, 1, 1))
    p.show_pdf_page(pymupdf.Rect(-3, 0, W - 3, H), src, 0)
    src.close(); dst.save(out)


if __name__ == "__main__":
    extract_art()
    front().save(HERE / "std-front.pdf")
    back().save(HERE / "std-back.pdf")
    imprint()
    for n in ("std-front.pdf", "std-imprint.pdf", "std-back.pdf"):
        d = pymupdf.open(HERE / n)
        print(n, [round(v, 2) for v in d[0].rect[2:]], "fonts:", sorted({f[3].split("+")[-1] for f in d[0].get_fonts()}))
