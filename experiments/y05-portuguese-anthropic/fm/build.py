#!/usr/bin/env python3
"""Build the book matter of «Português · 5.º Ano — Manual do aluno».

    /root/.hermes/cache/scratch/exp-venv/bin/python build.py [--harvest] [--check] [front|back]

--harvest  re-run harvest.py first (reads every unit's built PDF/HTML; cached by mtime)
--check    print the per-page DOM metrics (content bottom / right edge) after building

Outputs: build/front.pdf (8 pp.), build/back.pdf (8 pp.), build/png-front/NN.png, build/png-back/NN.png,
build/model.json (the data every page was built from).
"""
import json
import os
import re
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
ART = os.path.join(HERE, "art")
# headless_shell: the full chrome's --headless=new print path hangs on this (heavily loaded) host
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
sys.path.insert(0, HERE)
import pages  # noqa: E402
import solutions  # noqa: E402
from glossary import G, TAUGHT_AT  # noqa: E402
from plan import BACK_FIRST, PAL, UNITS, back_plan, total  # noqa: E402

SHORT = {1: "Informar e descrever", 2: "Narrativa", 3: "Poesia", 4: "Teatro", 5: "Revisões", 6: "Avaliação", 7: "Extra"}

# ---------------------------------------------------------------- curated overrides (edited by hand)
QR_TITLES = {  # url fragment -> short title for the «Recursos digitais» page (edited by hand; unknown URLs fall back to the label)
    "cienciaviva.pt/meias-com-ciencia": "Ciência Viva: a ficha da osga-comum",
    "arquivos.rtp.pt/conteudos/a-lenda-do-galo-de-barcelos": "RTP Arquivos: a Lenda do Galo de Barcelos",
    "arquivos.rtp.pt/conteudos/o-palacio-da-pena": "RTP Arquivos: o Palácio da Pena",
    "arquivos.rtp.pt/conteudos/um-electrico-chamado-28": "RTP Arquivos: um elétrico chamado 28",
    "ensina.rtp.pt/artigo/wwii-sousa-mendes": "RTP Ensina: os refugiados de Sousa Mendes",
    "ensina.rtp.pt/explicador/cinco-dicas-para-comunicar-com-sucesso": "RTP Ensina: cinco dicas para comunicar",
    "ensina.rtp.pt/artigo/a-contracena-no-teatro": "RTP Ensina: a contracena no teatro",
    "ensina.rtp.pt/artigo/sabe-o-que-e-uma-marcacao-em-teatro": "RTP Ensina: a marcação em teatro",
    "ensina.rtp.pt/artigo/adivinhas-que-animal-sou-eu": "RTP Ensina: adivinhas — que animal sou eu?",
    "ensina.rtp.pt/artigo/o-rato-roeu-a-rolha": "RTP Ensina: «O rato roeu a rolha»",
    "ensina.rtp.pt/explicador/recursos-expressivos-a-nivel-fonico": "RTP Ensina: recursos expressivos fónicos",
    "ensina.rtp.pt/explicador/recursos-expressivos-a-nivel-semantico": "RTP Ensina: recursos expressivos semânticos",
    "rtp.pt/play/estudoemcasa": "RTP Play: #EstudoEmCasa, Português",
    "wilder.pt/naturalistas": "Wilder: os pardais de Portugal",
    "listavermelhadasaves.pt": "O pardal-comum na Lista Vermelha das Aves",
    "pt.wikipedia.org/wiki/Caligrama": "«Caligrama» na Wikipédia",
    "priberam.org/onomatopeia": "«onomatopeia» no Dicionário Priberam",
    "priberam.org/pt-pt/lamela": "«lamela» no Dicionário Priberam",
    "tarentola-mauritanica": "A osga no Museu Virtual da Biodiversidade",
    "priberam.org/lamela": "«lamela» no Dicionário Priberam",
    "cm-barcelos.pt": "A lenda no site do Município de Barcelos",
    "aristides-de-sousa-mendes": "Aristides de Sousa Mendes no site da DGE",
    "tndm.pt": "A história do teatro no D. Maria II",
    "estacao-do-pinhao": "Os azulejos da estação do Pinhão",
    "dicionario.priberam.org/": "Dicionário Priberam (em linha)",
}

QR_SOURCES = {  # url fragment -> institution, for the references page
    "arquivos.rtp.pt": "RTP Arquivos", "ensina.rtp.pt": "RTP Ensina", "rtp.pt/play": "RTP Play", "priberam.org": "Dicionário Priberam",
    "cm-barcelos.pt": "Município de Barcelos", "dge.mec.pt": "DGE", "tndm.pt": "Teatro Nacional D. Maria II",
    "ippatrimonio.pt": "IP Património", "museubiodiversidade.uevora.pt": "Museu Virtual da Biodiversidade",
    "cienciaviva.pt": "Ciência Viva", "wilder.pt": "Wilder", "listavermelhadasaves.pt": "Lista Vermelha das Aves",
    "wikipedia.org": "Wikipédia", "pnl2027.gov.pt": "Plano Nacional de Leitura", "bnportugal.gov.pt": "Biblioteca Nacional de Portugal",
    "infopedia.pt": "Infopédia",
}

READINGS = [  # the year's readings in book order (unit, title, kind, regex of the heading of the page where it is read)
    (1, "«A osga-comum»", "artigo de enciclopédia", r"A osga-comum"),
    (1, "«osga» e outras palavras", "verbetes de dicionário", r"A casa de cada palavra"),
    (1, "«A D. Guilhermina» e «O sótão do Gabinete»", "retratos", r"A D\. Guilhermina"),
    (1, "Os avisos do Gabinete", "avisos", r"Textos que se leem de passagem"),
    (1, "«A visita guiada da Leonor»", "exposição oral", r"A visita guiada da Leonor"),
    (2, "«A Lenda do Galo de Barcelos»", "lenda tradicional", r"Lenda do Galo de Barcelos"),
    (2, "«Um dia em Sintra»", "relato de viagem", r"Um dia em Sintra"),
    (2, "«O cônsul que disse sim» — Aristides de Sousa Mendes", "biografia", r"O cônsul que disse sim"),
    (2, "«Uma língua, muitas casas»", "literaturas de língua portuguesa", r"Uma língua, muitas casas"),
    (2, "«O Rapaz de Bronze», Sophia de Mello Breyner Andresen", "conto (excerto; obra lida na aula)", r"^O Rapaz de Bronze"),
    (2, "«Ynari, a Menina das Cinco Tranças», Ondjaki", "conto (excerto; obra lida na aula)", r"^Ynari"),
    (2, "«Os Pardais da Horta»", "narrativa: um problema para resolver", r"Os Pardais da Horta"),
    (2, "«O Mistério das Coisas de Lã»", "conto de mistério", r"Mistério das Coisas de Lã"),
    (2, "«No Elétrico 28»", "história contada com falas", r"No Elétrico 28"),
    (3, "«O Alfabeto dos Bichos», José Jorge Letria", "poesia (excertos)", r"cheios de bichos"),
    (3, "«Noite e Dia»", "poema a duas vozes", r"Noite e Dia"),
    (4, "«O Aviso»", "texto dramático em duas cenas", r"Duas Cenas: O Aviso"),
    (4, "«A Chave Desaparecida»", "texto dramático", r"A Chave Desaparecida|Detetives da leitura"),
]


REFS = {  # every source cited in the units + every copyrighted work quoted (collected from the units' small print, edited by hand)
    1: ["Museu Virtual da Biodiversidade, Universidade de Évora — ficha «<i>Tarentola mauritanica</i>» (osga-comum). museubiodiversidade.uevora.pt · pp. 4–5",
        "Ciência Viva — Agência Nacional para a Cultura Científica e Tecnológica. cienciaviva.pt · p. 4",
        "<i>Dicionário Priberam da Língua Portuguesa</i> (em linha), verbete «lamela». dicionario.priberam.org · p. 9",
        "Artigo, verbetes, retratos, avisos e visita guiada: textos originais desta edição."],
    2: ["Sophia de Mello Breyner Andresen, <i>O Rapaz de Bronze</i>, il. Inês do Carmo. Porto: Porto Editora, 2013 (1.ª ed. da obra: 1956). Excertos breves, pp. 44–47; obra lida na íntegra na aula.",
        "Ondjaki, <i>Ynari, a Menina das Cinco Tranças</i>, il. Danuta Wojciechowska. Lisboa: Editorial Caminho, 2004. Excertos breves, pp. 49–50; obra lida na íntegra na aula.",
        "Município de Barcelos, «A Lenda do Galo». cm-barcelos.pt — reconto original desta edição, p. 28",
        "Parques de Sintra – Monte da Lua, «Palácio Nacional da Pena» e «Castelo dos Mouros». parquesdesintra.pt · p. 33",
        "Fundação Sousa Mendes, «Aristides de Sousa Mendes: His Life and Legacy». sousamendesfoundation.org; Direção-Geral da Educação, «Honras de Panteão Nacional». dge.mec.pt · p. 37",
        "CPLP, «Estados-membros». cplp.org; mapa desenhado a partir de Natural Earth (domínio público) · p. 40",
        "Plano Nacional de Leitura; fichas de autor da Porto Editora, Caminho e Moderna; DGLAB, «Prémio Camões». dglab.gov.pt · p. 41",
        "RTP Ensina, «Ondjaki, prosador e poeta da urbe angolana»; Biblioteca Nacional de Portugal · p. 48",
        "<i>Dicionário Priberam</i>: soba, cubata, capim, olongo, batuque, mais-velho · p. 49",
        "Relato, biografia, «Os Pardais da Horta», «O Mistério das Coisas de Lã» e «No Elétrico 28»: originais desta edição."],
    3: ["José Jorge Letria, «Polvo» (excerto), em <i>O Alfabeto dos Bichos</i>, il. André Letria. Lisboa: Oficina do Livro, 2005. Excerto breve, p. 68; poema completo lido na aula.",
        "Sociedade Portuguesa de Autores, «José Jorge Letria». spautores.pt; Agrupamento de Escolas Cidadela. aecidadela.pt · p. 67",
        "Wikipédia, «Polvo» e «<i>Octopus vulgaris</i>» (consultado em setembro de 2026) · p. 68",
        "«O Coreto Adormecido», «O Vento Brincalhão», «Chuva na Cidade», «A Noite da Mourinha» e «Noite e Dia»: poemas originais desta edição."],
    4: ["Teatro Nacional D. Maria II, «História». tndm.pt · p. 88",
        "«Duas Cenas: O Aviso» e «A Chave Desaparecida»: textos dramáticos originais, escritos para o Grupo de Teatro do 5.º ano."],
    5: ["Aves de Portugal. avesdeportugal.info; ICNF — Instituto da Conservação da Natureza e das Florestas · p. 99",
        "Município de Barcelos, «A Lenda do Galo». cm-barcelos.pt · p. 104",
        "Portal da Literatura; Bertrand Editora · p. 106",
        "Infraestruturas de Portugal, «Estação do Pinhão». ippatrimonio.pt · p. 110",
        "Conto, poema «Comboio da noite», cena e relato: originais desta edição."],
    6: ["Florestas.pt, «Sobreiro: a árvore mãe da cortiça» (2020); ICNF, 6.º Inventário Florestal Nacional; concurso Árvore Europeia do Ano 2018 · p. 115",
        "Os textos dos quatro testes foram escritos para esta edição."],
    7: ["<i>Dicionário Priberam da Língua Portuguesa</i> (em linha). dicionario.priberam.org · p. 132",
        "«A estante da Mourinha»: títulos e autores confirmados em setembro de 2026 nos catálogos da Caminho, Porto Editora, Planeta Tangerina e Wook e na Biblioteca Nacional de Portugal · p. 141",
        "Jogos, adivinhas, trava-línguas e caligramas: originais desta edição ou da tradição oral."],
}
REFS_GENERAL = [
    "Direção-Geral da Educação, <i>Aprendizagens Essenciais — Português, 5.º ano</i>. dge.mec.pt",
    "<i>Código do Direito de Autor e dos Direitos Conexos</i>, art. 75.º, n.º 2, al. h) — citação para fins de ensino.",
    "Tipos: Fraunces, Figtree, DM Mono e Caveat (SIL Open Font License).",
    "Ilustrações: criadas para esta edição; capa e contracapa da coleção Prime Books. Logótipo: Prime School.",
]


# ---------------------------------------------------------------- model
def nice(s):
    """sentence-case an ALL-CAPS PDF running head (fallback only)"""
    if s and s.upper() == s:
        return " · ".join(p.strip().capitalize() for p in s.split("·"))
    return s


def opener(u):
    """unit colour, genre line and genre chips, read from the unit's own opener (build/unit.html)"""
    import html as HH
    p = os.path.join(ROOT, u["folder"], "build", "unit.html")
    if not os.path.exists(p):
        return {}
    s = open(p, encoding="utf-8").read()
    m = re.search(r'<section class="page[^"]*?p-open[^"]*"', s)
    out = {}
    if m:
        rc = re.search(r"\br-(\w+)", m.group(0))
        if rc and rc.group(1) in PAL:
            out["pal"] = rc.group(1)
            out["c"], out["t"] = PAL[rc.group(1)]
        sec = s[m.start(): s.find("</section>", m.start())]
        sm = re.search(r'<div class="sub"><span>(.*?)</span>(.*?)</div>', sec, re.S)
        if sm:
            clean = lambda x: re.sub(r"\s+", " ", HH.unescape(re.sub(r"<[^>]+>", "", x))).strip()
            out["genre"] = clean(sm.group(1))
            out["kinds"] = [k.strip() for k in clean(sm.group(2)).split("·") if k.strip()]
    return out


def load_harvest():
    p = os.path.join(BUILD, "harvest.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def unit_entries(u, h):
    """group the unit's pages (after the opener) by the section key of their running head"""
    if not h or not h.get("exists"):
        return [dict(label="(unidade em construção)", subs=[], page=u["first"], provisional=True)]
    groups = []
    for p in h["pages"]:
        if p["pdf_page"] == 1:
            continue
        hp = p.get("html") or {}
        runR = hp.get("runR") or nice(p.get("runR", ""))
        h1 = hp.get("h1") or p.get("h1") or ""
        h1 = re.sub(r"\s+", " ", h1).strip().rstrip(",")
        folio = u["first"] + p["pdf_page"] - 1
        parts = [x.strip() for x in runR.split("·")] if runR else [h1 or "—"]
        if len(parts) > 1 and re.match(r"(?i)unidade \d", parts[0]):
            parts = parts[1:]  # «Unidade 6 · Como usar esta unidade» -> «Como usar esta unidade»
        key = parts[0]
        label = key if (len(parts) == 1 or re.match(r"(?i)unidade", parts[1])) else f"{parts[0]} · {parts[1]}"
        new = not (groups and groups[-1]["key"] == key)
        if not new:
            g = groups[-1]
        else:
            g = dict(key=key, label=label, subs=[], page=folio, first_sub="")
            groups.append(g)
        h1 = h1.strip(" “”\"'«»")
        if h1.lower().startswith(parts[-1].lower() + " "):
            h1 = h1[len(parts[-1]):].strip()  # «O Palco A mala azul» (two display lines) under «Estação 4 · O Palco»
        if len(h1) >= 4 and h1 not in g["subs"] and h1.lower() != label.lower() and h1.lower() not in label.lower():
            g["subs"].append(h1)
            if new:
                g["first_sub"] = h1  # the Índice only shows a heading that is printed on the entry's own page
    return groups


def qr_title(url, label):
    m = re.search(r"solucoes(?:-u(\d))?\.html", url)
    if m:
        return f"Soluções da Unidade {m.group(1) or 1} (professor)"
    for k, v in QR_TITLES.items():
        if k in url:
            return v
    lab = re.sub(r"^(OUVIR|EXPLORAR|PARA O PROFESSOR|DICIONÁRIO ONLINE|VER|LER|ÁUDIO)\s+", "", label).strip()
    kind = "Ouvir: " if url.endswith(".mp3") else ""
    first = re.split(r"(?<=[.!?])\s", lab)[0].rstrip(".")
    m = re.search(r"solucoes(?:-u(\d))?\.html", url)
    if m:
        return f"Soluções da Unidade {m.group(1) or 1} (professor)"
    return (kind + first)[:62]


def find_page(h, u, pattern, prefer_bold=True):
    """page where `pattern` is TAUGHT: score running head, heading, bold spans and plain mentions;
    the opener, the welcome page and the closing balance page only count as a last resort"""
    if not h or not h.get("exists"):
        return None
    rx = re.compile(pattern, re.I)
    n = len(h["pages"])
    best, best_s = None, 0.0
    for p in h["pages"]:
        hp = p.get("html") or {}
        k = p["pdf_page"]
        s = 0.0
        if rx.search(hp.get("runR", "") or p.get("runR", "")):
            s += 6
        if rx.search(hp.get("h1", "") or "") or rx.search(p.get("h1", "")):
            s += 5
        s += 2.5 * min(2, sum(1 for x in p.get("bold", []) if rx.search(x)))
        s += 0.4 * min(5, len(rx.findall(p.get("text", ""))))
        if k in (1, 2) or k == n:
            s *= 0.15
        if s > best_s:
            best, best_s = u["first"] + k - 1, s
    return best if best_s > 0 else None



def model(n_sol=0, n_tpl=0):
    H = load_harvest()
    BACK = back_plan(n_sol, n_tpl)
    bp = {t.replace(" (continuação)", ""): p for p, t in reversed(BACK)}
    span = {}
    for p, t in BACK:
        k = t.replace(" (continuação)", "")
        a, b = span.get(k, (p, p))
        span[k] = (min(a, p), max(b, p))
    units = []
    for u in UNITS:
        h = H.get(str(u["n"]))
        v = dict(u)
        if h and h.get("exists"):
            op = h["pages"][0]
            t = (op.get("html") or {}).get("h1") or ""
            if t:
                v["title"] = re.sub(r"\s+", " ", t).strip()
            v.update(opener(u))
        v["short"] = SHORT[u["n"]]
        v["entries"] = unit_entries(u, h)
        v["built"] = bool(h and h.get("exists"))
        units.append(v)
    # QR codes of the whole book
    qrs = []
    for u in UNITS:
        h = H.get(str(u["n"])) or {}
        for q in h.get("qrs", []):
            qrs.append(dict(unit=u["n"], page=u["first"] + q["pdf_page"] - 1, url=q["url"],
                            title=qr_title(q["url"], q["label"]), short=re.sub(r"^https?://", "", q["url"]), label=q["label"]))
    n_audio = len({q["url"] for q in qrs if q["url"].endswith(".mp3")})
    # glossary (curated terms, pages resolved from the unit PDFs; unit glossaries override definitions)
    harvested_defs = {}
    for u in UNITS:
        h = H.get(str(u["n"])) or {}
        for p in h.get("pages", []):
            for t, d in (p.get("html") or {}).get("gloss", []):
                harvested_defs[t.lower()] = (d, u["n"])
    gl = []
    for term, un, d, pats in G:
        u = next(x for x in UNITS if x["n"] == un)
        h = H.get(str(un))
        page, prov = None, False
        if term in TAUGHT_AT and h and h.get("exists"):
            rxh = re.compile(TAUGHT_AT[term], re.I)
            page = next((u["first"] + p["pdf_page"] - 1 for p in h["pages"]
                         if rxh.search((p.get("html") or {}).get("h1", "") or p.get("h1", ""))), None)
        for pat in ([] if page else pats):
            page = find_page(h, u, re.escape(pat))
            if page:
                break
        if not page:
            page, prov = u["first"], True
        hd = harvested_defs.get(term.lower())
        gl.append(dict(term=term, unit=un, page=page, provisional=prov, def_=hd[0] if hd else d))
    for g in gl:
        g["def"] = g.pop("def_")
        g["def"] = g["def"][0].lower() + g["def"][1:] if g["def"] and not g["def"][:2].isupper() else g["def"]
        if not g["def"].endswith("."):
            g["def"] += "."
    import locale  # noqa
    gl.sort(key=lambda g: g["term"].translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc")).lower())
    cut = int(len(gl) * 0.53)
    gloss_pages = [gl[:cut], gl[cut:]]
    # readings
    readings = []
    for un, title, kind, rx in READINGS:
        u = next(x for x in UNITS if x["n"] == un)
        h = H.get(str(un))
        rxh = re.compile(rx, re.I)
        pg = next((u["first"] + p["pdf_page"] - 1 for p in (h or {}).get("pages", [])
                   if rxh.search(re.sub(r"\s+", " ", (p.get("html") or {}).get("h1", "") or p.get("h1", "")).strip())), None) \
            or find_page(h, u, rx) or u["first"]
        readings.append(dict(unit=un, title=title, kind=kind, page=pg))
    # refs: curated + harvested small-print sources
    refs = {k: list(v) for k, v in REFS.items()}
    refs_harvested = []
    for u in UNITS:
        h = H.get(str(u["n"])) or {}
        for p in h.get("pages", []):
            for s in (p.get("html") or {}).get("sources", []):
                refs_harvested.append((u["n"], p["pdf_page"], s))
    # the institutions behind the book's public QR codes (one line; the addresses are on «Recursos digitais»)
    qr_insts = []
    for u in UNITS:
        by = {}
        for q in qrs:
            if q["unit"] != u["n"] or "vercel" in q["url"] or q["url"].endswith(".mp3"):
                continue
            name = next((v for k, v in QR_SOURCES.items() if k in q["url"]), re.sub(r"^https?://(www\.)?", "", q["url"]).split("/")[0])
            by.setdefault(name, [])
            if q["page"] not in by[name]:
                by[name].append(q["page"])
        for n in by:
            if n not in qr_insts:
                qr_insts.append(n)
    # year plan: 34 weeks
    refs_general = list(REFS_GENERAL)
    if qr_insts:
        refs_general.insert(2, f"Códigos QR (lista completa na p. {bp['Recursos digitais']}): " + ", ".join(qr_insts) + ".")
    plan = year_plan(units, bp)
    front_index = [("Como usar este livro", "iii"), ("Mapa do ano", "iv"), ("Índice", "v"), ("O meu ano de leitura", "vii"), ("Quem sou eu como leitor", "viii")]
    back_index = [({"Textos para o professor": "Textos para o professor ler em voz alta"}.get(t, t), p) for p, t in BACK if "continuação" not in t]
    pub = [q for q in qrs if "vercel" not in q["url"] and not q["url"].endswith(".mp3")]
    dq = next((q for q in pub if "osga" in q["url"] or "tarentola" in q["url"]), pub[0] if pub else None)
    demo = dq["url"] if dq else "https://dicionario.priberam.org/"
    demo_what = f"abres «{dq['title']}» (p. {dq['page']})" if dq else "abres o Dicionário Priberam"
    return dict(units=units, qrs=qrs, n_qr=len(qrs), n_audio=n_audio, gloss_pages=gloss_pages, readings=readings,
                own_rows=1, refs=refs, refs_harvested=refs_harvested, refs_general=refs_general, plan=plan, weeks=34, bp=bp,
                total=total(n_sol, n_tpl), back=BACK, span=span, back_first=BACK_FIRST, n_sol=n_sol, n_tpl=n_tpl,
                front_index=front_index, back_index=back_index, demo_qr=demo, demo_what=demo_what, index_split=3)


def year_plan(units, bp):
    U = {u["n"]: u for u in units}

    def rng(u, a=0, b=None):
        es = u["entries"][a:b]
        if not es:
            return "", ""
        lo = es[0]["page"]
        nxt = u["entries"][b]["page"] - 1 if b is not None and b < len(u["entries"]) else u["last"]
        det = "; ".join(e["label"] if not e["label"].startswith("Laborat") else re.sub(r"^Laborat[óo]rio da L[íi]ngua · ", "gramática: ", e["label"]) for e in es)
        return det, f"pp. {lo}–{nxt}" if lo != nxt else f"p. {lo}"

    def row(un, weeks, what, a=0, b=None):
        det, pgs = rng(U[un], a, b)
        return dict(unit=un, weeks=weeks, what=what, detail=det, pages=pgs)

    u2 = U[2]["entries"]
    half = max(1, len(u2) // 2)
    P1 = [dict(unit=None, weeks="1", what="Antes de começar", detail="Como usar este livro · Mapa do ano · Diário de leitura · Quem sou eu como leitor", pages="pp. iii–viii"),
          row(1, "2–6", f"Unidade 1 · {U[1]['title']}"),
          row(2, "7–14", f"Unidade 2 · {U[2]['title']} (1.ª parte)", 0, half)]
    P2 = [row(2, "15–18", f"Unidade 2 · {U[2]['title']} (2.ª parte)", half, None),
          row(3, "19–24", f"Unidade 3 · {U[3]['title']}")]
    P3 = [row(4, "25–28", f"Unidade 4 · {U[4]['title']}"),
          row(5, "29–31", f"Unidade 5 · {U[5]['title']}"),
          row(6, "32–34", f"Unidade 6 · {U[6]['title']}"),
          dict(unit=7, weeks="todo o ano", what=f"Unidade 7 · {U[7]['title']}", detail="para quem acaba mais cedo, trabalhos de casa, clubes e férias", pages=f"pp. {U[7]['first']}–{U[7]['last']}"),
          dict(unit=None, weeks="34", what="Fim do livro", detail="O meu 5.º ano — antes de fechar o livro · Diário de leitura completo", pages=f"p. {bp['O meu 5.º ano — antes de fechar o livro']}")]
    for r in P1 + P2 + P3:  # keep the detail line short
        if len(r["detail"]) > 190:
            r["detail"] = r["detail"][:187].rsplit("; ", 1)[0] + "; …"
    return [dict(name="1.º período", when="setembro – dezembro", rows=P1),
            dict(name="2.º período", when="janeiro – março", rows=P2),
            dict(name="3.º período", when="abril – junho", rows=P3)]


# ---------------------------------------------------------------- render
def prep_art():
    for src, dst, w in [("cover.png", "cover.jpg", 1700), ("still.png", "still.jpg", 1800)]:
        s, d = os.path.join(ART, src), os.path.join(ART, dst)
        if not os.path.exists(s):
            continue
        if os.path.exists(d) and os.path.getmtime(d) > os.path.getmtime(s):
            continue
        im = Image.open(s).convert("RGB")
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(d, quality=88, optimize=True, progressive=True)


def html_doc(title, sections):
    css = open(os.path.join(HERE, "src", "common.css"), encoding="utf-8").read() + open(os.path.join(HERE, "src", "pages.css"), encoding="utf-8").read()
    return f'<!doctype html>\n<html lang="pt-PT"><head><meta charset="utf-8"><title>{title}</title><style>\n{css}\n</style></head><body>\n{sections}\n</body></html>\n'


METRICS_JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();let bot=0,right=0,over=[];
p.querySelectorAll('*').forEach(el=>{if(el.closest('.folio,.run,.art,.veil,.stripe,.ptip,.gtip,.gfoot,.cfoot,.bfoot,.ifoot,.imprint-mini,.vstrip'))return;const b=el.getBoundingClientRect();if(!b.height||el.children.length)return;bot=Math.max(bot,b.bottom-r.top);right=Math.max(right,b.right-r.left);
 if(el.scrollWidth>el.clientWidth+1&&getComputedStyle(el).overflow!=='visible')over.push(el.className||el.tagName)});
let fixed=null;p.querySelectorAll('.ptip,.gtip,.gfoot,.cfoot,.ifoot,.vstrip').forEach(t=>{const b=t.getBoundingClientRect();fixed=fixed===null?b.top-r.top:Math.min(fixed,b.top-r.top)});
out.push([i+1,mm(bot),fixed===null?null:mm(fixed),mm(right),over.slice(0,4)])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},600)})</script>"""


def chrome(args, timeout=540):
    import shutil
    import tempfile
    prof = tempfile.mkdtemp(prefix="chrome-fm-", dir=BUILD)  # fresh profile per run: no lock clashes with concurrent builds
    base = [CHROME, "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw", "--no-first-run", "--disable-extensions", f"--user-data-dir={prof}"]
    try:
        return subprocess.run(base + args, capture_output=True, text=True, timeout=timeout)
    finally:
        subprocess.run(["pkill", "-f", prof])
        shutil.rmtree(prof, ignore_errors=True)


def render(name, sections, check):
    import pymupdf
    out = os.path.join(BUILD, f"{name}.html")
    doc = html_doc(f"Português · 5.º Ano — {name}", sections)
    open(out, "w", encoding="utf-8").write(doc)
    if check:
        chk = os.path.join(BUILD, f"{name}-chk.html")
        open(chk, "w", encoding="utf-8").write(doc.replace("</body>", METRICS_JS + "</body>"))
        r = chrome(["--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + chk])
        m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
        print(f"[{name}] page contentBottom fixedTop maxRight overflow   (limits: bottom ≤ 280, right ≤ 194)")
        if m:
            import html as HH
            for row in json.loads(HH.unescape(m.group(1))):
                print("  ", row)
    pdf = os.path.join(BUILD, f"{name}.pdf")
    r = chrome(["--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={pdf}", "file://" + out])
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    d = pymupdf.open(pdf)
    pd = os.path.join(BUILD, f"png-{name}")
    os.makedirs(pd, exist_ok=True)
    for f in os.listdir(pd):
        os.remove(os.path.join(pd, f))
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=110).save(os.path.join(pd, f"{i+1:02d}.png"))
    fonts = sorted({(f[2], f[3]) for pg in d for f in pg.get_fonts()})
    print(f"[{name}] pages {d.page_count}  size {tuple(round(v,1) for v in d[0].rect)}  MB {os.path.getsize(pdf)/1e6:.2f}")
    print(f"[{name}] fonts {fonts}")
    return d.page_count


FLOW_SIZES = [8.3, 8.1, 8.5, 7.9, 8.7, 7.7]  # solutions type size (pt): first one whose page count keeps the book even


def flow_doc(sol_blocks, tpl_blocks, size):
    body, start = pages.p_flow(sol_blocks, tpl_blocks, BACK_FIRST)
    css = open(os.path.join(HERE, "src", "common.css"), encoding="utf-8").read() + open(os.path.join(HERE, "src", "pages.css"), encoding="utf-8").read()
    return (f'<!doctype html>\n<html lang="pt-PT"><head><meta charset="utf-8"><title>Português · 5.º Ano — Soluções</title><style>\n{css}\n</style></head>'
            f'<body data-start="{start}" style="--sfs:{size}pt">\n{body}\n{solutions.PAGINATE_JS}</body></html>\n')


def flow_report(doc):
    p = os.path.join(BUILD, "flow-chk.html")
    open(p, "w", encoding="utf-8").write(doc)
    r = chrome(["--virtual-time-budget=15000", "--window-size=794,1123", "--dump-dom", "file://" + p])
    m = re.search(r'<pre id="report"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m:
        sys.exit("flow: paginator produced no report\n" + r.stderr[-1500:])
    import html as HH
    return json.loads(HH.unescape(m.group(1)))


def render_flow(M0):
    """paginate «Soluções» + «Textos para o professor»; returns (n_sol, n_tpl, report)"""
    sol, srep = solutions.solutions_blocks(ROOT, M0["units"])
    tpl, trep = solutions.teacher_blocks(ROOT, M0["units"])
    fixed = len(back_plan(0, 0))
    cands = []
    for size in FLOW_SIZES:
        rows = flow_report(flow_doc(sol, tpl, size))
        ns = sum(1 for r in rows if r[0] == "sol")
        nt = sum(1 for r in rows if r[0] == "tpl")
        tot = total(ns, nt)
        lasts = [r[3] for k, r in enumerate(rows) if k == len(rows) - 1 or rows[k + 1][0] != r[0]]
        print(f"[flow] {size}pt -> Soluções {ns} pp. + Textos {nt} pp. -> book {tot} pp. ({'even' if tot % 2 == 0 else 'odd'}); "
              f"last-page fill {lasts}%")
        if tot % 2 == 0:
            cands.append((min(lasts), size, rows, ns, nt))
            if min(lasts) >= 55:
                break
    if not cands:
        sys.exit("flow: no type size gives an even page count")
    # even book first; then the fullest last pages; the list order (8.3 first) breaks ties
    chosen = max(cands, key=lambda c: (c[0] >= 45, -abs(c[1] - 8.3) if c[0] >= 45 else c[0]))[1:]
    size, rows, ns, nt = chosen
    bad = [r for r in rows if r[4]]
    if bad:
        sys.exit(f"flow: overflow on {bad}")
    out = os.path.join(BUILD, "sol.html")
    open(out, "w", encoding="utf-8").write(flow_doc(sol, tpl, size))
    pdf = os.path.join(BUILD, "sol.pdf")
    r = chrome(["--no-pdf-header-footer", "--virtual-time-budget=15000", f"--print-to-pdf={pdf}", "file://" + out])
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    import pymupdf
    d = pymupdf.open(pdf)
    assert d.page_count == ns + nt, (d.page_count, ns, nt)
    rep = dict(size=size, n_sol=ns, n_tpl=nt, pages=rows, sources=srep, teacher=trep, fixed_back=fixed)
    json.dump(rep, open(os.path.join(BUILD, "flow-report.json"), "w"), ensure_ascii=False, indent=1)
    for x in srep + trep:
        if x.get("dropped"):
            print(f"[flow] u{x['unit']} {x['file']}: dropped {len(x['dropped'])} audio/vercel items: {[d[0] for d in x['dropped']]}")
    return ns, nt


def merge(parts, out):
    import pymupdf
    d = pymupdf.open()
    for p in parts:
        d.insert_pdf(pymupdf.open(p))
    d.save(out, garbage=3, deflate=True)
    pd = os.path.join(BUILD, "png-back")
    os.makedirs(pd, exist_ok=True)
    for f in os.listdir(pd):
        os.remove(os.path.join(pd, f))
    for i, pg in enumerate(d):
        pg.get_pixmap(dpi=110).save(os.path.join(pd, f"{i+1:02d}.png"))
    return d.page_count


def main():
    args = sys.argv[1:]
    os.makedirs(BUILD, exist_ok=True)
    if "--harvest" in args:
        subprocess.run([sys.executable, os.path.join(HERE, "harvest.py")], check=True)
    prep_art()
    check = "--check" in args
    M0 = model()
    ns, nt = render_flow(M0)
    if "--flow-only" in args:
        return
    M = model(ns, nt)
    assert M["total"] % 2 == 0, M["total"]
    json.dump(M, open(os.path.join(BUILD, "model.json"), "w"), ensure_ascii=False, indent=1)
    n = render("front", "".join(f(M) for f in pages.FRONT_PAGES), check)
    assert n == 7, f"front has {n} pages, expected 7 (ii–viii)"
    n = render("back-tail", "".join(f(M) for f in pages.BACK_PAGES), check)
    assert n == len(back_plan(0, 0)), f"back tail has {n} pages"
    n = merge([os.path.join(BUILD, "sol.pdf"), os.path.join(BUILD, "back-tail.pdf")], os.path.join(BUILD, "back.pdf"))
    assert n == len(M["back"]), (n, len(M["back"]))
    print(f"[book] front 1+7, units {sum(u['pages'] for u in UNITS)}, back {n} + back cover = {M['total']} pp.; "
          f"Soluções pp. {M['span']['Soluções']}, Textos {M['span'].get('Textos para o professor')}")


if __name__ == "__main__":
    main()
