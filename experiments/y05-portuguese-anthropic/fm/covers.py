#!/usr/bin/env python3
"""The book's covers, in Portuguese, on the master's own art (fm/build/covers.pdf, 2 pages at the master's 576 × 828 pt).

    /root/.venvs/y05exp/bin/python covers.py

Front = page 1 of /root/prime-books/public/library/y05-portuguese/book.pdf: the three live spans over the art
(«Portuguese 1st Language» / «Year 5» / «Student Manual») are redacted (text only — images and vector art are kept)
and re-set in the same font file, size, colour and baseline: «Português» / «5.º Ano» / «Manual do aluno».

Back = the master's last page, which is ONE raster with every word baked in. Its words are removed by copying the
same pixels from the text-free art of the same back (git 8817b5c, the cover_std build before it was flattened:
measured identical, 0 px shift, mean |Δ| 1.6 levels, colour-fitted per channel); inside the sand card the words are
filled with the card's own flat tone. Stripe, accent bar, card and art stay the master's pixels. The Portuguese copy
is then typeset as live text at the cover_std baselines (Poppins SemiBold/ExtraBold + Andika, the master's fonts).

Nothing under public/ is written; the master is only read. Assembly (assemble.py) fits these pages to A4 by scaling to
the width (×1.0335) and cropping the height symmetrically (6.9 pt ≈ 2.4 mm top and bottom).
"""
import io
import os
import subprocess

import numpy as np
import pymupdf
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
REPO = "/root/prime-books"
MASTER = os.path.join(REPO, "public/library/y05-portuguese/book.pdf")
FRONT_DY = 44.0   # pt: logo + title block moved down so the print wrap does not crop the logo
ASSETS = os.path.join(REPO, "tools/cover_assets")
F_XB = os.path.join(ASSETS, "Poppins-ExtraBold.ttf")
F_SB = os.path.join(ASSETS, "Poppins-SemiBold.ttf")
F_AN = os.path.join(ASSETS, "Andika-Regular.ttf")
DONOR_REV = "8817b5c"

INK = (0x1A / 255, 0x1A / 255, 0x1A / 255)
GREY = (0x6B / 255, 0x6B / 255, 0x5E / 255)
BODY = (0x2E / 255, 0x2A / 255, 0x24 / 255)
BROWN = (0x5A / 255, 0x24 / 255, 0x09 / 255)
TERRA = (0x7C / 255, 0x40 / 255, 0x22 / 255)

# Portuguese copy. hook/bullets = tools/cover_assets/back_copy.json["y05-portuguese"], unchanged; the blurb is the
# same sentence with «do Year 5» → «do 5.º ano» (the book never says «Year 5»).
TITLE = "Português"
SUBTITLE = "5.º Ano · Manual do aluno"
HOOK = "Ler, escrever e falar. Cada vez melhor."
BLURB = ("O português do 5.º ano: leitura de textos longos, escrita com intenção e fala em público. "
         "Gramática e ortografia sempre em contexto, nunca decoradas.")
CARD = "NESTE LIVRO"
BULLETS = ["Leitura, escrita e fala em todas as unidades", "Textos longos e oficinas de escrita",
           "Gramática e ortografia em contexto", "Apresentações orais guiadas", "Ilustração original em aguarela"]
FOOT1 = "Prime Books · Português"
FOOT2 = "9–10 anos · 2.º Ciclo do Ensino Básico"  # house pt-PT form (Y9: «14–15 anos · 3.º Ciclo do Ensino Básico»)
FOOT3 = "primeschool.pt"


def check_glyphs():
    for path, txt in [(F_XB, TITLE), (F_SB, "5.º Ano" + "P R I M E  B O O K S" + CARD + FOOT1 + FOOT3),
                      (F_AN, "Manual do aluno" + SUBTITLE + HOOK + BLURB + "".join(BULLETS) + FOOT2 + "•")]:
        f = pymupdf.Font(fontfile=path)
        miss = sorted({c for c in txt if c != " " and not f.has_glyph(ord(c))})
        assert not miss, (os.path.basename(path), miss)


def wrap(text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.text_length(t, fontsize=size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def front(out):
    src = pymupdf.open(MASTER)
    out.insert_pdf(src, from_page=0, to_page=0)
    pg = out[-1]
    spans = [s for b in pg.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
    want = {"Portuguese 1st Language": (TITLE, F_XB), "Year 5": ("5.º Ano", F_SB), "Student Manual": ("Manual do aluno", F_AN)}
    found = {s["text"].strip(): s for s in spans}
    assert set(want) <= set(found), found.keys()
    for s in spans:
        pg.add_redact_annot(pymupdf.Rect(s["bbox"]) + (-0.5, -0.5, 0.5, 0.5), fill=None)
    pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                        text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    assert not pg.get_text().strip(), "front: redaction left text"
    # The print wrap crops ~13 mm off the top of this page when it is fitted to BookVault's
    # 216 x 279 mm trim (A4-ish master, taller aspect), which put the logo on the cut. Move the
    # logo and the title block down by FRONT_DY so they clear the trim and the 5 mm safety line
    # with room to spare; the art below (from y = 315 pt) is untouched.
    logo = [im for im in pg.get_image_info(xrefs=True) if im["bbox"][3] < 200]
    assert len(logo) == 1, logo
    lx, lb = logo[0]["xref"], pymupdf.Rect(logo[0]["bbox"])
    pix = pymupdf.Pixmap(out, lx)
    if pix.alpha == 0:
        smask = out.xref_get_key(lx, "SMask")[1]
        if smask not in ("null", ""):
            pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(out, int(smask.split()[0])))
    logo_png = pix.tobytes("png")
    # hide the original placement under the page's own flat cream ground (drawing 0 = full-page fill;
    # the logo sits inside a form XObject, which redaction does not reach)
    ground = pg.get_drawings()[0]
    assert ground["rect"] == pg.rect and ground.get("fill"), ground
    pg.draw_rect(lb + (-1, -1, 1, 1), color=None, fill=ground["fill"], overlay=True)
    pg.insert_image(lb + (0, FRONT_DY, 0, FRONT_DY), stream=logo_png)
    for old, (new, ff) in want.items():
        s = found[old]
        c = s["color"]
        rgb = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
        name = {F_XB: "PoppinsXB", F_SB: "PoppinsSB", F_AN: "Andika"}[ff]
        o = s["origin"]
        pg.insert_text((o[0], o[1] + FRONT_DY), new, fontsize=s["size"], fontname=name, fontfile=ff, color=rgb)
    return [(s["text"], s["font"], round(s["size"], 2), hex(s["color"]), [round(v, 1) for v in s["origin"]]) for s in spans]


def donor_art():
    p = os.path.join(BUILD, "coverhist", f"{DONOR_REV}.pdf")
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        b = subprocess.run(["git", "show", f"{DONOR_REV}:public/library/y05-portuguese/book.pdf"], cwd=REPO,
                           capture_output=True, check=True).stdout
        open(p, "wb").write(b)
    d = pymupdf.open(p)
    last = d[-1]
    x = d.extract_image(last.get_images(full=True)[0][0])
    spans = [s for b in last.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
    return Image.open(io.BytesIO(x["image"])).convert("RGB"), spans


def back(out):
    src = pymupdf.open(MASTER)
    last = src[-1]
    W, H = last.rect.width, last.rect.height
    xs = last.get_images(full=True)
    x = src.extract_image(xs[-1][0])  # two identical full-page rasters are drawn; the last one is on top
    cur = Image.open(io.BytesIO(x["image"])).convert("RGB")
    S = cur.width / W
    don_img, don_spans = donor_art()
    don = np.asarray(don_img.resize(cur.size, Image.LANCZOS)).astype(float)
    a = np.asarray(cur).astype(float)
    # colour-fit donor -> today's raster on a text-free window (below the card)
    win = (slice(int(560 * S), int(680 * S)), slice(int(60 * S), int(560 * S)))
    fit = don.copy()
    for c in range(3):
        k, m = np.polyfit(don[win][..., c].ravel(), a[win][..., c].ravel(), 1)
        fit[..., c] = k * don[..., c] + m
    card = (71.0, 380.88, 430.0, 528.88)  # the sand card (cover_std geometry; measured on the raster 70.7–428.7 × 380.3–527.6)
    cx0, cy0, cx1, cy1 = [int(round(v * S)) for v in card]
    tone = np.median(a[cy0 + 8:cy0 + 18, cx0 + 250:cx1 - 20].reshape(-1, 3), axis=0)
    res = a.copy()
    boxes = []
    for s in don_spans:  # every word of the old template (the donor's own text boxes), padded
        r = pymupdf.Rect(s["bbox"]) + (-3, -2.5, 3, 2.5)
        if s["text"].startswith("Year 5"):
            r.x1 = max(r.x1, 330)  # the subtitle line, whatever its length
        x0, y0, x1, y1 = max(int(r.x0 * S), int(40 * S)), int(r.y0 * S), min(int(r.x1 * S), cur.width), int(r.y1 * S)
        inside = r.y0 >= card[1] and r.y1 <= card[3]
        if inside:
            res[y0:y1, x0:x1] = tone
        else:
            res[y0:y1, x0:x1] = fit[y0:y1, x0:x1]
        boxes.append((x0, y0, x1, y1, inside, s["text"]))
    img = Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))
    # 1 px melt on the patch borders
    soft = img.filter(ImageFilter.GaussianBlur(0.8))
    mask = Image.new("L", img.size, 0)
    mk = np.zeros((img.height, img.width), np.uint8)
    for x0, y0, x1, y1, _, _ in boxes:
        mk[max(y0 - 1, 0):y0 + 2, x0:x1] = 255
        mk[y1 - 2:y1 + 1, x0:x1] = 255
        mk[y0:y1, max(x0 - 1, 0):x0 + 2] = 255
        mk[y0:y1, x1 - 2:x1 + 1] = 255
    mask = Image.fromarray(mk)
    img.paste(soft, (0, 0), mask)
    # verification: nothing dark left where the words were (outside the card, the art's own lines stay > 150)
    arr = np.asarray(img).astype(int).sum(2) / 3
    chk = []
    for x0, y0, x1, y1, inside, t in boxes:
        chk.append((t[:28], inside, int(arr[y0:y1, x0:x1].min()), round(float(np.abs(arr[y0:y1, x0:x1] - np.asarray(don_img.resize(cur.size)).astype(int).sum(2)[y0:y1, x0:x1] / 3).mean()), 1)))
    clean_png = os.path.join(BUILD, "back-art-clean.png")
    img.save(clean_png)
    pg = out.new_page(width=W, height=H)
    pg.insert_image(pg.rect, filename=clean_png)
    x0 = 85.0
    pg.insert_text((x0, 78), "P R I M E  B O O K S", fontsize=9.6, fontname="PoppinsSB", fontfile=F_SB, color=GREY)
    pg.insert_text((x0, 128), TITLE, fontsize=33, fontname="PoppinsXB", fontfile=F_XB, color=INK)
    pg.insert_text((x0, 188), SUBTITLE, fontsize=11, fontname="Andika", fontfile=F_AN, color=GREY)
    fa = pymupdf.Font(fontfile=F_AN)
    pg.insert_text((x0, 214), HOOK, fontsize=11.4, fontname="Andika", fontfile=F_AN, color=BODY)
    y = 238.2
    for ln in wrap(BLURB, fa, 11.4, 438):
        pg.insert_text((x0, y), ln, fontsize=11.4, fontname="Andika", fontfile=F_AN, color=BODY)
        y += 17.2
    assert y < 300, y
    pg.insert_text((87, 404.9), CARD, fontsize=9.4, fontname="PoppinsSB", fontfile=F_SB, color=BROWN)
    yy = 424.9
    for b in BULLETS:
        pg.insert_text((87, yy), "•", fontsize=10.6, fontname="Andika", fontfile=F_AN, color=BODY)
        lines = wrap(b, fa, 10.6, 430 - 71 - 46)
        for k, ln in enumerate(lines):
            pg.insert_text((101, yy), ln, fontsize=10.6, fontname="Andika", fontfile=F_AN, color=BODY)
            yy += 19 if k == 0 else 15
    assert yy < card[3] + 12, yy
    pg.insert_text((x0, 700), FOOT1, fontsize=9, fontname="PoppinsSB", fontfile=F_SB, color=INK)
    pg.insert_text((x0, 716), FOOT2, fontsize=9, fontname="Andika", fontfile=F_AN, color=GREY)
    pg.insert_text((x0, 732), FOOT3, fontsize=9, fontname="PoppinsSB", fontfile=F_SB, color=TERRA)
    return chk


def main():
    os.makedirs(BUILD, exist_ok=True)
    check_glyphs()
    out = pymupdf.open()
    spans = front(out)
    chk = back(out)
    p = os.path.join(BUILD, "covers.pdf")
    out.save(p, garbage=3, deflate=True)
    d = pymupdf.open(p)
    print("covers.pdf", d.page_count, "pages", [tuple(round(v, 1) for v in pg.rect) for pg in d])
    print("front: master spans replaced:", spans)
    print("front text now:", d[0].get_text().split("\n"))
    print("back text now:", d[1].get_text().split("\n"))
    print("back: former word boxes (text, in card, min grey after, mean |Δ| vs donor):")
    for c in chk:
        print("   ", c)
    print("fonts:", sorted({(f[2], f[3]) for pg in d for f in pg.get_fonts()}))
    ev = os.path.join(HERE, "qa-evidence")
    os.makedirs(ev, exist_ok=True)
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=110).save(os.path.join(ev, f"cover-{'front' if i == 0 else 'back'}-after.png"))
    m = pymupdf.open(MASTER)
    m[0].get_pixmap(dpi=110).save(os.path.join(ev, "cover-front-before.png"))
    m[-1].get_pixmap(dpi=110).save(os.path.join(ev, "cover-back-before.png"))


if __name__ == "__main__":
    main()
