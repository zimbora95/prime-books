# Computing & Robotics (Structured) - Year 7 (Prime Book)
> Markdown companion of `public/library/y07-computing-structured/book.pdf` (135 pages).> RULE: when the PDF is edited, this file must be updated in the same change.

<!-- page 1 -->

---
## Computing & Robotics

## Year 7

Cambridge Lower Secondary

Student Manual · Structured edition

<!-- page 2 -->

---
## Contents

**UNIT 1**
**Computational Thinking**

Decomposition · Pattern recognition · Abstraction · Algorithms · Flowcharts · Pseudocode · Testing and debugging

**UNIT 2**
**Managing Data**

Data representation · Binary and decimal · Data storage · Databases · Collecting and analysing · Tables and queries

**UNIT 3**
**Networks and Digital Communication**

Networks · The internet · IP addresses · Routers and switches · Protocols · Digital communication · Cybersecurity · Online
safety

**UNIT 4**
**Computer Systems**

Hardware · CPU · RAM and ROM · Input and output · Secondary storage · Operating systems · System and application
software · Processing data

**UNIT 5**
**micro:bit and Robotics**

Introduction · The board · How computers work · Set up · Programming concepts · Pins · Block coding · MicroPython ·
Images · Buttons · Pins in practice · Music · Random

**UNIT 6**
**Communication**

Email · Effective use of the internet

**UNIT 7**
**Layout**

Documents · Tables · Headers and footers

**UNIT 8**
**Databases**

Structure · Manipulating data · Presenting data

**PROJECT**
**The Smart School Project**

A twelve-step interdisciplinary challenge

**BACKMATTER**
**Glossary and Assessment**

Glossary · End-of-unit tests · Teacher answer key

**Contents**

<!-- page 3 -->

---
**UNIT 1 · TOPIC 1**
## Decomposition

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what decomposition means
✓break a complex problem into smaller parts
✓say why decomposition makes problems easier to solve
✓spot decomposition in everyday life, programming and robotics

Some problems are too big to solve in one go. Decomposition means breaking a big problem down into
smaller parts that are each easy to think about. Solve every small part, put the answers together, and
the big problem is solved.

It is the first tool of computational thinking: a computer scientist faced with anything complicated
starts by taking it apart.

**Why decomposition helps**
Small parts are easier to understand, easier to share between a team, easier to test one at a time, and
easier to fix when something goes wrong. If a robot behaves badly, you can check each part separately
instead of staring at the whole program.

**Decomposition in everyday life**

**●EXAMPLES**

Making a sandwich: get the bread, spread the butter, add the filling, close the sandwich, cut it.

Planning a journey: choose the route, buy the ticket, pack the bag, leave on time.

Creating a computer game: design the levels, draw the characters, write the movement code, add the
sound.

Solving a maze: find the first turning, follow the wall, check for dead ends, reach the exit.

**●TRY IT**

**1**
Here is a complex problem: 'Run a stall at the school fair.' Divide it into at least six smaller tasks.

**2**
Compare your list with a partner. Did you both choose the same parts?

**UNIT 1 · COMPUTATIONAL THINKING**
1

<!-- page 4 -->

---
**ROBOTICS CONNECTION**
A robot that must travel from the classroom to the library is one big problem. Decompose it: read
a map of the school, plan a route, avoid obstacles, detect the library door, stop safely. Each part
can be built and tested on its own.

**▮KEY WORDS**

**decomposition breaking a complex problem into smaller, manageable parts**

**computational thinking approaching problems the way a computer scientist does**

**subproblem one of the smaller problems produced by decomposition**

**●CHALLENGE**

Robotics challenge: break down the problem of programming a robot to travel from the classroom to the
library. Write at least six subproblems, then number them in the order you would solve them.

**●CHECK YOUR UNDERSTANDING**

**1**
What does decomposition mean, in your own words?

**2**
Give one reason why decomposition makes problems easier to solve.

**3**
Name two everyday tasks that can be decomposed.

**4**
Why is decomposition useful when a team builds a computer game together?

**5**
True or false: decomposition means solving the whole problem at once.

**●EXIT TICKET**

**1**
Define decomposition in one sentence.

**2**
Why do programmers decompose programs into separate parts?

**3**
Write one subproblem of planning a school trip.

<!-- page 5 -->

---
**UNIT 1 · TOPIC 2**
## Pattern Recognition

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what pattern recognition means
✓spot similarities and repetition in problems
✓continue number patterns and shape patterns
✓find patterns in programs and robot movements

A pattern is something that repeats or follows a rule. Pattern recognition means looking carefully at a
problem and asking: have I seen something like this before? What stays the same? What changes?

Once you spot a pattern, you can reuse a solution you already have instead of inventing a new one every
time. This is the second tool of computational thinking.

**Patterns everywhere**
Number patterns: 2, 4, 6, 8 ... adds two each time. Shape patterns: triangle, square, triangle, square ...
repeats every two shapes. Music, wallpaper, dance steps and even the days of the week all follow
patterns.

In programming, the same small shapes appear again and again: get some input, check it, do something
with it, show the result. In robotics, a robot sweeping a floor repeats: move forward, detect wall, turn,
repeat.

**●EXAMPLES**

Number sequence: 3, 6, 9, 12 ... the rule is 'add 3'. The next term is 15.

Shape pattern: circle, circle, square, circle, circle, square ... the next shape is a circle.

Robot movement: forward, forward, turn left, forward, forward, turn left ... the pattern repeats every
three instructions.

**●TRY IT**

**1**
Continue each pattern and state its rule: (a) 5, 10, 15, 20, ... (b) 64, 32, 16, ... (c) 1, 1, 2, 3, 5, 8, ...

**2**
Draw the next two shapes: square, triangle, triangle, square, triangle, triangle, ...

**3**
A robot repeats: forward 2, turn right, forward 2, turn right, forward 2, turn right. What shape is it
drawing?

**UNIT 1 · COMPUTATIONAL THINKING**
3

<!-- page 6 -->

---
**ROBOTICS CONNECTION**
Robots repeat movements constantly. Instead of writing the same instruction fifty times,
programmers write it once and repeat it. Spotting the repeated part of a robot's route is what
makes short, clever programs possible.

**▮KEY WORDS**

**pattern recognition noticing similarities and repetition inside problems**

**sequence a list of things in order, where each item is called a term**

**repetition doing the same instruction more than once**

**●CHALLENGE**

Find the repeated pattern and predict what happens next. A floor robot follows this program forever:
forward 1, turn right, forward 1, turn right, forward 1, turn right, forward 1, turn right. Describe where
the robot is after 4, 8 and 100 repetitions, and explain how you know.

**●CHECK YOUR UNDERSTANDING**

**1**
What is a pattern?

**2**
Why is finding a pattern useful when solving a problem?

**3**
What is the rule of the sequence 7, 14, 21, 28?

**4**
Give an example of a pattern in a computer program.

**5**
How does pattern recognition help make robot programs shorter?

**●EXIT TICKET**

**1**
Define pattern recognition in one sentence.

**2**
Write the next two terms: 1, 2, 4, 8, ...

**3**
Name one pattern you saw today outside Computing.

<!-- page 7 -->

---
**UNIT 1 · TOPIC 3**
## Abstraction

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what abstraction means
✓decide which details matter and which do not
✓recognise abstraction in maps, games and programs
✓build a simple model of a real place

Abstraction means keeping the important information and throwing away the rest. A good model is not a
perfect copy of reality; it is a simplified version that shows exactly what you need.

Think of a metro map. It does not show streets, houses or hills. It shows only the lines, the stations and
the connections, because that is all a passenger needs. A bus driver needs a different map, and a
plumber needs yet another.

**Choosing what matters**
Abstraction always depends on the purpose. A game character in a driving game has speed, direction
and position, but not a favourite food, because the food does not matter to the game. In programming,
variables are chosen the same way: keep what the program needs, ignore the rest.

**●EXAMPLES**

A map represents a real environment without showing every object: roads as lines, towns as dots.

A contact card stores a name, phone number and email, but not the person's height.

A weather app shows temperature and rain probability, not the colour of every cloud.

**●TRY IT**

**1**
Draw a simplified map of your school showing only: the entrance, the corridors, the stairs, your
classroom and the library. Leave out furniture, colours and decorations.

**2**
Swap maps with a partner. Can they find your classroom using only your map?

**ROBOTICS CONNECTION**
A robot navigating a school does not need a photo of the school. It needs walls, distances and
turning points. Roboticists abstract the building into a grid or a map of nodes and connections,
keeping only what the robot's sensors can use.

**UNIT 1 · COMPUTATIONAL THINKING**
5

<!-- page 8 -->

---
**▮KEY WORDS**

**abstraction keeping the important details and removing the rest**

**model a simplified representation of something real**

**relevant mattering for the purpose at hand**

**●CHALLENGE**

Create a map that contains only the information a robot needs to navigate your classroom to the school
canteen. Label every item you kept and list three details you deliberately removed, explaining why the
robot does not need them.

**●CHECK YOUR UNDERSTANDING**

**1**
What does abstraction mean?

**2**
Why does a metro map not show houses?

**3**
Give one example of abstraction in a computer game.

**4**
Why do different users need different maps of the same place?

**5**
True or false: abstraction means removing details the problem does not need.

**●EXIT TICKET**

**1**
Define abstraction in one sentence.

**2**
Name two details a school map keeps and two it removes.

**3**
Why is abstraction useful in robotics?

<!-- page 9 -->

---
**UNIT 1 · TOPIC 4**
## Algorithms

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what an algorithm is
✓write clear step-by-step instructions
✓understand sequence, inputs and outputs
✓know what makes a good algorithm

An algorithm is a set of step-by-step instructions that solves a problem or completes a task. A recipe is
an algorithm. So is the method for long division, and so is the program inside a traffic light.

Algorithms work because of sequence: the order of the steps matters. Brush your teeth before applying
toothpaste and the algorithm fails, even though every step is correct.

**Inputs and outputs**
Many algorithms take an input, the information they start with, and produce an output, the result. A
drinks machine takes your coins and your button press as input, and produces a drink as output. Get
ready each morning takes the time you woke up as input and produces you, dressed and fed, as output.

**What makes a good algorithm?**

**●A GOOD ALGORITHM IS**

precise: every step says exactly what to do

ordered: the steps come in a sequence that works

complete: it covers every case, not just the easy ones

effective: it finishes and gives the right answer

**●TRY IT**

**1**
These instructions for making toast are in the wrong order. Rewrite them correctly: (1) Put the
bread in the toaster. (2) Eat the toast. (3) Buy the bread. (4) Butter the toast. (5) Push the lever
down.

**2**
Write your own algorithm for getting from your classroom to the sports hall, in numbered steps.
Assume the reader has never been in the school.

**3**
One step says 'Walk for a while'. Why is this a bad step? Rewrite it properly.

**UNIT 1 · COMPUTATIONAL THINKING**
7

<!-- page 10 -->

---
**ROBOTICS CONNECTION**
A robot follows an algorithm exactly. If the route algorithm says forward 3, turn left, forward 3,
the robot does precisely that, even if a wall is in the way. Every robotics challenge starts by
writing the route algorithm on paper before touching the robot.

**▮KEY WORDS**

**algorithm a precise set of step-by-step instructions that solves a problem**

**sequence the order in which instructions are carried out**

**input information an algorithm starts with**

**output the result an algorithm produces**

**●CHALLENGE**

Robotics challenge: create an algorithm for a floor robot to complete a simple route in your classroom,
from the door to the teacher's desk, avoiding at least one obstacle. Write it in numbered steps using
only forward, turn left, turn right and stop.

**●CHECK YOUR UNDERSTANDING**

**1**
What is an algorithm?

**2**
Why does the order of steps matter?

**3**
Give the input and output of a drinks machine algorithm.

**4**
Name two qualities of a good algorithm.

**5**
Why is 'stir a bit' a poor instruction in an algorithm?

**●EXIT TICKET**

**1**
Define algorithm in one sentence.

**2**
Write an algorithm with exactly four steps for a task you do every day.

**3**
What is the output of the algorithm 'input a number, multiply it by 2'?

<!-- page 11 -->

---
**UNIT 1 · TOPIC 5**
## Flowcharts

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓know the standard flowchart symbols
✓read a flowchart and follow its path
✓draw a flowchart for a simple algorithm
✓include decisions with IF/ELSE

A flowchart is a diagram of an algorithm. Instead of writing steps as sentences, you draw them as boxes
of different shapes joined by arrows. Anyone can read a good flowchart, whatever language they speak.

**The standard symbols**

**SYMBOL**
**SHAPE**
**MEANING**

Start / End
rounded rectangle
where the algorithm begins or stops

Process
rectangle
an action, such as 'calculate total'

Input / Output
parallelogram
receiving data or showing a result

Decision
diamond
a question with YES and NO paths

Arrow
arrow
the direction of flow between steps

**A flowchart with a decision**

**START**
**|**
**v**
**Check the weather**
**|**
**v**
**<Is it raining?> --YES--> Take umbrella --> END**
**|**
**NO**
**v**
**Go outside --> END**

The diamond asks a question. There must always be at least two arrows leaving it, one for each answer.
Following the arrows from START to END tells you exactly what the algorithm does.

**UNIT 1 · COMPUTATIONAL THINKING**
9

<!-- page 12 -->

---
**●TRY IT**

**1**
Match each symbol to its use: rectangle, diamond, parallelogram, rounded rectangle. Uses: 'ask the
user their age', 'calculate the average', 'is the answer correct?', 'start'.

**2**
Draw a flowchart for this algorithm: input a number, decide whether it is 10 or more, output 'big' or
'small'.

**3**
This flowchart has an error: a decision with only one exit arrow. Explain the error and fix it.

**ROBOTICS CONNECTION**
Robots constantly make decisions: is there an obstacle? is the line black? is the button pressed? A
flowchart of a robot program is mostly diamonds. Before coding, roboticists sketch the flowchart
to make sure every decision has a YES path and a NO path.

**▮KEY WORDS**

**flowchart a diagram showing the steps of an algorithm as symbols joined by arrows**

**decision a diamond symbol that asks a question and splits the flow**

**path one possible route through a flowchart**

**●CHALLENGE**

Robotics challenge: create a flowchart for a robot that moves forward and stops when it detects an
obstacle. Use the correct symbols, and make sure every decision has two exits. Test a partner: can they
act out your flowchart as the robot?

**●CHECK YOUR UNDERSTANDING**

**1**
Which symbol represents a decision?

**2**
What do the arrows in a flowchart show?

**3**
How many paths must leave a decision symbol?

**4**
Which symbol would you use for 'output the total'?

**5**
Why are flowcharts useful before writing a program?

**UNIT 1 · COMPUTATIONAL THINKING**
10

<!-- page 13 -->

---
**●EXIT TICKET**

**1**
Name the four main flowchart symbols.

**2**
What is the rule about arrows leaving a diamond?

**3**
Sketch the flowchart for 'is it raining?' from memory.

<!-- page 14 -->

---
**UNIT 1 · TOPIC 6**
## Pseudocode

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what pseudocode is and why programmers use it
✓write algorithms using INPUT, OUTPUT, IF, ELSE, REPEAT and WHILE
✓turn a description into structured pseudocode

Pseudocode is a way of writing an algorithm using structured half-English, half-code. It is not a real
programming language; nothing runs it. It exists so you can plan the logic of a program clearly before
translating it into Python or any other language.

Pseudocode uses a few consistent words: INPUT to collect information, OUTPUT to show a result, IF
and ELSE to make decisions, REPEAT to do something a fixed number of times, and WHILE to keep doing
something as long as a condition is true.

**Two examples**

**START**
**INPUT name**
**OUTPUT "Hello " + name**
**END**

**IF obstacle = TRUE THEN**
**STOP**
**ELSE**
**MOVE FORWARD**
**END IF**

**●TRY IT**

**1**
Write pseudocode that asks for two numbers and outputs the larger one.

**2**
Write pseudocode that outputs the word 'Fizz' for every number from 1 to 10.

**3**
Turn this sentence into pseudocode: 'While the battery is not empty, keep sweeping the floor.'

**ROBOTICS CONNECTION**
Robot programs are often planned in pseudocode first. The obstacle-avoiding robot above is a real
pattern: sense, decide, move. Pseudocode lets the whole team agree on the logic before anyone
fights with the syntax of a real language.

**UNIT 1 · COMPUTATIONAL THINKING**
12

<!-- page 15 -->

---
**▮KEY WORDS**

**pseudocode structured plain-English notes that describe an algorithm**

**condition a statement that is either true or false, used by IF and WHILE**

**loop instructions that repeat, written with REPEAT or WHILE**

**●CHALLENGE**

Robotics challenge: write pseudocode for a robot that moves forward and turns when it detects an
obstacle, and keeps doing this forever. Use a WHILE loop and clear conditions. Then swap with a
partner and check: is every END IF and END WHILE present?

**●CHECK YOUR UNDERSTANDING**

**1**
What is pseudocode and why do programmers use it?

**2**
Which pseudocode word collects information from the user?

**3**
What is the difference between REPEAT and WHILE?

**4**
Write one line of pseudocode using IF.

**5**
Can a computer run pseudocode? Explain your answer.

**●EXIT TICKET**

**1**
Define pseudocode in one sentence.

**2**
Write pseudocode for: input a password, output 'welcome' if it is correct.

**3**
Why does pseudocode travel well between different programming languages?

<!-- page 16 -->

---
**UNIT 1 · TOPIC 7**
## Testing and Debugging

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain testing, bugs and debugging
✓compare expected results with actual results
✓name the three kinds of error
✓follow the debugging cycle

A bug is a mistake in a program. Debugging means finding the bug and fixing it. Before a program is
trusted, it must be tested: you run it with known inputs and check that the output is what you expected.

A test case records three things: the input you tried, the result you expected, and the actual result. If
expected and actual differ, you have found a bug.

**Three kinds of error**

**ERROR**
**WHAT IT IS**
**EXAMPLE**

Syntax error
the code breaks the rules of the language and will
not run at all

prnt("hi") missing the i

Runtime error
the program starts but crashes part-way
10 / 0 dividing by zero

Logic error
the program runs happily but gives the wrong
answer

total = price - quantity instead of
price * quantity

**The debugging cycle**

**RUN -> OBSERVE -> FIND THE BUG -> FIX -> TEST AGAIN -> IMPROVE**

Debugging is a loop, not a single step. You fix one bug, test again, and often find another. Professional
programmers expect this: finding bugs is not failing, it is the job.

**●TRY IT**

**1**
Debug It! This program should greet the user: OUTPUT "Hello" + nam. Find and fix the bug.

**2**
Debug It! This program should add two numbers: total = numer1 + number2. What kind of error is
it?

**3**
Write a test case table for a program that converts kilometres to miles: include normal input, zero
and a negative number.

**UNIT 1 · COMPUTATIONAL THINKING**
14

<!-- page 17 -->

---
**ROBOTICS CONNECTION**
Robot bugs are visible: the robot drives into a wall. Watch what the robot actually does, compare
it with what it should do, and only then change the code. Changing three things at once means you
never learn which fix worked.

**▮KEY WORDS**

**testing running a program with known inputs to check it works**

**bug a mistake in a program**

**debugging finding and fixing mistakes**

**test case one input, the expected result and the actual result**

**logic error a program that runs but produces a wrong answer**

**●CHALLENGE**

Debug It! A robot should stop at a black line but drives straight over it. Its code says IF sensor = white
THEN stop. Identify the logic error, explain how you would test the fix, and name one way the sensor
data itself could mislead you.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between a bug and debugging?

**2**
What three things does a test case record?

**3**
Which kind of error stops a program from running at all?

**4**
Why can logic errors be the most dangerous kind?

**5**
Why do we test again after fixing a bug?

**●EXIT TICKET**

**1**
Define bug and debugging.

**2**
Name the three kinds of error with one example each.

**3**
Write the six steps of the debugging cycle from memory.

**UNIT 1 · COMPUTATIONAL THINKING**
15

<!-- page 18 -->

---
**UNIT 2 · TOPIC 1**
## Data Representation

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what data is
✓name the different types of data computers handle
✓understand that computers store everything using binary

Data is information: facts, words, numbers, pictures, sounds and videos. Computers can work with all of
it, but only after the data has been turned into numbers.

Inside a computer there are no letters and no colours, only tiny switches. Each switch is either off or on.
We write the two states as 0 and 1, and each single 0 or 1 is called a bit. Binary is this two-symbol
system.

Text becomes numbers through a code: each letter is given a number. Images become numbers: a
picture is split into tiny dots (pixels), and each pixel's colour is a number. Sound becomes numbers: a
microphone measures the shape of the sound wave thousands of times per second. Video is just many
images plus sound.

**Everything is bits**

**●EXAMPLES**

The letter A is the number 65 in the code called ASCII.

A photo on a phone is millions of numbers, one per pixel.

A three-minute song is hundreds of millions of bits.

**●TRY IT**

**1**
List five pieces of data a school holds about you. What type is each: text, number, image, sound or
video?

**2**
Why can a computer not store the letter 'a' directly?

**ROBOTICS CONNECTION**
A robot's sensors also produce data: a distance sensor returns a number of centimetres, a light
sensor a brightness level. The robot's processor decides what to do by comparing these numbers,
never by 'seeing' the world as we do.

**UNIT 2 · MANAGING DATA**
1

<!-- page 19 -->

---
**▮KEY WORDS**

**data information that a computer can store and process**

**bit a single 0 or 1, the smallest unit of data**

**binary the two-symbol number system computers use**

**pixel one tiny dot of a digital image**

**●CHALLENGE**

A smart doorbell captures video, sound and a date. Describe how each of the three becomes binary
inside the device, and estimate which of the three produces the most bits per second.

**●CHECK YOUR UNDERSTANDING**

**1**
What is data?

**2**
What two symbols does binary use?

**3**
How does a computer store text as numbers?

**4**
What is a pixel?

**5**
Why do sensors on a robot output numbers?

**●EXIT TICKET**

**1**
Define data and bit.

**2**
Name the five types of data from this topic.

**3**
How does sound become data?

<!-- page 20 -->

---
**UNIT 2 · TOPIC 2**
## Binary and Decimal Numbers

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain the decimal and binary number systems
✓read binary place values
✓convert small numbers between binary and decimal

The numbers you use every day are decimal, or base 10: there are ten digits, 0 to 9, and each place is
worth ten times the one to its right. Computers use binary, or base 2: there are only two digits, 0 and 1,
and each place is worth twice the one to its right.

**Binary place values**
Reading from the right, the places in an 8-bit binary number are worth 128, 64, 32, 16, 8, 4, 2 and 1. To
convert binary to decimal, add up the place values where a 1 sits.

**128**
**64**
**32**
**16**
**8**
**4**
**2**
**1**
**DECIMAL**

1
0
1
0
1
0
1
0
128+32+8+2 = 170

0
0
0
0
1
0
1
0
8+2 = 10

1
1
1
1
1
1
1
1
255

**Converting decimal to binary**
Take the number 45. Ask: is 128 needed? No, too big, write 0. Is 64 needed? No, 0. Is 32 needed? Yes,
45 minus 32 leaves 13, write 1. Is 16 needed? No, 0. Is 8 needed? Yes, 13 minus 8 leaves 5, write 1. Is 4
needed? Yes, 5 minus 4 leaves 1, write 1. Is 2 needed? No, 0. Is 1 needed? Yes, write 1. So 45 is
00101101.

**●TRY IT**

**1**
Convert to decimal: (a) 1010 (b) 10011 (c) 11111111.

**2**
Convert to binary: (a) 7 (b) 20 (c) 100.

**3**
What is the largest number that fits in 4 bits? What about 8 bits?

**ROBOTICS CONNECTION**
Robots count in binary because their processors are built from switches. An 8-bit sensor can
report 256 different levels; a light sensor reading of 10101100 is just the number 172 to the
robot's brain.

**UNIT 2 · MANAGING DATA**
3

<!-- page 21 -->

---
**▮KEY WORDS**

**decimal base 10, the everyday number system with digits 0-9**

**binary base 2, the number system with digits 0 and 1**

**place value what a digit position is worth**

**bit one binary digit**

**●CHALLENGE**

Binary Challenge: convert your age to binary, then your house number, then the year of your birth (you
will need more than 8 bits!). Write a short method card that a friend could follow to do any conversion.

**●CHECK YOUR UNDERSTANDING**

**1**
What are the first four binary place values, from right to left?

**2**
Convert 1101 to decimal.

**3**
Convert 6 to binary.

**4**
Why does 11111111 equal 255?

**5**
What is the difference between base 10 and base 2?

**●EXIT TICKET**

**1**
Convert 10110 to decimal.

**2**
Convert 9 to binary.

**3**
Why do computers use binary instead of decimal?

<!-- page 22 -->

---
**UNIT 2 · TOPIC 3**
## Data Storage

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain why computers need storage
✓distinguish primary and secondary, local and cloud storage
✓use the units bit, byte, KB, MB, GB and TB

A computer needs somewhere to keep its data when the power is off. Primary storage, such as RAM,
holds the programs that are running right now, but forgets everything when the computer switches off.
Secondary storage, such as a hard disk or SSD, keeps your files safely even with no power.

Storage can be local, inside or plugged into your device, or in the cloud, kept on a company's computers
far away and reached through the internet. Both have a place: local storage works offline; cloud storage
backs up your work and shares it between devices.

**Units of storage**
Eight bits make one byte, enough to store a single letter. From there, each unit is about a thousand
times bigger than the last.

**UNIT**
**SIZE**
**ROUGHLY HOLDS**

Byte (B)
8 bits
one character of text

Kilobyte (KB)
about 1,000 bytes
half a page of text

Megabyte (MB)
about 1,000 KB
one photo, or one minute of music

Gigabyte (GB)
about 1,000 MB
250 photos, or 30 minutes of video

Terabyte (TB)
about 1,000 GB
250,000 photos, or a whole film library

**●TRY IT**

**1**
Put these in order from smallest to largest: GB, bit, TB, byte, MB, KB.

**2**
A document is 900 KB. Roughly how many such documents fit on a 2 GB USB stick?

**3**
Give one advantage and one disadvantage of keeping work only in the cloud.

**UNIT 2 · MANAGING DATA**
5

<!-- page 23 -->

---
**ROBOTICS CONNECTION**
A robot with limited storage must decide what to keep: every sensor reading it saves takes space.
Real rovers like Mars rovers choose carefully which data to store and send home, because storage
and bandwidth are small.

**▮KEY WORDS**

**primary storage fast memory holding running programs; lost when power is off**

**secondary storage storage that keeps data when the power is off**

**cloud storage storage kept on remote servers, reached via the internet**

**byte 8 bits**

**●CHALLENGE**

Plan the storage for a school robotics club with 50 MB of photos per competition, 4 GB of video per year
and 200 KB of programs. Choose and justify a mix of local and cloud storage that keeps everything safe
for five years.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between primary and secondary storage?

**2**
How many bits are in a byte?

**3**
Name two differences between local and cloud storage.

**4**
Which is bigger: 500 MB or 1 GB?

**5**
Why does RAM forget everything when the computer turns off?

**●EXIT TICKET**

**1**
Name the storage units from smallest to largest.

**2**
What does one byte roughly hold?

**3**
Give one reason schools use cloud storage.

<!-- page 24 -->

---
**UNIT 2 · TOPIC 4**
## Databases

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what a database is and why we use them
✓use the words table, record, field and primary key
✓search, sort and filter data

A database is an organised collection of data. Instead of one person's messy notebooks, a database
stores data in tables so any piece can be found instantly. Schools, libraries, banks, shops and hospitals
all run on databases.

A table is made of records and fields. A record is one complete item, such as one pupil. A field is one
piece of that record, such as the pupil's surname. Each field has a data type: text, number, date or
true/false.

**PUPIL_ID**
**SURNAME**
**FIRST NAME**
**YEAR**
**HOUSE**

701
Silva
Matilde
7
Atlantico

702
Costa
Goncalo
7
Tejo

703
Ramos
Beatriz
8
Atlantico

The pupil ID is the primary key: a field whose value is different for every record, so each record can be
found without confusion. Two pupils may share a name; no two share a pupil ID.

**Finding what you need**
Searching looks for records that match something. Sorting arranges records into order, such as surname
A to Z. Filtering hides everything except the records you asked for, such as Year = 7. All three work
together in every database you will use.

**●TRY IT**

**1**
In the table above, which field is the primary key, and why not FIRST NAME?

**2**
Sort the table by YEAR, then by SURNAME. What changes?

**3**
Write down the records that pass this filter: HOUSE = Atlantico.

**UNIT 2 · MANAGING DATA**
7

<!-- page 25 -->

---
**ROBOTICS CONNECTION**
A smart library robot needs the library database: record 1 per book, fields for shelf, title and
borrowed status. The robot's program queries the database to decide which shelf to drive to.

**▮KEY WORDS**

**database an organised collection of data in tables**

**record one complete item in a table, shown as a row**

**field one piece of a record, shown as a column**

**primary key the field that is unique for every record**

**filter showing only records that match a condition**

**●CHALLENGE**

Design a table for a shop database selling sports equipment: choose five fields, give each a data type,
choose the primary key, and explain why a shop would sort by price and filter by category.

**●CHECK YOUR UNDERSTANDING**

**1**
What is a database?

**2**
What is the difference between a record and a field?

**3**
Why does every table need a primary key?

**4**
What is the difference between sorting and filtering?

**5**
Name three organisations that use databases.

**●EXIT TICKET**

**1**
Define record and field.

**2**
What makes a field suitable as a primary key?

**3**
Write a filter to find all Year 8 pupils.

<!-- page 26 -->

---
**UNIT 2 · TOPIC 5**
## Collecting and Analysing Data

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓name different sources of data
✓collect data with surveys, forms and sensors
✓organise data, find patterns and draw conclusions

Before data can be analysed it must be collected. Data can come from people, through surveys,
questionnaires and forms, or from the world, through observations and sensors. Asking people gives
opinions and habits; sensors give accurate measurements but only measure what they are built to
measure.

Good collection is planned. Decide exactly what you want to know, who or what you will ask or measure,
and how you will record the answers. A messy collection produces data nobody can use.

**From raw data to conclusions**

**●THE ANALYSIS STEPS**

organise: put the data in a table or tally chart

describe: totals, averages, the highest and lowest

find patterns: which answer repeats? what changes over time?

compare: does one group differ from another?

conclude: what does the data actually tell you?

**●TRY IT**

**1**
Design a three-question survey to find out how classmates travel to school. Include one question
where a sensor could replace asking.

**2**
Collect answers from ten classmates, tally them and state one conclusion.

**3**
A temperature sensor records the classroom every minute for a day. Describe two patterns you
might find in the data.

**UNIT 2 · MANAGING DATA**
9

<!-- page 27 -->

---
**ROBOTICS CONNECTION**
Sensors are robots' way of collecting data. A weather station project collects temperature, light
and rainfall; the analysis step asks what the numbers mean, for example the coldest hour of the
school day.

**▮KEY WORDS**

**data collection gathering information to answer a question**

**survey asking people questions to collect their answers**

**sensor a device that measures something from the real world**

**conclusion what the data tells you, stated carefully**

**●CHALLENGE**

Plan a data collection to answer: which corridor in school is busiest at break? Choose your method, what
you will measure, how many days you will collect for, and three things that could make your data
misleading.

**●CHECK YOUR UNDERSTANDING**

**1**
Name three ways of collecting data.

**2**
What is the difference between a survey and a sensor?

**3**
Why must data be organised before analysis?

**4**
What are the steps from raw data to conclusion?

**5**
Give one way a data collection could be unfair.

**●EXIT TICKET**

**1**
Name two sources of data.

**2**
Write one good survey question about screen time.

**3**
What is a conclusion?

<!-- page 28 -->

---
**UNIT 2 · TOPIC 6**
## Tables and Queries

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓read a data table using rows and columns
✓sort, filter and search a table
✓write simple queries with conditions

A table stores data in rows and columns. Each row is one record; each column is one field. Reading a
table means knowing that every value sits where one record meets one field.

A query is a saved question you ask a table. Instead of hunting through rows yourself, you write the
condition and the database answers instantly, even across thousands of records.

**Writing simple conditions**

**SELECT * FROM pupils WHERE Year = 7**

**SELECT Surname FROM pupils WHERE House = "Tejo"**

**SELECT * FROM books WHERE borrowed = FALSE**

Read the first line as: show me every field of every record in the pupils table where the Year field equals
7. The WHERE part is the condition; only records that pass it are shown.

**●TRY IT**

**1**
Using the pupils table from Topic 2.4, write what each query returns: WHERE Year = 7; WHERE
Surname = "Ramos"; WHERE House = "Atlantico" AND Year = 8.

**2**
Write a query to find all books in a library that are not borrowed.

**3**
Why does a query on 10,000 records beat searching by eye?

**ROBOTICS CONNECTION**
Warehouse robots run queries all day: which items are due today? which shelf holds item 1234?
The query result becomes the robot's next destination.

**UNIT 2 · MANAGING DATA**
11

<!-- page 29 -->

---
**▮KEY WORDS**

**query a saved question you ask a table**

**condition the test a record must pass, written after WHERE**

**sort put records in order by a field**

**filter show only records that match a condition**

**●CHALLENGE**

A school library table has fields: ID, Title, Author, Genre, Borrowed, DueDate. Write three queries: one
to find all fantasy books, one to find all borrowed books due before Friday, and one combining two
conditions. Predict each result.

**●CHECK YOUR UNDERSTANDING**

**1**
What do the rows and columns of a table represent?

**2**
What is a query?

**3**
What does the WHERE part of a query do?

**4**
Write a condition to find records where Age is 12.

**5**
When is sorting more useful than filtering?

**●EXIT TICKET**

**1**
Define query and condition.

**2**
Write a query finding all Year 7 pupils.

**3**
What is the difference between a filter and a query?

**UNIT 2 · MANAGING DATA**
12

<!-- page 30 -->

---
**UNIT 3 · TOPIC 1**
## Computer Networks

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what a network is
✓know the difference between a LAN and a WAN
✓weigh the advantages and disadvantages of networks

A network is two or more computers connected so they can share things: files, printers, an internet
connection. A computer on its own is powerful but lonely; connected, computers can work together.

A LAN, or local area network, covers one site, such as a school or an office. A WAN, or wide area
network, joins networks across towns, countries or the world. The internet is the biggest WAN of all.

**What networks give us**

**●ADVANTAGES**

share files and folders instantly

share expensive devices, such as printers

communicate by message and video call

store your work centrally and reach it anywhere

**●DISADVANTAGES**

if the network fails, everything stops

security: a virus can spread between machines

cost: cables, devices and experts to run it all

privacy: data must be protected from snoopers

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
1

<!-- page 31 -->

---
**●TRY IT**

**1**
Is the network in your classroom a LAN or a WAN? How do you know?

**2**
List every network device you can see in the classroom: computers, printers, access points,
switches.

**3**
Give one advantage and one disadvantage of your school keeping all reports on the network.

**ROBOTICS CONNECTION**
Robots in warehouses form networks: a central computer sends each robot its next job over wifi,
and robots report their positions back. A robot outside the network is useless, exactly like a
computer without connection.

**▮KEY WORDS**

**network two or more computers connected to share data and devices**

**LAN local area network, covering one site**

**WAN wide area network, joining sites over long distances**

**internet the worldwide network of networks**

**●CHALLENGE**

Sketch the network of your school: classrooms, the server room, wifi access points and the connection to
the internet. Label each part LAN or WAN, and mark the single most important device, with reasons.

**●CHECK YOUR UNDERSTANDING**

**1**
What is a network?

**2**
What is the difference between a LAN and a WAN?

**3**
Name two advantages of networks.

**4**
Name two disadvantages of networks.

**5**
Is the internet a LAN or a WAN?

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
2

<!-- page 32 -->

---
**●EXIT TICKET**

**1**
Define LAN and WAN.

**2**
Why do schools network their computers?

**3**
What happens to networked computers if the network goes down?

<!-- page 33 -->

---
**UNIT 3 · TOPIC 2**
## The Internet

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what the internet is
✓distinguish the internet from the World Wide Web
✓know the roles of clients and servers

The internet is a giant network of networks: billions of devices, connected by cables and radio, that
agree to move data for one another. It began as a research project and now carries almost all human
communication.

The World Wide Web is not the same thing. The web is the collection of websites and pages that travels
over the internet. The internet also carries email, video calls, games and app data, none of which are the
web. The internet is the road network; the web is one kind of traffic on it.

**Clients and servers**
When you open a website, your device is the client: it asks for something. The computer holding the
website is the server: it answers. A server can serve thousands of clients at once, which is why one
website works for the whole world.

**●TRY IT**

**1**
Classify each as internet or web: an email, a WhatsApp message, a news website, a video call, an
online game.

**2**
When you load a page, which device is the client and which is the server?

**3**
Why does one powerful server beat a classroom full of ordinary computers for hosting a website?

**ROBOTICS CONNECTION**
Cloud robotics uses the internet the same way: a small robot sends sensor data to a powerful
server, the server thinks, and sends the decision back. The robot borrows a bigger brain.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
4

<!-- page 34 -->

---
**▮KEY WORDS**

**internet the worldwide network that carries data between devices**

**World Wide Web websites and pages, one service that runs on the internet**

**client the device that asks for data**

**server the computer that stores data and answers requests**

**●CHALLENGE**

Explain to a Year 4 pupil, in five sentences and no jargon, the difference between the internet and the
web. Use one comparison of your own invention, like the road and traffic one.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the internet?

**2**
What is the World Wide Web?

**3**
What device asks for a web page, and what answers?

**4**
Is email part of the web? Explain.

**5**
Why is the client-server model useful?

**●EXIT TICKET**

**1**
Define client and server.

**2**
Give an internet service that is not the web.

**3**
Why is the internet called a network of networks?

<!-- page 35 -->

---
**UNIT 3 · TOPIC 3**
## IP Addresses

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what an IP address is
✓recognise an IPv4 address
✓understand public and private addresses at a simple level

Every device on a network needs an address, just as every house needs a street address. On the internet
that address is the IP address: a number that identifies one device on one network at one moment.

The most familiar form is IPv4: four numbers from 0 to 255, separated by dots, for example
192.168.1.42. Four numbers of eight bits each means an IPv4 address is really 32 bits, and there are
only about four billion of them, which the world has almost used up. IPv6, with much longer addresses,
solves that shortage.

**Public and private**
A public address is visible on the internet and belongs to one connection, like your school's line. A
private address is used inside your home or school network, such as 192.168.1.42, and is reused in
millions of homes. Your router translates between the two, which is why every device at home can share
one public address.

**●TRY IT**

**1**
Which of these could be IPv4 addresses: 192.168.0.5, 300.1.1.1, 10.0.4.77, 1.2.3.4.5?

**2**
Find the IP address of your school network with your teacher, and the private address of your
computer.

**3**
Why does every device on the school network need its own address, even though the school has one
public one?

**ROBOTICS CONNECTION**
A fleet of delivery robots communicates over the mobile network; each robot has its own address
so the control centre sends instructions to the right machine and not its neighbour.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
6

<!-- page 36 -->

---
**▮KEY WORDS**

**IP address a number identifying one device on a network**

**IPv4 four-number addresses, such as 192.168.1.42**

**public address an address visible on the internet**

**private address an address used only inside a local network**

**●CHALLENGE**

Your home has one public IP address but ten devices online. Draw how the router lets all ten share it,
and explain what could go wrong if two devices on the same network claimed the same private address.

**●CHECK YOUR UNDERSTANDING**

**1**
What is an IP address for?

**2**
How many numbers does an IPv4 address have, and what range?

**3**
What is the difference between a public and a private address?

**4**
Why did the world need IPv6?

**5**
Does your games console at home have a public or private address?

**●EXIT TICKET**

**1**
Write one example of a valid IPv4 address.

**2**
Who translates between public and private addresses?

**3**
Why must addresses be unique on a network?

<!-- page 37 -->

---
**UNIT 3 · TOPIC 4**
## Routers and Switches

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what a switch does
✓explain what a router does
✓trace the path from a computer to the internet

Two devices build every wired network. The switch connects the computers inside one building: it learns
which computer is on which cable and delivers each message only where it is needed.

The router connects your network to other networks, above all the internet. It chooses the best route
for data to travel, and it translates between your private addresses and the school's public one.

**The journey of a web page**

**Computer -> Switch -> Router -> Internet -> Server**
**(inside the school)   (the wider world)**

Your request hops from your computer to the switch, to the router, onto the internet, and reaches the
server holding the page. The page travels the same path back. Every hop takes a moment; the wonder is
how few moments the whole journey takes.

**●TRY IT**

**1**
Label this diagram: which box is the switch, which the router? [Classroom PCs] -> [?] -> [?] ->
Internet.

**2**
In one sentence each, state the switch's job and the router's job.

**3**
Why does a small home network often combine a switch, a router and wifi in one box?

**ROBOTICS CONNECTION**
Autonomous robots on a factory floor talk through industrial switches, and report to engineers
over a router and the internet. Inside the factory, speed matters, so switches; outside, reach
matters, so the router.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
8

<!-- page 38 -->

---
**▮KEY WORDS**

**switch a device that connects computers inside one network and delivers messages to the right one**

**router a device that joins networks together and chooses routes for data**

**●CHALLENGE**

Draw a full network diagram for a two-floor school: 30 computers, 2 switches, 1 router, wifi access
points and the internet link. Explain where you put the switches and why the router sits between the
switches and the internet.

**●CHECK YOUR UNDERSTANDING**

**1**
What does a switch do?

**2**
What does a router do?

**3**
Which device joins your network to the internet?

**4**
Why does a network need both devices?

**5**
Where does a message go after the switch?

**●EXIT TICKET**

**1**
Define switch and router.

**2**
Write the path from a classroom computer to a website.

**3**
Which device knows the way to other networks?

<!-- page 39 -->

---
**UNIT 3 · TOPIC 5**
## Communication Protocols

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what a protocol is
✓know HTTP/HTTPS and TCP/IP at a simple level
✓understand what DNS does

A protocol is an agreed set of rules for communication. Humans have protocols too: answering the
phone with 'hello', taking turns to speak, ending with 'goodbye'. Without agreed rules, two computers
talking would be noise.

Web pages travel by HTTP, the HyperText Transfer Protocol, or its secure version HTTPS, where the
content is encrypted so nobody can read it on the way. All internet data, whatever it is, is carried by
TCP/IP, a family of protocols that splits data into packets, numbers them, delivers them by any route
and reassembles them at the end.

**Finding names: DNS**
People remember names; computers need numbers. DNS, the Domain Name System, translates them.
Type prime-school examples like www.example.com and DNS finds the IP address of the server, in a
fraction of a second, like a phone book for the internet.

**●TRY IT**

**1**
Classify each as a protocol or a domain name: HTTPS, www.bbc.co.uk, TCP/IP, DNS.

**2**
Why does the padlock in the browser matter when you log in to a website?

**3**
What do you think happens if the DNS system cannot find a name?

**ROBOTICS CONNECTION**
Robots sharing a workspace follow protocols too: a fixed way to announce 'I am here, moving
north, priority 2'. Every brand of robot can then cooperate, exactly like every email server
cooperating through the same protocols.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
10

<!-- page 40 -->

---
**▮KEY WORDS**

**protocol an agreed set of rules for communication**

**HTTP/HTTPS the protocols of the web, HTTPS being the encrypted version**

**TCP/IP the protocols that carry all internet data in packets**

**DNS the system that translates names into IP addresses**

**●CHALLENGE**

Trace the full journey of typing a website name into a browser until the page appears: DNS, TCP/IP
packets, HTTP request and reply. Present it as a five-step numbered story for the class.

**●CHECK YOUR UNDERSTANDING**

**1**
What is a protocol?

**2**
What is the difference between HTTP and HTTPS?

**3**
What does TCP/IP do?

**4**
What does DNS translate?

**5**
Why must both computers follow the same protocol?

**●EXIT TICKET**

**1**
Define protocol.

**2**
Which protocol is secure, and how do you know when you are using it?

**3**
What happens without DNS?

<!-- page 41 -->

---
**UNIT 3 · TOPIC 6**
## Digital Communication

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓compare email, messaging, video calls and social media
✓choose the right tool for the message
✓communicate appropriately online

We communicate digitally in many ways. Email is formal and slow, perfect for school and work, with
attachments and a permanent record. Instant messaging is quick and informal. Video calls carry tone
and expression, ideal for meetings and family far away. Social media broadcasts to many people at once.

**Choosing well**

**TOOL**
**BEST FOR**
**BEWARE**

Email
formal messages, school, attachments
not instant; check your inbox

Instant message
quick questions, teamwork
easily misunderstood without tone

Video call
meetings, explanations
needs a quiet place and a good time

Social media
sharing news with many people
public, permanent, wide audience

Appropriate digital communication means matching the tool to the message and the audience: full
sentences and a greeting for a teacher; emoji-free clarity for a job application; nothing online that you
would not say face to face.

**●TRY IT**

**1**
Choose the best tool and explain why: telling a teacher you will miss tomorrow's lesson; asking a
partner a quick question during a project; showing your club's robot to the whole school.

**2**
Rewrite this message to a teacher properly: 'hey cant come 2morrow lol'.

**3**
Give one advantage and one disadvantage of doing group work over video call.

**ROBOTICS CONNECTION**
Robot teams in competitions communicate by radio with fixed message formats. Badly chosen
words or sloppy timing between humans causes the same failures as garbled robot messages:
nobody knows what to do next.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
12

<!-- page 42 -->

---
**▮KEY WORDS**

**digital communication communicating through connected devices**

**audience whoever will read or hear your message**

**netiquette good manners online**

**●CHALLENGE**

A classmate posts an embarrassing photo of you on a group chat. Write what you do: the message you
send them, who else you tell, and why you do not reply publicly with anger.

**●CHECK YOUR UNDERSTANDING**

**1**
Which communication tool is most formal?

**2**
Why can instant messages be misunderstood?

**3**
What is netiquette?

**4**
Name two things to check before posting anything.

**5**
Which tool fits a message to many people at once?

**●EXIT TICKET**

**1**
Name the four main digital communication tools.

**2**
Which would you use to write to a headteacher?

**3**
What is the golden rule of online communication?

<!-- page 43 -->

---
**UNIT 3 · TOPIC 7**
## Cybersecurity

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what cybersecurity means
✓recognise malware, phishing and password attacks
✓defend yourself: strong passwords, MFA, updates and backups

Cybersecurity means protecting devices, data and people from digital attacks. Most attacks are not
genius hacking; they are tricks that persuade a human to open the door.

**The common threats**

**THREAT**
**HOW IT WORKS**
**YOUR DEFENCE**

Malware and viruses
harmful programs that damage or spy
do not install unknown software; keep
systems updated
Phishing
fake emails and sites that imitate real ones
check the sender and address; never
rush
Password attacks
guessing or stealing passwords
long unique passwords; never reuse
them
Social engineering
pretending to be someone you trust
verify unusual requests through another
channel

**Building your defences**

**●FOUR HABITS THAT STOP MOST ATTACKS**

Strong passwords: three or four random words beat short complicated ones.

Multi-factor authentication: a code on your phone as well as the password.

Updates: they close the holes attackers use; install them promptly.

Backups: keep copies of important work somewhere separate.

**●TRY IT**

**1**
Rate these passwords weakest to strongest and explain: password7; BlueRocketHippoWindow;
P@ssw0rd!

**2**
Spot the phishing signs: 'Dear customer, your account will close in 1 hour, click here to keep it'.

**3**
List which of your accounts offer MFA, and switch on two of them this week.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
14

<!-- page 44 -->

---
**ROBOTICS CONNECTION**
Even robots get attacked: security researchers have shown they can take over poorly protected
toy drones and factory arms. Robot fleets, like your accounts, need strong passwords and
updates.

**▮KEY WORDS**

**cybersecurity protecting devices and data from digital attacks**

**malware software designed to harm or spy**

**phishing fake messages that imitate real companies to steal details**

**multi-factor authentication proving identity with a password plus a second proof**

**●CHALLENGE**

Audit your own digital defences: password strength, MFA, updates, backups. Give yourself a mark out of
4 for each and write one improvement you will make this week for each score below 3.

**●CHECK YOUR UNDERSTANDING**

**1**
What is cybersecurity?

**2**
What is phishing?

**3**
Why do long random-word passwords beat short complex ones?

**4**
What does MFA add to a password?

**5**
Why are updates a security matter?

**●EXIT TICKET**

**1**
Name three threats from this topic.

**2**
Write one rule for spotting a phishing email.

**3**
What are the four defensive habits?

<!-- page 45 -->

---
**UNIT 3 · TOPIC 8**
## Online Safety

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓protect personal information and privacy
✓understand your digital footprint
✓recognise and report cyberbullying
✓behave responsibly online

Everything you post, like and comment on leaves a trace. Together these traces form your digital
footprint, and it lasts far longer than you expect: future schools and employers can search it. The rule is
simple: post nothing you would not be happy for your headteacher, your grandmother and a stranger to
read.

Personal information, such as your address, phone number, school timetable and passwords, should be
shared rarely and only with people you trust. Privacy settings decide who can see what; check them on
every account, twice a year.

**Facing problems**

**●IF SOMETHING GOES WRONG ONLINE**

Do not reply to unkind or suspicious messages.

Save the evidence: screenshot the message or post.

Tell an adult you trust: a parent, a teacher, any member of staff.

Report the account or content through the platform's report button.

Cyberbullying is bullying through messages, posts or exclusion online. It is never the target's fault, and
reporting it is not weakness; it is exactly how the bullying is stopped.

**●TRY IT**

**1**
A new online friend asks which school you go to and for a photo of yourself. Decide what to share
and what not to, with reasons.

**2**
Search your own name in a search engine with a partner. What does your digital footprint show?

**3**
Write the four steps you would take if a classmate receives cruel messages in a group chat.

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
16

<!-- page 46 -->

---
**ROBOTICS CONNECTION**
School robots with cameras and microphones raise privacy questions: who may be recorded, and
where does the data go? Discussing a robot's data rules is the same skill as protecting your own.

**▮KEY WORDS**

**personal information details about you that others could misuse**

**digital footprint the trail of everything you do online**

**cyberbullying bullying carried out through messages and posts**

**privacy settings controls deciding who can see your content**

**●CHALLENGE**

Design a poster for Year 5 pupils: 'Be safe and kind online', with the four reporting steps, three things
never to share, and one memorable rule about the digital footprint.

**●CHECK YOUR UNDERSTANDING**

**1**
What is a digital footprint?

**2**
Name three pieces of personal information never to post.

**3**
What should you do first when you see cyberbullying?

**4**
Why do privacy settings matter?

**5**
Who can you tell when something online worries you?

**●EXIT TICKET**

**1**
Define digital footprint.

**2**
Write two things never to share online.

**3**
What are the four steps when something goes wrong?

**UNIT 3 · NETWORKS AND DIGITAL COMMUNICATION**
17

<!-- page 47 -->

---
**UNIT 4 · TOPIC 1**
## Hardware

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what hardware is
✓name the main internal and external components of a computer

Hardware means the physical parts of a computer: everything you can touch. Software, by contrast, is
the set of instructions that runs on it. A computer without software is a very expensive paperweight;
software without hardware is a daydream.

**Inside the case**

**●INTERNAL HARDWARE**

CPU: the processor, the brain that carries out instructions

RAM: working memory for programs that are running

Motherboard: the big circuit board connecting everything

Power supply: converts mains electricity into usable power

Storage drive (HDD or SSD): keeps your files when off

**Outside the case**
External hardware is everything attached to the case: the keyboard, mouse, monitor, headphones,
printer and camera. Some devices, such as a touchscreen, are both input and output.

**●TRY IT**

**1**
Classify as internal or external: CPU, monitor, RAM, mouse, motherboard, printer.

**2**
Choose the odd one out and justify: keyboard, mouse, monitor, microphone.

**3**
Why is a touchscreen both an input and an output device?

**ROBOTICS CONNECTION**
A robot is a computer wearing sensors and motors. Its hardware adds distance sensors, line
followers, motor controllers and battery systems to the same CPU, RAM and storage you find in a
laptop.

**UNIT 4 · COMPUTER SYSTEMS**
1

<!-- page 48 -->

---
**▮KEY WORDS**

**hardware the physical parts of a computer system**

**software the programs that run on hardware**

**component one part of a computer system**

**●CHALLENGE**

Design a specification for a classroom robot on paper: list at least eight hardware components, internal
and external, and explain what each one contributes.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between hardware and software?

**2**
Name three internal hardware components.

**3**
Name three external devices.

**4**
Which internal component is the 'brain'?

**5**
Where do your files live when the computer is off?

**●EXIT TICKET**

**1**
Define hardware.

**2**
Name two internal and two external components.

**3**
Is a robot's motor hardware or software?

<!-- page 49 -->

---
**UNIT 4 · TOPIC 2**
## The CPU

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what the CPU does
✓name the parts of the CPU
✓understand the fetch-decode-execute cycle

The CPU, or Central Processing Unit, is the brain of the computer. Every instruction in every program,
from a game to a spreadsheet, is carried out by the CPU, one instruction at a time, billions of times per
second.

**Inside the CPU**

**PART**
**JOB**

Control Unit
directs traffic: fetches instructions and tells the other parts what to do

ALU (Arithmetic Logic Unit)
does the maths and the comparisons: add, subtract, greater than, equal

Registers
tiny ultra-fast stores holding the instruction being worked on right now

**The fetch-decode-execute cycle**

**FETCH     fetch the next instruction from memory**
**DECODE    work out what the instruction means**
**EXECUTE   do it**
**^________________________ repeat, billions of times**
**|                         per second**

The CPU repeats this cycle endlessly. The faster it can loop, the more work it does each second, which is
what processor speed, measured in gigahertz, really means.

**●TRY IT**

**1**
Which CPU part handles 'is 7 greater than 3'?

**2**
Put in order: execute, fetch, decode.

**3**
A robot checks its distance sensor and decides to turn. Which CPU parts are involved, in which
order?

**UNIT 4 · COMPUTER SYSTEMS**
3

<!-- page 50 -->

---
**ROBOTICS CONNECTION**
A robot's processor runs the same cycle: fetch the next line of the control program, decode it,
execute it by reading a sensor or driving a motor, repeat. Real-time robots must complete the
cycle fast enough to react before hitting a wall.

**▮KEY WORDS**

**CPU Central Processing Unit, the processor that carries out instructions**

**Control Unit the CPU part that coordinates the work**

**ALU the CPU part that does calculations and comparisons**

**fetch-decode-execute the endless cycle the CPU follows**

**●CHALLENGE**

Write a program of six simple instructions for a robot on paper. Annotate each instruction to show what
the CPU does at fetch, decode and execute when it processes it.

**●CHECK YOUR UNDERSTANDING**

**1**
What does the CPU do?

**2**
Which part of the CPU does calculations?

**3**
What are registers for?

**4**
Name the three stages of the CPU cycle in order.

**5**
What does processor speed measure?

**●EXIT TICKET**

**1**
Define CPU.

**2**
What does ALU stand for?

**3**
Write the CPU cycle from memory.

<!-- page 51 -->

---
**UNIT 4 · TOPIC 3**
## RAM and ROM

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what RAM and ROM do
✓know the difference between volatile and non-volatile memory
✓understand why computers need memory

RAM, Random Access Memory, is the computer's working memory. Whatever programs are running, and
the data they are using, live in RAM because it is fast. RAM is volatile: it forgets everything the instant
the power goes off.

ROM, Read Only Memory, is the computer's permanent start-up instructions, written in the factory. It is
non-volatile: it survives power cuts. That is the point; it is how the computer knows how to wake up.

**RAM**
**ROM**

Purpose
holds running programs and their data
holds permanent start-up
instructions
Volatile?
yes: empty when power is off
no: keeps contents forever

Can you change it?
constantly, while working
no; it is read only

Size in a laptop
gigabytes
a few megabytes

Computers need both: ROM to start, RAM to work. When teachers say 'save your work', they mean
copying it from RAM, which will vanish, into storage, which will not.

**●TRY IT**

**1**
Why does unsaved work disappear when a computer crashes?

**2**
Why is ROM needed at all, if RAM is so fast?

**3**
Your program feels slow with many tabs open. Which memory is filling up?

**ROBOTICS CONNECTION**
A robot reads its program from storage into RAM to run it. Sensor readings also live briefly in
RAM. Losing power mid-run wipes the robot's memory of where it was, which is why robots
re-homing after a restart.

**UNIT 4 · COMPUTER SYSTEMS**
5

<!-- page 52 -->

---
**▮KEY WORDS**

**RAM fast working memory, lost when power is off**

**ROM permanent read-only memory holding start-up instructions**

**volatile loses its contents without power**

**●CHALLENGE**

Explain, as a story from pressing the power button to opening a program, exactly what ROM and RAM
each do along the way. Five sentences minimum.

**●CHECK YOUR UNDERSTANDING**

**1**
What does RAM stand for and do?

**2**
What does ROM hold?

**3**
Which memory is volatile?

**4**
Why is RAM bigger than ROM in a laptop?

**5**
What does saving really do?

**●EXIT TICKET**

**1**
Define volatile.

**2**
Which memory survives a power cut, and why must it?

**3**
Where does a running program live?

<!-- page 53 -->

---
**UNIT 4 · TOPIC 4**
## Input and Output Devices

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain input and output
✓classify devices as input, output or both
✓know the special role of sensors and actuators

An input device sends data into the computer; an output device brings data out to you. A keyboard
inputs characters; a monitor outputs images. Simple rule: data flowing in is input; data flowing out is
output.

**The catalogue**

**INPUT**
**OUTPUT**
**BOTH**

keyboard
monitor
touchscreen

mouse
printer
smartboard

microphone
speakers
headset with mic

camera
projector

sensors
actuators (motors)

Sensors are inputs that measure the world: temperature, light, distance. Actuators are outputs that act
on the world: motors, grippers, buzzers. Together they are the input and output of robotics.

**●TRY IT**

**1**
Classify each: webcam, scanner, headphones, joystick, plotter, thermometer sensor.

**2**
For a door-opening robot, name one input and two output devices it would need.

**3**
Why is a headset with microphone both input and output?

**ROBOTICS CONNECTION**
Every robot is an input-process-output machine: sensors in, decisions made, actuators out. A
line-following robot inputs light readings and outputs motor speeds, many times per second.

**UNIT 4 · COMPUTER SYSTEMS**
7

<!-- page 54 -->

---
**▮KEY WORDS**

**input device hardware that sends data into the computer**

**output device hardware that presents data from the computer**

**sensor an input that measures the real world**

**actuator an output that acts on the real world**

**●CHALLENGE**

Design the input and output hardware for a robot guide dog for a blind pupil. List at least three sensors
and three actuators, and explain what each is for.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between input and output?

**2**
Is a printer input or output?

**3**
Name two devices that are both.

**4**
What does a sensor do?

**5**
What is an actuator?

**●EXIT TICKET**

**1**
Give one example each of input and output.

**2**
Classify: microphone, projector, touchscreen.

**3**
Why does a robot need both sensors and actuators?

<!-- page 55 -->

---
**UNIT 4 · TOPIC 5**
## Secondary Storage

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓name the main kinds of secondary storage
✓compare them on capacity, speed, portability, reliability and cost

Secondary storage keeps your files when the power is off. There are more choices than ever, each with
strengths.

**TYPE**
**STRENGTH**
**WEAKNESS**

HDD (hard disk drive)
cheap per gigabyte, large
mechanical, slower, fragile when dropped

SSD (solid state drive)
very fast, silent, no moving parts
more expensive per gigabyte

USB flash drive
tiny and pocketable
easy to lose, limited capacity

Memory card
fits cameras and small devices
small, easy to lose

Optical disc (CD/DVD)
cheap archive, lasts well stored
slow, small capacity

Cloud storage
anywhere access, safe from loss
needs internet; ongoing cost

Choosing storage is a balancing act: capacity, speed, portability, reliability and cost. A film editor needs
fast SSDs; a family archive may prefer cloud plus one external drive.

**●TRY IT**

**1**
Recommend storage for each, with reasons: a school report; a holiday film collection; photos to post
to a friend; a 10-year family archive.

**2**
Why are SSDs replacing HDDs in laptops, but HDDs survive in data centres?

**3**
Which storage would fail first if dropped: HDD or SSD? Why?

**ROBOTICS CONNECTION**
Small robots use memory cards and flash chips for programs and sensor logs. Space missions
choose storage that survives radiation and years without power, so 'reliable' beats 'fast' and
'cheap'.

**UNIT 4 · COMPUTER SYSTEMS**
9

<!-- page 56 -->

---
**▮KEY WORDS**

**secondary storage storage that keeps data when power is off**

**HDD hard disk drive: spinning magnetic disks**

**SSD solid state drive: fast storage with no moving parts**

**●CHALLENGE**

You have 60 euros to store 100 GB of robot competition video. Research or estimate prices of USB
drives, memory cards, an external HDD and cloud subscriptions, and justify your choice on all five
criteria.

**●CHECK YOUR UNDERSTANDING**

**1**
What does secondary storage do?

**2**
Name three types of secondary storage.

**3**
Why is an SSD faster than an HDD?

**4**
Which is most portable?

**5**
Give one advantage of cloud storage.

**●EXIT TICKET**

**1**
Define secondary storage.

**2**
SSD or HDD: which has moving parts?

**3**
Name the five comparison criteria.

<!-- page 57 -->

---
**UNIT 4 · TOPIC 6**
## Operating Systems

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain what an operating system does
✓name its main jobs
✓recognise common operating systems

The operating system, or OS, is the manager of the whole computer. Applications never talk to hardware
directly; the OS sits between them, sharing the machine fairly and safely.

**●WHAT THE OS DOES**

user interface: the screen, windows and icons you interact with

file management: folders, saving, deleting, finding files

device management: making keyboard, printer and camera work

memory management: dividing RAM between running programs

security: passwords, permissions, keeping programs apart

You have met several: Windows and macOS on computers, Linux on servers, Android and iOS on phones.
They look different but do the same five jobs.

**●TRY IT**

**1**
Which OS runs your phone? Which runs the school computers?

**2**
Your game slows down when many programs run. Which OS job is under pressure?

**3**
Why does the OS, and not each program, manage the printer?

**ROBOTICS CONNECTION**
Robots run operating systems too: many use special real-time ones, and popular robots run ROS,
the Robot Operating System, which manages sensors and motors the way your phone's OS
manages the touchscreen.

**UNIT 4 · COMPUTER SYSTEMS**
11

<!-- page 58 -->

---
**▮KEY WORDS**

**operating system the core software managing hardware and programs**

**user interface the part of a system you see and touch**

**resource management sharing CPU, memory and devices fairly**

**●CHALLENGE**

Compare the OS on your phone and on a school computer: list three things they do identically and three
ways they differ, and explain why phones and laptops need different designs.

**●CHECK YOUR UNDERSTANDING**

**1**
What is an operating system?

**2**
Name two jobs of the OS.

**3**
Name three operating systems.

**4**
Why do applications not talk to hardware directly?

**5**
Which OS job protects your files with a password?

**●EXIT TICKET**

**1**
Define operating system.

**2**
Name two operating systems.

**3**
Who shares RAM between programs?

<!-- page 59 -->

---
**UNIT 4 · TOPIC 7**
## System and Application Software

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓distinguish system software from application software
✓classify examples of each

System software runs the computer: the operating system, its tools and the drivers that speak to
hardware. Application software does the jobs you actually want: writing, browsing, editing photos,
playing games.

The test is simple: does it help the computer run, or does it help you do something? If the computer
could run without it, it is an application; if the computer cannot run without it, it is system software.

**SYSTEM SOFTWARE**
**APPLICATION SOFTWARE**

Windows 11, macOS, Linux
word processor, presentation app

device drivers
web browser, email client

disk and file tools
photo editor, video editor

security tools built into the OS
games, educational apps

**●TRY IT**

**1**
Classify each: web browser, operating system, spreadsheet app, driver, antivirus that came with the
OS, photo editor.

**2**
Why is a web browser an application, not system software?

**3**
Which piece of software does every application depend on?

**ROBOTICS CONNECTION**
A robot's firmware and control system are system software; the program that makes it dance is an
application. Robots fail when hobbyists change system parts carelessly.

**UNIT 4 · COMPUTER SYSTEMS**
13

<!-- page 60 -->

---
**▮KEY WORDS**

**system software programs that run and manage the computer itself**

**application software programs that do tasks for the user**

**driver system software that lets the OS talk to one device**

**●CHALLENGE**

Make a poster sorting twelve programs into system and application software. Add three tricky cases,
such as antivirus and file managers, with a sentence defending each decision.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between system and application software?

**2**
Give two examples of each.

**3**
What does a driver do?

**4**
Which type would a game be?

**5**
Why does every application need the OS?

**●EXIT TICKET**

**1**
Define both types of software.

**2**
Classify: word processor, driver.

**3**
Which type is an operating system?

<!-- page 61 -->

---
**UNIT 4 · TOPIC 8**
## How Computers Process Data

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓explain input, processing, output and storage
✓trace the four stages in real systems
✓connect the model to robotics

Every computer system, from a smartwatch to a weather satellite, follows the same pattern: input,
processing, output, storage. Data comes in, the processor works on it, results go out, and important
data is kept.

**INPUT  ->  PROCESSING  ->  OUTPUT**
**|**
**STORAGE**

**The model in action**

**●EXAMPLES**

A calculator: you press keys (input), the processor computes (processing), the screen shows the result
(output), nothing is saved (storage: none).

A cash machine: your card (input), the bank check (processing), cash and a receipt (output), the
transaction recorded (storage).

A smart speaker: your voice (input), speech recognition and the answer (processing), the speaker's reply
(output), your preferences (storage).

**●TRY IT**

**1**
Label input, processing, output and storage for: a self-service checkout; a school attendance
system; a fitness tracker.

**2**
Which stage is missing in a plain calculator?

**3**
Why must an attendance system include storage?

**ROBOTICS CONNECTION**
A robot is the same model in motion: Sensor -> CPU -> Decision -> Motor. Input is the distance
reading, processing is the comparison 'too close?', output is the stop command to the motors, and
storage is the robot's log of what it did.

**UNIT 4 · COMPUTER SYSTEMS**
15

<!-- page 62 -->

---
**▮KEY WORDS**

**input data entering a system**

**processing working on data to produce meaning**

**output the result leaving a system**

**storage keeping data for later**

**●CHALLENGE**

Choose any device in your home with a processor, such as a microwave or a washing machine. Map all
four stages in detail, then draw the same diagram for a robot vacuum cleaner and compare them.

**●CHECK YOUR UNDERSTANDING**

**1**
Name the four stages in order.

**2**
Which stage happens in the CPU?

**3**
Give an input and an output for a microwave.

**4**
Which stage does a light sensor represent in a robot?

**5**
Why is storage part of the model?

**●EXIT TICKET**

**1**
Write the four-stage model from memory.

**2**
Give one example of each stage in a games console.

**3**
How does the model apply to robots?

**UNIT 4 · COMPUTER SYSTEMS**
16

<!-- page 63 -->

---
**UNIT 5 · TOPIC 1**
## Introduction to the micro:bit

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓say what the micro:bit is and what it is used for
✓explain the microcontroller idea
✓understand physical computing

The BBC micro:bit is a pocket-sized circuit board designed for learning. It has a processor, a grid of
lights, buttons, sensors and connector pins. You write a program on a computer, send it to the micro:bit,
and the board runs it on its own, without the computer.

At its heart is a microcontroller: a small computer built onto one chip, with its processor, memory and
input-output all together. Washing machines, drones and car brakes run on microcontrollers; the
micro:bit lets you learn the same technology safely.

This is physical computing: programs that sense and change the real world, not just a screen. A
micro:bit program can read how hot the room is, and respond by lighting up or playing a sound.

**What people build with micro:bits**

**●EXAMPLES**

a step counter that senses movement

a compass that shows direction on its lights

a plant waterer that senses dry soil and opens a valve

a radio messaging device between two micro:bits

the brain of a small robot buggy

**●TRY IT**

**1**
Which of the five examples above interest you most? Explain why in two sentences.

**2**
Why is a micro:bit better than a laptop for building a small robot?

**3**
Find the processor, buttons, light grid and pins on a micro:bit, and point to each.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
1

<!-- page 64 -->

---
**ROBOTICS CONNECTION**
This unit's robotics all runs on the micro:bit: it reads the sensors, makes the decisions and drives
the motors. Everything you learn about it transfers to real robots.

**▮KEY WORDS**

**micro:bit a pocket programmable board for learning physical computing**

**microcontroller a complete tiny computer on one chip**

**physical computing programs that sense and control the real world**

**●CHALLENGE**

Invent a micro:bit gadget for the school library: state the problem, the sensors you would use, what the
outputs would do, and why a microcontroller fits the job better than a full computer.

**●CHECK YOUR UNDERSTANDING**

**1**
What is a micro:bit?

**2**
What is a microcontroller?

**3**
Name three things a micro:bit can do.

**4**
What is physical computing?

**5**
Why do washing machines use microcontrollers?

**●EXIT TICKET**

**1**
Define microcontroller.

**2**
Name two sensors on the micro:bit.

**3**
Why does the micro:bit run without a computer attached?

<!-- page 65 -->

---
**UNIT 5 · TOPIC 2**
## What is the micro:bit?

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓identify the parts of a micro:bit board
✓know what each part does

Look closely at the board and you find a complete computer, laid out for your eyes.

**PART**
**WHAT IT IS**
**WHAT IT DOES**

LED matrix
25 small lights in a 5 by 5 grid
shows images, text and patterns

Buttons
two labelled buttons A and B
input you control with your thumb

Pins
metal contacts along the edge
connect sensors, motors and other parts

Sensors
built-in measuring devices
light, temperature, compass, movement

Processor
the chip at the heart of the board
runs your program

USB port
the connector at the top
power and transferring programs

Radio and Bluetooth
wireless communication
talks to other micro:bits and devices

Battery holder
connectors for two AAA batteries
makes the project portable

**●TRY IT**

**1**
Without looking at the table, sketch the front of a micro:bit and label six parts.

**2**
Which part is input, which output, and which both: buttons, LED matrix, pins?

**3**
Why does the LED matrix have 25 lights rather than a screen?

**ROBOTICS CONNECTION**
For robotics you use nearly every part: pins drive the motors, sensors watch the world, buttons
start and stop the program, and radio lets two robots talk.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
3

<!-- page 66 -->

---
**▮KEY WORDS**

**LED matrix the 5 by 5 grid of lights on the micro:bit**

**pin a metal contact for connecting circuits**

**port a connection point for cables and devices**

**●CHALLENGE**

Design a labelled diagram poster of the micro:bit for the classroom wall: every part named, with one
plain-English sentence about its job.

**●CHECK YOUR UNDERSTANDING**

**1**
How many lights are in the LED matrix?

**2**
What are the buttons called?

**3**
What are pins for?

**4**
Name two built-in sensors.

**5**
What does the USB port do?

**●EXIT TICKET**

**1**
Name five parts of the micro:bit.

**2**
Which parts give input and which give output?

**3**
What powers the micro:bit away from a computer?

<!-- page 67 -->

---
**UNIT 5 · TOPIC 3**
## How do computers work?

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓apply the input-process-output model to the micro:bit
✓trace simple micro:bit systems

The micro:bit is the input-process-output model from Unit 4, made real. Inputs arrive from buttons and
sensors. The processor runs your program on them. Outputs leave through the lights, pins and speaker.

**INPUT              PROCESS            OUTPUT**
**Button A  ---->  your program  ---->  happy face**
**temperature --->  compares to 20  --> hot icon**
**compass    --->  finds north    ---> arrow**

**Two complete systems**

**●EXAMPLES**

Button -> micro:bit -> LED: press button A, and the program lights the whole grid. Input, process,
output.

Temperature sensor -> micro:bit -> display: the program reads the temperature, compares it with 20,
and shows a sun or a snowflake.

**●TRY IT**

**1**
For each example above, name the input device, the processing rule and the output device.

**2**
Design input, process and output for a doorbell that shows a different image by day and night.

**3**
Which of the five flowchart symbols from Unit 1 would the day-or-night test use?

**ROBOTICS CONNECTION**
The robot pattern is Sensor -> CPU -> Decision -> Motor. The micro:bit is the CPU; its pins connect
the sensors and motors. Every robot program, however fancy, is this loop repeating.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
5

<!-- page 68 -->

---
**▮KEY WORDS**

**input data entering the micro:bit**

**process the program working on that data**

**output the micro:bit acting on the result**

**●CHALLENGE**

Draw the input-process-output diagram for a nightlight: light sensor in, a decision, the LED grid out.
Then extend it with a second output, a sound, and explain what changes in the program.

**●CHECK YOUR UNDERSTANDING**

**1**
Name three inputs and three outputs of the micro:bit.

**2**
What does the processing?

**3**
Trace 'button B pressed shows a heart'.

**4**
What is the robot version of the model?

**5**
Can one program have several inputs? Give an example.

**●EXIT TICKET**

**1**
Write the model from memory.

**2**
Give one input and one output for a step counter.

**3**
Where does the decision happen?

<!-- page 69 -->

---
**UNIT 5 · TOPIC 4**
## Set up the micro:bit

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓connect and program a micro:bit
✓transfer, run and test a program
✓troubleshoot common problems

The micro:bit needs no installation: everything happens in the browser. This is the workflow for every
project in this unit.

**●THE WORKFLOW**

Connect: plug the micro:bit into the computer with a USB cable.

Open the editor: go to python.microbit.org (or makecode.microbit.org for blocks).

Create: write your program in the editor.

Transfer: click Send to micro:bit, or download the file and drag it onto the MICROBIT drive.

Run: the yellow light on the back flashes while the program transfers, then the program starts by itself.

Test: try the inputs. Does it do what you expected?

Debug: if not, change the program and send it again.

**When something will not work**

**SYMPTOM**
**LIKELY CAUSE**
**FIX**

No MICROBIT drive appears
cable is power-only or port is loose
use a data USB cable; re-plug
firmly
Yellow light never stops flashing
program too big, or drive nearly full
delete old files from the drive;
resend
Nothing happens on the grid
program error or batteries flat
check the error message; replace
batteries
Wrong program runs
old file still on the drive
re-send and wait for the flash to
finish

Always eject the MICROBIT drive before unplugging the cable, exactly as with a memory stick.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
7

<!-- page 70 -->

---
**●TRY IT**

**1**
Send the sample 'Hello, World' program to a micro:bit and make it scroll your name.

**2**
Deliberately send a program with a spelling mistake in a command. Read the error and fix it.

**3**
Time how long the transfer takes for the whole class, and suggest a fair way to share the cables.

**ROBOTICS CONNECTION**
Robot projects add a motor board connected to the micro:bit pins. The workflow is the same, plus
one rule: disconnect the battery pack before changing any wiring.

**▮KEY WORDS**

**flash transferring a program to the board**

**MICROBIT drive how the board appears on your computer when plugged in**

**troubleshooting a systematic search for the cause of a fault**

**●CHALLENGE**

Write the class troubleshooting guide for the micro:bit: the five most common problems, their
symptoms, causes and fixes, ready to laminate for the robot club table.

**●CHECK YOUR UNDERSTANDING**

**1**
Where do you write micro:bit programs?

**2**
What does the yellow flashing light mean?

**3**
Why might the MICROBIT drive not appear?

**4**
What must you do before unplugging the board?

**5**
What is the last step after testing fails?

**UNIT 5 · MICRO:BIT AND ROBOTICS**
8

<!-- page 71 -->

---
**●EXIT TICKET**

**1**
List the workflow steps from memory.

**2**
Name two troubleshooting fixes.

**3**
Why does the program start on its own after transfer?

<!-- page 72 -->

---
**UNIT 5 · TOPIC 5**
## Programming concepts

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓use sequence, selection and repetition
✓use variables, inputs, outputs and events

Every micro:bit program, however creative, is built from the same seven ideas.

**CONCEPT**
**MEANING**
**MICRO:BIT EXAMPLE**

Sequence
instructions run in order
show image, pause, show another

Selection
choosing between paths with IF
IF button A pressed, show a smile

Repetition
repeating instructions with loops
scroll a message forever

Variables
named stores for values that change
score = score + 1

Inputs
data arriving from buttons and sensors
reading the temperature

Outputs
the board acting on the world
lighting the grid, playing a sound

Events
instructions triggered when something
happens

on button A pressed

Events deserve a special note: instead of running top to bottom only, an event lets the program react.
'On shake' or 'on button A' means: whenever this happens, run this block.

**●TRY IT**

**1**
A program shows a smiley, waits a second, then shows a heart, forever. Which concepts are used?

**2**
Turn 'if the room is dark, show a star' into an event version that reacts continuously.

**3**
Design a two-button counter: A adds one, B resets to zero. Which concepts appear?

**ROBOTICS CONNECTION**
A robot's program is usually one endless loop: read sensors, decide, drive motors, repeat. Inside
the loop, selection handles obstacles, and variables remember where the robot has been.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
10

<!-- page 73 -->

---
**▮KEY WORDS**

**sequence instructions executed one after another**

**selection choosing between alternatives with IF**

**repetition running instructions again with a loop**

**event a trigger that starts instructions when something happens**

**●CHALLENGE**

Take the two-button counter and extend it: the micro:bit should also count shakes, show the total when
both buttons are pressed, and never go above 99. List every concept your final program uses.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between sequence and selection?

**2**
What does a loop do?

**3**
Why are variables useful in a game program?

**4**
Name two micro:bit inputs and two outputs.

**5**
What is an event? Give an example.

**●EXIT TICKET**

**1**
Name the three core control concepts.

**2**
Write one event for the micro:bit.

**3**
What kind of structure does a robot's main program usually have?

<!-- page 74 -->

---
**UNIT 5 · TOPIC 6**
## The pins: a user guide

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓know what the pins are for
✓distinguish input and output pins
✓use pins safely

The metal strips along the bottom edge of the micro:bit are the pins. They are the board's hands:
connections through which it senses and controls other circuits. Big pins, labelled 0, 1, 2, 3V and GND,
take crocodile clips; the small pins connect to edge-connector boards for robotics.

**Input pins and output pins**
An input pin receives information: a homemade switch, a moisture sensor, another chip. An output pin
sends commands: lighting an external LED, driving a motor through a control board. The 3V pin supplies
small amounts of power; GND is the return path every circuit needs.

**Safety rules**

**●PIN RULES**

Never connect a pin straight to a battery or mains power.

Only connect components your teacher has provided.

Connect and disconnect circuits while power is off.

Static electricity from a jumper can damage the chip: touch something metal first.

Keep wires neat and short so they cannot short-circuit each other.

**●TRY IT**

**1**
Label a diagram of the edge connector: pin 0, pin 1, pin 2, 3V, GND.

**2**
Plan a circuit that lights an external LED when button A is pressed: which pins would you use and
why?

**3**
Explain the GND rule to a Year 6 pupil in two sentences.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
12

<!-- page 75 -->

---
**ROBOTICS CONNECTION**
Robot buggies use the pins for everything: motor boards draw power through 3V and GND, and
receive speed and direction commands on pins 0 and 1. Respecting pin limits is what keeps the
board alive.

**▮KEY WORDS**

**pin a contact on the micro:bit edge for connecting circuits**

**GND the ground pin, the return path of every circuit**

**short circuit an accidental path with no resistance, which damages parts**

**●CHALLENGE**

Design on paper a pin plan for a buggy with two motors, a line sensor and a headlight: allocate pins,
mark power connections, and add two safety notes for the user guide you are writing.

**●CHECK YOUR UNDERSTANDING**

**1**
What are the five big pins called?

**2**
What is the difference between an input and an output pin?

**3**
What does GND do?

**4**
Why never connect a pin straight to power?

**5**
How do robot motors connect to the micro:bit?

**●EXIT TICKET**

**1**
Name the pins from memory.

**2**
Which pin never changes and why?

**3**
Write one safety rule for pins.

<!-- page 76 -->

---
**UNIT 5 · TOPIC 7**
## Block coding

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓build programs with blocks in MakeCode
✓use events, loops, conditions and variables in blocks

MakeCode, at makecode.microbit.org, lets you build micro:bit programs by dragging coloured blocks
that click together, like Scratch. Blocks that make no sense refuse to join, so many mistakes are
impossible before you even run the program.

**The block families you will use**

**●BLOCK FAMILIES**

Basic: show an image, scroll text, pause

Input: events on buttons, shake, tilt and pins

Loops: repeat, while, for each value

Logic: IF/ELSE conditions and comparisons

Variables: make and change a variable

Radio: send and receive messages between micro:bits

The habits from Unit 1 map straight across: an algorithm becomes blocks, a decision becomes a Logic
diamond, a repeated pattern becomes a Loop block.

**●TRY IT**

**1**
Build a program that shows a different image for each of: button A, button B and shake.

**2**
Build an endless animation of at least four frames, half a second apart.

**3**
Build a score counter: A adds one, B takes one away, both buttons together show the score.

**ROBOTICS CONNECTION**
MakeCode also drives robots: motor blocks, sensor blocks and radio blocks combine into buggy
programs without a single typed line, ideal for first robotics.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
14

<!-- page 77 -->

---
**▮KEY WORDS**

**MakeCode the block editor for the micro:bit**

**block a ready-made instruction shape that clicks with others**

**●CHALLENGE**

Build a two-player reaction game in blocks: each player has a button; when the grid flashes after a
random wait, the first press scores; first to five wins and the micro:bit celebrates. List the block families
you used.

**●CHECK YOUR UNDERSTANDING**

**1**
What is MakeCode?

**2**
Which block family holds IF/ELSE?

**3**
Which block family would you use to make a variable?

**4**
What are the three input events used in the first Try It?

**5**
Why are loops useful in an animation?

**●EXIT TICKET**

**1**
Name three block families.

**2**
How does a loop appear in blocks?

**3**
What connects blocks to the micro:bit?

<!-- page 78 -->

---
**UNIT 5 · TOPIC 8**
## Introduction to MicroPython

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓know what MicroPython is
✓write short programs with variables, IF, loops and functions

MicroPython is a small version of Python made to run on microcontrollers like the micro:bit. The same
language you will meet in larger machines, trimmed to fit a pocket-sized board. You write it at
python.microbit.org.

**from microbit import ***

**while True:**
**if button_a.is_pressed():**
**display.show(Image.HAPPY)**
**elif button_b.is_pressed():**
**display.show(Image.SAD)**
**else:**
**display.clear()**

Read it slowly: import the micro:bit commands, then repeat forever: if A is pressed show a happy face,
otherwise if B is pressed show a sad face, otherwise show nothing. Indentation, the spaces at the start
of lines, tells Python which instructions belong where.

**A function of your own**

**def flash(n):**
**for i in range(n):**
**display.show(Image.HEART)**
**sleep(300)**
**display.clear()**
**sleep(300)**

**flash(3)**

A function is a named block you write once and use many times. flash(3) now means 'flash the heart
three times' anywhere in the program.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
16

<!-- page 79 -->

---
**●TRY IT**

**1**
Type the first program and change the images.

**2**
Predict what flash(3) does before running it, then check.

**3**
Write a function cheer() that shows three different images in a row.

**ROBOTICS CONNECTION**
Serious robotics teams program in MicroPython because text scales: as programs grow, typed
code stays manageable while piles of blocks become unreadable.

**▮KEY WORDS**

**MicroPython a small version of Python for microcontrollers**

**indentation the leading spaces that group Python instructions**

**function a named block of instructions you can reuse**

**●CHALLENGE**

Write a MicroPython nightlight: read the light sensor forever; if dark, show a dim heart; if very dark,
show a bright one; otherwise clear the display. Then wrap the display part in a function.

**●CHECK YOUR UNDERSTANDING**

**1**
What is MicroPython?

**2**
What does indentation do?

**3**
What does 'while True:' create?

**4**
Why write functions?

**5**
How do you run a MicroPython program on the board?

**UNIT 5 · MICRO:BIT AND ROBOTICS**
17

<!-- page 80 -->

---
**●EXIT TICKET**

**1**
Write the first line of every micro:bit program.

**2**
What is a function?

**3**
Which symbol ends a line that starts a block?

<!-- page 81 -->

---
**UNIT 5 · TOPIC 9**
## Images

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓display images on the LED matrix
✓create your own images
✓animate images

The 5 by 5 grid displays built-in images with a single line: display.show(Image.HAPPY) lights a set
pattern. There are dozens ready-made, from DUCK to GHOST.

Your own images are drawn as strings of digits, one digit per light, 0 meaning off and 9 meaning fully on.

**boat = Image("05050:05050:05050:99999:09990")**
**display.show(boat)**

Each row of five digits is one row of lights, and the rows are separated by colons. Change the digits and
the picture changes; every number between 0 and 9 is a brightness.

**Animation**

**frames = [Image("00000:00000:00900:00000:00000"),**
**Image("00000:00900:00900:00900:00000"),**
**Image("00900:00900:00900:00900:00900")]**
**display.show(frames, delay=200, loop=True)**

A list of frames shown one after another, looping, is an animation, exactly like a flick book.

**●TRY IT**

**1**
Draw your initial on the grid as a string of digits.

**2**
Make a two-frame blinking eye animation.

**3**
Adjust the delay until the animation looks right; note the value.

**ROBOTICS CONNECTION**
A robot's face is its interface: robot designers use exactly this technique, grids of lights showing
expressions, so people can read what the machine intends to do.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
19

<!-- page 82 -->

---
**▮KEY WORDS**

**image string digits describing which lights are on, 0 to 9**

**frame one still picture of an animation**

**delay how long each frame shows, in milliseconds**

**●CHALLENGE**

Create your own micro:bit icon: a personal logo drawn on the grid, shown as a three-frame animation
with a smooth entrance and exit. Document the digit strings in your book.

**●CHECK YOUR UNDERSTANDING**

**1**
How many lights does the matrix have?

**2**
What do the digits 0 and 9 mean in an image string?

**3**
What separates the rows in an image string?

**4**
How do you make an animation?

**5**
What does delay control?

**●EXIT TICKET**

**1**
Write an image string for a heart.

**2**
How many frames make an animation?

**3**
What is the command to show an image?

<!-- page 83 -->

---
**UNIT 5 · TOPIC 10**
## Buttons

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓use button A, button B and A+B together
✓write event-driven programs
✓build a reaction game

The two buttons are the micro:bit's simplest and most reliable inputs. Each can be tested on its own, and
pressing both at once counts as a third input, A+B.

**from microbit import ***

**while True:**
**if button_a.is_pressed() and button_b.is_pressed():**
**display.scroll("BOTH")**
**elif button_a.is_pressed():**
**display.scroll("A")**
**elif button_b.is_pressed():**
**display.scroll("B")**

Notice the order: the two-button test comes first. If the single-button tests came first, A+B would never
be reached, because pressing A is also true when both are pressed. Order of tests matters.

**●TRY IT**

**1**
Change the program so A shows an image, B a different image, and both scrolls your name.

**2**
Count how many times the loop runs each second by adding a pause; explain what you observe.

**3**
Why does the order of the IF tests matter? Explain with the A+B example.

**ROBOTICS CONNECTION**
Real devices are built on exactly this pattern: one button arms a robot, the second starts it, both
together stop it. Choosing an order for the tests prevents dangerous shortcuts.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
21

<!-- page 84 -->

---
**▮KEY WORDS**

**event an input occurrence a program reacts to**

**button A+B both buttons pressed together, a third input**

**debounce ignoring the tiny bounce of contacts so one press counts once**

**●CHALLENGE**

Create a digital reaction game: after a random wait, the grid flashes; the first of two players to press
their button wins the round; first to five wins the match, and the micro:bit celebrates.

**●CHECK YOUR UNDERSTANDING**

**1**
How many inputs do the buttons give?

**2**
Which test must come first: A+B or A alone? Why?

**3**
What does is_pressed() return?

**4**
How would you make one press count only once?

**5**
What is a reaction game testing?

**●EXIT TICKET**

**1**
Write the condition for both buttons pressed.

**2**
Why test A+B first?

**3**
Name a real device with a two-button safety pattern.

<!-- page 85 -->

---
**UNIT 5 · TOPIC 11**
## Input and output pins

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓read values from input pins
✓control output pins
✓build simple sensor and actuator circuits

Pins turn the micro:bit from a toy into a control system. Input pins read a number from an attached
circuit; output pins drive one.

**# read an input pin (0 to 1023)**
**reading = pin0.read_analog()**

**# control an output pin (0 to 1023)**
**pin1.write_analog(512)   # about half power**

The numbers run from 0 to 1023: 0 is nothing, 1023 is the maximum. An input pin might read a
homemade moisture sensor; an output pin might set how fast an external motor spins.

**A complete circuit example**

**●SENSORS AND ACTUATORS**

Input: a moisture probe in soil, read on pin 0. High reading means wet.

Process: the program compares the reading with a threshold you choose.

Output: a pump, driven through a motor board on pin 1, waters the plant.

**●TRY IT**

**1**
Trace the plant waterer: what happens when the reading is 900? When it is 100?

**2**
Write the pseudocode for the plant waterer before any wiring.

**3**
What safety rule from Topic 5.6 applies to the pump circuit?

**ROBOTICS CONNECTION**
Robotics is pins at work: light sensors on input pins steer a line follower; motor boards on output
pins drive the wheels. The micro:bit is the decision-maker between them.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
23

<!-- page 86 -->

---
**▮KEY WORDS**

**analog value a reading between 0 and 1023, not just on or off**

**threshold the value a program compares a reading against**

**actuator an output device that acts on the world**

**●CHALLENGE**

Design an automatic fan for the classroom: a temperature sensor decides, a motor spins the fan at one
of three speeds, and a button overrides it for two minutes. Draw the pin plan and write the pseudocode.

**●CHECK YOUR UNDERSTANDING**

**1**
What range of values does an analog pin read?

**2**
Which command reads a pin? Which writes one?

**3**
What is a threshold?

**4**
Name one sensor and one actuator.

**5**
Why does a motor need a control board rather than a direct pin?

**●EXIT TICKET**

**1**
Write the two pin commands from memory.

**2**
What does write_analog(1023) mean?

**3**
Where does the decision happen in a pin system?

<!-- page 87 -->

---
**UNIT 5 · TOPIC 12**
## Music

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓play notes and tunes through the micro:bit
✓use pitch and duration

Connect a small speaker or headphones with crocodile clips to pin 0 and GND, and the micro:bit can play
music. The command music.play() takes a list of notes.

**from microbit import ***
**import music**

**tune = ["C4:2", "D4:2", "E4:2", "F4:2",**
**"E4:2", "D4:2", "C4:2"]**
**music.play(tune)**

Each note is a name such as C4 and a length such as 2, separated by a colon. Put several notes in a list,
in order, and the micro:bit plays them one after another. Rests are written R.

**Pitch and duration**
The pitch of a note is how high or low it sounds, shown by its letter and number; the duration is how long
it sounds, shown by the number after the colon. Composing for the micro:bit is choosing a pleasing order
of both.

**●TRY IT**

**1**
Play the example tune, then swap two notes and describe the difference.

**2**
Write the first line of a song you know, as a note list.

**3**
Add pauses with R and make the tune swing.

**ROBOTICS CONNECTION**
Warning sounds are part of robot design: a reversing beep, a fault signal, a success chime. The
musical commands are the same; only the purpose changes.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
25

<!-- page 88 -->

---
**▮KEY WORDS**

**pitch how high or low a note sounds**

**duration how long a note plays**

**rest a silence in a tune, written R**

**●CHALLENGE**

Create a digital musical instrument: press A to play a rising scale, B a falling one, and shake for your
own three-note chord of joy. Notate your composition in your book.

**●CHECK YOUR UNDERSTANDING**

**1**
Where do you connect a speaker?

**2**
What does C4:2 mean?

**3**
How do you write a silence?

**4**
Which command plays a tune?

**5**
What makes one note higher than another?

**●EXIT TICKET**

**1**
Write a three-note tune as a list.

**2**
What separates a note's name and length?

**3**
How would a robot use music?

<!-- page 89 -->

---
**UNIT 5 · TOPIC 13**
## Random

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓use random numbers and random choices
✓build unpredictable programs
✓create a digital dice

True unpredictability is hard for computers, which follow instructions exactly. The random module gives
the micro:bit a convincing imitation: numbers nobody can predict, drawn from a range you choose.

**from microbit import ***
**import random**

**number = random.randint(1, 6)**
**display.show(number)**

random.randint(1, 6) picks a whole number from 1 to 6, both included. random.choice(list) picks one
item from a list, useful for random images, directions or messages.

**faces = [Image.HAPPY, Image.SAD, Image.ANGRY]**
**display.show(random.choice(faces))**

**●TRY IT**

**1**
Build the six-sided dice: show a number from 1 to 6 on shake.

**2**
Extend it: hold down button A while shaking to roll two dice and show the total.

**3**
Use random.choice to show a random animal image every three seconds.

**ROBOTICS CONNECTION**
Unpredictable behaviour has serious uses: search-and-rescue robots randomise their exploration
patterns to cover ground no planned route would reach. Games robots randomise to be less
predictable opponents.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
27

<!-- page 90 -->

---
**▮KEY WORDS**

**random unpredictable, without a pattern**

**range the set of values a random number is drawn from**

**seed the hidden starting value that keeps runs different**

**●CHALLENGE**

Create a random dice with a twist: a 12-sided dice on shake, plus a 'lucky dip' mode on button A that
shows one of six mystery images, and a penalty mode on button B that scrolls a random forfeit. Keep a
tally: are all outcomes appearing equally?

**●CHECK YOUR UNDERSTANDING**

**1**
Which command picks a number from 1 to 6?

**2**
Are both 1 and 6 possible results?

**3**
What does random.choice do?

**4**
Why is randomness useful in games?

**5**
Give one serious use of robot randomness.

**●EXIT TICKET**

**1**
Write the dice line from memory.

**2**
How do you pick a random image?

**3**
Why is predictability sometimes a problem?

**UNIT 5 · MICRO:BIT AND ROBOTICS**
28

<!-- page 91 -->

---
**UNIT 6 · TOPIC 1**
## Communication using email

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓write and manage email correctly
✓use To, Subject, CC, BCC, Reply and Forward
✓follow email etiquette

Email is the formal channel of digital communication: school, work and organisations all rely on it. A
good email gets read and answered; a poor one gets ignored or misunderstood.

**The parts of an email**

**PART**
**PURPOSE**

To
the main recipient, who must act or reply

CC (carbon copy)
people kept informed, with no action needed

BCC (blind carbon copy)
hidden recipients; nobody else can see their addresses

Subject
the headline; make it specific and short

Body
the message itself, with a greeting and a sign-off

Attachment
a file travelling with the email

**Email etiquette**

**●THE RULES**

Greet by name, and say who you are if the reader may not know you.

One topic per email, stated in the subject line.

Short sentences; full words, not text speak.

Say clearly what you are asking for, and by when.

Check spelling, then send. Re-reading finds almost every error.

**An example**

**UNIT 6 · COMMUNICATION**
1

<!-- page 92 -->

---
**To: Mrs Ferreira**
**Subject: Homework question, 7B Science**

**Dear Mrs Ferreira,**
**I was ill on Tuesday and missed the lesson on**
**photosynthesis. Could you tell me which pages of**
**the book I should read before Friday's test?**
**Thank you for your help.**
**Kind regards,**
**Goncalo Costa, 7B**

**●TRY IT**

**1**
Identify three etiquette rules the example follows.

**2**
When would you use BCC instead of CC? Give a school example.

**3**
Rewrite this properly: 'missed the hw wat do i do'.

**ROBOTICS CONNECTION**
Robot teams live on clear communication; engineers' status emails use the same rules. An unclear
email about a robot's battery fault causes the same crashes as an unclear error message.

**▮KEY WORDS**

**CC recipients kept informed, visible to all**

**BCC hidden recipients, invisible to everyone else**

**attachment a file sent with an email**

**etiquette the polite conventions of a form of communication**

**●CHALLENGE**

Write a complete email to your Computing teacher explaining why you were unable to finish the
micro:bit project on time, and proposing how you will catch up. Full etiquette: greeting, subject, clear
request, sign-off.

**UNIT 6 · COMMUNICATION**
2

<!-- page 93 -->

---
**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between CC and BCC?

**2**
What makes a good subject line?

**3**
Name three etiquette rules.

**4**
When do you use Reply and when Forward?

**5**
Why avoid text speak in school emails?

**●EXIT TICKET**

**1**
Name the parts of an email.

**2**
Write a good subject line for a lost homework query.

**3**
Who sees BCC addresses?

<!-- page 94 -->

---
**UNIT 6 · TOPIC 2**
## Effective use of the internet

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓search effectively with good keywords
✓evaluate the reliability of sources
✓respect copyright and avoid plagiarism

The internet answers almost any question, but it also repeats mistakes, half-truths and inventions. A
computer scientist searches well, then checks what the results are worth.

**Searching well**

**●SEARCH TIPS**

Use specific keywords: 'micro:bit compass calibration' beats 'how does my thing work'.

Exclude the noise: put quotes around exact phrases.

Read three sources, not one, before you believe a claim.

Go to the source: museums, universities and official sites outrank random pages.

**Is it reliable?**

**CHECK**
**GOOD SIGN**
**WARNING SIGN**

Author
named expert or institution
anonymous or 'someone said'

Date
recent, or clearly dated
no date on fast-changing topics

Evidence
sources and data cited
claims with no proof

Purpose
informing
selling or persuading

Cross-check
other sites agree
found nowhere else

**Copyright and plagiarism**
Words, images and code belong to the people who made them. Copying work and presenting it as yours
is plagiarism, a serious offence in every school. Using sources honestly means quoting, crediting and
listing them; fair use for schoolwork lets you copy small amounts with credit, never whole works.

**UNIT 6 · COMMUNICATION**
4

<!-- page 95 -->

---
**●TRY IT**

**1**
Improve this search: 'roman empire'. What exactly would you want to find out?

**2**
Rate two websites on one topic using the five checks. Which wins?

**3**
You find the perfect paragraph for your project. What are your honest options?

**ROBOTICS CONNECTION**
Roboticists share designs under open licences; using someone's code means following their licence
and naming them. The same ethics apply to your projects as to professional research.

**▮KEY WORDS**

**keyword the search words you type**

**reliability how much a source deserves to be trusted**

**plagiarism presenting someone else's work as your own**

**copyright the legal ownership of creative work**

**●CHALLENGE**

Fact-check a claim from social media: find three independent sources, apply all five reliability checks to
each, and write a verdict with evidence. Then write the reference list, honestly formatted.

**●CHECK YOUR UNDERSTANDING**

**1**
Name two ways to improve a search.

**2**
List three reliability checks.

**3**
What is plagiarism?

**4**
What does copyright protect?

**5**
Why read more than one source?

**UNIT 6 · COMMUNICATION**
5

<!-- page 96 -->

---
**●EXIT TICKET**

**1**
Improve the search 'volcano'.

**2**
Give one warning sign of an unreliable page.

**3**
How do you use a source honestly?

**UNIT 6 · COMMUNICATION**
6

<!-- page 97 -->

---
**UNIT 7 · TOPIC 1**
## Creating and editing documents

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓create, open and save documents
✓format text and paragraphs
✓produce consistent, readable documents

A word processor, such as Microsoft Word or Google Docs, is where reports, projects and homework are
prepared. The skill is not typing; it is making a document that is easy to read.

**The basics**

**●CORE SKILLS**

Create a new document, or open and edit an existing one.

Save with a clear name, in the right folder, early and often.

Format: font, size, bold and italic for emphasis.

Paragraphs: one idea each, with spacing between them.

Alignment: left for body text, centre for titles.

Line spacing: 1.15 or 1.5 makes long text readable.

**Rules of tidy documents**
Choose one font family and at most three sizes: title, heading, body. Never rely on colour alone to carry
meaning. Use bold headings so a reader can skim the structure. Consistency is the whole game: a
document that looks the same on page 1 and page 6 looks professional.

**●TRY IT**

**1**
Format a plain page of notes into a tidy document: title, two headings, spaced paragraphs.

**2**
Find three formatting faults in a poorly made document and fix them.

**3**
Set up a document template for your science reports and save it.

**UNIT 7 · LAYOUT**
1

<!-- page 98 -->

---
**ROBOTICS CONNECTION**
Robotics competitions demand written reports. Judges reward clear, consistent documents; the
layout is part of the engineering, not decoration.

**▮KEY WORDS**

**word processor software for creating formatted text documents**

**formatting changing how text looks**

**template a ready-made document setup you reuse**

**●CHALLENGE**

Produce a one-page guide to your micro:bit project: consistent fonts, centred title, clear headings, 1.15
line spacing and a footer with your name. Swap with a partner and mark each other's consistency.

**●CHECK YOUR UNDERSTANDING**

**1**
Name two word processors.

**2**
What are the core text formatting tools?

**3**
How many fonts should a good document use?

**4**
What line spacing suits long text?

**5**
Why save early and often?

**●EXIT TICKET**

**1**
Name three formatting decisions in a tidy document.

**2**
When is centred alignment appropriate?

**3**
What is a template?

<!-- page 99 -->

---
**UNIT 7 · TOPIC 2**
## Tables

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓create and edit tables
✓format tables clearly
✓use tables to organise information

A table shows structured information at a glance: rows for items, columns for facts about them. Test
results, prices, survey data and project plans all belong in tables, not paragraphs.

**Making and editing a table**

**●TABLE SKILLS**

Insert a table, choosing rows and columns.

Add and delete rows and columns as content demands.

Adjust column widths so nothing is squashed.

Format: a shaded header row, clear borders, consistent alignment.

Keep the unit in the header, not repeated in every cell: 'Price (euros)'.

**A well-made table**

**TEST**
**INPUT**
**EXPECTED**
**ACTUAL**
**PASS?**

Far sensor
40 cm
forward
forward
yes

Near sensor
8 cm
stop
stop
yes

Edge
black line
turn right
turn left
no

Notice the header row, the short cells and the honest 'no'. This table tells the story of a robot's testing
in seconds.

**●TRY IT**

**1**
Build this table in a word processor, matching the formatting.

**2**
Add a fourth test row for 'obstacle on the right'.

**3**
Rewrite a squashed table with better column widths and a shaded header.

**UNIT 7 · LAYOUT**
3

<!-- page 100 -->

---
**ROBOTICS CONNECTION**
Test tables are the heart of every robotics logbook: planned tests, expected results, actual results,
verdicts. The layout skill is an engineering skill.

**▮KEY WORDS**

**table a grid of rows and columns for structured information**

**header row the top row naming each column**

**cell one box of a table**

**●CHALLENGE**

Design a results table for a five-day survey of corridor traffic, with columns for day, time, count and
notes. Then format it so a reader can spot the busiest day within three seconds.

**●CHECK YOUR UNDERSTANDING**

**1**
When is a table better than a paragraph?

**2**
How do you add a column?

**3**
What belongs in the header row?

**4**
Name two formatting rules for clear tables.

**5**
Where should units go?

**●EXIT TICKET**

**1**
Define row, column and cell.

**2**
Why shade the header row?

**3**
Give an example of information you would tabulate.

<!-- page 101 -->

---
**UNIT 7 · TOPIC 3**
## Headers and footers

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓use headers and footers correctly
✓add page numbers, titles and dates
✓produce consistently formatted documents

A header is the small line at the top of every page; a footer sits at the bottom. They carry the
information a reader needs on every page: the document title, the author, the date and the page
number.

**●WHAT GOES WHERE**

Header: document title, or section name in longer reports.

Footer: page number ('Page 2 of 6'), author, date or school.

Everything in a small size, 9 or 10 points, and light grey or black.

Never put body content in a header or footer.

Set headers and footers once and every page inherits them, including correct page numbers as pages
are added or removed. This is why professionals never type page numbers by hand: the document counts
for you.

**●TRY IT**

**1**
Add a header with your project title and a footer with 'Page X of Y' and your name.

**2**
Change the footer to show the date. Which date should it show: created or last edited? Defend your
choice.

**3**
Add a different first page (a title page without header) to a document.

**ROBOTICS CONNECTION**
Engineering logbooks use headers and footers religiously: every page carries the project code, the
author and the page number, so a dropped stack of papers can be rebuilt in order.

**UNIT 7 · LAYOUT**
5

<!-- page 102 -->

---
**▮KEY WORDS**

**header the repeating line at the top of each page**

**footer the repeating line at the bottom of each page**

**page number field an automatic page number that updates itself**

**●CHALLENGE**

Produce the final formatting pass on your Smart School project report: consistent heading styles, tidy
tables, a header with the project name and a footer with page numbers, your name and the date. Check
every page.

**●CHECK YOUR UNDERSTANDING**

**1**
What is the difference between a header and a footer?

**2**
Name three things that belong in a footer.

**3**
Why use an automatic page number field?

**4**
What size should header and footer text be?

**5**
Why does the content never go in the header?

**●EXIT TICKET**

**1**
Define header and footer.

**2**
What goes on a title page instead?

**3**
Write a good footer for your project.

**UNIT 7 · LAYOUT**
6

<!-- page 103 -->

---
**UNIT 8 · TOPIC 1**
## Creating a database structure

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓plan a database for a purpose
✓identify fields and choose data types
✓create tables with primary keys
✓understand relationships at an introductory level

A good database is designed before it is filled. Planning means asking: what must the database record,
and what will people want to find? Every later problem in a project traces back to a rushed structure.

**Design steps**

**●HOW TO PLAN A DATABASE**

Describe the purpose in one sentence.

List the entities: the things you keep records of, such as pupils and books.

For each entity, list the fields, one fact per field.

Choose a data type for each field: text, number, date, true/false.

Choose a primary key: unique, never empty, never changing.

Check: can every question you need be answered from these fields?

**An example: the school library**

**FIELD**
**DATA TYPE**
**WHY**

BookID
number (key)
unique code for every copy

Title
text
the book's name

Author
text
who wrote it

Genre
text
for browsing and filters

Borrowed
true/false
is it out right now?

DueDate
date
when it must return

**Relationships**
Two tables connect through a relationship. A Loans table records BookID, PupilID and the date, pointing
at one row in Books and one in Pupils. This is how real databases avoid repeating information: the book's
details live once, in the Books table.

**UNIT 8 · DATABASES**
1

<!-- page 104 -->

---
**●TRY IT**

**1**
Design a table for a school lost-property database: five fields, types, primary key.

**2**
Why is 'Title' a poor primary key for the library?

**3**
Sketch the relationship between a Teams table and a Players table for a sports day database.

**ROBOTICS CONNECTION**
A delivery robot's control system keeps tables of locations and parcels; the robot queries the
relationship between them to decide its route. Database design is robot logistics.

**▮KEY WORDS**

**entity a thing a database keeps records of**

**data type the kind of value a field holds**

**relationship a connection between two tables through a shared field**

**●CHALLENGE**

Design the full database for the Smart School project: at least three tables, all fields with data types,
primary keys and the relationships between them. Test your design: write five questions it must be able
to answer.

**●CHECK YOUR UNDERSTANDING**

**1**
Why design before filling a database?

**2**
What are the common data types?

**3**
What makes a good primary key?

**4**
Why is Borrowed a true/false field?

**5**
What does a relationship connect?

**UNIT 8 · DATABASES**
2

<!-- page 105 -->

---
**●EXIT TICKET**

**1**
Name the design steps from memory.

**2**
Give a field and a data type for a birthday.

**3**
Why does a Loans table beat writing names inside the Books table?

<!-- page 106 -->

---
**UNIT 8 · TOPIC 2**
## Manipulating data

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓add, edit and delete records
✓sort, filter and search data
✓update data correctly and safely

Data is never finished: records are added, corrected, and removed. Doing this carefully is the difference
between a database you can trust and a spreadsheet of chaos.

**The four operations**

**OPERATION**
**WHAT IT DOES**
**CARE NEEDED**

Add
create a new record
complete every field; correct data types

Edit
change values in a record
update the whole truth, not a note

Delete
remove a record
often permanent; check twice

Update
change many records at once
preview the affected records first

**Finding and ordering**
Search finds records matching your words; filter shows records passing a condition; sort orders records
by a chosen field. Queries, from Unit 2, combine all three: the saved question 'show all unborrowed
fantasy books due before Friday' is a query.

**●TRY IT**

**1**
In a book table, sort by Author, then filter Genre = 'adventure'. What shows?

**2**
A pupil changes house. Which operation updates the record, and what must be true of the change?

**3**
Write a filter finding all borrowed books due before a given date.

**ROBOTICS CONNECTION**
Warehouse robots live on these operations: add parcels, edit locations, delete delivered items,
update the day's routes. The robot is a moving part of the database.

**UNIT 8 · DATABASES**
4

<!-- page 107 -->

---
**▮KEY WORDS**

**add creating a new record**

**edit changing a record's values**

**delete removing a record permanently**

**update changing many records at once**

**●CHALLENGE**

Your Smart School database has a wrong room number recorded for a whole corridor. Describe the safe
update procedure: how you preview the damage, apply the change, and prove it worked afterwards.

**●CHECK YOUR UNDERSTANDING**

**1**
Name the four data operations.

**2**
What is the difference between search and filter?

**3**
Why preview a bulk update?

**4**
What happens to a deleted record?

**5**
When is a query better than manual filtering?

**●EXIT TICKET**

**1**
Which operation adds a record?

**2**
Write a filter for Genre = 'history'.

**3**
Why is deleting dangerous?

<!-- page 108 -->

---
**UNIT 8 · TOPIC 3**
## Presenting data

**✓LEARNING OBJECTIVES**

In this topic you will learn to:
✓turn data into reports, tables and charts
✓format presentations clearly
✓match the presentation to the audience

Collecting data earns nothing until it is communicated. Presenting data means choosing the form that
lets your audience see the point instantly: a table for exact values, a bar chart for comparisons, a line
chart for change over time, a pie chart for shares of a whole.

**YOU WANT TO SHOW...**
**USE**
**BECAUSE**

exact values
table
every number is visible

comparing groups
bar chart
lengths compare at a glance

change over time
line chart
the shape of the trend shows

parts of a whole
pie chart
shares are visible as slices

**Presenting well**

**●PRESENTATION RULES**

Title every chart and table, and label every axis.

One message per chart: split a crowded chart into two.

Colour consistently: the same thing keeps the same colour.

Round numbers for display; keep the precise values in the database.

Choose what to include for the audience, not for yourself.

A report brings it together: an introduction saying what was asked, the data presented in tables and
charts, and a conclusion stating what the data shows, in honest language.

**UNIT 5 · MICRO:BIT AND ROBOTICS**
6

<!-- page 109 -->

---
**●TRY IT**

**1**
Choose the chart type for: temperatures every hour; favourite sports; sales by month; test scores of
five pupils.

**2**
Take any table from Unit 2 and turn it into the right chart, fully labelled.

**3**
Write two conclusions from your chart: one the data supports, one it does not.

**ROBOTICS CONNECTION**
Robot teams present their logbook data to judges: sensor graphs, test tables, and a clear verdict.
Judges trust charts with axes and honesty over flashy slides without either.

**▮KEY WORDS**

**bar chart a chart comparing quantities with bar lengths**

**line chart a chart showing change over time**

**report a document presenting data and conclusions**

**●CHALLENGE**

Present your corridor-traffic data from Unit 2 as a one-page report: introduction, a table of the raw
counts, two labelled charts, and a recommendation for the school, written for the headteacher as the
audience.

**●CHECK YOUR UNDERSTANDING**

**1**
Which chart shows change over time?

**2**
Which chart compares groups?

**3**
Name three presentation rules.

**4**
Why label every axis?

**5**
What does a report contain?

**UNIT 5 · MICRO:BIT AND ROBOTICS**
7

<!-- page 110 -->

---
**●EXIT TICKET**

**1**
Match chart to purpose: parts of a whole.

**2**
Write a good chart title.

**3**
Who decides what to include in a presentation?

**UNIT 5 · MICRO:BIT AND ROBOTICS**
8

<!-- page 111 -->

---
## SMART SCHOOL PROJECT

Your final challenge of Year 7: design and build part of a Smart School, a system that uses computing
and robotics to solve a real problem in your own school.

The project brings together every unit of this book. You will think like a computer scientist, work with
data, understand the systems you are using, program a micro:bit, communicate your findings, present a
professional report and defend your work.

**The process: twelve steps**

**STEP**
**WHAT YOU DO**

1 Identify the problem
choose a real school problem your system solves

2 Decompose
break it into subproblems, one per team member

3 Research
find reliable information; record your sources

4 Design
algorithm, flowchart, pseudocode and system diagram

5 Build
create the micro:bit prototype

6 Collect data
survey or sensors, properly planned

7 Create the database
tables, fields, types, keys

8 Analyse
sort, filter, query, chart

9 Test
test cases: expected versus actual

10 Debug
find, fix, and test again

11 Present
professional report and presentation

12 Reflect
what you learned; how you would improve it

**What your Smart School could do**

**SMART SCHOOL PROJECT**
1

<!-- page 112 -->

---
**●IDEAS TO START FROM**

a smart doorbell for the school office that shows who has arrived

a corridor traffic monitor that counts the busiest minutes of the day

a plant watering system for the biology lab

a lost-property register with a searchable database

a quiet-corner indicator for the library, using the light and sound sensors

an attendance system for a club, with a database and a report

**What you must hand in**

**●DELIVERABLES**

the design: algorithm, flowchart, pseudocode, system diagram

the micro:bit program, on the board and in your book

the database: structure and data

the analysis: queries, tables, charts, conclusions

the report: professionally formatted, headers and footers, tables and charts

the presentation: five minutes, for the class and the teacher

the reflection: what you learned, what you would improve

<!-- page 113 -->

---
**SMART SCHOOL PROJECT · GUIDEBOOK**
## The Smart School guidebook

Work through the steps in order. Each connects directly to a unit of this book, so look back whenever
you need the detail.

**Steps 1-4: thinking and design**
Choose a problem you can observe for yourselves; vague ideas make weak projects. Decompose until
every subproblem fits one person and one week. Research with the reliability checks from Unit 6. Design
means paper before programming: algorithm first, then flowchart, then pseudocode. Your teacher
should be able to trace your program back to your flowchart line by line.

**Steps 5-8: building and data**
Build in small steps: one input, one process, one output, tested before anything else is added. Collect
data honestly, with the planning discipline of Unit 2. Create the database with the design steps of Unit
8: entities, fields, types, keys. Then analyse with queries, and chart only what you will actually explain.

**Steps 9-12: proving and presenting**
Test with written test cases: input, expected, actual. Debug one fault at a time, using the cycle from
Unit 1. Present with the layout discipline of Unit 7: consistent fonts, labelled charts, headers and
footers. Reflect honestly: judges respect a project that says 'our first design failed because...' far more
than one that pretends everything worked.

**Working as a team**

**●TEAM RULES**

agree the decomposition in writing before starting

each member owns their subproblems, but everyone can explain the whole

keep one shared project log, dated, in the team's report

disagreements go to evidence: what does the data say?

**▮KEY WORDS**

**prototype a first working version, built to learn from**

**deliverable an item the team must hand in**

**reflection honest analysis of what you learned**

**SMART SCHOOL PROJECT**
3

<!-- page 114 -->

---
**●CHALLENGE**

Full marks: extend your project beyond the brief with one feature nobody asked for, such as radio
communication between two micro:bits, or an automatic weekly report generated from the database.
Innovation earns the top band, if and only if the twelve core steps are also complete.

**●CHECK YOUR UNDERSTANDING**

**1**
Why must the problem be real and observable?

**2**
What comes first: programming or the flowchart?

**3**
What does a test case record?

**4**
Who can explain your project at the presentation?

**5**
What does reflection add to a report?

**●EXIT TICKET**

**1**
Name the twelve steps from memory.

**2**
Which step do teams most often skip, and why is it fatal?

**3**
Write one sentence: why does your school need your Smart School?

<!-- page 115 -->

---
## Glossary

**abstraction keeping the important details and removing the rest**

**actuator an output device that acts on the real world, like a motor**

**algorithm a precise set of step-by-step instructions that solves a problem**

**ALU the part of the CPU that does calculations and comparisons**

**analog value a reading between 0 and 1023, not just on or off**

**application software programs that do tasks for the user, like a word processor**

**attachment a file sent with an email**

**BCC email recipients hidden from everyone else**

**binary the base 2 number system, using only 0 and 1**

**bit a single 0 or 1, the smallest unit of data**

**bug a mistake in a program**

**byte 8 bits, enough for roughly one character of text**

**CC email recipients kept informed, visible to all**

**client the device that asks for data from a server**

**cloud storage storage on remote servers reached through the internet**

**computational thinking approaching problems the way a computer scientist does**

**CPU Central Processing Unit, the processor that carries out instructions**

**cyberbullying bullying through messages, posts or exclusion online**

**cybersecurity protecting devices and data from digital attacks**

**data information that a computer can store and process**

<!-- page 116 -->

---
**database an organised collection of data in tables**

**debugging finding and fixing mistakes in a program**

**decomposition breaking a complex problem into smaller parts**

**digital footprint the trail of everything you do online**

**DNS the system that translates names into IP addresses**

**event a trigger that starts instructions when something happens**

**field one piece of a record, shown as a table column**

**filter showing only records that match a condition**

**flowchart a diagram of an algorithm using standard symbols**

**function a named block of instructions you can reuse**

**hardware the physical parts of a computer system**

**HTTP/HTTPS the protocols of the web; HTTPS is the encrypted version**

**input data entering a system**

**internet the worldwide network that carries data between devices**

**IP address a number identifying one device on a network**

**LAN local area network, covering one site**

**logic error a program that runs but produces a wrong answer**

**malware software designed to harm or spy**

**micro:bit a pocket programmable board for physical computing**

**microcontroller a complete tiny computer on one chip**

<!-- page 117 -->

---
**network two or more computers connected to share data and devices**

**operating system the core software managing hardware and programs**

**output the result leaving a system**

**pattern recognition noticing similarities and repetition inside problems**

**phishing fake messages imitating real companies to steal details**

**pixel one tiny dot of a digital image**

**primary key the field that is unique for every record**

**protocol an agreed set of rules for communication**

**pseudocode structured plain-English notes describing an algorithm**

**query a saved question you ask a database table**

**RAM fast working memory, lost when power is off**

**record one complete item in a table, shown as a row**

**relationship a connection between two tables through a shared field**

**ROM permanent read-only memory holding start-up instructions**

**router a device joining networks together and routing data**

**runtime error an error that crashes a program while it runs**

**secondary storage storage that keeps data when power is off**

**sensor an input that measures the real world**

**sequence instructions executed one after another**

**server the computer that stores data and answers requests**

<!-- page 118 -->

---
**software the programs that run on hardware**

**switch a device connecting computers inside one network**

**syntax error an error that breaks the language rules, so the program will not run**

**system software programs that run and manage the computer itself**

**TCP/IP the protocol family carrying all internet data in packets**

**testing running a program with known inputs to check it works**

**variable a named place in memory holding a value that can change**

**WAN wide area network, joining sites over long distances**

**World Wide Web websites and pages, one service running on the internet**

**GLOSSARY**
8

<!-- page 119 -->

---
## End-of-unit tests

One test per unit. Each has multiple choice, true or false, matching, short answers and one problem to
solve. Work without the book, then mark with the answer key at the end of this section.

**Unit 1 test: Computational Thinking**

**●SECTION A · MULTIPLE CHOICE**

**1**
Breaking a big problem into smaller parts is called: A) abstraction B) decomposition C) pattern
recognition D) debugging

**2**
The flowchart symbol for a question is: A) rectangle B) diamond C) oval D) parallelogram

**3**
A program that runs but gives the wrong answer has: A) a syntax error B) a runtime error C) a logic
error D) a virus

**4**
Which is pseudocode? A) print('hi') B) OUTPUT "hi" C) say hi D) hi.out

**5**
Recognising that two problems share a structure is: A) decomposition B) abstraction C) pattern
recognition D) testing

**●SECTION B · TRUE OR FALSE**

**1**
A decision symbol must have at least two exit arrows.

**2**
Pseudocode can be run by a computer.

**3**
The order of steps in an algorithm rarely matters.

**4**
A logic error stops a program running.

**5**
Abstraction removes detail that the purpose does not need.

**●SECTION C · MATCHING**

**1**
Match each term to its meaning: algorithm, bug, flowchart, test case, debugging. Meanings: a
diagram of an algorithm; a mistake in a program; a precise set of steps; finding and fixing a mistake;
one input with expected and actual results.

**ASSESSMENT**
1

<!-- page 120 -->

---
**●SECTION D · SHORT ANSWER**

**1**
Explain, with an example, why decomposition helps a team build a program.

**2**
Write pseudocode for a program that asks for a number and outputs 'even' or 'odd'.

**3**
List the three kinds of error and give one example of each.

**4**
Draw the flowchart for: input age, if age is 13 or more output 'teenager', otherwise output 'child'.

**●SECTION E · PROBLEM SOLVING**

**1**
A robot should sweep a square room but instead sweeps the same strip forever. The pseudocode
says REPEAT 4 TIMES: sweep strip, turn left, but the robot never turns. Identify the most likely
error type, explain your reasoning, and write a test plan to prove your fix works.

<!-- page 121 -->

---
**Unit 2 test: Managing Data**

**●SECTION A · MULTIPLE CHOICE**

**1**
How many values can one bit hold? A) 1 B) 2 C) 8 D) 256

**2**
The binary 1010 in decimal is: A) 8 B) 10 C) 12 D) 20

**3**
Eight bits make one: A) nibble B) byte C) kilobyte D) word

**4**
A row of a database table is called a: A) field B) record C) key D) query

**5**
SELECT * FROM books WHERE borrowed = FALSE is a: A) filter by hand B) query C) sort D) field

**●SECTION B · TRUE OR FALSE**

**1**
RAM keeps your files when the power is off.

**2**
A primary key can repeat values.

**3**
A filter hides records that do not match.

**4**
One megabyte is about a thousand gigabytes.

**5**
Sensors are one way of collecting data.

**●SECTION C · MATCHING**

**1**
Match: bit, byte, record, field, primary key. Meanings: unique identifier of a record; one row of a
table; one 0 or 1; one column of a table; eight bits.

**●SECTION D · SHORT ANSWER**

**1**
Convert 10011 to decimal, showing your working.

**2**
Convert 22 to binary.

**3**
Explain the difference between sorting and filtering, with one example of each.

**4**
A survey asks 'Do you like games?' Explain one way this question is poorly designed.

**●SECTION E · PROBLEM SOLVING**

**1**
Design a database table for a school tuck shop: five fields, types, primary key. Then write two
queries the shop manager would run every day, and say what each returns.

<!-- page 122 -->

---
**Unit 3 test: Networks and Digital Communication**

**●SECTION A · MULTIPLE CHOICE**

**1**
A network covering one school site is a: A) WAN B) LAN C) VPN D) DNS

**2**
The device that joins your network to the internet is the: A) switch B) router C) server D) sensor

**3**
HTTPS differs from HTTP because it: A) is faster B) is encrypted C) uses cables D) needs no IP
address

**4**
DNS translates: A) IP addresses to binary B) names to IP addresses C) bytes to bits D) email to web
pages

**5**
A fake email imitating your bank is: A) malware B) phishing C) a virus D) spam

**●SECTION B · TRUE OR FALSE**

**1**
The World Wide Web and the internet are the same thing.

**2**
Every device on a network needs an address.

**3**
A switch chooses the route to other networks.

**4**
Long random-word passwords are stronger than short complex ones.

**5**
Anything you post online can disappear permanently whenever you want.

**●SECTION C · MATCHING**

**1**
Match: LAN, WAN, client, server, protocol. Meanings: covers one site; agreed rules for
communication; asks for data; worldwide network of networks; answers requests.

**●SECTION D · SHORT ANSWER**

**1**
Explain the difference between the internet and the web with an analogy of your own.

**2**
Write the path of a web request from a classroom computer to a website, naming the devices.

**3**
Name the four defensive habits against cyberattacks.

**4**
What is a digital footprint, and why does it matter for your future?

**ASSESSMENT**
4

<!-- page 123 -->

---
**●SECTION E · PROBLEM SOLVING**

**1**
Your friend receives a message: 'Your account is locked! Click this link and enter your password to
keep it.' List every warning sign, describe what you would tell your friend to do, and explain who
they should report it to.

<!-- page 124 -->

---
**Unit 4 test: Computer Systems**

**●SECTION A · MULTIPLE CHOICE**

**1**
The CPU part that does calculations is the: A) Control Unit B) ALU C) register D) bus

**2**
Volatile memory that forgets everything without power is: A) ROM B) RAM C) SSD D) HDD

**3**
A microphone is: A) an input device B) an output device C) software D) storage

**4**
Which storage has no moving parts? A) HDD B) SSD C) DVD D) cassette

**5**
The software that manages the whole computer is the: A) browser B) operating system C) driver D)
game

**●SECTION B · TRUE OR FALSE**

**1**
ROM holds the start-up instructions.

**2**
A touchscreen is both input and output.

**3**
Applications talk to hardware directly, without the operating system.

**4**
SSDs are usually faster than HDDs.

**5**
An actuator is an input device.

**●SECTION C · MATCHING**

**1**
Match: CPU, RAM, ROM, sensor, actuator. Meanings: measures the world; permanent start-up
memory; the brain of the computer; acts on the world; working memory lost at power off.

**●SECTION D · SHORT ANSWER**

**1**
Name the three stages of the CPU cycle in order, and say what the ALU does in one of them.

**2**
Explain why unsaved work vanishes when a computer crashes.

**3**
Give the four-stage model of how computers process data, and map a robot vacuum onto it.

**4**
Classify as system or application software: word processor, operating system, browser, driver.

**ASSESSMENT**
6

<!-- page 125 -->

---
**●SECTION E · PROBLEM SOLVING**

**1**
A family buys a laptop with a small SSD. Recommend how they should store: the operating system, a
photo library of 200 GB, and school work. Justify each choice on capacity, speed, portability,
reliability and cost.

<!-- page 126 -->

---
**Unit 5 test: micro:bit and Robotics**

**●SECTION A · MULTIPLE CHOICE**

**1**
The micro:bit LED matrix has: A) 9 B) 16 C) 25 D) 100 lights

**2**
The command to pick a whole number from 1 to 6 is: A) pick(1,6) B) random.randint(1,6) C)
number(1,6) D) dice()

**3**
In an image string, the digit 9 means a light is: A) off B) dim C) fully on D) green

**4**
The GND pin is: A) ground, the return path B) a data pin C) the antenna D) a button

**5**
while True: creates: A) an event B) an endless loop C) a function D) a variable

**●SECTION B · TRUE OR FALSE**

**1**
The micro:bit can run programs without a computer attached.

**2**
You may connect a pin straight to a battery.

**3**
random.choice picks one item from a list.

**4**
Pin readings range from 0 to 1023.

**5**
In MicroPython, indentation is only decoration.

**●SECTION C · MATCHING**

**1**
Match: sequence, selection, repetition, event, function. Meanings: reacts when something happens;
instructions in order; a reusable named block; repeating instructions; choosing between paths.

**●SECTION D · SHORT ANSWER**

**1**
Name three inputs and three outputs of the micro:bit.

**2**
Explain why the A+B button test must come before the single-button tests.

**3**
What does each digit in an image string mean, and how do you animate?

**4**
Write the two commands to read pin 0 and write half power to pin 1.

**ASSESSMENT**
8

<!-- page 127 -->

---
**●SECTION E · PROBLEM SOLVING**

**1**
Write, in pseudocode or MicroPython, a program for an automatic nightlight: reads light level
forever; if dark shows a dim heart; if very dark shows a bright one; otherwise clears the display.
Then list two test cases with expected and actual results.

<!-- page 128 -->

---
**Unit 6 test: Communication**

**●SECTION A · MULTIPLE CHOICE**

**1**
Recipients hidden from all others are in: A) To B) CC C) BCC D) Subject

**2**
A specific, short email headline belongs in the: A) body B) subject C) greeting D) attachment

**3**
Presenting someone else's work as your own is: A) copyright B) plagiarism C) licence D) quotation

**4**
The best search for information about micro:bit compass calibration is: A) 'micro:bit compass
calibration' B) 'how thing work' C) 'micro:bit' D) 'compass'

**5**
A page with no author and no date is: A) reliable B) a warning sign C) official D) always wrong

**●SECTION B · TRUE OR FALSE**

**1**
Text speak is fine in emails to teachers.

**2**
Quoting a source with credit is honest use.

**3**
One source is enough before believing a claim.

**4**
The purpose of a page (informing versus selling) affects its reliability.

**5**
Fair use lets you copy whole works for schoolwork.

**●SECTION C · MATCHING**

**1**
Match: To, CC, Subject, attachment, etiquette. Meanings: file travelling with an email; the main
recipient; polite conventions; people informed, visible to all; the headline of an email.

**●SECTION D · SHORT ANSWER**

**1**
Rewrite properly: 'hey sir cant come 2morrow sick lol'.

**2**
List three reliability checks for a website.

**3**
Explain when you would use BCC instead of CC.

**ASSESSMENT**
10

<!-- page 129 -->

---
**●SECTION E · PROBLEM SOLVING**

**1**
Write a complete email to your Computing teacher explaining that a broken USB cable stopped you
finishing the micro:bit project, and proposing a catch-up plan. Full etiquette: greeting, subject,
clear request, sign-off.

<!-- page 130 -->

---
**Unit 7 test: Layout**

**●SECTION A · MULTIPLE CHOICE**

**1**
The repeating line at the bottom of every page is the: A) header B) footer C) margin D) style

**2**
Body text in a tidy document should usually be: A) centred B) right-aligned C) left-aligned D)
justified only

**3**
How many font families should a good document use? A) one B) two C) three D) as many as possible

**4**
In a table, the top row naming each column is the: A) cell B) header row C) footer D) key

**5**
Page numbers should be: A) typed by hand B) automatic fields C) in the header only D) omitted

**●SECTION B · TRUE OR FALSE**

**1**
Colour alone should never carry meaning.

**2**
One idea per paragraph is a good rule.

**3**
Squashed columns with repeated units are fine.

**4**
A template helps keep documents consistent.

**5**
Headers should contain the main body text.

**●SECTION C · MATCHING**

**1**
Match: header, footer, table, template, cell. Meanings: one box of a table; repeating top line; a
reusable document setup; a grid for structured data; repeating bottom line with page numbers.

**●SECTION D · SHORT ANSWER**

**1**
Name three formatting rules for clear tables.

**2**
List what belongs in a header and what belongs in a footer.

**3**
Describe how you would format a one-page project report for consistency.

**ASSESSMENT**
12

<!-- page 131 -->

---
**●SECTION E · PROBLEM SOLVING**

**1**
A test table has squashed columns, no header shading and units repeated in every cell. Describe
every fault and rewrite the table design so a reader can use it at a glance.

<!-- page 132 -->

---
**Unit 8 test: Databases**

**●SECTION A · MULTIPLE CHOICE**

**1**
One fact per column is the definition of a: A) record B) field C) key D) query

**2**
A field that is unique for every record is the: A) primary key B) name C) date D) type

**3**
Removing a record permanently is: A) add B) edit C) delete D) update

**4**
To show change over time, use a: A) pie chart B) bar chart C) line chart D) table

**5**
A connection between two tables through a shared field is a: A) link B) relationship C) join type D)
filter

**●SECTION B · TRUE OR FALSE**

**1**
A database should be designed before it is filled.

**2**
Borrowed (yes or no) suits a true/false data type.

**3**
A bulk update should never be previewed first.

**4**
Charts need titles but not axis labels.

**5**
The audience decides what to include in a report.

**●SECTION C · MATCHING**

**1**
Match: entity, data type, relationship, query, report. Meanings: the kind of value a field holds; a
saved question; a thing you keep records of; a document presenting data and conclusions; a
connection between tables.

**●SECTION D · SHORT ANSWER**

**1**
List the six design steps for a new database.

**2**
Why is a book's title a poor primary key?

**3**
Name the four data operations, with one care point each.

**●SECTION E · PROBLEM SOLVING**

**1**
Design the database for a school lost-property office: entities, fields, types, primary keys and one
relationship. Write two queries the office would run daily, and choose the chart you would use to
show what has been lost most, justifying your choice.

**ASSESSMENT**
14

<!-- page 133 -->

---
## Teacher answer key

Answers for the eight end-of-unit tests. Section E answers are model responses: accept any
well-reasoned equivalent.

**Unit 1 · Computational Thinking**
A: 1B, 2B, 3C, 4B, 5C.

B: 1 True, 2 False, 3 False, 4 False, 5 True.

C: algorithm = precise set of steps; bug = mistake in a program; flowchart = diagram of an algorithm; test case
= one input with expected and actual results; debugging = finding and fixing a mistake.

D: model answers; pseudocode for even/odd must use MOD or division remainder; error examples: syntax
(misspelled command), runtime (divide by zero), logic (wrong operator).

E: logic error (a step is missing or mistyped so the turn never runs). Test plan: run one square, record turns;
fix; run four squares; confirm four turns and full coverage.

**Unit 2 · Managing Data**
A: 1B, 2B, 3B, 4B, 5B.

B: 1 False, 2 False, 3 True, 4 False, 5 True.

C: bit = one 0 or 1; byte = eight bits; record = one row; field = one column; primary key = unique identifier of a
record.

D: 10011 = 16+2+1 = 19; 22 = 10110; sorting orders records, filtering hides non-matches; the survey question
is leading ('like games' presumes an answer) and should offer balanced options.

E: model answer; expect five sensible fields, a numeric or auto-numbered primary key, and two queries such as
stock below five and sales today.

**ASSESSMENT · TEACHER ANSWER KEY**
1

<!-- page 134 -->

---
**Unit 3 · Networks and Digital Communication**
A: 1B, 2B, 3B, 4B, 5B.

B: 1 False, 2 True, 3 False, 4 True, 5 False.

C: LAN = one site; WAN = worldwide network of networks; client = asks; server = answers; protocol = agreed
rules.

D: web is one service on the internet (any sound analogy); computer, switch, router, internet, server; four
habits: strong passwords, MFA, updates, backups; footprint = permanent public trail checked by future schools
and employers.

E: warning signs: urgency, generic greeting, link, password request, mismatched sender. Action: do not click,
tell a trusted adult, report to the platform and to the bank's real fraud address.

**Unit 4 · Computer Systems**
A: 1B, 2B, 3A, 4B, 5B.

B: 1 True, 2 True, 3 False, 4 True, 5 False.

C: CPU = brain; RAM = working memory lost at power off; ROM = start-up memory; sensor = measures;
actuator = acts.

D: fetch, decode, execute; unsaved work lives only in RAM; robot mapping: bump or dirt sensor (input), CPU
(process), motors (output), dustbin log (storage); word processor and browser are applications, operating
system and driver are system software.

E: model answer; expect OS on SSD (speed), photo library on cloud or external HDD (capacity and safety),
school work on both (redundancy), with cost justified.

**Unit 5 · micro:bit and Robotics**
A: 1C, 2B, 3C, 4A, 5B.

B: 1 True, 2 False, 3 True, 4 True, 5 False.

C: sequence = order; selection = choosing paths; repetition = repeating; event = reacts when something
happens; function = reusable named block.

D: inputs include buttons, light, temperature, compass, pins; outputs include LED grid, pins, speaker (V2); A+B
first because single tests would fire when both are held; digits 0-9 are brightness, animation is a list of frames
with a delay; read = pin0.read_analog(), write = pin1.write_analog(512).

E: model answer; expect a forever loop, two-level comparison, and test cases such as bright room (clear) and
covered sensor (bright heart).

**ASSESSMENT · TEACHER ANSWER KEY**
2

<!-- page 135 -->

---
**Unit 6 · Communication**
A: 1C, 2B, 3B, 4A, 5B.

B: 1 False, 2 True, 3 False, 4 True, 5 False.

C: To = main recipient; CC = informed, visible; Subject = headline; attachment = file; etiquette = polite
conventions.

D: proper email must include greeting, full sentences, clear statement and sign-off; checks: author, date,
evidence, purpose, cross-check; BCC for mailing many people without exposing addresses.

E: model answer marked on etiquette, clarity, honesty and a concrete catch-up plan.

**Unit 7 · Layout**
A: 1B, 2C, 3A, 4B, 5B.

B: 1 True, 2 True, 3 False, 4 True, 5 False.

C: header = repeating top line; footer = repeating bottom line; table = grid for structured data; template =
reusable setup; cell = one box.

D: shaded header row, units in headers not cells, readable column widths, consistent alignment; header: title;
footer: page number, name, date; report format: one font family, three sizes, headings, spacing, footer.

E: faults: squashed columns, no shading, repeated units, no clear verdict column; fix: widen columns, shade
header, move units once, add pass/fail column.

**Unit 8 · Databases**
A: 1B, 2A, 3C, 4C, 5B.

B: 1 True, 2 True, 3 False, 4 False, 5 True.

C: entity = thing recorded; data type = kind of value; relationship = connection between tables; query = saved
question; report = document presenting data and conclusions.

D: purpose, entities, fields, types, primary key, check questions; titles repeat, so they cannot be unique keys;
add (complete every field), edit (whole truth), delete (permanent, check twice), update (preview first).

E: model answer; expect Items and Locations tables linked by a code field, daily queries such as items found
today and items unclaimed over 30 days, and a bar chart comparing categories lost.

**ASSESSMENT · TEACHER ANSWER KEY**
3
