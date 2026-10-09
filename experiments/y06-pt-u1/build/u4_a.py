import parts
from parts import *
parts.UNIT.update(n=4, total=16)

P = {}
CAST = {"INÊS": "var(--coral)", "TOMÁS": "var(--ink)", "DUARTE": "var(--sea)",
        "PROFESSORA HELENA": "#6B4E9B", "SENHOR ABÍLIO": "#7A5C2E",
        "DÉDALO": "var(--ink)", "ÍCARO": "var(--coral)", "CORO": "var(--sea)"}

def sp(who, text):
    """One speech. (…) = stage direction, [à parte …] = aside."""
    import re
    text = re.sub(r"\[(.+?)\]", r'<span class="aside">\1</span>', text)
    text = re.sub(r"\((.+?)\)", r'<span class="did">(\1)</span>', text)
    label = who.replace("PROFESSORA ", "PROF.ª ").replace("SENHOR ", "SR. ")
    return f'<div class="sp"><div class="who" style="color:{CAST[who]}">{label}</div><div>{text}</div></div>'
def stage(t): return f'<div class="stage">{t}</div>'
def scene(t): return f'<div class="scene">{t}</div>'

# ---------------------------------------------------------------- 1 OPENER
P[1] = page(1, '''
<div class="abs" style="left:0;right:0;top:0;height:140mm"><img class="cover" src="img/palco.jpg"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:150mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">4</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 4 · Texto dramático</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">O palco das<br><em>escolhas</em></h1>
    </div>
  </div>
  <p class="lead" style="margin-top:6mm;font-size:12.6pt">Um texto dramático não foi escrito só para ser lido: foi escrito para ganhar corpo, voz e movimento num palco. Nesta unidade, vais ler uma peça sobre uma escolha difícil, ver um mito antigo transformado em teatro — e vais escrever e representar as tuas próprias cenas.</p>
  <div class="panel" style="margin-top:7mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4.5mm 5mm">
    <div class="display" style="font-size:26pt;color:var(--ink);line-height:1">3 min</div>
    <div style="font-size:10.2pt"><b class="blue">Quadro vivo.</b> Em grupos de três, escolham uma destas situações e mostrem-na à turma como uma fotografia, <b>sem falar e sem se mexer</b>: <i>encontrar uma carteira no chão · partir um objeto de alguém · ver um colega a copiar</i>. A turma adivinha: que escolha vai cada personagem fazer?</div>
  </div>
  <div style="margin-top:auto;display:grid;grid-template-columns:repeat(2,1fr);gap:4mm">
    <div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><div class="kicker blue">4.1</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.4pt;margin-top:.8mm">O julgamento da escolha</div></div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:2mm"><div class="kicker coral">4.2</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.4pt;margin-top:.8mm">Ícaro em cena</div></div>
  </div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 ROUTE + VOCABULARY OF THEATRE
st = [("4.1","O julgamento da escolha","peça num ato e três cenas · representação · uma cena nova","3","var(--ink)"),
      ("4.2","Ícaro em cena","do mito ao palco · o que muda · duas cenas tuas","11","var(--coral)")]
sthtml = "".join(f'''<div style="display:grid;grid-template-columns:17mm 1fr 12mm;gap:4mm;align-items:center;padding:3.4mm 0;border-top:.6pt solid var(--rule)">
  <div class="display" style="font-size:24pt;line-height:1;color:{c}">{n}</div>
  <div><div style="font-family:FrauncesText;font-weight:700;font-size:12pt;color:var(--ink)">{t}</div><div class="small muted">{g}</div></div>
  <div style="font-family:Grotesk;font-weight:700;font-size:8pt;color:{c};text-align:right">p. {p}</div></div>''' for n,t,g,p,c in st)
terms = [("Ato","Grande parte de uma peça. Esta peça tem um só ato: é uma peça num ato."),
         ("Cena","Parte do ato. Em regra, muda de cena quando entra ou sai uma personagem, ou quando muda o lugar."),
         ("Fala","O que cada personagem diz. Vem a seguir ao nome da personagem."),
         ("Aparte","Fala que a personagem diz para o público, como se as outras personagens não a ouvissem."),
         ("Indicações cénicas","Informações sobre o cenário, os gestos, o tom de voz, a luz, as entradas e saídas. Escrevem-se entre parênteses e em itálico."),
         ("Personagens","Lista de quem entra na peça, no início do texto.")]
th = "".join(f'<div style="border-top:.6pt solid var(--rule);padding:2.4mm 0;display:grid;grid-template-columns:33mm 1fr;gap:3mm"><b class="blue" style="font-family:FrauncesText;font-size:10.6pt">{a}</b><span style="font-size:9.4pt">{b}</span></div>' for a,b in terms)
P[2] = page(2, f'''
<div class="kicker">Antes de começar</div>
<h2 style="margin-top:2mm">A rota desta unidade</h2>
<div style="margin-top:4mm">{sthtml}</div>
<div class="grid2" style="margin-top:6mm;grid-template-columns:1.15fr 1fr;gap:7mm">
  <div>
    <div class="kicker blue">O vocabulário do teatro</div>
    <div style="margin-top:2mm">{th}</div>
  </div>
  <div>
    <h3>No fim da unidade, vais conseguir…</h3>
    <ul style="list-style:none;margin-top:2.6mm;font-size:9.5pt;line-height:1.36">
      <li style="margin-top:1.8mm"><span class="chk"></span>identificar <b>ato</b>, <b>cena</b>, <b>fala</b>, <b>aparte</b> e <b>indicações cénicas</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>ler e <b>representar</b> uma peça;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>explicar a relação entre uma <b>escolha</b> e a sua <b>consequência</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>explicar o que muda quando uma narrativa passa a <b>teatro</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>escrever cenas com falas, apartes e indicações;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>distinguir <b>frase simples</b> de <b>frase complexa</b> e usar o <b>vocativo</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>identificar o <b>complemento direto</b> e o <b>indireto</b>, e pontuar o diálogo.</li>
    </ul>
    <div class="rule-card o" style="margin-top:5mm;font-size:9.2pt"><b class="coral">Como se lê uma peça.</b> Não há narrador. Tudo o que sabes vem das <b>falas</b> e das <b>indicações cénicas</b>. Lê as indicações com atenção: são as instruções para quem vai pôr a peça em cena.</div>
  </div>
</div>
<div class="grid2" style="margin-top:6mm;grid-template-columns:1.25fr 1fr;gap:6mm;align-items:stretch">
  <div><div class="kicker">Os textos que vais ler</div><div style="display:grid;gap:3mm;margin-top:2.4mm"><div style="border-left:1.2mm solid var(--ink);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--ink)">P. 3 · PEÇA ORIGINAL</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">O julgamento da escolha</div><div class="small muted">um ato, três cenas</div></div><div style="border-left:1.2mm solid var(--coral);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--coral)">P. 11 · MITO</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">Dédalo e Ícaro</div><div class="small muted">reconto a partir de Ovídio</div></div><div style="border-left:1.2mm solid var(--coral);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--coral)">P. 12 · ADAPTAÇÃO</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">Ícaro em cena</div><div class="small muted">o mito em duas cenas</div></div></div></div>
  <div class="panel" style="padding:3.6mm 4mm;display:flex;flex-direction:column"><div class="kicker blue">Onde começou o teatro português?</div><p style="font-size:9pt;line-height:1.45;margin-top:1.6mm">Em 1502, para celebrar o nascimento do futuro rei D. João III, <b>Gil Vicente</b> apresentou o <i>Monólogo do Vaqueiro</i> (ou <i>Auto da Visitação</i>). É considerado o início do teatro em Portugal — e Gil Vicente, o «pai do teatro português».</p><div style="margin-top:auto;padding-top:2mm">{qr("q-gilvicente", "Conhecer", "Gil Vicente na Wikipédia.")}</div></div>
</div>
''', station="A rota")

# ---------------------------------------------------------------- 3-5 THE PLAY
cast = "".join(f'<div style="display:flex;gap:2mm;align-items:baseline"><span style="width:2.4mm;height:2.4mm;border-radius:50%;background:{CAST[k]};display:inline-block;flex:none"></span><b style="font-family:Grotesk;font-size:7.6pt;letter-spacing:.08em">{k}</b><span class="small muted">{v}</span></div>' for k,v in
  [("INÊS","11 anos, aluna do 6.º B"),("TOMÁS","11 anos, colega de turma"),("DUARTE","11 anos, colega de turma"),("PROFESSORA HELENA","diretora de turma"),("SENHOR ABÍLIO","jardineiro da escola")])
cena1 = "".join([
 scene("Cena 1"),
 stage("Recreio da escola. Ao fundo, a estufa onde a turma do 6.º B cultiva tomates e manjericos. TOMÁS faz toques com a bola. INÊS está sentada num banco, a ler."),
 sp("TOMÁS","Inês, vê só! Vinte toques sem deixar cair!"),
 sp("INÊS","(sem levantar os olhos) Estou a ler, Tomás. E o Senhor Abílio já disse que não se joga à bola ao pé da estufa."),
 sp("TOMÁS","O Senhor Abílio está no refeitório. Vinte e um… vinte e dois…"),
 stage("A bola foge-lhe do pé. Ouve-se um vidro a partir-se. Silêncio."),
 sp("INÊS","(levantando-se de um salto) Tomás!"),
 sp("TOMÁS","Não fui eu. Quer dizer… fui, mas não foi de propósito."),
 sp("INÊS","Temos de contar à professora."),
 sp("TOMÁS","Temos? Tu não fizeste nada. Inês, por favor, não digas a ninguém. Se a minha mãe sabe, fico sem o torneio de sábado."),
 sp("INÊS","[(à parte) E agora? Se conto, ele fica zangado comigo. Se não conto… a estufa é de todos.]"),
 sp("TOMÁS","Promete."),
 stage("Toca a campainha. TOMÁS apanha a bola e sai a correr. INÊS fica sozinha, a olhar para o vidro partido."),
 sp("INÊS","Eu não prometi nada."),
])
cena2 = "".join([
 scene("Cena 2"),
 stage("Sala de aula. A PROFESSORA HELENA está junto ao quadro. Os alunos estão sentados. DUARTE tem as mãos sujas de terra."),
 sp("PROFESSORA HELENA","Meninos, o Senhor Abílio encontrou um vidro da estufa partido. Alguém sabe o que aconteceu?"),
 stage("Silêncio. TOMÁS olha para o chão."),
 sp("PROFESSORA HELENA","Duarte, tu estiveste na estufa ao intervalo, não estiveste?"),
 sp("DUARTE","Estive, professora. Fui regar os manjericos. Mas, quando lá cheguei, o vidro já estava partido!"),
 sp("TOMÁS","[(à parte) Ninguém viu. Ninguém vai saber.]"),
 sp("PROFESSORA HELENA","Tens as mãos cheias de terra, Duarte…"),
 sp("DUARTE","Porque estive a regar! Não fui eu!"),
 sp("INÊS","[(à parte) O Duarte vai ser castigado por uma coisa que não fez. E eu sei a verdade.]"),
 sp("PROFESSORA HELENA","Amanhã, na assembleia de turma, falamos sobre isto. Quem souber alguma coisa ainda tem tempo para falar."),
 stage("Os alunos saem. INÊS aproxima-se de TOMÁS."),
 sp("INÊS","Tomás, tens até amanhã."),
 sp("TOMÁS","Ou quê? Vais fazer queixa de mim?"),
 sp("INÊS","Vou fazer o que está certo. Espero que tu também."),
 stage("INÊS sai. TOMÁS fica sozinho, com a bola nas mãos."),
 sp("TOMÁS","[(à parte, baixinho) Um vidro. Só um vidro… Porque é que pesa tanto?]"),
])
cena3 = "".join([
 scene("Cena 3"),
 stage("Assembleia de turma. As mesas estão em círculo. A PROFESSORA HELENA preside. O SENHOR ABÍLIO está de pé, junto à porta, com o boné na mão."),
 sp("PROFESSORA HELENA","Está aberta a assembleia. Primeiro ponto: o vidro da estufa."),
 sp("DUARTE","(levantando-se) Eu repito: não fui eu."),
 sp("SENHOR ABÍLIO","Encontrei isto dentro da estufa. (Mostra a bola.) O Duarte não tinha bola nenhuma."),
 stage("Todos olham para TOMÁS. INÊS levanta o braço."),
 sp("INÊS","Senhora professora, posso falar?"),
 sp("PROFESSORA HELENA","Fala, Inês."),
 sp("INÊS","[(à parte, com a voz a tremer) É agora.]"),
 stage("Pausa. TOMÁS põe-se de pé antes de ela falar."),
 sp("TOMÁS","Fui eu. Parti o vidro com a bola, sem querer, e deixei o Duarte ficar com a culpa. Desculpa, Duarte."),
 sp("DUARTE","(depois de um silêncio) Podias ter dito logo."),
 sp("TOMÁS","Podia. Tive medo."),
 sp("PROFESSORA HELENA","Obrigada, Tomás. Dizer a verdade custa. Mas repara: o vidro continua partido. O que propões?"),
 sp("TOMÁS","Ajudo o Senhor Abílio a arranjá-lo. E ponho o dinheiro que tinha juntado para o torneio."),
 sp("SENHOR ABÍLIO","Aceito o ajudante. Traz luvas, rapaz, que o vidro corta."),
 sp("INÊS","[(à parte, sorrindo) Às vezes, a melhor escolha é dar tempo ao outro para escolher bem.]"),
 stage("As luzes baixam sobre a turma. Só INÊS e TOMÁS ficam iluminados."),
 sp("TOMÁS","Obrigado por esperares."),
 sp("INÊS","Obrigada por não me obrigares a falar por ti."),
 stage("Fecha o pano."),
])
P[3] = page(3, f'''
<div class="kicker blue">Estação 4.1 · Texto dramático</div>
<h2 style="margin-top:2mm;font-size:30pt">O julgamento da escolha</h2>
<p class="small muted" style="margin-top:1.2mm">Peça num ato e três cenas, escrita para esta unidade.</p>
<div class="panel" style="margin-top:4mm;display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 6mm;padding:3.6mm 4.5mm">
  <div class="kicker" style="grid-column:1/-1">Personagens</div>{cast}
</div>
<div class="play" style="margin-top:1mm">{cena1}</div>
<div style="margin-top:4mm">{act(1,"Prever", 'Quem achas que partiu o vidro? Escreve o teu palpite antes de virares a página — e confirma-o depois.'+lines(2))}</div>
    <div class="panel blue" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:9.3pt">
  <div><div class="kicker blue">Antes de ler</div><p style="margin-top:1.4mm">Já tiveste de escolher entre proteger um amigo e dizer a verdade? O que decidiste — e o que aconteceu depois?</p></div>
  <div><div class="kicker blue">Enquanto lês</div><p style="margin-top:1.4mm">Lê as falas em voz baixa e as indicações cénicas em silêncio. Imagina o palco: onde está cada personagem?</p></div>
</div>
<div class="rule-card" style="margin-top:3mm;font-size:8.8pt;display:flex;gap:5mm"><span><span class="did" style="font-family:FrauncesText">(itálico entre parênteses)</span> = indicação cénica</span><span><span class="aside" style="font-family:FrauncesText">fundo coral</span> = aparte</span></div>
''', station="4.1 · A escolha")
P[4] = page(4, f'''<div class="play">{cena2}</div>
<div class="panel coral" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center">
  <div class="hand" style="font-size:15pt;line-height:1.1;max-width:40mm">Pausa para pensar</div>
  <div style="font-size:9.6pt">O público sabe mais do que a professora. <b>Como é que sabe?</b> E o que farias tu, no lugar da Inês, antes da assembleia? Discute com o teu colega antes de virares a página.</div>
</div>
<div class="panel" style="margin-top:4mm;padding:3.6mm 4.4mm"><div class="kicker">O diário da Inês</div><p class="small" style="margin-top:1mm">Nessa noite, a Inês escreveu no diário. Escreve tu, na 1.ª pessoa, o que ela sentiu e o que decidiu.</p><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div>''', station="4.1 · A escolha")
P[5] = page(5, f'''<div class="play">{cena3}</div>
<div class="panel blue" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:9.3pt">
  <div><div class="kicker blue">Depois de ler · oralmente</div><p style="margin-top:1.4mm">Porque é que o Tomás se levanta <b>antes</b> de a Inês falar? O que teria mudado se fosse ela a contar?</p><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div>
  <div><div class="kicker blue">A última fala</div><p style="margin-top:1.4mm">Lê a última fala da Inês. O que agradece ela, exatamente? Explica por palavras tuas.</p><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div>
</div>
<p class="src" style="margin-top:2mm">Texto dramático original, escrito para esta unidade.</p>''', station="4.1 · A escolha")

# ---------------------------------------------------------------- 6 COMPREHENSION: CHOICE & CONSEQUENCE
P[6] = page(6, f'''
<div class="kicker blue">Estação 4.1 · Compreender</div>
<h2 style="margin-top:2mm">Cada escolha tem uma <em>consequência</em></h2>
<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>
{act(1,"Localizar", 'Onde se passa cada cena? Quem está em palco?<div style="display:grid;grid-template-columns:16mm 1fr;gap:2.4mm 3mm;margin-top:2mm;align-items:end"><b class="blue">Cena 1</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><b class="blue">Cena 2</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><b class="blue">Cena 3</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div>',"blue")}
{act(2,"Interpretar", 'No fim da cena 1, a Inês diz: «Eu não prometi nada.» O que quer ela dizer?'+lines(3),"blue")}
{act(3,"Inferir", 'Porque é que o Duarte parece culpado? Que indicação cénica o sugere?'+lines(3),"blue")}
{act(4,"Relacionar", 'O que descobrimos pelos <b>apartes</b> que as outras personagens não sabem?'+lines(5),"blue")}
</div>
<div>
  <div class="kicker coral">Mapa das escolhas</div>
  <p class="small" style="margin-top:1.4mm">Completa: para cada escolha, a consequência que teve (ou teria tido).</p>
  <div style="display:grid;grid-template-columns:1fr 6mm 1fr;gap:3mm 0;align-items:center;margin-top:3mm;font-size:9pt">
    <div class="panel" style="padding:2.6mm">Tomás joga à bola junto à estufa.</div><b class="coral" style="text-align:center">→</b><div class="panel coral" style="padding:2.6mm;min-height:18mm"></div>
    <div class="panel" style="padding:2.6mm">Tomás pede à Inês que não conte.</div><b class="coral" style="text-align:center">→</b><div class="panel coral" style="padding:2.6mm;min-height:18mm"></div>
    <div class="panel" style="padding:2.6mm">A Inês dá um prazo ao Tomás.</div><b class="coral" style="text-align:center">→</b><div class="panel coral" style="padding:2.6mm;min-height:18mm"></div>
    <div class="panel" style="padding:2.6mm">Tomás confessa na assembleia.</div><b class="coral" style="text-align:center">→</b><div class="panel coral" style="padding:2.6mm;min-height:18mm"></div>
    <div class="panel" style="padding:2.6mm"><i>E se a Inês nunca tivesse falado?</i></div><b class="coral" style="text-align:center">→</b><div class="panel coral" style="padding:2.6mm;min-height:18mm"></div>
  </div>
  {act(5,"Opinar", 'O título é «O julgamento da escolha». Quem é julgado, afinal? Dá a tua opinião com um argumento.'+lines(4))}
</div>
</div>
<div class="panel blue" style="margin-top:auto">
{act(6,"Debater", 'Em grupo: a Inês devia ter contado logo à professora, na cena 1? Cada grupo escolhe uma posição e apresenta dois argumentos à turma. Regista a posição do teu grupo e os argumentos.'+lines(3),"blue")}
</div>
''', station="4.1 · A escolha")

# ---------------------------------------------------------------- 7 ANATOMY OF A PLAY
def tagc(t,c): return f'<span style="font-family:Grotesk;font-weight:700;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:{c};border-radius:1mm;padding:.5mm 1.4mm;white-space:nowrap">{t}</span>'
P[7] = page(7, f'''
<div class="kicker">Estação 4.1 · Como se constrói uma peça</div>
<h2 style="margin-top:2mm">Anatomia do texto dramático</h2>
<div class="panel" style="margin-top:4mm;padding:5mm 6mm">
  <div style="display:grid;grid-template-columns:1fr 42mm;gap:4mm;align-items:center">
    <div class="play" style="margin:0"><div class="scene" style="margin-top:0">Cena 1</div></div><div>{tagc("divisão em cena","var(--coral)")}</div>
    <div class="play"><div class="stage" style="margin-left:0">Recreio da escola. Ao fundo, a estufa…</div></div><div>{tagc("indicação cénica: cenário","#4A5568")}</div>
    <div class="play">{sp("TOMÁS","Inês, vê só! Vinte toques sem deixar cair!")}</div><div>{tagc("nome + fala","var(--ink)")}</div>
    <div class="play">{sp("INÊS","(sem levantar os olhos) Estou a ler, Tomás.")}</div><div>{tagc("indicação: gesto","#4A5568")}</div>
    <div class="play">{sp("INÊS","[(à parte) E agora? Se conto, ele fica zangado comigo.]")}</div><div>{tagc("aparte","var(--coral)")}</div>
    <div class="play"><div class="stage" style="margin-left:0">Ouve-se um vidro a partir-se. Silêncio.</div></div><div>{tagc("indicação: som","#4A5568")}</div>
  </div>
</div>
<div class="grid2" style="margin-top:5mm;gap:7mm">
<div>
{act(1,"Contar", 'Quantas falas tem a Inês na cena 3? E quantas delas são apartes?'+lines(2))}
{act(2,"Classificar", 'Copia uma indicação cénica de cada tipo.<div style="display:grid;grid-template-columns:20mm 1fr;gap:2.4mm 3mm;margin-top:2mm;align-items:end;font-size:9.4pt"><b>luz</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><b>tom de voz</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><b>objeto</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><b>movimento</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div>')}
</div>
<div>
{act(3,"Explicar", 'Porque é que, num texto dramático, as indicações cénicas são tão importantes? Pensa em quem as vai ler.'+lines(3))}
{act(4,"Transformar", 'Escreve como aparte o que o Duarte pode estar a pensar quando a professora olha para as mãos dele.'+lines(3))}
</div>
</div>
<div class="panel coral" style="margin-top:auto">
{act(5,"Experimentar", 'Em pares, leiam as falas do quadro duas vezes: primeiro <b>ignorando</b> as indicações cénicas, depois <b>cumprindo-as</b>. O que mudou na forma como o público entende a cena?'+lines(2))}
</div>
''', station="4.1 · A escolha")

# ---------------------------------------------------------------- 8 STAGING
roles = [("Encenador","decide onde fica cada ator e dá as indicações"),("Atores","cinco personagens"),("Ponto","segue o texto e ajuda quem se esquece"),("Contra-regra","adereços: bola, boné, livro, mesas"),("Luz e som","o vidro a partir, a campainha, o foco final")]
rh = "".join(f'<div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><b class="blue" style="font-size:9.6pt">{a}</b><div class="small muted" style="margin-top:.6mm">{b}</div></div>' for a,b in roles)
P[8] = page(8, f'''
<div class="kicker">Estação 4.1 · Oralidade</div>
<h2 style="margin-top:2mm">Pôr a peça <em>em cena</em></h2>
<p class="lead" style="margin-top:3mm">Um texto dramático só fica completo quando é representado. Organizem a turma numa pequena companhia de teatro.</p>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin-top:5mm">{rh}</div>
<div class="grid2" style="margin-top:6mm;gap:6mm">
  <div class="panel blue">
    <div class="kicker blue">Ensaio em quatro passos</div>
    <ol style="margin:2.4mm 0 0 4.5mm;font-size:9.6pt;line-height:1.45">
      <li><b>Leitura à mesa</b>: leiam a peça sentados, cada um com a sua personagem.</li>
      <li><b>Marcação</b>: decidam onde fica e para onde anda cada ator.</li>
      <li><b>Apartes</b>: quem diz um aparte vira-se para o público e baixa um pouco a voz.</li>
      <li><b>Ensaio geral</b>: com adereços, luz, som e sem texto na mão.</li>
    </ol>
  </div>
  <div class="panel">
    <div class="kicker">Planta do palco</div>
    <p class="small" style="margin-top:1mm">Desenha onde ficam a estufa, o banco e as mesas na cena que vão representar.</p>
    <div style="margin-top:2mm;height:46mm;border:.8pt dashed #AEB7C4;background:#fff;border-radius:2mm;position:relative"><span class="small muted" style="position:absolute;bottom:1.4mm;left:0;right:0;text-align:center">PÚBLICO</span></div>
  </div>
</div>
<div class="kicker" style="margin-top:6mm">Avaliação da representação</div>
<table class="cmp ruled" style="margin-top:2mm">
  <tr><th style="background:var(--ink)">Critério</th><th style="background:var(--ink);text-align:center">A melhorar</th><th style="background:var(--ink);text-align:center">Bom</th><th style="background:var(--ink);text-align:center">Muito bom</th></tr>
  <tr><td>Sabem o texto</td><td></td><td></td><td></td></tr>
  <tr><td>Voz clara e audível</td><td></td><td></td><td></td></tr>
  <tr><td>Os apartes distinguem-se das falas</td><td></td><td></td><td></td></tr>
  <tr><td>Gestos e movimentos seguem as indicações</td><td></td><td></td><td></td></tr>
  <tr><td>Respeitam as deixas (sem silêncios longos)</td><td></td><td></td><td></td></tr>
</table>
<div style="margin-top:auto"><b class="blue" style="font-size:9.6pt">Notas do encenador para o próximo ensaio</b>{lines(4)}</div>
''', station="4.1 · A escolha")

# ---------------------------------------------------------------- 9 GRAMMAR: SIMPLE / COMPLEX SENTENCE + VOCATIVE
P[9] = page(9, f'''
<div class="kicker sea">Estação 4.1 · Gramática</div>
<h2 style="margin-top:2mm">Frase simples, frase complexa e <em>vocativo</em></h2>
<div class="grid2" style="margin-top:4mm;gap:6mm;align-items:stretch">
  <div class="panel sea">
    <div class="kicker sea">Frase simples e frase complexa</div>
    <p style="margin-top:1.8mm;font-size:9.5pt">Conta as <b>formas verbais</b>. Uma frase com <b>uma só</b> forma verbal é uma <b>frase simples</b>. Uma frase com <b>duas ou mais</b> formas verbais é uma <b>frase complexa</b>.</p>
    <p style="margin-top:2mm;font-family:FrauncesText;font-size:10pt">Tomás <b class="sea">confessou</b>. <span class="small muted" style="font-family:Body">→ simples</span></p>
    <p style="margin-top:1.4mm;font-family:FrauncesText;font-size:10pt">Tomás <b class="sea">confessou</b> e o Duarte <b class="sea">perdoou</b>. <span class="small muted" style="font-family:Body">→ complexa</span></p>
    <p style="margin-top:1.4mm;font-family:FrauncesText;font-size:10pt">Se a minha mãe <b class="sea">sabe</b>, <b class="sea">fico</b> sem o torneio. <span class="small muted" style="font-family:Body">→ complexa</span></p>
  </div>
  <div class="panel coral">
    <div class="kicker">Vocativo</div>
    <p style="margin-top:1.8mm;font-size:9.5pt">É a palavra ou expressão com que <b>chamamos</b> alguém. Não faz parte do sujeito nem do predicado e separa-se sempre por <b>vírgula</b>.</p>
    <p style="margin-top:2mm;font-family:FrauncesText;font-size:10pt"><b class="coral">Inês</b>, vê só!</p>
    <p style="margin-top:1.4mm;font-family:FrauncesText;font-size:10pt">Traz luvas, <b class="coral">rapaz</b>, que o vidro corta.</p>
    <p style="margin-top:2mm;font-size:9.2pt">Cuidado: em <i>A Inês lê.</i>, «a Inês» é o <b>sujeito</b>, não um vocativo.</p>
  </div>
</div>
{act(1,"Classificar", 'Escreve <b>S</b> (simples) ou <b>C</b> (complexa).<div style="display:grid;grid-template-columns:1fr 9mm;gap:1.8mm 3mm;margin-top:2mm;font-size:9.6pt"><span>Todos olham para o Tomás.</span><span class="chk"></span><span>Fui regar os manjericos, mas o vidro já estava partido.</span><span class="chk"></span><span>Está aberta a assembleia.</span><span class="chk"></span><span>Quem souber alguma coisa ainda tem tempo para falar.</span><span class="chk"></span></div>',"sea")}
{act(2,"Encontrar", 'Na peça, sublinha cinco vocativos. Copia dois e diz quem fala a quem.'+lines(2))}
{act(3,"Pontuar", 'Coloca as vírgulas do vocativo.<div style="font-family:FrauncesText;font-size:10.2pt;line-height:1.7;margin-top:1.6mm">Duarte tu estiveste na estufa?<br>Obrigada Tomás por teres falado.<br>Senhor Abílio posso ajudar?</div>')}
{act(4,"Transformar", 'Junta as duas frases simples numa frase complexa. <i>O Tomás partiu o vidro. Ele teve medo.</i>'+lines(2),"sea")}
{act(5,"Escrever", 'Escreve uma fala para o Senhor Abílio com um <b>vocativo</b> e uma <b>frase complexa</b>.'+lines(2))}
''', station="4.1 · A escolha")

# ---------------------------------------------------------------- 10 WRITING: A NEW SCENE
P[10] = page(10, f'''
<div class="kicker">Estação 4.1 · Escrita</div>
<h2 style="margin-top:2mm">Cena 4: uma semana depois</h2>
<p class="lead" style="margin-top:3mm">Tomás cumpre o que prometeu e vai ajudar o Senhor Abílio a arranjar o vidro da estufa. O Duarte aparece. Escreve essa cena.</p>
<div class="grid3" style="margin-top:4mm">
  <div class="panel"><div class="kicker blue">Onde e quando?</div><p class="small" style="margin-top:1.4mm">Escreve a indicação cénica inicial: lugar, luz, quem está em palco.</p>{lines(2)}</div>
  <div class="panel"><div class="kicker blue">O que acontece?</div><p class="small" style="margin-top:1.4mm">Há um pequeno problema ou uma nova escolha?</p>{lines(2)}</div>
  <div class="panel coral"><div class="kicker">Como acaba?</div><p class="small" style="margin-top:1.4mm">Com uma fala, um gesto ou uma indicação de luz?</p>{lines(2)}</div>
</div>
{act(1,"Escrever", 'Escreve a cena com <b>pelo menos oito falas</b>, <b>um aparte</b> e <b>três indicações cénicas</b>. Usa a pontuação do texto dramático: o nome da personagem antes de cada fala e as indicações cénicas entre parênteses.')}
{lines(20)}
<div style="display:flex;gap:5mm;flex-wrap:wrap;margin-top:auto;font-size:8.8pt;border-top:.6pt solid var(--rule);padding-top:3mm">
  <span><span class="chk"></span>indicação cénica inicial</span><span><span class="chk"></span>8 falas ou mais</span><span><span class="chk"></span>1 aparte</span><span><span class="chk"></span>3 indicações</span><span><span class="chk"></span>1 vocativo</span><span><span class="chk"></span>sem narrador</span>
</div>
''', station="4.1 · A escolha")
