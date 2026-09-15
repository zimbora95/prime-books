#!/usr/bin/env python3
"""The house structure for a unit/subunit title, applied to every source.

    <Label> <N> · <Title>          e.g.  Unit 4 · Timeless tales

The catalogue is built from two very different sources - the school's input
spreadsheets, and (where no spreadsheet exists) the section list the reader reads
out of the book's own contents page. Both arrive with the same class of defect,
so both go through this one module:

  * SHOUTED LABELS      "UNIT 1 · FUTSAL"           -> "Unit 1 · Futsal"
  * a label that is not the book's label
                        "Stop 1 · Going places"     -> "Unit 1 · Going places"
  * FUSED WORDS         "Stop 8 · HowI feel"        -> "How I feel"
                        "Unidade 7 · A gotaeo jardim" -> "A gota e o jardim"
                        "1 · FINALPROJECT"          -> "Final Project"
  * STRAY SPACING       "TOPIC 1 . 3"               -> "Topic 1.3"
                        "Review exam3"              -> "Review exam 3"
  * BROKEN NUMBERING    "Unit 2, Unit 4, Unit 6"    -> "Unit 1, Unit 2, Unit 3"
                        "Unit 12, Unit 12, Unit 14" -> "Unit 1, Unit 2, Unit 3"

THE BOOK IS THE AUTHORITY FOR SPELLING. Fused words cannot be split by rule -
"A gotaeo jardim" is "A gota e o jardim" because that is what the book prints -
so the label is looked up in the title's own markdown text (public/markdown/
<slug>.md, the readable text of the same book) on a space-and-punctuation-free
key, and the spelling found there is adopted verbatim. Case is only forced where
the source SHOUTS: a label the author wrote in mixed case ("How I feel",
"Conhece o teu A Level Português") is left exactly as the book has it.

Nothing here invents content: a label the book does not corroborate is left
alone, and a title whose numbering is already sound is not touched.

    from title_norm import normalise_units        # the pipeline both writers use
    .venv/bin/python tools/normalise_titles.py    # dry run over every source
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PUB = REPO / "public"
MARKDOWN = PUB / "markdown"

# ---------------------------------------------------------------- vocabulary

# The label a numbered row opens with, in the house spelling. A source that
# calls its units something else ("Stop") is renamed: the page has one structure.
PREFIX = {
    "unit": "Unit", "unite": "Unité", "unidade": "Unidade", "unidad": "Unidad",
    "stop": "Unit", "tema": "Tema", "topic": "Topic", "module": "Module",
    "chapter": "Chapter", "term": "Term", "part": "Part",
}

# Words that stay lowercase inside a Title-Cased label (never the first word).
FUNCTION = {
    "en": {"a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "is",
           "of", "on", "or", "the", "to", "with", "vs"},
    "pt": {"a", "à", "às", "ao", "aos", "as", "da", "das", "de", "do", "dos", "e",
           "em", "na", "nas", "no", "nos", "o", "os", "ou", "para", "por", "um",
           "uma", "com", "sem"},
    "es": {"a", "al", "como", "con", "de", "del", "e", "el", "en", "la", "las",
           "los", "o", "para", "por", "un", "una", "y"},
    "de": {"am", "an", "auf", "der", "des", "die", "das", "im", "in", "mit", "und",
           "von", "zu", "zum", "zur"},
}

# Tokens that are already correct when a label is Title-Cased.
KEEP = {"ict", "it", "ai", "pe", "dt", "re", "stem", "uk", "usa", "eu", "un",
        "igd", "cambridge", "ib", "a", "an"}

ROMAN = re.compile(r"^[IVXLC]+$")
NUMWORD = re.compile(r"[0-9]")

# The subject decides which function words apply.
SUBJECT_LANG = (("portuguese", "pt"), ("português", "pt"), ("spanish", "es"),
                ("español", "es"), ("german", "de"), ("deutsch", "de"))


def lang_of(slug: str) -> str:
    s = (slug or "").lower()
    for key, lang in SUBJECT_LANG:
        if key in s:
            return lang
    return "en"


# ---------------------------------------------------------------- book text

_TEXT: dict[str, str] = {}


def book_text(slug: str) -> str:
    """The title's own readable text, or "" when there is none to consult."""
    if slug not in _TEXT:
        try:
            _TEXT[slug] = (MARKDOWN / f"{slug}.md").read_text(encoding="utf-8")
        except Exception:                                              # noqa: BLE001
            _TEXT[slug] = ""
    return _TEXT[slug]


MARKUP = re.compile(r"[*_`#>|]+")


def book_clean(slug: str) -> str:
    """The same text with markdown markers blanked, so a matched run never drags
    '**' or a '#' into a title."""
    return MARKUP.sub(" ", book_text(slug))


def squeeze(text: str):
    """Text -> a key with no spaces or punctuation, plus where each kept
    character sits in the original, so a hit can be mapped back to real text."""
    kept, pos = [], []
    for i, ch in enumerate(text):
        if ch.isalnum():
            kept.append(ch.lower())
            pos.append(i)
    return "".join(kept), pos


def split_label(label: str):
    """-> (prefix, title) for 'Unit 4 · Timeless tales' style labels."""
    if "·" in label:
        head, title = label.split("·", 1)
        return head.strip(), title.strip()
    return label.strip(), ""


# ---------------------------------------------------------------- case

def title_case(text: str, lang: str) -> str:
    """SHOUTED text -> the house's Title Case. Tokens carrying digits, roman
    numerals, single letters and known acronyms are left alone."""
    words = text.split()
    out = []
    for i, w in enumerate(words):
        m = re.match(r"^([^\w]*)(.*?)([^\w]*)$", w, re.UNICODE)
        lead, core, tail = (m.group(1), m.group(2), m.group(3)) if m else ("", w, "")
        low = core.lower()
        if not core or NUMWORD.search(core) or ROMAN.match(core) or len(core) == 1 \
                or low in KEEP:
            keep = core
        elif i and low in FUNCTION.get(lang, set()):
            keep = low
        else:
            keep = core[:1].upper() + core[1:].lower()
        out.append(lead + keep + tail)
    return " ".join(out)


def tidy(text: str) -> str:
    """Stray spacing the sources carry: 'TOPIC 1 . 3', 'Review exam3'.

    Deliberately narrow. Anything wider starts rewriting text the author wrote
    on purpose ("1st Term" -> "1 st Term", "micro:bit" -> "Micro: bit").
    """
    s = re.sub(r"\s+", " ", text).strip()
    s = re.sub(r"(\d)\s*\.\s*(?=\d)", r"\1.", s)      # "1 . 3" / "1 .3" -> "1.3"
    s = re.sub(r"\s+([,;:])", r"\1", s)               # "story , time" -> "story, time"
    s = re.sub(r"([a-zà-öø-ÿ]),(?=[^\s\d])", r"\1, ", s)   # "one,two" -> "one, two"
    s = re.sub(r"(?<=[a-zà-öø-ÿ])(?=\d)", " ", s)     # "exam3" -> "exam 3"
    return re.sub(r"\s+", " ", s).strip()


def norm_prefix(label: str) -> str:
    """'UNIT 1 · X' -> 'Unit 1 · X'; 'Stop 1 · X' -> 'Unit 1 · X'."""
    m = re.match(r"^([A-Za-zÀ-ÿ]+)\s*(\d+)(.*)$", label.strip(), re.UNICODE)
    if not m:
        return label
    word, num, rest = m.group(1), m.group(2), m.group(3)
    house = PREFIX.get(word.lower())
    if not house:
        return label
    return f"{house} {num}{rest}".strip()


# ---------------------------------------------------------------- recovery

def from_book(label: str, slug: str) -> str | None:
    """The book's own spelling of this label, or None when it cannot be found.

    The label is matched against the title's markdown on a spacing-free key, so
    a fused label ("HowI feel" -> "howifeel") still lands on the real text
    ("How I feel"), and the run found there is taken verbatim.
    """
    text = book_clean(slug)
    if not text:
        return None
    _, title = split_label(label)
    core = title or label
    key, _ = squeeze(core)
    if len(key) < 4:
        return None
    hay, pos = squeeze(text)
    if not hay:
        return None
    # Digits must correspond too: "1.3" and "13" share a spacing-free key, and
    # matching a different book's "TOPIC 13" onto "TOPIC 1 . 3" is a coin flip
    # the key cannot see. The digit runs, in order, settle it.
    want = re.findall(r"\d+", core)
    best = None
    start = hay.find(key)
    while start != -1:
        a, b = pos[start], pos[start + len(key) - 1]
        while a > 0 and text[a - 1].isalnum():
            a -= 1
        while b + 1 < len(text) and text[b + 1].isalnum():
            b += 1
        span = re.sub(r"^[^\w(]+", "", text[a:b + 1].strip())
        span = re.sub(r"\s+", " ", span).strip()
        if span and not re.search(r"[?*_#|<>]", span) \
                and re.findall(r"\d+", span) == want:   # a sentence is not a title
            score = 0
            if sum(c.islower() for c in span) >= 2:
                score += 3          # the author's own mixed case: trust it
            if "\n" in text[a:b + 1]:
                score -= 2          # a hit split across lines is a weaker match
            if len(span) > len(core) * 2.2:
                score -= 2
            if best is None or score > best[0]:
                best = (score, span)
        start = hay.find(key, start + 1)
    return best[1] if best and best[0] >= 0 else None


# ---------------------------------------------------------------- suspicion

_WORDS: dict[str, set[str]] = {}
WRD = re.compile(r"[^\W\d_]+", re.UNICODE)


def book_words(slug: str) -> set[str]:
    if slug not in _WORDS:
        _WORDS[slug] = {w.lower() for w in WRD.findall(book_clean(slug))}
    return _WORDS[slug]


def shouted(label: str) -> bool:
    """The source prints the whole title in capitals ("UNIT 1 · FUTSAL")."""
    _, title = split_label(label)
    core = title or label
    return bool(core == core.upper() and re.search(r"[A-ZÀ-Þ]{3}", core))


def suspect(label: str, slug: str) -> list[str]:
    """Tokens the book does not contain as words - the tell-tale of a fused
    label ('gotaeo', 'HowI', 'FINALPROJECT', 'textosdosmedia')."""
    pool = book_words(slug)
    if not pool:
        return []
    _, title = split_label(label)
    return [t for t in WRD.findall(title or label)
            if len(t) > 1 and t.lower() not in pool]


def needs_repair(label: str, slug: str) -> bool:
    """Only touch a label that is demonstrably wrong.

    A label the author wrote in mixed case and that the book corroborates
    ("Unit 7 · The night Rui would not sleep", "micro:bit and Robotics") is not a
    defect, and rewriting it would be the page inventing house style over the
    school's own words.
    """
    if shouted(label):
        return True
    if re.search(r"[a-zà-ÿ][A-ZÀ-Þ]", label):        # a fused camel boundary
        return True
    return bool(suspect(label, slug))


# ---------------------------------------------------------------- one label

def normalise_title(label: str, slug: str) -> tuple[str, list[str]]:
    """-> (house label, notes) for a single unit/subunit/section row."""
    notes: list[str] = []
    lang = lang_of(slug)
    label = tidy(re.sub(r"\s+", " ", str(label or "")).strip())
    if not label:
        return "", notes
    head, title = split_label(label)
    head = norm_prefix(head)
    if not title:
        return tidy(head), notes

    chosen = title
    if shouted(label):
        # The source shouts, so the house's Title Case decides - over the book's
        # own wording where the book can be found ("FINALPROJECT" -> "Final
        # Project", "CHECK YOUR PROGRESS" -> "Check Your Progress").
        found = from_book(label, slug)
        chosen = title_case(found or title, lang)
        if chosen != title:
            notes.append(f"SHOUTED label -> {chosen!r}"
                         + (f" (book: {found!r})" if found else ""))
    elif needs_repair(label, slug):
        found = from_book(label, slug)
        if found:
            chosen = found
            notes.append(f"spelling from the book: {title!r} -> {found!r}")
    chosen = tidy(chosen)
    if chosen and chosen[0].isalpha() and not chosen[0].isupper() \
            and chosen.split()[0].isalpha() \
            and chosen.split()[0].lower() not in FUNCTION.get(lang, set()):
        chosen = chosen[0].upper() + chosen[1:]
    return tidy(f"{head} · {chosen}" if head else chosen), notes


# ---------------------------------------------------------------- pipelines

def lead_number(title: str):
    m = re.match(r"^\s*[A-Za-zÀ-ÿ]+\s*(\d+)\s*(?:·|$)", title, re.UNICODE)
    return int(m.group(1)) if m else None


def lead_word(title: str) -> str:
    m = re.match(r"^\s*([A-Za-zÀ-ÿ]+)\s*\d+", title, re.UNICODE)
    return m.group(1) if m else "Unit"


def is_term(title: str) -> bool:
    """'Term 1' is a divider in the book's scheme, not a unit in its own right."""
    return bool(re.fullmatch(r"Term\s*\d+", title.strip(), re.I))


FURNITURE = re.compile(r"^(índice|indice|index|contents|table of contents|"
                       r"sumário|sumario|how to use this book)$", re.I)


def is_furniture(title: str) -> bool:
    """A contents page is not a unit, however the contents page lists itself."""
    _, own = split_label(title.strip())
    return bool(FURNITURE.match(own or title.strip()))


def renumber(units: list) -> list[str]:
    """Units numbered 1..N in the book's own order, each with its own subunits
    numbered to match.

    The numbers a contents page yields are frequently unusable (2,4,6 because
    every other opener was missed; 12,12,2,14; 0 eight times over), so a list
    that already reads 1..N is left exactly as the book printed it.
    """
    notes = []
    numbers = [lead_number(u["title"]) for u in units]
    if len(units) >= 2 and numbers != list(range(1, len(units) + 1)):
        notes.append(f"renumbered {numbers} -> 1..{len(units)}")
        for i, u in enumerate(units, start=1):
            word = lead_word(u["title"])
            _, own = split_label(u["title"])
            u["title"] = f"{word} {i} · {own}" if own else f"{word} {i}"
    for i, u in enumerate(units, start=1):
        n = lead_number(u["title"]) or i
        for j, s in enumerate(u.get("subs") or [], start=1):
            s["title"] = re.sub(r"^\s*\d+\.\d+\s*", f"{n}.{j} ", s["title"], count=1)
    return notes


def nest_repeats(units: list) -> list[str]:
    """Rows that repeat a unit's own number are that unit's subunits.

    'Unidade 1', 'Unidade 1 · TEXTO 1', 'Unidade 1 · TEXTO 2' is one unit with
    two subunits, not three units - the reader lists them flat because the
    book's contents page prints them flat.
    """
    notes = []
    out: list = []
    for u in units:
        title = u["title"]
        num = lead_number(title)
        prev = out[-1] if out else None
        same = bool(prev) and num is not None and lead_number(prev["title"]) == num
        if same and not is_term(title):
            _, sub = split_label(title)
            if not sub:
                # a bare 'Unit 12' twice over: the same row listed twice is one
                # row, two different pages are two stops
                if prev.get("page") == u.get("page"):
                    prev["multi"] = prev.get("multi", 1) + 1
                    continue
                out.append(u)
                continue
            dup = next((s for s in prev["subs"]
                        if s["title"] == sub and s.get("page") == u.get("page")), None)
            if dup is not None:
                dup["count"] = dup.get("count", 1) + 1
            else:
                prev["subs"].append({"title": sub, "page": u.get("page")})
                notes.append(f"{sub!r} nested under {prev['title']!r}")
            continue
        out.append(u)
    for u in out:
        for j, s in enumerate(u.get("subs") or [], start=1):
            if re.match(r"^\s*\d+\.\d+\s", s["title"]):
                continue
            s["title"] = f"{lead_number(u['title']) or 1}.{j} {s['title']}"
    return out, notes


def normalise_units(units: list, slug: str, source: str = "book") -> tuple[list, list[str]]:
    """The whole pipeline for one title's unit list.

    `source` is "book" (labels read out of the book, numbers unreliable) or
    "input" (the school's own spreadsheet - its numbering is the school's and is
    never rewritten, only its spelling is corrected).
    """
    notes: list[str] = []
    for u in units:
        title, n = normalise_title(u.get("title") or "", slug)
        notes += n
        u["title"] = title
        for s in u.get("subs") or []:
            s["title"], sn = normalise_title(s.get("title") or "", slug)
            notes += sn
    if source == "book":
        for u in units:
            if is_term(u["title"]):
                u["kind"] = "term"
            elif is_furniture(u["title"]):
                u["kind"] = "furniture"
                _, own = split_label(u["title"])
                if own:
                    u["title"] = own      # the index page has no unit number
        kept = [u for u in units if not u.get("kind")]
        kept, nest_notes = nest_repeats(kept)
        notes += nest_notes
        notes += renumber(kept)
        has_extra = any(u.get("kind") for u in units)
        if has_extra:
            order = []
            for u in units:
                if u.get("kind"):
                    order.append(u)
                elif kept:
                    order.append(kept.pop(0))
            units[:] = order
            extra = [u for u in units if u.get("kind")]
            n_term = sum(1 for u in extra if u["kind"] == "term")
            notes.append(f"{n_term} term divider(s) and "
                         f"{len(extra) - n_term} page-furniture row(s) kept as "
                         f"non-unit rows")
        else:
            units[:] = kept
    elif source == "input":
        for u in units:
            if is_furniture(u["title"]):
                u["kind"] = "furniture"
    return units, notes