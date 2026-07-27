# Prime Books — "Circuitry & Craft" Design System
Cambridge Computing Year 07 · Prime School · 2026

A fresh identity. Deliberately NOT the Humanities Y7 book, NOT the primeschool.pt website.

## Concept
"Circuitry & Craft": the warmth of a well-made book meets the precision of a circuit board.
Editorial serif display (Fraunces, wonky/soft axes) against technical grotesque (Space Grotesk)
and a true mono (JetBrains Mono) for code. Every unit is colour-coded by a **signal hue**;
page furniture behaves like a trace routed across the page.

## Palette
| Token | Hex | Use |
|---|---|---|
| `--ink` | #0E1330 | body text, deep navy-black |
| `--ink-soft` | #3A4166 | secondary text |
| `--paper` | #FBF8F1 | page stock (warm cream) |
| `--paper-2` | #F2EDE1 | tint panels |
| `--rule` | #D8D0BF | hairlines |
| `--signal-1` | #2B5BE8 | Unit 7.1 electric blue |
| `--signal-2` | #00A38C | Unit 7.2 teal |
| `--signal-3` | #6B4EE6 | Unit 7.3 violet |
| `--signal-4` | #E4682A | Unit 7.4 amber-orange |
| `--signal-5` | #C42D6B | Unit 7.5 magenta |
| `--signal-6` | #1F8A3B | Unit 7.6 green |
| `--coral` | #FF5A47 | accent, alerts |
| `--gold` | #C9A35C | rare flourish, cover foil |

Rule: exactly ONE signal hue per unit. Feature blocks tint from that hue, never mix two signals.

## Typography
- **Display** Fraunces (opsz/wght/SOFT/WONK) — unit numbers, titles, drop numerals.
- **UI/Headings** Space Grotesk — feature labels, running heads, tables.
- **Body** Source Sans 3 — 10.2pt / 15.2pt leading.
- **Code** JetBrains Mono — 9pt, tab=4.
No em-dashes anywhere. En-dashes only for ranges.

## Page
- Trim 210 × 270 mm, margins 18mm outer / 20mm top / 22mm bottom, gutter 20mm.
- Two-column body on Learn spreads; single column for projects/evaluation.
- Running foot: unit number · topic · folio, hairline above, signal-tinted folio chip.

## Feature blocks (each has a fixed visual grammar)
| Feature | Treatment |
|---|---|
| Get started | Full-bleed signal band, reversed white type, hero illustration |
| Scenario | Cream card, 3mm signal left-edge, italic Fraunces intro |
| Learning outcomes | Ruled checklist, signal ticks |
| Warm up | Rounded tint panel, dashed signal border |
| Do you remember | Paper-2 panel, circular signal numeral |
| Learn | Body text; keyword terms bolded in signal |
| Practise | Numbered list, signal numeral chips |
| Did you know | Coral hairline box + spark glyph |
| Go further | Violet-neutral panel, arrow glyph |
| Challenge yourself | Solid signal panel, reversed type |
| Final project | Full page, brief + milestones + rubric |
| Evaluation | Traffic-light self-assessment grid |
| What can you do | Outcome checklist, tick column |
| Keywords | Signal-tinted definition strip |
| Code | Dark ink slab, mono, signal caret gutter |

## Illustration
fal.ai `openai/gpt-image-2`, quality medium. Flat geometric editorial vector, isometric where
technical. Strict palette, generous negative space, NO text/lettering in any generated image.
