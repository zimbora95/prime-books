"""Page generators for the book matter (front i–viii, back 145–151 + back cover).

Every page is an HTML <section class="page ..."> in Unit 1's visual system. All data comes from
build.model() (harvested from the built units, with provisional fallbacks from plan.py).
"""
import html as H
import re

import segno

from plan import UNITS, YEAR5

E = H.escape
KEYC = {"bronze": "#B7723A", "prata": "#8E99A6", "ouro": "#D6A21E"}
MOU = "../../art/mou-{}.png"


def key_svg(k):
    c = KEYC[k]
    return (f'<svg class="key" viewBox="0 0 34 16" aria-label="chave {k}"><circle cx="7.5" cy="8" r="5.6" fill="none" stroke="{c}" stroke-width="3"/>'
            f'<path d="M13 8h19M26 8v5M30.5 8v4" stroke="{c}" stroke-width="3" stroke-linecap="round" fill="none"/></svg>')


def qr_svg(url, error="m", border=4):
    q = segno.make(url, error=error, boost_error=False)
    svg = q.svg_inline(scale=1, border=border, dark="#1C2536", light="#ffffff")
    m = re.search(r'width="(\d+)" height="(\d+)"', svg)
    return svg.replace(m.group(0), f'viewBox="0 0 {m.group(1)} {m.group(2)}" shape-rendering="crispEdges"', 1)


QRICON = '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm;flex:none"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>'


def star(fill="none", stroke="#B9AE98"):
    return (f'<svg viewBox="0 0 24 24"><path d="M12 2.6l2.8 6 6.5.7-4.9 4.4 1.4 6.4L12 16.9 6.2 20.1l1.4-6.4L2.7 9.3l6.5-.7z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.6" stroke-linejoin="round"/></svg>')


SPARK = '<svg class="spark" viewBox="0 0 24 24"><path d="M12 1.5c.9 5.6 4.9 9.6 10.5 10.5-5.6.9-9.6 4.9-10.5 10.5C11.1 16.9 7.1 12.9 1.5 12 7.1 11.1 11.1 7.1 12 1.5z" fill="currentColor"/></svg>'
STARS = '<span class="stars">' + star() * 5 + '</span>'


def run(left, strong, right):
    return f'<header class="run"><span>{left}</span><span><b>{strong}</b>{" · " + right if right else ""}</span></header>'


def folio(n, roman=False):
    cls = "folio rom" + (" w" if roman and len(n) > 2 else "") if roman else "folio"
    return f'<footer class="{cls}">{n}</footer>'


def pp(a, b=None):
    return f"p. {a}" if b is None or a == b else f"pp. {a}–{b}"


def ucolor(n):
    return next(u for u in UNITS if u["n"] == n)


# ============================================================ FRONT MATTER
def p_cover(M):
    return f"""
<section class="page odd cover">
  <div class="art"></div><div class="veil"></div><div class="stripe"></div>
  <div class="brandrow"><img src="../art/logo_prime_school.png" alt=""><span>P R I M E &nbsp; S C H O O L &nbsp; P R E S S</span></div>
  <div class="ttl">
    <h1 class="disp">Português</h1>
    <div class="yr"><span class="pill">5.º Ano</span><span class="man">Manual do aluno</span></div>
    <div class="sub">Português Língua Materna · 5.º ano</div>
  </div>
</section>"""


def p_imprint(M):
    rows = [
        ("Edição", f"1.ª edição, 2026. Formato A4 (210 × 297 mm), impressão a cores, {M['total']} páginas."),
        ("Editora", "A Prime School Press é a chancela editorial da Prime School, Portugal."),
        ("Direitos", "© Prime School 2026. Todos os direitos reservados. Nenhuma parte desta publicação pode ser reproduzida, armazenada ou transmitida, por qualquer forma ou meio, sem autorização prévia e escrita do editor."),
        ("Textos", "Os textos originais desta edição são © Prime School. As obras protegidas — de Sophia de Mello Breyner Andresen, Ondjaki e José Jorge Letria — aparecem só em excertos breves, ao abrigo do direito de citação para fins de ensino (Código do Direito de Autor, art. 75.º, n.º 2, al. h), sempre com o nome do autor e da obra; as obras completas leem-se na aula. Os textos tradicionais são recontados por nós."),
        ("Imagens", "Ilustrações criadas para esta edição, geradas digitalmente e revistas pela equipa editorial; não retratam pessoas reais."),
        ("Em linha", "Os códigos QR levam só a páginas públicas de instituições e obras de referência (dicionários, museus, municípios, arquivos); foram todos testados em setembro de 2026."),
        ("Créditos", "Conselho Editorial. Grupo Académico Pedagógico · Equipa Pedagógica · Departamento Pedagógico · Equipa de Criação de Conteúdos. Escrito, ilustrado e paginado no estúdio da Prime School Press."),
        ("Ortografia", "Português europeu, segundo o Acordo Ortográfico de 1990."),
        ("Professores", f"No fim do livro: soluções de todas as unidades ({pp(*M['span']['Soluções'])}){tpl_ref(M)}, planificação anual (p. {M['bp']['Planificação anual']}) e todos os códigos QR (p. {M['bp']['Recursos digitais']})."),
        ("ISBN", "A atribuir na primeira impressão."),
    ]
    rh = "".join(f'<div class="r"><b>{k}</b><span>{v}</span></div>' for k, v in rows)
    inside = [
        "Sete unidades: informar e descrever, narrar, poesia, teatro, revisões, avaliação e atividades extra",
        "Lenda, relato, biografia, «O Rapaz de Bronze», «Ynari», poemas e peças de teatro",
        "Atividades numeradas em três níveis: bronze, prata e ouro",
        f"{M['n_qr']} códigos QR para páginas públicas, todos reunidos na p. {M['bp']['Recursos digitais']}",
        "Quatro testes, grelhas de autoavaliação e um balanço do ano",
        f"Soluções, glossário, referências e planificação nas pp. {M['back_first']}–{M['bp']['Colofão']}",
    ]
    ih = "".join(f"<li>{E(x)}</li>" for x in inside)
    return f"""
<section class="page even imprint">
  <div class="capline"><span>P R I M E &nbsp; S C H O O L &nbsp; P R E S S</span><img src="../art/logo_prime_school.png" alt=""></div>
  <h1 class="disp">Português · 5.º Ano</h1>
  <div class="st">Manual do aluno · Português Língua Materna · 5.º ano</div>
  <div class="bar"></div>
  <p class="hook">Ler para saber, ler para sonhar — e escrever e falar com as próprias palavras.</p>
  <p class="leadp">Um ano de português em sete unidades: textos que informam, histórias de cá e de lá do mar, poemas para dizer a duas vozes, peças para pôr em cena. A osga Mourinha acompanha-te do princípio ao fim.</p>
  <div class="inside"><div class="lab">D E N T R O &nbsp; D E S T E &nbsp; L I V R O</div><ul>{ih}</ul></div>
  <div class="card"><div class="ctab">F I C H A &nbsp; T É C N I C A</div>{rh}</div>
  <div class="ifoot">
    <p><b>Publicação independente.</b> Esta é uma publicação independente, produzida pela Prime School para uso nos seus próprios programas de estudo. Não é afiliada, licenciada, patrocinada nem aprovada pelo Ministério da Educação, por qualquer júri de exames ou por outra editora. Segue as Aprendizagens Essenciais de Português do 5.º ano.</p>
    <div class="rt"><span>9–10 anos · 5.º Ano</span><b>www.primeschool.pt</b></div>
  </div>
</section>"""


def p_howto(M):
    chips = "".join(f'<span style="background:{u["c"]}">{u["n"]}</span>' for u in UNITS)
    demo_qr = M["demo_qr"]
    return f"""
<section class="page odd howto">
  {run("Português · 5.º Ano", "Antes de começar", "Como usar este livro")}
  <div class="kick">Antes de começar</div>
  <h1 class="disp">Como usar este livro</h1>
  <p class="lead" style="margin-top:3mm">Sete unidades, cada uma com a sua cor: quatro tipos de texto, as revisões, os testes e um baú de jogos. Conhece as peças que se repetem em todas as páginas.</p>
  <div class="hgrid">
    <div class="hc">
      <div class="lab">1 · A cor da unidade</div>
      <div class="chips">{chips}</div>
      <p>Cada unidade abre com uma <b>página ilustrada</b> e tem uma cor. A cor repete-se no separador da margem, no cabeçalho e no número da página.</p>
    </div>
    <div class="hc">
      <div class="lab">2 · Onde estou?</div>
      <div class="minirun"><span>O Gabinete das Coisas Verdadeiras</span><span><b>Sala 1</b> · A Enciclopédia</span></div>
      <p>No <b>cabeçalho</b> lês o nome da unidade e da secção. O <b>separador</b> na margem ajuda-te a encontrar a secção de dedo.</p>
    </div>
    <div class="hc wide">
      <div class="lab">3 · As atividades</div>
      <div class="act-h demo" style="--c:var(--verde)"><span class="num">7</span>{key_svg("prata")}<h3>Procura três factos no artigo</h3><span class="skill">Ler</span></div>
      <p>As atividades estão <b>numeradas</b> de 1 até ao fim de cada unidade; as perguntas de cada atividade têm letras — a), b), c). A etiqueta à direita diz o que treinas: <i>ler, escrever, falar, ouvir, gramática</i>.</p>
    </div>
    <div class="hc wide keysc">
      <div class="lab">4 · As três chaves</div>
      <div class="k3">
        <div>{key_svg("bronze")}<b>Bronze</b><span>aquecer — começa por aqui</span></div>
        <div>{key_svg("prata")}<b>Prata</b><span>aplicar o que aprendeste</span></div>
        <div>{key_svg("ouro")}<b>Ouro</b><span>desafiar-te a ir mais longe</span></div>
      </div>
    </div>
    <div class="hc">
      <div class="lab">5 · Explorar em linha</div>
      <div class="qr">{qr_svg(demo_qr)}<div class="ql"><b>Experimenta já</b>Aponta a câmara: {E(M['demo_what'])}.</div></div>
      <p style="margin-top:2mm">Os <b>códigos QR</b> levam a páginas públicas e seguras — dicionários, museus, arquivos. Estão todos na p. {M['bp']['Recursos digitais']}.</p>
    </div>
    <div class="hc">
      <div class="lab">6 · A Mourinha</div>
      <div class="tip"><img src="{MOU.format(3)}" alt=""><div class="bub">Sou a <b>Mourinha</b>, a osga do Gabinete. Deixo-te dicas como esta.</div></div>
      <p style="margin-top:2mm">Quando vires a osga, lê a dica <b>antes</b> de responderes.</p>
    </div>
    <div class="hc">
      <div class="lab">7 · Laboratório da língua</div>
      <div class="rule"><span class="lab">Regra</span>O <b>nome coletivo</b> designa um conjunto: <i>cardume, rebanho, biblioteca</i>.</div>
      <p style="margin-top:2mm">Nas caixas escuras está <b>a regra</b> de gramática, pronta para estudar e rever antes dos testes.</p>
    </div>
    <div class="hc">
      <div class="lab">8 · Escrever no livro</div>
      <p class="hand" style="font-size:15pt;line-height:1;color:#223a78;margin:1mm 0 -1mm">Era uma vez uma osga…</p>
      <span class="ln s"></span><span class="ln s"></span>
      <p style="margin-top:1.6mm">Escreve a <b>lápis</b> nas linhas e nas caixas. No fim de cada unidade, faz o <b>balanço</b>: «Sou capaz de…».</p>
    </div>
  </div>
  <div class="steps4">
    <div class="lab" style="grid-column:1/5;color:var(--ink)">Estudar com este livro, em quatro passos</div>
    <div><b>1</b><h4>Lê duas vezes</h4><p>A primeira para perceber; a segunda, de lápis na mão, para sublinhar.</p></div>
    <div><b>2</b><h4>Começa no bronze</h4><p>Faz as chaves pela ordem. O ouro fica para quando estiveres pronto.</p></div>
    <div><b>3</b><h4>Responde por inteiro</h4><p>Frase completa, com uma prova do texto entre aspas.</p></div>
    <div class="dk"><b>4</b><h4>Confirma e corrige</h4><p>No balanço, pinta o que já sabes e volta ao que falta.</p></div>
  </div>
  {folio("iii", True)}
</section>"""


def p_map(M):
    cards = []
    for u in M["units"]:
        kinds = "".join(f"<span>{E(k)}</span>" for k in u["kinds"])
        cards.append(f"""
    <div class="mc" style="--c:{u['c']};--t:{u['t']}">
      <img src="../art/{u['vign']}.png" alt="">
      <div class="mtop"><div class="mh"><span class="big">{u['n']}</span><span class="lab">Unidade {u['n']} · {pp(u['first'], u['last'])}</span></div>
      <h3>{E(u['title'])}</h3>
      <div class="gen">{E(u['genre'])}</div></div>
      <p class="bq">{E(u['q'])}</p>
      <div class="kinds">{kinds}</div>
    </div>""")
    bp = M["bp"]
    cards.append(f"""
    <div class="mc fim">
      <img src="../art/v-livros.png" alt="">
      <div class="mtop"><div class="mh"><span class="big">{SPARK}</span><span class="lab">Fim do livro · {pp(M['back_first'], bp['Colofão'])}</span></div>
      <h3>A caixa de ferramentas</h3>
      <div class="gen">Para consultar durante todo o ano</div></div>
      <p class="bq">Onde confirmo uma resposta, uma palavra ou uma fonte?</p>
      <div class="kinds"><span>soluções</span><span>glossário</span><span>recursos digitais</span><span>planificação</span></div>
    </div>""")
    return f"""
<section class="page even map">
  {run("Português · 5.º Ano", "Antes de começar", "Mapa do ano")}
  <div class="kick">Mapa do ano · Prime School Press</div>
  <h1 class="disp">Um ano, sete viagens</h1>
  <p class="lead" style="margin-top:2.6mm">Cada unidade faz uma <b>grande pergunta</b>. No fim de cada viagem vais ser capaz de lhe responder — com textos que leste, escreveste e disseste em voz alta.</p>
  <div class="mgrid">{''.join(cards)}</div>
  {folio("iv", True)}
</section>"""


def _index_card(u):
    ents = []
    for e in u["entries"]:
        subs = f'<i> — {E(e["first_sub"])}</i>' if e.get("first_sub") else ""
        lab = E(e["label"])
        lab = re.sub(r"^Laborat[óo]rio da L[íi]ngua · ", '<em class="lab-pill">Lab</em>', lab)
        lab = re.sub(r"^Oficina de escrita · ", '<em class="lab-pill of">Oficina</em>', lab)
        ents.append(f'<li><span class="t"><b>{lab}</b>{subs}</span><span class="pg">{e["page"]}</span></li>')
    return f"""
  <div class="ic" style="--c:{u['c']};--t:{u['t']}">
    <div class="ib"><span>{u['n']}</span></div>
    <div class="ibody">
      <div class="ih"><div><div class="lab">Unidade {u['n']} · {E(u['genre'])}</div><h3>{E(u['title'])}</h3></div><div class="ipg">{u['first']}</div></div>
      <ul class="{ 'two' if len(ents) > 5 else '' }" style="--rows:{(len(ents) + 1) // 2 if len(ents) > 5 else len(ents)}">{''.join(ents)}</ul>
    </div>
  </div>"""


def _colour_bar(M):
    seg = "".join(f'<span style="flex:{u["last"]-u["first"]+1};background:{u["c"]}"><i>{u["n"]}</i></span>' for u in M["units"])
    return f'<div class="cbar"><span class="fm" style="flex:8"></span>{seg}<span class="fm" style="flex:8"></span></div><div class="cbar-l"><span>i</span><span>1</span><span>{M["units"][-1]["last"]}</span><span>{M["total"]- 8 - 144 + 144}</span></div>'


def p_index(M):
    split = M["index_split"]
    a = "".join(_index_card(u) for u in M["units"][:split])
    b = "".join(_index_card(u) for u in M["units"][split:])
    bp = M["bp"]
    fim = "".join(f'<li><span class="t"><b>{E(t)}</b></span><span class="pg">{p}</span></li>' for t, p in M["back_index"])
    ante = "".join(f'<li><span class="t"><b>{E(t)}</b></span><span class="pg">{p}</span></li>' for t, p in M["front_index"])
    return f"""
<section class="page odd index">
  {run("Português · 5.º Ano", "Índice", "")}
  <div class="kick">Índice</div>
  <h1 class="disp">O ano em sete unidades</h1>
  {_colour_bar(M)}
  {a}
  {folio("v", True)}
</section>
<section class="page even index">
  {run("Português · 5.º Ano", "Índice", "continuação")}
  <div class="kick">Índice · continuação</div>
  {b}
  <div class="ic fimc">
    <div class="ib"><span>{SPARK}</span></div>
    <div class="ibody">
      <div class="ih"><div><div class="lab">Antes de começar e fim do livro</div><h3>Ferramentas para o ano inteiro</h3></div><div class="ipg">{M['back_first']}</div></div>
      <div class="fimgrid"><ul>{ante}</ul><ul>{fim}</ul></div>
    </div>
  </div>
  {folio("vi", True)}
</section>"""


def p_reading(M):
    rows = []
    for r in M["readings"]:
        u = ucolor(r["unit"])
        rows.append(f'<tr><td class="u"><span style="background:{u["c"]}">{r["unit"]}</span></td><td class="w"><b>{E(r["title"])}</b><small>{E(r["kind"])} · p. {r["page"]}</small></td><td class="d"></td><td class="s">{STARS}</td><td class="f"></td></tr>')
    for _ in range(M["own_rows"]):
        rows.append(f'<tr class="own"><td class="u"><span class="o">+</span></td><td class="w"><i>Por minha conta:</i></td><td class="d"></td><td class="s">{STARS}</td><td class="f"></td></tr>')
    return f"""
<section class="page odd reading">
  {run("Português · 5.º Ano", "Antes de começar", "O meu ano de leitura")}
  <div class="kick">Antes de começar · O meu ano de leitura</div>
  <div class="rtop">
    <div>
      <h1 class="disp">Diário de leitura</h1>
      <p class="lead" style="margin-top:2.4mm">Estas são as leituras do ano, pela ordem do livro. Quando acabares uma, escreve a <b>data</b>, pinta as <b>estrelas</b> e guarda uma <b>frase</b> — tua ou do texto. Nas últimas linhas, junta os livros que leres por tua conta.</p>
    </div>
    <div class="tip"><img src="{MOU.format(4)}" alt=""><div class="bub">Cinco estrelas = <b>quero reler!</b> Uma estrela = não era para mim — e também é bom saber isso.</div></div>
  </div>
  <table class="log"><thead><tr><th>Un.</th><th>Leitura</th><th>Li em</th><th>Gostei</th><th>Uma frase para lembrar</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
  {folio("vii", True)}
</section>"""


def p_profile(M):
    likes = ["aventuras", "mistério", "banda desenhada", "poesia", "teatro", "animais e natureza", "ciência", "vidas de pessoas reais", "humor", "contos tradicionais", "fantasia", "notícias"]
    lk = "".join(f"<span><i class='chk'></i>{x}</span>" for x in likes)
    goals = [("Ler", "verde", "ler um livro inteiro por mês"), ("Escrever", "verm", "escrever sem esquecer a pontuação"),
             ("Falar e ouvir", "turq", "falar para a turma sem ler o papel"), ("Gramática", "ultra", "conjugar bem os verbos no passado")]
    gh = ""
    for name, col, ex in goals:
        gh += f"""<div class="goal" style="--c:var(--{col})"><div class="gh"><b>{name}</b><span class="per"><i>1.º</i><i>2.º</i><i>3.º</i></span></div>
        <p class="ex">por exemplo: <span class="hand">{ex}</span></p><span class="ln s"></span><span class="ln s"></span><span class="ln s"></span></div>"""
    return f"""
<section class="page even profile">
  {run("Português · 5.º Ano", "Antes de começar", "Quem sou eu como leitor")}
  <div class="kick">Antes de começar · Quem sou eu como leitor</div>
  <h1 class="disp">Eu, leitor — e os meus objetivos</h1>
  <div class="pgrid">
    <div class="frame"><div class="ph"><span>Desenha-te aqui<br>(ou cola uma fotografia)</span></div>
      <div class="fl"><b>Nome</b><span></span></div><div class="fl"><b>Turma</b><span></span></div><div class="fl"><b>Ano letivo</b><span></span></div></div>
    <div class="me">
      <div class="lab">Eu, leitor</div>
      <div class="q"><b>Gosto de ler sobre…</b><div class="likes">{lk}</div></div>
      <div class="q"><b>Leio melhor…</b><div class="likes"><span><i class='chk'></i>na cama</span><span><i class='chk'></i>no sofá</span><span><i class='chk'></i>na biblioteca</span><span><i class='chk'></i>no carro</span><span><i class='chk'></i>ao ar livre</span></div></div>
      <div class="q"><b>O último livro de que gostei muito</b><span class="ln s"></span></div>
      <div class="q"><b>Um livro que quero ler este ano</b><span class="ln s"></span></div>
      <div class="q"><b>Para mim, ler é como…</b><span class="ln s"></span></div>
    </div>
  </div>
  <div class="lab" style="margin:5mm 0 2mm;color:var(--ink)">Os meus objetivos para o 5.º ano <span style="color:var(--ink2);letter-spacing:.06em">— no fim de cada período, pinta o círculo se já conseguiste</span></div>
  <div class="goals">{gh}</div>
  <div class="ptip tip"><img src="{MOU.format(1)}" alt=""><div class="bub">Um bom objetivo é <b>pequeno e claro</b>: «ler 10 minutos antes de dormir» ganha a «ler mais».</div></div>
  {folio("viii", True)}
</section>"""


# ============================================================ BACK MATTER
def p_glossary(M):
    cols = M["gloss_pages"]
    out = []
    for k, entries in enumerate(cols):
        pno = M["bp"]["Glossário"] + k
        body, last = [], None
        for g in entries:
            L = g["term"][0].upper()
            L = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}.get(L, L)
            if L != last:
                body.append(f'<h4 class="L">{L}</h4>')
                last = L
            u = ucolor(g["unit"])
            body.append(f'<p><b>{E(g["term"])}</b> <span class="gp" style="background:{u["c"]}">{g["page"]}</span> — {E(g["def"])}</p>')
        head = ('<div class="kick">Fim do livro · Glossário</div><h1 class="disp">Glossário</h1>'
                '<p class="lead gl-lead">As palavras-chave do ano, por ordem alfabética. O número indica a <b>página onde a palavra é ensinada</b>; a cor, a unidade.</p>'
                + '<div class="glegend">' + "".join(f'<span><i style="background:{u["c"]}"></i>{u["n"]} · {E(u["short"])}</span>' for u in M["units"][:4]) + "</div>") if k == 0 else '<div class="kick">Fim do livro · Glossário (continuação)</div>'
        par = "odd" if pno % 2 else "even"
        out.append(f"""
<section class="page {par} gloss-p">
  {run("Português · 5.º Ano", "Fim do livro", "Glossário" + (" (continuação)" if k else ""))}
  {head}
  <div class="gcols">{''.join(body)}</div>
  {'<div class="gfoot"><div class="mygl"><div class="lab">O meu glossário · palavras novas que encontrei este ano</div>' + ''.join('<div class="myr"><span></span><span></span></div>' for _ in range(4)) + '</div><div class="tip"><img src="' + MOU.format(2) + '" alt=""><div class="bub">Não encontras uma palavra? Procura-a no <b>dicionário</b> — aprendeste a usá-lo na p. 8.</div></div></div>' if k == len(cols) - 1 else ''}
  {folio(pno)}
</section>""")
    return "".join(out)


SHORT_TITLES = {  # the resource cards hold two lines of title: shorter forms, edited by hand
    "Ouvir: a biografia de Aristides de Sousa Mendes": "Ouvir: a biografia de Aristides",
    "A lenda no site do Município de Barcelos": "A lenda no site de Barcelos",
    "Ouvir: «O Vento Brincalhão» e «Chuva na Cidade»": "Ouvir: o vento e a chuva",
    "A osga no Museu Virtual da Biodiversidade": "A osga no Museu Virtual",
    "Aristides de Sousa Mendes no site da DGE": "Aristides no site da DGE",
    "Ouvir: «O Mistério das Coisas de Lã»": "Ouvir: «O Mistério das Coisas de Lã»",
    "Dicionário Priberam (em linha)": "Dicionário Priberam",
    "A história do teatro no D. Maria II": "O teatro no D. Maria II",
}


def p_resources(M):
    pno = M["bp"]["Recursos digitais"]
    groups = {}
    for q in M["qrs"]:  # one card per address; a code printed on two pages shows both pages
        groups.setdefault(q["url"], []).append(q)
    cells = []
    for url, qs in groups.items():
        q = qs[0]
        u = ucolor(q["unit"])
        short = q["short"]
        segs = short.rstrip("/").split("/")
        if len(short) > 44 and len(segs) > 2:  # long external address: domain/…/last-segment (the QR holds the full URL)
            short = f"{segs[0]}/…/{segs[-1]}"
        title = SHORT_TITLES.get(q["title"], q["title"])
        pages = "p. " + str(q["page"]) if len(qs) == 1 else "pp. " + " e ".join(str(x["page"]) for x in qs)
        qz = 4 if len(groups) <= 24 else (1 if len(url) > 110 else 2)  # few codes: the full 4-module quiet zone
        cells.append(f"""<div class="rq" style="--c:{u['c']};--t:{u['t']}">{qr_svg(url, "m" if qz == 4 else "l", qz)}<div class="rl"><span class="rp"><i>{q['unit']}</i>{pages}</span><b>{E(title)}</b><small>{E(short)}</small></div></div>""")
    legend = "".join(f'<span><i style="background:{u["c"]}">{u["n"]}</i>{E(u["short"])}</span>' for u in M["units"])
    return f"""
<section class="page {'odd' if pno % 2 else 'even'} res">
  {run("Português · 5.º Ano", "Fim do livro", "Recursos digitais")}
  <div class="rhead"><div><div class="kick">Fim do livro · Recursos digitais</div>
  <h1 class="disp">Recursos digitais</h1></div>
  <p class="lead res-lead">Os {M['n_qr']} códigos QR do livro, pela ordem das páginas{" (um endereço repetido aparece uma vez)" if len(groups) < M['n_qr'] else ""}. Todos levam a <b>páginas públicas</b> de instituições e obras de referência, testadas em setembro de 2026; nos endereços longos, «…» substitui o meio — o código tem o endereço completo.</p></div>
  <div class="rg{" big" if len(groups) <= 24 else ""}">{''.join(cells)}</div>
  {folio(pno)}
</section>"""


def p_refs(M):
    pno = M["bp"]["Referências e créditos"]
    blocks = []
    for u in M["units"]:
        refs = M["refs"].get(u["n"], [])
        if not refs:
            continue
        li = "".join(f"<li>{r}</li>" for r in refs)
        blocks.append(f'<div class="rf" style="--c:{u["c"]}"><div class="rfh"><span>{u["n"]}</span>{E(u["title"])}</div><ul>{li}</ul></div>')
    gen = "".join(f"<li>{r}</li>" for r in M["refs_general"])
    return f"""
<section class="page {'odd' if pno % 2 else 'even'} refs">
  {run("Português · 5.º Ano", "Fim do livro", "Referências e créditos")}
  <div class="kick">Fim do livro · Referências e créditos</div>
  <h1 class="disp">Referências e créditos</h1>
  <p class="lead" style="margin-top:2mm;font-size:10.4pt">Obras, edições e fontes usadas em cada unidade. As obras protegidas por direitos de autor aparecem apenas em <b>excertos breves</b>, com fins de ensino e com indicação do autor e da obra; lê-as inteiras na aula ou na biblioteca.</p>
  <div class="rfcols">{''.join(blocks)}<div class="rf gen"><div class="rfh"><span>{SPARK}</span>Créditos da edição</div><ul>{gen}</ul></div></div>
  {folio(pno)}
</section>"""


def p_plan(M):
    pno = M["bp"]["Planificação anual"]
    rows = []
    for per in M["plan"]:
        first = True
        for r in per["rows"]:
            u = ucolor(r["unit"]) if r["unit"] else None
            col = u["c"] if u else "#8C8577"
            rows.append(f'<tr>{"<td class=per rowspan=" + str(len(per["rows"])) + "><b>" + per["name"] + "</b><span>" + per["when"] + "</span></td>" if first else ""}'
                        f'<td class="wk">{r["weeks"]}</td><td class="un"><span style="background:{col}">{r["unit"] or SPARK}</span></td>'
                        f'<td class="ct"><b>{E(r["what"])}</b>{"<small>" + E(r["detail"]) + "</small>" if r["detail"] else ""}</td><td class="pgs">{r["pages"]}</td></tr>')
            first = False
    return f"""
<section class="page {'odd' if pno % 2 else 'even'} plan">
  {run("Português · 5.º Ano", "Fim do livro", "Planificação anual")}
  <div class="kick">Fim do livro · Planificação anual</div>
  <h1 class="disp">Planificação anual</h1>
  <p class="lead" style="margin-top:2mm;font-size:10.4pt">Uma proposta para <b>{M['weeks']} semanas</b> de aulas, ao ritmo das aulas de Português de cada semana. O professor ajusta o ritmo à turma; as <b>Atividades Extra</b> (Unidade 7) usam-se ao longo de todo o ano.</p>
  <table class="pl"><thead><tr><th>Período</th><th>Semanas</th><th>Un.</th><th>Conteúdos</th><th>Páginas</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
  {folio(pno)}
</section>"""


def p_close(M):
    pno = M["bp"]["O meu 5.º ano — antes de fechar o livro"]
    prompts = ["O texto do ano de que mais gostei foi…", "A personagem que eu queria conhecer é…", "O verso ou a frase que vou guardar é…",
               "Na escrita, melhorei sobretudo em…", "Na oralidade, o momento de que mais me orgulho foi…", "A regra de gramática que já não esqueço é…",
               "O livro que vou ler nas férias é…", "Uma pergunta que ainda tenho sobre a língua portuguesa é…"]
    ph = "".join(f'<div class="cp"><b><i>{k+1}</i>{E(t)}</b><span class="ln"></span><span class="ln"></span><span class="ln"></span></div>' for k, t in enumerate(prompts))
    return f"""
<section class="page {'odd' if pno % 2 else 'even'} close">
  {run("Português · 5.º Ano", "Fim do livro", "O meu 5.º ano")}
  <div class="kick">Fim do livro · O meu 5.º ano</div>
  <h1 class="disp">Antes de fechar o livro</h1>
  <p class="lead" style="margin-top:2.4mm">Oito frases para completar no último dia de aulas. Guarda esta página: no 6.º ano, vais gostar de a reler.</p>
  <div class="cgrid">{ph}</div>
  <div class="cfoot">
    <div class="tip"><img src="{MOU.format(2)}" alt=""><div class="bub">Foi um ano cheio de palavras. <b>Obrigada pela companhia</b> — e boas leituras de verão!</div></div>
    <div class="sig"><span></span><small>assinatura do leitor</small></div>
  </div>
  {folio(pno)}
</section>"""


def p_colophon(M):
    pno = M["bp"]["Colofão"]
    cards = [
        ("Texto e língua", "Português europeu, segundo o Acordo Ortográfico de 1990. Os textos originais foram escritos para esta edição; os excertos de obras protegidas são breves e citados com autor e obra."),
        ("Tipografia", "Fraunces (títulos e textos para ler), Figtree (instruções e atividades), DM Mono (etiquetas e legendas) e Caveat (notas manuscritas) — todas com licença SIL Open Font License, integradas no PDF."),
        ("Ilustração", "Capa e contracapa da coleção Prime Books do 5.º ano. Imagens interiores criadas para esta edição com ferramentas digitais de geração de imagem, à maneira do guache e do lápis de cor, com grão de papel visível e cor mate."),
        ("Para o professor", f"As soluções de todas as unidades estão no fim do livro ({pp(*M['span']['Soluções'])}).{tpl_colo(M)} Não há gravações: os textos para ouvir são lidos pela voz do professor."),
        ("Impressão", f"Formato A4 (210 × 297 mm), a cores, {M['total']} páginas: 8 de abertura (i–viii), 144 de unidades e {M['total'] - 152} de fim do livro. Cada unidade tem a sua cor."),
        ("Recursos digitais", f"{M['n_qr']} códigos QR, só para páginas públicas, todos testados antes da impressão (setembro de 2026) e reunidos na p. {M['bp']['Recursos digitais']}."),
    ]
    ch = "".join(f'<div class="cc"><div class="lab">{t}</div><p>{E(x)}</p></div>' for t, x in cards)
    bar = "".join(f'<span style="background:{u["c"]}"></span>' for u in M["units"])
    return f"""
<section class="page {'odd' if pno % 2 else 'even'} colo">
  {run("Português · 5.º Ano", "Fim do livro", "Colofão")}
  <div class="kick">Fim do livro · Colofão</div>
  <h1 class="disp">Como este livro foi feito</h1>
  <div class="ccgrid">{ch}</div>
  <div class="cbar7">{bar}</div>
  <blockquote><p>«Minha pátria é a língua portuguesa.»</p><cite>Bernardo Soares (Fernando Pessoa), <i>Livro do Desassossego</i></cite></blockquote>
  <div class="owner"><div class="lab">Este livro pertence a</div><span class="l1"></span><div class="lab">Turma</div><span class="l2"></span><div class="lab">Ano letivo</div><span class="l3"></span></div>
  <div class="vstrip">{''.join(f'<figure style="--c:{u["c"]}"><img src="../art/{u["vign"]}.png" alt=""><figcaption><b>{u["n"]}</b>{E(u["short"])}</figcaption></figure>' for u in M["units"])}</div>
  <div class="imprint-mini"><img src="../art/logo_prime_school.png" alt=""><span>Prime School Press · Português · 5.º Ano · 1.ª edição, 2026</span></div>
  {folio(pno)}
</section>"""


def p_backcover(M):
    bullets = ["Sete unidades, do artigo de enciclopédia ao teatro", "A Lenda do Galo de Barcelos, «O Rapaz de Bronze» e «Ynari»",
               "Poemas para dizer a duas vozes e peças para pôr em cena", "Atividades em três níveis: bronze, prata e ouro",
               f"{M['n_audio']} áudios em português europeu, com códigos QR", "Quatro testes, balanço do ano, glossário e planificação"]
    bh = "".join(f"<li>{E(b)}</li>" for b in bullets)
    return f"""
<section class="page even backc">
  <div class="stripe"></div>
  <div class="art"></div>
  <div class="bc">
    <div class="imp">P R I M E &nbsp; S C H O O L &nbsp; P R E S S</div>
    <h1 class="disp">Português</h1>
    <div class="abar"></div>
    <div class="sub">5.º Ano · Prime School Press · Manual do aluno</div>
    <p class="hook">Um ano inteiro a ler, a escrever e a falar — com uma osga por companhia.</p>
    <p class="blurb">Português Língua Materna para o 5.º ano: textos que informam e descrevem, lendas e contos, a literatura dos países de língua portuguesa, poesia e teatro. Cada página foi desenhada para se ler com gosto e para se escrever nela a lápis.</p>
    <div class="card"><div class="lab">N E S T E &nbsp; L I V R O</div><ul>{bh}</ul></div>
  </div>
  <div class="bfoot"><b>Prime School Press · Português</b><span>9–10 anos · 5.º Ano</span><em>primeschool.pt</em></div>
</section>"""


def tpl_ref(M):
    return f", textos para o professor ler em voz alta ({pp(*M['span']['Textos para o professor'])})" if M["span"].get("Textos para o professor") else ""


def tpl_colo(M):
    return f" Nas atividades de compreensão do oral, o professor lê em voz alta os textos das {pp(*M['span']['Textos para o professor'])}." if M["span"].get("Textos para o professor") else ""


# ============================================================ SOLUÇÕES + TEXTOS PARA O PROFESSOR (one flowing document)
def _flow_template(sec, first, kick, title, lead, right):
    head = f'<div class="kick">{kick}</div><h1 class="disp">{title}</h1><p class="lead sol-lead">{lead}</p>' if first else f'<div class="kick">{kick} · continuação</div>'
    return (f'<template data-sec="{sec}" data-first="{1 if first else 0}"><section class="page sol sec-{sec}">'
            f'{run("Português · 5.º Ano", "Fim do livro", right)}{head}<div class="cols"></div><footer class="folio"></footer></section></template>')


SOL_LEAD = ("Todas as respostas do livro, unidade a unidade. Nas perguntas abertas há um <b>exemplo</b> ou os <b>critérios</b> "
            "que orientam a resposta — aceitam-se todas as respostas bem justificadas com o texto. Primeiro, tenta sozinho; "
            "depois, confirma — e corrige a lápis.")
TPL_LEAD = ("Nas atividades de <b>compreensão do oral</b> e nos ditados, o professor lê estes textos em voz alta, na aula. "
            "Não aparecem nas páginas das atividades: quem ouve não os lê antes. Cada texto indica a página e a atividade.")


def p_flow(sol_blocks, tpl_blocks, start):
    T = [_flow_template("sol", True, "Fim do livro · Soluções", "Soluções", SOL_LEAD, "Soluções"),
         _flow_template("sol", False, "Fim do livro · Soluções", "Soluções", SOL_LEAD, "Soluções")]
    src = f'<div class="flowsrc" data-sec="sol">{"".join(sol_blocks)}</div>'
    if tpl_blocks:
        T += [_flow_template("tpl", True, "Fim do livro · Para o professor", "Textos para o professor ler em voz alta", TPL_LEAD, "Textos para o professor"),
              _flow_template("tpl", False, "Fim do livro · Para o professor", "Textos para o professor", TPL_LEAD, "Textos para o professor")]
        src += f'<div class="flowsrc" data-sec="tpl">{"".join(tpl_blocks)}</div>'
    return f'<div id="pg-templates" style="display:none">{"".join(T)}</div>{src}', start


FRONT_PAGES = [p_imprint, p_howto, p_map, p_index, p_reading, p_profile]  # i (cover) = the master's front, set by covers.py
BACK_PAGES = [p_glossary, p_resources, p_refs, p_plan, p_close, p_colophon]  # the back cover = the master's back, covers.py
