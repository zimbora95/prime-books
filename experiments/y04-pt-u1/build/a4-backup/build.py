#!/usr/bin/env python3
"""Build Rua das Palavras (Unidades 1–7).

pages/NN.html are page fragments. This script wraps them in <section class="page">,
adds the folio, inlines the SVG icon sprite, prints them to PDF with headless Chromium,
renders PNGs with PyMuPDF and reports any page whose content overflows.

usage: build.py [--bleed] [--pages 7,8]
"""
import argparse, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CHROME = pathlib.Path.home() / ".cache/ms-playwright/chromium-1243/chrome-linux64/chrome"

# (fragment, colour, kind, running label)
PAGES = [
    ("01", "red",  "full", ""),
    ("02", "sage", "std", "Prime School Press · Imprint"),
    ("03", "red",  "std",  "Unidade 1 · Mensagens na Rua do Limoeiro"),
    ("04", "red", "std", "Índice"),
    ("05", "red", "std", "Índice"),
    ("06", "red",  "full", ""),
    ("07", "red",  "std",  "Unidade 1 · O mapa da unidade"),
    ("08", "red",  "std",  "Unidade 1 · Antes de ler"),
    ("09", "red",  "std",  "Unidade 1 · A história"),
    ("10", "red",  "std",  "Paragem 1 · A carta"),
    ("11", "red",  "std",  "Paragem 1 · A carta"),
    ("12", "yel",  "std",  "Paragem 2 · O convite"),
    ("13", "yel",  "std",  "Paragem 2 · O convite"),
    ("14", "blue", "std",  "Paragem 3 · A notícia"),
    ("15", "blue", "std",  "Paragem 3 · A notícia"),
    ("16", "sage", "std",  "Paragem 4 · A banda desenhada"),
    ("17", "sage", "std",  "Paragem 4 · A banda desenhada"),
    ("18", "plum", "std",  "Oficina de gramática · Tipos de frase"),
    ("19", "plum", "std",  "Oficina de gramática · Sim ou não?"),
    ("20", "plum", "std",  "Oficina de gramática · Jogo"),
    ("21", "plum", "std",  "Oficina de gramática · Sinais da escrita"),
    ("22", "red",  "std",  "Oficina de escrita · Uma carta com opinião"),
    ("23", "red",  "std",  "Oficina de escrita · Uma carta com opinião"),
    ("24", "blue", "std",  "Paragem 5 · Projeto final"),
    ("25", "sage", "std",  "Unidade 1 · Já consigo…"),
    ("26", "plum", "std",  "Notas para o professor · Unidade 1"),
    ("27", "plum", "std",  "Notas para o professor · Unidade 1"),
    ("28", "plum", "full", ""),
    ("29", "plum", "std", "Unidade 2 · O mapa da unidade"),
    ("30", "sage", "std", "Estante 1 · Conto de animais"),
    ("31", "sage", "std", "Estante 1 · Conto de animais"),
    ("32", "sage", "std", "Estante 1 · Conto de animais"),
    ("33", "sage", "std", "Estante 1 · Conto de animais"),
    ("34", "sage", "std", "Estante 1 · Conto de animais"),
    ("35", "sage", "std", "Estante 1 · Conto de animais"),
    ("36", "yel", "std", "Estante 2 · Conto tradicional"),
    ("37", "yel", "std", "Estante 2 · Conto tradicional"),
    ("38", "yel", "std", "Estante 2 · Conto tradicional"),
    ("39", "yel", "std", "Estante 2 · Conto tradicional"),
    ("40", "yel", "std", "Estante 2 · Conto tradicional"),
    ("41", "yel", "std", "Estante 2 · Conto tradicional"),
    ("42", "blue", "std", "Estante 3 · António Torrado"),
    ("43", "blue", "std", "Estante 3 · António Torrado"),
    ("44", "blue", "std", "Estante 3 · António Torrado"),
    ("45", "blue", "std", "Estante 3 · António Torrado"),
    ("46", "blue", "std", "Estante 3 · António Torrado"),
    ("47", "blue", "std", "Estante 3 · António Torrado"),
    ("48", "red", "std", "Estante 4 · Jorge Amado"),
    ("49", "red", "std", "Estante 4 · Jorge Amado"),
    ("50", "red", "std", "Estante 4 · Jorge Amado"),
    ("51", "red", "std", "Estante 4 · Jorge Amado"),
    ("52", "red", "std", "Estante 4 · Jorge Amado"),
    ("53", "red", "std", "Estante 4 · Jorge Amado"),
    ("54", "teal", "std", "Estante 5 · Um conto de Cabo Verde"),
    ("55", "teal", "std", "Estante 5 · Um conto de Cabo Verde"),
    ("56", "teal", "std", "Estante 5 · Um conto de Cabo Verde"),
    ("57", "teal", "std", "Estante 5 · Um conto de Cabo Verde"),
    ("58", "teal", "std", "Estante 5 · Um conto de Cabo Verde"),
    ("59", "teal", "std", "Estante 5 · Um conto de Cabo Verde"),
    ("60", "orng", "std", "Estante 6 · O diário"),
    ("61", "orng", "std", "Estante 6 · O diário"),
    ("62", "orng", "std", "Estante 6 · O diário"),
    ("63", "orng", "std", "Estante 6 · O diário"),
    ("64", "orng", "std", "Estante 6 · O diário"),
    ("65", "orng", "std", "Estante 6 · O diário"),
    ("66", "plum", "std", "Estante 7 · A aventura"),
    ("67", "plum", "std", "Estante 7 · A aventura"),
    ("68", "plum", "std", "Estante 7 · A aventura"),
    ("69", "plum", "std", "Estante 7 · A aventura"),
    ("70", "plum", "std", "Estante 7 · A aventura"),
    ("71", "plum", "std", "Estante 7 · A aventura"),
    ("72", "sage", "std", "Unidade 2 · Já consigo…"),
    ("73", "plum", "std", "Notas para o professor · Unidade 2"),
    ("74", "plum", "std", "Notas para o professor · Unidade 2"),
    ("75", "plum", "std", "Notas para o professor · Unidade 2"),
    ("76", "plum", "std", "Notas para o professor · Unidade 2"),
    ("77", "teal", "full", ""),
    ("78", "teal", "std", "Unidade 3 · O mapa da unidade"),
    ("79", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("80", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("81", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("82", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("83", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("84", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("85", "red", "std", "Varal 1 · Lengalengas e quadras"),
    ("86", "plum", "std", "Varal 2 · Um poema sobre um sentimento"),
    ("87", "plum", "std", "Varal 2 · Um poema sobre um sentimento"),
    ("88", "plum", "std", "Varal 2 · Um poema sobre um sentimento"),
    ("89", "plum", "std", "Varal 2 · Um poema sobre um sentimento"),
    ("90", "plum", "std", "Varal 2 · Um poema sobre um sentimento"),
    ("91", "plum", "std", "Varal 2 · Um poema sobre um sentimento"),
    ("92", "blue", "std", "Varal 3 · Um poema sobre o mar"),
    ("93", "blue", "std", "Varal 3 · Um poema sobre o mar"),
    ("94", "blue", "std", "Varal 3 · Um poema sobre o mar"),
    ("95", "blue", "std", "Varal 3 · Um poema sobre o mar"),
    ("96", "blue", "std", "Varal 3 · Um poema sobre o mar"),
    ("97", "blue", "std", "Varal 3 · Um poema sobre o mar"),
    ("98", "sage", "std", "Unidade 3 · Já consigo…"),
    ("99", "plum", "std", "Notas para o professor · Unidade 3"),
    ("100", "plum", "std", "Notas para o professor · Unidade 3"),
    ("101", "orng", "full", ""),
    ("102", "orng", "std", "Unidade 4 · O mapa da unidade"),
    ("103", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("104", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("105", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("106", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("107", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("108", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("109", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("110", "blue", "std", "Cena 1 · A Lua no chafariz"),
    ("111", "sage", "std", "Cena 2 · Na escola"),
    ("112", "sage", "std", "Cena 2 · Na escola"),
    ("113", "sage", "std", "Cena 2 · Na escola"),
    ("114", "sage", "std", "Cena 2 · Na escola"),
    ("115", "sage", "std", "Cena 2 · Na escola"),
    ("116", "sage", "std", "Cena 2 · Na escola"),
    ("117", "sage", "std", "Cena 2 · Na escola"),
    ("118", "sage", "std", "Cena 2 · Na escola"),
    ("119", "orng", "std", "Unidade 4 · A nossa peça"),
    ("120", "sage", "std", "Unidade 4 · Já consigo…"),
    ("121", "plum", "std", "Notas para o professor · Unidade 4"),
    ("122", "plum", "std", "Notas para o professor · Unidade 4"),
    ("123", "red", "full", ""),
    ("124", "red", "std", "Unidade 5 · O mapa do tesouro"),
    ("125", "blue", "std", "Pista 1 · A notícia"),
    ("126", "blue", "std", "Pista 1 · A notícia"),
    ("127", "red", "std", "Pista 2 · A carta"),
    ("128", "red", "std", "Pista 2 · A carta"),
    ("129", "yel", "std", "Pista 3 · O convite"),
    ("130", "yel", "std", "Pista 3 · O convite"),
    ("131", "sage", "std", "Pista 4 · A banda desenhada"),
    ("132", "sage", "std", "Pista 4 · A banda desenhada"),
    ("133", "plum", "std", "Pista 5 · O conto"),
    ("134", "plum", "std", "Pista 5 · O conto"),
    ("135", "orng", "std", "Pista 6 · O diário"),
    ("136", "orng", "std", "Pista 6 · O diário"),
    ("137", "teal", "std", "Pista 7 · O poema"),
    ("138", "teal", "std", "Pista 7 · O poema"),
    ("139", "blue", "std", "Pista 8 · A cena"),
    ("140", "blue", "std", "Pista 8 · A cena"),
    ("141", "red", "std", "Unidade 5 · O Jogo da Rua"),
    ("142", "sage", "std", "Unidade 5 · Já consigo…"),
    ("143", "plum", "std", "Notas para o professor · Unidade 5"),
    ("144", "plum", "std", "Notas para o professor · Unidade 5"),
    ("145", "plum", "std", "Notas para o professor · Unidade 5"),
    ("146", "blue", "full", ""),
    ("147", "blue", "std", "Unidade 6 · Mostra o que sabes"),
    ("148", "teal", "std", "Prova 1 · Ler em voz alta"),
    ("149", "teal", "std", "Prova 1 · Ler em voz alta"),
    ("150", "plum", "std", "Prova 2 · Uma narrativa revista"),
    ("151", "plum", "std", "Prova 2 · Uma narrativa revista"),
    ("152", "plum", "std", "Prova 2 · Uma narrativa revista"),
    ("153", "orng", "std", "Prova 3 · A minha opinião"),
    ("154", "red", "std", "Prova 4 · Os tempos dos verbos"),
    ("155", "red", "std", "Prova 4 · Os tempos dos verbos"),
    ("156", "sage", "std", "Unidade 6 · Aprendo com os meus erros"),
    ("157", "plum", "std", "Notas para o professor · Unidade 6"),
    ("158", "sage", "full", ""),
    ("159", "sage", "std", "Unidade 7 · O meu projeto de leitura"),
    ("160", "sage", "std", "Unidade 7 · A minha estante"),
    ("161", "sage", "std", "Unidade 7 · Ficha de leitura"),
    ("162", "sage", "std", "Unidade 7 · Ficha de leitura"),
    ("163", "sage", "std", "Unidade 7 · Recomendo!"),
    ("164", "sage", "std", "Unidade 7 · Livros para o 3.º ano"),
    ("165", "sage", "std", "Unidade 7 · Diploma de leitor"),
    ("166", "plum", "std", "Glossário"),
    ("167", "plum", "std", "Glossário"),
    ("168", "red", "full", ""),
]

ICONS = {
    "ouvir":   '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4" height="7" rx="1.5"/><rect x="17" y="14" width="4" height="7" rx="1.5"/>',
    "falar":   '<path d="M4 4h16v11H10l-5 4.5V15H4z"/><path d="M8 9h8M8 12h5"/>',
    "ler":     '<path d="M3 5.5c3-1.2 6-1 9 1 3-2 6-2.2 9-1V19c-3-1.2-6-1-9 1-3-2-6-2.2-9-1z"/><path d="M12 6.5V20"/>',
    "escrever":'<path d="M4 20l1.2-4.4L16 4.8l3.2 3.2L8.4 18.8z"/><path d="M14 6.8l3.2 3.2"/><path d="M4 20h7"/>',
    "desenhar":'<path d="M20 3.5l.5.5-8.2 9.6-1.9-1.9z"/><path d="M10 12c-3 0-4.2 2-4.2 4.1 0 1.7-1.3 2.8-2.8 2.9 3.2 2 8.6 1.3 9.3-3.5z"/>',
    "pares":   '<circle cx="8" cy="8" r="3"/><circle cx="16.5" cy="8" r="3"/><path d="M2.5 20c0-3.6 2.5-6 5.5-6s5.5 2.4 5.5 6"/><path d="M13 14.4c.9-.3 2.2-.4 3.5-.4 3 0 5.5 2.4 5.5 6"/>',
    "grupo":   '<circle cx="12" cy="7" r="2.8"/><circle cx="5" cy="10" r="2.3"/><circle cx="19" cy="10" r="2.3"/><path d="M7 20c0-3.4 2.2-5.6 5-5.6s5 2.2 5 5.6"/><path d="M1.5 19c0-2.6 1.5-4.4 3.5-4.4 1 0 1.8.3 2.4.9"/><path d="M22.5 19c0-2.6-1.5-4.4-3.5-4.4-1 0-1.8.3-2.4.9"/>',
    "qr":      '<rect x="6.5" y="2" width="11" height="20" rx="2.2"/><path d="M10.5 18.5h3"/><rect x="9" y="6" width="2.5" height="2.5"/><rect x="12.5" y="9.5" width="2.5" height="2.5"/><rect x="9" y="11" width="1.5" height="1.5"/>',
    "carta":   '<rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "convite": '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M12 7.5l1.3 2.7 3 .4-2.2 2 .6 3-2.7-1.5-2.7 1.5.6-3-2.2-2 3-.4z"/>',
    "noticia": '<path d="M4 5h13v14H6.2A2.2 2.2 0 0 1 4 16.8z"/><path d="M17 8.5h3v8.5a2 2 0 0 1-2 2h-1"/><path d="M7 9h7M7 12h7M7 15h4"/>',
    "bd":      '<rect x="3" y="3.5" width="8" height="8" rx="1"/><rect x="13" y="3.5" width="8" height="8" rx="1"/><rect x="3" y="13.5" width="18" height="7" rx="1"/>',
    "jornal":  '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M6 8h12M6 11.5h5M6 15h5M13.5 11.5H18V16h-4.5z"/>',
    "jogo":    '<rect x="4" y="4" width="16" height="16" rx="3.5"/><circle cx="8.5" cy="8.5" r=".9" fill="currentColor"/><circle cx="15.5" cy="15.5" r=".9" fill="currentColor"/><circle cx="12" cy="12" r=".9" fill="currentColor"/><circle cx="15.5" cy="8.5" r=".9" fill="currentColor"/><circle cx="8.5" cy="15.5" r=".9" fill="currentColor"/>',
    "gram":    '<path d="M5 19L10 5h1.5l5 14"/><path d="M7 14h8"/><circle cx="19.5" cy="18.5" r="1.4"/>',
    "estrela": '<path d="M12 3.5l2.5 5.2 5.7.8-4.1 4 1 5.7-5.1-2.7-5.1 2.7 1-5.7-4.1-4 5.7-.8z"/>',
    "star":    '<path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3-4.6-4.4 6.3-.9z" fill="currentColor" stroke="none"/>',
    "olho":    '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
}

FACES = {
    "f1": '<circle cx="12" cy="12" r="10" fill="#FBEBC0"/><circle cx="8.5" cy="10" r="1.2" fill="#1F2A44"/><circle cx="15.5" cy="10" r="1.2" fill="#1F2A44"/><path d="M8 16.5c2.4-1.6 5.6-1.6 8 0" stroke="#1F2A44" stroke-width="1.6" fill="none" stroke-linecap="round"/>',
    "f2": '<circle cx="12" cy="12" r="10" fill="#FBEBC0"/><circle cx="8.5" cy="10" r="1.2" fill="#1F2A44"/><circle cx="15.5" cy="10" r="1.2" fill="#1F2A44"/><path d="M8 15.5h8" stroke="#1F2A44" stroke-width="1.6" fill="none" stroke-linecap="round"/>',
    "f3": '<circle cx="12" cy="12" r="10" fill="#FBEBC0"/><circle cx="8.5" cy="10" r="1.2" fill="#1F2A44"/><circle cx="15.5" cy="10" r="1.2" fill="#1F2A44"/><path d="M7.5 14c2.2 3.2 6.8 3.2 9 0" stroke="#1F2A44" stroke-width="1.6" fill="none" stroke-linecap="round"/>',
}

SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + "".join(
    f'<symbol id="{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in FACES.items()) + "</svg>"

CHECK_JS = r"""
<script>
window.addEventListener('load', () => { setTimeout(() => {
  const out = [];
  document.querySelectorAll('.page').forEach((pg, i) => {
    const pr = pg.getBoundingClientRect();
    const inner = pg.querySelector('.inner');
    if (inner) {
      const r = inner.getBoundingClientRect();
      if (inner.scrollHeight > inner.clientHeight + 2) out.push(`${pg.id}: inner overflow ${inner.scrollHeight - inner.clientHeight}px`);
      inner.querySelectorAll('*').forEach(el => {
        const e = el.getBoundingClientRect();
        if (e.width === 0 || getComputedStyle(el).position === 'absolute') return;
        if (e.bottom > r.bottom + 2 || e.right > r.right + 2) out.push(`${pg.id}: <${el.tagName.toLowerCase()} class="${el.className && el.className.baseVal === undefined ? el.className : ''}"> past box by ${Math.round(Math.max(e.bottom-r.bottom, e.right-r.right))}px`);
      });
    }
    pg.querySelectorAll('.fit').forEach(el => {
      if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
        out.push(`${pg.id}: .fit overflow (${el.scrollWidth-el.clientWidth}x${el.scrollHeight-el.clientHeight}) ${el.textContent.trim().slice(0,40)}`);
    });
  });
  document.querySelectorAll('.page .inner').forEach(inn => {
    if (inn.scrollHeight > inn.clientHeight + 1) {
      const pid = inn.parentElement.id;
      out.push(pid + ' HEIGHTS: ' + [...inn.children].map(k => (k.className||k.tagName) + '=' + (k.getBoundingClientRect().height/3.7795).toFixed(1)).join(' | '));
    }
  });
  document.querySelectorAll('.page .inner').forEach(inn => {
    const pid = inn.parentElement.id;
    const kids = [...inn.children].filter(k => k.tagName !== 'STYLE');
    for (let i = 1; i < kids.length; i++) {
      const a = kids[i-1].getBoundingClientRect(), b = kids[i].getBoundingClientRect();
      if (a.bottom > b.top + 1) out.push(pid + ' OVERLAP: ' + kids[i-1].className + ' over ' + kids[i].className + ' by ' + Math.round(a.bottom-b.top) + 'px');
    }
    inn.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (!/(block|grid|flex)/.test(cs.display) || cs.overflow !== 'visible' || el.clientHeight < 5) return;
      if (el.closest('svg')) return;
      if (el.scrollHeight > el.clientHeight + 3) out.push(pid + ' SPILL: ' + el.tagName + '.' + el.className + ' content ' + (el.scrollHeight - el.clientHeight) + 'px taller than box');
    });
  });
  const pre = document.createElement('pre'); pre.id = 'overflow-report';
  pre.textContent = JSON.stringify(out); document.body.appendChild(pre);
}, 400); });
</script>"""


def stars(n):
    return '<span class="stars" title="' + "★" * 0 + f'nível {n}">' + "".join(
        f'<svg class="{"on" if k < n else "off"}" viewBox="0 0 24 24"><use href="#i-star"/></svg>' for k in range(3)) + "</span>"


def expand(html):
    html = re.sub(r"\{\{s([123])\}\}", lambda m: stars(int(m.group(1))), html)
    # {{lines:N}} or {{lines:N:8}} -> N ruled writing lines (default pitch 10 mm)
    def lines(m):
        n = int(m.group(1)); pitch = m.group(2) or "10"
        return f'<div class="wl" style="--lp:{pitch}mm">' + '<div class="ln"></div>' * n + "</div>"
    return re.sub(r"\{\{lines:(\d+)(?::(\d+(?:\.\d+)?))?\}\}", lines, html)


def assemble(bleed: bool, only=None, check=False):
    parts = []
    for i, (frag, col, kind, label) in enumerate(PAGES, start=1):
        if only and i not in only:
            continue
        html = expand((HERE / "pages" / f"{frag}.html").read_text(encoding="utf-8"))
        side = "odd" if i % 2 else "even"
        style = f"--c:var(--{col});--ct:var(--{col}-t)"
        if kind == "full":
            parts.append(f'<section class="page {side} full" id="p{i}" style="{style}">{html}</section>')
        else:
            folio = f'<div class="folio"><b>{i}</b><span class="route"></span><span>{label}</span></div>'
            parts.append(f'<section class="page {side}" id="p{i}" style="{style}"><div class="inner">{html}</div>{folio}</section>')
    bleed_css = "<style>:root{--b:3mm}</style>" if bleed else ""
    return ("<!doctype html><html lang=\"pt-PT\"><head><meta charset=\"utf-8\">"
            "<title>Rua das Palavras</title>"
            f'<link rel="stylesheet" href="style.css">{bleed_css}</head><body>{SPRITE}'
            + "".join(parts) + (CHECK_JS if check else "") + "</body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bleed", action="store_true")
    ap.add_argument("--pages", default="")
    ap.add_argument("--dpi", type=int, default=70)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    only = {int(x) for x in a.pages.split(",") if x} or None
    name = a.out or ("unit1-print" if a.bleed else "unit1")
    html_path = HERE / f"{name}.html"
    pdf_path = HERE / f"{name}.pdf"

    # 1) overflow check (DOM dump)
    chk = HERE / f"{name}.check.html"
    chk.write_text(assemble(a.bleed, only, check=True), encoding="utf-8")
    dom = subprocess.run([str(CHROME), "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                          "--window-size=1400,1200", "--virtual-time-budget=6000", "--dump-dom", chk.as_uri()],
                         capture_output=True, text=True, timeout=180).stdout
    m = re.search(r'<pre id="overflow-report">(.*?)</pre>', dom, re.S)
    report = json.loads(m.group(1).replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")) if m else ["NO REPORT"]
    chk.unlink()

    # 2) PDF
    html_path.write_text(assemble(a.bleed, only), encoding="utf-8")
    subprocess.run([str(CHROME), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   capture_output=True, text=True, timeout=300, check=True)

    # 3) renders
    import pymupdf
    doc = pymupdf.open(pdf_path)
    rdir = ROOT / "renders" / name
    rdir.mkdir(parents=True, exist_ok=True)
    nums = sorted(only) if only else list(range(1, len(PAGES) + 1))
    for idx, page in enumerate(doc):
        n = nums[idx] if idx < len(nums) else idx + 1
        page.get_pixmap(dpi=a.dpi).save(rdir / f"p{n:02d}.png")
    fonts = sorted({f[3] for p in doc for f in p.get_fonts()})
    sizes = {(round(p.rect.width / 72 * 25.4, 1), round(p.rect.height / 72 * 25.4, 1)) for p in doc}
    print(json.dumps({"pdf": str(pdf_path), "pages": doc.page_count, "sizes_mm": sorted(sizes),
                      "fonts": fonts, "overflow": report}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
