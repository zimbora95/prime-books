"""Generate the Y8 cover art (house cover collection style) in parallel.

    ../.venv/bin/python covers/gen_art.py [front_a front_b back_art ...]
"""
import concurrent.futures as cf, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
REPO = HERE.parents[2]
GEN = [str(REPO / ".venv/bin/python"), str(REPO / "tools/pb_image_gen.py")]
END = " No text, no letters, no numbers, no logos."

BASE = ("Editorial 3D still-life render for a school textbook cover, same series as a Mediterranean minimalist "
        "collection: seamless flat warm cream studio background (#F9F5EA) with no horizon line, the top fifth of the "
        "image completely empty cream. Behind the objects, one large perfectly FLAT two-dimensional circle in muted "
        "slate blue (#546E9E), no gradient, no shading, no shadows on it, about 60 percent of the image width, centred "
        "slightly left, in the upper two thirds. Objects stand on two chunky stepped slabs of porous beige travertine "
        "stone that rest on the cream floor, with a thin strip of cream floor visible below. Warm Mediterranean "
        "sunlight from the upper left, crisp contact shadows falling to the right, soft ambient bounce, matte tactile "
        "materials. Every object rests firmly on a surface or leans against one, nothing floating or levitating. ")

JOBS = {
    "front_a": (BASE + "Objects, Portuguese in feeling: a guitarra portuguesa (pear-shaped Portuguese twelve-string "
                "guitar with a round body and a fan-shaped metal tuning head) standing upright and leaning against the "
                "higher slab; on the lower slab a small stack of hand-painted blue-and-white Portuguese azulejo tiles "
                "with the front tile propped upright; on the higher slab a small antique brass armillary sphere on a "
                "short stand, and two glossy black ceramic swallows in the Bordallo Pinheiro style perched on the slab "
                "edge; a slim terracotta jug holding a sprig of olive leaves." + END, "1024x1024"),
    "front_b": (BASE + "Objects, Portuguese in feeling: a stack of three old cloth-bound books lying flat on the higher "
                "slab with a small antique brass armillary sphere on a short stand standing on top of them; a guitarra "
                "portuguesa (pear-shaped Portuguese twelve-string guitar with a round body and fan-shaped metal tuning "
                "head) leaning upright against the higher slab; on the lower slab a small stack of blue-and-white "
                "Portuguese azulejo tiles with one propped upright and a glossy black ceramic swallow in the Bordallo "
                "Pinheiro style sitting beside it; a potted slender cypress in a terracotta pot standing on the floor "
                "at the far left." + END, "1024x1024"),
    "back_art": ("Delicate loose pencil drawing with light sepia watercolour washes on warm cream paper, airy and "
                 "faint, lots of untouched paper: a quiet writer's desk beside an open tall window in an old Lisbon "
                 "house; through the window, tiled rooftops of Alfama and the river Tagus far away; on the desk an "
                 "open notebook, a small stack of books, a cup, a ceramic swallow; a wall partly covered in "
                 "hand-painted azulejo tiles drawn in fine line; a guitarra portuguesa leaning against the wall. Muted "
                 "sepia, soft grey and a touch of faded blue only. Composition spread evenly, the upper half very "
                 "light and sparse." + END, "1024x1536"),
}


def run(name):
    prompt, size = JOBS[name]
    r = subprocess.run(GEN + [prompt, str(HERE / f"{name}.png"), "--size", size], capture_output=True, text=True)
    return name, r.returncode, (r.stdout + r.stderr).strip()[-300:]


if __name__ == "__main__":
    names = sys.argv[1:] or list(JOBS)
    with cf.ThreadPoolExecutor(len(names)) as ex:
        for name, rc, log in ex.map(run, names):
            print(name, rc, log)
