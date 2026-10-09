import parts
from parts import *
parts.UNIT.update(n=1, total=28)

P = {}
rows = [
  ("0", "Ponto de partida", "Avaliação diagnóstica", "6 páginas", "var(--coral)", True),
  ("1", "Informar ou convencer?", "Textos expositivos e de opinião", "7 de 28 páginas", "var(--ink)", True),
  ("3", "Vozes que o tempo guardou", "Romance tradicional e texto poético", "16 páginas", "var(--coral)", True),
  ("4", "O palco das escolhas", "Texto dramático", "16 páginas", "var(--ink)", True),
  ("5", "O ano num só mapa", "Revisões anuais", "12 páginas", "var(--sea)", True),
]
todo = [("1", "Informar ou convencer? — páginas 8 a 28"),
        ("2", "Texto narrativo — mitos, clássicos e autores"), ("6", "Avaliação"),
        ("7", "Projeto de leitura autónoma")]
rh = "".join(f'''<div style="display:grid;grid-template-columns:22mm 1fr auto;gap:5mm;align-items:center;padding:3.8mm 0;border-bottom:.6pt solid var(--rule)">
  <div class="display" style="font-size:34pt;line-height:.9;color:{c}">{n}</div>
  <div><div style="font-family:FrauncesText;font-weight:700;font-size:14pt;color:var(--ink)">{t}</div><div class="small muted" style="margin-top:.8mm">{s}</div></div>
  <div class="kicker" style="color:{c}">{p}</div></div>''' for n, t, s, p, c, _ in rows)
th = "".join(f'<div style="display:grid;grid-template-columns:22mm 1fr;gap:5mm;padding:2.2mm 0;font-size:10pt"><b class="muted">Unidade {n}</b><span>{t}</span></div>' for n, t in todo)
P[8] = page(8, f'''
<div class="kicker">Esta edição</div>
<h1 style="font-size:34pt;margin-top:2mm">Farol · Português 6</h1>
<p class="lead" style="margin-top:3mm;font-size:12pt">Edição de pré-visualização. Reúne as unidades já concluídas do manual, pela ordem em que aparecem no livro. Cada unidade tem a sua própria numeração de páginas.</p>
<div style="margin-top:7mm;border-top:1.2mm solid var(--ink)">{rh}</div>
<div class="panel" style="margin-top:9mm">
  <div class="kicker">Em preparação</div>
  <div style="margin-top:2mm">{th}</div>
</div>
<p class="src" style="margin-top:auto">Prime School · Manual do aluno · Português 6.º ano</p>
''', rh=False, tide=False)
