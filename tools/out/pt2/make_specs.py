#!/usr/bin/env python3
"""Write the imprint-page specs for the Year 7-9 Portuguese 2nd Language books.

    .venv/bin/python tools/out/pt2/make_specs.py

The content follows the house imprint standard (tools/std_imprint_lib.py) and the
book's OWN copy where it exists:

  * hook + lead  = the book's own back-cover hook and blurb, recovered from the
    pre-damage master (git rev 1231bbd).  The reference books (y07-art-and-design,
    y07-humanities) carry exactly this pair on page 2 and on the back.
  * bullets      = the book's own INSIDE THIS BOOK items, verbatim, in Portuguese.
  * rows         = the standard six, plus LANGUAGE, because this book's own front
    matter turns on the European-Portuguese norm.
  * CURRICULUM   = the book's own claim ("segue o scheme of work de Português
    (2.ª língua) do Cambridge Lower Secondary"), never an invented syllabus code.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(HERE, "specs")

RIGHTS = ("© Prime School 2026. All rights reserved. No part of this publication "
          "may be reproduced, stored in a retrieval system or transmitted in any "
          "form or by any means without the prior written permission of the "
          "publisher.")
CREDITS = ("Editorial Board. Pedagogical Academic Group · Pedagogical Team · "
           "Pedagogical Department · Content Creation Team. Written and typeset "
           "in the Prime School Press studio, Lisbon.")
LICENCE = ("It is an independent publication and is not an official Cambridge "
           "Assessment International Education or Oxford University Press "
           "publication.")
LANGUAGE = ("European Portuguese (norma europeia): metric measurements, prices "
            "in euros, the 24-hour clock, and Portuguese spelling as used in "
            "Portugal.")

BULLETS = [
    "Unidades por temas do quotidiano",
    "Diálogos e textos autênticos",
    "Gramática apresentada e revista",
    "Cultura portuguesa e lusófona",
    "Listas de vocabulário e revisões",
]

BOOKS = [
    dict(slug="y07-portuguese-2nd", year=7, ages="Ages 11 to 12", page="612x792"),
    dict(slug="y08-portuguese-2nd", year=8, ages="Ages 12 to 13", page="595x765.12"),
    dict(slug="y09-portuguese-2nd", year=9, ages="Ages 13 to 14", page="595x765.12"),
]

for b in BOOKS:
    y = b["year"]
    spec = {
        "slug": b["slug"],
        "year": y,
        "title": "Portuguese 2nd",
        "sub": "Year %d · Student Manual" % y,
        "hook": "Português de verdade, passo a passo.",
        "lead": ("Português Língua Segunda para o Year %d: comunicação do dia a dia, "
                 "textos autênticos e gramática que cresce aos poucos." % y),
        "bullets": BULLETS,
        "rows": [
            ["EDITION", "First edition, 2026. Printed in full colour on white stock."],
            ["PUBLISHER", "Prime School Press is the publishing imprint of Prime School, Portugal."],
            ["RIGHTS", RIGHTS],
            ["CREDITS", CREDITS],
            ["CURRICULUM",
             "Follows the Cambridge Lower Secondary Portuguese (Second Language) "
             "scheme of work, Stage %d. Ages about %s." % (y, b["ages"][5:].replace(" to ", " to "))],
            ["LICENCE", LICENCE],
            ["LANGUAGE", LANGUAGE],
        ],
        "ages": b["ages"],
        "band": "Lower Secondary",
        "folio": 2,
        "page_size": b["page"],
    }
    os.makedirs(SPECS, exist_ok=True)
    path = os.path.join(SPECS, b["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", path, "| rows:", len(spec["rows"]))
