#!/usr/bin/env python3
"""Generate the picture-glossary vignettes for Year 1 Physical Education.

Fourteen words, fourteen vignettes, in the same house style as the rest of the
book's plates (warm watercolour over ink line, British countryside, the book's
own cast). Transparent background so each one drops onto a cream card without a
white box around it. Model: openai/gpt-image-2.5-sunburst, medium, PNG.

  ./.venv/bin/python tools/y01pe_glossary_images.py [--only space hop]
"""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUTDIR = os.path.join(REPO, "work", "y01pe", "img")
GEN = os.path.join(HERE, "pb_image_gen.py")
PY = os.path.join(REPO, ".venv", "bin", "python")

STYLE = ("Children's picture-book illustration for a British primary school textbook, "
         "in the Prime Books house style: warm traditional watercolour washes over fine "
         "ink linework, soft cream paper, muted natural palette, hedgerow and meadow. "
         "Cast: Pip the red squirrel in a mustard-yellow knitted jumper, Bramble the "
         "badger in a blue jacket, Sorrel the hare in a brown waistcoat, Willow the barn "
         "owl, a small hedgehog in a russet shirt and an otter in a green vest. "
         "One clear subject only, centred, simple readable silhouette, generous empty "
         "space around it, gentle and encouraging in mood. "
         "No text, no letters, no numbers, no labels, no signs, no border, no frame, "
         "no watermark, plain transparent background.")

WORDS = {
    "space": "Sorrel the hare and Bramble the badger stand side by side with a wide clear "
             "gap between them, both stretching one arm out to show the gap.",
    "stop": "Pip the squirrel stands perfectly still on both feet with one paw raised "
            "flat, frozen mid-meadow, eyes forward.",
    "hop": "Sorrel the hare springs off one foot and lands on the same foot, the other "
           "leg tucked up, ears lifted with the effort.",
    "skip": "The little hedgehog skips: one step then a small hop, scarf swinging, "
            "both feet clear of the grass for a moment.",
    "join": "Pip the squirrel lands out of a small jump and, in the same smooth "
            "movement, walks straight on across the meadow.",
    "speed": "The same hare shown twice, one running fast with a blurred trail of "
             "motion, one plodding slowly, so fast and slow are seen together.",
    "level": "The badger crouches very low to the ground while, beside him, the "
             "squirrel stands up tall on tiptoe, showing a low level and a high level.",
    "apparatus": "A neat group of PE apparatus on the grass: a wooden bench, a rolled "
                 "blue mat, two red hoops and four small cones, nothing moving.",
    "watcher": "Willow the barn owl sits on a low fence post, head turned, both eyes "
               "wide and watching one thing closely.",
    "rule": "Six small animals sit in a ring on the grass and raise a paw together, "
            "agreeing a rule, faces calm and friendly.",
    "goal": "Pip the squirrel crouches ready to throw a small soft ball at one cone "
            "standing alone on the grass, a clear simple target.",
    "fair play": "Two animals take turns, one passing a yellow ball to the other while "
                 "the second waits with open paws, patient and smiling.",
    "warm-up": "Three animals gently jog and stretch on the grass in the morning air, "
               "loose and unhurried, waking their bodies up.",
    "cool-down": "The otter sits calmly on the grass drinking from a small cup of "
                 "water, breathing slowly, shoulders relaxed.",
}


def run(word, force=False):
    out = os.path.join(OUTDIR, "gl_" + word.replace(" ", "_") + ".png")
    if os.path.exists(out) and not force:
        return word, "kept"
    prompt = WORDS[word] + "\n\n" + STYLE
    cmd = [PY, GEN, prompt, out, "--size", "1024x1024", "--quality", "medium",
           "--transparent"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    ok = p.returncode == 0 and os.path.exists(out)
    return word, ("ok %d bytes" % os.path.getsize(out)) if ok else \
        ("FAIL " + (p.stderr or p.stdout)[-160:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUTDIR, exist_ok=True)
    words = a.only or list(WORDS)
    with ThreadPoolExecutor(max_workers=5) as pool:
        for word, status in pool.map(lambda w: run(w, a.force), words):
            print("%-11s %s" % (word, status), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
