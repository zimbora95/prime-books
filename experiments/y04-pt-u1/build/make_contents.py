import pathlib, re, html
B = pathlib.Path('/root/prime-books/experiments/y04-pt-u1/build')
s = (B / 'build.py').read_text()
rows = re.findall(r'^    \("(\d+)", "(\w+)", *"(\w+)", *"([^"]*)"\)', s, re.M)
TOTAL = len(rows)
# group by running label
groups = []
for n, c, k, l in rows:
    n = int(n)
    key = l if k != 'full' else f'OPENER{n}'
    if groups and groups[-1]['key'] == key:
        groups[-1]['b'] = n
    else:
        groups.append(dict(key=key, a=n, b=n, col=c, kind=k, label=l))
UNITS = [
    (1, 'red', 'Mensagens na Rua do Limoeiro', 'Textos do quotidiano: a carta, o convite, a notícia e a banda desenhada'),
    (2, 'plum', 'Histórias da Pequena Biblioteca', 'Texto narrativo: autores para a infância e tradição popular'),
    (3, 'teal', 'A Rua que Rima', 'Texto poético: lengalengas, quadras e poemas'),
    (4, 'orng', 'A Rua Sobe ao Palco', 'Texto dramático: duas cenas para ler e representar'),
    (5, 'red', 'A Caça ao Tesouro da Rua', 'Revisões do ano: oito pistas, oito tipos de texto'),
    (6, 'blue', 'Mostra o que Sabes', 'Avaliação: ler, escrever, opinar e usar os verbos'),
    (7, 'sage', 'Leitores de Verão', 'Atividades extra: o meu projeto de leitura'),
]
openers = [g['a'] for g in groups if g['kind'] == 'full'][1:8]  # skip front cover
ranges = []
for i, a in enumerate(openers):
    b = openers[i + 1] - 1 if i + 1 < len(openers) else next(g['a'] for g in groups if g['label'] == 'Glossário') - 1
    ranges.append((a, b))

def short(l):
    l = re.sub(r'^Unidade \d · ', '', l)
    return l

def items(a, b):
    out = []
    for g in groups:
        if a < g['a'] <= b and g['kind'] != 'full':
            lab = short(g['label'])
            if lab.startswith('Notas para o professor'): lab = 'Notas para o professor'
            out.append((lab, g['a'], g['col']))
    return out

def card(u):
    n, col, title, sub = UNITS[u - 1]
    a, b = ranges[u - 1]
    li = ''.join(f'<li><span class="t">{html.escape(t)}</span><span class="dots"></span><span class="pg">{p}</span></li>' for t, p, c in items(a, b))
    return f'''<div class="uc" style="--k:var(--{col});--kt:var(--{col}-t)">
  <div class="uh"><span class="un">{n}</span><div class="ut"><b>{title}</b><span>{sub}</span></div><span class="ur">pp. {a}–{b}</span></div>
  <ul>{li}</ul>
</div>'''

def bar(active):
    segs = ''
    for i, (n, col, t, s_) in enumerate(UNITS):
        a, b = ranges[i]
        w = b - a + 1
        segs += f'<span style="flex:{w};background:var(--{col});opacity:1"></span>'
    return f'<div class="cbar">{segs}</div>'

CSS = '''<style>
#pN .cbar { display: flex; height: 4mm; border-radius: 2mm; overflow: hidden; gap: .8mm; }
#pN .ucs { display: flex; flex-direction: column; gap: 3.2mm; flex: 1; }
#pN .uc { background: var(--kt); border-radius: 4mm; padding: 3mm 4.5mm 3.2mm; border-left: 2.2mm solid var(--k); }
#pN .uh { display: grid; grid-template-columns: 11mm 1fr auto; gap: 3mm; align-items: center; margin-bottom: 1.8mm; }
#pN .un { width: 10mm; height: 10mm; border-radius: 50%; background: var(--k); color: #fff; font-family: "FrX"; font-size: 16pt; display: grid; place-items: center; }
#pN .ut b { display: block; font-family: "FrS"; font-weight: 400; font-size: 16pt; line-height: 1.1; }
#pN .ut span { font-size: 10.5pt; color: var(--ink2); }
#pN .ur { font-size: 11pt; font-weight: 700; color: var(--ink); white-space: nowrap; }
#pN .uc ul { list-style: none; padding: 0; margin: 0; column-count: 2; column-gap: 8mm; font-size: 11pt; line-height: 1.5; }
#pN .uc li { display: flex; align-items: flex-end; gap: 1.5mm; break-inside: avoid; }
#pN .uc .t { min-width: 0; }
#pN .uc .dots { flex: 1; border-bottom: .8pt dotted #b9a888; transform: translateY(-1mm); min-width: 3mm; }
#pN .uc .pg { font-weight: 700; min-width: 7mm; text-align: right; }
#pN .extra { display: grid; grid-template-columns: 1.3fr 1fr 1.2fr; gap: 3mm; }
#pN .extra div { background: #fff; border-radius: 3mm; padding: 2.4mm 4mm; font-size: 11pt; display: flex; justify-content: space-between; gap: 2mm; white-space: nowrap; }
#pN .extra b { font-weight: 700; }
</style>
'''
gl = next(g['a'] for g in groups if g['label'] == 'Glossário')
cr = 2
p3 = f'''<div class="head">
  <h1>Índice</h1>
  <p class="lede">Sete unidades, um ano inteiro na Rua do Limoeiro. Cada unidade tem a sua cor: procura-a no alto de cada página.</p>
</div>
{bar({1, 2, 3})}
<div class="ucs">{''.join(card(u) for u in (1, 2, 3))}</div>
''' + CSS.replace('#pN', '#p4') + '<style>#p4 .ucs { gap: 5mm; } #p4 .uc { padding: 4mm 5mm 4.5mm; } #p4 .uc ul { font-size: 12pt; line-height: 1.6; } #p4 .uh { margin-bottom: 2.5mm; }</style>\n'
p4 = f'''<div class="head">
  <h1>Índice <span style="font-size:.6em;color:var(--ink2)">(continuação)</span></h1>
  <p class="lede">No fim do livro encontras o glossário, com as palavras que usámos para falar de textos e de gramática.</p>
</div>
{bar({4, 5, 6, 7})}
<div class="ucs">{''.join(card(u) for u in (4, 5, 6, 7))}
  <div class="extra"><div><span>Imprint</span><b>2</b></div><div><span>Bem-vindo à Rua do Limoeiro</span><b>3</b></div><div><span>Glossário</span><b>{gl}</b></div></div>
</div>
''' + CSS.replace('#pN', '#p5')
(B / 'pages' / '04.html').write_text(p3)
(B / 'pages' / '05.html').write_text(p4)
print(TOTAL, ranges, gl, cr)
