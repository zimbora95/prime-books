# Year 1 Physical Education — book specification

Slug `y01-physical-education` · Year 1 · Cambridge Early Years · Prime School Press

Re-issued 2026-09-14 on **Standard A 2.0**: the house layout (one colour per
unit, card contents page, unit-deep openers) with the Standard A 2.0 type ladder,
scattered unit-attributed QR codes and a picture glossary.

> The machine-checked authority for Years 1–6 is the constants in
> `tools/audit_standard.py` (`audit_standard.py y01-physical-education`). This
> page records what this particular book does within that standard.

## The rebuild in one line

The interior was rebuilt from `tools/y01pe_book_content.py` by
`tools/y01pe_a2_build.py`; cover, imprint and the Welcome page (1–3) and the back
cover are spliced from the master unchanged.

| | |
|---|---|
| Total pages | 98 (even, so the flipbook never shows the back cover alone) |
| Interior | 94 pages: front matter, six units, back matter, teacher index |
| Numbering | Welcome page 3, contents page 4, folios 4–96, back cover 98 |
| Reading text | 16 pt on 21 pt leading (Standard A 2.0 ladder, `pb_engine.A2`) |
| Page display heading | 24.5 pt Fredoka (house size, measured and gated) |
| Panels, step lists, kit cards | 15 pt on 18.6 pt |
| Captions, table cells | 11.5 pt / 12.5 pt |

## Theme map

Outside pages (cover, imprint, Welcome, back matter) keep the house ochre
`#9a6a12` on `#f6eedc`. Each unit carries one colour, used for its band, rule,
kicker, headings, badges, contents card and opener flood:

| Unit | Name | Deep (opener flood) | Mid (band rule, accents) | Tint (band, panels) |
|------|------|---------------------|--------------------------|---------------------|
| 1 | Moving Well — light blue | `#1e4e6b` | `#3c7ca6` | `#eaf3f9` |
| 2 | Understanding Movement — meadow green | `#2c4127` | `#4e6b45` | `#edf3e6` |
| 3 | Moving Creatively — rose | `#6e2a25` | `#b4564e` | `#fbedec` |
| 4 | Taking Part — golden | `#6b4a0c` | `#c08a1e` | `#fdf3dc` |
| 5 | Taking Responsibility — lilac | `#442f63` | `#7a5fa0` | `#f4eff9` |
| 6 | Healthy Bodies — clay | `#6b3410` | `#b4622a` | `#faede2` |

The contents page opens with the six-segment colour bar in the unit mid tones and
then gives each unit its own card, keyed to the same colours, so the contents
reads as the colour code of the book.

## Scan and show — the QR policy

Codes are attributed to the unit that carries them and scattered, never printed
on every page: 20 codes across the unit topic pages (about one page in five,
irregular within each unit), plus the welcome and look-back pages, the teacher's
twelve-code link grid, and a "Scan and show" teacher index page listing every
address in the book with a QR for the routine used most.

* every address is a named organisation (BBC Teach, NHS, GoNoodle, Cosmic Kids,
  Youth Sport Trust, British Heart Foundation, Woodland Trust, RSPB) and was
  link-checked with an HTTP HEAD before the build;
* every QR tile is drawn in its unit's deep colour, never plain black;
* captions carry an adult-facing "for families"/"teacher reading" note;
* the gate decodes every rendered code back to the address printed beside it.

## Picture glossary

Fourteen words, fourteen transparent watercolour vignettes in the house style
(`tools/y01pe_glossary_images.py`, `openai/gpt-image-2.5-sunburst`, medium,
transparent PNG), laid out as picture cards rather than a plain table — the
illustrated glossary Standard A 2.0 asks for.

## Gates run before publishing

`tools/y01pe_a2_verify.py` (read-only; replays the builder's own page plan):

1. every contents card points at a page that really carries that title;
2. every interior page carries its folio, in the folio position;
3. no page runs past the type area, outside the margins, or sits empty;
4. every interior page is set in its unit's own colour, openers flooded in the
   unit's deep tone;
5. every QR code decodes back to its printed address;
6. reading text is at least 16 pt;
7. the page count is even.

Plus, on the published file: `tools/audit_standard.py y01-physical-education`,
`tools/check_books.py`, `tools/md_sync.py --check` and `npm run build`.
