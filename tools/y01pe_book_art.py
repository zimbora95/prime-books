#!/usr/bin/env python3
"""Generate every plate for the Year 1 Physical Education book.

Pack A "Beatrix Potter" prompt template from 02-design-system.md, with the two
placeholders substituted. Quality is pinned to medium (user requirement).

Scene plates are generated on a plain warm-cream paper ground so the page
generator can sample the corner pixel and fill the figure panel with exactly
that colour. Character assets are generated with a transparent background
because they sit straight on the page.
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PY = os.path.join(REPO, ".venv", "bin", "python")
GEN = os.path.join(REPO, "tools", "pb_image_gen.py")
OUT = os.path.join(REPO, "work", "y01pe", "img")

TPL = ("Soft children's storybook illustration in a Beatrix Potter style: {subject}, "
       "{action}. Gentle hand-drawn ink outlines, loose watercolour washes, warm muted "
       "palette, rounded friendly shapes, paper texture, no text, no hard shadows, "
       "cozy and calm.")

CREAM = ("plain uniform warm cream paper background showing on all four sides, "
         "the whole scene inside the picture with nothing cropped, no border, no frame, "
         "no lettering, no words, no signature, no numbers")

TRANSPARENT = ("single isolated figure on a fully transparent background, nothing "
               "behind the figure, cut out cleanly, no white box, no shadow on the ground")

# --------------------------------------------------------------- characters --
PIP = "a red squirrel in a mustard knitted jumper"
BRAM = "a badger in a teal jacket"
SORR = "a brown hare in an olive vest"
TUFT = "a small hedgehog in a terracotta vest"
WILL = "a barn owl"
ROWA = "an otter in a green vest"
SIX = (f"{PIP}, {BRAM}, {SORR}, {TUFT}, {WILL}, and {ROWA}")
MEADOW = ("a wildflower meadow behind a small stone schoolhouse, tall grass, "
          "daisies and buttercups, a hawthorn hedge and a wooden gate in the far "
          "background, soft English countryside")

JOBS = [
    # ---------------------------------------------------------- front matter --
    ("fm_welcome", "1536x1024", False,
     f"six woodland friends arriving together at a wooden gate in a meadow: {SIX}",
     f"all six walking in through the gate one behind the other, leaving a clear gap of grass between each of them, {MEADOW}, {CREAM}"),
    ("fm_meet", "1536x1024", False,
     f"portrait line-up of six woodland friends standing side by side: {SIX}",
     f"each one standing upright and whole so every figure is clearly separate and none overlaps, calm friendly expressions, {MEADOW}, {CREAM}"),
    ("fm_kit", "1536x1024", False,
     "a Year 1 physical education kit laid out neatly on meadow grass: four small cones, "
     "a wooden hoop, three beanbags, a rolled mat, a skipping rope, a water bottle and a small hand bell",
     f"every object shown whole and separate with clear space around it, tidy arrangement seen from above and in front, {CREAM}"),
    ("fm_hall", "1536x1024", False,
     f"a school hall on a wet day with wooden floor, wall bars and a stack of mats, and {PIP} coming in from the rain",
     f"rain on tall windows, the squirrel shaking a tiny coat dry at the door, the empty polished floor ready for the lesson, {CREAM}"),
    ("fm_warmup", "1536x1024", False,
     f"the six woodland friends in a row on the meadow doing a warm-up together: {SIX}",
     f"all six with arms reaching up and heels lifting at the same time, a teacher's small hand bell on the grass in front of them, {MEADOW}, {CREAM}"),
    ("bm_festival", "1536x1024", False,
     f"a small festival of games on the meadow with the six woodland friends busy at different games: {SIX}",
     f"a hoop game, a rolling ball, a skipping rope, a cone race and two friends waiting their turn, bunting between two apple trees, {MEADOW}, {CREAM}"),

    # ------------------------------------------------------------- unit two --
    ("u2_opener", "1536x1024", False,
     f"{WILL} perched on a wooden hedge post, watching {BRAM} jump in the meadow below her",
     f"the badger mid-jump with both feet off the grass and the owl completely still on her post, hedge with brambles and wild roses, {MEADOW}, {CREAM}"),
    ("u2_p21", "1536x1024", False,
     f"{WILL} pointing one wing at {SORR} the hare in mid-jump, naming the movement",
     f"the owl perched on a post with a wing raised toward the jumping hare, the hare caught at the top of its jump, {MEADOW}, {CREAM}"),
    ("u2_p22", "1536x1024", False,
     f"{WILL} watching very still from her post while {BRAM} jumps on the meadow",
     f"the owl's body completely still and her eyes on the badger, the badger landing with a soft bend in the knees, {MEADOW}, {CREAM}"),
    ("u2_p23", "1536x1024", False,
     f"{PIP} landing a jump on the grass with bent knees and both arms out to the sides",
     f"the squirrel caught at the exact moment of landing, knees bent, arms wide, tail up for balance, {MEADOW}, {CREAM}"),
    ("u2_p24", "1536x1024", False,
     f"three friends waiting behind a white chalk line on the grass with a wooden hoop ahead of them: {PIP}, {TUFT} and {SORR}",
     f"all three with their feet behind the line and nobody having crossed it, the hoop empty and waiting a few steps ahead, {MEADOW}, {CREAM}"),

    # ----------------------------------------------------------- unit three --
    ("u3_opener", "1536x1024", False,
     f"a ring of flat stones on the meadow, with {SORR} dancing with a long silk ribbon and {WILL} watching from a post",
     f"the hare in a wide open shape with the ribbon curving through the air, the owl still and attentive, {MEADOW}, {CREAM}"),
    ("u3_p31", "1536x1024", False,
     f"{TUFT} making a wide star shape with arms and legs spread, beside {SORR} making a tall thin shape stretched up on tiptoe",
     f"two very different shapes side by side on the grass so the contrast is clear, {MEADOW}, {CREAM}"),
    ("u3_p32", "1536x1024", False,
     f"a large wooden hoop lying flat on the grass looking exactly like a little river, with {ROWA} stepping in and out of it",
     f"the otter mid-step with one foot inside the hoop and one outside, grass and daisies around the hoop, {MEADOW}, {CREAM}"),
    ("u3_p33", "1536x1024", False,
     f"a path across the meadow made of three cones, a hoop and a low bench, with {PIP} halfway along it deciding what to do next",
     f"the squirrel paused in the middle of the path, looking at the bench ahead, the whole path visible, {MEADOW}, {CREAM}"),
    ("u3_p34", "1536x1024", False,
     f"{SORR} dancing with a long ribbon inside the stone ring on the meadow while {WILL} watches",
     f"the ribbon sweeping in a wide curve, the hare's movement light and swirling like weather, {MEADOW}, {CREAM}"),

    # ------------------------------------------------------------ unit four --
    ("u4_opener", "1536x1024", False,
     f"six woodland friends sitting in a ring on the meadow grass with one yellow ball: {SIX}",
     f"everyone sitting in the circle including the last one, one ball in the middle, an owl on a post at the edge keeping score in a little book, {MEADOW}, {CREAM}"),
    ("u4_p41", "1536x1024", False,
     f"a sitting ring on the meadow with a yellow ball inside it and every one of the friends in the ring: {SIX}",
     f"no gaps and nobody left outside the ring, the ball resting in the middle on the grass, {MEADOW}, {CREAM}"),
    ("u4_p42", "1536x1024", False,
     f"{ROWA} throwing a spotted ball underarm while {PIP} catches it with both paws",
     f"the ball in the air between them, both animals watching the ball, an owl on a post behind them, {MEADOW}, {CREAM}"),
    ("u4_p44", "1536x1024", False,
     f"{SORR} leading three friends in a hopping line: {TUFT}, {PIP} and {ROWA} copying her hop",
     f"the hare at the front hopping and the three behind copying the same hop, all on one leg at the same moment, {MEADOW}, {CREAM}"),
    ("u4_p46", "1536x1024", False,
     f"{PIP} with ears up and both paws still, listening to {BRAM} who is speaking to him",
     f"the badger talking and the squirrel frozen mid-step, listening first and moving afterwards, {MEADOW}, {CREAM}"),

    # ------------------------------------------------------------ unit five --
    ("u5_opener", "1536x1024", False,
     f"{BRAM} and {PIP} carrying a gym mat together across the meadow",
     f"both pairs of hands on the mat, four hands visible, walking slowly and together, {MEADOW}, {CREAM}"),
    ("u5_p52", "1536x1024", False,
     f"two friends carrying one rolled gym mat between them across the grass: {BRAM} and {PIP}",
     f"the mat entirely inside the picture and the weight clearly shared, both animals walking in step, {MEADOW}, {CREAM}"),
    ("u5_p53", "1536x1024", False,
     f"{TUFT} and {ROWA} sitting on the grass with one yellow ball between them, one waiting and one rolling it",
     f"the otter rolling the ball along the grass and the hedgehog waiting patiently with his paws in his lap, {MEADOW}, {CREAM}"),
    ("u5_p54", "1536x1024", False,
     f"{TUFT} asking {WILL} for help beside a spilled basket of beanbags on the grass",
     f"the hedgehog looking up and speaking, the owl on her post turning to listen, beanbags scattered and not yet tidied, {MEADOW}, {CREAM}"),
    ("u5_p55", "1536x1024", False,
     f"the woodland friends clapping for {TUFT} after a jump, {SORR}, {ROWA} and {PIP} cheering",
     f"the hedgehog standing a little shy in the middle and the others clapping with their paws up, warm afternoon light, {MEADOW}, {CREAM}"),

    # ------------------------------------------------------------- unit six --
    ("u6_opener", "1536x1024", False,
     f"{PIP} sitting under a big oak tree after a run, one paw on his chest and a water bottle on the grass beside him",
     f"the squirrel resting and completely still in the shade, chest rising, the bottle standing in the grass, {MEADOW}, {CREAM}"),
    ("u6_p61", "1536x1024", False,
     f"{PIP} sitting under the oak tree with his paw on his chest and a water bottle waiting on the grass close by",
     f"the squirrel resting quietly in the shade with a calm face, a few leaves falling around the tree, {MEADOW}, {CREAM}"),
    ("u6_p62", "1536x1024", False,
     f"{BRAM} showing the body parts that work in a jump, touching his knees and then pointing to his elbow",
     f"the badger standing in the meadow and pointing at his own knees and elbow so a child can copy, {MEADOW}, {CREAM}"),
    ("u6_p65", "1536x1024", False,
     f"the six woodland friends standing together on the meadow stretching their arms up before a game: {SIX}",
     f"all six with arms reaching high and heels lifting, a warm-up before play, {MEADOW}, {CREAM}"),
    ("u6_p66", "1536x1024", False,
     f"a small picnic on a checkered cloth under the oak tree: a whole apple, a pear, a carrot, a little bread, "
     f"a piece of cheese and a full water bottle, with {PIP} sitting beside it",
     f"every item of food shown whole and separate, the water bottle standing upright and easy to see, {MEADOW}, {CREAM}"),

    # ------------------------------------------------- character cut-outs ----
    ("ch_pip", "1024x1024", True, PIP,
     "standing upright and facing the reader, head and shoulders portrait, calm friendly expression, " + TRANSPARENT),
    ("ch_bramble", "1024x1024", True, BRAM,
     "standing upright and facing the reader, head and shoulders portrait, steady thoughtful expression, " + TRANSPARENT),
    ("ch_sorrel", "1024x1024", True, SORR,
     "standing upright and facing the reader, head and shoulders portrait, lively alert expression, " + TRANSPARENT),
    ("ch_tuft", "1024x1024", True, TUFT,
     "standing upright and facing the reader, head and shoulders portrait, careful shy expression, " + TRANSPARENT),
    ("ch_willow", "1024x1024", True, WILL,
     "perched upright and facing the reader, head and shoulders portrait, calm watchful expression, " + TRANSPARENT),
    ("ch_rowan", "1024x1024", True, ROWA,
     "standing upright and facing the reader, head and shoulders portrait, cheerful expression, " + TRANSPARENT),

    # ------------------------------------------------------- unit closes ----
    ("u2_close", "1536x1024", False,
     f"{WILL} on her hedge post with {BRAM} sitting on the grass below, both looking out over the meadow",
     f"the owl calm and the badger resting, a quiet end to the lesson, {MEADOW}, {CREAM}"),
    ("u3_close", "1536x1024", False,
     f"the six woodland friends making one big shape together on the meadow: {SIX}",
     f"all six joined into a single wide star shape with arms and wings out, laughing, {MEADOW}, {CREAM}"),
    ("u4_close", "1536x1024", False,
     f"the six woodland friends in a ring on the meadow with all their paws and wings together in the middle: {SIX}",
     f"a team huddle, one yellow ball resting on the grass beside the ring, {MEADOW}, {CREAM}"),
    ("u5_close", "1536x1024", False,
     f"the six woodland friends tidying the kit together on the meadow: mats stacked, hoops counted in a pile, cones in a neat row",
     f"{PIP} and {BRAM} carrying the last mat while the others stack hoops, everything tidy and complete, {MEADOW}, {CREAM}"),
    ("u6_close", "1536x1024", False,
     f"the six woodland friends resting together in the shade of a big oak tree at the end of the lesson: {SIX}",
     f"all six sitting and lying quietly under the oak, water bottles and a rolled mat on the grass, warm afternoon light, {MEADOW}, {CREAM}"),

    # --------------------------------------------------- spot vignettes ----
    ("sp_shapes", "1024x1024", True,
     f"{TUFT} standing in a wide star shape with arms and legs spread, beside {SORR} stretched tall on tiptoe",
     f"two friends showing two different body shapes side by side, {TRANSPARENT}"),
    ("sp_dance", "1024x1024", True,
     f"{SORR} dancing with a long silk ribbon curving through the air above her",
     f"the hare in a light twisting shape on tiptoe, {TRANSPARENT}"),
    ("sp_strong", "1024x1024", True,
     f"{PIP}, {ROWA} and {SORR} clapping and cheering together with their paws and wings up",
     f"three friends celebrating a good try, warm and friendly, {TRANSPARENT}"),
    ("sp_pace", "1024x1024", True,
     f"{PIP} walking briskly forward in mid-step with his arms swinging comfortably",
     f"an easy steady walk, calm face, {TRANSPARENT}"),
    ("sp_rest", "1024x1024", True,
     f"{PIP} sitting still on the grass resting with his paws on his knees and a water bottle standing beside him",
     f"the squirrel calm and a little tired, taking a rest, {TRANSPARENT}"),
    ("sp_match", "1024x1024", True,
     "a small soft beanbag and a little stitched leather ball resting together on a folded cloth",
     f"everyday gym kit for a throwing game, both objects whole and separate, {TRANSPARENT}"),
    ("sp_kit", "1024x1024", True,
     "a tidy pile of gym kit stacked neatly together: a folded mat, three hoops stood in a stack, and two cones beside them",
     f"everything put away neatly and complete, {TRANSPARENT}"),
    ("sp_share", "1024x1024", True,
     f"two small pairs of paws resting together on the rim of one wooden hoop on the grass",
     f"sharing one piece of kit, gentle and careful, {TRANSPARENT}"),
    ("sp_words", "1024x1024", True,
     f"{WILL} perched beside a small open book with words written on the pages, and {PIP} standing next to her pointing at one of them",
     f"two friends learning new words together, calm and friendly, {TRANSPARENT}"),
    ("sp_facts", "1024x1024", True,
     f"{WILL} perched on a stack of two old books with a small open notebook under one wing",
     f"the owl reading and checking, calm and scholarly, {TRANSPARENT}"),
]




def run(job):
    name, size, transp, subject, action = job
    prompt = TPL.format(subject=subject, action=action)
    out = os.path.join(OUT, name + ".png")
    if os.path.exists(out) and os.path.getsize(out) > 20000 and "--force" not in sys.argv:
        return name, True, os.path.getsize(out), "kept"
    cmd = [PY, GEN, prompt, out, "--size", size, "--quality", "medium"]
    if transp:
        cmd.append("--transparent")
    log = open(os.path.join(OUT, name + ".log"), "w")
    r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=REPO)
    log.close()
    ok = r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 20000
    return name, ok, os.path.getsize(out) if os.path.exists(out) else 0, "new"


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    jobs = [j for j in JOBS if not only or j[0] in only]
    os.makedirs(OUT, exist_ok=True)
    fails = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for name, ok, size, how in ex.map(run, jobs):
            print(("OK  " if ok else "FAIL"), name, size, how, flush=True)
            if not ok:
                fails.append(name)
    print("FAILED:", fails)
