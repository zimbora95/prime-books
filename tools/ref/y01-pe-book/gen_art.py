#!/usr/bin/env python3
"""Generate this book's own plates, in its own material and cast.

Prompts are written per plate, not templated: the standard's illustration
direction (Beatrix Potter watercolour, fine ink contours, warm muted pigments,
cream paper) is fixed, but every scene names the cast, the object and the place
so the art belongs to THIS book's meadow rather than to a generic sports day.
No plate carries lettering: text inside generated art is banned by the standard,
and a generated word is always a broken word.

    .venv/bin/python gen_art.py            # everything still missing
    .venv/bin/python gen_art.py opener-1   # one plate
"""
import os
import subprocess
import sys

WORK = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(WORK, "art")
GEN = os.path.join(WORK, "..", "..", "tools", "pb_image_gen.py")

STYLE = ("Children's book illustration in the style of Beatrix Potter: traditional "
         "watercolour with fine ink contours on lightly textured cream paper, warm "
         "muted pigments, gentle light, no modern objects, no lettering, no words, "
         "no numbers, no signage anywhere in the picture.")
CAST = ("The characters: Pip, a red squirrel in a mustard knitted jumper; Bramble, a "
        "badger in a teal jacket; Sorrel, a brown hare in an olive waistcoat; Tuft, a "
        "small hedgehog in a rust vest; Willow, a barn owl; Rowan, an otter in a green "
        "vest.")
PLACE = ("The place: the meadow behind a small stone village school, with a white "
         "chalk line and small orange cones on the grass, and the school's double "
         "doors standing open onto a wooden hall with wall bars and a stack of mats.")

PLATES = {
 # unit 1 - Moving Well
 "opener-1": ("Wide morning view of the meadow: Pip the squirrel in his mustard jumper "
              "running along a white chalk line, Bramble the badger in a teal jacket "
              "placing a small orange cone, Sorrel the hare in an olive waistcoat "
              "mid-hop, Tuft the hedgehog in a rust vest rolling a wooden hoop, Willow "
              "the barn owl on a low bench, Rowan the otter in a green vest with a red "
              "ball. " + PLACE + " " + CAST + " " + STYLE),
 "hook-1": ("A single wide panel: the meadow seen from a child's height, five small "
            "woodland animals crossing the grass in five different ways - running, "
            "walking, hopping, rolling, skipping - each in knitted clothes, small in "
            "the wide green field. " + PLACE + " " + CAST + " " + STYLE),
 "model-1": ("A close, warm study of four pairs of animal feet on a white chalk line: a "
             "squirrel's paws at a walk, a hare's long feet mid-run, a badger's feet "
             "stopped still side by side, a hedgehog's small feet beside an orange "
             "cone. Low viewpoint on the grass. " + PLACE + " " + CAST + " " + STYLE),
 "breath-1": ("One large image: Sorrel the brown hare in her olive waistcoat landing "
              "from a hop on the grass, front paws planted together, ears back, a "
              "single small puff of chalk dust under her feet. Big quiet space around "
              "her. " + PLACE + " " + CAST + " " + STYLE),
 "step-1a": ("A small vignette: a hare hopping on one foot on the grass, the other foot "
             "tucked up, seen from the side. " + CAST + " " + STYLE),
 "step-1b": ("A small vignette: a squirrel and a badger skipping side by side towards a "
             "low wooden bench, holding one hand each. " + CAST + " " + STYLE),
 "step-1c": ("A small vignette: Pip the squirrel and Bramble the badger walking together "
             "holding paws, moving as one, their feet in step on the grass. "
             + PLACE + " " + CAST + " " + STYLE),

 # unit 2 - Understanding Movement
 "opener-2": ("Willow the barn owl on the bench at the edge of the meadow, watching the "
              "others: the squirrel and the badger copying each other's shape on the "
              "grass, the hare mid-stride, the otter with a ball. " + PLACE + " " + CAST
              + " " + STYLE),
 "model-2": ("A clear, simple study: a squirrel, a badger and a hare standing in a row "
             "seen from the front, each showing one body part - head, arm, leg, foot - "
             "in a still, easy pose. " + CAST + " " + STYLE),
 "breath-2": ("One large image: the owl Willow perched on the back of a wooden bench in "
              "the meadow at dusk, everything else still, long soft shadows on the "
              "grass. " + PLACE + " " + CAST + " " + STYLE),
 "step-2a": ("A small vignette: a badger watching a hare's shape, both standing still, "
             "the badger's head tilted. " + CAST + " " + STYLE),
 "step-2b": ("A small vignette: two animals copying the same shape side by side, arms "
             "out wide like a tree. " + CAST + " " + STYLE),
 "step-2c": ("A small vignette: Sorrel the hare holding a shape - one leg lifted, arms "
             "wide - while Willow the owl on her bench watches her closely. "
             + PLACE + " " + CAST + " " + STYLE),

 # unit 3 - Moving Creatively
 "opener-3": ("The meadow in wind: the six animals making shapes on the grass, arms and "
              "legs curved like branches, one rolling like a leaf, one stretched tall "
              "like a tree, chalk line forgotten. " + PLACE + " " + CAST + " " + STYLE),
 "model-3": ("A playful study of invented shapes on the grass: a hedgehog curled into a "
             "round shape, a hare stretched long, a squirrel balanced on one paw, an "
             "otter arched like a bridge. " + CAST + " " + STYLE),
 "breath-3": ("One large image: autumn leaves blowing across the meadow in a gust, one "
              "hare mid-leap chasing a leaf, the grass bent all one way. " + PLACE + " "
              + CAST + " " + STYLE),
 "breath-3b": ("One large image: soft rain falling on the meadow, puddles forming in the "
               "grass, the school door open with warm light inside, nobody outside. "
               + PLACE + " " + STYLE),
 "step-3a": ("A small vignette: a wooden hoop lying on the grass and a hedgehog looking "
             "at it, considering. " + CAST + " " + STYLE),
 "step-3b": ("A small vignette: a blue mat on the hall floor and a squirrel rolling "
             "along it. " + PLACE + " " + CAST + " " + STYLE),

 # unit 4 - Taking Part
 "opener-4": ("A meadow game in progress: an otter throwing a red ball, a badger "
              "catching it, a squirrel collecting bean bags into a basket, a hare and a "
              "hedgehog waiting their turn beside an orange cone. " + PLACE + " " + CAST
              + " " + STYLE),
 "model-4": ("A clear study of three jobs in one small game: a thrower with a red ball, "
             "a catcher with paws ready, a collector holding a basket of bean bags. "
             + PLACE + " " + CAST + " " + STYLE),
 "breath-4": ("One large image: a red ball caught in mid-air above the grass, the "
              "meadow soft behind it, one small paw just out of frame. " + PLACE + " "
              + CAST + " " + STYLE),
 "breath-4b": ("One large image: the meadow at the end of the afternoon, kit packed "
               "away against the school wall - hoops stacked, a folded mat, two cones - "
               "and the grass empty and still. " + PLACE + " " + STYLE),
 "step-4a": ("A small vignette: animals forming a line behind an orange cone, waiting "
             "their turn, calm and patient. " + CAST + " " + STYLE),
 "step-4b": ("A small vignette: a hedgehog leading a small game, standing in front of "
             "the others, one paw raised. " + CAST + " " + STYLE),
 "step-4c": ("A small vignette: Rowan the otter standing at the head of a small game "
             "with one paw raised in the air to start it, the others lined up behind "
             "the cone, all looking at him. " + PLACE + " " + CAST + " " + STYLE),

 # unit 5 - Taking Responsibility
 "opener-5": ("End of a lesson: the animals carrying kit back together - a badger and a "
              "squirrel carrying a low bench between them, a hare with a hoop over her "
              "shoulder, a hedgehog rolling a mat, the owl watching from the bench, the "
              "otter holding the hall door open. " + PLACE + " " + CAST + " " + STYLE),
 "model-5": ("A warm study of sharing and care: two animals passing a hoop to each "
             "other, one animal kneeling to help another up, a third holding a door. "
             + PLACE + " " + CAST + " " + STYLE),
 "breath-5": ("One large image: a stack of mats and hoops resting against the wall bars "
              "in the quiet hall, late light through the open door, nobody in the room. "
              + PLACE + " " + CAST + " " + STYLE),
 "breath-5b": ("One large image: the open hall door from inside, bright meadow grass "
               "beyond it, the otter holding the door with one paw, the others going "
               "out into the light. " + PLACE + " " + CAST + " " + STYLE),
 "step-5a": ("A small vignette: a badger carrying a wooden hoop safely at his side, "
             "both paws on it. " + CAST + " " + STYLE),
 "step-5b": ("A small vignette: two animals speaking kindly, one with a paw on the "
             "other's shoulder. " + CAST + " " + STYLE),

 # unit 6 - Healthy Bodies
 "opener-6": ("After the lesson: the animals resting on the grass, chests rising and "
              "falling, a water bottle and a small cup beside them, the hall door open "
              "behind. Warm afternoon light. " + PLACE + " " + CAST + " " + STYLE),
 "model-6": ("A gentle study of a moving body: a hare with a paw on her own chest, a "
             "badger with a paw on his ribs, both standing still and breathing, and a "
             "squirrel drinking from a small cup. " + PLACE + " " + CAST + " " + STYLE),
 "breath-6": ("One large image: the six animals lying on their backs in the meadow "
              "grass looking up at soft clouds, arms and legs spread, completely still, "
              "warm light. " + PLACE + " " + CAST + " " + STYLE),
 "breath-6b": ("One large image: a small cup of water standing on a low wooden bench in "
               "the sun, the meadow out of focus behind it, one drop on the wood. "
               + PLACE + " " + STYLE),
 "step-6a": ("A small vignette: a squirrel with a paw on his own wrist feeling his "
             "heartbeat, eyes closed. " + CAST + " " + STYLE),
 "step-6b": ("A small vignette: a cup of water and a small bottle standing on a low "
             "bench in the sun. " + PLACE + " " + STYLE),
 "step-6c": ("A small vignette: two animals sitting on the grass, paws resting on their "
             "chests, eyes closed, breathing slowly and calmly in the shade of the "
             "wall. " + PLACE + " " + CAST + " " + STYLE),

 # front and back matter
 "cover": ("The meadow at first light seen wide, the six animals mid-movement along a "
           "white chalk line with the school's open doors behind them, generous empty "
           "sky above the horizon. " + PLACE + " " + CAST + " " + STYLE),
 "gloss-hoop": ("A small vignette: a wooden hoop standing on the grass. " + STYLE),
 "gloss-cone": ("A small vignette: a small orange cone on the grass. " + STYLE),
 "gloss-line": ("A small vignette: a white chalk line drawn across green grass. "
                + STYLE),
 "gloss-mat": ("A small vignette: a blue mat folded on the hall floor. " + PLACE
               + " " + STYLE),
 "backcover": ("Late afternoon, seen wide and quiet: the six animals in their knitted "
               "clothes walking away from the reader along the white chalk line "
               "towards the school's open doors, the meadow empty and still behind "
               "them, long soft shadows on the grass. No lettering. "
               + PLACE + " " + CAST + " " + STYLE),
}

SIZE = {"opener-1": "1536x1024", "cover": "1536x1024", "hook-1": "1536x1024",
        "backcover": "1536x1024",
        "breath-1": "1024x1024", "breath-2": "1024x1024", "breath-3": "1024x1024",
        "breath-4": "1024x1024", "breath-5": "1024x1024", "breath-6": "1024x1024"}
DEFAULT_SIZE = "1024x1024"


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    todo = only or list(PLATES)
    for name in todo:
        dest = os.path.join(ART, f"{name}.png")
        if os.path.exists(dest) and not only:
            print(f"  {name}: already there")
            continue
        size = SIZE.get(name, DEFAULT_SIZE)
        print(f"  generating {name} ({size}) ...", flush=True)
        r = subprocess.run([os.path.join(WORK, "..", "..", ".venv", "bin", "python"),
                            GEN, PLATES[name], dest, "--size", size],
                           capture_output=True, text=True)
        print("   ", (r.stdout or r.stderr).strip().splitlines()[-1:] or r.returncode)


if __name__ == "__main__":
    main()
