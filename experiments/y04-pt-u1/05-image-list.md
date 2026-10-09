# 05: Image list (v2, Beatrix Potter style)

- **Model:** `openai/gpt-image-2.5-sunburst`. The backend ignores the aspect-ratio and quality settings, so the outputs came back at 1024×1536, 1536×1024, 1254² and about 1994×789.
- **Prompts:** every full prompt, word for word, is in **`images/prompts-v2-potter.json`**.
- **Style sentence:** each prompt starts with the same one, word for word: "…the classic Edwardian picture-book style of Beatrix Potter: delicate fine pen-and-ink linework, soft transparent watercolour washes, naturalistic animals in simple period clothing, gentle muted palette, cream paper showing through…". This is followed by the character anchors and "Absolutely no text, letters, numbers or signage anywhere."
- **Consistency:** `00-cast.png` was generated first. Every scene was then generated with it as the reference `image_url`.
- **Superseded art:** the human-cast v1 (with its image list) is in `archive-v1-human/`.

| File | Page(s) | Content | Vision check |
|---|---|---|---|
| 00-cast.png | 2 (reference for all) | Model sheet: rabbit Inês, mouse Tomás in a wooden wheelchair, squirrel Amara, terrier puppy Farrusco, badger Dona Rosa, tortoise Sr. Joaquim | all six on model; no text |
| 01-opener.png | 3 | Steep Lisbon street, envelopes in the wind, the cast running; open sky at the top | on model |
| 02-found.png | 5 | The puppy with the envelope beside the red postbox; the whole cast | on model |
| 03-kiosk.png | 7 | Green kiosk; Dona Rosa moved, Sr. Joaquim shy | on model |
| 04-mailbox-library.png | 9, 22 | The postbox turned into a library (vignette, no characters) | ok |
| 05-inauguration.png | 12 | Ribbon-cutting, bunting, neighbours clapping | on model; extra neighbours as briefed |
| 06–09-bd1…bd4.png | 13, 14 | Four comic panels: the puppy steals a book → the chase → the book given to Sr. Joaquim → story time | on model; balloons checked against the speakers |
| 10-cover.png | 1 | All six at the postbox-library, with the river and bridge behind | on model |
| 11-newsroom.png | 21 | Making the class newspaper | first attempt hid the wheelchair; **regenerated** as an edit so the wheelchair is visible |
| 12-writing.png | 20 | Amara writing a letter, the puppy asleep | ok |
| 13-radio.png | 11 | The four friends listening to a wooden radio | ok |

- **Print preparation:** ×2 Lanczos upscale, light unsharp mask, JPEG q90 → `build/img/`. Plain-cream images are white-balanced to the page colour #FCF4E3.
- **Licence:** Beatrix Potter's own illustrations are in the public domain in the UK and EU (she died in 1943). These images are new AI-generated works in her *style*, with an original cast. Before commercial print, the publisher must confirm the provider's terms for commercial use.
