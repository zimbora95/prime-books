#!/usr/bin/env python3
"""Write site/solucoes-u7.html (teacher solutions + audio scripts) from the SAME puzzle data the book prints."""
import html as H, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build, puzzles, audio_scripts as A  # noqa: E402

P = build.load_puzzles()
cw, ws, dom = P["cw"], P["ws"], P["dom"]
os.makedirs(os.path.join(HERE, "site"), exist_ok=True)

clA = "".join(f"<li><b>{n}</b> {w}</li>" for n, d, w, *_ in cw["entries"] if d == "A")
clD = "".join(f"<li><b>{n}</b> {w}</li>" for n, d, w, *_ in cw["entries"] if d == "D")
wsl = " · ".join(f"{w} (linha {r+1}, coluna {c+1}, {d})" for w, r, c, d in ws["sol"])
chain = " → ".join(f"{a}|{b}" for a, b, _ in dom["chain"])
pairs = "".join(f"<li>{w} — {'sinónimo' if rel == 'sin' else 'antónimo'}: <b>{a}</b></li>" for w, rel, a in puzzles.DOMINO)


def script(name):
    return "".join(f"<p>{H.escape(t)}</p>" for _, _, _, t, _ in A.TRACKS[name])


page = f"""<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Soluções · Atividades Extra · Português Year 5 · Unidade 7</title>
<style>
body{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;max-width:780px;margin:0 auto;padding:24px 18px 60px;color:#1C2536;background:#F6F0E4;line-height:1.5}}
h1{{font-family:Georgia,serif;font-size:1.9rem;margin:.2em 0}}h2{{font-family:Georgia,serif;margin-top:1.8em;border-bottom:2px solid #1C2536;padding-bottom:.2em}}
.k{{font:600 .75rem ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:#C9761C}}
dl{{display:grid;grid-template-columns:max-content 1fr;gap:.3em 1em}}dt{{font-weight:700}}
audio{{width:100%;margin:.4em 0 1em}}
.note{{background:#fff;border-radius:8px;padding:.8em 1em;border:1px solid #D8CCB6}}
.grids{{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}}
table.cw,table.ws{{border-collapse:collapse;background:#fff}}
table.cw td{{width:26px;height:26px;border:1px solid #1C2536;text-align:center;font:700 14px Georgia,serif;position:relative;padding:0}}
table.cw td.x{{border:none;background:transparent}}
table.cw td i{{position:absolute;left:1px;top:0;font:500 8px ui-monospace,monospace;color:#2D4BA8}}
table.ws td{{width:26px;height:26px;border:1px solid #DCD3C0;text-align:center;font:600 14px ui-monospace,monospace;padding:0}}
table.ws td.on{{background:#DCE1F3;color:#1C2536}}table.ws td.left{{background:#FBEFD2;color:#9A6512}}
ol.c{{list-style:none;padding:0;columns:2}}ol.c li{{margin-bottom:.2em}}
details{{background:#fff;border:1px solid #D8CCB6;border-radius:8px;padding:.6em 1em;margin:.6em 0}}summary{{font-weight:700;cursor:pointer}}
</style></head><body>
<div class="k">Português · Year 5 · Unidade 7 · Para o professor</div>
<h1>Atividades Extra — soluções</h1>
<p class="note">Respostas dos jogos (pp. 131–144) e guiões dos áudios. As grelhas foram geradas e verificadas por programa: cada palavra está na grelha exatamente onde a pista indica. Nas tarefas de escrita e de oralidade, aceitam-se todas as respostas adequadas.</p>

<h2>1 · Palavras cruzadas do ano (p. 131)</h2>
<div class="grids">{build.cw_grid(cw, solved=True)}
<div><b>Horizontais</b><ol class="c" style="columns:1">{clA}</ol><b>Verticais</b><ol class="c" style="columns:1">{clD}</ol></div></div>

<h2>2 · Sopa de letras com segredo (p. 132)</h2>
<div class="grids">{build.ws_grid(ws, solved=True)}
<div style="max-width:360px"><p>Azul: as 14 palavras. Amarelo: as letras que sobram.</p><p><b>Frase secreta:</b> «Ler é viajar sem sair da cadeira.»</p><p style="font-size:.85rem">{wsl}</p><p style="font-size:.85rem">Escritas ao contrário (←): CENA e ARTIGO.</p></div></div>

<h2>3 · O jogo do dicionário (p. 132)</h2>
<dl><dt>alfarrábio</dt><dd>a) livro antigo e, geralmente, muito grande.</dd>
<dt>almocreve</dt><dd>b) pessoa que conduzia animais de carga, a transportar mercadorias.</dd>
<dt>bátega</dt><dd>c) chuva grossa e forte que cai de repente.</dd>
<dt>galhofa</dt><dd>b) risota, brincadeira barulhenta.</dd>
<dt>mafarrico</dt><dd>a) criança traquina, endiabrada (em sentido figurado; também quer dizer «diabo»).</dd>
<dt>sarapintado</dt><dd>c) com pintas de várias cores.</dd></dl>
<p class="note">Definições verdadeiras confirmadas no Dicionário Priberam da Língua Portuguesa. As falsas foram inventadas para o jogo.</p>

<h2>4–5 · O jogo das famílias e a fábrica de palavras (p. 133)</h2>
<dl><dt>MAR</dt><dd>maresia, marinheiro, marítimo, maré</dd>
<dt>LIVRO</dt><dd>livraria, livrinho, livreiro, livrete</dd>
<dt>PEDRA</dt><dd>pedreiro, pedregulho, empedrado, pedrada</dd>
<dt>FLOR</dt><dd>florista, floreira, florir, florido</dd>
<dt>Impostoras</dt><dd>flauta, livre (de <i>liberdade</i>), pedal (de <i>pé</i>), marmelada (de <i>marmelo</i>)</dd>
<dt>5</dt><dd>desfazer (voltar a separar o que estava feito) · reler (ler outra vez) · infeliz (que não é feliz) · sapateiro (quem faz ou arranja sapatos) · casinha (casa pequena) · colherada (o que cabe numa colher).</dd>
<dt>Ouro</dt><dd>Família de <i>terra</i> (exemplos): terreno, terreiro, terrestre, terráqueo, terramoto, enterrar, desenterrar, aterrar, aterragem, território, conterrâneo, térreo. As pistas: terramoto (treme), extraterrestre (vem de outro planeta), aterrar (o avião, no fim da viagem).</dd></dl>

<h2>6 · Dominó dos sinónimos e dos antónimos (p. 134)</h2>
<ul>{pairs}</ul>
<p style="font-size:.85rem"><b>O círculo completo</b> (peças como aparecem, metade esquerda|metade direita): {chain} → volta à primeira.</p>

<h2>7–11 · Escrita criativa (pp. 135–137)</h2>
<dl><dt>7–10</dt><dd>Respostas livres. Verificar: estrutura da narrativa (situação inicial, problema, tentativas, resolução); na carta — local e data, saudação, corpo, despedida, assinatura; no diário — 1.ª pessoa, pretérito perfeito e imperfeito.</dd>
<dt>11</dt><dd>Respostas livres. Ouro — exemplo: «— Olha, Mourinha, é um mapa! — exclamou a Leonor, a apontar para o farol.»</dd></dl>

<h2>12–15 · Oralidade (pp. 138–139)</h2>
<dl><dt>12</dt><dd>Sons repetidos: m · ch · p · s · g · tr (aliteração).</dd>
<dt>13</dt><dd>Jogo livre.</dd><dt>14</dt><dd>Imperfeito: era, brincavas, era (livro preferido); perfeito: mudou.</dd><dt>15</dt><dd>Livre.</dd></dl>

<h2>16–19 · Clube de leitura (pp. 140–141)</h2>
<p>Livre. Os dez livros recomendados na p. 141 foram confirmados em catálogos de editoras e livrarias e na Biblioteca Nacional de Portugal (setembro de 2026).</p>

<h2>20–21 · O jornal da turma (pp. 142–143)</h2>
<p>Projeto livre. Na manchete: frase curta, com verbo. No lead: quem, o quê, quando, onde (e, se couber, como e porquê).</p>

<h2>22–23 · Poesia visual e adivinhas (p. 144)</h2>
<dl><dt>22</dt><dd>Texto do caligrama: «{H.escape(build.CALI_TEXT)}»</dd>
<dt>23</dt><dd>1 o livro · 2 a osga · 3 o pente · 4 o escuro · 5 a agulha · 6 o mapa.</dd></dl>

<h2>Áudios</h2>
<p>u7-01 · Trava-línguas da Mourinha (p. 138)</p><audio controls src="audio/u7-01-trava-linguas.mp3"></audio>
<details><summary>Guião</summary>{script("u7-01-trava-linguas")}</details>
<p>u7-02 · Adivinha, adivinha! (p. 144)</p><audio controls src="audio/u7-02-adivinhas.mp3"></audio>
<details><summary>Guião</summary>{script("u7-02-adivinhas")}</details>
<p>u7-03 · Começo de história: a chave do farol (p. 135)</p><audio controls src="audio/u7-03-comeco-de-historia.mp3"></audio>
<details><summary>Guião</summary>{script("u7-03-comeco-de-historia")}</details>
<p class="note">Vozes sintéticas em português europeu. Todos os textos gravados (trava-línguas, adivinhas, começo de história) são originais, escritos para este livro.</p>
</body></html>
"""
open(os.path.join(HERE, "site", "solucoes-u7.html"), "w", encoding="utf-8").write(page)
print("site/solucoes-u7.html", len(page))
