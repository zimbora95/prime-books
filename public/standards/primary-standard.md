# Standard A 2.0 · Prime Books · Years 1–6

> **How this document now relates to the house gate.** `tools/audit_standard.py`
> is the machine-checked authority for Years 1–6: it measures the published
> master and fails a book that breaks the house rules. Where this document and
> that tool differ, **the tool and the shipped book win** — specifically: the
> interior display heading is 24.5 pt (not 24), unit openers flood the unit's
> **deep** tone (not its mid tone), and the contents page is the six-segment
> mid-tone colour bar followed by one card per unit (not a dot-leader list).
> The unit colour order is fixed as: 1 light blue, 2 meadow green, 3 rose,
> 4 golden, 5 lilac, 6 clay. This document's type ladder, component behaviour
> and illustration direction remain the working specification on top of that.

## Authority and scope

**Design reference: Year 1 Art & Design, with Beatrix Potter-style illustration direction.**
Reference: https://prime-books-pi.vercel.app/book/y01-art-and-design

This is the current Primary publishing specification. It supersedes the older
Lexend/Noto Sans Primary rules, the Physical Education master designation, the
Years 1–4 scope and the mandatory six-unit contents design. Standard B (Years
7–12) is not changed. A reference is not a certificate: retain its successful
visual language, not its accidental defects.

The analysed PDF has 88 pages, all 612 × 792 pt. The repository master and the
PDF downloaded from the supplied live site matched SHA-256:
`7bf143ab68901df224cb5ba97059e5cdeac6c281e22c6ab69e12ed7d9d7dbb52`.

This revision updates the standard, not the reference PDF or other books.
The reference's illustration conversion remains to be produced and approved.
“Beatrix Potter” means the established ink-and-watercolour art direction, not
a claim that the images were made by Potter or permission to copy any edition.

**Precedence:** teacher's explicit decision → this specification and its tokens
→ measured reference components → legacy tools. Do not let a legacy renderer
silently override this specification. Preserve every teacher-placed sentence,
image and activity on its existing page unless a change is expressly authorised.

## 1. What makes this the standard

- A coherent, child-friendly teaching book, not a collection of worksheets.
- Fredoka display headings and Andika reading text; a clear title/lead/action hierarchy.
- One colour identity per unit, carried through opener, running band, labels and folios.
- Large, purposeful pictures that demonstrate the adjacent instruction.
- Predictable progression: discover → model → practise → extend → reflect → recall.
- Visible space for drawing, writing, ticking, discussing and making.
- Illustrated vocabulary, unit reflection and a subject-appropriate final portfolio/review.
- Quiet publisher-led covers and imprint; no examination-board endorsement claims.

Replicate the system, not the four studio-room names, sixteen Art topics or
88-page count. Unit count and content follow the target book's actual input.

## 2. Physical format and page furniture

Coordinates below are PDF points, top-left origin. They describe the visible
reference; do not confuse text bounding-box tops with text baselines.

| Component | Measured reference / replication rule |
|---|---|
| Trim | US Letter portrait, 612 × 792 pt throughout |
| Extent | Even total including covers; length determined by content |
| Standard content box | x 50.25–561.75; y 66–734.25; width 511.5 |
| Unit running band | Full width, y 0–47; unit tint |
| Band rule | y 46–47.8; unit mid colour, not universal ochre |
| Header left | x 50; Fredoka SemiBold 10.5 pt, baseline 26.23 |
| Header right | Right-aligned at x 562; Andika 10 pt, baseline 29.21 |
| Kicker | x 50.25; Fredoka SemiBold 9.5 pt, baseline 83.25 |
| Page title | x 50.25; Fredoka SemiBold 24 pt, baseline 120.75 |
| Opening reading line | x 50.25; Andika 16 pt, baseline 152.25; next line 173.25 |
| Footer rule | x 50–562, y 742, 0.6 pt |
| Main folio | Circle centre (550,758), diameter 24 pt; Fredoka 11 pt |
| Folio contrast | Unit mid + white numeral on light pages; white + unit numeral on openers |
| Covers | No folios; genuine logo composited, never generated |

The reference's imprint uses a smaller 21 pt folio centred (550,748); this is
an explicit imprint variant, not permission for random folio positions.
Covers, imprint, contents, welcome and back matter use their own page-type
layouts; **do not impose the unit header band on every page**. The reference's
contents and glossary do not have that band. Content never enters the footer
zone. Full-bleed artwork and an opener's background are deliberate exceptions
to content margins, not permission for text overflow.

## 3. Typography and age progression

**Primary core: Fredoka SemiBold + Andika Regular/Bold, Years 1–6.** Poppins is
reserved for covers and publisher/imprint information. Caveat may appear as a
short optional annotation, never an essential instruction. Gelasio is optional
for an actual quotation, not a second body face. No Helvetica, Verdana, Arial,
Type3, missing glyphs or accidental fallback in newly composed book content.
Authentic third-party document facsimiles are reviewed and recorded separately.

The reference's principal pupil reading text is **16 pt Andika**, not the
11.5 pt stated by the old PE-based standard. It also contains smaller captions,
word-card definitions and supplementary text. Do not use the smallest size
found in a PDF as the standard for every paragraph.

| Year | Core pupil reading size | Default leading | Status |
|---|---|---|---|
| 1 | 16 pt | 21 pt | Measured from reference |
| 2 | 16 pt | 21 pt | Adopted series default |
| 3 | 15 pt | 20 pt | Adopted series default |
| 4 | 14.5 pt | 19.5 pt | Adopted series default |
| 5 | 14 pt | 19 pt | Adopted series default |
| 6 | 13.5 pt | 18.5 pt | Adopted series default |

Year 2–6 sizes are an explicit extrapolation, not measurements from nonexistent
reference books. Keep larger established sizes on an existing teacher-edited
page. Never auto-shrink text, tighten tracking or distort letterforms to fit.
Measure and wrap first; propose a continuation or revised layout if content
cannot fit, obtaining permission before moving or deleting content.

- Page titles: 24 pt. Long titles wrap; do not silently scale them down.
- Unit titles: approximately 44 pt in the reference, subtitle 17 pt, topic pills 13 pt.
- Panel labels: generally Fredoka 12–15 pt; subordinate labels 9.5–11 pt.
- Essential short pupil prompts: aim for the year's reading size; review any smaller text.
- Secondary captions: reference approximately 11 pt, with some 11.5 pt variants.
- Glossary headwords: approximately 14 pt; reference definitions approximately 11 pt.
  These are reference observations, not blanket accessibility approval. Enlarge
  essential definitions where children are expected to read independently.
- Publisher/legal copy can be smaller because it is adult-facing, not a pupil task.
- Left aligned, ragged right. No text over busy imagery. No stranded headings.

## 4. Colour: page identity is separate from illustration pigment

Retain the reference's four measured unit palettes as the starter set. The
Beatrix Potter change applies to illustration treatment; it is not permission
to arbitrarily recolour all page furniture. Additional unit colours must be
named in the target book's theme map and contrast-tested before use.

| Starter theme | Deep (headings) | Mid (opener/rule/badge) | Tint (band) |
|---|---|---|---|
| Violet · reference Unit 1 | #4A3173 | #6B4BA1 | #EFE6FA |
| Rose · reference Unit 2 | #96204A | #D6336C | #FCE4EC |
| Terracotta · reference Unit 3 | #8C3A12 | #C4561F | #FBE7D8 |
| Blue · reference Unit 4 | #0B3C85 | #1256B8 | #DEEAFB |

Common text: #2E2740; muted: #6B6280; paper: white; warm panel/border accents
from the reference, with exact per-component geometry in the measurement report.
Cover stripe Year 1: #F1B300. Retain the established series ladder for later
covers: Year 2 #7FC3E8, Year 3 #EF7522, Year 4 #60BB46, Year 5 #C32480,
Year 6 #835FC1. Year stripe and unit palette are different concepts.

Illustrations use cream #FBF6EC, sage #A8BF9B, terracotta #C97B5A,
butter #F0CE7A, dusky blue #8FA8C7 and ink #3E3A35. Accurate colour samples,
flags, maps and scientific information must retain their correct colours.

## 5. Cover and imprint components

**Front, physical page 1:** 34 pt full-height year stripe; actual logo at
(85,42)–(149,106); subject Poppins ExtraBold 33 pt at x85, baseline140;
Year N Poppins SemiBold17 at baseline203.95; Student Manual Andika11 at
baseline228.03. Measured art slot (34,315)–(612,792). Keep the typography
clear of the artwork. Use a unique subject-specific watercolour scene;
aspect-fit without stretching and preserve heads, hands and teaching objects.
Do not invent a programme line that is absent from the approved reference.

**Imprint, physical page 2:** publisher identity, subject, Year N · Student Book,
book-specific tagline, INSIDE THIS BOOK summary, structured IMPRINT rows,
independence statement, age/stage and website. Measured main text bounds
x56–556. Rows: Edition, Publisher, Rights, Credits, Trademarks, Safety,
Teachers. Update factual metadata only; preserve approved legal language.
Do not carry Art's “no printed answers” statement into a subject that needs an
answer key. Add truthful AI-illustration disclosure when generated work is used;
never claim generated artwork is a historical Potter original or that AI wrote
teacher-authored text. Verify credits, actual imprint, age and edition.

**Back, physical page 88:** PRIME SCHOOL PRESS, subject, metadata, short hook and
blurb, warm rounded INSIDE THIS BOOK card, publisher/age/site footer and a
separate quiet art treatment. Title x85 baseline128, Poppins ExtraBold33.
Reference feature card is (71,364.32)–(470,512.32). Copy the hierarchy, not
Art-specific copy or line lengths. No invented ISBN, retail price, endorsement
or decorative barcode. A print barcode is added only when required and supplied.

## 6. Book architecture and component library

Default new-book sequence follows the reference:
**cover → imprint → contents → welcome → how to use → getting ready/safety →
units → synthesis/portfolio → year review where relevant → illustrated glossary
→ sources and image credits → closing reflection → back cover.**

A previously approved book order is not silently rearranged. Contents on page 3
and welcome on page 4 are the actual reference order; the old fixed welcome-on-3
rule is not the new general standard. Answers, index and watch/listen resources
are subject-dependent; do not force “Watch and learn” into every final three
pages or add irrelevant sections to mimic another subject.

| Component | Reference physical pages | Reusable contract |
|---|---|---|
| Contents | 3 | Visual overview; coloured unit groups; indented topics; right-aligned verified targets. Four units here, not a fixed six-segment bar. |
| Welcome | 4 | Meaningful hero image, book invitation, learning context; original prose retained. |
| How to use | 5 | Label + icon + meaning; establish conventions once. |
| Preparation | 6–7 | Materials, practical safety and picture vocabulary appropriate to subject. |
| Unit opener | 8,25,41,56 | Coloured full-page field, unit number, title, subtitle, wrapping topic pills, large framed scene. |
| Get started | 9–10,26–27 | Prior-knowledge question, goals, warm-up and achievable action. |
| Concept + model | 11,13,28,30,44,61 | Title, readable explanation, accurate illustration/diagram, linked caption, modelled step. |
| Your turn | 12,20,29,60 | Prompt stays with workspace; drawing/handwriting/swatches sized to the task. |
| Extension | 17,37,50 | Distinguish Go a bit further from Big challenge; optional, not punitive. |
| Applied project | 22,38,52,68 | Visible end goal and numbered method; adapt to the subject. |
| Reflection | 23,39,53,69 | I can statements, rating choices and evidence; labels as well as colour. |
| Unit word bank | 24,40,54,70 | Compact visual recall cards; not the same density as the final dictionary. |
| Portfolio/synthesis | 71–74 | Demonstrate and reflect on learning, not an Art exhibition in every subject. |
| Illustrated glossary | 77–84 | Two columns × three cards; image, headword, short definition; optional handwriting. |
| Sources / credits | 85–86 | Traceable facts and image provenance; real URLs/licences, hanging indents. |
| Closing reflection | 87 | Short meaningful close; art and/or photograph with verified credit. |

Panels retain their distinct meanings: pale topic tint for support, warm amber
for facts, deep unit fill for challenge, light framed/dashed areas for pupil
response. Do not flatten all boxes into a single style. Tables use a readable
header and alternation within the selected theme; retain teacher-approved
existing table styling. Padding and row height are measured from content, not
made smaller to force a table onto a page. Use consistent label/icon positions
and approximately 12–16 pt inner padding as a new-component default.

Whitespace is valid when it is usable drawing/writing space or an intentional
pause. A page with one stranded sentence is not automatically a good worksheet.
Mark response areas clearly and keep the task instructions with them. Never
fill teacher-reserved space with decoration to improve an automated density score.

## 7. Beatrix Potter illustration production contract

### Replace the illustrative voice, not the evidence

- Narrative scenes: original woodland animals in believable clothing, gentle
  ink contours, transparent watercolour, paper texture, natural proportion and
  restrained expression. Same cast and clothing within a book; distinct actions.
- Isolated tools/nature/vocabulary: precise, recognisable watercolour studies.
  Do not add an animal if it obscures the object or distracts from the word.
- Procedural pictures: show the exact safe hand/paw position, tool, orientation
  and material required by the instruction. Prioritise clarity over charm.
- Technical diagrams, maths models, letterforms and colour wheels: retain
  precision; draw labels as live text. Watercolour is not a substitute for truth.
- Photographs of authentic artworks, places, specimens or primary evidence:
  retain where educationally necessary with verified rights and captions.
  Never substitute an invented painting for a named real artwork.
- Artwork is unique per scene. Reuse of a tiny glossary symbol for deliberate
  recall is allowed only when recorded; no repeated hero image as filler.

### Brief required for every image

Record `id`, target physical page, slot rectangle, subject, learning objective,
scene/action, cast/wardrobe, required visible objects, prohibited errors, palette,
source/type, rights/credit, native dimensions, fit/crop decision and approval.
No global xref replacement until shared placements are understood.

Prompt scaffold:
> Original Beatrix Potter-style ink-and-watercolour illustration for a Year
> {year} {subject} textbook. Show {precise action} to teach {learning objective}.
> {characters and consistent clothing}. Gentle fine ink outlines, transparent
> watercolour washes, warm muted pigments and lightly textured cream paper.
> {composition and required clear objects}. No lettering, labels, logo, border,
> signature or watermark; no plastic 3D finish, vector-flat fills or hard shadows.
> Leave {specific text-safe space}; preserve accurate tool use and anatomy.

Cover/scene/picture-card briefs must be different. Generate one pilot of each
kind, inspect it at full size, then approve the batch. Do not claim 300 dpi from
an upscaled file. Record native pixels and effective dpi at placed size. Target
300 dpi for print raster artwork; anything below the printer's agreed threshold
requires explicit review. Technical text/line diagrams should remain vector.
Actual historical Potter art needs an asset-specific provenance and rights check,
including the source edition and distribution territory; age alone is not a licence.

### Age progression without a different collection

Years 1–2: large actions, short sequences, direct naming, generous response areas.
Years 3–4: more process detail, comparisons, labelled evidence, less decorative cast.
Years 5–6: more analytical diagrams, purposeful still lifes and independent enquiry.
Keep the same illustration medium and book architecture; do not turn Year 6 into
a nursery storybook or switch it to the Secondary geometric pack.

## 8. Reference defects excluded from the standard

The reference is visually authoritative, not technically perfect.

- Contents drift: Unit 3 listed at42 but opens41; Unit 4 listed57 but opens56;
  portfolio listed74 but begins73; word book listed78 but begins77; sources
  listed86 but begin85. Topic references also need a complete truth-check.
- Extracted content includes Helvetica, Verdana and one Arial-BoldMT span.
  These are legacy substitutions/figure labels, not approved series fonts.
- Sparse continuations visible at31,35,45,55,64,67,76 need teacher review.
  Some contain genuine work areas; do not automatically delete, fill or merge them.
- The page47 Your turn label and page48 response need a full-size continuity check.
- Unit3 and Unit4 opener folios have later violet badge patches instead of the
  original inverse unit treatment. Preserve the intended component, not the patch.
- Current narrative illustration does not yet meet the requested Potter direction.
- All physical interior folio values currently match their page numbers. Do not
  report a numbering failure just because contents references are stale.

## 9. Replication workflow and acceptance gates

1. Inventory target PDF, markdown, input, page count, book-specific curriculum,
   images/credits, and teacher-approved exceptions. Save a durable restore point.
2. Create a page-by-page adaptation map: existing physical page, component,
   preserved text, theme, artwork brief, response area and planned change. No
   silent content movement, deletion or font shrinkage.
3. Approve a representative pilot: cover, imprint, contents, opener, teaching
   page, pupil task, review, glossary and back cover. Do not rebuild the corpus blind.
4. Typeset through measured components with explicit year/font/theme settings.
   `tools/pb_engine.py` is a PE-derived implementation, **not yet a compliant
   universal renderer**: its 11.5 pt body defaults, 24.5 pt heading and ochre theme
   must not be accepted as the new standard. Do not run its subject scripts on
   another book or replace a current master with an old rebuild.
5. Preflight with `.venv/bin/python tools/audit_standard.py <slug> --json <report>`.
   Current automated checks: trim, parity, folio values and extracted font families.
   Exit0 means these checks passed, **not** that the book is approved.
6. Manually verify every page: legibility, no clipping/collision/tofu, actual
   response space, tables, chapter continuity, image meaning/rights/uniqueness,
   realistic safe technique, contrast and no essential colour-only coding.
7. Rebuild and truth-check contents, index and cross-references against physical
   destinations. Test actual QR codes, link targets and access suitability.
8. Compare original and resulting text page by page. Explain any authorised
   additions or relocations. Blank-response areas are not missing content.
9. Sync changed PDF companions, cover thumbnails, catalogue/manifest extent and
   wrap assets as applicable. Do not edit a markdown companion alone and call
   the book updated. Preserve working-tree changes from other sessions.
10. Reopen the saved PDF, render and review spreads/full-size samples, print-proof
    representative pages and compare a downloaded served asset's digest with disk.
    Publish/commit only within the teacher-authorised scope.

**Release checklist:** content preserved; age reading size approved; navigation
correct; illustration pilots approved; every image credited or recorded as original;
print resolution reviewed; all pages visually inspected; automated errors zero;
manual checks signed; master/markdown/catalogue synchronised; served digest verified.

## Supporting artefacts

- `/standards/primary-standard.json`: machine-readable tokens and page-type map.
- `tools/measure_primary_reference.py`: read-only whole-book measurement and renders.
- `work/primary-standard-reference/measurement.json`: all88 pages' spans, drawings,
  image placements and link data; contact sheets cover every page.
- `/standards/primary-reference-audit.json`: executable preflight of the reference.
- `/standard`: human-readable site summary; this document is the detailed authority.
