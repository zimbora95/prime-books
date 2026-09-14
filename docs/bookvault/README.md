# BookVault: the spec this repo builds to

These three files are BookVault's own, kept here because every number in
`tools/make_bookvault_files.py` comes out of them. They win over the code: if
BookVault change a figure, update this folder first, then the tool.

| File | What it is |
|---|---|
| `Guide-To-PDFs.pdf` | *Your Guide to Supplying Print-Ready PDF Files*, 23 pages |
| `v4_Text_279_216.pdf` | the text (interior) template: 222 x 285 mm media |
| `v4_PerfectBound_Cover_279_216_5.pdf` | the cover template, perfect bound, 5 mm spine: 443 x 285 mm |

## Text file (the interior)

- Single pages, portrait. Page 1 prints on the first **right-hand** page (p.5).
- **3 mm bleed** on every edge (p.5); a page needing bleed means the whole
  document is set up that way. Trim 216 x 279 mm gives a media box of
  **222 x 285 mm**, which is exactly their text template's page size.
- **Safety margin 20 mm on the gutter** (p.3); their template draws its binding
  edge at **17 mm**. Content keeps 5 mm clear of the other three trim edges.
- **Page count: one less than a divisible of 12** (11, 23, 35 ... 107). Their
  production barcode is added to the last page, so keep that page clear (p.5).
- Images 300 DPI (150 absolute minimum), fonts embedded, transparency flattened,
  no trim or bleed marks (p.3, p.9).
- PDF/A compliant or, if possible, **PDF/X-1a:2001** (p.5). Colour: CMYK with a
  FOGRA profile is preferred, **RGB is accepted** and converted by them (p.6).
- Files are checked by their preflight before printing: solid black 100% K,
  overprint off, minimum 4 pt text, and no lines thinner than 0.25 pt (p.9-11).

## Cover file (the wrap)

- One document: **back + spine + front**, sized by the p.18 formula
  `2 x trim width + spine + 3 mm + 3 mm` by `trim height + 3 mm + 3 mm`. Their
  perfect-bound template carries a 5 mm spine, so it is 443 x 285 mm.
- Spine width comes from their **sizing calculator** (home > help > sizing
  calculator), rounded **up to a whole millimetre** - p.18: 100 pages on 80 gsm
  bond = 5.6 mm, rounded to 6 mm.
- Keep spine content central and clear of its edges (p.19); if the inside of the
  cover is printed, leave 5 mm blank either side of the spine for the glue.
- **Barcode area**: their template reserves a **38 x 25 mm** box on the back
  cover, 6.4 mm in from the right trim and 3.3 mm up. A barcode is required for
  printing outside the UK - Prime School is in Portugal, so keep it clear.
- Content stays 5 mm clear of the trim; no trim or bleed marks (p.3, p.19).

## Binding options

The pack builder emits a **perfect-bound paperback** spread. The guide has a
separate setup for case-laminate hardback and for a jacketed hardback (board
sizes, 18 mm wrap, 133 mm dustjacket flaps) - see p.20-23 - which is not
implemented: no Prime Books title is printed as hardback yet.
