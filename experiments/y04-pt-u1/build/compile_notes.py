#!/usr/bin/env python3
"""Compile the builders' notes/*.md into the teacher-notes pages of Units 2–5."""
import html, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
N = ROOT / 'notes'; P = ROOT / 'build' / 'pages'

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'`(.+?)`', r'\1', s)
    return s

def md(text, top_class='sec'):
    out, lst, para, tbl = [], None, [], []
    def flush_para():
        if para: out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    def flush_list():
        nonlocal lst
        if lst: out.append(f'<{lst[0]}>' + ''.join(f'<li>{inline(x)}</li>' for x in lst[1]) + f'</{lst[0]}>'); lst = None
    def flush_tbl():
        if tbl:
            rows = [r for r in tbl if not re.fullmatch(r'\|?[\s:|-]+\|?', r)]
            h = ''
            for i, r in enumerate(rows):
                cells = [c.strip() for c in r.strip().strip('|').split('|')]
                tag = 'th' if i == 0 else 'td'
                h += '<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>'
            out.append(f'<table>{h}</table>'); tbl.clear()
    for line in text.splitlines():
        s = line.rstrip()
        if s.startswith('|'):
            flush_para(); flush_list(); tbl.append(s); continue
        flush_tbl()
        if not s.strip():
            flush_para(); flush_list(); continue
        m = re.match(r'^(#{1,4})\s+(.*)', s)
        if m:
            flush_para(); flush_list()
            lvl = len(m.group(1))
            out.append(f'<h2 class="{top_class}">{inline(m.group(2))}</h2>' if lvl == 1 else f'<h3>{inline(m.group(2))}</h3>')
            continue
        m = re.match(r'^\s*(?:[-*]|(\d+)\.)\s+(.*)', s)
        if m:
            flush_para()
            kind = 'ol' if m.group(1) else 'ul'
            if not lst or lst[0] != kind: flush_list(); lst = (kind, [])
            lst[1].append(m.group(2)); continue
        if lst and line.startswith('  '):
            lst[1][-1] += ' ' + s.strip(); continue
        flush_list(); para.append(s.strip())
    flush_para(); flush_list(); flush_tbl()
    return '\n'.join(out)

REF = re.compile(r'(?P<w>\b(?:pp?\.|[Pp]áginas?)\s?)(?P<a>\d{1,3})(?P<rest>(?:\s?[–-]\s?\d{1,3}|\s(?:e|a)\s\d{1,3})?)')
def sh(n):
    n = int(n); return n + (1 if n > 72 else 0) + (1 if n > 140 else 0)
def prep(t):
    def r(m):
        rest = re.sub(r'\d{1,3}', lambda k: str(sh(k.group())), m.group('rest'))
        return f"{m.group('w')}{sh(m.group('a'))}{rest}"
    t = REF.sub(r, t)
    t = re.sub(r'^## (Objetivos|Sessões|Sessões sugeridas)\b.*$', lambda m: '## ' + ('Objetivos' if m.group(1) == 'Objetivos' else 'Sessões sugeridas (60 min)'), t, flags=re.M)
    t = re.sub(r'^## Recursos.*?(?=^## |\Z)', '', t, flags=re.M | re.S)
    return t

def page(title, intro, files, first):
    body = ''
    if first:
        body += f'''<div class="head">
    <span class="stop"><i><svg class="ico" style="width:4.6mm;height:4.6mm;stroke:var(--plum)"><use href="#i-ler"/></svg></i>Notas para o professor</span>
    <h1 style="font-size:24pt">{title}</h1>
  </div>
  <p class="intro">{intro}</p>'''
    cols = '\n'.join(md(prep((N / f).read_text())) for f in files)
    return f'''<div class="tn">
  {body}
  <div class="cols">
{cols}
  </div>
</div>
'''

STY = '''<style>
#pN .tn {{ display: flex; flex-direction: column; gap: 2.5mm; height: 100%; }}
#pN .tn .intro {{ font-size: 10.5pt; line-height: 1.38; background: var(--plum-t); border-radius: 3mm; padding: 2.5mm 4mm; }}
#pN .tn .cols {{ font-size: {fs}pt; line-height: 1.3; column-count: 2; column-gap: 6mm; column-fill: balance; }}
#pN .tn .cols h2.sec {{ font-family: "FrS"; font-size: 12.5pt; color: var(--plum); margin: 2mm 0 1mm; break-after: avoid; }}
#pN .tn .cols h3 {{ font-size: {h3}pt; margin: 1.6mm 0 .6mm; break-after: avoid; }}
#pN .tn .cols p, #pN .tn .cols li {{ margin: 0 0 .7mm; }}
#pN .tn .cols ul, #pN .tn .cols ol {{ padding-left: 4mm; margin: 0 0 .8mm; }}
#pN .tn .cols table {{ font-size: {tf}pt; margin-bottom: 1mm; }}
</style>
'''

UNITS = {
 2: ('Unidade 2 · Histórias da Pequena Biblioteca', 'A unidade organiza o texto narrativo em <b>sete estantes</b> de seis páginas: fábula, conto popular português, dois autores de referência (António Torrado e Jorge Amado), um conto da tradição oral de Cabo Verde, um diário e uma aventura. Em cada estante: ler → compreender → contar → gramática → escrever. As obras protegidas por direitos de autor (Torrado, Amado) não são reproduzidas: o professor lê-as a partir das edições originais. Tempo previsto: <b>cerca de 30 sessões de 60 minutos</b>. Autoavaliação na p. 69.',
     [['u2-e1.md'], ['u2-e2.md', 'u2-e3.md'], ['u2-e4.md', 'u2-e5.md'], ['u2-e6.md', 'u2-e7.md']], [70, 71, 72, 73]),
 3: ('Unidade 3 · A Rua que Rima', 'O texto poético em <b>três varais</b>: lengalengas e quadras da tradição popular; um poema sobre um sentimento, escolhido pelo professor em <i>As Fadas Verdes</i> (Matilde Rosa Araújo) ou em <i>Poemas da Mentira e da Verdade</i> (Luísa Ducla Soares), que os alunos copiam à mão (os poemas não são reproduzidos por direitos de autor); e um poema original sobre o mar, para leitura em coro, com áudio. Rima, verso, estrofe, sílaba tónica e leitura expressiva. Tempo previsto: <b>cerca de 14 sessões</b>. Autoavaliação na p. 95.',
     [['u3-v1.md'], ['u3-v2.md', 'u3-v3.md']], [96, 97]),
 4: ('Unidade 4 · A Rua Sobe ao Palco', 'O texto dramático em <b>duas cenas originais</b>: «A Lua no chafariz» e «Na escola». Os alunos leem, distribuem papéis, ensaiam e representam; identificam falas, indicações cénicas e a pontuação própria do texto dramático; transformam narração em diálogo e vice-versa. A unidade termina com o espetáculo e o cartaz da peça (p. 116). Tempo previsto: <b>cerca de 16 sessões</b>. Autoavaliação na p. 117.',
     [['u4-c1.md'], ['u4-c2.md']], [118, 119]),
 5: ('Unidade 5 · A Caça ao Tesouro da Rua', 'Revisão anual em <b>oito pistas</b>, uma por tipo de texto do ano (notícia, carta, convite, banda desenhada, conto, diário, poema e cena). Cada pista traz um texto novo, leitura, gramática e uma escrita curta, e dá uma letra da palavra secreta (LIMOEIRO), registada no passaporte da p. 121. O Jogo da Rua (p. 138) revê o ano em grupo. Tempo previsto: <b>cerca de 18 sessões</b>. Autoavaliação na p. 139.',
     [['u5-a.md'], ['u5-b.md', 'u5-c.md'], ['u5-d.md']], [140, 141, 142]),
}

def write(fs=9.2, h3=9.6, tf=8.6, only=None):
    for u, (title, intro, groups, nums) in UNITS.items():
        if only and u not in only: continue
        for i, (files, n) in enumerate(zip(groups, nums)):
            t = page(title, intro, files, i == 0)
            if i > 0:
                t = t.replace('<div class="tn">', f'<div class="tn">\n  <h2 style="font-family:\'FrS\';font-size:15pt;color:var(--plum)">{title} (continuação)</h2>', 1)
            (P / f'{n}.html').write_text(t + STY.format(fs=fs, h3=h3, tf=tf).replace('#pN', f'#p{n}'))
            print('wrote', n)

if __name__ == '__main__':
    fs = float(sys.argv[1]) if len(sys.argv) > 1 else 9.2
    write(fs=fs, h3=fs + .4, tf=fs - .6)
