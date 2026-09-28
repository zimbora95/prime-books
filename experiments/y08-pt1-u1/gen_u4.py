"""Generate src/u4.html — Unidade 4 · Texto dramático (Y8 PT)."""
import pathlib
R = pathlib.Path(__file__).parent


def rail(t): return f'<div class="rail"><span>{t}</span></div>'
def folio(t): return f'<div class="folio"><span class="n"></span><span class="t">{t}</span></div>'


def page(id_, cls, railt, inner, foliot=None):
    return f'''
<section id="{id_}" class="page v-dra {cls}">
  {rail(railt)}
  <div class="inner">
{inner}
  </div>
  {folio(foliot or railt)}
</section>'''


def cite(txt, src):
    return f'<blockquote class="cq dq"><p>{txt}</p><cite>{src}</cite></blockquote>'


# ---------- a tiny play-script renderer: lines are  NAME: speech  |  (didascália)  |  ## CENA ...
def script(src):
    out = []
    for raw in [l.strip() for l in src.strip().split("\n") if l.strip()]:
        if raw.startswith("## "):
            out.append(f'<h3 class="sc-hd">{raw[3:]}</h3>')
        elif raw.startswith("(") and raw.endswith(")"):
            out.append(f'<p class="did">{raw}</p>')
        else:
            who, _, said = raw.partition(":")
            said = said.strip()
            # inline stage directions (…) inside a speech
            import re
            said = re.sub(r"\(([^)]+)\)", r'<i class="di">(\1)</i>', said)
            out.append(f'<p class="fala"><b>{who.strip()}</b> {said}</p>')
    return "\n".join(out)


PLAY = """
## CENA I
(Acampamento castelhano, no sopé do monte da Franqueira. É noite. Uma fogueira ilumina a tenda do Adiantado. Ao fundo, recortado contra o céu, o castelo de Faria. NUNO GONÇALVES, velho, de mãos atadas, está sentado num tronco. Entra PEDRO RODRÍGUEZ SARMENTO, Adiantado da Galiza, seguido de um SOLDADO.)
SARMENTO: Então, velho? Dizem-me que queres falar comigo. Vens pedir clemência?
NUNO: Venho oferecer-vos um castelo, senhor Adiantado.
SARMENTO: (Ri-se.) Um prisioneiro a oferecer castelos! E qual?
NUNO: (Aponta para o fundo.) Aquele. O de Faria. Governa-o meu filho, Gonçalo Nunes, que me quer mais do que às pedras que guarda.
SARMENTO: E porque havia ele de o entregar?
NUNO: Porque, se me vir em ferros ao pé da barbacã, e se eu lho pedir, não terá coragem de deixar morrer o pai. Levai-me lá amanhã. Falarei com ele. Sem uma gota de sangue, o castelo será vosso.
SARMENTO: (Desconfiado, anda à volta dele.) És muito generoso para um português.
NUNO: Sou velho, senhor. Os velhos querem morrer na cama.
SARMENTO: Seja. Ao nascer do sol, subimos o monte. (Ao SOLDADO.) Que não lhe falte nada esta noite. Nem ele fuja.
(Saem SARMENTO e o SOLDADO. NUNO fica só. A luz da fogueira desce até lhe iluminar apenas o rosto.)
NUNO: (À parte, para o público.) Amanhã, meu filho, vais ouvir a voz de teu pai pela última vez. E hás de fazer-me a vontade.
(Escuro.)
## CENA II
(Diante da barbacã do castelo de Faria. Manhã. No alto das ameias, BESTEIROS com as bestas apontadas. No terreiro, atrás da cerca, ouve-se o POVO: choro de crianças, murmúrios. Entram, pela esquerda, o ARAUTO, o ALMOCADÉM e SOLDADOS castelhanos, trazendo NUNO GONÇALVES no meio deles. Pela direita, sobre o muro, aparece GONÇALO NUNES.)
ARAUTO: (Avança sozinho, com a bandeira erguida.) Moço alcaide, moço alcaide! Teu pai, cativo do mui nobre Pedro Rodríguez Sarmento, deseja falar contigo de fora de teu castelo!
(As bestas inclinam-se para o chão. Silêncio total.)
GONÇALO: A Virgem proteja meu pai. Dizei-lhe que eu o espero.
(O ARAUTO recua. NUNO dá dois passos em frente, sozinho, e ergue a cabeça.)
NUNO: Sabes tu, Gonçalo Nunes, de quem é esse castelo que entreguei à tua guarda?
GONÇALO: É de nosso rei e senhor, D. Fernando de Portugal, a quem fizestes preito e menagem.
NUNO: E sabes tu que o dever de um leal alcaide é nunca o entregar a inimigos, embora fique enterrado debaixo das suas ruínas?
GONÇALO: (Em voz baixa, inclinado sobre o muro.) Sei, meu pai. Mas não vedes que a vossa morte é certa, se eles percebem o que me aconselhais?
(Os SOLDADOS castelhanos começam a murmurar. O ALMOCADÉM leva a mão à espada.)
NUNO: (Gritando, para que todos ouçam.) Pois, se o sabes, cumpre o teu dever, alcaide do castelo de Faria! Maldito sejas tu, se os que me cercam entrarem nesse castelo sem tropeçarem no teu cadáver!
ALMOCADÉM: Traição! Morra! Morra o que nos enganou!
(Os SOLDADOS lançam-se sobre NUNO. Ele cai. A luz fixa-se nele.)
NUNO: (Num fio de voz.) Defende-te… alcaide!
GONÇALO: (Desesperado, a correr ao longo do muro.) Pai! Pai! (Voltando-se para os BESTEIROS.) Disparai! Disparai!
(Uma nuvem de setas. Gritos. O ruído do combate cresce e, de repente, corta-se. Escuro.)
## CENA III · EPÍLOGO
(Anos depois. Uma pequena igreja, ao pé do monte. Luz de velas. GONÇALO NUNES, com vestes de padre, reza sozinho diante do altar.)
GONÇALO: Defendi o castelo, meu pai. Levantaram o cerco; el-rei louvou-me; os homens chamam-me herói. E, no entanto, todas as noites ouço a vossa voz: «Defende-te, alcaide!». Deixei a espada ao pé deste altar. É com orações que vos pago o que vos devo. (Pausa. Olha para o público.) Do castelo, já não resta pedra sobre pedra. Mas enquanto alguém contar esta história, meu pai não morreu em vão.
(A luz das velas apaga-se devagar. Pano.)
"""

P = []
# ------------------------------------------------------------------ OPENER
P.append('''
<section id="u4" class="page v-dra opener u4-opener">
  <div class="bleed" style="background-image:url(../art/jpg/u4_opener.jpg); background-position: 50% 45%;"></div>
  <div class="opener-card">
    <div class="kicker"><b>Unidade 4</b> Texto dramático</div>
    <h1 class="title">Sobe <em>o pano</em></h1>
    <p class="lede">Um rei que quer saber qual das filhas o ama mais — e não percebe a resposta da mais sincera. Um velho alcaide que escolhe as suas últimas palavras. Nesta unidade, o texto deixa de ser só para ler: é para <b>dizer, mostrar e representar</b>. E vais descobrir o que muda quando uma história sai da página e sobe ao palco.</p>
    <div class="opener-qs">
      <div><span>?</span>Como se conta uma história sem narrador?</div>
      <div><span>?</span>Pode uma palavra — «sal» — decidir o destino de um reino?</div>
      <div><span>?</span>O que ganha e o que perde uma história quando vai para o teatro?</div>
    </div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Unidade 4</span></div>
</section>''')

# ------------------------------------------------------------------ PROGRAMA
P.append(page('u4-prog', '', 'Programa', '''
    <div class="kicker"><b>Unidade 4</b> O programa</div>
    <h1 class="title">Dois textos, <em>um palco</em></h1>
    <div class="u4-2">
      <div class="u4-c a"><span class="u4-n">1</span><b>Leandro, rei da Helíria</b><small>Alice Vieira · peça em dois atos</small>
        <ul><li>Ato, cena, fala, didascálias</li><li>Leitura em papéis e representação de uma cena</li><li>Temas: o poder e a identidade</li><li>Escrita: resumo da ação e comentário a uma escolha da personagem</li><li>Gramática: didascálias e discurso das falas · frase ativa e passiva</li></ul>
        <span class="u4-p">p. <span class="ref" data-ref="u4-l1"></span></span></div>
      <div class="u4-c b"><span class="u4-n">2</span><b>Do Castelo de Faria à cena</b><small>Alexandre Herculano · adaptação da Prime School</small>
        <ul><li>Comparar a narrativa com a cena dramatizada</li><li>O que muda quando a narrativa passa a ter falas e indicações</li><li>Escrita: duas cenas a partir de um episódio narrativo</li><li>Gramática: sujeito, complemento direto, complemento indireto e modificador</li></ul>
        <span class="u4-p">p. <span class="ref" data-ref="u4-l2"></span></span></div>
    </div>
    <div class="u2-foot u4-foot">
      <div><b>Antes de começar</b><span>O mapa do texto dramático · p. <span class="ref" data-ref="u4-map"></span></span></div>
      <div><b>No fim</b><span>Em cena! · p. <span class="ref" data-ref="u4-proj"></span></span></div>
      <div><b>Verificar</b><span>Balanço e soluções · p. <span class="ref" data-ref="u4-bal"></span></span></div>
    </div>
    <div class="u4-img big" style="background-image:url(../art/jpg/u4_stage.jpg)"></div>
    <div class="note-f"><i>Leandro, rei da Helíria</i>, de Alice Vieira, é uma obra protegida: lê a peça completa na edição da turma; aqui citam-se apenas falas breves. A adaptação dramática de «O Castelo de Faria» foi escrita para esta unidade, a partir do texto de Herculano (domínio público), que já leste na Unidade 2.</div>'''))

# ------------------------------------------------------------------ MAPA DO TEXTO DRAMÁTICO
P.append(page('u4-map', '', 'Mapa do texto dramático', '''
    <div class="kicker"><b>Unidade 4</b> <span class="skill sk-lit">Ed. literária</span> Referência</div>
    <h1 class="title">O mapa <em>do texto dramático</em></h1>
    <p class="lede sm">Um texto dramático é escrito para ser <b>representado</b>. Não há narrador: a história avança pelas falas das personagens e pelas indicações para quem o põe em cena.</p>
    <div class="dm">
      <div class="dm-c"><b>Texto principal</b><p>As <b>falas</b> das personagens. Formas:</p>
        <ul><li><b>Diálogo</b> — conversa entre personagens.</li><li><b>Monólogo</b> — uma personagem fala sozinha, em voz alta.</li><li><b>Aparte</b> — fala que só o público ouve (as outras personagens «não ouvem»).</li></ul></div>
      <div class="dm-c alt"><b>Texto secundário</b><p>As <b>didascálias</b> (ou indicações cénicas): em itálico, muitas vezes entre parênteses. Dizem:</p>
        <ul><li>onde e quando (cenário, luz, som);</li><li>quem entra e quem sai;</li><li>como se fala e se move (tom, gestos, expressão).</li></ul></div>
    </div>
    <div class="acts">
      <div class="ac-h">A estrutura externa</div>
      <div class="ac"><b>Ato</b><span>Grande divisão da peça; muitas vezes, muda o tempo ou o lugar. Marca-se com a descida do pano.</span></div>
      <div class="ac"><b>Cena</b><span>Divisão do ato; muda quando entra ou sai uma personagem.</span></div>
      <div class="ac"><b>Quadro</b><span>Divisão marcada por uma mudança de cenário.</span></div>
    </div>
    <div class="acts">
      <div class="ac-h">A estrutura interna</div>
      <div class="ac"><b>Exposição</b><span>Apresentação das personagens e da situação.</span></div>
      <div class="ac"><b>Conflito</b><span>O problema cresce até ao clímax.</span></div>
      <div class="ac"><b>Desenlace</b><span>A resolução do conflito.</span></div>
    </div>
    <div class="team">
      <div class="tm-h">Quem faz o espetáculo</div>
      <span><b>Encenador</b> dirige tudo</span><span><b>Atores</b> dão corpo às personagens</span><span><b>Cenógrafo</b> cenário</span><span><b>Figurinista</b> guarda-roupa</span><span><b>Luminotécnico</b> luz</span><span><b>Sonoplasta</b> som e música</span><span><b>Ponto</b> sopra as falas esquecidas</span>
    </div>
    <div class="anno">
      <div class="an-h">Exemplo anotado · <i>O Castelo de Faria</i>, cena I (p. <span class="ref" data-ref="u4-l2"></span>)</div>
      <div class="an-t">
        <p class="did">(Saem SARMENTO e o SOLDADO. NUNO fica só. A luz da fogueira desce até lhe iluminar apenas o rosto.)</p>
        <p class="fala"><b>NUNO</b> <i class="di">(À parte, para o público.)</i> Amanhã, meu filho, vais ouvir a voz de teu pai pela última vez.</p>
      </div>
      <div class="an-k"><span><i>1</i>didascália de <b>saída</b>: muda a cena</span><span><i>2</i>didascália de <b>luz</b>: trabalho do luminotécnico</span><span><i>3</i>nome da <b>personagem</b> antes da fala</span><span><i>4</i>didascália de <b>tom</b>: é um aparte</span></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Explica, por palavras tuas, a diferença entre um <b>monólogo</b> e um <b>aparte</b>. Porque é que o público gosta de saber coisas que as personagens não sabem?</p>
      <div class="lines l3"></div>
    </div></div>'''))

# ------------------------------------------------------------------ AQUECIMENTO
P.append(page('u4-aq', '', 'Aquecimento', '''
    <div class="kicker"><b>Aquecimento</b> 15 minutos · a três</div>
    <h1 class="title">Uma cena <em>na bilheteira</em></h1>
    <div class="mini-play">
      <p class="did">(Bilheteira do Cinema Aurora, em Vila Nova do Farol. Fim de tarde. Chove. Atrás do vidro, D. ROSA faz palavras cruzadas. Entra TIAGO, 13 anos, a correr, encharcado.)</p>
      <p class="fala"><b>TIAGO</b> Um bilhete para as sete, se faz favor!</p>
      <p class="fala"><b>D. ROSA</b> <i class="di">(Sem levantar os olhos.)</i> Esgotado.</p>
      <p class="fala"><b>TIAGO</b> Esgotado? Mas é a estreia de <i>O Farol das Baleias</i>! Esperei um mês!</p>
      <p class="fala"><b>D. ROSA</b> Por isso mesmo. <i class="di">(Pausa. Olha-o por cima dos óculos.)</i> Vieste sozinho?</p>
      <p class="fala"><b>TIAGO</b> <i class="di">(À parte.)</i> Se lhe digo que fugi aos trabalhos de casa, estou feito.</p>
      <p class="fala"><b>D. ROSA</b> Então?</p>
      <p class="fala"><b>TIAGO</b> Vim com… com a minha avó. Está a estacionar.</p>
      <p class="did">(Entra a AVÓ, de guarda-chuva, a sacudir a água.)</p>
      <p class="fala"><b>AVÓ</b> Tiago! Pensava que estavas a estudar!</p>
      <p class="did">(D. ROSA ri-se, tira dois bilhetes da gaveta e empurra-os por baixo do vidro.)</p>
      <p class="fala"><b>D. ROSA</b> Guardei-os ontem. Sabia que vinhas. <i class="di">(Para a AVÓ.)</i> A senhora também, não é, Graça? Uma sessão destas não se perde.</p>
      <p class="did">(Escuro.)</p>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Sublinha a azul as <b>falas</b> e a amarelo as <b>didascálias</b>. Encontra um <b>aparte</b>: o que tem de especial?</p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Quantas cenas tem este excerto, se contarmos uma nova cena sempre que entra ou sai uma personagem? Justifica.</p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Leiam a cena em voz alta, a três. Depois, mudem <b>uma</b> didascália (por exemplo, o tom de D. Rosa) e voltem a ler. O que muda? <span class="pill oral">Oralidade</span></p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">4</div><div class="body">
      <p class="q">Escreve a cena seguinte (4 a 6 falas): Tiago e a Avó à entrada da sala. Usa pelo menos duas didascálias. <span class="pill stretch">Desafio</span></p>
      <div class="lines l5"></div>
    </div></div>'''))

# ------------------------------------------------------------------ L1 · LEANDRO
P.append(page('u4-l1', '', 'Leitura 1 · Leandro, rei da Helíria', f'''
    <div class="kicker"><b>Leitura 1</b> <span class="skill sk-lit">Ed. literária</span> Antes de ler · lê a peça completa na edição da turma</div>
    <h1 class="title">Leandro, <em>rei da Helíria</em></h1>
    <p class="byline">Alice Vieira · teatro · dois atos, onze cenas cada</p>
    <div class="hero-img short" style="background-image:url(../art/jpg/u4_opener.jpg); background-position: 50% 42%;"></div>
    <div class="guide">
      <div class="gd-c">
        <h3>A autora</h3>
        <p><b>Alice Vieira</b> (n. 1943), lisboeta, jornalista e escritora, é uma das autoras mais lidas pelos jovens portugueses. Escreveu romances, poesia, contos e teatro.</p>
        <h3>A história por trás da história</h3>
        <p>A peça parte de um conto popular — o do rei que pergunta às filhas quanto gostam dele e expulsa a que responde «como a comida gosta do sal». É a mesma história que Shakespeare transformou em tragédia, <i>O Rei Lear</i>. Alice Vieira fê-la acabar de outra maneira.</p>
        {cite('Estranho sonho tive esta noite…', 'Leandro · 1.º ato, cena I')}
        {cite('Os sonhos são recados dos deuses.', '1.º ato, cena I')}
      </div>
      <div class="gd-c rd">
        <h3>As personagens</h3>
        <div class="cast">
          <div><b>Leandro</b><span>rei da Helíria, velho e cansado; um sonho inquieta-o</span></div>
          <div><b>O Bobo</b><span>o bobo da corte: faz rir, mas é quem diz as verdades</span></div>
          <div><b>Amarílis</b><span>a filha mais velha</span></div>
          <div><b>Hortênsia</b><span>a filha do meio</span></div>
          <div><b>Violeta</b><span>a filha mais nova</span></div>
          <div><b>Os pretendentes</b><span>os príncipes que querem casar com as princesas</span></div>
          <div><b>O Pastor</b><span>um homem simples que o rei encontra no caminho</span></div>
        </div>
        <div class="act"><div class="num">1</div><div class="body">
          <p class="q">Lê a lista de personagens da tua edição. Pelo nome e pela descrição, qual te parece que vai ser a mais importante? E a mais divertida?</p>
          <div class="lines l4"></div>
        </div></div>
      </div>
    </div>'''))

P.append(page('u4-l1-g', '', 'Leitura 1 · Leandro, rei da Helíria', '''
    <div class="kicker"><b>Leitura 1</b> <span class="skill sk-lei">Leitura</span> Guião de leitura por atos</div>
    <h1 class="title">O rei, as filhas <em>e o sal</em></h1>
    <div class="acts2">
      <div class="a1"><div class="a-h">1.º ato</div>
        <ol class="qs">
          <li>Cena I: onde se passa? Que didascália o indica? O que preocupa o rei?<div class="lines l3"></div></li>
          <li>Porque é que o Bobo se queixa da vida que leva? O que pensa dos ricos e dos pobres?<div class="lines l3"></div></li>
          <li>Que decisão toma o rei sobre o reino? Que prova pede às filhas?<div class="lines l3"></div></li>
          <li>Compara as respostas de Amarílis e Hortênsia com a de Violeta. Porque é que o rei se zanga?<div class="lines l4"></div></li>
          <li>O que acontece a Violeta no fim do 1.º ato?<div class="lines l2"></div></li>
        </ol></div>
      <div class="a2"><div class="a-h">2.º ato</div>
        <ol class="qs" start="6">
          <li>Como tratam as filhas mais velhas o pai, depois de receberem o reino? Dá um exemplo.<div class="lines l3"></div></li>
          <li>Que papel tem o Pastor na viagem do rei?<div class="lines l3"></div></li>
          <li>Na cena XI, Violeta serve ao pai pratos sem sal. Porquê? O que percebe finalmente Leandro?<div class="lines l4"></div></li>
          <li>Que diferença há entre o final desta peça e o de <i>O Rei Lear</i>, que é uma tragédia?<div class="lines l3"></div></li>
        </ol>
        <blockquote class="cq dq"><p>Como fui louco! E tanto que eu vos amava!</p><cite>Leandro · 2.º ato, cena XI</cite></blockquote>
      </div>
    </div>
    <div class="arc4"><span>Exposição<small>1.º ato, cenas I–VI</small></span><span>Conflito<small>1.º ato, cena VII → 2.º ato, cena VIII</small></span><span>Desenlace<small>2.º ato, cenas IX–XI</small></span></div>
    <div class="act"><div class="num">✎</div><div class="body">
      <p class="q">Escolhe a cena que achaste mais importante em cada ato e explica porquê, numa frase para cada uma.</p>
      <div class="lines l3"></div>
    </div></div>'''))

P.append(page('u4-l1-t', '', 'Leitura 1 · Leandro, rei da Helíria', '''
    <div class="kicker"><b>Leitura 1</b> <span class="skill sk-lit">Ed. literária</span> <span class="skill sk-ora">Oralidade</span> Poder e identidade · leitura em papéis</div>
    <h1 class="title">Quem és tu, <em>sem coroa?</em></h1>
    <div class="pw">
      <div><b>O poder</b><p>O rei tem tudo e decide tudo. Mas decide mal: confunde palavras bonitas com amor verdadeiro. Quando entrega o poder, descobre como o tratam os que o bajulavam.</p></div>
      <div><b>A identidade</b><p>Sem reino, Leandro é um velho errante. Quem é ele, então? O que fica de uma pessoa quando lhe tiram o título, a casa, o poder?</p></div>
      <div><b>A verdade</b><p>O Bobo e Violeta dizem a verdade — um a rir, a outra a sério. Os dois são castigados por isso. Porque é tão difícil ouvir a verdade?</p></div>
    </div>
    <ol class="qs">
      <li>No início, Leandro é rei. No fim, é pai. Explica esta frase com dois momentos da peça.<div class="lines l4"></div></li>
      <li>«Gosto de vós como a comida gosta do sal.» Porque é que esta é a resposta mais sincera? Porque é que o rei não a entende?<div class="lines l4"></div></li>
      <li>O Bobo é a personagem mais inteligente da peça? Justifica. <span class="pill stretch">Desafio</span><div class="lines l5"></div></li>
    </ol>
    <div class="roles-t">
      <div class="rt-h">Leitura em papéis · como preparar</div>
      <div class="rt"><i>1</i><span>Em grupos, escolham uma cena curta (por exemplo, a das respostas das filhas).</span></div>
      <div class="rt"><i>2</i><span>Distribuam as personagens e um <b>leitor das didascálias</b>.</span></div>
      <div class="rt"><i>3</i><span>Marquem no texto: <u>palavras a realçar</u>, pausas (/), tom (irónico, zangado, doce…).</span></div>
      <div class="rt"><i>4</i><span>Ensaiem duas vezes. Na segunda, os atores já não leem as didascálias: <b>fazem-nas</b>.</span></div>
      <div class="rt"><i>5</i><span>Apresentem à turma. Os colegas dizem uma coisa que resultou e uma a melhorar.</span></div>
    </div>'''))

P.append(page('u4-l1-e', 'v-oficina-d', 'Leitura 1 · Escrita', '''
    <div class="kicker"><b>Leitura 1</b> <span class="skill sk-esc">Escrita</span> Resumo da ação · comentário a uma escolha</div>
    <h1 class="title">O que aconteceu <em>e porquê</em></h1>
    <div class="twoR">
      <div><b>Resumo da ação</b><p>Um parágrafo por grande momento (exposição, conflito, desenlace). 3.ª pessoa, presente do indicativo, sem falas copiadas. 100 a 130 palavras.</p></div>
      <div><b>Comentário a uma escolha</b><p>Escolhe uma decisão de uma personagem. Explica-a, avalia-a com argumentos e diz o que farias no seu lugar. 120 a 160 palavras.</p></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Resume a ação de <i>Leandro, rei da Helíria</i>.</p>
      <div class="lines l10"></div>
    </div></div>
    <div class="ch">
      <div class="ch-h">Escolhe uma decisão para comentar</div>
      <span>Leandro expulsa Violeta</span><span>Violeta diz «como a comida gosta do sal»</span><span>As filhas mais velhas fecham a porta ao pai</span><span>O Bobo acompanha o rei</span><span>Violeta serve pratos sem sal</span>
    </div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Escreve o comentário: tese (a decisão foi certa ou errada?), dois argumentos com exemplos da peça, conclusão.</p>
      <div class="lines l12"></div>
    </div></div>'''))

P.append(page('u4-l1-gr', 'v-oficina-d', 'Leitura 1 · Gramática', '''
    <div class="kicker"><b>Leitura 1</b> <span class="skill sk-gra">Gramática</span> Didascálias e discurso das falas · frase ativa e passiva</div>
    <h1 class="title">Quem fala, <em>como fala</em></h1>
    <div class="gx">
      <div class="gx-c"><b>A língua das didascálias</b><p>Frases curtas, muitas vezes sem verbo; presente do indicativo; 3.ª pessoa; informação objetiva.</p><p class="ex">(No jardim do palácio. Entra o Bobo, a correr. Tocam as trombetas.)</p></div>
      <div class="gx-c"><b>A língua das falas</b><p>1.ª e 2.ª pessoas (eu, tu, vós); frases exclamativas e interrogativas; vocativos; interjeições; registo que depende da personagem.</p><p class="ex">Ai, Senhor! Então não vedes que vos mentem?</p></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Transforma este pequeno texto narrativo numa fala com didascália: <i>«O rei, furioso, levantou-se do trono e gritou à filha mais nova que saísse do palácio e nunca mais voltasse.»</i></p>
      <div class="lines l4"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Faz o contrário: transforma em narração (3.ª pessoa, pretérito perfeito): <i>VIOLETA (Baixando os olhos.) Gosto de vós, meu pai, como a comida gosta do sal.</i></p>
      <div class="lines l4"></div>
    </div></div>
    <div class="rev"><b>Revisão · frase ativa e passiva</b> (Unidade 1)<span>Ativa: <i>O rei expulsou Violeta.</i></span><span>Passiva: <i>Violeta foi expulsa pelo rei.</i></span></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Passa à passiva: <b>a)</b> As filhas receberam o reino. <b>b)</b> O Pastor acolheu o rei. <b>c)</b> Violeta preparará o banquete. Passa à ativa: <b>d)</b> O rei foi reconhecido pelo Bobo.</p>
      <div class="lines l6"></div>
    </div></div>
    <div class="act"><div class="num">4</div><div class="body">
      <p class="q">Porque é que, numa didascália, se escreve «Tocam as trombetas» e não «As trombetas são tocadas pelos músicos»? <span class="pill stretch">Desafio</span></p>
      <div class="lines l3"></div>
    </div></div>'''))

# ------------------------------------------------------------------ L2 · CASTELO À CENA (flow)
P.append(f'''
<section id="u4-l2" class="page v-dra flow">
  {rail('Leitura 2 · O Castelo de Faria em cena')}
  <div class="inner">
    <div class="flow-head">
      <div class="kicker"><b>Leitura 2</b> <span class="skill sk-lei">Leitura</span> <span class="skill sk-ora">Oralidade</span> Adaptação dramática</div>
      <h2 class="tx-title">O Castelo de Faria</h2>
      <p class="tx-by">Cenas a partir de Alexandre Herculano · adaptação da Prime School</p>
      <div class="dp">
        <div><b>Personagens</b><span>NUNO GONÇALVES, alcaide de Faria, velho · GONÇALO NUNES, seu filho · PEDRO RODRÍGUEZ SARMENTO, Adiantado da Galiza · O ARAUTO · O ALMOCADÉM castelhano · SOLDADOS · BESTEIROS · O POVO (vozes)</span></div>
        <div><b>Lugar e tempo</b><span>Minho, século XIV, durante a guerra entre D. Fernando de Portugal e Castela.</span></div>
      </div>
    </div>
    <div class="flow-body cols2 play">
{script(PLAY)}
<p class="src">Adaptação da Prime School a partir de «O Castelo de Faria», de Alexandre Herculano (<i>Lendas e Narrativas</i>, 1851). Algumas falas seguem de perto o texto original (Unidade 2).</p>
<div class="dnote"><div class="dn-h">Caderno do encenador</div>
  <p class="dn-i">Escolhe uma cena e prepara-a como se fosses pô-la em palco.</p>
  <div class="dn-r"><b>Cena</b><i></i></div>
  <div class="dn-r"><b>Cenário</b><i></i></div><div class="dn-r"><b></b><i></i></div>
  <div class="dn-r"><b>Luz</b><i></i></div><div class="dn-r"><b></b><i></i></div>
  <div class="dn-r"><b>Som</b><i></i></div><div class="dn-r"><b></b><i></i></div>
  <div class="dn-r"><b>Adereços</b><i></i></div><div class="dn-r"><b></b><i></i></div>
  <div class="dn-r"><b>Figurinos</b><i></i></div><div class="dn-r"><b></b><i></i></div>
  <div class="dn-r"><b>Momento-chave</b><i></i></div><div class="dn-r"><b></b><i></i></div>
  <div class="dn-r"><b>Porquê</b><i></i></div><div class="dn-r"><b></b><i></i></div>
</div>
<div class="dnote alt"><div class="dn-h">Para dizer bem</div>
  <p class="dn-i"><b>Nuno</b>, na cena II, começa calmo e acaba a gritar: marca no texto onde a voz sobe. <b>Gonçalo</b> fala «em voz baixa» — o público tem de o ouvir na mesma. Como? <b>O Arauto</b> fala com solenidade: é a voz oficial do inimigo.</p>
  <div class="lines l6"></div>
</div>
    </div>
  </div>
  {folio('Leitura 2 · O Castelo de Faria em cena')}
</section>''')

P.append(page('u4-l2-c', '', 'Leitura 2 · Comparar', '''
    <div class="kicker"><b>Leitura 2</b> <span class="skill sk-lit">Ed. literária</span> Da narrativa à cena</div>
    <h1 class="title">O que muda <em>no palco?</em></h1>
    <table class="fill cmp">
      <tr><th style="width:36mm"></th><th>Na narrativa (Herculano, Unidade 2)</th><th>Na cena dramatizada</th></tr>
      <tr><td><b>Quem conta</b></td><td>um narrador não participante, que comenta</td><td></td></tr>
      <tr><td><b>O lugar</b></td><td>descrito ao longo de seis parágrafos</td><td></td></tr>
      <tr><td><b>As personagens</b></td><td>caracterizadas pelo narrador</td><td></td></tr>
      <tr><td><b>O que pensam</b></td><td>o narrador diz-nos</td><td></td></tr>
      <tr><td><b>O tempo</b></td><td>séculos de história, do castelo ao convento</td><td></td></tr>
      <tr><td><b>O final</b></td><td>o narrador tira a lição</td><td></td></tr>
    </table>
    <ol class="qs">
      <li>A cena I não existe em Herculano (lá, o ardil é contado num parágrafo). Porque é que o adaptador a inventou?<div class="lines l3"></div></li>
      <li>Encontra o <b>aparte</b> da cena I e o <b>monólogo</b> da cena III. Que informação dão ao público que as outras personagens não sabem?<div class="lines l3"></div></li>
      <li>O narrador de Herculano descreve o incêndio do terreiro. Na cena II, como se mostra o combate? Que profissionais do espetáculo tornam isso possível?<div class="lines l3"></div></li>
      <li>Qual das versões te emocionou mais? Justifica com um momento de cada. <span class="pill stretch">Desafio</span><div class="lines l4"></div></li>
    </ol>'''))

P.append(page('u4-l2-e', 'v-oficina-d', 'Leitura 2 · Escrita', '''
    <div class="kicker"><b>Leitura 2</b> <span class="skill sk-esc">Escrita</span> Duas cenas a partir de um episódio narrativo</div>
    <h1 class="title">A tua vez <em>de adaptar</em></h1>
    <p class="lede sm">Escolhe um episódio de uma das narrativas da Unidade 2 e transforma-o em <b>duas cenas</b>, com título, lista de personagens, didascálias e falas.</p>
    <div class="ch">
      <div class="ch-h">Episódios possíveis</div>
      <span>O pai e os sete vimes (Trindade Coelho)</span><span>Castelo conhece o Barão (Lima Barreto)</span><span>A aposta no Reform Club (Verne)</span><span>O senhor Otis e o fantasma (Wilde)</span>
    </div>
    <div class="steps4">
      <div><i>1</i><b>Corta</b><span>Escolhe só os momentos que se podem <u>mostrar</u>. O resto passa para as didascálias ou desaparece.</span></div>
      <div><i>2</i><b>Divide</b><span>Duas cenas: muda de cena quando entra ou sai uma personagem, ou quando muda o lugar.</span></div>
      <div><i>3</i><b>Dá voz</b><span>O que o narrador dizia passa a ser dito pelas personagens (ou mostrado).</span></div>
      <div><i>4</i><b>Encena</b><span>Didascálias de cenário, luz, som, entradas, saídas, tom e gestos.</span></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escreve as tuas duas cenas (250 a 350 palavras no total). Continua no caderno, se precisares.</p>
      <div class="scr-frame">
        <div class="sf-row"><b>Título</b><i></i></div>
        <div class="sf-row"><b>Personagens</b><i></i></div>
        <div class="sf-row"><b>Cena I</b><i></i></div>
      </div>
      <div class="lines l14"></div>
    </div></div>
    <div class="chk"><b>Revê</b><span>título e personagens</span><span>duas cenas bem marcadas</span><span>didascálias de lugar, entradas e tom</span><span>nome da personagem antes de cada fala</span><span>250–350 palavras</span></div>'''))

P.append(page('u4-l2-g', 'v-oficina-d', 'Leitura 2 · Gramática', '''
    <div class="kicker"><b>Leitura 2</b> <span class="skill sk-gra">Gramática</span> Sujeito · complemento direto · complemento indireto · modificador</div>
    <h1 class="title">Quem faz o quê, <em>a quem</em></h1>
    <div class="fx4">
      <div class="f-s"><b>Sujeito</b><span>quem pratica a ação ou de quem se fala</span><em>Pergunta: quem? o quê? (antes do verbo)</em></div>
      <div class="f-cd"><b>Complemento direto</b><span>completa o verbo sem preposição; substitui-se por <i>o, a, os, as</i></span><em>Pergunta: o quê? quem?</em></div>
      <div class="f-ci"><b>Complemento indireto</b><span>o destinatário da ação; com <i>a</i>; substitui-se por <i>lhe, lhes</i></span><em>Pergunta: a quem?</em></div>
      <div class="f-m"><b>Modificador</b><span>acrescenta informação (tempo, lugar, modo, causa…); pode sair da frase</span><em>Pergunta: quando? onde? como?</em></div>
    </div>
    <div class="parse">
      <div class="ps-row"><span class="f-s">O arauto</span><span class="vb">entregou</span><span class="f-cd">a mensagem</span><span class="f-ci">ao moço alcaide</span><span class="f-m">nessa manhã</span>.</div>
      <div class="ps-key"><span class="f-s">sujeito</span><span class="vb">verbo</span><span class="f-cd">CD</span><span class="f-ci">CI</span><span class="f-m">modificador</span></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Identifica as funções sintáticas sublinhando com as cores do quadro.</p>
      <ol class="mini" type="a">
        <li>Nuno Gonçalves ofereceu o castelo ao Adiantado.</li>
        <li>Na manhã seguinte, os soldados levaram o velho até à barbacã.</li>
        <li>Gonçalo respondeu ao pai em voz baixa.</li>
        <li>O rei deu o reino às duas filhas mais velhas.</li>
        <li>Violeta serviu ao pai pratos sem sal.</li>
      </ol>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Substitui o CD e o CI por pronomes: <b>a)</b> O Bobo contou a verdade ao rei. <b>b)</b> Os besteiros apontaram as bestas aos castelhanos.</p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Escreve uma frase sobre uma das peças com sujeito, CD, CI e dois modificadores. Identifica cada função.</p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">4</div><div class="body">
      <p class="q">Numa fala, o CD e o CI aparecem muitas vezes como pronomes. Identifica-os: <i>NUNO Dizei-lhe que eu o espero. · SARMENTO Que não lhe falte nada esta noite. · VIOLETA Eu dou-vos o meu amor.</i></p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">5</div><div class="body">
      <p class="q">Retira os modificadores e reescreve a frase: <i>«Na manhã seguinte, junto à barbacã, o velho falou ao filho em voz alta.»</i> Que informação se perdeu? A frase continua correta?</p>
      <div class="lines l1"></div>
    </div></div>'''))

# ------------------------------------------------------------------ PROJETO
P.append(page('u4-proj', '', 'Em cena!', '''
    <div class="kicker"><b>Projeto</b> <span class="skill sk-ora">Oralidade</span> Em grupo · 2 semanas</div>
    <h1 class="title">Em <em>cena!</em></h1>
    <p class="lede sm">O Cinema Aurora vai, pela primeira vez, abrir o palco ao teatro. Cada grupo apresenta uma cena de 5 a 8 minutos: uma cena de <i>Leandro, rei da Helíria</i>, a adaptação de «O Castelo de Faria», ou as duas cenas que escreveram.</p>
    <div class="ep">
      <div><span>01</span><b>Escolher</b><p>A cena e os papéis: atores, encenador, cenógrafo, luz e som.</p></div>
      <div><span>02</span><b>Ler à mesa</b><p>Leitura em papéis, marcações no texto, discussão das personagens.</p></div>
      <div><span>03</span><b>Preparar</b><p>Cenário simples, adereços, figurinos, música e ruídos.</p></div>
      <div><span>04</span><b>Ensaiar</b><p>De cor, com movimento, entradas e saídas.</p></div>
      <div><span>05</span><b>Estrear</b><p>A apresentação e uma conversa com o público.</p></div>
    </div>
    <table class="fill tall gui"><tr><th style="width:34mm">Função</th><th>Quem</th><th>O que vai fazer</th></tr>
      <tr><td>Encenador</td><td></td><td></td></tr><tr><td>Atores</td><td></td><td></td></tr><tr><td>Cenário e adereços</td><td></td><td></td></tr><tr><td>Luz e som</td><td></td><td></td></tr></table>
    <table class="fill rub">
      <tr><th>Critério</th><th>Em construção</th><th>Consolidado</th><th>Excelente</th></tr>
      <tr><td><b>Interpretação</b></td><td>falas ditas sem intenção</td><td>tom adequado às personagens</td><td>personagens vivas: voz, corpo e olhar</td></tr>
      <tr><td><b>Didascálias</b></td><td>poucas indicações respeitadas</td><td>entradas, saídas e tom respeitados</td><td>didascálias transformadas em ação expressiva</td></tr>
      <tr><td><b>Memorização</b></td><td>leitura</td><td>de cor, com hesitações</td><td>de cor e fluido</td></tr>
      <tr><td><b>Encenação</b></td><td>sem cenário nem som</td><td>elementos simples e coerentes</td><td>soluções criativas de cenário, luz ou som</td></tr>
      <tr><td><b>Trabalho de grupo</b></td><td>participação desigual</td><td>todos contribuem</td><td>equipa coordenada, papéis claros</td></tr>
    </table>
    <div class="after"><b>Depois da estreia</b> O que aprendeste sobre o texto dramático ao representá-lo que não tinhas percebido ao lê-lo?<div class="lines l4"></div></div>'''))

# ------------------------------------------------------------------ BALANÇO
P.append(page('u4-bal', '', 'Balanço', '''
    <div class="kicker"><b>Balanço</b> Unidade 4</div>
    <h1 class="title">Dez perguntas <em>de bastidores</em></h1>
    <div class="quiz">
      <div><i>1</i>As indicações para a representação chamam-se <span class="blank w2"></span></div>
      <div><i>2</i>O texto das falas é o texto <span class="opt">principal · secundário</span></div>
      <div><i>3</i>Fala que só o público ouve: <span class="blank w2"></span></div>
      <div><i>4</i>Uma personagem sozinha, a falar em voz alta: <span class="blank w2"></span></div>
      <div><i>5</i>Muda-se de cena quando <span class="blank w3"></span></div>
      <div><i>6</i>Quem cuida da luz do espetáculo é o <span class="blank w2"></span></div>
      <div><i>7</i>Violeta compara o seu amor ao <span class="blank w2"></span></div>
      <div><i>8</i>Em «O rei deu o reino às filhas», «às filhas» é <span class="blank w2"></span></div>
      <div><i>9</i>Em «O arauto falou ao alcaide nessa manhã», «nessa manhã» é <span class="blank w2"></span></div>
      <div><i>10</i>Passa à passiva: «O Bobo reconheceu Violeta.» <span class="blank w4"></span></div>
    </div>
    <div class="selfcheck">
      <div class="sc-hd"><span>Consigo…</span><span>ainda não</span><span>quase</span><span>sim!</span></div>
      <div class="sc-r"><span>distinguir texto principal e texto secundário</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>identificar ato, cena, diálogo, monólogo e aparte</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>explicar o tema do poder e da identidade em <i>Leandro</i></span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>ler uma cena em papéis, com expressividade</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>comparar uma narrativa com a sua adaptação dramática</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>escrever cenas com falas e didascálias</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>identificar sujeito, CD, CI e modificador</span><i></i><i></i><i></i></div>
    </div>
    <div class="act"><div class="num">✎</div><div class="body">
      <p class="q">Que personagem de teatro gostavas de representar? Porquê?</p>
      <div class="lines l6"></div>
    </div></div>'''))

# ------------------------------------------------------------------ GLOSSÁRIO + SOLUÇÕES
P.append(page('u4-sol', 'backmatter', 'Glossário · soluções', '''
    <div class="bm-cols">
      <div>
        <h2>Glossário</h2>
        <dl class="gl">
          <dt>Aparte</dt><dd>Fala dirigida ao público, que as outras personagens não ouvem.</dd>
          <dt>Ato</dt><dd>Grande divisão de uma peça de teatro.</dd>
          <dt>Cena</dt><dd>Divisão de um ato; muda com a entrada ou saída de personagens.</dd>
          <dt>Didascália</dt><dd>Indicação cénica: cenário, luz, som, movimentos, tom.</dd>
          <dt>Diálogo</dt><dd>Troca de falas entre personagens.</dd>
          <dt>Encenador</dt><dd>Quem dirige o espetáculo.</dd>
          <dt>Exposição · conflito · desenlace</dt><dd>Os três momentos da estrutura interna da ação.</dd>
          <dt>Figurinista</dt><dd>Quem desenha o guarda-roupa.</dd>
          <dt>Luminotécnico · sonoplasta</dt><dd>Responsáveis pela luz e pelo som.</dd>
          <dt>Quadro</dt><dd>Divisão da peça marcada por mudança de cenário.</dd>
          <dt>Monólogo</dt><dd>Fala de uma personagem sozinha em cena.</dd>
          <dt>Texto principal</dt><dd>O conjunto das falas.</dd>
          <dt>Texto secundário</dt><dd>O conjunto das didascálias.</dd>
          <dt>Complemento direto</dt><dd>Completa o verbo sem preposição; <i>o, a, os, as</i>.</dd>
          <dt>Complemento indireto</dt><dd>Destinatário da ação; <i>lhe, lhes</i>.</dd>
          <dt>Modificador</dt><dd>Informação acessória sobre a ação.</dd>
        </dl>
      </div>
      <div>
        <h2>Soluções</h2>
        <div class="sol">
          <p><b>p. <span class="ref" data-ref="u4-aq"></span> · Aquecimento.</b> 1. Aparte: «Se lhe digo que fugi aos trabalhos de casa, estou feito.» — só o público o ouve. 2. Duas cenas: a entrada da Avó abre uma nova cena.</p>
          <p><b>p. <span class="ref" data-ref="u4-l1-gr"></span> · Falas e passiva.</b> 1. Exemplo: <i>LEANDRO (Levantando-se do trono, furioso.) Sai do meu palácio e não voltes nunca mais!</i> 2. Exemplo: Violeta baixou os olhos e disse ao pai que gostava dele como a comida gosta do sal. 3. a) O reino foi recebido pelas filhas. b) O rei foi acolhido pelo Pastor. c) O banquete será preparado por Violeta. d) O Bobo reconheceu o rei. 4. As didascálias são curtas e objetivas; o agente não interessa.</p>
          <p><b>p. <span class="ref" data-ref="u4-l2-g"></span> · Funções sintáticas.</b> 1. a) S: Nuno Gonçalves · CD: o castelo · CI: ao Adiantado. b) Mod: Na manhã seguinte · S: os soldados · CD: o velho · Mod: até à barbacã. c) S: Gonçalo · CI: ao pai · Mod: em voz baixa. d) S: O rei · CD: o reino · CI: às duas filhas mais velhas. e) S: Violeta · CI: ao pai · CD: pratos sem sal. 2. a) O Bobo contou-lha. b) Os besteiros apontaram-lhas.</p>
          <p><b>p. <span class="ref" data-ref="u4-l2-g"></span> · 4 e 5.</b> 4. <i>lhe</i> (CI) e <i>o</i> (CD) · <i>lhe</i> (CI) · <i>vos</i> (CI) e <i>o meu amor</i> (CD). 5. «O velho falou ao filho.» Perdem-se o tempo, o lugar e o modo; a frase continua correta, porque os modificadores não são obrigatórios.</p>
          <p><b>p. <span class="ref" data-ref="u4-l2-c"></span> · Comparar.</b> Na cena: não há narrador; o lugar está nas didascálias; as personagens mostram-se pelo que dizem e fazem; o que pensam diz-se em apartes e monólogos; o tempo é concentrado em três momentos; o final é um monólogo, sem lição explícita.</p>
          <p><b>p. <span class="ref" data-ref="u4-bal"></span> · Balanço.</b> 1 didascálias · 2 principal · 3 aparte · 4 monólogo · 5 entra ou sai uma personagem · 6 luminotécnico · 7 sal · 8 complemento indireto · 9 modificador · 10 Violeta foi reconhecida pelo Bobo.</p>
        </div>
      </div>
    </div>
    <div class="memo sm">
      <div class="memo-h">Cartão de memória · a unidade numa página</div>
      <div class="memo-g">
        <div class="m-s"><b>O texto dramático</b><ul><li>Texto principal (falas) e secundário (didascálias).</li><li>Diálogo, monólogo, aparte.</li><li>Ato, cena, quadro. Exposição, conflito, desenlace.</li></ul></div>
        <div class="m-r"><b>Da página ao palco</b><ul><li>Sem narrador: o que se pensa diz-se ou mostra-se.</li><li>Encenador, atores, cenógrafo, figurinista, luminotécnico, sonoplasta.</li><li>Adaptar: cortar, dividir, dar voz, encenar.</li></ul></div>
        <div class="m-g"><b>Gramática</b><ul><li>Sujeito · CD (<i>o, a</i>) · CI (<i>lhe</i>) · modificador.</li><li>Didascálias: frases curtas, presente, 3.ª pessoa.</li><li>Falas: 1.ª/2.ª pessoa, exclamações, vocativos.</li><li>Ativa e passiva (revisão).</li></ul></div>
      </div>
    </div>'''))

(R / 'src' / 'u4.html').write_text("\n".join(P))
print(len(P), 'pages')
