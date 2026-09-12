#!/usr/bin/env python3
"""Generate the Unit 1 artwork for the Year 1 Physical Education book.

Runs tools/pb_image_gen.py concurrently (quality: medium, always).
Every asset keeps the Pack A "Beatrix Potter" prompt template from
02-design-system.md, with the two placeholders substituted.

Scene plates are generated on a plain warm-cream paper ground so the
page generator can sample the corner pixel and fill its figure panel with
exactly that colour (seamless vignette). Character icons are generated
with a transparent background because they sit straight on the page.
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PY = os.path.join(REPO, ".venv", "bin", "python")
GEN = os.path.join(REPO, "tools", "pb_image_gen.py")
OUT = os.path.join(REPO, "work", "y01pe_u1", "img")

TPL = ("Soft children's storybook illustration in a Beatrix Potter style: {subject}, "
       "{action}. Gentle hand-drawn ink outlines, loose watercolour washes, warm muted "
       "palette, rounded friendly shapes, paper texture, no text, no hard shadows, "
       "cozy and calm.")

CREAM = ("plain uniform warm cream paper background showing on all four sides, "
         "the whole scene inside the picture with nothing cropped, no border, no frame, "
         "no lettering, no words, no signature")

TRANSPARENT = ("single isolated character on a fully transparent background, nothing "
               "behind the character, cut out cleanly, no white box, no shadow on the ground")

SIX = ("a red squirrel in a mustard knitted jumper, a badger in a teal jacket, a brown hare "
       "in an olive vest, a small hedgehog in a terracotta vest, a barn owl, and an otter in "
       "a green vest")

PIP = "a red squirrel in a mustard knitted jumper"
BRAM = "a badger in a teal jacket"
SORR = "a brown hare in an olive vest"
TUFT = "a small hedgehog in a terracotta vest"
WILL = "a barn owl"
ROWA = "an otter in a green vest"

JOBS = [
    # ---- scene plates (opaque, cream paper ground) -------------------------
    ("u1_opener", 0, "1536x1024", False,
     f"a sunny wildflower meadow behind a school on a summer morning, with six woodland friends standing together on the grass: {SIX}",
     f"all six standing upright together like pupils, leaving a clear gap of grass between each one, a low wooden gate and a hawthorn hedge in the far background, {CREAM}"),

    ("u1_close", 0, "1536x1024", False,
     f"the six woodland friends sitting resting in a loose ring on the meadow grass after a lesson: {SIX}",
     f"tired and happy, a water bottle and a folded mat on the grass beside them, {WILL} holding a small notebook under one wing, late afternoon light, {CREAM}"),

    ("u1_p11_space", 0, "1536x1024", False,
     f"{PIP} and {BRAM} walking side by side across a grassy meadow",
     f"keeping a very wide gap of empty grass between them so they are not touching, {SORR} waiting further back and watching them, gentle grass and small daisies, {CREAM}"),

    ("u1_p12_hopskip", 0, "1536x1024", False,
     f"{PIP} hopping high on one foot with the other leg tucked up, beside {BRAM} skipping with a long skipping rope",
     f"two different ways of springing up off the ground side by side on the grass, a cone in the background, {CREAM}"),

    ("u1_p13_speed", 0, "1536x1024", False,
     f"{SORR} sprinting low and fast across the meadow, and {TUFT} creeping slowly on tiptoe",
     f"two very different speeds and body heights on the same grass, stretching hare and a crouched careful hedgehog, {CREAM}"),

    ("u1_p14_apparatus", 0, "1536x1024", False,
     f"{PIP} crawling through a large wooden hoop standing upright on the grass, with a low wooden bench, a rolled mat and two cones waiting behind him",
     f"the whole hoop and the squirrel's paws both clearly visible, tidy apparatus on a grassy meadow, {CREAM}"),

    ("u1_games", 0, "1536x1024", False,
     f"three simple activity stations set out on the meadow grass: a line of three hoops, a low wooden bench with a soft mat at each end, and three small cones"
     f", with {PIP}, {BRAM} and {SORR} busy at different stations",
     f"a tidy circuit of movement stations with clear room between each station, warm afternoon light, {CREAM}"),

    # ---- character busts (transparent) -------------------------------------
    ("ch_pip", 0, "1024x1024", True,
     PIP, "standing upright and facing the reader, head and shoulders portrait, calm friendly expression, " + TRANSPARENT),
    ("ch_bramble", 0, "1024x1024", True,
     BRAM, "standing upright and facing the reader, head and shoulders portrait, steady thoughtful expression, " + TRANSPARENT),
    ("ch_sorrel", 0, "1024x1024", True,
     SORR, "standing upright and facing the reader, head and shoulders portrait, lively alert expression, " + TRANSPARENT),
    ("ch_tuft", 0, "1024x1024", True,
     TUFT, "standing upright and facing the reader, head and shoulders portrait, careful shy expression, " + TRANSPARENT),
    ("ch_willow", 0, "1024x1024", True,
     WILL, "perched upright and facing the reader, head and shoulders portrait, calm watchful expression, " + TRANSPARENT),
    ("ch_rowan", 0, "1024x1024", True,
     ROWA, "standing upright and facing the reader, head and shoulders portrait, cheerful expression, " + TRANSPARENT),
]


def run(job):
    name, _pad, size, transp, subject, action = job
    prompt = TPL.format(subject=subject, action=action)
    out = os.path.join(OUT, name + ".png")
    cmd = [PY, GEN, prompt, out, "--size", size, "--quality", "medium"]
    if transp:
        cmd.append("--transparent")
    log = open(os.path.join(OUT, name + ".log"), "w")
    r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=REPO)
    log.close()
    ok = r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 20000
    return name, ok, os.path.getsize(out) if os.path.exists(out) else 0


if __name__ == "__main__":
    only = sys.argv[1:]
    jobs = [j for j in JOBS if not only or j[0] in only]
    os.makedirs(OUT, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        for name, ok, size in ex.map(run, jobs):
            print(("OK  " if ok else "FAIL"), name, size, flush=True)
