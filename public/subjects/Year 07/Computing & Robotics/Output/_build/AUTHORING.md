# AUTHORING GUIDE — Prime Books "Computing 7"
Read this in full before writing any unit. Follow it exactly.

## Non-negotiables
1. **Rewrite everything from scratch.** Keep pedagogy and concepts; never reuse source phrasing.
   Every scenario, name, number, worked example, warm-up puzzle, test value and exercise datum
   must be NEW. Verify every calculation by hand.
2. **British English.** programme, recognise, organise, colour, centre, practise (verb) /
   practice (noun), pupils (not students, though "learners" is fine), Year (not Grade),
   enquiry, whilst is fine, maths (not math).
3. **NO em-dashes (—) anywhere.** Use commas, colons or full stops. En-dash (–) ONLY for
   numeric ranges: `Ages 11–14`, `pages 12–18`.
4. **Portuguese flavour.** Pupil names: Beatriz, Gonçalo, Inês, Tomás, Matilde, Rodrigo, Leonor,
   Duarte, Carolina, Afonso, Salvador, Mariana. Contexts: Lisbon trams (28, 15E), the Tejo,
   olive groves in the Alentejo, cork oaks, the Atlantic, Cascais marina, pastéis de nata,
   Serra da Estrela, Douro vineyards, sardine festivals, Oceanário, Belém, Sintra.
   Currency €. Metric units. 24-hour clock.
5. **No placeholders.** No "TODO", no lorem, no "sample". Everything finished.

## Markdown dialect (the build engine)
```
## [Unit 7.1 · Topic 3] Topic heading        -> topic heading with signal eyebrow
### Sub heading                              -> signal-coloured subhead
#### Small heading                           -> minor heading
- bullet            +ticked bullet           -> dot list / tick list
1. numbered         a. lettered              -> signal numeral chips / alpha list
| a | b |  with |---|---| separator          -> table
```python  ... ```                           -> highlighted dark code slab
```out   ... ```                              -> console-output panel
!fig[**Figure 1.2** Caption text](name.png)  -> figure with caption
!fig[**Figure 1.2** Caption](n.png){fig-frame} -> figure with hairline border
::: scenario ... :::        ::: warmup Warm up ... :::
::: remember ... :::        ::: know ... :::
::: further Go further ...:::  ::: challenge Challenge yourself ... :::
::: practise Practise ... :::  ::: keywords ... :::
<!--html  ...raw html...  -->                -> raw passthrough (openers, project pages)
```
Block labels: pass a custom label after the block name, e.g. `::: practise Practise 3`.
Inline: `code`, **bold**, *italic*, [link](url).

## Unit file skeleton
Each unit file `NN_unit7X.md` starts with `<!-- unit: uX -->` (u1..u6 sets the signal colour),
then:
1. **Opener** (raw html `.opener` sheet): unit number, title, learning outcomes panel, art.
2. **Get started** + **Scenario** + **Warm up** + **Do you remember**
3. **Topics** in order (see curriculum map). Each topic = `## [Unit 7.X · Topic N] Title`
   followed by `### Learn` prose, figures, code, tables, then `::: practise`.
   Sprinkle `::: keywords`, `::: know`, `::: further` where they genuinely help.
4. **Go further**, **Challenge yourself**
5. **Final project** (raw html `.brief` + milestones + rubric table)
6. **Evaluation** (traffic-light table using `<span class="dotc g/a/r"></span>`)
7. **What can you do?** (tick checklist)
8. **Keywords** round-up strip

## Tone
Warm, precise, second person ("you"), never patronising. Short paragraphs (2–4 sentences).
Explain the why before the how. Assume a bright 11 to 12 year old who has used Scratch.

## Code rules
- Python 3 syntax, 4-space indent, valid and runnable. Comments in British English.
- micro:bit code uses `from microbit import *`.
- Every code block that prints must be followed by a matching ```out block with the EXACT
  output that code would produce. Check it mentally line by line.
- Keep lines under ~62 characters so they never overflow the slab.

## Figures
Reference images that will exist in `Output/Images/`. Use the naming convention
`u<unit>_<slug>.png`, e.g. `u1_idle_shell.png`. List every figure you reference at the
END of your file inside an HTML comment block:
```
<!--IMAGEJOBS
[{"name":"u1_idle_shell","size":"landscape_4_3","prompt":"..."}]
-->
```
Prompt style: "Flat geometric editorial vector illustration ... Strict palette: deep indigo
#0E1330, <signal hex>, warm cream #FBF8F1, coral #FF5A47 ... Absolutely no text, no letters,
no numbers, no words, no watermark." NEVER ask for text in an image; labels come from captions.

## Length target
Each unit: 4,500–6,000 words of finished prose, roughly 26–34 printed pages.

## Signal colours
u1 #2B5BE8 blue · u2 #00A38C teal · u3 #6B4EE6 violet · u4 #E4682A amber
u5 #C42D6B magenta · u6 #1F8A3B green
