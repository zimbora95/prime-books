# Year 1 Physical Education — book specification (Standard A 2.0)

Slug `y01-physical-education` · Year 1 · Cambridge Early Years · Prime School Press
Rebuilt 2026-09-14 on Standard A 2.0 (the Year 1 Art & Design layout authority).

## Theme map

Six units, six named themes. The outside of the book (cover, imprint, front
matter, back matter) keeps the house ochre `#9a6a12` on `#f6eedc`, so every
Prime Book opens the same way; each unit inside carries its own colour.

| Unit | Name | Deep | Mid (band rule, opener flood) | Tint (band, panels) |
|------|------|------|-------------------------------|---------------------|
| 1 | Meadow green | `#2c4127` | `#4e6b45` | `#edf3e6` |
| 2 | Watching blue | `#1e4e6b` | `#3c7ca6` | `#eaf3f9` |
| 3 | Dancing rose | `#6e2a25` | `#b4564e` | `#fbedec` |
| 4 | Team amber | `#6b4a0c` | `#c08a1e` | `#fdf3dc` |
| 5 | Responsibility violet | `#442f63` | `#7a5fa0` | `#f4eff9` |
| 6 | Healthy terracotta | `#6b3410` | `#b4622a` | `#faede2` |

The contents page is keyed to this map: each unit heading takes the unit's deep
colour with a colour dot, and every topic's page number is set in the unit's mid
colour. Opener pages flood in the unit's mid tone; title, narrative and captions
switch between white and deep ink by measured contrast (WCAG `readable_on`), so
the light mids (Team amber) stay readable without special-casing.

## Type (Standard A 2.0 profile, `pb_engine.A2`)

| Element | Size / leading |
|---------|----------------|
| Page title | 24 pt Fredoka (fit to width, floor 17) |
| Reading text (lead, paragraphs) | 16 pt / 21 pt Andika |
| Panels, step lists, ticks, kit cards | 15 pt / 18.6 pt |
| Small cards, QR blurbs | 13–13.5 pt |
| Table cells | 12.5 pt / 14 pt |
| Picture captions, folio label | 11.5 pt |

Measured on the finished file: the most-read size is 16 pt; no page is below the
year's reading size for its body text.

## Scan and show — the QR policy

Educational links are attributed to the unit that carries them, and scattered,
never printed on every page: 20 codes across 95 interior pages (about one page
in five, irregular within each unit), plus the welcome and look-back pages and
the teacher's twelve-code link grid at the back.

* every address is a named organisation (BBC Teach, NHS, GoNoodle, Cosmic Kids,
  Youth Sport Trust, British Heart Foundation, Woodland Trust, RSPB) and was
  link-checked with an HTTP HEAD before the build;
* every QR tile is drawn in its unit's deep colour, not plain black;
* an adult-facing "for families"/"teacher reading" note rides on the caption;
* the gate decodes every rendered code back to the address printed beside it.

## Picture glossary

Fourteen words, fourteen transparent watercolour vignettes generated in the
house style (`tools/y01pe_glossary_images.py`, `openai/gpt-image-2.5-sunburst`,
medium, PNG with transparency), laid out as picture cards rather than a plain
table — the illustrated glossary Standard A 2.0 asks for.

## Gates run before publishing

`tools/y01pe_a2_verify.py` (read-only, replays the builder's own page plan):

1. all 57 contents entries point at a page that really carries that title;
2. every interior page has its folio in the folio position;
3. no page overflows the type area, breaks the margins or sits empty;
4. each unit has exactly one band+rule colour and no two units share one;
5. every QR code decodes back to its printed address;
6. reading text is at least 16 pt.

Plus, on the published file: `tools/check_books.py`, `tools/report_violations.py`,
`tools/audit_standard.py y01-physical-education`, `tools/md_sync.py --check` and
`npm run build`.
