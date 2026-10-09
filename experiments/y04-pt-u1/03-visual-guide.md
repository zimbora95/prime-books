# 03 — Visual guide

## Big visual idea: "Documents from a real street"
The unit is a walk down Rua do Limoeiro. Every text type is shown **as the physical object**: a letter on lined paper, an invitation card with a deckled edge, a folded newspaper, a comic strip. Children handle "real" documents on the page, then annotate them. A dotted **route line** (the postman's path) links the stops and runs through the map (p. 4) and the stop headers.

## Typography (all SIL Open Font License; embedded in the PDF)
| Role | Font | Size |
|---|---|---|
| Display / headings | **Fraunces** (variable, SOFT 100, WONK 1): warm, bookish, slightly wobbly | 30–64 pt |
| Body / instructions | **Andika**: SIL typeface designed for beginning readers, with single-storey a and g, clear I/l/1 | 15 pt, leading 1.45 |
| Handwritten documents | **Patrick Hand**: used only for letters and notes written by characters | 17–19 pt |

Type scale (5 levels): 64 / 34 / 22 / 15 / 12 pt.
Every font covers ã õ ç á à â é ê í ó ô ú « » — (verified with fontTools).

## Colour
| Name | Hex | Use |
|---|---|---|
| Papel (paper) | #FCF4E3 | page ground (matches the illustration paper) |
| Tinta (ink) | #1F2A44 | all body text; contrast on paper 13.9:1 |
| Correio (red) | #D8432E | Stop 1 Carta, key accents |
| Girassol (yellow) | #F2B632 | Stop 2 Convite; fills only, never text |
| Azulejo (cobalt) | #2F5DA8 | Stop 3 Notícia |
| Salva (sage) | #5E8C66 | Stop 4 BD |
| Ameixa (plum) | #7A4A7A | Gramática |

Colour is never the only code. Every stop also has its icon and a number, and the stars mark difficulty.

## Grid
- Trim: A4 portrait 210 × 297 mm. The print file adds 3 mm bleed on every side.
- Margins: 16 mm outer and top, 18 mm inner, 20 mm bottom. Safe area is 5 mm inside the trim.
- 6-column grid, 5 mm gutters. Reading texts use 1 or 2 columns, never 3.

## Illustration (v2, 25 Sep 2026: book-wide rule from the user)
- **One style for the whole book: the Edwardian picture-book style of Beatrix Potter.** Delicate pen-and-ink linework, soft transparent watercolour washes, naturalistic animals in simple period clothing, a muted palette, cream paper showing through, and vignettes that fade into the paper.
- The characters are **original**. There are no Potter characters (no Peter Rabbit, no Mrs Tiggy-winkle) and nothing is copied from her plates. The style is borrowed; the cast is ours.
- **Generation:** openai/gpt-image-2.5-sunburst, **always** with `images/00-cast.png` as the reference image. Each prompt repeats the fixed style sentence and the character anchors (see `images/prompts-v2-potter.json`).
- **No text in images.** Every word is set in the layout.
- **Page colour:** plain-cream vignettes are white-balanced so their paper matches `--paper` #FCF4E3 exactly (a gain per channel). This leaves no visible box edge on the page.
- The previous human-cast gouache version is archived in `archive-v1-human/`.

## Cast (model sheet: images/00-cast.png, left → right)
| Character | Animal | Anchor details | Role |
|---|---|---|---|
| Inês | young brown rabbit | round red spectacles, yellow ribbon on one ear, yellow oilskin raincoat | asks questions |
| Tomás | young field mouse | small wooden wheelchair with red-spoked wheels, navy jacket | the joker; writes the (messy) news |
| Amara | young red squirrel | green knitted scarf, sketchbook and pencil | draws the comic |
| Farrusco | scruffy terrier puppy, white with tan patches | red collar, **no clothes**, the only animal on four legs | the troublemaker |
| Dona Rosa | plump lady badger | lilac shawl, white apron, newspaper | runs the kiosk |
| Sr. Joaquim | old tortoise | navy postman's cap, round spectacles, brown leather postbag | retired postman |

## Icons (drawn in SVG, 1 stroke weight, ink colour)
ouvir (ear), falar (speech bubble), ler (open book), escrever (pencil), desenhar (brush), a pares (2 heads), em grupo (3 heads), QR (phone).
