# Standard A for Years 1 to 4, edition A-2.2

Locked by the teacher on 14 September 2026. Web version:
https://prime-books-pi.vercel.app/standard/years-1-4
Machine-readable tokens: `public/standards/years-1-4.json`

This is the working specification for every Prime Books title from Year 1 to Year 4. The full house
record for Years 1 to 12 stays in `public/standards/primary-standard.md`. Where this file and that one
disagree for Years 1 to 4, this file wins.

A-2.2 supersedes A-2.1: the teacher delegated the five open items and added the Welcome cast, the QR
policy, the References section, the safe-margin rule and the image-reference workflow.

## Precedence

1. The teacher's explicit decision.
2. This file and `years-1-4.json`.
3. The measured components of the Year 1 Art & Design reference, and the Unit 1 "Moving well" opener
   of Year 1 Physical Education as the unit page reference.
4. Legacy tools. The old PE engine is an implementation to adapt, never the authority.

Nothing teacher-placed is deleted, moved or shrunk to fit without explicit permission.

## Physical format

| Item | Value |
|---|---|
| Authoring page | US Letter 612 x 792 pt |
| Print trim | 216 x 279 mm (the same physical book within 0.4 mm), declared to BookVault |
| Media, with bleed | 222 x 285 mm, 3 mm bleed on all four edges |
| Safe area | 20 mm (56.7 pt) from the binding edge, 5 mm (14.2 pt) from the other three trim edges |
| Margins | mirrored: deeper inside, shallower outside |
| Folio | 24 pt circle, centre (550, 758) pt, no folio on covers |
| Unit band | full width y 0 to 47 pt, 1.8 pt unit-colour rule at y 46 to 47.8 |
| Footer rule | y 742 pt from the trim top |

Millimetres are the source of truth for print, points for authoring, converted at 72/25.4. Existing
612 x 792 pt masters are not migrated: the pack builder normalises to the print trim.

## Extent

- Legal counts: 11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 131 ... one less than a multiple of 12,
  counted after the front and back covers are stripped for the cover wrap.
- **Round up to the next legal count. Never round down. Never pad with a blank page.**
- Budget: front matter 7 pages, units at 8 to 10 pages each in Year 1 rising to 12 to 14 in Year 4,
  back matter 12 to 14 pages (glossary, references, sources, closing). Minimum viable extent 35.
- The last interior page stays clear in its lower area for BookVault's printed barcode.

## Page map

cover, imprint, contents, welcome and cast, how to use, preparation and safety, units, portfolio and
synthesis, illustrated glossary, **references**, sources and link list, closing reflection,
production reserve, back cover.

Within a unit: opener, get started, concept and model, your turn, extension, applied project,
reflection, word bank. A subject that needs no extension page simply has none.

Contents is physical page 3: a colour bar with one segment per unit, then one tinted card per unit
carrying the unit number, its start page, the unit name, a one-line strand summary, the topic rows and
a final `Unit n, How did it go?` row. Front and back matter are plain dot-leader rows, the glossary
and the references included. Page numbers are generated from the built PDF.

## The unit page header

The unit name appears **once** at the top of a unit page.

- On the opener: unit eyebrow, numeral, unit title, subtitle. No running head repeating the unit name
  above or below it.
- On a topic page: the running head in the 47 pt band carries `Unit 1, Moving Well`; the kicker
  carries `UNIT 1, TOPIC 1.1` with the topic title. The unit name is not printed a third time in the
  body.

Measured reason: on the Unit 1 opener of Year 1 Physical Education (page 12) the tracked eyebrow
starts at x 36.8 pt, which is 13 mm from the trim, 7 mm inside the 20 mm gutter, and it repeats what
the big unit title says directly beneath it. In a perfect-bound book that lettering disappears into
the spine. Every piece of furniture must sit inside the safe area.

**No blank pages.** A page that exists teaches, gives workspace or records sources. Padding to reach
a legal count is done with usable content, never with white space.

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

Only the Year 1 reading size is measured from the reference. The rest are adopted defaults, advisory
for authors and re-measured after the first Year 1 rebuild. Never shrink text to fit.

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
| 6 | ochre | #6B4A0C | #9A6A12 | #FBF0D8 |

Rungs 1 to 4 are measured from the reference. Rungs 5 and 6 were locked on 14 September 2026; the
ochre's mid tone is the house ochre so a white folio numeral keeps 4.7 to 1 contrast. The cover year
stripe (Year 1 #F1B300, Year 2 #7FC3E8, Year 3 #EF7522, Year 4 #60BB46) is a separate system.

## The welcome cast, one per subject

Every subject gets its **own** cast of four to six named characters, dressed for that subject, no
shared six across the year group. The welcome page introduces each with a portrait and one line, and
those same characters then carry the narrative scenes through the whole book.

Consistency is held by an **image reference**, not by memory: the approved character sheet goes to
`google/gemini-3-pro-image` through OpenRouter's chat endpoint as an image alongside the scene prompt.
Verified working: the same squirrel in the same mustard knit jumper came back in a new scene.
`openai/gpt-image-2.5-sunburst` ignores a reference image, so it is used for new plates only, always
at **quality medium**.

## QR codes

- Purpose: a teacher in front of the class shows the activity on the board in one scan.
- Placement: at the point of the activity, inside the topic page, beside the instruction it belongs
  to. Never collected on one page at the back.
- Frequency: roughly one per unit of 8 to 14 pages, more in practical subjects, none where there is
  nothing worth showing.
- Size: at least 74 x 74 pt on a white card, 4 pt inset, quiet zone respected.
- Caption: what it shows and how long it runs, in the child's reading size.
- Verification: every URL fetched, every code decoded back out of the rendered page before print.
- Print list: every target is also printed as a readable address in the back matter, so the book
  survives a dead link. The flipbook shows the same link as text.

## References

A references section follows the illustrated glossary: every information source the book used, books,
websites, datasets, and the credit and licence for every image that is not ours. One source per row,
laid out like the contents rows, each marked with the page or topic it supports. It is the printed
proof of where the facts came from.

## Illustration

Original Beatrix Potter direction: fine ink contours, transparent watercolour washes, warm muted
pigments, lightly textured cream paper. Palette cream #FBF6EC, sage #A8BF9B, terracotta #C97B5A,
butter #F0CE7A, dusky blue #8FA8C7, ink #3E3A35. Authentic evidence photographs and precise technical
diagrams are retained, with live-text labels and verified rights. No lettering inside generated art,
no stretched images, no repeated hero scene, 300 dpi target recorded as native pixels. Years 1 and 2
use large actions and generous space; Years 3 and 4 add process detail, comparison and labelled
evidence in the same medium.

## Print, BookVault perfect bound

- Trim 216 x 279 mm, media 222 x 285 mm, 3 mm bleed, safe area as above.
- Cover wrap 443 x 285 mm: back, spine and front on one sheet. Spine width from BookVault's sizing
  calculator for the stock ordered, rounded up to a whole millimetre; spine text only from 6 mm.
- Barcode zone 38 x 25 mm, 6.4 mm in from the back cover trim edge, 3.3 mm up. Mandatory.
- Smallest text 4 pt, thinnest line 0.25 pt, body and heading black 100 percent K only.
- Images 300 dpi, 150 dpi floor. Transparency flattened. Fonts embedded and subset.
- PDF/X-1a:2001 preferred, PDF/X-3:2002 accepted. No crop marks. Overprint off.
- The spine is a measured number: confirm with calipers on the first physical proof and correct the
  per-page figure if it is out by more than half a millimetre.

## How a title becomes standardised

1. The **standards bot** measures the published PDF against the locked tokens and writes
   `public/standards-report.json`, and the machine verdict appears on `/status` under **Checks**.
   Run it by hand with `.venv/bin/python tools/standards_bot.py`, or let the scheduled job do it.
2. **Clean** means no hard failure: page size, embedded fonts, folio on the interior pages, the
   contents bar matching the book's own unit count, a unit opener in a unit colour, every word inside
   the safe area, covers without a folio and a labelled back cover.
3. **Standardised** stays a human act. Click the column on `/status`, which records the sign-off
   server-side in `public/standardized.json`. The bot never writes that file: it cannot see whether
   teacher content was preserved, whether an image is licensed, whether a colour reads correctly on
   paper, whether a QR code scans off paper, or whether a proof copy was held.

## Decided on 14 September 2026

- Palette rungs 5 and 6 locked (sage, ochre with the house-ochre mid tone).
- No size migration: authoring stays US Letter, the pack builder normalises the print trim.
- Extent is a formula, not a fixed budget, and blank pages are forbidden.
- The spine figure is measured, not assumed.
- The year ladder, ruling and word counts are locked as authoring guidance and re-measured after the
  first Year 1 rebuild.

## Open item

The real spine width for the stock actually ordered, from BookVault's sizing calculator.