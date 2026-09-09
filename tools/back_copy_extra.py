SUBJ_COPY = {
 'english': (
  "Read between every line.",
  "This Year {year} English course builds confident readers and precise writers: wide reading, real writing purposes and discussion that sharpens thinking.",
  ["Wide reading across genres and eras", "Writing for real audiences and purposes",
   "Vocabulary, grammar and style in context", "Speaking, listening and debate",
   "Regular checkpoints with model answers"]),
 'mathematics': (
  "Mathematics that explains itself.",
  "Year {year} mathematics moves step by step from concrete to abstract: every rule is derived, every method modelled, every unit practised and reviewed.",
  ["Worked examples before every exercise", "Fluency practice and problem-solving",
   "Calculator and non-calculator skills", "Cumulative unit reviews",
   "Exam-style questions with answers"]),
 'science': (
  "Ask questions. Trust evidence.",
  "Year {year} science combines clear explanations with hands-on investigation across biology, chemistry and physics, building the habits of working scientifically.",
  ["Biology, chemistry and physics strands", "Practical investigations throughout",
   "Diagrams, data and vocabulary support", "End-of-unit checkpoints",
   "Full glossary and answer key"]),
 'physical-education': (
  "Move well. Understand why.",
  "Year {year} physical education develops practical skill and the theory behind it: anatomy, training, tactics and healthy participation for life.",
  ["Practical units across sports and athletics", "Anatomy, physiology and training theory",
   "Tactics, leadership and officiating", "Health, fitness and wellbeing",
   "Assessment preparation included"]),
 'humanities': (
  "Learn to read the world.",
  "Year {year} humanities weaves history, geography and citizenship into one course: sources, maps, case studies and big questions about people and place.",
  ["History: sources and enquiry", "Geography: maps, place and process",
   "Citizenship and global issues", "Skills practice: sources, data, essays",
   "Unit reviews with model answers"]),
 'global-perspectives': (
  "See every issue from every side.",
  "Year {year} global perspectives builds research, reasoning and collaboration through big global topics, ending in a personal project you can defend.",
  ["Big global topics, locally explored", "Research and evidence skills",
   "Collaboration and debate", "Reflection and personal projects",
   "Assessment-ready checkpoints"]),
 'computing-and-robotics': (
  "Understand the machine. Then build with it.",
  "Year {year} computing and robotics pairs computational thinking with hands-on builds: programming, data, networks and working robots.",
  ["Programming projects in every unit", "How computers and networks really work",
   "Data, logic and problem-solving", "Robotics builds with everyday kits",
   "Digital safety and responsibility"]),
 'art-and-design': (
  "Every child is an artist. Keep the studio open.",
  "Year {year} art and design develops making, looking and thinking: drawing, colour, print, 3D and the artists who changed how we see.",
  ["Skills: drawing, paint, print, 3D", "Artists and movements in context",
   "Sketchbook habit and portfolio building", "Critique language and reflection",
   "Final project per unit"]),
 'music-and-drama': (
  "Make something the room remembers.",
  "Year {year} music and drama builds performing, composing and responding alongside staging, voice and ensemble work.",
  ["Performing and composing units", "Voice, movement and staging",
   "Listening and repertoire study", "Ensemble and group-devising work",
   "Showcase tasks per unit"]),
 'spanish': (
  "Real Spanish, from the first page.",
  "Year {year} Spanish builds confident communication: everyday topics, authentic texts and grammar that grows step by step.",
  ["Topic-based units with real dialogues", "Grammar introduced and recycled",
   "Speaking, listening, reading, writing", "Culture of the Spanish-speaking world",
   "Vocabulary lists and review pages"]),
 'portuguese-1st': (
  "A língua que já é tua — agora escrita com orgulho.",
  "Português Língua Materna para o Year {year}: leitura, escrita, gramática e oralidade com textos autênticos e projetos de escrita.",
  ["Leitura e interpretação de textos", "Escrita guiada e criativa",
   "Gramática em contexto", "Oralidade e debate",
   "Balanço no fim de cada unidade"]),
 'portuguese-2nd': (
  "Português de verdade, passo a passo.",
  "Português Língua Segunda para o Year {year}: comunicação do dia a dia, textos autênticos e gramática que cresce aos poucos.",
  ["Unidades por temas do quotidiano", "Diálogos e textos autênticos",
   "Gramática apresentada e revista", "Cultura portuguesa e lusófona",
   "Listas de vocabulário e revisões"]),
 'business-btec-l2': (
  "Business, learned by doing business.",
  "This BTEC Level 2 course in Year {year} covers enterprise, finance, marketing and people through real business scenarios and assessed coursework.",
  ["Enterprise and entrepreneurship", "Finance and record-keeping",
   "Marketing and the customer", "People and operations",
   "Assignment-style practice tasks"]),
 'portuguese-a-level': (
  "A língua ao nível do pensamento.",
  "Português A Level: análise literária, debate de ideias e escrita sofisticada, com os autores e os temas que preparam o ensino superior.",
  ["Literatura e análise textual", "Ensaios argumentativos",
   "Tradução e compreensão avançada", "Tema: sociedade, cultura e atualidade",
   "Preparação para o exame"]),
 'spanish-a-level': (
  "From fluent to formidable.",
  "Spanish A Level in Year {year}: literature, essay craft and debate on Hispanic society and culture, with the grammar to hold any argument.",
  ["Literary and film study", "Essay technique and argument",
   "Translation both ways", "Hispanic society and culture topics",
   "Examination practice throughout"]),
}

def copy_for(subjkey, year):
    key = subjkey
    if key not in SUBJ_COPY:
        k2 = key.rstrip('-0123456789')
        if k2 in SUBJ_COPY: key = k2
    if key not in SUBJ_COPY and 'igcse' in key:
        key = key.split('-igcse')[0]
    if key == 'portuguese': key = 'portuguese-1st'
    if key not in SUBJ_COPY: key = 'english'
    hook, blurb, bullets = SUBJ_COPY[key]
    return {'hook': hook, 'blurb': blurb.format(year=year), 'bullets': bullets}
