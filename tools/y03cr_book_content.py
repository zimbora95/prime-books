#!/usr/bin/env python3
"""Content for the re-cut of y03-computing-and-robotics onto Standard A-2.3.

Every sentence below is the teacher's own, taken from the published 32-page
sample (public/library/y03-computing-and-robotics/book.pdf) and from its
markdown companion. Nothing is deleted, reworded or moved out of its unit: the
book is re-typeset at US Letter with the house furniture, the Year 3 reading
ladder and one colour per unit. Page breaks move because the page is a
different size and the type is a different size; the reading order does not.

Marker glyphs in the source (the ring arrow, the star, the square, the dot) are
not glyphs in the house fonts, so each becomes the panel it marked, with the
engine's drawn icon doing the work. That is the one systematic addition.
"""
from __future__ import annotations

import pb_engine as E
from pb_engine import B

FRONT = "COMPUTING & ROBOTICS  YEAR 3"
UNIT1 = "UNIT 1  COMPUTATIONAL THINKING AND PROGRAMMING"
HR_FRONT = "Computing & Robotics · Year 3"

# ---------------------------------------------------------------- contents ---
CONTENTS = [
    {"kind": "rows", "items": [("Welcome to the bench", 4), ("Who you will meet", 5),
                               ("How to use this book", 6), ("How to work at this bench", 7),
                               ("Getting set up", 8), ("For teachers", 9)]},
    {"kind": "unit", "n": 1, "page": 10,
     "name": "Computational thinking and programming",
     "sub": "Think it, say it, try it, fix it. Nobody at this bench picks up a tool "
            "before the plan is pinned to the board.",
     "items": [("1.1  Learn what an algorithm is", 13),
               ("1.2  Use an algorithm", 17),
               ("1.3  Learn what an error is", 22),
               ("1.4  Find an error in algorithm", 26),
               ("Show the bench: the morning routine", 30),
               ("How did it go?", 31)]},
    {"kind": "unit", "n": 2, "page": "–", "name": "Coding and programming",
     "sub": "In preparation.", "items": []},
    {"kind": "unit", "n": 3, "page": "–", "name": "Managing data",
     "sub": "In preparation.", "items": []},
    {"kind": "unit", "n": 4, "page": "–", "name": "Networks and digital communication",
     "sub": "In preparation.", "items": []},
    {"kind": "unit", "n": 5, "page": "–", "name": "Computer systems",
     "sub": "In preparation.", "items": []},
    {"kind": "rows", "items": [("Word list", 32), ("For teachers", 33),
                               ("Answers", 34), ("Sources and references", 37)]},
]
CONTENTS_LEAD = ("Units 2 to 5 are in preparation and are not in this sample.")

# ------------------------------------------------------------------- pages ---
# Each page: dict(kind, unit, folio, hl, hr, kick, title, blocks)
# `unit` 0 = house ochre (front and back matter), 1..5 = the unit colour rung.


def c(unit, folio, hl, hr, kick, title, blocks):
    return dict(kind="page", unit=unit, folio=folio, hl=hl, hr=hr, kick=kick,
                title=title, blocks=blocks)


def front(folio, kick, title, blocks):
    return c(0, folio, FRONT, HR_FRONT, kick, title, blocks)


def unit1(folio, kick, title, blocks):
    return c(1, folio, UNIT1, HR_FRONT, kick, title, blocks)


def build_pages():
    pages = []

    # ---------------------------------------------------------- front matter --
    pages.append(dict(kind="toc", num=3, folio=FRONT, unit=0,
                      spec=dict(hl=FRONT, hr=HR_FRONT,
                                kick="COMPUTING & ROBOTICS · YEAR 3",
                                title="Contents",
                                blocks=[B.toc(CONTENTS, lead=CONTENTS_LEAD)])))

    pages.append(front(FRONT, "WELCOME", "Welcome to the bench", [
        B.lead("Last year you walked a path and learned to put steps in order."),
        B.subhead("This year you sit down at a bench."),
        B.para("A bench is where things get taken apart. On this bench there is a "
               "robot called Rebite who is not finished, a wall of tools that all "
               "have their own hook, and a planning board where every job is written "
               "down before anybody picks anything up."),
        B.para("You are the new apprentice. Your work this year is to write "
               "instructions so precise that a machine cannot get them wrong, and "
               "then to find the fault when it does anyway."),
        B.para("Because it will. That is not the sad part of computing. That is the "
               "craft."),
        B.panel("tint", "Do you remember?", [
            "You already know how to put steps in order, follow a simple program, "
            "and spot a pattern. Keep all of that. This year you add one word to "
            "everything you do: precise."], icon="didyou"),
    ]))

    pages.append(front(FRONT, "WHO YOU WILL MEET", "Who you will meet", [
        B.lead("Four people work at this bench, and you are one of them."),
        B.cards([("Mestre Raposo",
                  "The keeper of the bench. He rarely gives you the answer. Instead "
                  "he asks \u201cand then what happens?\u201d until you find it yourself. "
                  "His notebook is always open somewhere."),
                 ("Leonor",
                  "The apprentice before you. Quick, curious, and happy to be wrong "
                  "in public, which is why she learns faster than anybody. She tries "
                  "first and checks after.")], numbered=False),
        B.cards([("Rebite",
                  "The bench robot. Half-built at the start of this book and still "
                  "being improved at the end. Does exactly what the instructions say, "
                  "never what you meant."),
                 ("You",
                  "The new apprentice. You get a pencil, a place at the bench, and "
                  "permission to take things apart.")], numbered=False),
    ]))

    pages.append(front(FRONT, "HOW TO USE THIS BOOK", "How to use this book", [
        B.lead("Every topic in this book is built the same way, so you only learn "
               "the furniture once."),
        B.cards([("On the bench today",
                  "A short story from the workshop. Read it first."),
                 ("Warm up",
                  "A quick game, usually standing up, usually without a device."),
                 ("Here is how it works", "The teaching. Deliberately short.")],
                numbered=False),
        B.cards([("Watch me work one out",
                  "Mestre Raposo does one slowly, and says why."),
                 ("Check it a different way",
                  "A second route to the same answer, because one route is a trick."),
                 ("Your turn", "Numbered practice with real room to write.")],
                numbered=False),
        B.cards([("From the notebook",
                  "A true fact off a page of Mestre Raposo's notebook."),
                 ("Find the fault", "Something is broken on purpose. Repair it."),
                 ("One step more", "For when you finish early.")],
                numbered=False),
        B.cards([("Bench challenge", "The hard one. Worth the effort."),
                 ("No screen needed", "This task needs no device at all."),
                 ("Now I can", "Tick these when they are true, not before.")],
                numbered=False),
    ]))

    pages.append(front(FRONT, "HOW TO WORK AT THIS BENCH", "How to work at this bench", [
        B.steps("How to work at this bench", [
            "Read the story, then say the key words out loud.",
            "Read the teaching once, then close the book and say it back in your "
            "own words.",
            "Follow the worked example with a pencil in your hand, not just your "
            "eyes.",
            "Do your turn. Write in the book. It is your book.",
            "When something goes wrong, do not rub it all out. Find the one thing "
            "that is wrong.",
        ]),
        B.panel("tint", "From the notebook", [
            "There is a rule on the wall above this bench, and it is the whole of "
            "Year 3 computing: change one thing, then run it again. Change three "
            "things and you will never know which one mattered."], icon="note"),
    ]))

    pages.append(front(FRONT, "GETTING SET UP", "Getting set up", [
        B.panel("plain", "Open the bench", [
            "You need very little for this book, and for the whole of Unit 1 you "
            "need no device at all.",
            "From Unit 2 onwards you will also need a tablet or a computer with "
            "Scratch, when your teacher opens it."], icon="kit"),
        B.ticks("In your kit", [
            "a pencil, and a rubber you are allowed to use",
            "this book, which you are allowed to write in",
            "a partner, because most tasks here are done out loud with somebody else",
            "squared paper, for when you run out of room",
            "a floor space or a table for grid-mat tasks",
        ]),
        B.panel("warn", "Stop and think", [
            "When you go online later in this book, three rules never change: ask a "
            "trusted adult before you share anything, never give your full name or "
            "your school, and tell an adult straight away if something makes you "
            "uncomfortable. Unit 4 spends a whole topic on this."], icon="safety"),
    ]))

    pages.append(front(FRONT, "FOR TEACHERS", "For teachers", [
        B.panel("plain", "For teachers", [
            "This title is authored in MARKDOWN/ and composed by the engine in "
            "WORKSTATION/_build. The scheme of work is PDF/Input/Edu360 Topic "
            "(edu360.topic) Computing Y3.xlsx, and the five units and 31 topics are "
            "kept verbatim from it. The plan the book is gated against is "
            "MARKDOWN/06-SCHEME-MAP.md.",
            "Unit 1 is entirely unplugged by design. Pupils who meet precision on "
            "paper first make far fewer guesses when Scratch arrives in Unit 2. The "
            "full curriculum mapping, the assumptions about prior learning, and the "
            "answers are in the back matter."], icon="note"),
    ]))

    # ------------------------------------------------------------- unit one ---
    pages.append(dict(kind="opener", num=10, spec=dict(
        kicker="UNIT 1 · THE PLANNING BOARD", num=1,
        title="Computational thinking and programming",
        ground="Think it, say it, try it, fix it.",
        blurb="Nobody at this bench picks up a tool before the plan is pinned to "
              "the board.",
        narrative="",
        topics=[],
        img="unit1_opener",
        caption=("On the bench",
                 "The planning board, the wall of tools and Rebite, half-built, "
                 "waiting for the plan to be pinned up."))))

    pages.append(unit1(UNIT1, "UNIT 1 · WHAT THIS UNIT ASKS OF YOU",
                       "What this unit asks of you", [
        B.cards([("Think it", "What must happen, and in what order?"),
                 ("Say it", "Write the steps so precisely that nobody can guess "
                            "wrong."),
                 ("Try it & fix it",
                  "Run the steps, find the fault, change one thing.")], numbered=False),
        B.ticks("By the end you will", [
            "say what an algorithm is, in your own words",
            "follow an algorithm exactly, even when you can see a shortcut",
            "write an algorithm precise enough for somebody else to follow",
            "explain what an error is, and why order matters",
            "find the one broken step in an algorithm and repair it",
        ]),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · ON THE BENCH TODAY", "On the bench today", [
        B.panel("tint", "On the bench today", [
            "Mestre Raposo has taped a long strip of paper to the planning board. "
            "On it, in his neat handwriting, are eleven steps for building Rebite's "
            "left arm.",
            "Leonor reads step one, picks up the wrong screwdriver, and stops. She "
            "looks again. Step one does not say which screwdriver.",
            "\u201cThen step one is not finished,\u201d says Mestre Raposo, and hands her a "
            "pencil. \u201cMend the step, not the arm.\u201d"], icon="watch"),
        B.panel("plain", "Warm up", [
            "Stand up. Give your partner three instructions to get from their chair "
            "to the classroom door, and nothing more. Your partner must do exactly "
            "what you say, no guessing.",
            "Most partners end up facing a wall. That is the lesson, not a failure."],
            icon="play"),
        B.plate("pic_1_1", ("Picture 1.1",
                            "Nothing is built at this bench until the plan on the "
                            "board is precise."), flex=True, minh=170, maxh=250),
    ]))

    # ---------------------------------------------------------- topic 1.1 -----
    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.1  LEARN WHAT AN ALGORITHM IS",
                       "Learn what an algorithm is", [
        B.subhead("Here is how it works"),
        B.lead("An algorithm is a set of steps, in order, that gets a job done."),
        B.para("It is not a computer word. It is a plan word. When you clean a "
               "paintbrush, feed a cat or catch tram 28 in Lisbon, you follow steps "
               "in order. Write those steps down and you have written an algorithm."),
        B.cards([("It has steps", "not a vague idea"),
                 ("The steps are in order", "and the order matters"),
                 ("Each step is precise",
                  "so two different people do the same thing")], numbered=True),
        B.panel("tint", "Do you remember?", [
            "In Year 2 you put steps in order and ran them. This year you make the "
            "steps so precise that no one has to guess what you meant."],
            icon="didyou"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.1  LEARN WHAT AN ALGORITHM IS",
                       "The steps have to be precise", [
        B.steps("Watch me work one out", [
            "Hold the pencil in your writing hand.",
            "Put the pencil point into the sharpener hole.",
            "Turn the pencil eight times.",
            "Take the pencil out and look at the point.",
            "If the point is still flat, turn it four more times.",
        ], tail=None, icon="watch"),
        B.plate("pic_1_2", ("Picture 1.2",
                            "Five precise steps, and one sharp pencil. Step 3 says "
                            "how many turns, not \u201ca few\u201d."), height=260),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.1  LEARN WHAT AN ALGORITHM IS",
                       "Why eight turns, not a few", [
        B.para("Now read step 3 again. It does not say \u201cturn it a bit\u201d. It says "
               "eight times. That is what makes it precise, and precision is why "
               "somebody else can follow it and get your result."),
        B.panel("plain", "Check it a different way", [
            "Swap the order of steps 2 and 3, then read it again: turn the pencil "
            "eight times, then put it into the sharpener. Same five steps, same "
            "words, and now the pencil is not sharp.",
            "An algorithm is its steps and their order. Change one, and you have "
            "changed the plan."], icon="play"),
        B.panel("tint", "From the notebook", [
            "The word algorithm comes from a person's name. Muhammad ibn Musa "
            "al-Khwarizmi worked at the House of Wisdom in Baghdad around the year "
            "820, and he wrote careful step-by-step methods for working with "
            "numbers. When his book was translated into Latin, his name was written "
            "Algoritmi, and that is the word we still use today.",
            "He did not invent the idea of following steps in order. People had "
            "been doing that for thousands of years. His name simply stuck to it."],
            icon="note"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.1  LEARN WHAT AN ALGORITHM IS",
                       "Your turn", [
        B.panel("plain", "No screen needed", [
            "You have not touched a device yet in this unit, and you will not need "
            "one until Unit 2. Computational thinking happens in your head, on "
            "paper and out loud, long before it happens on a screen."], icon="look"),
        B.steps("Your turn", [
            "Write an algorithm of four steps for washing your hands. Somebody else "
            "must be able to follow it without asking you a single question.",
            "Read a classmate's hand-washing algorithm out loud and do exactly what "
            "it says.",
        ], extra="WHERE DID YOU HAVE TO GUESS?  WRITE THE STEP NUMBER HERE",
            icon="try"),
        B.drawbox("Write your four steps here", height=150),
    ]))

    # ---------------------------------------------------------- topic 1.2 -----
    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.2  USE AN ALGORITHM",
                       "Use an algorithm", [
        B.subhead("Here is how it works"),
        B.lead("Writing an algorithm is half the work. Using one means following it "
               "exactly, in order, without adding anything of your own."),
        B.para("That is harder than it sounds, because your brain wants to be "
               "helpful. A computer is never helpful. It does what the steps say."),
        B.para("Rebite drives on a square grid mat on the bench. Each instruction "
               "moves it one square."),
        B.plate("pic_1_3", ("Picture 1.3",
                            "Rebite waits on the start square. It will not move until "
                            "you say so, and it will move exactly one square for each "
                            "instruction."), flex=True, minh=150, maxh=220),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.2  USE AN ALGORITHM",
                       "Which of these is an algorithm?", [
        B.lead("Which of these is an algorithm? Tick the ones that are."),
        B.para("a. Be tidy."),
        B.para("b. Put the lids on the pens, then put the pens in the pot, then "
               "close the drawer."),
        B.para("c. Draw a house."),
        B.para("d. Fold the paper in half, then in half again, then open it once."),
        B.note("Tick the ones that are algorithms, and be ready to say why the "
               "others are not.", who="Mestre Raposo"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.2  USE AN ALGORITHM",
                       "Leonor runs five arrows", [
        B.steps("Watch me work one out", [
            "Leonor runs the five arrows below, starting on the square marked S at "
            "the bottom left. She says each one out loud and moves one square only.",
        ], icon="watch"),
        B.table(["STEP", "INSTRUCTION", "WHERE REBITE IS NOW"], [
            ["1", "up", "second row from the bottom, left column"],
            ["2", "up", "third row, left column"],
            ["3", "right", "third row, second column"],
            ["4", "right", "third row, third column"],
            ["5", "up", "top row, third column, on the flag"],
        ], widths=[0.14, 0.22, 0.64]),
        B.para("Five instructions, five squares, and Rebite lands on the flag. "
               "Notice that Leonor never moved two squares for one arrow, even when "
               "she could see where the flag was."),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.2  USE AN ALGORITHM",
                       "Run it backwards to check it", [
        B.panel("plain", "Check it a different way", [
            "Read the five arrows backwards from the flag: down, left, left, down, "
            "down. You should arrive back at S.",
            "If running an algorithm forwards and backwards does not agree, one of "
            "the two runs is wrong. That is a check you can do on any route, on any "
            "mat, without asking anybody."], icon="play"),
        B.steps("Your turn", [
            "Write the arrows that take Rebite from S to the flag going along the "
            "bottom row first, then up the right-hand side. Use the boxes.",
            "The dark square is a broken tile and Rebite may not drive on it. Write "
            "a five-arrow route that avoids it, or write not possible and explain "
            "why in one sentence.",
            "Your partner writes six arrows in secret and reads them to you one at "
            "a time. Put your finger on S and follow. Where do you land?",
        ], extra="DRAW THE ROUTE, ONE ARROW IN EACH BOX", icon="try"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.2  USE AN ALGORITHM",
                       "One step more", [
        B.panel("plain", "One step more", [
            "Write a route for Rebite that visits the flag and finishes back on S. "
            "How many arrows does the shortest one need? Prove it by drawing the "
            "route."], icon="challenge"),
        B.drawrow(["Route one", "Route two"], height=190),
    ]))

    # ---------------------------------------------------------- topic 1.3 -----
    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.3  LEARN WHAT AN ERROR IS",
                       "Learn what an error is", [
        B.subhead("Here is how it works"),
        B.lead("An error is a step that does not do what you wanted. Programmers "
               "also call an error a bug."),
        B.para("An error is not a scolding and it is not a mess. It is information. "
               "It tells you exactly where your thinking and your instructions "
               "stopped agreeing with each other."),
        B.para("Errors at this bench come in three kinds, and naming the kind is "
               "most of the repair:"),
        B.table(["KIND OF ERROR", "WHAT IT LOOKS LIKE", "EXAMPLE"], [
            ["A step is missing", "the job stops early, or something is left undone",
             "you never said \u201cclose the lid\u201d"],
            ["A step is in the wrong order", "every step is there, and the result is "
                                             "still wrong",
             "you turned the pencil before putting it in the sharpener"],
            ["A step is not precise", "two people follow it and get two different "
                                      "results", "\u201cmove a bit\u201d"],
        ], widths=[0.28, 0.36, 0.36]),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.3  LEARN WHAT AN ERROR IS",
                       "Rebite draws a square", [
        B.steps("Watch me work one out", [
            "Rebite must draw a square. Leonor writes: forward 4, turn right, "
            "forward 4, turn right, forward 4, turn right, forward 4.",
        ], icon="watch"),
        B.para("Rebite draws two sides, then drives straight on and off the edge of "
               "the mat."),
        B.para("Mestre Raposo does not rewrite the whole thing. He asks one "
               "question: \u201cwhich kind of error?\u201d Step 4 should have been turn "
               "right, so a step is in the wrong order, or rather the wrong step is "
               "in that place. One word changes, and the square closes."),
        B.para("Naming the kind of error tells you where to look. Rewriting "
               "everything tells you nothing."),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.3  LEARN WHAT AN ERROR IS",
                       "Find the fault: a jam sandwich", [
        B.lead("Here is an algorithm for making a jam sandwich. One step is in the "
               "wrong place."),
        B.para("Write the number of the step that is in the wrong place:"),
        B.drawbox("Step number", lines=1, height=46),
        B.para("Now write the four steps in the right order."),
        B.steps("The jam sandwich", [
            "Take two slices of bread.",
            "Spread the jam on one slice.",
            "Put the two slices together.",
            "Open the jam jar.",
        ], extra="WRITE THE FOUR STEPS IN THE RIGHT ORDER", icon="try"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.3  LEARN WHAT AN ERROR IS",
                       "The first computer bug", [
        B.plate("pic_1_4", ("Picture 1.4",
                            "A bug in the logbook. The word was already in use for "
                            "a fault, which is why the joke was worth taping down."),
                height=230),
        B.panel("tint", "From the notebook", [
            "The first computer bug that anybody kept was a real insect. On 9 "
            "September 1947, engineers testing the Harvard Mark II computer found "
            "a moth caught in one of its switches. They taped the moth into the "
            "machine's logbook and wrote \u201cfirst actual case of bug being found\u201d. "
            "That page is kept in a museum in Washington today.",
            "Here is the joke: engineers were already calling a fault a bug long "
            "before 1947. That is why finding a real one was funny enough to tape "
            "down."], icon="note"),
    ]))

    # ---------------------------------------------------------- topic 1.4 -----
    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.4  FIND AN ERROR IN ALGORITHM",
                       "Find an error in algorithm", [
        B.subhead("Here is how it works"),
        B.lead("Finding an error has its own algorithm, and it is the most useful "
               "one in this book."),
        B.steps("The five steps of finding an error", [
            "Read the steps out loud, one at a time.",
            "Predict what each step will do, before you run it.",
            "Run the steps and watch for the first place the real result and your "
            "prediction disagree.",
            "Change one thing only.",
            "Run it again and compare.",
        ], icon="try"),
        B.para("Step 4 is the one everybody breaks. If you change three things and "
               "the fault disappears, you do not know which change repaired it, so "
               "you have not learnt anything and it will come back."),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.4  FIND AN ERROR IN ALGORITHM",
                       "Leonor repairs a route", [
        B.steps("Watch me work one out", [
            "Rebite must fetch a bolt from the far corner of the mat. Leonor's "
            "route sends it into the broken tile. She works through the five steps.",
        ], icon="watch"),
        B.table(["STEP OF THE REPAIR", "WHAT LEONOR DOES", "WHAT SHE FINDS"], [
            ["Read", "says the six arrows out loud", "all six are readable"],
            ["Predict", "says where Rebite should be after each arrow",
             "after arrow 3 it should be one square left of the broken tile"],
            ["Run", "moves Rebite one square per arrow",
             "after arrow 3 it is on the broken tile"],
            ["Change one thing", "changes arrow 3 from right to up",
             "nothing else is touched"],
            ["Run again", "runs all six from the start", "Rebite reaches the bolt"],
        ], widths=[0.24, 0.36, 0.40]),
        B.para("The fault was in arrow 3. Arrows 4, 5 and 6 were never broken, and "
               "Leonor never rewrote them."),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.4  FIND AN ERROR IN ALGORITHM",
                       "Check it, and the bench challenge", [
        B.panel("plain", "Check it a different way", [
            "Ask a classmate to run your repaired algorithm without telling them "
            "where the fault was. If they reach the same result you did, the repair "
            "holds. If they do not, your steps are still not precise enough for "
            "somebody else, which is the only test that counts."], icon="play"),
        B.steps("Bench challenge", [
            "Write a six-step algorithm with one error hidden in it, on purpose, "
            "for a partner to find. You must be able to say which kind of error you "
            "hid.",
            "Swap. Your partner must name the kind of error, name the step number, "
            "and repair it by changing one thing only.",
            "Then run the repaired algorithm together and check it does the job.",
        ], icon="challenge"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · TOPIC 1.4  FIND AN ERROR IN ALGORITHM",
                       "Your turn", [
        B.steps("Your turn", [
            "Here is a route for Rebite: up, up, right, right, right, up. The mat "
            "is four squares across. Predict where Rebite finishes. Then run it. "
            "Did your prediction match?",
            "Write, in order, the five steps of finding an error.",
            "Why should you change only one thing at a time? Answer in two "
            "sentences.",
        ], extra="PREDICT FIRST. THEN RUN IT. WRITE WHAT YOU FOUND.", icon="try"),
        B.drawbox("Your answer", height=120),
    ]))

    # ------------------------------------------------------------- project ----
    pages.append(unit1(UNIT1, "UNIT 1 · SHOW THE BENCH", "Show the bench", [
        B.lead("The morning routine, written for a robot."),
        B.para("Rebite is going to run your classroom's morning routine. Your job "
               "is to write it precisely enough that a robot could not get it "
               "wrong."),
        B.table(["WHAT IS BEING MARKED", "GETTING THERE", "DONE WELL"], [
            ["Steps and order", "most steps are there",
             "every step is there and the order is defended"],
            ["Precision", "a partner had to guess once or twice",
             "a partner followed it with no questions"],
            ["Finding the error", "found it with a hint",
             "named the kind, found the step, changed one thing"],
        ], widths=[0.28, 0.32, 0.40]),
        B.steps("Show the bench", [
            "Watch and list. Write down every step of your real morning routine, "
            "from coming through the door to sitting down. Do not tidy it yet.",
            "Put it in order. Number the steps. Two steps that could happen in "
            "either order get the same number, and say why.",
            "Make it precise. Rewrite any step that a partner could follow in two "
            "different ways.",
            "Hide one error. Copy your algorithm out with one error hidden in it, "
            "and label which kind it is on a separate slip.",
            "Swap and repair. Trade with a partner. Find the error, name its kind, "
            "change one thing, and run the repaired routine together.",
        ], icon="challenge"),
    ]))

    pages.append(unit1(UNIT1, "UNIT 1 · HOW DID IT GO?", "How did it go?", [
        B.lead("Tick where you are, honestly. EASY is fine, and ASK AGAIN is a "
               "question, not a mark."),
        B.traffic(["1.1  What an algorithm is",
                   "1.2  Using an algorithm",
                   "1.3  What an error is",
                   "1.4  Finding an error"]),
        B.cards([("Easy", "I did it on my own."),
                 ("Getting there", "I got there with a hint."),
                 ("Ask again", "I want this explained once more.")], numbered=False),
        B.ticks("Now I can", [
            "say what an algorithm is in my own words",
            "follow an algorithm exactly, even when I can see a shortcut",
            "write an algorithm a classmate can follow with no questions",
            "name the three kinds of error",
            "predict, run, and find where the two disagree",
            "repair an algorithm by changing one thing only",
        ]),
    ]))

    # ---------------------------------------------------------- back matter ---
    pages.append(front(FRONT, "WORD LIST", "Word list", [
        B.lead("Every word taught in this sample, with the topic it comes from."),
        B.cards([("algorithm", "a set of steps, in order, that gets a job done (1.1)"),
                 ("bug", "another word for an error (1.3)"),
                 ("error", "a step that does not do what you wanted (1.3)")],
                numbered=False),
        B.cards([("hardware", "the physical parts of a computer you can touch "
                              "(front matter)"),
                 ("instruction", "one thing you tell a machine to do (1.2)"),
                 ("order", "which step comes first, second, third (1.1)")],
                numbered=False),
        B.cards([("precise", "so clear that two people do the same thing (1.1)"),
                 ("predict", "say what will happen before you run it (1.4)"),
                 ("repair", "change one thing so the algorithm works (1.4)")],
                numbered=False),
        B.cards([("run", "carry out the steps, one at a time, in order (1.2)"),
                 ("step", "one instruction in an algorithm (1.1)"),
                 ("unplugged", "a computing task done without any device (1.1)")],
                numbered=False),
    ]))

    pages.append(front(FRONT, "FOR TEACHERS  UNIT 1", "For teachers: Unit 1", [
        B.panel("plain", "For teachers", [
            "Unit 1 is deliberately unplugged from beginning to end. Pupils who "
            "meet precision on paper and out loud first make far fewer guesses when "
            "Scratch arrives in Unit 2.",
            "The wall-facing warm up. Pupils must be allowed to fail it. The "
            "instruction that sends a partner into a wall is the evidence for "
            "everything else in the unit.",
            "Change one thing only. Pupils will want to fix three steps at once. "
            "Insist on one, and ask them to say what they expect before they run it "
            "again.",
            "Vocabulary to hear in the room by the end of the unit: algorithm, "
            "step, order, precise, error, bug, predict, repair. Home task: ask "
            "pupils to write four precise steps for a job they do at home with an "
            "adult, and bring the steps in, not the job."], icon="note"),
        B.ticks("Two points worth protecting when time is short", [
            "the wall-facing warm up, and permission to fail it",
            "changing one thing only, and predicting before running",
        ]),
    ]))

    pages.append(front(FRONT, "ANSWERS  TOPICS 1.1 AND 1.2",
                       "Answers: topics 1.1 and 1.2", [
        B.lead("No answers are printed inside the units, so that pupils answer "
               "aloud first. They are here."),
        B.subhead("Topic 1.1"),
        B.steps("Answers", [
            "Open. Accept any four steps a partner can follow with no questions. "
            "Look for a number or a named object in at least one step, for example "
            "\u201cturn the tap on\u201d rather than \u201cuse water\u201d.",
            "Open. The point is that the pupil can name a step number where they "
            "had to guess.",
        ], icon="try"),
        B.subhead("Topic 1.2"),
        B.steps("Answers", [
            "b and d are algorithms. a (\u201cBe tidy\u201d) is an instruction with no "
            "steps. c (\u201cDraw a house\u201d) is a task with no steps. Accept a pupil who "
            "argues that c could be an algorithm if it were broken into steps, "
            "because that is the right idea.",
            "Along the bottom row first, then up: right, right, up, up, up. Five "
            "arrows, and it is the same length as the route in the worked example, "
            "which is worth pointing out.",
        ], icon="try"),
    ]))

    pages.append(front(FRONT, "ANSWERS  TOPICS 1.2 AND 1.3",
                       "Answers: topics 1.2 and 1.3", [
        B.subhead("Topic 1.2, continued"),
        B.steps("Answers", [
            "Possible. The broken tile is in the third row, second column. Any "
            "five-arrow route that stays clear of it works, for example up, up, "
            "right, right, up as printed in the worked example, which passes "
            "through the third row third column and not the broken tile. Pupils who "
            "write \u201cnot possible\u201d have usually assumed Rebite must travel in a "
            "straight line.",
            "Open, depends on the partner's six arrows. The check is that the "
            "pupil's finger and the partner's intention agree.",
            "Go further: the shortest route that reaches the flag and returns to "
            "the start is ten arrows: five out, five back. Any pupil claiming "
            "fewer has usually let Rebite move two squares on one arrow.",
        ], icon="try"),
        B.subhead("Topic 1.3"),
        B.para("Find the fault: step 4 is in the wrong place. Correct order: open "
               "the jam jar, take two slices of bread, spread the jam on one slice, "
               "put the two slices together. Accept \u201ctake two slices\u201d before \u201copen "
               "the jar\u201d, because both work; the fault is that the jar is opened "
               "after the jam is spread, which is impossible."),
    ]))

    pages.append(front(FRONT, "ANSWERS  TOPIC 1.4", "Answers: topic 1.4", [
        B.subhead("Topic 1.4"),
        B.steps("Answers", [
            "The mat is four squares across. Starting bottom left: up, up puts "
            "Rebite in the third row, first column. Then right, right, right puts "
            "it in the fourth column. The final up puts it in the top row, fourth "
            "column. It does not land on the flag, which is in the third column. "
            "The third \u201cright\u201d is the fault.",
            "Read, predict, run, change one thing, run again.",
            "Open. Look for: if you change three things and it works, you do not "
            "know which change repaired it, so you have not learnt anything and the "
            "fault can come back.",
            "Open. Look for: a step is missing, a step is in the wrong order, a "
            "step is not precise.",
            "Open. Accept anything that fixes the vagueness, for example \u201cpour "
            "water into the jug until it reaches the line\u201d.",
            "Open. Look for the idea that an error is information, not a judgement. "
            "For example: \u201cAn error tells you where your instructions and your "
            "thinking stopped agreeing. Everybody who writes instructions gets "
            "them.\u201d",
        ], icon="try"),
    ]))

    pages.append(front(FRONT, "SOURCES AND REFERENCES  THE WORD ALGORITHM",
                       "Sources: the word algorithm", [
        B.lead("Every fact in this book was checked before it was printed. These "
               "are the checks."),
        B.panel("plain", "The word algorithm (topic 1.1)", [
            "Muhammad ibn Musa al-Khwarizmi, born about 780, died about 850, "
            "worked at the House of Wisdom in Baghdad around 820. The Latin "
            "translation of his book on Hindu-Arabic numerals, Algoritmi de numero "
            "Indorum, gave English the word algorithm from the Latin form of his "
            "name.",
            "The book says al-Khwarizmi's name gave us the word, and that he did "
            "not invent the idea of following steps in order, because step-by-step "
            "methods are thousands of years older than he is."], icon="note"),
        B.reflist([
            ("MacTutor History of Mathematics, University of St Andrews, biography "
             "of al-Khwarizmi",
             "https://mathshistory.st-andrews.ac.uk/Biographies/Al-Khwarizmi",
             "topic 1.1"),
            ("Mehri, B., \u201cFrom Al-Khwarizmi to Algorithm\u201d",
             "Olympiads in Informatics, 2017, volume 11, special issue, pages 71 "
             "to 74", "topic 1.1"),
        ]),
    ]))

    pages.append(front(FRONT, "SOURCES AND REFERENCES  THE FIRST BUG",
                       "Sources: the first computer bug", [
        B.panel("plain", "The first computer bug (topic 1.3)", [
            "On 9 September 1947 a team testing the Harvard Mark II at Harvard "
            "University found a moth between the contacts of a relay, taped it into "
            "the machine's logbook, and wrote \u201cfirst actual case of bug being "
            "found\u201d. The page is held by the Smithsonian's National Museum of "
            "American History in Washington.",
            "The book does not say who found the moth. Grace Hopper was a member of "
            "the Mark II team and made the story famous in her lectures, but the "
            "museum does not attribute that logbook page to her, so naming her as "
            "the finder would teach something untrue.",
            "The word \u201cbug\u201d already meant a small fault before 1947. Thomas Edison "
            "used it that way in a letter in 1878, which is why finding a real "
            "insect was funny enough to keep."], icon="note"),
        B.reflist([
            ("Computer History Museum, This Day in History, 9 September",
             "https://www.computerhistory.org/tdih/september/9", "topic 1.3"),
            ("Centre for Computing History, \u201cFirst computer bug is found\u201d, "
             "9 September 1947",
             "https://www.computinghistory.org.uk/det/5927/First-computer-bug-is-found",
             "topic 1.3"),
        ]),
        B.panel("tint", "For teachers", [
            "The printed word list is generated from the keyword panels in the "
            "units, so it cannot drift from the body text. Adding a word to a unit "
            "adds it here automatically."], icon="note"),
    ]))

    pages.append(front(FRONT, "ABOUT THIS BOOK", "About this book", [
        B.para("Curriculum. This book follows the Edu360 Computing Year 3 scheme of "
               "work: five units and 31 topics, kept in the scheme's own order and "
               "with the scheme's own titles. The plan the book is built and gated "
               "against is MARKDOWN/06-SCHEME-MAP.md, and a topic in that plan that "
               "does not reach the printed page fails the build rather than going "
               "unnoticed."),
        B.para("This sample. What you are holding is Unit 1 with its full front and "
               "back matter, built so that the design, the voice and the panel "
               "furniture can be judged before Units 2 to 5 are written. It is not "
               "the finished 104-page book."),
        B.para("Assumed prior learning. Pupils have put steps in order and followed "
               "a simple program in Year 2. They have met patterns and sequences. "
               "They are not assumed to have used Scratch, which begins in Unit 2."),
        B.para("Why Unit 1 has no screens at all. Pupils who meet precision on "
               "paper and out loud first guess far less when they reach a screen. "
               "Every task in Unit 1 can be done with a pencil, a partner and a "
               "floor space. That is a deliberate choice, not a shortage of "
               "material."),
        B.para("Assessment. There are no high-stakes tests in this book. The "
               "traffic-light table at the end of each unit and the Now I can "
               "checklist are formative, for the pupil to fill in and for you to "
               "read. The project rubric marks three things only: steps and order, "
               "precision, and finding the error."),
        B.para("Language. British English throughout. Pupils, programme, practise "
               "as a verb and practice as a noun. The book addresses pupils "
               "directly as \u201cyou\u201d, and all adult-facing copy in it is written to "
               "teachers."),
        B.para("Home learning. Ask pupils to write four precise steps for a job "
               "they do at home with an adult, and to bring in the steps rather "
               "than the job."),
    ]))

    return pages
