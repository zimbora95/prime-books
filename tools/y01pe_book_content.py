#!/usr/bin/env python3
"""The whole Year 1 Physical Education book as page data.

Every original sentence from the book is preserved. Page numbers are assigned
by position, so the contents page is generated from the same list and can
never drift.
"""
from pb_engine import B

# --------------------------------------------------------------- unit meta --
UNITS = {
    1: ("Moving Well", "The Open Meadow", "U N I T  O N E"),
    2: ("Understanding Movement", "Watching Hedge", "U N I T  T W O"),
    3: ("Moving Creatively", "The Dance Ring", "U N I T  T H R E E"),
    4: ("Taking Part", "The Team Patch", "U N I T  F O U R"),
    5: ("Taking Responsibility", "The Kit Basket", "U N I T  F I V E"),
    6: ("Healthy Bodies", "Resting Oak", "U N I T  S I X"),
}


def hl(n):
    return f"Unit {n} · {UNITS[n][0]}"


def hr(n):
    return UNITS[n][1]


# ------------------------------------------------------------------ links --
LINKS = {
    "supermovers": ("https://www.bbc.co.uk/teach/supermovers/ks1-collection/zbr4scw",
                    "BBC Teach Super Movers — KS1",
                    "Songs and movement routines the class can copy together.",
                    "about 5 minutes each"),
    "shakeup": ("https://www.nhs.uk/healthier-families/activities/10-minute-shake-up/",
                "NHS 10 Minute Shake Up",
                "Ten-minute movement games, made for children aged 5 to 11.",
                "10 minutes"),
    "supermovers_all": ("https://www.bbc.co.uk/teach/supermovers",
                        "BBC Teach Super Movers",
                        "Watch a routine, then name the movements you saw.",
                        "about 5 minutes each"),
    "cosmic": ("https://cosmickids.com/learn/",
               "Cosmic Kids — learn",
               "Story-led yoga and movement for Early Years and Key Stage 1.",
               "5 to 20 minutes"),
    "gonoodle": ("https://www.gonoodle.com/",
                 "GoNoodle",
                 "Short movement and team games for a classroom or a hall.",
                 "3 to 10 minutes"),
    "yst": ("https://www.youthsporttrust.org/",
            "Youth Sport Trust",
            "Inclusive games and fair-play guidance for primary schools.",
            "teacher planning"),
    "nhs_active": ("https://www.nhs.uk/better-health/get-active/",
                   "NHS — get active",
                   "Why moving every day matters, and how much is enough.",
                   "teacher reading"),
    "nhs_five": ("https://www.nhs.uk/live-well/eat-well/5-a-day/",
                 "NHS — 5 A Day",
                 "What counts towards fruit and vegetables, and how much.",
                 "teacher reading"),
    "nhs_food": ("https://www.nhs.uk/healthier-families/food-facts/",
                 "NHS — healthier families: food facts",
                 "Everyday food and drink advice for families.",
                 "for families"),
    "nhs_exercise": ("https://www.nhs.uk/live-well/exercise/",
                     "NHS — exercise",
                     "Exercise guidance, including what children need.",
                     "teacher reading"),
    "nature": ("https://www.woodlandtrust.org.uk/naturedetectives/",
               "Woodland Trust — Nature Detectives",
               "Outdoor activities for the meadow, the park or the garden.",
               "outdoor lesson"),
    "rspb": ("https://www.rspb.org.uk/fun-and-learning/for-kids",
             "RSPB — fun and learning for kids",
             "Bird and wildlife activities to do outside.",
             "outdoor lesson"),
    "bhf": ("https://www.bhf.org.uk/informationsupport/support/healthy-living/staying-active",
            "British Heart Foundation — staying active",
            "How an active day helps the heart.",
            "teacher reading"),
    "cambridge": ("https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-primary/",
                  "Cambridge Primary",
                  "The programme framework this school follows.",
                  "teacher planning"),
    "primeschool": ("https://primeschool.pt/", "Prime School",
                    "The school this book belongs to.", "school site"),
}


def qr(key, title=None, blurb=None):
    url, t, blb, mins = LINKS[key]
    return B.qr(url, title or t, blurb or blb, minutes=mins)


def cap(label, text):
    return (label, text)


# ============================================================== the pages ===
def build_pages():
    pages, toc = [], []

    def add(kind, spec, folio, toc_entry=None):
        n = 3 + len(pages)
        pages.append(dict(kind=kind, spec=spec, folio=folio, num=n))
        if toc_entry:
            toc.append((toc_entry[0], n, toc_entry[1]))
        return n

    def c(hl_, hr_, kick, title, blocks, folio, toc_entry=None):
        return add("content", dict(hl=hl_, hr=hr_, kick=kick, title=title, blocks=blocks),
                   folio, toc_entry)

    def op(n, blurb, narrative, caption):
        name, ground, kick = UNITS[n]
        return add("opener", dict(num=n, kicker=kick, title=name.lower().capitalize(),
                                  ground=ground, blurb=blurb, narrative=narrative,
                                  topics=[(f"{n}.{i}", t) for i, t in
                                          enumerate(TOPICS[n], start=1)],
                                  caption=caption, img=f"u{n}_opener"),
                   f"UNIT {n}", (f"Unit {n} · {name}", 1))

    # ---------------------------------------------------- front matter ------
    c("Prime School Press", "Physical Education · Year 1",
      "PHYSICAL EDUCATION · YEAR 1", "About this book",
      [B.lead("This book is for children in Year 1, about five to six years old, and for "
              "the teachers and families who move with them."),
       B.para("Physical Education in Year 1 is not a sport exam. It is how a body learns "
              "to share a space, to stop when asked, to try a jump again, and to be kind "
              "while it does those things."),
       B.para("Children will practise walking, running, jumping, hopping, skipping, "
              "rolling, throwing, catching, kicking and balancing. They will dance, play "
              "simple team games, and notice what their body does when it works hard."),
       B.panel("green", "Success is trying", [
           "The activities are written so a child can join in with confidence. Success "
           "is trying, looking after a partner, and leaving the space tidy."], icon="safety"),
       B.plate("fm_warmup", None, flex=True, minh=200, maxh=270),
       B.para("Prime Books Physical Education Year 1 is a complete student book for the "
              "first year of primary school. It covers moving well, understanding "
              "movement, moving creatively, taking part, taking responsibility and "
              "healthy bodies, matching the school's Year 1 Physical Education scheme. "
              "Short teaching, unique watercolour plates, safety panels and play tasks "
              "sit on every topic.", size=11.0, pitch=14.6, after=0)],
      "ABOUT THIS BOOK", ("About this book", 1))

    add("toc", None, "CONTENTS", ("Contents", 1))

    c("Prime School Press", "Physical Education · Year 1",
      "PHYSICAL EDUCATION · YEAR 1", "The year at a glance",
      [B.lead("Three terms. Three chances to show what your body can do."),
       B.cards([("TERM 1 · Move and watch",
                 "Units 1 and 2. Space, run, jump, hop. Words for a movement. Look back "
                 "in December."),
                ("TERM 2 · Create and join",
                 "Units 3 and 4. Shapes and dance. Jobs in a small game. Look back in "
                 "March."),
                ("TERM 3 · Care and health",
                 "Units 5 and 6. Fair play and kit. Heart, rest, food, water. Look back "
                 "in June.")], numbered=False),
       B.plate("fm_welcome", None, flex=True, minh=180, maxh=310),
       B.note("Dates follow the Prime School year 2026/27: December 2026, March 2027, "
              "June 2027.", who="THE TEACHER SHOULD CONFIRM")],
      "THE YEAR AT A GLANCE", ("The year at a glance", 1))

    c("Prime School Press", "Before Unit 1", "GETTING STARTED · WELCOME TO THE MEADOW",
      "Welcome to the meadow",
      [B.lead("Behind the school there is a meadow. Grass, little flowers, room to run."),
       B.para("When it rains, there is the hall instead. Wooden floor, wall bars, mats in "
              "a stack. This book uses both places. The jobs do not change."),
       B.para("You will move. You will watch. You will take turns. You will stop when the "
              "teacher says stop."),
       B.plate("fm_welcome", cap("Picture 0.1", "Six friends arriving at the meadow gate. "
                                                "Look at the space they leave between each "
                                                "other."), flex=True, minh=170, maxh=230),
       B.panel("tint", "Come out to the meadow", [
           "Take off your jumper if you are hot. Drink some water. Look at the space. Are "
           "you ready?"], icon="move"),
       qr("nature", "Outside, all year",
          "Outdoor activities for the meadow, the park or the garden.")],
      "WELCOME TO THE MEADOW", ("Welcome to the meadow", 1))

    c("Prime School Press", "Before Unit 1", "GETTING STARTED · MEET THE SIX",
      "Meet the six",
      [B.lead("You will see them on almost every page. They are pupils, like you. They "
              "are not coaches."),
       B.plate("fm_meet", cap("Picture 0.2", "Pip, Bramble, Sorrel, Tuft, Willow and "
                                              "Rowan, standing so you can see each one "
                                              "whole."), flex=True, minh=180, maxh=240),
       B.cards([("Pip", "A red squirrel in a mustard jumper. He tries first."),
                ("Bramble", "A badger in a teal jacket. He is steady, and he likes to "
                            "count."),
                ("Sorrel", "A brown hare in an olive vest. She is fast.")], numbered=False),
       B.cards([("Tuft", "A small hedgehog in a terracotta vest. He is careful."),
                ("Willow", "A barn owl. She watches, and she says what she saw."),
                ("Rowan", "An otter in a green vest. He likes games with a ball.")],
               numbered=False)],
      "MEET THE SIX", ("Meet the six", 1))

    c("Prime School Press", "Before Unit 1", "GETTING STARTED · HOW TO USE THIS BOOK",
      "How to use this book",
      [B.lead("Each topic uses a few kinds of panel. Learn them once."),
       B.table(["Panel", "What you do"],
               [["The kit you need", "Read it before anybody moves."],
                ["Move it", "A short warm-up."],
                ["Watch me try", "One of the six shows the idea slowly."],
                ["Try it", "Your turn, with a body, not only a pencil."],
                ["Play together", "A game with at least one other person."],
                ["Safety first", "Read this. Then move."],
                ["Willow's notes", "What a watcher actually saw."],
                ["Look what I can do", "Tick what is true for you today."],
                ["Scan and show", "A link an adult opens for the whole class."]],
               widths=[0.34, 0.66]),
       B.panel("warn", "Who opens a link", [
           "A teacher or another adult holds any device that opens a link. You do not scan "
           "codes on your own."], icon="qr"),
       B.plate("fm_warmup", None, flex=True, minh=120, maxh=190)],
      "HOW TO USE THIS BOOK", ("How to use this book", 1))

    c("Prime School Press", "Before Unit 1", "GETTING STARTED · GETTING SET UP",
      "Getting set up",
      [B.lead("You need: a clear floor, trainers or bare feet as the teacher says, water, "
              "and the kit named on the page."),
       B.plate("fm_kit", cap("Picture 0.3", "The kit for a Year 1 lesson, laid out so every "
                                            "object is whole: cones, hoop, beanbags, mat, "
                                            "rope, water, bell."), flex=True, minh=180,
               maxh=250),
       B.today("Remember every lesson", [
           "Look at the space before you move into it.",
           "Know which kit is yours today.",
           "Leave the space tidy at the end."]),
       qr("supermovers")],
      "GETTING SET UP", ("Getting set up", 1))

    c("Prime School Press", "Before Unit 1",
      "GETTING STARTED · THE HALL, AND SAFETY FIRST", "The hall, and safety first",
      [B.lead("When it rains, the floor is the lesson."),
       B.plate("fm_hall", cap("Picture 0.4", "The hall on a wet day. Pip comes in from the "
                                             "rain. The floor is the lesson now."),
               flex=True, minh=170, maxh=230),
       B.panel("green", "Safety first", [
           "Listen to the teacher. Leave a space you could lie down in. Stop when you hear "
           "the bell or the word stop. Tell an adult if something hurts. Drink water. Take "
           "turns."], icon="safety"),
       B.ticks("Before every lesson", [
           "My space is a lie-down space.",
           "My water is at the side, not on the running line.",
           "I know where the mats are."])],
      "THE HALL, AND SAFETY FIRST", ("The hall, and safety first", 1))

    # ------------------------------------------------------- the six units ---
    for n in (1, 2, 3, 4, 5, 6):
        globals()["unit_%d" % n](c, op, toc, pages)

    # -------------------------------------------------------- back matter ----
    c("Physical Education · Year 1", "Look back", "THE YEAR · LOOK BACK", "Look back",
      [B.cards([("TERM 1 · Units 1 and 2",
                 "Can you still leave a space, stop, hop, skip, name a movement, and wait "
                 "behind a line?"),
                ("TERM 2 · Units 3 and 4", "A shape, a kit idea, a job in a ring, a listen."),
                ("TERM 3 · Units 5 and 6", "Fair play, kit, heart, water.")], numbered=False),
       B.plate("bm_festival", cap("Picture 7.0", "The festival of games at the end of the "
                                                 "year. Every game in this book comes back "
                                                 "for one afternoon."), flex=True, minh=170,
               maxh=240),
       B.steps("Try it", ["Show a hop-hop-skip to a partner.",
                          "Watch one jump and say one true sentence.",
                          "Play Traffic for one minute."]),
       B.ticks("Look what I can do", ["I can stop.", "I can name a movement.",
                                      "I can wait my turn."])],
      "LOOK BACK", ("Look back: the whole year", 1))

    words = [
        ("space", "A gap you can see. In Year 1, one you could lie down in."),
        ("stop", "Freeze. Feet still. Eyes on the teacher."),
        ("hop", "A spring on one foot, landing on the same foot."),
        ("skip", "A step and a hop, repeating."),
        ("join", "Finishing one movement and starting the next with no long pause."),
        ("speed", "How quickly a movement happens."),
        ("level", "How high or low the body is."),
        ("apparatus", "Kit you move on, over or through."),
        ("watcher", "The person who looks at one thing and says what they saw."),
        ("rule", "An agreement the group will keep."),
        ("goal", "One thing you will try, that a watcher can see."),
        ("fair play", "Same turns, no pushing, truth about the ball, keep going after a "
                      "mistake."),
        ("warm-up", "Gentle movement before the hard work."),
        ("cool-down", "Slowing the body after the hard work."),
    ]
    c("Physical Education · Year 1", "Words we used", "WORDS WE USED · 1 TO 7",
      "Words we used",
      [B.lead("Every word here is used somewhere in this book. Read it, say it, then use "
              "it."),
       B.table(["Word", "What it means"], [list(w) for w in words[:7]],
               widths=[0.28, 0.72]),
       B.spot("sp_words", 168)],
      "WORDS WE USED 1", ("Words we used (1)", 1))

    c("Physical Education · Year 1", "Words we used", "WORDS WE USED · 8 TO 14",
      "Words we used",
      [B.table(["Word", "What it means"], [list(w) for w in words[7:]],
               widths=[0.28, 0.72]),
       B.steps("Try it", ["Carry a mat with a partner.",
                          "Jog twenty seconds, then rest and drink water.",
                          "Say one kind, true sentence."]),
       qr("bhf", "A body that keeps moving",
          "How an active day helps the heart, from the British Heart Foundation.")],
      "WORDS WE USED 2", ("Words we used (2)", 1))

    c("Physical Education · Year 1", "Answers for every unit",
      "ANSWERS · UNITS 1, 2 AND 3", "Answers for every unit",
      [B.lead("Most PE tasks are answered with a body. Where a tick or a word is asked for, "
              "this page says what a good answer contains."),
       B.subhead("Unit 1"),
       B.table(["Topic", "Good answer"],
               [["1.1 stop", "Feet still. Space kept."],
                ["1.2 join", "Hop then skip with no long pause."],
                ["1.3 harder", "Slow is an acceptable answer."],
                ["1.4 bench", "Step down, one child, adult at the side."]],
               widths=[0.34, 0.66]),
       B.subhead("Unit 2"),
       B.table(["Topic", "Good answer"],
               [["2.1 word", "The word matches the movement (jump is not hop)."],
                ["2.3 landing", "Two feet, bent knees, still at the end."],
                ["2.4 line", "Wait until your name is called."]],
               widths=[0.34, 0.66]),
       B.subhead("Unit 3"),
       B.table(["Topic", "Good answer"],
               [["3.1 fifth shape", "Any held shape that is not the four named ones."],
                ["3.3 no run", "Walk, hop, crawl or skip. Not a run."],
                ["3.4 weather", "A movement that matches storm, leaf or rain."]],
               widths=[0.34, 0.66])],
      "ANSWERS 1", ("Answers for every unit (1)", 1))

    c("Physical Education · Year 1", "Answers for every unit",
      "ANSWERS · UNITS 4, 5 AND 6",
      "Answers for every unit",
      [B.subhead("Unit 4"),
       B.table(["Topic", "Good answer"],
               [["4.2 jobs", "Thrower, catcher, collector, swapped."],
                ["4.3 goal", "A body detail a watcher can see, not \u201cbe better\u201d."],
                ["4.6 listen", "Move only after the instruction ends."]],
               widths=[0.34, 0.66]),
       B.subhead("Unit 5"),
       B.table(["Topic", "Good answer"],
               [["5.2 fingers", "Out from under the mat."],
                ["5.3 extra turn", "Give the next two turns to the partner."],
                ["5.4 last box", "\u201cI want to go first\u201d is a want, not a need."]],
               widths=[0.34, 0.66]),
       B.subhead("Unit 6"),
       B.table(["Topic", "Good answer"],
               [["6.1 heart", "Faster after a jog, slower after rest."],
                ["6.2 parts", "Knees and ankles (not ears or nose)."],
                ["6.6 drink", "Water."]], widths=[0.34, 0.66])],
      "ANSWERS 2", ("Answers for every unit (2)", 1))

    c("Physical Education · Year 1", "Answers for every unit",
      "ANSWERS · WHERE THE FACTS CAME FROM", "Where the facts came from",
      [B.lead("Every Did you know? in this book was read on the named page on "
              "2026-08-19."),
       B.table(["Claim", "Source"],
               [["The heart beats faster during play because muscles need more blood, then "
                 "slows at rest", "NHS, physical activity for children and young people"],
                ["Warm up before harder play; slow down afterwards",
                 "NHS, activity advice for children"],
                ["Children need water when they have been running about",
                 "NHS, drinks and hydration for children"],
                ["Fruit and vegetables are part of everyday food", "NHS, 5 a day"]],
               widths=[0.55, 0.45]),
       B.panel("plain", "Why the sources are printed", [
           "A teacher or a family can check every one of these for themselves. The full "
           "addresses are listed on the next page."], icon="think"),
       B.spot("sp_facts", 158)],
      "WHERE THE FACTS CAME FROM", ("Where the facts came from", 1))

    c("Prime School Press", "Sources", "OUR SOURCES · FOR THE TEACHER", "Watch and learn",
      [B.lead("Every link in this book, in one place. Open these on a staff device first, "
              "then show the class."),
       B.qrgrid([(LINKS[k][1], LINKS[k][0]) for k in (
           "supermovers", "shakeup", "cosmic", "gonoodle", "yst", "nhs_active",
           "nhs_five", "nature", "rspb", "bhf", "nhs_food", "cambridge")], cols=4),
       B.para("All of these addresses were opened and checked before this book went to "
              "print. If an address ever stops working, the teacher can find the same "
              "organisation by name.", size=11.5, pitch=15.5, after=0)],
      "WATCH AND LEARN", ("Watch and learn (for the teacher)", 1))

    c("Prime School Press", "Sources", "OUR SOURCES · FOR THE TEACHER", "Our sources",
      [B.lead("Every fact and every address in this book comes from a named organisation, "
              "so an adult can look it up."),
       B.reflist([(LINKS[k][1], LINKS[k][0], LINKS[k][3]) for k in (
           "supermovers", "shakeup", "supermovers_all", "cosmic", "gonoodle", "yst",
           "nhs_active", "nhs_five", "nhs_food", "nhs_exercise", "nature", "rspb", "bhf",
           "cambridge", "primeschool")]),
       B.panel("plain", "Illustrations", [
           "Every illustration in this book is original artwork made for Prime Books, "
           "drawn in the Prime School Press studio. There are no photographs of real "
           "people in this book."], icon="kit")],
      "OUR SOURCES", ("Our sources", 1))

    return pages, toc


# ============================================================= unit content ==
TOPICS = {
    1: ["Space, walk, run, stop", "Hop, skip, join", "Fast, slow, high, low",
        "Hoops, benches, mats"],
    2: ["Words for a body", "Watch, then copy", "What good looks like", "A simple rule"],
    3: ["New shapes", "What the kit suggests", "Answer with your body",
        "Moving like weather"],
    4: ["Joining in", "Thrower, catcher, collector", "Your own goal", "A turn at leading",
        "What I can do", "Listen, then move"],
    5: ["Share and take turns", "Carry kit safely", "Fair play", "Ask for help",
        "Kind words"],
    6: ["What changes when you move", "Name the working parts", "How hard is hard enough",
        "Knowing your limit today", "Before, and afterwards",
        "Food and water for a moving body"],
}


def _k(n, i, extra=""):
    return f"UNIT {n} · TOPIC {n}.{i}" + (f" · {extra}" if extra else "")


def unit_1(c, op, toc, pages):
    n = 1
    op(n, "This ground is about using a space, then using a body: walk, run, stop, hop, "
          "skip, and kit that changes the floor.",
       "Pip runs. Bramble leaves a space. Willow watches the stop.",
       ("Picture 1.0", "The Open Meadow at the start of the year. Six friends, six bodies, "
                       "plenty of grass."))

    c(hl(n), hr(n), _k(n, 1), TOPICS[1][0],
      [B.plate("u1_p11_space", cap("Picture 1.1", "Pip and Bramble walk with a wide space "
                                                 "between them. Sorrel waits further back. "
                                                 "Look how nobody is touching."), flex=True,
               minh=200, maxh=330),
       B.today("Today you will", ["leave a space and stop when asked",
                                 "hop, skip and join two movements",
                                 "change speed and level on purpose",
                                 "move on, over and through simple apparatus"]),
       B.panel("plain", "The kit you need",
               ["Four cones, a clear floor, and a teacher with a bell or a clear word for "
                "stop."], icon="kit")],
      "1.1  SPACE, WALK, RUN, STOP", ("1.1  Space, walk, run, stop", 2))

    c(hl(n), hr(n), _k(n, 1, "WALK, RUN AND STOP"), "Walk, run and stop",
      [B.para("A space is a gap you can see. In Year 1, a good space is one you could lie "
              "down in without touching anyone."),
       B.para("Walk uses both feet, one after the other. Run uses both feet too, but there "
              "is a moment when both are off the floor. Stop means freeze: feet still, "
              "eyes on the teacher."),
       B.panel("tint", "Move it", ["Walk anywhere for one minute. Change direction when "
                                   "you meet somebody. Do not touch. Then stand still."],
               icon="move"),
       B.watch(["Pip runs. Bramble calls stop. Pip's feet finish the step they started, "
                "then they stay. He does not skid into Sorrel."], "ch_pip"),
       B.panel("green", "Safety first", ["Look where you are going. Leave a lie-down space. "
                                         "Stop means stop, even if the game is exciting."],
               icon="safety"),
       B.steps("Try it", ["Walk the space. Count how many children you can see without "
                          "turning your head.",
                          "Run to a cone and stop before you touch it. Do this four times.",
                          "When the teacher says stop, freeze. Tick if your feet were "
                          "still."]),
       B.ticks("Look what I can do", ["I left a space.", "I stopped when I was asked."])],
      "1.1  WALK, RUN AND STOP")

    c(hl(n), hr(n), _k(n, 2), TOPICS[1][1],
      [B.plate("u1_p12_hopskip", cap("Picture 1.2", "Pip hops on one foot. Bramble skips "
                                                    "with a rope. Two different movements, "
                                                    "both using a spring."), flex=True,
               minh=190, maxh=300),
       B.panel("tint", "Play together", ["Traffic. Green means walk. Yellow means slow. Red "
                                         "means stop. Play for two minutes. Nobody is out. "
                                         "If you bump, you just start again with a bigger "
                                         "space."], icon="play"),
       B.panel("plain", "The kit you need", ["Skipping ropes if you have them, or just a "
                                             "clear floor. Work in pairs."], icon="kit"),
       B.panel("tint", "Move it", ["Ten heel raises. Ten gentle jumps on the spot. Shake "
                                   "your feet."], icon="move")],
      "1.2  HOP, SKIP, JOIN", ("1.2  Hop, skip, join", 2))

    c(hl(n), hr(n), _k(n, 2, "THE JOIN"), "The join",
      [B.para("A hop is a spring on one foot, landing on the same foot. A skip is a step "
              "and a hop, repeating. To join them, you finish the hop and start the skip "
              "with no long pause in the middle."),
       B.watch(["Tuft hops three times on his right foot. Then he skips to the cone. The "
                "join is the third landing, which becomes the first skip."], "ch_tuft"),
       B.panel("green", "Safety first", ["Land softly, with a little bend in the knee. If "
                                         "you wobble, put the other foot down. That is "
                                         "still good work."], icon="safety"),
       B.steps("Try it", ["Hop four times on each foot. Hold a wall if you need to.",
                          "Skip to a cone and skip back.",
                          "Join them: hop, hop, skip, skip. Draw the order."],
               extra="MY SEQUENCE"),
       B.panel("warn", "Challenge", ["Do hop-hop-skip across the meadow without stopping in "
                                     "the middle. A partner watches the join."],
               icon="challenge")],
      "1.2  THE JOIN")

    c(hl(n), hr(n), _k(n, 3), TOPICS[1][2],
      [B.plate("u1_p13_speed", cap("Picture 1.3", "Sorrel sprints. Tuft creeps. Same "
                                                  "meadow, two speeds. Look at how high "
                                                  "each body is."), flex=True, minh=190,
               maxh=300),
       B.para("Speed is how quickly a movement happens. Level is how high or low the body "
              "is. You can change one of them on purpose."),
       B.para("Fast is not better than slow. Slow is often harder to hold."),
       B.panel("plain", "The kit you need", ["Two cones about eight metres apart, and a "
                                             "partner who watches."], icon="kit"),
       B.panel("tint", "Move it", ["Walk, then jog, then walk. Thirty seconds each."],
               icon="move")],
      "1.3  FAST, SLOW, HIGH, LOW", ("1.3  Fast, slow, high, low", 2))

    c(hl(n), hr(n), _k(n, 3, "FAST AND SLOW"), "Fast and slow",
      [B.watch(["Sorrel runs the eight metres as fast as she can. Then she crosses again "
                "as slowly as she can without stopping. Willow times both with a count of "
                "\u201cone-elephant, two-elephant\u201d."], "ch_sorrel"),
       B.panel("green", "Safety first", ["Fast needs a long space behind the finish cone so "
                                         "you can slow down. Do not run at a wall."],
               icon="safety"),
       B.steps("Try it", ["Cross fast. Cross slow. Tell your partner which felt harder.",
                          "Walk on tiptoes (high). Walk in a small squat (low).",
                          "Tick the sentence that is true for you."],
               tail=["Slow was harder than fast.", "High made me wobble.",
                     "I could change speed when asked."]),
       B.duo([("ch_sorrel", "FAST", "a long low run, arms working"),
              ("ch_tuft", "SLOW", "a small careful creep, body low")])],
      "1.3  FAST AND SLOW")

    c(hl(n), hr(n), _k(n, 4), TOPICS[1][3],
      [B.plate("u1_p14_apparatus", cap("Picture 1.4", "Pip crawls through a hoop. A bench "
                                                      "and a mat wait behind. The whole "
                                                      "hoop is in the picture, and so are "
                                                      "Pip's feet."), flex=True, minh=190,
               maxh=300),
       B.para("Apparatus is kit you move on, over or through. The movement you already know "
              "must still work when the floor changes."),
       B.panel("plain", "The kit you need", ["Hoops, a low bench or a line of mats, and a "
                                             "teacher who has tested the bench."],
               icon="kit"),
       B.panel("tint", "Move it", ["Bear walk to a hoop and stand inside it."], icon="move")],
      "1.4  HOOPS, BENCHES, MATS", ("1.4  Hoops, benches, mats", 2))

    c(hl(n), hr(n), _k(n, 4, "THE MEADOW GAMES"), "The meadow games",
      [B.lead("Play three stations. Spend four minutes at each."),
       B.watch(["Pip steps into the hoop, crawls through, then walks along the bench with "
                "his eyes on the far end. He does not rush the bench."], "ch_pip"),
       B.panel("green", "Safety first", ["Only one child on a bench. An adult stands at the "
                                         "side. Mats stay flat. Never jump off a bench in "
                                         "this topic: step down."], icon="safety"),
       B.steps("Try it", ["Through a hoop, then along a line of mats.",
                          "Change the order: mats first, hoop second.",
                          "Tell Willow one thing that changed when the kit was there."]),
       B.cards([("Space tag", "Walk only. If you are tagged, freeze until someone gives you "
                              "a thumbs-up from a lie-down space away."),
                ("Join the hop", "Hop to a cone, skip home."),
                ("Hoop path", "Three hoops in a line. In, through, out.")]),
       B.ticks("Look what I can do", ["I can stop when I am asked.", "I can hop and skip.",
                                      "I can change speed.",
                                      "I can use a hoop or a mat without rushing."])],
      "1.4  THE MEADOW GAMES")

    unit_close(c, n, "u1_close", [
        "I can stop when I am asked.", "I can hop and skip.", "I can change speed.",
        "I can use a hoop or a mat without rushing."])


def unit_close(c, n, img, rows, closing=None):
    name, ground, _ = UNITS[n]
    c(hl(n), hr(n), f"UNIT {n} · HOW DID IT GO?", "How did it go?",
      [B.lead("Colour one circle in each row. Green means yes, yellow means nearly, and red "
              "means not yet. Not yet is a fine answer: it just means you have more to "
              "do."),
       B.traffic(rows),
       B.plate(img, None, flex=True, minh=150, maxh=260),
       B.para(closing or "Which page in this unit did you enjoy most? Turn back to it and "
                         "show someone why.", size=11.0, pitch=14.6, after=0)],
      f"UNIT {n} · HOW DID IT GO?", (f"Unit {n} · How did it go?", 2))


def unit_2(c, op, toc, pages):
    n = 2
    op(n, "This ground is about words, watching, and a rule you can say out loud.",
       "Willow sees the jump. Then she says what the body did.",
       ("Picture 2.0", "Willow on the hedge post. Bramble jumps. One of them is moving. "
                       "The other one is working too."))

    c(hl(n), hr(n), _k(n, 1), TOPICS[2][0],
      [B.plate("u2_p21", cap("Picture 2.1", "Willow points at a jumping hare. She is naming "
                                            "the movement, not guessing."), flex=True,
               minh=200, maxh=330),
       B.today("Today you will", ["use simple words for a movement",
                                 "watch one thing and say what you saw",
                                 "name what good looks like today",
                                 "follow one rule in a small game"]),
       B.panel("plain", "The kit you need", ["A partner, and a list of words on the board: "
                                             "walk, run, hop, jump, skip, stop, roll."],
               icon="kit")],
      "2.1  WORDS FOR A BODY", ("2.1  Words for a body", 2))

    c(hl(n), hr(n), _k(n, 1, "NAMING WHAT YOU SAW"), "Naming what you saw",
      [B.para("A movement word is a name for what a body did. Jump is not the same as hop. "
              "If you use the wrong word, the watcher cannot help you."),
       B.panel("tint", "Move it", ["The teacher says a word. You do it for five seconds."],
               icon="move"),
       B.watch(["Willow says: \u201cSorrel jumped. Two feet left the grass. Two feet came "
                "back.\u201d That is a description, not a score."], "ch_willow"),
       B.steps("Try it", ["Watch your partner do one movement. Write or tick the word.",
                          "Swap. Do they agree with your word?",
                          "Draw the movement you named."]),
       B.drawbox("THE MOVEMENT I SAW", height=54),
       qr("supermovers_all", "Watch, then name it",
          "Watch a movement routine, then name every movement you saw.")],
      "2.1  NAMING WHAT YOU SAW")

    c(hl(n), hr(n), _k(n, 2), TOPICS[2][1],
      [B.plate("u2_p22", cap("Picture 2.2", "Willow watches from the post. Bramble jumps on "
                                            "the meadow. Look at Willow's still body."),
               flex=True, minh=180, maxh=250),
       B.para("A watcher looks at one thing: feet, or arms, or the landing. Not the whole "
              "body at once."),
       B.panel("plain", "The kit you need", ["Pairs. One mover, one watcher. Swap every "
                                             "three goes."], icon="kit"),
       B.note("Feet together at take-off. Soft knees at landing. He looked at the grass, "
              "not at me.", who="WILLOW'S NOTES"),
       B.steps("Try it", ["Watch three jumps. Say one true sentence each time."])],
      "2.2  WATCH, THEN COPY", ("2.2  Watch, then copy", 2))

    c(hl(n), hr(n), _k(n, 3), TOPICS[2][2],
      [B.plate("u2_p23", cap("Picture 2.3", "Pip lands a jump with bent knees and arms out. "
                                            "That landing is the criterion for this page."),
               flex=True, minh=180, maxh=250),
       B.para("A criterion is a picture of good, for today. For a Year 1 jump, good is: "
              "take off on two feet, land on two feet, knees a little bent, still at the "
              "end."),
       B.table(["Check", "Go 1", "Go 2", "Go 3"],
               [["Two feet off", "", "", ""], ["Two feet land", "", "", ""],
                ["Knees bent", "", "", ""], ["Still at the end", "", "", ""]],
               widths=[0.46, 0.18, 0.18, 0.18]),
       B.steps("Try it", ["Jump. Check the four things. Colour the ones you did.",
                          "Copy the jump you liked. Keep the same one thing.",
                          "Tick: I watched before I copied."]),
       B.ticks("Tick what is true", ["I watched first."])],
      "2.3  WHAT GOOD LOOKS LIKE", ("2.3  What good looks like", 2))

    c(hl(n), hr(n), _k(n, 4), TOPICS[2][3],
      [B.plate("u2_p24", cap("Picture 2.4", "Three friends wait behind a chalk line. The "
                                            "hoop is ahead. Nobody has crossed the line "
                                            "yet."), flex=True, minh=180, maxh=250),
       B.para("A rule is an agreement. In this game the rule is: wait behind the line until "
              "your name is called."),
       B.panel("green", "Safety first", ["Land on the mat if the floor is hard. Do not "
                                         "bounce straight into another jump."],
               icon="safety"),
       B.steps("Try it", ["Circle the go that was your best."])],
      "2.4  A SIMPLE RULE", ("2.4  A simple rule", 2))

    c(hl(n), hr(n), _k(n, 4, "WATCHER'S DAY"), "Watcher's day",
      [B.lead("A tactic is a small plan inside the rule. Walking to the hoop is safer than "
              "running, because the line is close."),
       B.para("Spend the lesson as mover and watcher, half and half."),
       B.panel("tint", "Play together", ["Call and go. Wait behind the line. When you hear "
                                         "your name, walk to the hoop, stand in it, and "
                                         "walk back. If you go early, you just walk back "
                                         "and wait again. Nobody is out."], icon="play"),
       B.panel("plain", "Think about it", ["Why does the line help? Write one word or draw "
                                           "the line."], icon="think"),
       B.drawbox("THE LINE HELPS BECAUSE", height=54),
       B.ticks("Look what I can do", ["I can name a movement with the right word.",
                                      "I can watch one thing.",
                                      "I can say what good looks like today.",
                                      "I can wait behind a line."])],
      "2.4  WATCHER'S DAY")

    unit_close(c, n, "u2_close", [
        "I can name a movement with the right word.", "I can watch one thing.",
        "I can say what good looks like today.", "I can wait behind a line."])


def unit_3(c, op, toc, pages):
    n = 3
    op(n, "This ground asks for a movement nobody showed you first.",
       "A ribbon, a hoop, a mood. The answer is a body.",
       ("Picture 3.0", "The Dance Ring. Sorrel moves with a ribbon. Willow watches the "
                       "shape, not the score."))

    c(hl(n), hr(n), _k(n, 1), TOPICS[3][0],
      [B.plate("u3_p31", cap("Picture 3.1", "Tuft makes a wide star. Sorrel makes a tall "
                                            "thin shape. Two answers to the same request: "
                                            "make a shape."), flex=True, minh=200, maxh=330),
       B.today("Today you will", ["make a new body shape",
                                 "let apparatus suggest a movement",
                                 "answer a task with a body",
                                 "move like a mood or the weather"]),
       B.panel("tint", "Move it", ["Shake hands, shake feet, make a tiny ball shape, then a "
                                   "wide shape."], icon="move")],
      "3.1  NEW SHAPES", ("3.1  New shapes", 2))

    c(hl(n), hr(n), _k(n, 1, "SHAPES YOU INVENT"), "Shapes you invent",
      [B.para("A shape is how the body fills the space: wide, tall, small, twisted. There "
              "is no single right shape."),
       B.steps("Try it", ["Make wide, tall, small, twisted. Hold each for a count of three.",
                          "Invent a fifth shape. Draw it.",
                          "Show it to a partner. Can they copy it?"],
               extra="MY FIFTH SHAPE"),
       B.spot("sp_shapes", 168),
       B.duo([("ch_tuft", "WIDE", "arms and legs spread like a star"),
              ("ch_sorrel", "TALL", "stretched right up on tiptoe")])],
      "3.1  SHAPES YOU INVENT")

    c(hl(n), hr(n), _k(n, 2), TOPICS[3][1],
      [B.plate("u3_p32", cap("Picture 3.2", "A hoop on the grass like a river. Rowan steps "
                                            "in and out. The hoop suggested the game."),
               flex=True, minh=180, maxh=250),
       B.para("The kit is not only for the use printed on the box. A hoop can be a river, a "
              "nest, a window, a cave."),
       B.panel("plain", "The kit you need", ["One hoop between two children."], icon="kit"),
       B.steps("Try it", ["Name three things your hoop could be. Try two of them.",
                          "Swap hoops with another pair. Does the new hoop suggest the same "
                          "ideas?"]),
       B.panel("green", "Safety first", ["Hoops stay on the floor in this topic, unless the "
                                         "teacher says you may lift them. Never swing a "
                                         "hoop at a head."], icon="safety")],
      "3.2  WHAT THE KIT SUGGESTS", ("3.2  What the kit suggests", 2))

    c(hl(n), hr(n), _k(n, 3), TOPICS[3][2],
      [B.plate("u3_p33", cap("Picture 3.3", "A path of cones, a hoop and a bench. Pip is "
                                            "halfway, choosing the next movement."),
               flex=True, minh=180, maxh=250),
       B.para("A task is a job with a start and an end. The teacher might say: cross the "
              "meadow without using a run. Your body answers."),
       B.steps("Try it", ["Cross without running. Tick what you used.",
                          "Now cross without using the movement you chose first."]),
       B.chips(["walk", "hop", "crawl", "skip"]),
       B.panel("warn", "Challenge", ["The path must include one hoop and one change of "
                                     "level. Show Willow."], icon="challenge")],
      "3.3  ANSWER WITH YOUR BODY", ("3.3  Answer with your body", 2))

    c(hl(n), hr(n), _k(n, 4), TOPICS[3][3],
      [B.plate("u3_p34", cap("Picture 3.4", "Sorrel dances with a ribbon in the Dance Ring. "
                                            "Willow watches the weather in the movement."),
               flex=True, minh=170, maxh=230),
       B.para("Storm is fast and strong. Leaf is light and slow. Rain is little repeated "
              "taps. You choose how your body says that."),
       B.panel("plain", "The kit you need", ["Ribbons or scarves if you have them. Music the "
                                             "teacher has chosen, or a drum."], icon="kit"),
       B.panel("tint", "Play together", ["The teacher names a weather. Everyone moves. When "
                                         "you hear sun, freeze in a shape."], icon="play"),
       qr("cosmic")],
      "3.4  MOVING LIKE WEATHER", ("3.4  Moving like weather", 2))

    c(hl(n), hr(n), _k(n, 4, "SHOW A DANCE"), "Show a dance",
      [B.lead("In twos, make an eight-count dance: two shapes, one kit idea, one weather. "
              "Show it once."),
       B.panel("plain", "Think about it", ["Which weather was hardest to show? Why?"],
               icon="think"),
       B.spot("sp_dance", 172),
       B.ticks("Look what I can do", ["I made a shape nobody showed me.",
                                      "I used kit as more than one thing.",
                                      "I answered a task with my body.",
                                      "I moved like a mood."])],
      "3.4  SHOW A DANCE")

    unit_close(c, n, "u3_close", [
        "I made a shape nobody showed me.", "I used kit as more than one thing.",
        "I answered a task with my body.", "I moved like a mood."])


def unit_4(c, op, toc, pages):
    n = 4
    op(n, "This ground is about joining a group, having a job, and listening before you "
          "move.", "A ball, a circle, a turn. Everybody has work.",
       ("Picture 4.0", "The Team Patch. Six friends in a ring with one ball. Look who is "
                       "waiting."))

    c(hl(n), hr(n), _k(n, 1), TOPICS[4][0],
      [B.plate("u4_p41", cap("Picture 4.1", "A ring on the meadow and a yellow ball. "
                                            "Everybody is in. Nobody is left on the hedge."),
               flex=True, minh=190, maxh=290),
       B.para("Joining in means going to the circle, leaving a space, and staying in the "
              "game when it is not your throw."),
       B.today("Today you will", ["join a group activity",
                                 "know your job and someone else's",
                                 "practise one goal on your own",
                                 "take a turn at leading",
                                 "notice a strength",
                                 "listen, then move"])],
      "4.1  JOINING IN", ("4.1  Joining in", 2))

    c(hl(n), hr(n), _k(n, 2), TOPICS[4][1],
      [B.plate("u4_p42", cap("Picture 4.2", "Rowan throws a spotted ball. Pip catches it "
                                            "with both paws. Two jobs, one ball."),
               flex=True, minh=180, maxh=250),
       B.panel("tint", "Play together", ["Circle roll. Sit in a ring. Roll the ball to the "
                                         "child you name. Say the name first. If the ball "
                                         "leaves the ring, the nearest child fetches it and "
                                         "the game goes on."], icon="play"),
       B.ticks("Tick what you did", ["I sat in the ring.",
                                     "I said a name before I rolled.",
                                     "I fetched the ball without a fuss."]),
       B.duo([("ch_rowan", "THROWER", "sends the ball under-arm"),
              ("ch_pip", "CATCHER", "two paws, eyes on the ball")])],
      "4.2  THROWER, CATCHER, COLLECTOR", ("4.2  Thrower, catcher, collector", 2))

    c(hl(n), hr(n), _k(n, 3), TOPICS[4][2],
      [B.para("The thrower sends. The catcher receives. The collector picks up what is "
              "missed. Swap every five throws."),
       B.para("A goal is one thing you will try for the next ten throws. Not \u201cbe "
              "better\u201d. Something a watcher can see: catch with two hands, or throw to "
              "the chest."),
       B.para("Keep the same ball and the same three jobs. The new work is the goal you "
              "write down, then watch."),
       B.panel("plain", "The kit you need", ["One beanbag or a soft ball between three: "
                                             "thrower, catcher, collector."], icon="kit"),
       B.panel("green", "Safety first", ["Under-arm throws in this topic. No ball at a "
                                         "face. If it hurts, stop and tell an adult."],
               icon="safety"),
       B.steps("Try it", ["Five throws each job.",
                          "Tick the job you want to practise next week.",
                          "Write your goal in five words or fewer."],
               tail=["thrower", "catcher", "collector"], extra="MY GOAL IN FIVE WORDS")],
      "4.3  YOUR OWN GOAL", ("4.3  Your own goal", 2))

    c(hl(n), hr(n), _k(n, 4), TOPICS[4][3],
      [B.plate("u4_p44", cap("Picture 4.4", "Sorrel leads. Tuft, Pip and Rowan copy the hop. "
                                            "The leader is a pupil, not a coach."),
               flex=True, minh=180, maxh=250),
       B.para("Leading in Year 1 is showing one movement and waiting while the line copies. "
              "Then you go to the back."),
       B.panel("tint", "Play together", ["Follow me. The leader chooses walk, hop or skip. "
                                         "After the line reaches a cone, the leader goes to "
                                         "the back and the next child leads."], icon="play"),
       B.steps("Try it", ["Ten throws at that goal. A partner tallies yes or no.",
                          "Did the goal get easier? Circle: yes / not yet / I changed it."]),
       B.chips(["yes", "not yet", "I changed it"])],
      "4.4  A TURN AT LEADING", ("4.4  A turn at leading", 2))

    c(hl(n), hr(n), _k(n, 5), TOPICS[4][4],
      [B.para("Different bodies are good at different things today. Pip is quick. Bramble is "
              "steady. Tuft is careful. None of those is a rank."),
       B.panel("green", "Safety first", ["The leader looks where they are going, not only at "
                                         "the line behind."], icon="safety"),
       B.steps("Try it", ["Name one thing you did well today.",
                          "Name one thing a partner did well. Tell them.",
                          "Name one thing you will try next lesson."],
               extra="NEXT TIME I WILL TRY"),
       B.spot("sp_strong", 168)],
      "4.5  WHAT I CAN DO", ("4.5  What I can do", 2))

    c(hl(n), hr(n), _k(n, 6), TOPICS[4][5],
      [B.plate("u4_p46", cap("Picture 4.6", "Pip's ears are up. Bramble is speaking. Then Pip "
                                            "hops. The listen comes first."), flex=True,
               minh=180, maxh=250),
       B.panel("tint", "Play together", ["Listen and go. Freeze. The teacher gives one "
                                         "instruction. Move only when the instruction is "
                                         "finished. If you go early, walk back and wait."],
               icon="play"),
       B.ticks("Look what I can do", ["I joined the ring.", "I knew my job.",
                                      "I had a goal I could see.", "I led once.",
                                      "I said something kind about a partner."])],
      "4.6  LISTEN, THEN MOVE", ("4.6  Listen, then move", 2))

    c(hl(n), hr(n), _k(n, 6, "THE MINI MATCH"), "The mini match",
      [B.lead("A four-minute mini game: circle roll, then three jobs with a beanbag. Swap "
              "jobs when the bell goes. No scores against each other. The score is how many "
              "kind waits you noticed."),
       B.cards([("Job 1 · Thrower", "Send the beanbag under-arm to the catcher's chest."),
                ("Job 2 · Catcher", "Two paws, eyes on the beanbag, feet still."),
                ("Job 3 · Collector", "Fetch what is missed, then back to the ring.")],
               numbered=False),
       B.ticks("Tick what you did", ["I waited until the instruction ended."]),
       B.spot("sp_match", 158),
       qr("gonoodle")],
      "4.6  THE MINI MATCH")

    unit_close(c, n, "u4_close", [
        "I joined the ring.", "I knew my job.", "I had a goal I could see.", "I led once.",
        "I said something kind about a partner."])


def unit_5(c, op, toc, pages):
    n = 5
    op(n, "This ground is about sharing, carrying, fair play, asking for help, and kind "
          "words.", "Two bodies, one mat. The kit is everybody's.",
       ("Picture 5.0", "Bramble and Pip carry a mat together. Look at both pairs of hands."))

    c(hl(n), hr(n), _k(n, 1), TOPICS[5][0],
      [B.para("Sharing is using the same kit without grabbing. Taking turns is waiting, "
              "then going, then letting the next child go."),
       B.today("Today you will", ["share space and kit, and take turns",
                                 "carry and put down equipment safely",
                                 "play fairly",
                                 "ask for help at the right moment",
                                 "give a kind, useful word"]),
       B.panel("tint", "Play together", ["One hoop, two children. One minute in the hoop, "
                                         "one minute watching. Swap when the teacher claps. "
                                         "If you both want it, the watcher goes next."],
               icon="play"),
       B.ticks("Tick what you did", ["I waited.", "I went.",
                                     "I let the next child go."]),
       B.spot("sp_share", 168)],
      "5.1  SHARE AND TAKE TURNS", ("5.1  Share and take turns", 2))

    c(hl(n), hr(n), _k(n, 2), TOPICS[5][1],
      [B.plate("u5_p52", cap("Picture 5.2", "Two friends carry one mat. The weight is "
                                            "shared. The mat is whole in the picture."),
               flex=True, minh=180, maxh=250),
       B.panel("plain", "The kit you need", ["Mats, hoops, cones. An adult names who carries "
                                             "with whom."], icon="kit"),
       B.panel("green", "Safety first", ["Two children to a mat. Walk, do not run. Put the "
                                         "mat down together. Fingers stay out from under "
                                         "the edge. Cones in two hands, against your "
                                         "chest."], icon="safety"),
       B.steps("Try it", ["Carry a mat with a partner to a cone and back.",
                          "Stack hoops. Count them out loud."])],
      "5.2  CARRY KIT SAFELY", ("5.2  Carry kit safely", 2))

    c(hl(n), hr(n), _k(n, 3), TOPICS[5][2],
      [B.plate("u5_p53", cap("Picture 5.3", "Tuft and Rowan with one yellow ball. One waits. "
                                            "One rolls. That wait is fair play."),
               flex=True, minh=180, maxh=250),
       B.para("Fair play in Year 1 is: same turn length, no pushing, tell the truth if the "
              "ball was out, and keep playing after a mistake."),
       B.ticks("Tick if nobody's fingers were under a mat", ["Fingers safe."]),
       B.panel("plain", "Think about it", ["If two children reach the ball together, what "
                                           "is a fair choice?"], icon="think"),
       B.duo([("ch_tuft", "WAITS", "paws in the lap, eyes on the ball"),
              ("ch_rowan", "ROLLS", "one steady under-arm roll")])],
      "5.3  FAIR PLAY", ("5.3  Fair play", 2))

    c(hl(n), hr(n), _k(n, 4), TOPICS[5][3],
      [B.plate("u5_p54", cap("Picture 5.4", "Tuft asks Willow for help beside spilled "
                                            "beanbags. Asking is a skill, not a failure."),
               flex=True, minh=180, maxh=250),
       B.para("Ask when the kit is too heavy, when you cannot see a safe path, or when "
              "something hurts. Ask before you guess with a risky movement."),
       B.panel("tint", "Play together", ["Roll and wait. Five rolls each. If you take an "
                                         "extra turn, you give the next two turns to your "
                                         "partner."], icon="play"),
       B.steps("Try it", ["Practise the sentence: Please can you help me with this mat?",
                          "When would you ask? Tick."],
               tail=["The mat is too heavy."])],
      "5.4  ASK FOR HELP", ("5.4  Ask for help", 2))

    c(hl(n), hr(n), _k(n, 5), TOPICS[5][4],
      [B.plate("u5_p55", cap("Picture 5.5", "Friends clap for Tuft after a jump. Kind words "
                                            "are specific: \u201csoft knees\u201d, not only "
                                            "\u201cgood\u201d."), flex=True, minh=170,
               maxh=230),
       B.para("Kind words name what you actually saw. \u201cSoft knees\u201d helps. "
              "\u201cGood\u201d does not say what to do next time."),
       B.ticks("Two things you can say", ["I feel a pinch in my knee.",
                                          "I want to go first."]),
       B.para("The last box is a want, not a need. The teacher can still help you wait."),
       B.note("Soft knees. You looked at the grass. That landing was still.",
              who="WILLOW'S NOTES"),
       B.steps("Try it", ["Watch a partner. Say one true, kind sentence.",
                          "Write the sentence, or draw the moment."])],
      "5.5  KIND WORDS", ("5.5  Kind words", 2))

    c(hl(n), hr(n), _k(n, 5, "KIT INSPECT"), "Kit inspect",
      [B.lead("Before you leave: mats stacked, hoops counted, water bottles off the floor, "
              "fingers checked."),
       B.ticks("Look what I can do", ["I took turns.",
                                      "I carried kit with a partner.",
                                      "I played fairly.",
                                      "I asked for help when I needed it.",
                                      "I said something kind and true."]),
       B.drawbox("THE KIND SENTENCE", height=54),
       B.spot("sp_kit", 168),
       qr("yst")],
      "5.5  KIT INSPECT")

    unit_close(c, n, "u5_close", [
        "I took turns.", "I carried kit with a partner.", "I played fairly.",
        "I asked for help when I needed it.", "I said something kind and true."])


def unit_6(c, op, toc, pages):
    n = 6
    op(n, "This ground is about what a body does when it works, and what it needs "
          "afterwards.", "A faster heart, a drink of water, a rest in the shade.",
       ("Picture 6.0", "Pip under the oak after a run. Paw on chest, water on the grass. "
                       "Look how still he is now."))

    c(hl(n), hr(n), _k(n, 1), TOPICS[6][0],
      [B.plate("u6_p61", cap("Picture 6.1", "Pip sits under the oak after running. His paw "
                                            "is on his chest. The water bottle is "
                                            "waiting."), flex=True, minh=190, maxh=300),
       B.today("Today you will", ["notice what changes when you move",
                                 "name the body parts doing the work",
                                 "choose an intensity that fits the task",
                                 "stop when you have reached your limit today",
                                 "warm up and cool down",
                                 "choose food and water that help a moving body"]),
       qr("nhs_active", "Why moving matters",
          "What happens inside a body when it moves, from the NHS.")],
      "6.1  WHAT CHANGES WHEN YOU MOVE", ("6.1  What changes when you move", 2))

    c(hl(n), hr(n), _k(n, 1, "A FASTER HEART"), "A faster heart",
      [B.para("When you run, your heart beats faster. You breathe faster. You may feel "
              "warm. Those changes are the body doing its job, not a problem."),
       B.panel("tint", "Move it", ["Sit still. Put a hand on your chest. Then jog on the "
                                   "spot for twenty seconds. Hand on chest again."],
               icon="move"),
       B.panel("didyou", "Did you know?", ["A child's heart beats faster during play because "
                                           "the muscles need more blood. When you rest, the "
                                           "beat slows again. (NHS, physical activity and "
                                           "children.)"], icon="didyou"),
       B.steps("Try it", ["Count \u201cbeats\u201d with a hand on your chest for ten "
                          "seconds, before and after a jog. The number does not have to be "
                          "exact. Did it get faster?",
                          "Draw a still Pip and a running Pip."]),
       B.drawrow(["STILL", "AFTER A JOG"], height=66)],
      "6.1  A FASTER HEART")

    c(hl(n), hr(n), _k(n, 2), TOPICS[6][1],
      [B.plate("u6_p62", cap("Picture 6.2", "Bramble shows the parts that work in a jump: "
                                            "knees, elbows, paws."), flex=True, minh=180,
               maxh=250),
       B.steps("Try it", ["Point to knees, ankles, hips, shoulders, elbows on yourself.",
                          "Which parts work hardest in a jump? Tick two."]),
       B.chips(["knees", "ankles", "ears", "nose"]),
       B.note("Knees and ankles did the spring. Arms helped him balance. Ears did not jump.",
              who="WILLOW'S NOTES")],
      "6.2  NAME THE WORKING PARTS", ("6.2  Name the working parts", 2))

    c(hl(n), hr(n), _k(n, 3), TOPICS[6][2],
      [B.lead("Intensity is how hard the work feels. A walk to a cone is light. A thirty "
              "second run is harder. A lesson needs both."),
       B.steps("Try it", ["Walk a lap. Jog a lap. Walk a lap. Which one could you do for a "
                          "whole lesson?",
                          "Circle how the jog felt: easy / just right / too much today."]),
       B.chips(["easy", "just right", "too much today"]),
       B.spot("sp_pace", 158),
       B.duo([("ch_pip", "LIGHT", "a walk to a cone, easy breathing"),
              ("ch_sorrel", "HARDER", "a thirty second run, quick breathing")])],
      "6.3  HOW HARD IS HARD ENOUGH", ("6.3  How hard is hard enough", 2))

    c(hl(n), hr(n), _k(n, 4), TOPICS[6][3],
      [B.lead("Your limit today is not a score against a friend. It is the moment you need "
              "to rest, drink, or choose a lighter job."),
       B.panel("green", "Safety first", ["Harder is not always better. If you feel dizzy or "
                                         "a sharp pain, stop and tell an adult."],
               icon="safety"),
       B.steps("Try it", ["After a run, sit until your breathing feels easy again.",
                          "Tick the honest sentence."],
               tail=["I could have done one more go.", "I needed a rest.",
                     "Something hurt, so I stopped."]),
       B.spot("sp_rest", 168)],
      "6.4  KNOWING YOUR LIMIT TODAY", ("6.4  Knowing your limit today", 2))

    c(hl(n), hr(n), _k(n, 5), TOPICS[6][4],
      [B.plate("u6_p65", cap("Picture 6.5", "The six friends stretch arms up before a game. "
                                            "A warm body is ready. A cold body is not."),
               flex=True, minh=170, maxh=230),
       B.para("A warm-up wakes the body: walk, gentle jumps, shoulder rolls. A cool-down "
              "slows it: walk, stretch, sit, water."),
       B.para("All three can be right on different days."),
       B.steps("Try it", ["Lead a thirty-second warm-up for a partner.",
                          "After the game, walk one lap and sit. Drink water."])],
      "6.5  BEFORE, AND AFTERWARDS", ("6.5  Before, and afterwards", 2))

    c(hl(n), hr(n), _k(n, 6), TOPICS[6][5],
      [B.plate("u6_p66", cap("Picture 6.6", "A picnic under the oak: fruit, bread, cheese, "
                                            "carrot, water. Look at the water bottle."),
               flex=True, minh=170, maxh=230),
       B.panel("didyou", "Did you know?", ["Warming up and slowing down help the body go "
                                           "from rest to play and back again. You do not "
                                           "skip them because the game looks more fun. "
                                           "(NHS, activity for children.)"], icon="didyou"),
       B.panel("didyou", "Did you know?", ["Children need regular drinks of water, "
                                           "especially when they have been running about. "
                                           "Fruit and vegetables are part of everyday food. "
                                           "(NHS, drinks and \u201c5 a day\u201d.)"],
               icon="didyou"),
       qr("nhs_five")],
      "6.6  FOOD AND WATER FOR A MOVING BODY", ("6.6  Food and water for a moving body", 2))

    c(hl(n), hr(n), _k(n, 6, "HEALTHY ME"), "Healthy me",
      [B.lead("A last circuit: warm up, a one-minute jog, a rest under the oak, water, a "
              "kind sentence to a partner, kit away."),
       B.steps("Try it", ["Circle the drink for a PE lesson: water / a fizzy drink.",
                          "Draw one fruit you might eat after the lesson.",
                          "Why does a moving body need water? One short sentence."],
               extra="AFTER PE"),
       B.panel("green", "Safety first", ["Water at the side of the hall, not on the running "
                                         "line. Tell an adult if you feel too hot."],
               icon="safety"),
       B.ticks("Look what I can do", ["I felt my heart change.",
                                      "I named two body parts that worked.",
                                      "I chose a pace I could keep.",
                                      "I rested when I needed to.",
                                      "I warmed up and cooled down.",
                                      "I chose water."]),
       qr("nhs_food")],
      "6.6  HEALTHY ME")

    unit_close(c, n, "u6_close", [
        "I felt my heart change.", "I named two body parts that worked.",
        "I chose a pace I could keep.", "I rested when I needed to.",
        "I warmed up and cooled down.", "I chose water."])
