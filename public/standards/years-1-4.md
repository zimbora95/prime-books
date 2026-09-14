# Standard A for Years 1 to 4, edition A-2.1

Locked 14 September 2026. Web version: https://prime-books-pi.vercel.app/standard/years-1-4
Machine-readable tokens: `public/standards/years-1-4.json`

This is the short working specification for every Prime Books title from Year 1 to Year 4. The full
house record for Years 1 to 12 stays in `public/standards/primary-standard.md`. Where this file and
that one disagree for Years 1 to 4, this file wins.

## Precedence

1. The teacher's explicit decision.
2. This file and `years-1-4.json`.
3. The measured components of the Year 1 Art & Design reference.
4. Legacy tools. The old PE engine is an implementation to adapt, never the authority.

Nothing teacher-placed is deleted, moved or shrunk to fit without explicit permission.

## Physical format

| Item | Value |
|---|---|
| Trim | 216 x 279 mm (US Letter portrait) |
| Media, with bleed | 222 x 285 mm, 3 mm bleed on all four edges |
| Margins | mirrored: 20 mm inside gutter, 15 mm outside, 23.25 mm top, 20 mm bottom |
| Trim safety | 5 mm clear of the other three trim edges |
| Folio | 24 pt circle, centre (550, 758) pt, no folio on covers |
| Unit band | full width y 0 to 47 pt, 1.8 pt unit-colour rule at y 46 to 47.8 |
| Footer rule | y 742 pt from the trim top |

Millimetres are the source of truth; points are derived at 72/25.4.

## Extent

- Interior page count is one less than a multiple of 12: 11, 23, 35, 47, 59, 71, 83, 95, 107.
- This is counted after the front and back covers are stripped for the cover wrap.
- Year targets: Year 1 59, Year 2 71, Year 3 83, Year 4 95.
- The last interior page stays clear in its lower area for BookVault's printed barcode.

## Typography

Fredoka SemiBold for display, Andika for reading, Poppins for covers and publisher matter, Caveat only
for a short annotation, Gelasio only for a quotation. No Helvetica, Verdana, Arial, Type3 or accidental
fallback in new content.

| Year | Reading text | Leading | Writing lines | Instruction | Words per page |
|---|---|---|---|---|---|
| 1 | 16 pt | 21 pt | 4-line guides, 24 mm | 3 to 7 words | 80 |
| 2 | 16 pt | 21 pt | 3-line guides, 18 mm | 5 to 9 words | 110 |
| 3 | 15 pt | 20 pt | single line and mid guide, 12 mm | 8 to 12 words | 140 |
| 4 | 14.5 pt | 19.5 pt | single line, 9 mm | 10 to 14 words | 170 |

Only the Year 1 reading size is measured from the reference. The rest are adopted defaults. Never
shrink text to fit and never reduce an established teacher-approved size.

Page title 24 pt. Unit title 44 pt. Unit subtitle 17 pt. Topic pill 13 pt. Kicker 9.5 pt. Running head
Fredoka 10.5 / Andika 10. Folio numeral Fredoka 11.

## Unit colour

Unit n takes rung n in every book of the series.

| Unit | Name | Deep | Mid | Tint |
|---|---|---|---|---|
| 1 | violet | #4A3173 | #6B4BA1 | #EFE6FA |
| 2 | rose | #96204A | #D6336C | #FCE4EC |
| 3 | terracotta | #8C3A12 | #C4561F | #FBE7D8 |
| 4 | blue | #0B3C85 | #1256B8 | #DEEAFB |
| 5 | sage | #2F5233 | #4E7C52 | #E8F0E3 |
| 6 | ochre | #6B4A0C | #B5832A | #FBF0D8 |

Rungs 1 to 4 are measured from the reference. Rungs 5 and 6 are proposals awaiting the teacher's eye.
Deep for headings and the opener flood, mid for the rule, badge and kicker, tint for the band and
support panels. The gold accent stays gold in every unit. The cover year stripe (Year 1 #F1B300,
Year 2 #7FC3E8, Year 3 #EF7522, Year 4 #60BB46) is a separate system.

## Page map

cover, imprint, contents, welcome and cast, how to use, preparation and safety, units, portfolio and
synthesis, illustrated glossary, sources and credits, closing reflection, production reserve, back cover.

Within a unit: opener, get started, concept and model, your turn, extension, applied project,
reflection, word bank. A subject that needs no extension page simply has none; it never invents a
different shape.

Contents is physical page 3: a colour bar with one segment per unit, then one tinted card per unit
carrying the unit number, its start page, the unit name, a one-line strand summary, the topic rows and
a final `Unit n, How did it go?` row. Front and back matter are plain dot-leader rows. Page numbers are
generated from the built PDF.

## Illustration

Original Beatrix Potter direction: fine ink contours, transparent watercolour washes, warm muted
pigments, lightly textured cream paper. Illustration palette cream #FBF6EC, sage #A8BF9B, terracotta
#C97B5A, butter #F0CE7A, dusky blue #8FA8C7, ink #3E3A35. Same cast and clothing throughout a book.
Authentic evidence photographs and precise technical diagrams are retained, with live-text labels and
verified rights. No lettering inside generated art, no stretched images, no repeated hero scene,
300 dpi target recorded as native pixels. Years 1 and 2 use large actions and generous space; Years 3
and 4 add process detail, comparison and labelled evidence in the same medium.

## Print, BookVault perfect bound

- Trim 216 x 279 mm, media 222 x 285 mm, 3 mm bleed.
- Cover wrap 443 x 285 mm: back cover, spine, front cover on one sheet. Spine width from BookVault's
  sizing calculator for the stock ordered, rounded up to a whole millimetre; spine text only from 6 mm.
- Barcode zone 38 x 25 mm, 6.4 mm in from the back cover trim edge, 3.3 mm up. Mandatory.
- Smallest text 4 pt, thinnest line 0.25 pt, body and heading black 100 percent K only.
- Images 300 dpi, 150 dpi absolute floor. Transparency flattened. Fonts embedded and subset.
- PDF/X-1a:2001 preferred, PDF/X-3:2002 accepted. No crop or bleed marks. Overprint off.

## Known work before this standard can be enforced

- `tools/audit_standard.py` fails any odd page count, while BookVault requires one. It also checks a
  612 x 792 pt page, while the trim is 216 x 279 mm. Both rules must change.
- The gate checks only trim, parity, folio values and font families. Band, rule colour, reading size,
  contents segment count, content overflow and missing glyphs are unchecked.
- The contents component is written for six units. It must become one segment and one card per unit.
- `tools/pb_engine.py` is PE-derived and is not a compliant renderer. Its body sizes, heading size and
  ochre default must not become the standard.

## Open items

1. Palette rungs 5 and 6.
2. The real spine width for the stock ordered.
3. Whether older 612 x 792 pt masters migrate to 216 x 279 mm.
4. The page budget per year.
5. The handwriting ruling and words-per-page ladder, once a Year 1 book is read against a Year 4 book.
