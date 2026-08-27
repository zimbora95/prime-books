# 02 - Design System

One shared layout skeleton, two art directions. A book is 100% in one pack,
decided by YEAR, never by subject. Never mix packs inside a book.

## Which pack a year uses

| Pack | Style | Years |
|---|---|---|
| Pack A "Beatrix Potter" | soft watercolour and ink | Year 1-6 (Lower and Upper Primary) |
| Pack B "Geometrical" | flat vector, bold shapes | Year 7+ (Secondary and Advanced Levels) |

The boundary sits at Year 6/7. Everything below it is warm and storybook;
everything above it is grown-up and editorial.

## The shared layout skeleton (identical in both packs)

Every book renders the same six surfaces, in the same order:

1. Front cover: logo top-left, subject title, "Year N", Cambridge band,
   "Student Manual", a short accent rule, then the cover art, then a
   full-height spine bar.
2. Back cover: a single panel of the same palette as the front, no title block.
3. Imprint / copyright page: fixed boilerplate, copied verbatim, never
   rewritten.
4. Unit opener: a full-bleed opener image in the pack's voice plus the unit
   title and learning outcomes.
5. Running footer: page number, book title, Prime School mark.
6. Call-outs: feature boxes (Get started, Scenario, Did you know, Challenge
   yourself) drawn in the pack's palette and shapes.

Only the art below the accent rule changes between packs; the title block is
rigid. Two families, one layout.

## Pack A: Beatrix Potter (Year 1-6)

- Medium: soft watercolour washes over gentle hand-drawn ink outlines. No hard
  vector edges, no flat fills, no hard shadows.
- Subject matter: friendly woodland animals wearing human clothing (painters'
  smocks, school blazers, aprons) using human tools. The Prime School uniform
  spec is mandatory on any child that appears.
- Palette (warm, muted, never saturated):
  - cream `#FBF6EC`
  - sage `#A8BF9B`
  - terracotta `#C97B5A`
  - butter `#F0CE7A`
  - dusky blue `#8FA8C7`
  - ink `#3E3A35`
- Typography: a rounded friendly display face, plus a legible rounded sans for
  body.
- Image prompt (use verbatim, substituting the two placeholders):

  "Soft children's storybook illustration in a Beatrix Potter style: {subject},
  {action}. Gentle hand-drawn ink outlines, loose watercolour washes, warm muted
  palette, rounded friendly shapes, paper texture, no text, no hard shadows,
  cozy and calm."

## Pack B: Geometrical (Year 7+)

- Medium: flat vector shapes with crisp edges and a subtle grain. No gradients,
  no hand-drawn line work, no cartoon mascots.
- Subject matter: a central bold geometric form (circle, square, triangle, arc)
  carrying subject-specific objects: a circuit board for Computing, a compass
  and set square for Mathematics, a microscope and DNA model for Science.
- Palette (crisp, academic):
  - off-white `#F7F8FA`
  - charcoal `#1F2933`
  - teal `#1F6F6B`
  - orange `#D2703C`
  - slate `#4B5D7A`
- Typography: a strong geometric sans display face, plus a clean neutral sans
  for body.
- Image prompt (use verbatim, substituting the two placeholders):

  "Minimal flat vector illustration for a secondary-school textbook: {subject},
  {concept}. Bold geometric shapes, crisp edges, deep teal / burnt orange /
  slate / charcoal on off-white, subtle grain, no gradients, no text, no cartoon
  mascots, clean and academic."

## Rules that apply to every book

1. A book is 100% in one pack. Covers, unit openers, call-outs and every
   illustration use the same pack.
2. No text inside the cover art: the title block names the book.
3. Real photographs beat AI imagery wherever a photograph is possible. Composite
   the real Prime School logo, never let an image model draw it.
4. Vary composition within AND across books. Two Mathematics books must not
   share an object layout. "Same boring design logic" is a rejection trigger.
5. Uniform is mandatory on any cover child.
6. British English throughout (pupils, programme, -ise, colour, centre, grey,
   practise as the verb). No em-dashes anywhere; en-dash only for ranges.
7. The imprint/copyright boilerplate is fixed: copy verbatim, do not rewrite.

## Image generation

The working route is fal.ai's gpt-image-2, at roughly 768 x 1024 maximum, so
full-bleed art lands around 93 dpi at 210 mm. Record that honestly rather than
claiming 300 dpi. Catalogue cover art at 720 x 926 is within the model's native
resolution. Pilot one asset per kind and inspect it before spending the batch;
verify the files on disk against the manifest afterwards.

This file supersedes `docs/DESIGN-STANDARD.md`. The old boundary there (Year 1-4
storybook, Year 5+ geometric) is retired: the boundary is now Year 1-6 Pack A,
Year 7+ Pack B.
