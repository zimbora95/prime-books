#!/usr/bin/env python3
"""QA of the assembled book (fm/build/book.pdf) — run after assemble.py.

1. page count, even, no blank page;
2. contents (Índice): EVERY entry checked against the real page text (units: the entry's first heading; front/back
   matter: the page's own title);
3. every QR code in the whole book decoded (brief's tiled cv2 at 200 dpi, multi-decode per tile, on every page; the
   «Recursos digitais» page again one crop per code); the decoded set is compared with the codes harvested from the
   units; none may contain «vercel»; every distinct URL must answer HTTP 200 (curl -L);
4. every page's text searched for «vercel», «Year», «YEAR», «Ouvir a faixa», «vozes sintéticas» (must be none), plus
   a watch list («áudio», «faixa», «.mp3», «textos-professor.md») reported for review;
5. fonts: only Fraunces / Figtree / DM Mono / Caveat (+ the cover's Poppins / Andika), all Type0, no Type3.
Writes build/qa.json and build/qa.md and prints a summary.
"""
import json
import os
import re
import subprocess
import sys

import cv2
import numpy as np
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
sys.path.insert(0, HERE)
import qrscan  # noqa: E402

FRONT = 8
FORBIDDEN = ["vercel", "Year", "YEAR", "Ouvir a faixa", "vozes sintéticas"]
WATCH = [r"(?i)\báudio", r"(?i)\bfaixas?\b", r"(?i)\.mp3", r"textos-professor\.md", r"(?i)audio/"]
FAMILIES = ("Fraunces", "Figtree", "DMMono", "Caveat", "Poppins", "Andika")


def norm(s):
    return re.sub(r"[^\wáàâãéêíóôõúç]", "", s.lower())


def per_code_decode(pg):
    det = cv2.QRCodeDetector()
    rs = []
    for x in pg.get_drawings():
        r = x["rect"]
        if 35 < r.width < 95 and abs(r.width - r.height) < 1 and not any(abs(r.x0 - q.x0) < 3 and abs(r.y0 - q.y0) < 3 for q in rs):
            rs.append(r)
    rs.sort(key=lambda r: (round(r.y0), r.x0))
    out = []
    for r in rs:
        v = ""
        for m in (8, 2, 12, 0, 4):  # 200 dpi, crop margins in pt; cv2 is sensitive to the crop, not to the code
            pix = pg.get_pixmap(dpi=200, clip=r + (-m, -m, m, m))
            a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
            v, _, _ = det.detectAndDecode(a)
            if v:
                break
        out.append(dict(rect=[round(c) for c in r], url=v))
    return out


def qr_candidates(pg):
    """vector QR codes (segno SVG -> one dark stroked path of hundreds of module runs), deduplicated by position"""
    rs = []
    for x in pg.get_drawings():
        r = x["rect"]
        col = x.get("color") or x.get("fill") or (1, 1, 1)
        if 28 < r.width < 130 and abs(r.width - r.height) < 3 and len(x["items"]) > 150 and sum(col) < 1.5 \
                and not any(abs(r.x0 - q.x0) < 4 and abs(r.y0 - q.y0) < 4 for q in rs):
            rs.append(r)
    return rs


def decode_rects(pg, rs):
    det = cv2.QRCodeDetector()
    out = []
    for r in rs:
        v = ""
        for m in (8, 2, 12, 0, 4, 16):
            pix = pg.get_pixmap(dpi=200, clip=(r + (-m, -m, m, m)) & pg.rect)
            a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
            v, _, _ = det.detectAndDecode(a)
            if v:
                break
        out.append(dict(rect=[round(c) for c in r], url=v))
    return out


def http(url):
    r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code} %{url_effective}", "--max-time", "40",
                        "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
                        "-H", "Accept-Language: pt-PT,pt;q=0.9", url], capture_output=True, text=True)
    code, _, eff = r.stdout.partition(" ")
    return code, eff


def main():
    book = pymupdf.open(os.path.join(BUILD, "book.pdf"))
    M = json.load(open(os.path.join(BUILD, "model.json")))
    H = json.load(open(os.path.join(BUILD, "harvest.json")))
    qa = dict(pages=book.page_count, even=book.page_count % 2 == 0, plan_total=M["total"])
    qa["blank"] = [i + 1 for i, pg in enumerate(book) if not pg.get_text().strip() and not pg.get_images() and not pg.get_drawings()]
    # --- 2. contents: every entry
    checks = []
    for u in M["units"]:
        for e in u["entries"]:
            if e.get("provisional"):
                checks.append(dict(unit=u["n"], entry=e["label"], page=e["page"], ok=False, probe="(provisional)"))
                continue
            txt = norm(book[e["page"] + FRONT - 1].get_text())
            probes = [e["label"].split("·")[-1]] + ([e["first_sub"]] if e.get("first_sub") else [])
            ok = all(norm(p) in txt for p in probes)  # the label AND the heading shown beside it are on that page
            checks.append(dict(unit=u["n"], entry=e["label"] + (f" — {e['first_sub']}" if e.get("first_sub") else ""),
                               probe=" + ".join(probes), page=e["page"], ok=ok))
    for t, p in M["back_index"]:
        txt = book[p + FRONT - 1].get_text()
        probe = {"Textos para o professor ler em voz alta": "Textos para o professor",
                 "O meu 5.º ano — antes de fechar o livro": "Antes de fechar o livro"}.get(t, t)
        checks.append(dict(unit="fim", entry=t, probe=probe, page=p, ok=norm(probe) in norm(txt)))
    roman = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]
    for t, f in M["front_index"]:
        txt = book[roman.index(f)].get_text()
        probe = {"Índice": "O ano em sete unidades", "O meu ano de leitura": "Diário de leitura",
                 "Quem sou eu como leitor": "Eu, leitor"}.get(t, t)
        checks.append(dict(unit="abertura", entry=t, probe=probe, page=f, ok=norm(probe) in norm(txt)))
    qa["contents_checks"] = checks
    # --- 3. QR: whole book (tiled, multi) + resources page per code
    allq = qrscan.scan(os.path.join(BUILD, "book.pdf"), multi=True)
    qa["book_qr"] = [(p, u) for p, u, _ in allq]
    rp = M["bp"]["Recursos digitais"] + FRONT
    codes = per_code_decode(book[rp - 1])
    unit_urls = {q["url"] for k in map(str, range(1, 8)) for q in (H.get(k) or {}).get("qrs", [])}
    dec = {c["url"] for c in codes}
    qa["resources"] = dict(book_page=rp, folio=M["bp"]["Recursos digitais"], codes=len(codes), decoded=sum(1 for c in codes if c["url"]),
                           matches_units=dec == unit_urls, missing=sorted(unit_urls - dec), extra=sorted(dec - unit_urls - {""}),
                           undecoded=[c["rect"] for c in codes if not c["url"]])
    # every vector QR on every page, one crop per code (independent of the tiled scan)
    per = []
    for i, pg in enumerate(book):
        for c in decode_rects(pg, qr_candidates(pg)):
            per.append((i + 1, c["url"], c["rect"]))
    qa["book_qr_percode"] = per
    tiled_by_page = {}
    for p, u in qa["book_qr"]:
        tiled_by_page.setdefault(p, []).append(u)
    qa["percode_undecoded"] = [(p, r) for p, u, r in per if not u]
    qa["tiled_not_in_percode"] = sorted({(p, u) for p, u in qa["book_qr"]} - {(p, u) for p, u, _ in per})
    urls = sorted({u for _, u in qa["book_qr"]} | (dec - {""}) | {u for _, u, _ in per if u})
    qa["vercel_qr"] = [u for u in urls if "vercel" in u.lower()]
    qa["http"] = {u: http(u) for u in urls}
    qa["http_bad"] = {u: v for u, v in qa["http"].items() if v[0] != "200"}
    # --- 4. text search
    hits, watch = [], []
    for i, pg in enumerate(book):
        t = pg.get_text()
        for w in FORBIDDEN:
            for m in re.finditer(re.escape(w), t):
                hits.append((i + 1, w, t[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")))
        for w in WATCH:
            for m in re.finditer(w, t):
                watch.append((i + 1, w, t[max(0, m.start() - 50):m.end() + 50].replace("\n", " ")))
    qa["forbidden_text"] = hits
    qa["watch_text"] = watch
    # --- 5. fonts
    fonts = sorted({(f[2], re.sub(r"^[A-Z]{6}\+", "", f[3])) for pg in book for f in pg.get_fonts()})
    qa["fonts"] = fonts
    qa["fonts_bad"] = [f for f in fonts if f[0] != "Type0" or not re.sub(r"[\s-]", "", f[1]).startswith(FAMILIES)]
    json.dump(qa, open(os.path.join(BUILD, "qa.json"), "w"), ensure_ascii=False, indent=1)
    ok_c = sum(c["ok"] for c in checks)
    L = [f"pages {qa['pages']} (plan {qa['plan_total']}) even={qa['even']} blank={qa['blank']}",
         f"contents: {ok_c}/{len(checks)} entries confirmed on their page"]
    L += [f"   BAD p.{c['page']} {c['entry']} | probe {c['probe']}" for c in checks if not c["ok"]]
    L += [f"QR whole book: {len(allq)} codes on {len({p for p, _, _ in allq})} pages, {len(urls)} distinct URLs; vercel: {qa['vercel_qr'] or 'none'}",
          f"QR one crop per vector code, every page: {len(per)} codes found, {sum(1 for x in per if x[1])} decoded, undecoded {qa['percode_undecoded'] or 'none'}; "
          f"tiled hits not found as vector codes: {qa['tiled_not_in_percode'] or 'none'}",
          f"Recursos digitais (book p. {rp}): {qa['resources']['decoded']}/{qa['resources']['codes']} decoded one crop per code; "
          f"same set as the units: {qa['resources']['matches_units']} missing {qa['resources']['missing']} extra {qa['resources']['extra']}",
          f"HTTP: {sum(1 for v in qa['http'].values() if v[0] == '200')}/{len(urls)} return 200; not 200: {qa['http_bad'] or 'none'}",
          f"forbidden text: {len(hits)} hits" + "".join(f"\n   p.{p} «{w}»: …{c}…" for p, w, c in hits[:40]),
          f"watch list: {len(watch)} hits" + "".join(f"\n   p.{p} {w}: …{c}…" for p, w, c in watch[:80]),
          f"fonts: {fonts}", f"fonts not allowed: {qa['fonts_bad'] or 'none'}"]
    L += ["QR by book page (one crop per code):"] + [f"   p.{p} {u}  -> {qa['http'].get(u, ('?',))[0]}" for p, u, _ in per]
    open(os.path.join(BUILD, "qa.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
