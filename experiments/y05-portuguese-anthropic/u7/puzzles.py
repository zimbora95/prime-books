"""Programmatic, verified puzzles for Unit 7 (crossword, word search, domino).

Deterministic (fixed seeds) so every rebuild prints the same grids. Every generator
VERIFIES its output and raises if anything is wrong:
  * crossword — each answer is readable in the grid at its number/direction, no two
    words run together, every white cell belongs to a clued word, grid is connected;
  * word search — each word is found exactly once, the leftover letters spell the
    hidden message exactly;
  * domino — the 12 tiles close a single loop.
"""
import random

# ---------------------------------------------------------------- crossword
CW_WORDS = [
    ("DIDASCALIA", "Indicação, no texto de teatro, sobre gestos, cenário ou tom de voz."),
    ("PERSONAGEM", "Ser que participa na ação de uma história ou de uma peça."),
    ("ONOMATOPEIA", "Palavra que imita um som, como «tchibum!» ou «miau»."),
    ("METAFORA", "Figura de estilo que compara sem usar a palavra «como»."),
    ("NARRADOR", "Quem conta a história."),
    ("ESTROFE", "Conjunto de versos de um poema."),
    ("VERBETE", "Cada entrada de um dicionário, com a palavra e os seus significados."),
    ("LENDA", "Narrativa tradicional que mistura factos e fantasia, como a do Galo de Barcelos."),
    ("FACTO", "Informação que pode ser verificada."),
    ("AVISO", "Texto curto que alerta ou dá uma ordem, muitas vezes no imperativo."),
    ("VERSO", "Cada linha de um poema."),
    ("RIMA", "Semelhança de sons no fim de dois ou mais versos."),
    ("OSGA", "Réptil que sobe paredes lisas graças às lamelas dos dedos."),
    ("CENA", "Parte de um ato, no texto dramático."),
]


def _cw_try(words, size, rng):
    g = {}
    placed = []  # (word, r, c, dir)

    def ok(w, r, c, d):
        dr, dc = (0, 1) if d == "A" else (1, 0)
        if r < 0 or c < 0 or r + dr * (len(w) - 1) >= size or c + dc * (len(w) - 1) >= size:
            return -1
        # cell before / after must be empty
        if (r - dr, c - dc) in g or (r + dr * len(w), c + dc * len(w)) in g:
            return -1
        cross = 0
        for i, ch in enumerate(w):
            rr, cc = r + dr * i, c + dc * i
            if (rr, cc) in g:
                if g[(rr, cc)][0] != ch or d in g[(rr, cc)][1]:
                    return -1
                cross += 1
            else:
                # side neighbours must be empty (no accidental words)
                for sr, sc in ((rr + dc, cc + dr), (rr - dc, cc - dr)):
                    if (sr, sc) in g:
                        return -1
        return cross

    def put(w, r, c, d):
        dr, dc = (0, 1) if d == "A" else (1, 0)
        for i, ch in enumerate(w):
            k = (r + dr * i, c + dc * i)
            if k in g:
                g[k] = (ch, g[k][1] | {d})
            else:
                g[k] = (ch, {d})
        placed.append((w, r, c, d))

    first = words[0]
    put(first, size // 2, (size - len(first)) // 2, "A")
    for w in words[1:]:
        cands = []
        for (rr, cc), (ch, _) in list(g.items()):
            for i, x in enumerate(w):
                if x != ch:
                    continue
                for d in "AD":
                    r, c = (rr, cc - i) if d == "A" else (rr - i, cc)
                    s = ok(w, r, c, d)
                    if s > 0:
                        cands.append((s, rng.random(), r, c, d))
        if cands:
            cands.sort(reverse=True)
            top = [x for x in cands if x[0] == cands[0][0]]
            s, _, r, c, d = rng.choice(top)
            put(w, r, c, d)
    return g, placed


def crossword(size=15, tries=4000, seed=7):
    rng = random.Random(seed)
    best = None
    words = [w for w, _ in CW_WORDS]
    for t in range(tries):
        order = words[:2] + rng.sample(words[2:], len(words) - 2) if t else words
        g, placed = _cw_try(order, size, rng)
        rs = [k[0] for k in g]; cs = [k[1] for k in g]
        h, wd = max(rs) - min(rs) + 1, max(cs) - min(cs) + 1
        score = (len(placed), -(h * wd), -abs(h - wd))
        if best is None or score > best[0]:
            best = (score, g, placed)
    _, g, placed = best
    if len(placed) != len(words):
        raise SystemExit(f"crossword: only {len(placed)}/{len(words)} placed")
    r0 = min(k[0] for k in g); c0 = min(k[1] for k in g)
    H = max(k[0] for k in g) - r0 + 1; W = max(k[1] for k in g) - c0 + 1
    grid = [[None] * W for _ in range(H)]
    for (r, c), (ch, _) in g.items():
        grid[r - r0][c - c0] = ch
    placed = [(w, r - r0, c - c0, d) for w, r, c, d in placed]
    # numbering in reading order
    starts = sorted({(r, c) for _, r, c, _ in placed})
    num = {rc: i + 1 for i, rc in enumerate(starts)}
    clue = dict(CW_WORDS)
    entries = sorted([(num[(r, c)], d, w, clue[w], r, c) for w, r, c, d in placed])
    _verify_cw(grid, entries)
    return {"grid": grid, "entries": entries, "num": {f"{r},{c}": n for (r, c), n in num.items()}, "H": H, "W": W}


def _verify_cw(grid, entries):
    H, W = len(grid), len(grid[0])
    cells_used = set()
    for n, d, w, _, r, c in entries:
        dr, dc = (0, 1) if d == "A" else (1, 0)
        got = "".join(grid[r + dr * i][c + dc * i] for i in range(len(w)))
        assert got == w, (n, d, w, got)
        before = (r - dr, c - dc); after = (r + dr * len(w), c + dc * len(w))
        for rr, cc in (before, after):
            if 0 <= rr < H and 0 <= cc < W:
                assert grid[rr][cc] is None, ("run-on", w)
        cells_used |= {(r + dr * i, c + dc * i) for i in range(len(w))}
    # every maximal run of >=2 letters must be an entry
    runs = set()
    for r in range(H):
        for c in range(W):
            for d, (dr, dc) in (("A", (0, 1)), ("D", (1, 0))):
                if grid[r][c] and not (0 <= r - dr and 0 <= c - dc and grid[r - dr][c - dc]):
                    L = 0
                    while r + dr * L < H and c + dc * L < W and grid[r + dr * L][c + dc * L]:
                        L += 1
                    if L > 1:
                        runs.add((r, c, d, L))
    ent = {(r, c, d, len(w)) for _, d, w, _, r, c in entries}
    assert runs == ent, ("unclued runs", runs - ent)
    white = {(r, c) for r in range(H) for c in range(W) if grid[r][c]}
    assert white == cells_used
    # connected
    seen, st = set(), [next(iter(white))]
    while st:
        p = st.pop()
        if p in seen:
            continue
        seen.add(p)
        for q in ((p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)):
            if q in white:
                st.append(q)
    assert seen == white, "grid not connected"


# ---------------------------------------------------------------- word search
WS_WORDS = ["POEMA", "ESTROFE", "RIMA", "VERSO", "LENDA", "CONTO", "FABULA", "TEATRO",
            "CENA", "FALA", "ARTIGO", "AVISO", "RETRATO", "NOTICIA"]
WS_MESSAGE = "LEREVIAJARSEMSAIRDACADEIRA"   # «Ler é viajar sem sair da cadeira.»
WS_DIRS = {"→": (0, 1), "↓": (1, 0), "↘": (1, 1), "←": (0, -1)}


def wordsearch(size=10, seed=3, tries=20000):
    rng = random.Random(seed)
    need = size * size - len(WS_MESSAGE)
    for t in range(tries):
        g = {}
        sol = []
        okall = True
        for w in sorted(WS_WORDS, key=len, reverse=True):
            opts = []
            for d, (dr, dc) in WS_DIRS.items():
                if d == "←" and rng.random() < .6:
                    continue
                for r in range(size):
                    for c in range(size):
                        er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                        if not (0 <= er < size and 0 <= ec < size):
                            continue
                        ov = 0; bad = False
                        for i, ch in enumerate(w):
                            k = (r + dr * i, c + dc * i)
                            if k in g:
                                if g[k] != ch:
                                    bad = True; break
                                ov += 1
                        if not bad and ov < len(w):
                            opts.append((ov, rng.random(), r, c, d))
            if not opts:
                okall = False; break
            ov, _, r, c, d = rng.choice(opts)
            dr, dc = WS_DIRS[d]
            for i, ch in enumerate(w):
                g[(r + dr * i, c + dc * i)] = ch
            sol.append((w, r, c, d))
        if not okall or len(g) != need:
            continue
        # every direction used at least once, and a few reversed words for «ouro»
        if len({x[3] for x in sol}) < 4:
            continue
        grid = [[g.get((r, c)) for c in range(size)] for r in range(size)]
        it = iter(WS_MESSAGE)
        for r in range(size):
            for c in range(size):
                if grid[r][c] is None:
                    grid[r][c] = next(it)
        try:
            _verify_ws(grid, sol)
        except AssertionError:
            continue
        return {"grid": grid, "sol": sorted(sol, key=lambda x: WS_WORDS.index(x[0])), "size": size, "tries": t + 1}
    raise SystemExit("word search: no layout found")


def _verify_ws(grid, sol):
    n = len(grid)
    alld = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]
    for w in WS_WORDS:
        hits = 0
        for r in range(n):
            for c in range(n):
                for dr, dc in alld:
                    s = ""
                    for i in range(len(w)):
                        rr, cc = r + dr * i, c + dc * i
                        if not (0 <= rr < n and 0 <= cc < n):
                            break
                        s += grid[rr][cc]
                    if s == w:
                        hits += 1
        assert hits == 1, (w, hits)
    used = set()
    for w, r, c, d in sol:
        dr, dc = WS_DIRS[d]
        used |= {(r + dr * i, c + dc * i) for i in range(len(w))}
    left = "".join(grid[r][c] for r in range(n) for c in range(n) if (r, c) not in used)
    assert left == WS_MESSAGE, left


# ---------------------------------------------------------------- domino
DOMINO = [  # (word, relation, answer)  — tile k shows [answer of k-1 | word k]
    ("alegre", "sin", "contente"), ("corajoso", "ant", "medroso"), ("começar", "sin", "iniciar"),
    ("antigo", "ant", "moderno"), ("rápido", "sin", "veloz"), ("generoso", "ant", "avarento"),
    ("esconder", "sin", "ocultar"), ("claro", "ant", "escuro"), ("enorme", "sin", "gigantesco"),
    ("chegar", "ant", "partir"), ("bonito", "sin", "belo"), ("aceitar", "ant", "recusar"),
]


def domino(seed=11):
    n = len(DOMINO)
    tiles = [(DOMINO[k - 1][2], DOMINO[k][0], DOMINO[k][1]) for k in range(n)]
    # verify loop: right side of k is answered by left side of k+1
    for k in range(n):
        assert tiles[(k + 1) % n][0] == DOMINO[k][2]
    order = list(range(n))
    random.Random(seed).shuffle(order)
    return {"tiles": [tiles[i] for i in order], "chain": [tiles[i] for i in range(n)]}


if __name__ == "__main__":
    cw = crossword()
    print("crossword", cw["H"], "x", cw["W"])
    for r in cw["grid"]:
        print(" ".join(ch or "." for ch in r))
    for e in cw["entries"]:
        print(e[:3])
    ws = wordsearch()
    print("wordsearch tries", ws["tries"])
    for r in ws["grid"]:
        print(" ".join(r))
    print(ws["sol"])
    print(domino()["tiles"])
