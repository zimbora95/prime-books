import parts
from parts import *
from u4_a import sp, stage, scene, CAST
parts.UNIT.update(n=4, total=16)

P = {}

# ---------------------------------------------------------------- 11 THE MYTH (NARRATIVE)
P[11] = page(11, '''
<div class="abs" style="left:0;right:0;top:0;height:112mm"><img class="cover" src="img/icaro.jpg" style="object-position:50% 40%"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:119mm;bottom:15mm;display:flex;flex-direction:column">
  <div class="kicker coral">Estação 4.2 · Ícaro em cena · Texto 1: a narrativa</div>
  <h2 style="margin-top:2mm">Dédalo e Ícaro</h2>
  <div class="reading" style="column-count:2;column-gap:8mm;margin-top:3mm;font-family:FrauncesText;font-size:10pt;line-height:1.47;text-align:left">
    <p>Dédalo era o inventor mais engenhoso de Atenas. Anos antes, fora chamado a Creta pelo rei Minos, para quem construíra o Labirinto, um palácio de corredores tão enredados que quem lá entrava nunca mais encontrava a saída. Quando Dédalo quis regressar a casa, o rei não o deixou partir: ninguém que conhecesse os segredos do Labirinto podia sair da ilha. E assim Dédalo e o filho, Ícaro, ficaram prisioneiros.</p>
    <p style="margin-top:2mm">«Minos pode fechar-me a terra e o mar», pensou Dédalo, «mas o céu não é dele.» Durante semanas, juntou penas de aves, das mais pequenas às maiores, e prendeu-as com fio e com cera, curvando-as como asas verdadeiras. Ícaro brincava ao lado dele, soprando as penas que voavam e amassando a cera com o polegar.</p>
    <p style="margin-top:2mm">Quando as asas ficaram prontas, Dédalo experimentou-as e ergueu-se no ar. Depois, prendeu outras aos ombros do filho e avisou-o de que devia voar sempre a meio caminho: se descesse muito, a água do mar tornaria as penas pesadas; se subisse muito, o calor do sol derreteria a cera.</p>
    <p style="margin-top:2mm">Levantaram voo. Os pescadores que os viam passar julgavam que eram deuses. Ícaro, porém, começou a gostar tanto de voar que se afastou do pai e subiu, subiu, em direção ao céu. O sol amoleceu a cera. Ícaro agitou os braços nus, mas já não havia penas que o segurassem. Chamou pelo pai e caiu no mar, que desde então tem o seu nome: mar Icário.</p>
    <p style="margin-top:2mm">Dédalo chamou-o, desesperado. Quando viu as penas a boiar nas ondas, amaldiçoou a sua própria arte.</p>
  </div>
  <p class="src" style="margin-top:auto">Reconto escrito para esta unidade, a partir do mito grego narrado por Ovídio nas <i>Metamorfoses</i> (livro VIII).</p>
</div>
''', station="4.2 · Ícaro", bleed=True, rh=False)

# ---------------------------------------------------------------- 12-13 THE PLAY
castI = "".join(f'<div style="display:flex;gap:2mm;align-items:baseline"><span style="width:2.4mm;height:2.4mm;border-radius:50%;background:{CAST[k]};display:inline-block;flex:none"></span><b style="font-family:Grotesk;font-size:7.6pt;letter-spacing:.08em">{k}</b><span class="small muted">{v}</span></div>' for k,v in
  [("DÉDALO","inventor"),("ÍCARO","seu filho"),("CORO","pescadores, três ou mais vozes")])
c1 = "".join([
 scene("Cena 1"),
 stage("Uma torre no alto de um penhasco, em Creta. Há penas espalhadas pelo chão. Uma vela acesa derrete um pedaço de cera. DÉDALO prende penas a uma armação de madeira. ÍCARO sopra uma pena para o ar."),
 sp("ÍCARO","Pai, para que queres tantas penas? Vais fazer uma almofada para o rei Minos?"),
 sp("DÉDALO","(sem parar de trabalhar) Para o rei Minos não faço mais nada. Ele fechou-nos a terra e o mar. Mas o céu, Ícaro, o céu não é dele."),
 sp("ÍCARO","(de olhos muito abertos) Vamos voar?"),
 sp("DÉDALO","Vamos voltar para casa. Dá-me essa pena grande."),
 stage("ÍCARO entrega-lha, mas amassa a cera com o polegar."),
 sp("DÉDALO","Não mexas na cera! É ela que segura as penas."),
 sp("ÍCARO","[(à parte) Se a cera é tão fraca… as asas também são?]"),
 stage("DÉDALO prende as asas aos ombros e ergue-se no ar. Luz dourada."),
 sp("DÉDALO","Vês? Agora ouve bem o que te vou dizer. Voa sempre a meio caminho. Se desceres muito, a água do mar molha as penas e puxa-te para baixo. Se subires muito, o sol derrete a cera. Segue-me e não te afastes."),
 sp("ÍCARO","Prometo-te, pai."),
 sp("DÉDALO","(prendendo-lhe as asas, com as mãos a tremer) [(à parte) Nunca tive tanto medo de uma invenção minha.]"),
])
c2 = "".join([
 scene("Cena 2"),
 stage("O céu sobre o mar. Ao fundo, um grande sol suspenso. Em baixo, os pescadores do CORO puxam as redes."),
 sp("CORO","Olhem! Olhem para o céu! — Dois homens com asas! — Serão deuses? — Os deuses não precisam de asas!"),
 stage("DÉDALO voa baixo, sereno. ÍCARO dá voltas cada vez mais largas."),
 sp("ÍCARO","Pai, é tão fácil! O vento leva-me sozinho!"),
 sp("DÉDALO","Fica perto de mim, Ícaro!"),
 sp("ÍCARO","[(à parte, subindo) Só mais um bocadinho. Só quero tocar na luz.]"),
 stage("A luz torna-se branca e quente. Caem penas, uma a uma, sobre o CORO."),
 sp("CORO","Está a chover penas! — A cera derrete! — Ele sobe demais!"),
 sp("ÍCARO","(agitando os braços) Pai! Pai!"),
 stage("Escuridão. Ouve-se um grande som de água. Depois, silêncio. A luz volta, azul e fria. DÉDALO está sozinho, a olhar para o mar."),
 sp("DÉDALO","Ícaro! Ícaro, onde estás? (Apanha uma pena que flutua.) Dei-lhe asas e não lhe dei juízo. Maldita seja a minha arte."),
 sp("CORO","(baixinho) Desde esse dia, este mar chama-se Icário. — E os pescadores contam aos filhos que se deve voar a meio caminho."),
 stage("Fecha o pano."),
])
P[12] = page(12, f'''
<div class="kicker coral">Estação 4.2 · Texto 2: o texto dramático</div>
<h2 style="margin-top:2mm;font-size:30pt">Ícaro em cena</h2>
<p class="small muted" style="margin-top:1.2mm">Adaptação dramática em duas cenas, escrita para esta unidade.</p>
<div class="panel" style="margin-top:4mm;display:grid;grid-template-columns:repeat(3,1fr);gap:1.6mm 5mm;padding:3.6mm 4.5mm"><div class="kicker" style="grid-column:1/-1">Personagens</div>{castI}</div>
<div class="play">{c1}</div>
<div class="panel" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:9.2pt">
  <div><div class="kicker">Adereços da cena 1</div><p style="margin-top:1.4mm">penas · armação de madeira · vela · pedaço de cera · dois pares de asas</p></div>
  <div><div class="kicker">Luz e som</div><p style="margin-top:1.4mm">luz de fim de tarde na torre; luz <b>dourada</b> quando Dédalo se ergue no ar</p></div>
</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(1,"Prever", 'O que achas que vai acontecer na cena 2? Que pistas te dá a cena 1?'+lines(3))}</div>
  <div>{act(2,"Ensaiar", 'Lê a fala «Voa sempre a meio caminho» em três tons: <b>calmo</b>, <b>zangado</b> e <b>aflito</b>. Qual resulta melhor? Porquê?'+lines(3))}</div>
</div>
''', station="4.2 · Ícaro")
P[13] = page(13, f'''<div class="play">{c2}</div>
<div class="panel" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:9.2pt">
  <div><div class="kicker">Luz e som da cena 2</div><p style="margin-top:1.4mm">luz de dia → <b>branca e quente</b> → escuridão → <b>azul e fria</b>; som de água</p></div>
  <div><div class="kicker">Para pensar</div><p style="margin-top:1.4mm">Que diz a mudança de luz sobre o que sente Dédalo no fim?</p></div>
</div>
<div class="rule-card o" style="margin-top:3mm;font-size:9.2pt"><b class="coral">O coro.</b> No teatro grego antigo, um grupo de atores — o <b>coro</b> — comentava a ação e falava ao público. Aqui, os pescadores fazem esse papel: contam o que o público não pode ver e tiram a lição da história. Os travessões separam as vozes diferentes do coro.</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(3,"Interpretar", 'Dédalo diz: «Dei-lhe asas e não lhe dei juízo.» O que quer dizer com isto?'+lines(3))}</div>
  <div>{act(4,"Opinar", 'Qual é a lição que o coro tira da história? Concordas? Dá uma razão.'+lines(3))}</div>
</div>
<div style="margin-top:3mm">{qr("q-ovidio", "Ir à fonte", "As <i>Metamorfoses</i>, de Ovídio, onde o mito foi contado há dois mil anos.")}</div>''', station="4.2 · Ícaro")

# ---------------------------------------------------------------- 14 NARRATIVE -> STAGE
rows = [("Quem conta?","Um narrador.",""),("Como sabemos o que pensam as personagens?","O narrador diz-nos: «pensou Dédalo».",""),("Como se descrevem os lugares?","Com frases descritivas.",""),("Como se mostram as falas?","Às vezes em discurso indireto: «avisou-o de que devia voar…».",""),("Como sabemos o fim?","O narrador conta o que Dédalo sentiu.","")]
tr = "".join(f'<tr><td style="font-size:8.8pt">{a}</td><td style="font-weight:400;color:var(--text);font-size:8.8pt">{b}</td><td style="vertical-align:bottom;height:12mm"><div style="border-bottom:.6pt solid #AEB7C4;height:5mm"></div></td></tr>' for a,b,_ in rows)
P[14] = page(14, f'''
<div class="kicker coral">Estação 4.2 · Educação literária</div>
<h2 style="margin-top:2mm">Da página ao <em>palco</em>: o que muda?</h2>
<table class="cmp ruled" style="margin-top:4mm;table-layout:fixed">
  <tr><th style="background:var(--ink);width:44mm"></th><th style="background:var(--ink)">Na narrativa (p. 11)</th><th style="background:var(--coral)">No texto dramático (pp. 12-13)</th></tr>
  {tr}
</table>
<p class="small muted" style="margin-top:1.4mm">Completa a última coluna.</p>
<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>
{act(1,"Comparar", 'Na narrativa, «Ícaro brincava ao lado dele, soprando as penas». Como passou esta frase para o texto dramático?'+lines(3))}
{act(2,"Descobrir", 'O adaptador <b>acrescentou</b> falas e momentos que não estão na narrativa. Indica dois.'+lines(3))}
{act(3,"Avaliar", 'O coro substitui o narrador? Justifica com um exemplo.'+lines(3))}
</div>
<div>
{act(4,"Transformar", 'Passa para fala de teatro, com indicação cénica: <i>Dédalo avisou-o de que devia voar sempre a meio caminho.</i>'+lines(3))}
{act(5,"Imaginar", 'Se fosses o encenador, como mostrarias a queda de Ícaro no palco da escola, sem pôr ninguém em perigo?'+lines(4))}
</div>
</div>
<div class="rule-card" style="margin-top:auto;font-size:9.3pt"><b class="blue">Em resumo.</b> Quando uma narrativa se torna texto dramático, o <b>narrador desaparece</b>: as descrições passam a <b>indicações cénicas</b>, o discurso indireto passa a <b>falas</b>, e os pensamentos passam a <b>apartes</b> ou a gestos.</div>
''', station="4.2 · Ícaro")

# ---------------------------------------------------------------- 15 GRAMMAR: CD / CI + DIALOGUE PUNCTUATION
P[15] = page(15, f'''
<div class="kicker sea">Estação 4.2 · Gramática</div>
<h2 style="margin-top:2mm">Quem dá o quê <em>a quem</em>?</h2>
<div class="grid2" style="margin-top:4mm;gap:6mm">
  <div class="panel sea">
    <div class="kicker sea">Complemento direto (CD) e indireto (CI)</div>
    <p style="margin-top:1.8mm;font-size:9.4pt">O <b>CD</b> responde a <b>o quê?</b> ou <b>quem?</b> e pode ser substituído por <b>o, a, os, as</b>. O <b>CI</b> responde a <b>a quem?</b> e pode ser substituído por <b>lhe, lhes</b>.</p>
    <p style="margin-top:2.2mm;font-family:FrauncesText;font-size:10pt">Ícaro entregou <b class="sea">a pena</b> <b class="coral">ao pai</b>.</p>
    <p class="small" style="margin-top:.6mm"><b class="sea">CD</b>: a pena → <i>entregou-a</i> · <b class="coral">CI</b>: ao pai → <i>entregou-lhe</i></p>
    <p style="margin-top:2mm;font-size:9.2pt">Os dois juntos: <i>entregou-<b>lha</b></i> (lhe + a) — tal como na indicação cénica da página 12.</p>
  </div>
  <div class="panel coral">
    <div class="kicker">Pontuar o diálogo</div>
    <p style="margin-top:1.8mm;font-size:9.3pt"><b>Na narrativa</b>, as falas abrem com travessão, em parágrafo novo:</p>
    <p style="margin-top:1mm;font-family:FrauncesText;font-size:9.8pt">— Fica perto de mim! — gritou Dédalo.</p>
    <p style="margin-top:2mm;font-size:9.3pt"><b>No texto dramático</b>, escreve-se o nome da personagem e a fala; as indicações vão entre parênteses:</p>
    <p style="margin-top:1mm;font-family:FrauncesText;font-size:9.8pt"><b style="font-family:Grotesk;font-size:7.6pt">DÉDALO</b> <i>(gritando)</i> Fica perto de mim!</p>
  </div>
</div>
{act(1,"Identificar", 'Sublinha o CD a azul e o CI a coral.<div style="font-family:FrauncesText;font-size:10pt;line-height:1.75;margin-top:1.6mm">Dá-me essa pena grande.<br>Dédalo prendeu as asas aos ombros do filho.<br>Os pescadores contam a história aos filhos.</div>',"sea")}
{act(2,"Substituir", 'Reescreve, substituindo o CD e o CI pelos pronomes.<div style="display:grid;grid-template-columns:62mm 1fr;gap:2.4mm 4mm;margin-top:1.8mm;font-size:9.6pt;align-items:end"><i>Dédalo explicou o plano ao filho.</i><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><i>O rei negou a partida a Dédalo.</i><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><i>Ariadne deu o novelo a Teseu.</i><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div>',"sea")}
{act(3,"Transformar", 'Passa este diálogo de narrativa para texto dramático.<div style="font-family:FrauncesText;font-size:9.8pt;line-height:1.55;margin-top:1.6mm">— Pai, é tão fácil! — exclamou Ícaro, a rir.<br>— Não te afastes! — respondeu Dédalo, assustado.</div>'+lines(4))}
<div class="panel sea" style="margin-top:auto">
{act(4,"Escrever", 'Escreve duas falas novas para o coro, na cena 2. Numa delas usa um <b>CD</b> e, na outra, um <b>CI</b>. Sublinha-os.'+lines(3),"sea")}
</div>
''', station="4.2 · Ícaro")

# ---------------------------------------------------------------- 16 WRITING: TWO SCENES + CHECK
P[16] = page(16, f'''
<div class="kicker">Estação 4.2 · Escrita · Chegada</div>
<h2 style="margin-top:2mm">Do episódio às <em>duas cenas</em></h2>
<div class="panel" style="margin-top:3mm;font-family:FrauncesText;font-size:9.8pt;line-height:1.48">
  <div class="kicker" style="font-family:Grotesk">Episódio: Teseu e o fio de Ariadne</div>
  <p style="margin-top:1.6mm">Teseu chegou a Creta para enfrentar o Minotauro, o monstro que vivia no centro do Labirinto. Ariadne, filha do rei Minos, quis ajudá-lo. Na véspera, foi ter com ele às escondidas e deu-lhe um novelo de fio. Explicou-lhe que devia prender a ponta à entrada e ir desenrolando o fio pelos corredores; depois de vencer o monstro, só teria de o seguir para voltar. Teseu agradeceu-lhe. No dia seguinte, entrou no Labirinto. No escuro, ouviu o bramido do Minotauro e apertou o fio com força.</p>
  <p class="src" style="margin-top:1mm;font-family:Body">Reconto do mito grego, escrito para esta unidade.</p>
</div>
{act(1,"Planear", 'Divide o episódio em duas cenas.<div style="display:grid;grid-template-columns:18mm 1fr;gap:2.4mm 3mm;margin-top:2mm;align-items:end;font-size:9.4pt"><b class="coral">Cena 1</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><b class="coral">Cena 2</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div>')}
{act(2,"Escrever", 'Escreve as duas cenas no caderno: personagens, indicação cénica inicial em cada cena, falas, <b>um aparte</b> e pelo menos um <b>CD</b> e um <b>CI</b> nas falas. Começa aqui:<div class="play" style="margin-top:1.4mm"><div class="scene" style="margin-top:0">Cena 1</div></div>'+lines(5))}
<div class="kicker blue" style="margin-top:auto">Consegues? Autoavaliação da Unidade 4</div>
<table class="cmp" style="margin-top:2mm">
<tr><th style="background:var(--ink)">Consigo…</th><th style="background:var(--ink);text-align:center;width:12mm">Sim</th><th style="background:var(--ink);text-align:center;width:12mm">Quase</th><th style="background:var(--coral);text-align:center;width:16mm">Ainda não</th></tr>
''' + "".join(f'<tr><td style="font-weight:400;color:var(--text)">{c}</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk o"></span></td></tr>' for c in
 ["identificar ato, cena, fala, aparte e indicações cénicas.","representar uma cena, distinguindo falas e apartes.","explicar o que muda da narrativa para o teatro.","distinguir frase simples de frase complexa e usar o vocativo.","identificar o CD e o CI e pontuar o diálogo."]) + '</table>', station="Chegada")
