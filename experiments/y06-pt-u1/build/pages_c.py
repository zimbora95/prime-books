import parts
from parts import *
parts.UNIT.update(n=1, total=28)

P = {}
U = lambda h=6.5: f'<span style="display:block;border-bottom:.6pt solid #AEB7C4;height:{h}mm"></span>'
SEA_D = "var(--sea-d,#2E8C7B)"

def pg(n, body, station):
    return page(n, body, station=station, cls="flex")

# ---------------------------------------------------------------- 18 ANATOMY OF AN OPINION TEXT
parts_ = [("Tese", "§ 1", "a opinião que o autor defende", "«Na minha opinião, os golfinhos não devem viver em cativeiro…»", "var(--coral)"),
          ("Argumento 1 + exemplo", "§ 2", "uma razão, apoiada num facto", "«…são animais do mar aberto.» — as mães cuidam das crias durante anos", "var(--ink)"),
          ("Argumento 2 + exemplo", "§ 3", "outra razão, com outro exemplo", "«…não precisamos de os fechar para os conhecer.» — passeios na Nazaré e no Sado", "var(--ink)"),
          ("Contra-argumento + resposta", "§ 4", "a opinião contrária, e porque não convence", "«Há quem diga que… Mas…»", SEA_D),
          ("Conclusão", "§ 5", "retoma a tese e fecha o texto", "«Por isso, defendo que…»", "var(--coral)")]
ph = "".join(f'''<div style="display:grid;grid-template-columns:44mm 1fr;gap:4mm;align-items:stretch;margin-top:2mm">
  <div style="background:{c};color:#fff;border-radius:1.6mm;padding:2.2mm 3mm"><div style="font-weight:700;font-size:9.4pt;line-height:1.2">{a}</div><div style="font-size:7.8pt;opacity:.85;margin-top:.6mm">{p} · {b}</div></div>
  <div style="border-bottom:.6pt solid var(--rule);padding:1.6mm 0;font-family:FrauncesText;font-size:9.8pt;line-height:1.4;align-self:center">{q}</div></div>''' for a, p, b, q, c in parts_)
blank = "".join(f'''<div style="display:grid;grid-template-columns:44mm 1fr;gap:4mm;align-items:end;margin-top:2mm">
  <div style="border:1.2pt solid {c};color:var(--ink);border-radius:1.6mm;padding:2mm 3mm;font-weight:700;font-size:9pt;align-self:start">{a}</div><span>{U(7)}{U(7)}</span></div>''' for a, p, b, q, c in parts_)
P[18] = pg(18, f'''
<div class="kicker">Texto 4A · Por dentro</div>
<h2 style="margin-top:2mm">O esqueleto de um texto de opinião</h2>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Um bom texto de opinião não é um desabafo: é uma construção. Cada parágrafo tem uma função. Vê como o texto da Clara está organizado.</p>
<div style="margin-top:1.4mm">{ph}</div>
<div class="grid2" style="margin-top:3mm;gap:5mm">
  <div class="rule-card o" style="font-size:9.2pt;line-height:1.5"><b class="coral">Marcas de opinião</b> — 1.ª pessoa (<i>eu, defendo, acho</i>), expressões como <i>na minha opinião</i>, palavras que avaliam (<i>melhor, não faz sentido</i>).</div>
  <div class="rule-card" style="font-size:9.2pt;line-height:1.5"><b class="blue">Organizadores</b> — ajudam o leitor a seguir o raciocínio: <i>em primeiro lugar, além disso, há quem diga que, por isso</i>.</div>
</div>
{act(1, "Aplicar", 'Agora faz o mesmo com o texto do <b>Tiago</b>: copia uma frase curta de cada parte.', "")}
<div>{blank}</div>
<div style="margin-top:1mm">{act(2, "Avaliar", 'Há alguma parte que falte no texto do Tiago, ou que esteja mais fraca? Explica.' + lines(1))}</div>
''', "Est. 4 · Defender")

# ---------------------------------------------------------------- 19 COMPARE THE TWO COLUMNS
rows = ["Tese", "Argumento 1", "Exemplo do argumento 1", "Argumento 2", "Exemplo do argumento 2", "Proposta final"]
tr = "".join(f'<tr><td style="font-size:9pt;width:36mm">{r}</td><td style="height:21mm"></td><td></td></tr>' for r in rows)
P[19] = pg(19, f'''
<div class="kicker">Textos 4A e 4B · Comparar</div>
<h2 style="margin-top:2mm">Frente a frente: a Clara e o Tiago</h2>
<table class="cmp ruled" style="margin-top:3mm">
  <tr><th style="background:var(--coral)"></th><th style="background:var(--coral)">Clara · «Um golfinho não cabe num tanque»</th><th style="background:var(--coral)">Tiago · «Conhecer para proteger»</th></tr>
  {tr}
</table>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(1, "Descobrir", 'A Clara e o Tiago citam a <b>mesma fonte</b>. Qual? Usam-na para defender o mesmo?' + lines(3))}</div>
  <div>{act(2, "Explicar", 'O Tiago escreve «É verdade que um tanque não é o oceano». Porque é que concorda com a Clara nesse ponto?' + lines(3))}</div>
</div>
<div class="grid2" style="margin-top:2mm;gap:7mm">
  <div>{act(3, "Avaliar", 'Qual dos dois textos te convenceu mais? Dá <b>uma razão</b> ligada à forma como está escrito.' + lines(4))}</div>
  <div>{act(4, "Voltar atrás", 'Relê o que escreveste na p. 16, antes de ler. Mudaste de opinião? Porquê?' + lines(4))}</div>
</div>
''', "Est. 4 · Defender")

# ---------------------------------------------------------------- 20 WEIGHING ARGUMENTS
strong = [("Apoia-se num facto que se pode verificar", "«Em 2023, nasceram seis crias no Sado.»"),
          ("Dá um exemplo concreto", "«Ao largo da Nazaré, há passeios de observação.»"),
          ("Indica uma fonte de confiança", "«Os cientistas do MARE explicam que…»")]
weak = [("Generaliza sem provas", "«Toda a gente sabe que os golfinhos são felizes.»"),
        ("Ataca a pessoa, não a ideia", "«O Tiago não percebe nada de animais.»"),
        ("Repete a opinião, sem razão", "«Não deve haver parques porque não deve.»")]
card = lambda items, cls, title, col: f'''<div class="rule-card{cls}" style="font-size:9.2pt;line-height:1.45"><b style="color:{col}">{title}</b>''' + "".join(f'<div style="margin-top:2mm"><b>{a}</b><div style="font-family:FrauncesText;font-style:italic;color:var(--muted);margin-top:.4mm">{b}</div></div>' for a, b in items) + '</div>'
args = ["Os golfinhos nadam longas distâncias no oceano, por isso um tanque é pequeno para eles.",
        "Quem defende os parques aquáticos é má pessoa.",
        "A lei francesa de 2021 acaba com os espetáculos de cetáceos a partir de 2026.",
        "Todos os golfinhos adoram fazer truques.",
        "Os investigadores do MARE observaram que o excesso de barcos perturba os golfinhos.",
        "Os parques são maus porque não são bons."]
ah = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr 30mm;gap:3mm;align-items:center;margin-top:2.2mm;font-size:9.4pt"><b class="coral">{chr(97+i)})</b><span style="font-family:FrauncesText;line-height:1.4">{t}</span><span style="display:flex;gap:2mm;align-items:center;font-size:8.2pt"><span class="chk"></span>forte<span class="chk o"></span>fraco</span></div>' for i, t in enumerate(args))
P[20] = pg(20, f'''
<div class="kicker">Estação 4 · Pensar</div>
<h2 style="margin-top:2mm">Argumento forte ou argumento fraco?</h2>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Um argumento é tanto mais forte quanto mais <b>fácil for de verificar</b>. Gritar mais alto não conta!</p>
<div class="grid2" style="margin-top:3mm;gap:5mm">{card(strong, "", "Argumentos fortes", "var(--ink)")}{card(weak, " o", "Argumentos fracos", "var(--coral)")}</div>
{act(1, "Classificar", 'Assinala se cada argumento é forte ou fraco.')}
<div style="padding-left:9mm">{ah}</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(2, "Justificar", 'Escolhe um argumento <b>fraco</b> e explica porque não convence.' + lines(4))}</div>
  <div>{act(3, "Melhorar", 'Reescreve o argumento <b>d)</b>, de forma a torná-lo mais forte.' + lines(4))}</div>
</div>
<div class="panel coral" style="margin-top:auto">{act(4, "Criar", 'Pensa na tua resposta da p. 16. Escreve agora um argumento <b>forte</b> para a opinião <b>contrária</b> à tua, com um facto ou um exemplo.' + lines(4))}</div>
''', "Est. 4 · Defender")

# ---------------------------------------------------------------- 21 INTENTION DETECTOR
ex = [("«A cabeceira do canhão fica a menos de um quilómetro da praia.»", "Texto 1"),
      ("«Sabias que os cientistas conseguem reconhecer cada golfinho?»", "Texto 2"),
      ("«Nunca vou para o mar sem consultar a previsão.»", "Texto 3"),
      ("«O lugar dos golfinhos é o mar.»", "Texto 4A"),
      ("«Em vez de proibir, defendo que se criem regras mais exigentes.»", "Texto 4B"),
      ("«O golfinho-comum pode atingir 2,3 metros.»", "Texto 2")]
eh = "".join(f'''<div style="display:grid;grid-template-columns:1fr 18mm 50mm;gap:3mm;align-items:center;padding:2mm 0;border-bottom:.6pt solid var(--rule)">
  <span style="font-family:FrauncesText;font-size:9.8pt;line-height:1.4">{t}</span><span class="small muted">{s}</span>
  <span style="display:flex;gap:2.4mm;align-items:center;font-size:8.4pt"><span class="chk"></span>{LUPA.replace('class="ico"','class="ico" style="width:5mm;height:5mm"')}informa<span class="chk o"></span>{MEGA.replace('class="ico"','class="ico" style="width:5mm;height:5mm"')}defende</span></div>''' for t, s in ex)
P[21] = pg(21, f'''
<div class="kicker">Estações 1 a 4 · Juntar tudo</div>
<h2 style="margin-top:2mm">O detetor de intenções</h2>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Um texto que <b class="blue">informa</b> quer que compreendas. Um texto que <b class="coral">defende</b> quer que concordes. Antes de acreditares num texto, pergunta sempre: <i>o que quer ele que eu faça?</i></p>
{act(1, "Detetar", 'Assinala a intenção de cada frase.')}
<div style="border-top:.6pt solid var(--rule);margin-top:2mm">{eh}</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(2, "Justificar", 'Escolhe uma frase que <b>defende</b>. Que palavra ou expressão te ajudou a descobrir?' + lines(4))}</div>
  <div>{act(3, "Desafio", 'A frase do Texto 3 é de uma entrevista. Informa ou defende? Pode fazer as duas coisas?' + lines(4))}</div>
</div>
{act(4, "Transformar", 'Pega neste facto e escreve-o de duas maneiras: <i>«Nas águas portuguesas vivem mais de 20 espécies de cetáceos.»</i>')}
<div class="grid2" style="margin-top:1mm;gap:6mm">
  <div class="panel blue" style="padding:3mm 3.6mm"><div class="kicker blue">Para informar</div>{U()}{U()}{U()}</div>
  <div class="panel coral" style="padding:3mm 3.6mm"><div class="kicker">Para defender uma opinião</div>{U()}{U()}{U()}</div>
</div>
<div style="margin-top:auto">{act(5, "Refletir", 'Porque é importante saber se um texto quer informar-nos ou convencer-nos? Dá um exemplo da tua vida (publicidade, redes sociais, notícias…).' + lines(3))}</div>
''', "Est. 4 · Defender")

# ---------------------------------------------------------------- 22 GRAMMAR — conjunctions & connectors
kinds = [("Causa", "porque, pois", "indica a razão, o motivo", "Os golfinhos orientam-se pelo som <b>porque</b> emitem estalidos e escutam o eco.", "var(--ink)"),
         ("Explicação", "pois", "justifica o que se disse antes", "Leva um casaco, <b>pois</b> está frio no barco.", SEA_D),
         ("Contraste", "mas, porém", "opõe duas ideias", "Um tanque é grande, <b>mas</b> não é o oceano.<br>Um tanque é grande. Não é, <b>porém</b>, o oceano.", "var(--coral)")]
kh = "".join(f'''<div style="border-top:1.4mm solid {c};padding-top:2.4mm">
  <div class="kicker" style="color:{c}">{k}</div><div class="display" style="font-size:16pt;color:var(--ink);line-height:1.1;margin-top:1mm">{w}</div>
  <div class="small muted" style="margin-top:.6mm">{d}</div><div style="font-family:FrauncesText;font-size:9.8pt;line-height:1.45;margin-top:2mm">{e}</div></div>''' for k, w, d, e, c in kinds)
P[22] = pg(22, f'''
<div style="display:flex;justify-content:space-between;align-items:flex-start">
  <div><div class="kicker sea">Estação 5 · As pontes</div><h2 style="margin-top:2mm">Palavras que ligam ideias</h2></div>
  <div>{PONTE.replace('class="ico"','class="ico" style="width:15mm;height:15mm"')}</div>
</div>
<p class="lead" style="margin-top:2.6mm;font-size:10.6pt">As <b>conjunções</b> são palavras invariáveis que ligam palavras ou frases. Num texto de opinião, são as <b>pontes</b> do raciocínio: sem elas, os argumentos ficam soltos.</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:4mm">{kh}</div>
<div class="grid2" style="margin-top:5mm;gap:5mm">
  <div class="rule-card" style="font-size:9.2pt;line-height:1.5"><b class="blue">Atenção ao «pois».</b> Quando <i>pois</i> introduz uma explicação, escreve-se depois de uma <b>vírgula</b>: <i>Fiquei em casa, pois estava doente.</i> Na maior parte das frases, <i>pois</i> e <i>porque</i> podem trocar de lugar.</div>
  <div class="rule-card o" style="font-size:9.2pt;line-height:1.5"><b class="coral">Atenção ao «porém».</b> Ao contrário de <i>mas</i>, <i>porém</i> pode mudar de lugar na frase, e fica entre vírgulas: <i>Os parques, porém, têm regras.</i></div>
</div>
<div class="panel" style="margin-top:4mm;display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:center">
  <div style="font-size:9.2pt;line-height:1.5"><b class="blue">Na gramática</b>, <i>mas</i> e <i>porém</i> são conjunções <b>coordenativas adversativas</b>; <i>porque</i> é uma conjunção <b>subordinativa causal</b>; <i>pois</i> pode ser causal ou explicativa, conforme a frase.</div>
  {qr("q-pois", "Tira-dúvidas", "O valor de «pois», no Ciberdúvidas.")}
</div>
{act(1, "Encontrar", 'Nos Textos 4A e 4B, encontra uma frase com <b>mas</b> e outra com <b>porém</b>. Copia-as.' + lines(4), "sea")}
<div class="grid2" style="margin-top:1mm;gap:7mm">
  <div>{act(2, "Distinguir", 'Em qual destas frases <b>pois</b> indica a <b>causa</b> e em qual introduz uma <b>explicação</b>?<div style="font-family:FrauncesText;font-size:9.6pt;line-height:1.5;margin-top:1.4mm">a) Não fui à praia, pois estava a chover.<br>b) Leva o guarda-chuva, pois vai chover.</div>' + lines(5), "sea")}</div>
  <div>{act(3, "Substituir", 'Troca <b>porque</b> por <b>pois</b> e <b>mas</b> por <b>porém</b>. O sentido muda?<div style="font-family:FrauncesText;font-size:9.6pt;line-height:1.5;margin-top:1.4mm">Fiquei em casa porque estava cansado, mas queria ir ao cinema.</div>' + lines(5), "sea")}</div>
</div>
''', "Est. 5 · Ligar")

# ---------------------------------------------------------------- 23 GRAMMAR PRACTICE
fill = ["O mar estava calmo, ________ a previsão anunciava ondas de oito metros.",
        "Os surfistas treinam todo o ano, ________ as ondas gigantes são perigosas.",
        "Fiquei na praia a ver o mar, ________ não havia ondas para surfar.",
        "A cabeceira do canhão fica perto da costa. As ondas, ________, só crescem no inverno."]
fh = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;margin-top:2.4mm;font-family:FrauncesText;font-size:10pt;line-height:1.5"><b class="display" style="color:{SEA_D};font-size:11pt">{chr(97+i)})</b><span>{t}</span></div>' for i, t in enumerate(fill))
join = [("Os golfinhos vivem em grupo.", "São animais muito sociais.", "causa"),
        ("O canhão tem cinco mil metros.", "A sua cabeceira fica perto da praia.", "contraste"),
        ("Leva protetor solar.", "O sol está muito forte.", "explicação")]
jh = "".join(f'<div style="margin-top:2.6mm"><div style="font-family:FrauncesText;font-size:9.8pt"><b style="color:{SEA_D}">{chr(97+i)})</b> {a} + {b} <span class="small muted">({c})</span></div>{U(6.5)}</div>' for i, (a, b, c) in enumerate(join))
P[23] = pg(23, f'''
<div class="kicker sea">Estação 5 · Praticar</div>
<h2 style="margin-top:2mm">Construir pontes</h2>
{act(1, "Completar", 'Completa com <b>porque</b>, <b>pois</b>, <b>mas</b> ou <b>porém</b>. Às vezes, há mais do que uma resposta certa.', "sea")}
<div style="padding-left:9mm">{fh}</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(2, "Ligar", 'Junta as duas frases numa só, com a conjunção indicada.<div>' + jh + '</div>', "sea")}</div>
  <div>
    {act(3, "Corrigir", 'Esta frase usa a conjunção errada. Corrige-a e explica porquê: <i>«Gosto muito de golfinhos, porque nunca vi nenhum.»</i>' + lines(4), "sea")}
    {act(4, "Pontuar", 'Coloca as vírgulas que faltam: <i>O Tiago porém não concorda com a Clara.</i>' + lines(2), "sea")}
  </div>
</div>
{act(5, "Classificar", 'Indica o valor da conjunção sublinhada: <b>causa</b>, <b>explicação</b> ou <b>contraste</b>.<div style="display:grid;grid-template-columns:1fr 34mm;gap:2mm 4mm;margin-top:1.6mm;font-family:FrauncesText;font-size:9.6pt;align-items:end"><span>Um tanque é grande, <u>mas</u> não é o oceano.</span>' + U(5.5) + '<span>Os surfistas ficaram em terra <u>porque</u> o mar estava calmo.</span>' + U(5.5) + '<span>Vem cedo, <u>pois</u> o barco sai às nove.</span>' + U(5.5) + '</div>', "sea")}
<div class="panel sea" style="margin-top:auto">{act(6, "Escrever", 'Escreve <b>três frases</b> sobre o mar da Nazaré: uma com uma conjunção de <b>causa</b>, uma de <b>explicação</b> e uma de <b>contraste</b>. Sublinha as conjunções.' + lines(4), "sea")}</div>
''', "Est. 5 · Ligar")

# ---------------------------------------------------------------- 24 DEBATE
roles = [("Moderador", "dá a palavra, controla o tempo e mantém a calma"), ("Equipa A", "defende uma posição"),
         ("Equipa B", "defende a posição contrária"), ("Relator", "toma notas e, no fim, resume a posição de cada grupo")]
rh = "".join(f'<div style="border-top:1.1mm solid var(--coral);padding-top:1.6mm"><b style="font-size:9.4pt;color:var(--ink)">{a}</b><div class="small muted" style="margin-top:.4mm;line-height:1.3">{b}</div></div>' for a, b in roles)
steps = [("5 min", "Cada equipa prepara dois argumentos com exemplos."), ("2 min", "Equipa A apresenta a sua posição."),
         ("2 min", "Equipa B apresenta a sua posição."), ("4 min", "Debate livre: responder aos argumentos do outro lado."),
         ("2 min", "Os relatores resumem a posição de cada grupo.")]
sh = "".join(f'<div style="display:grid;grid-template-columns:15mm 1fr;gap:3mm;padding:1.6mm 0;border-bottom:.6pt solid var(--rule);font-size:9.2pt"><b class="coral">{a}</b><span>{b}</span></div>' for a, b in steps)
phr = ["Concordo com… porque…", "Compreendo o teu ponto de vista, mas…", "Tenho uma opinião diferente, pois…", "Podes dar um exemplo?"]
ph = "".join(f'<div style="font-family:Caveat;font-size:14pt;color:var(--ink);line-height:1.3">«{t}»</div>' for t in phr)
P[24] = pg(24, f'''
<div class="abs" style="left:0;right:0;top:0;height:80mm"><img class="cover" src="img/debate.jpg"></div>
<div style="height:86mm"></div>
<div style="display:flex;justify-content:space-between;align-items:flex-end">
  <div><div class="kicker">Estação 6 · A tua voz</div><h2 style="margin-top:2mm">Debate: golfinhos em parques aquáticos?</h2></div>
  <div>{MICRO.replace('class="ico"','class="ico" style="width:13mm;height:13mm"')}</div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:3mm">{rh}</div>
<div class="grid2" style="grid-template-columns:1.15fr 1fr;gap:7mm;margin-top:4mm">
  <div><h3>Como funciona (15 minutos)</h3><div style="margin-top:1.4mm;border-top:.6pt solid var(--rule)">{sh}</div></div>
  <div class="panel coral" style="padding:3.4mm 4mm"><div class="kicker">Frases para debater com respeito</div><div style="margin-top:1.6mm">{ph}</div></div>
</div>
<div class="panel" style="margin-top:4mm;padding:3.6mm 4mm"><div class="kicker">Resumo do relator</div>
  <div style="font-family:FrauncesText;font-size:9.8pt;line-height:1.5;margin-top:1.6mm">A posição do nosso grupo é que</div>{U()}{U()}
  <div style="font-family:FrauncesText;font-size:9.8pt;line-height:1.5;margin-top:1.4mm">O nosso argumento mais forte foi</div>{U()}
  <div style="font-family:FrauncesText;font-size:9.8pt;line-height:1.5;margin-top:1.4mm">Reconhecemos que o outro grupo tem razão quando diz que</div>{U()}{U()}
</div>
''', "Est. 6 · A tua voz")

# ---------------------------------------------------------------- 25 PLAN AN OPINION TEXT
topics = ["Devia ser proibido surfar ondas gigantes?", "Os telemóveis deviam ser proibidos no recreio?", "As aulas deviam começar mais tarde?"]
th = "".join(f'<div style="display:flex;gap:2.4mm;align-items:center;margin-top:1.6mm;font-size:9.4pt"><span class="chk"></span><span>{t}</span></div>' for t in topics)
box = lambda title, hint, col, k=3: f'<div style="border-left:1.4mm solid {col};padding:1.6mm 0 1.6mm 3.4mm;margin-top:2.6mm"><b style="font-size:9.6pt;color:var(--ink)">{title}</b> <span class="small muted">{hint}</span>{"".join(U() for _ in range(k))}</div>'
P[25] = pg(25, f'''
<div style="display:flex;gap:4mm;align-items:center">{LAPIS}<div><div class="kicker">Estação 6 · Escrever</div><h2 style="margin-top:1mm">O meu texto de opinião · planear</h2></div></div>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Vais escrever um texto de opinião com <b>dois argumentos</b> e uma <b>conclusão</b> (entre 120 e 180 palavras). Primeiro, planeia.</p>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:2.6mm">
  <div class="panel" style="padding:3.4mm 4mm"><div class="kicker">1 · Escolhe o tema</div>{th}<div style="display:flex;gap:2.4mm;align-items:flex-end;margin-top:1.6mm;font-size:9.4pt"><span class="chk"></span><span>Outro:</span><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div></div>
  <div class="panel blue" style="padding:3.4mm 4mm"><div class="kicker blue">2 · Pesquisa um facto</div><p class="small" style="margin-top:1mm">Um facto verdadeiro que apoie a tua opinião, e onde o encontraste.</p>{U()}{U()}</div>
</div>
{box("Tese", "— a minha opinião, numa frase clara", "var(--coral)")}
{box("Argumento 1 + exemplo", "— começa por «Em primeiro lugar…»", "var(--ink)")}
{box("Argumento 2 + exemplo", "— começa por «Além disso…»", "var(--ink)")}
{box("Contra-argumento + resposta", "— «Há quem diga que… Porém…»", SEA_D)}
{box("Conclusão", "— «Por isso, defendo que…»", "var(--coral)")}
<div class="panel sea" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:3.2mm 4mm">
  <div class="kicker sea" style="max-width:28mm">Pontes a usar</div>
  <div style="font-size:9.2pt;line-height:1.5"><i>na minha opinião · considero que · em primeiro lugar · além disso · porque · pois · mas · porém · há quem diga que · por isso · em conclusão</i></div>
</div>
''', "Est. 6 · A tua voz")

# ---------------------------------------------------------------- 26 WRITE + REVISE
chk = ["Tenho uma <b>tese</b> clara no primeiro parágrafo.", "Tenho <b>dois argumentos</b>, cada um com um exemplo.",
       "Usei pelo menos <b>três conjunções</b> diferentes.", "Escrevi uma <b>conclusão</b> que retoma a tese.",
       "Usei a 1.ª pessoa e expressões de opinião.", "Revi a ortografia e a pontuação."]
ck = "".join(f'<div style="display:grid;grid-template-columns:5mm 5mm 1fr;gap:2mm;margin-top:1.4mm;align-items:start;font-size:8.8pt;line-height:1.4"><span class="chk"></span><span class="chk o"></span><span>{t}</span></div>' for t in chk)
P[26] = pg(26, f'''
<div class="kicker">Estação 6 · Escrever</div>
<div style="display:flex;gap:3mm;align-items:flex-end;margin-top:1.4mm"><b class="coral" style="font-size:11pt">Título:</b><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:7mm"></span></div>
{lines(24)}
<div class="grid2" style="grid-template-columns:1.1fr 1fr;gap:6mm;margin-top:auto">
  <div class="panel" style="padding:3.4mm 4mm"><div style="display:flex;justify-content:space-between"><div class="kicker">Rever</div><div class="small muted">eu · colega</div></div>{ck}</div>
  <div class="panel coral" style="padding:3.4mm 4mm"><div class="kicker">O comentário do meu colega</div><p class="small" style="margin-top:1mm">O teu argumento mais forte é… Podias melhorar…</p>{U()}{U()}{U()}</div>
</div>
''', "Est. 6 · A tua voz")

# ---------------------------------------------------------------- 27 CONSEGUES? (check yourself)
P[27] = pg(27, f'''
<div class="kicker">Consegues?</div>
<h2 style="margin-top:2mm">Mostra o que aprendeste</h2>
<div class="panel" style="margin-top:3mm;padding:4mm 5mm;font-family:FrauncesText;font-size:10.2pt;line-height:1.55">
  <b style="font-family:Body;color:var(--ink)">Farol ou museu?</b><br>
  O farol da nossa vila deixou de ter faroleiro há muitos anos, pois hoje funciona de forma automática. Na minha opinião, a casa do faroleiro devia tornar-se um pequeno museu do mar. Em primeiro lugar, a vila não tem nenhum espaço onde se conte a história dos pescadores. Além disso, um museu atrairia visitantes no inverno, quando a praia está vazia. Há quem diga que um museu custa caro; porém, a casa já existe e só precisa de obras. Por isso, defendo que a câmara municipal aproveite este edifício.
  <p class="src" style="font-family:Body;margin-top:1.4mm">Texto escrito para este manual.</p>
</div>
<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>
{act(1, "Intenção", 'Este texto informa ou defende uma opinião? Como o sabes?' + lines(3))}
{act(2, "Tese", 'Copia a tese do autor.' + lines(3))}
{act(3, "Argumentos", 'Quais são os dois argumentos?' + lines(3))}
</div>
<div>
{act(4, "Facto e opinião", 'Copia uma frase que seja um <b>facto</b>.' + lines(3))}
{act(5, "Conjunções", 'Sublinha <b>pois</b> e <b>porém</b>. Que valor tem cada uma?' + lines(3))}
{act(6, "Entrevista", 'Escreve uma pergunta <b>aberta</b> que farias ao antigo faroleiro da vila.' + lines(3))}
</div>
</div>
<div class="panel coral" style="margin-top:auto">{act(7, "Contra-argumentar", 'Escreve um pequeno parágrafo com a opinião contrária. Usa <b>mas</b> ou <b>porém</b>.' + lines(3))}</div>
''', "Chegada")

# ---------------------------------------------------------------- 28 SELF-ASSESSMENT + UNIT GLOSSARY
goals = ["distinguir um facto de uma opinião", "reconhecer um texto expositivo e um texto de divulgação", "ler e preparar uma entrevista com seis perguntas",
         "distinguir um texto que informa de um que defende uma posição", "escrever um texto de opinião com dois argumentos e uma conclusão",
         "ligar ideias com porque, pois, mas, porém", "debater dois pontos de vista e resumir a posição do grupo"]
circ = '<svg viewBox="0 0 20 20" style="width:4.2mm;height:4.2mm"><circle cx="10" cy="10" r="8" fill="none" stroke="#17315A" stroke-width="1.6"/></svg>'
gt = "".join(f'<tr><td style="font-size:8.8pt;font-weight:400">Consigo {g}.</td><td style="text-align:center">{circ}</td><td style="text-align:center">{circ}</td><td style="text-align:center">{circ}</td></tr>' for g in goals)
gl = [("argumento", "razão que apoia uma opinião"), ("contra-argumento", "razão que apoia a opinião contrária"), ("conjunção", "palavra invariável que liga palavras ou frases"),
      ("entrevista", "texto de perguntas e respostas entre um entrevistador e um entrevistado"), ("facto", "informação que se pode verificar"),
      ("opinião", "aquilo que alguém pensa sobre um assunto"), ("tese", "a opinião principal defendida num texto"),
      ("texto de divulgação", "texto que explica ciência a leitores não especialistas, de forma cativante"), ("texto expositivo", "texto que explica um tema com rigor e objetividade")]
gh = "".join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in gl)
P[28] = pg(28, f'''
<div class="kicker">Chegada</div>
<h2 style="margin-top:2mm">A maré está cheia</h2>
<div style="display:grid;grid-template-columns:1fr 52mm;gap:6mm;margin-top:3mm;flex:1">
<div>
  <table class="cmp ruled" style="font-size:8.8pt"><tr><th style="background:var(--ink)">No fim da viagem…</th><th style="background:var(--ink);text-align:center;width:13mm">Ainda<br>não</th><th style="background:var(--ink);text-align:center;width:13mm">Quase</th><th style="background:var(--ink);text-align:center;width:13mm">Já<br>sei</th></tr>{gt}</table>
  <div class="panel blue" style="margin-top:4mm;padding:3.4mm 4mm"><div class="kicker blue">O texto de que mais gostei foi… porque…</div>{U()}{U()}</div>
  <div class="panel coral" style="margin-top:4mm;padding:3.4mm 4mm"><div class="kicker">Uma coisa que ainda quero treinar</div>{U()}</div>
  <div class="hand" style="margin-top:5mm;font-size:16pt">Próxima paragem: mitos, clássicos e autores.</div>
</div>
<aside style="border-left:.6pt solid var(--rule);padding-left:5mm">
  <div class="kicker blue">Glossário da unidade</div>
  <dl class="gloss" style="margin-top:2.4mm">{gh}</dl>
</aside>
</div>
''', "Chegada")
