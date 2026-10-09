from parts import *

P = {}

# ---------------------------------------------------------------- 1 COVER
P[1] = page(1, '''
<div class="full" style="background:#F2E4D0"><img class="cover" src="img/capa2.jpg" style="object-position:50% 100%"></div>
<div class="abs" style="left:23.5mm;right:16mm;top:15mm;display:flex;justify-content:space-between;align-items:center">
  <div style="font-family:Grotesk;font-weight:700;letter-spacing:.34em;font-size:9pt;color:var(--ink)">FAROL</div>
  <div style="font-family:Grotesk;font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--ink)">Português · 6.º ano</div>
</div>
<div class="abs" style="left:23.5mm;right:16mm;top:31mm">
  <div class="kicker">Unidade 1</div>
  <h1 style="font-size:58pt;line-height:.9;margin-top:3mm">Informar<br><em>ou</em> convencer?</h1>
  <div style="width:26mm;height:1.2mm;background:var(--coral);margin-top:7mm"></div>
  <div style="font-family:Grotesk;font-weight:500;font-size:9.6pt;letter-spacing:.03em;color:var(--ink);margin-top:4mm;max-width:130mm;line-height:1.5">Texto expositivo · Texto de divulgação · Entrevista<br>Texto de opinião · Conjunções e conectores</div>
</div>
<div class="abs" style="left:23.5mm;bottom:12mm;font-family:Grotesk;font-size:7pt;letter-spacing:.18em;text-transform:uppercase;color:#fff">Prime School · Manual do aluno</div>
''', bleed=True, rh=False, tide=False)

# ---------------------------------------------------------------- 2 MAP OF THE UNIT
chart = '''
<svg viewBox="0 0 520 210" style="width:100%;display:block">
  <rect width="520" height="210" rx="10" fill="#EEF3F8"/>
  <path d="M520 0 V210 H468 C478 180 458 160 470 135 C482 110 460 90 472 62 C482 38 464 20 476 0 Z" fill="#F4EDE1"/>
  <path d="M476 0 C464 20 482 38 472 62 C460 90 482 110 470 135 C458 160 478 180 468 210" fill="none" stroke="#17315A" stroke-width="1.4"/>
  <g stroke="#C3D0E0" stroke-width="1" fill="none" stroke-dasharray="2 4">
    <path d="M10 50 C120 30 260 70 440 55"/><path d="M10 110 C140 95 270 130 440 115"/><path d="M10 170 C140 155 280 190 440 180"/>
  </g>
  <path d="M452 186 C400 186 372 170 350 150 C322 124 290 150 262 150 C226 150 212 120 180 118 C140 116 128 150 92 146 C58 142 44 110 64 84 C84 58 130 76 164 64 C204 50 238 34 290 38 C340 42 380 30 430 26" fill="none" stroke="#E4502F" stroke-width="2.4" stroke-dasharray="7 5" stroke-linecap="round"/>
  <g transform="translate(34 36)"><circle r="14" fill="none" stroke="#17315A" stroke-width="1"/><path d="M0 -18 L4.5 0 L0 18 L-4.5 0Z" fill="#17315A"/><path d="M0 -18 L4.5 0 L-4.5 0Z" fill="#E4502F"/><text y="-21" text-anchor="middle" font-family="Grotesk" font-size="9" font-weight="700" fill="#17315A">N</text></g>
  <g transform="translate(448 28)"><rect x="-5" y="-20" width="10" height="22" fill="#E4502F"/><rect x="-7" y="-24" width="14" height="5" fill="#17315A"/><path d="M-6 -22 L-40 -32 L-40 -12Z" fill="#F7D98B" opacity=".8"/><rect x="-9" y="2" width="18" height="5" fill="#17315A"/></g>
  <g font-family="Grotesk" font-weight="700" font-size="12" fill="#fff" text-anchor="middle">
    <g transform="translate(452 186)"><circle r="12" fill="#17315A"/><text y="4.5">1</text></g>
    <g transform="translate(350 150)"><circle r="12" fill="#17315A"/><text y="4.5">2</text></g>
    <g transform="translate(262 150)"><circle r="12" fill="#17315A"/><text y="4.5">3</text></g>
    <g transform="translate(180 118)"><circle r="12" fill="#E4502F"/><text y="4.5">4</text></g>
    <g transform="translate(64 84)"><circle r="12" fill="#2E8C7B"/><text y="4.5">5</text></g>
    <g transform="translate(290 38)"><circle r="12" fill="#E4502F"/><text y="4.5">6</text></g>
  </g>
  <text x="452" y="206" font-family="FrauncesText" font-style="italic" font-size="10" fill="#5B6475" text-anchor="middle">partida</text>
  <text x="400" y="50" font-family="FrauncesText" font-style="italic" font-size="10" fill="#5B6475" text-anchor="middle">chegada</text>
</svg>'''
stations = [
 ("1","O texto que explica","Texto expositivo","5","var(--ink)"),
 ("2","O texto que encanta","Texto de divulgação","8","var(--ink)"),
 ("3","O texto que pergunta","Entrevista","11","var(--ink)"),
 ("4","O texto que defende","Texto de opinião","16","var(--coral)"),
 ("5","As pontes","Conjunções e conectores","22","var(--sea)"),
 ("6","A tua voz","Debate e escrita","24","var(--coral)"),
]
st_html = "".join(f'''<div style="border-top:1.2mm solid {c};padding-top:2mm">
  <div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:{c}">ESTAÇÃO {n} · P. {pg}</div>
  <div style="font-family:FrauncesText;font-weight:700;font-size:10.4pt;line-height:1.12;color:var(--ink);margin-top:1mm">{t}</div>
  <div class="small muted" style="margin-top:.6mm">{g}</div></div>''' for n,t,g,pg,c in stations)

P[2] = page(2, f'''
<div class="kicker">Antes de zarpar</div>
<h2 style="margin-top:2mm">A rota desta unidade</h2>
<p class="lead" style="margin-top:3mm;max-width:160mm">Vais ler quatro textos sobre o mesmo mar. Todos falam da Nazaré e dos animais que ali vivem — mas cada um quer levar-te a fazer uma coisa diferente: <b class="blue">perceber</b>, <b class="blue">admirar</b>, <b class="blue">conhecer alguém</b> ou <b class="coral">concordar</b>.</p>
<div style="margin-top:5mm">{chart}</div>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:3.2mm;margin-top:4mm">{st_html}</div>
<div class="grid2" style="margin-top:7mm;grid-template-columns:1.12fr 1fr;align-items:stretch">
  <div>
    <h3>No fim da viagem, vais conseguir…</h3>
    <ul style="list-style:none;margin-top:2.6mm;font-size:9.5pt;line-height:1.36">
      <li style="margin-top:1.8mm"><span class="chk"></span>distinguir um <b>facto</b> de uma <b>opinião</b> e dizer como o sabes;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>reconhecer um <b>texto expositivo</b> e um <b>texto de divulgação</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>ler e preparar uma <b>entrevista</b> com seis perguntas;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>distinguir um texto que <b>informa</b> de um texto que <b>defende uma posição</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>escrever um <b>texto de opinião</b> com dois argumentos e uma conclusão;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>ligar ideias com <b>porque, pois, mas, porém</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>debater dois pontos de vista e <b>resumir a posição do grupo</b>.</li>
    </ul>
  </div>
  <div class="panel" style="padding:4.5mm">
    <div class="kicker blue">O código desta unidade</div>
    <div style="display:grid;grid-template-columns:10mm 1fr;gap:3.4mm 3mm;align-items:center;margin-top:3mm;font-size:9.2pt;line-height:1.3">
      {LUPA}<div><b class="blue">Lupa · azul</b><br>o texto <b>informa</b>: factos, dados, explicações.</div>
      {MEGA}<div><b class="coral">Megafone · coral</b><br>o texto <b>defende</b> uma opinião.</div>
      {PONTE}<div><b class="sea">Ponte · verde</b><br>palavras que <b>ligam</b> ideias.</div>
      <svg viewBox="0 0 22 40" style="width:7mm;height:13mm;justify-self:center"><rect width="22" height="40" fill="#EADFCB"/><rect y="24" width="22" height="16" fill="#17315A"/></svg><div><b class="blue">A maré</b> na margem de cada página sobe à medida que avanças. Na última página, estará cheia.</div>
    </div>
  </div>
</div>
<div style="margin-top:7mm"><div class="kicker">Os textos que vais ler</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:2.4mm"><div style="border-left:1.2mm solid var(--ink);padding:1mm 0 1mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--ink)">TEXTO 1 · P. 6</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;line-height:1.2;color:var(--ink);margin-top:.8mm">O Canhão da Nazaré</div><div class="small muted">expositivo</div></div><div style="border-left:1.2mm solid var(--ink);padding:1mm 0 1mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--ink)">TEXTO 2 · P. 9</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;line-height:1.2;color:var(--ink);margin-top:.8mm">Os vizinhos do canhão</div><div class="small muted">divulgação</div></div><div style="border-left:1.2mm solid var(--ink);padding:1mm 0 1mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--ink)">TEXTO 3 · P. 12</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;line-height:1.2;color:var(--ink);margin-top:.8mm">«O mar da Nazaré guarda um segredo no fundo»</div><div class="small muted">entrevista</div></div><div style="border-left:1.2mm solid var(--coral);padding:1mm 0 1mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--coral)">TEXTOS 4A E 4B · P. 16</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;line-height:1.2;color:var(--ink);margin-top:.8mm">Um golfinho não cabe num tanque · Conhecer para proteger</div><div class="small muted">opinião</div></div></div></div>
''', station="A rota")

# ---------------------------------------------------------------- 3 OPENER
P[3] = page(3, f'''
<div class="abs" style="left:0;right:0;top:0;height:175mm"><img class="cover" src="img/onda.jpg"></div>
<div class="abs" style="left:23.5mm;top:19mm;display:flex;align-items:flex-start;gap:4mm">
  <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">1</div>
  <div style="padding-top:2mm"><div class="kicker blue">Unidade 1</div><div style="font-family:Grotesk;font-size:8pt;letter-spacing:.08em;color:var(--ink);margin-top:1mm">Textos expositivos e de opinião</div></div>
</div>
<div class="abs" style="left:23.5mm;right:21mm;top:186mm;bottom:15mm;display:flex;flex-direction:column">
  <h1 style="font-size:44pt">Informar <em>ou</em> convencer?</h1>
  <p class="lead" style="margin-top:5mm;font-size:13pt">Na Praia do Norte, na Nazaré, o mar levanta algumas das maiores ondas alguma vez surfadas. Há quem as <b>explique</b>, há quem as <b>conte</b>, há quem <b>pergunte</b> por elas — e há quem tenha uma <b class="coral">opinião</b> firme sobre elas. Nesta unidade, vais aprender a reconhecer a intenção escondida em cada texto.</p>
  <div class="panel" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4.5mm 5mm">
    <div class="display" style="font-size:26pt;color:var(--ink);line-height:1">30 s</div>
    <div style="font-size:10.2pt"><b class="blue">A pares.</b> Olha para a imagem durante 30 segundos. Depois, diz ao teu colega <b class="blue">uma coisa que vês</b> e <b class="coral">uma coisa que pensas</b>. Qual das duas frases o teu colega poderia verificar?</div>
  </div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 4 FACT / OPINION
rows = [
 "A Praia do Norte fica na Nazaré.",
 "As ondas da Nazaré são as mais bonitas do mundo.",
 "Em 2020, foi surfada na Nazaré uma onda com 26,21 metros.",
 "Surfar ondas gigantes devia ser proibido.",
 "O farol da Nazaré fica no Forte de São Miguel Arcanjo.",
 "Acho que o inverno é a melhor altura para visitar a Nazaré.",
 "As ondas gigantes aparecem sobretudo no outono e no inverno.",
 "Os surfistas de ondas grandes são os atletas mais corajosos.",
]
WL = lambda: LUPA.replace('class="ico"','class="ico" style="width:5.4mm;height:5.4mm;vertical-align:-1.4mm"')
WM = lambda: MEGA.replace('class="ico"','class="ico" style="width:5.4mm;height:5.4mm;vertical-align:-1.4mm"')
trs = "".join(f'<tr><td style="font-family:Grotesk;font-weight:700;color:var(--coral);width:6mm">{chr(65+i)}</td><td style="font-weight:400;color:var(--text);width:auto;padding-top:2.1mm;padding-bottom:2.1mm">{s}</td><td style="text-align:center;width:12mm"><span class="chk"></span></td><td style="text-align:center;width:12mm"><span class="chk o"></span></td><td style="width:46mm;vertical-align:bottom"><div style="border-bottom:.6pt solid #AEB7C4;height:5mm"></div></td></tr>' for i,s in enumerate(rows))
P[4] = page(4, f'''
<div class="kicker">Ponto de partida</div>
<h2 style="margin-top:2mm">O que <span class="blue">vês</span> e o que <em>pensas</em></h2>
<p style="margin-top:3mm;max-width:160mm">Antes de ler textos inteiros, treina o olhar em frases soltas. Todas falam da Nazaré. Algumas podem ser <b>verificadas</b>; outras mostram aquilo que alguém <b>pensa</b> ou <b>sente</b>.</p>
{act(1,"Classificar", 'Marca cada frase com a <b class="blue">lupa</b> (facto) ou com o <b class="coral">megafone</b> (opinião). Na última coluna, escreve <b>como sabes</b>: onde a poderias verificar, ou que palavra mostra a opinião.')}
<table class="cmp" style="margin-top:3mm">
<tr><th style="background:var(--ink)" colspan="2">Frase</th><th style="background:var(--ink-soft);text-align:center">{WL()}</th><th style="background:var(--coral-soft);text-align:center">{WM()}</th><th style="background:var(--ink)">Como sabes?</th></tr>
{trs}
</table>
{act(2,"Descobrir a regra", 'Completa com as tuas palavras.<div style="margin-top:2.6mm;display:grid;gap:3.4mm"><div style="display:flex;gap:2mm;align-items:flex-end"><span style="white-space:nowrap">Um <b class="blue">facto</b> é uma informação que</span><span style="flex:1;border-bottom:.6pt solid #AEB7C4"></span></div><div style="display:flex;gap:2mm;align-items:flex-end"><span style="white-space:nowrap">Uma <b class="coral">opinião</b> é</span><span style="flex:1;border-bottom:.6pt solid #AEB7C4"></span></div></div>')}
{act(3,"Transformar", 'Reescreve a frase <b>C</b> como uma opinião e a frase <b>B</b> como um facto.<div style="display:grid;grid-template-columns:8mm 1fr;margin-top:1.4mm;align-items:end"><b class="coral">C</b><div class="lines"><i></i></div><b class="blue">B</b><div class="lines"><i></i></div></div>')}
<div class="grid2" style="margin-top:5mm;gap:5mm;align-items:stretch">
  <div class="panel coral">
    <div class="kicker">Sinais de opinião</div>
    <div class="opts" style="margin-top:2mm">
      <span class="chip">acho que</span><span class="chip">na minha opinião</span><span class="chip">considero</span><span class="chip">devia / deviam</span><span class="chip">o melhor</span><span class="chip">o mais bonito</span><span class="chip">corajoso</span><span class="chip">infelizmente</span>
    </div>
    <p class="small" style="margin-top:2.4mm">Palavras que <b>avaliam</b> (bonito, melhor, corajoso) e verbos que <b>recomendam</b> (devia) quase sempre denunciam uma opinião.</p>
  </div>
  <div class="panel blue">
    <div class="kicker blue">Atenção, detetive</div>
    <p class="small" style="margin-top:2mm">Um facto é algo que <b>se pode verificar</b> — não é, obrigatoriamente, verdadeiro. Se alguém escrever «A Nazaré fica no Algarve», isso não é uma opinião: é uma <b>informação falsa</b>. Pode verificar-se… e está errada!</p>
  </div>
</div>
''', station="Partida")

# ---------------------------------------------------------------- 5 STATION 1 — before reading
mapsvg = '''
<svg viewBox="0 0 300 190" style="width:100%;display:block">
  <rect width="300" height="190" rx="6" fill="#DCE5F0"/>
  <path d="M300 0 V190 H236 C231 170 240 152 232 132 C226 118 222 108 219 100 C214 88 222 70 226 52 C230 32 238 16 242 0Z" fill="#F4EDE1"/>
  <path d="M242 0 C238 16 230 32 226 52 C222 70 214 88 219 100 C222 108 226 118 232 132 C240 152 231 170 236 190" fill="none" stroke="#17315A" stroke-width="1.3"/>
  <path d="M190 0 C184 40 176 80 180 118 C184 150 196 170 200 190" fill="none" stroke="#17315A" stroke-width=".9" stroke-dasharray="3 3" opacity=".6"/>
  <path d="M219 99 C205 97 196 93 186 96 C170 101 160 94 146 98 C126 104 112 96 94 101 C74 107 56 100 34 106 C24 109 14 108 4 110 L4 124 C16 121 26 122 38 119 C60 113 78 119 98 113 C116 108 130 115 150 109 C166 104 176 110 190 104 C200 101 210 102 219 101Z" fill="#17315A"/>
  <circle cx="219" cy="100" r="3.6" fill="#E4502F" stroke="#fff" stroke-width="1.2"/>
  <g font-family="Grotesk" font-size="8.6" fill="#17315A" font-weight="700">
    <text x="228" y="104">Nazaré</text>
    <text x="229" y="82" font-weight="400" font-size="7.4">Praia do Norte</text>
    <text x="40" y="138">Canhão da Nazaré</text>
    <text x="20" y="30" font-weight="400" font-size="8" letter-spacing="1.2">OCEANO ATLÂNTICO</text>
    <text x="196" y="184" font-weight="400" font-size="7" text-anchor="end">limite da plataforma continental</text>
    <text x="247" y="152" font-weight="400" font-size="7" letter-spacing=".8">PORTUGAL</text>
  </g>
  <g transform="translate(20 160)"><rect width="45" height="3" fill="#17315A"/><text y="-3" font-family="Grotesk" font-size="7" fill="#17315A">50 km</text></g>
  <g transform="translate(280 22)"><path d="M0 -12 L4 2 L0 0 L-4 2Z" fill="#E4502F"/><text y="12" text-anchor="middle" font-family="Grotesk" font-size="8" font-weight="700" fill="#17315A">N</text></g>
</svg>'''
profile = '''
<svg viewBox="0 0 300 190" style="width:100%;display:block">
  <rect width="300" height="190" rx="6" fill="#fff" stroke="#C9CFD9"/>
  <g font-family="Grotesk" font-size="7" fill="#5B6475">
    <g stroke="#E3E7ED" stroke-width="1">
      <line x1="40" y1="56" x2="290" y2="56"/><line x1="40" y1="82" x2="290" y2="82"/><line x1="40" y1="108" x2="290" y2="108"/><line x1="40" y1="134" x2="290" y2="134"/><line x1="40" y1="160" x2="290" y2="160"/>
    </g>
    <text x="34" y="32" text-anchor="end">0 m</text><text x="34" y="58" text-anchor="end">1000</text><text x="34" y="84" text-anchor="end">2000</text><text x="34" y="110" text-anchor="end">3000</text><text x="34" y="136" text-anchor="end">4000</text><text x="34" y="162" text-anchor="end">5000</text>
    <text x="290" y="180" text-anchor="end">costa</text><text x="40" y="180">200 km ao largo</text>
  </g>
  <path d="M290 30 C282 36 276 44 268 52 C250 66 232 76 210 86 C180 100 150 114 120 128 C95 140 70 152 44 160 L40 161 L40 168 L290 168Z" fill="#17315A" opacity=".92"/>
  <path d="M290 30 L240 33 C228 34 222 38 214 52 C206 68 196 80 180 92" fill="none" stroke="#E4502F" stroke-width="1.8" stroke-dasharray="4 3"/>
  <line x1="40" y1="30" x2="290" y2="30" stroke="#17315A" stroke-width="1.6"/>
  <text x="44" y="25" font-family="Grotesk" font-size="7" fill="#17315A">superfície do mar</text>
  <g font-family="Body" font-size="8" font-weight="700">
    <text x="112" y="152" fill="#fff">fundo do canhão</text>
    <text x="176" y="52" fill="#E4502F">fundo ao lado do canhão</text>
  </g>
</svg>'''
vocab = [("canhão submarino","zona pouco funda do mar, junto à costa, antes de o fundo descer a pique"),
         ("cabeceira","vale profundo e estreito, de paredes inclinadas, no fundo do mar"),
         ("plataforma continental","fundo do oceano, plano e muito profundo, longe da costa"),
         ("planície abissal","ponto onde começa um vale ou um rio")]
vhtml = "".join(f'<b class="blue" style="text-align:right">{a}</b><span style="width:2.6mm;height:2.6mm;border-radius:50%;background:var(--ink);display:block"></span><span></span><span style="width:2.6mm;height:2.6mm;border-radius:50%;background:var(--ink);display:block"></span><span>{b}</span>' for a,b in vocab)
P[5] = page(5, f'''
<div style="display:flex;justify-content:space-between;align-items:flex-start">
  <div>
    <div class="kicker blue">Estação 1 · O texto que explica</div>
    <h2 style="margin-top:2mm">Um vale escondido<br>debaixo do mar</h2>
  </div>
  <div style="text-align:right">{LUPA.replace('class="ico"','class="ico" style="width:17mm;height:17mm"')}</div>
</div>
<p class="lead" style="margin-top:3mm">Um <b>texto expositivo</b> explica um tema com rigor: apresenta factos, organiza-os por partes e usa o vocabulário exato de cada assunto. Não quer convencer-te de nada — quer que <b>compreendas</b>.</p>
<div class="grid2" style="margin-top:4mm;gap:5mm">
  <div class="panel blue" style="padding:3.4mm 4mm"><div class="kicker blue">O que já sei sobre a Nazaré</div><div class="lines"><i></i><i></i></div></div>
  <div class="panel coral" style="padding:3.4mm 4mm"><div class="kicker">O que quero saber</div><div class="lines"><i></i><i></i></div></div>
</div>
<div class="grid2" style="margin-top:5mm;gap:5mm">
  <div><div class="kicker blue" style="margin-bottom:1.6mm">Vista de cima</div>{mapsvg}</div>
  <div><div class="kicker blue" style="margin-bottom:1.6mm">Em corte</div>{profile}</div>
</div>
<p class="src" style="margin-top:1.6mm">Esquemas simplificados, sem escala exata. Dados: Instituto Hidrográfico; Nazaré Qualifica.</p>
{act(1,"Prever", 'O texto da página seguinte chama-se <b>«O Canhão da Nazaré»</b>. Observa o mapa e o perfil. Que pergunta achas que o texto vai responder?' + lines(1),"blue")}
{act(2,"Vocabulário", 'Liga cada termo à sua definição. Depois, confirma durante a leitura.',"blue")}
<div style="display:grid;grid-template-columns:40mm 4mm 16mm 4mm 1fr;column-gap:2mm;row-gap:3.2mm;margin-top:3mm;margin-left:12mm;font-size:9.6pt;align-items:center">{vhtml}</div>
{act(3,"Oralidade", 'Com base no perfil, explica ao teu colega, numa só frase, a diferença entre as duas linhas. Usa a palavra <b>porque</b>.',"blue")}
''', station="Est. 1 · Explicar")

# ---------------------------------------------------------------- 6 EXPOSITORY TEXT
def para(n, html):
    return f'<p style="position:relative"><span style="position:absolute;left:-7.5mm;top:.2mm;width:5mm;height:5mm;border-radius:50%;background:var(--coral);color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{n}</span>{html}</p>'
nums = [("200 km","de comprimento, aprox."),("+ 5000 m","de profundidade"),("&lt; 1 km","da praia à cabeceira"),("26,21 m","onda-recorde (2020)")]
numhtml = "".join(f'<div style="border-top:.6pt solid var(--rule);padding:1.6mm 0"><div class="display" style="font-size:15pt;line-height:1;color:var(--ink)">{a}</div><div class="small muted">{b}</div></div>' for a,b in nums)
P[6] = page(6, f'''
<div style="display:grid;grid-template-columns:1fr 44mm;gap:7mm;height:100%">
<div>
  <div class="kicker blue">Texto 1 · Texto expositivo</div>
  <h2 style="margin-top:2mm;font-size:27pt">O Canhão da Nazaré</h2>
  <div class="reading" style="margin-top:4mm;padding-left:7.5mm">
  {para(1,'Em frente à vila da Nazaré, no distrito de Leiria, existe um dos maiores <b>desfiladeiros</b> submarinos da Europa: o Canhão da Nazaré. Este vale escondido no fundo do mar é a principal razão pela qual a Praia do Norte recebe algumas das maiores ondas alguma vez surfadas.')}
  {para(2,'Um canhão submarino é um vale profundo e estreito, com paredes muito inclinadas, escavado no fundo do oceano. O Canhão da Nazaré estende-se por cerca de 200 quilómetros, desde a costa até à planície abissal, e ultrapassa os 5000 metros de profundidade. A sua cabeceira, isto é, o ponto onde começa, fica a menos de um quilómetro da praia. Esta proximidade é rara no mundo.')}
  {para(3,'A origem do canhão ainda está a ser estudada. Os cientistas associam-na à <b>falha</b> da Nazaré, uma fratura da crosta terrestre que atravessa esta zona da costa.')}
  {para(4,'O canhão transforma as ondas que chegam do Atlântico Norte, sobretudo no outono e no inverno, quando há grandes tempestades no alto mar. Ao aproximarem-se da costa, as ondas encontram dois fundos diferentes. Sobre o canhão, a água é muito profunda e as ondas mantêm a velocidade e a energia. Ao lado, sobre a plataforma continental, a água é pouco profunda e as ondas abrandam. Esta diferença faz com que as ondas mudem de direção — um fenómeno chamado <b>refração</b> — e se encontrem junto à Praia do Norte, onde se somam. Por fim, ao entrarem em águas pouco profundas, crescem em altura: é o <b>empolamento</b>.')}
  {para(5,'O resultado pode ser medido. Uma onda com 4 metros no alto mar pode ultrapassar os 8 metros junto à costa e, em condições <b>excecionais</b>, os 20 metros. No dia 29 de outubro de 2020, o surfista alemão Sebastian Steudtner surfou ali uma onda de 26,21 metros, registada pelo Guinness World Records como recorde mundial.')}
  {para(6,'Por tudo isto, o Instituto Hidrográfico da Marinha Portuguesa estuda o canhão e utiliza modelos de computador para prever o comportamento das ondas. O Canhão da Nazaré mostra que aquilo que acontece à superfície do mar depende, muitas vezes, daquilo que não se vê no fundo.')}
  </div>
  <p class="src" style="margin-top:3.2mm;padding-left:7.5mm">Texto criado para esta unidade, com base em informação do Instituto Hidrográfico, da Nazaré Qualifica e do Guinness World Records.</p>
</div>
<aside style="border-left:.6pt solid var(--rule);padding-left:5mm;display:flex;flex-direction:column">
  <div class="kicker blue" style="margin-top:12mm">Glossário</div>
  <dl class="gloss" style="margin-top:2.4mm">
    <dt>desfiladeiro</dt><dd>passagem estreita e funda entre paredes altas.</dd>
    <dt>falha</dt><dd>fratura na crosta terrestre, ao longo da qual as rochas se podem deslocar.</dd>
    <dt>refração</dt><dd>mudança de direção de uma onda quando passa para águas de profundidade diferente.</dd>
    <dt>empolamento</dt><dd>aumento da altura da onda quando a água fica menos profunda.</dd>
    <dt>excecional</dt><dd>que acontece muito raramente.</dd>
  </dl>
  <div class="kicker blue" style="margin-top:3mm;margin-bottom:1mm">Em números</div>
  {numhtml}
  <div style="margin-top:auto">
    {qr("q-canhao","Explorar","O Canhão da Nazaré na Wikipédia.")}
    <div style="height:3mm"></div>
    {qr("q-recorde","Verificar","O recorde de 2020 no Guinness World Records.")}
  </div>
</aside>
</div>
''', station="Est. 1 · Explicar")

# ---------------------------------------------------------------- 7 COMPREHENSION + X-RAY
seq = ["As ondas encontram dois fundos diferentes.","Uma tempestade forma-se no Atlântico Norte.","As ondas crescem em altura junto à costa.","As ondas chegam à zona da Nazaré.","As ondas mudam de direção e somam-se."]
seqhtml = "".join(f'<div style="display:flex;gap:2.4mm;align-items:center"><span style="width:6.4mm;height:6.4mm;border:1.2px solid var(--ink);border-radius:50%;flex:none;background:#fff"></span><span>{s}</span></div>' for s in seq)
ul = lambda: '<span style="flex:1;border-bottom:.6pt solid #AEB7C4;min-height:6mm"></span>'
row = lambda label: f'<div style="display:flex;gap:2mm;align-items:flex-end"><span style="white-space:nowrap">{label}</span>{ul()}</div>'
P[7] = page(7, f'''
<div class="kicker blue">Texto 1 · Compreender</div>
<h2 style="margin-top:2mm">Raio-X de um texto que explica</h2>
<div class="grid2" style="margin-top:1mm;grid-template-columns:1.05fr 1fr;gap:7mm">
<div>
{act(1,"Localizar", 'Completa com dados do texto.<div style="margin-top:1.4mm;display:grid;gap:1.4mm">'+row("Comprimento:")+row("Profundidade máxima:")+row("Distância da cabeceira à praia:")+'</div>',"blue")}
{act(2,"Ordenar", 'Numera de 1 a 5 as etapas do nascimento de uma onda gigante (parágrafo 4).<div style="display:grid;gap:2.2mm;margin-top:2.4mm;font-size:9.5pt">'+seqhtml+'</div>',"blue")}
{act(3,"Inferir", 'Porque é que as ondas gigantes aparecem na Praia do Norte e não em qualquer outra praia portuguesa? Começa por <b>«Porque…»</b>.'+lines(3),"blue")}
{act(4,"Relacionar", 'No parágrafo 2 lê-se «Esta proximidade é rara no mundo». A que proximidade se refere o texto?'+lines(2),"blue")}
</div>
<div>
  <div class="panel blue" style="margin-top:4.2mm">
    <div class="kicker blue">A estrutura</div>
    <div style="display:grid;grid-template-columns:25mm 1fr;gap:2.6mm 3mm;margin-top:2.6mm;font-size:9pt;line-height:1.3;align-items:center">
      <div style="background:var(--ink);color:#fff;border-radius:1.5mm;padding:1.6mm 2.2mm;font-weight:700">Introdução<br><span style="font-weight:400;font-size:8pt">parágrafo 1</span></div><div>apresenta o tema e diz porque é importante.</div>
      <div style="background:var(--ink-2);color:#fff;border-radius:1.5mm;padding:1.6mm 2.2mm;font-weight:700;align-self:stretch">Desenvolvi&shy;mento<br><span style="font-weight:400;font-size:8pt">parágrafos 2 a 5</span></div>
      <div>cada parágrafo trata de um <b>subtema</b>. Dá um título a cada um:<div style="display:grid;gap:1.2mm;margin-top:1mm">{row("2")}{row("3")}{row("4")}{row("5")}</div></div>
      <div style="background:var(--ink);color:#fff;border-radius:1.5mm;padding:1.6mm 2.2mm;font-weight:700">Conclusão<br><span style="font-weight:400;font-size:8pt">parágrafo 6</span></div><div>fecha o tema com uma ideia geral.</div>
    </div>
  </div>
  {act(5,"Provar", 'Encontra no texto um exemplo de cada característica.<div style="display:grid;gap:1.4mm;margin-top:1.4mm;font-size:9.2pt">'+row("<b>verbo no presente</b>")+row("<b>número ou data</b>")+row("<b>termo científico</b>")+row("<b>explicação de um termo</b>")+'</div>',"blue")}
  {act(6,"Pensar", 'Há alguma opinião no texto? Procura palavras como <i>bonito, fantástico, devia</i>. O que concluis?'+lines(2),"blue")}
</div>
</div>
{act(7,"Escrever", '<b>Resumo relâmpago.</b> Explica o essencial do texto em duas frases, com <b>35 palavras no máximo</b>. Conta-as!'+lines(5),"blue")}
''', station="Est. 1 · Explicar")
