#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate all 40 Stage 5 lesson markdown files — Morphology, Fluency, Composition, Grammar."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "lessons" / "stage-5"
OUT.mkdir(parents=True, exist_ok=True)

# ── ROOT DATA ───────────────────────────────────────────────────────

ROOTS = [
    ("dict", "say, speak", "Latin", "dict", "The root DICT means 'say' or 'speak.' Every word with DICT has something to do with speaking or saying.",
     [("dictate","dict + ate","say with authority"),("dictionary","dict + ion + ary","book that 'says' what words mean"),
      ("predict","pre (before) + dict","say before it happens"),("verdict","ver (true) + dict","true saying — a jury's decision"),
      ("contradict","contra (against) + dict","say against"),("dictator","dict + at + or","one who says what to do"),
      ("diction","dict + ion","manner of speaking words")],
     ["dictate","predict","contradict","dictionary","verdict"]),

    ("duct", "lead", "Latin", "duct/duc", "DUCT means 'lead' or 'draw.' Think of a duct — it leads air or water. Words with DUCT are about leading or being led.",
     [("conduct","con (with) + duct","lead together"),("product","pro (forward) + duct","something led forth / made"),
      ("duct","duct","tube that leads air"),("viaduct","via (road) + duct","bridge that leads a road"),
      ("deduct","de (down) + duct","lead down / subtract"),("introduce","intro (into) + duce","lead into")],
     ["conduct","product","duct","deduct","introduce"]),

    ("spect", "see, look", "Latin", "spect/spic", "SPECT means 'see' or 'look.' A spectator looks, an inspector looks into things, and spectacles help you see!",
     [("inspect","in (into) + spect","look into carefully"),("spectator","spect + at + or","one who watches"),
      ("respect","re (back) + spect","look back at with honor"),("spectacle","spect + acle","amazing sight"),
      ("prospect","pro (forward) + spect","look forward to"),("suspect","sus (under) + spect","look under / doubt")],
     ["inspect","spectator","respect","spectacle","suspect"]),

    ("port", "carry", "Latin", "port", "PORT means 'carry.' A porter carries luggage. A transport carries goods. An import is carried IN, an export is carried OUT.",
     [("transport","trans (across) + port","carry across"),("portable","port + able","able to be carried"),
      ("import","im (in) + port","carry in"),("export","ex (out) + port","carry out"),
      ("report","re (back) + port","carry back / tell"),("porter","port + er","one who carries")],
     ["transport","portable","import","export","report"]),

    ("form", "shape", "Latin", "form", "FORM means 'shape' or 'structure.' To FORM something is to shape it. Information shapes your thinking.",
     [("transform","trans (across) + form","change shape"),("uniform","uni (one) + form","one shape — same clothes"),
      ("perform","per (through) + form","carry out a shape / execute"),("reform","re (again) + form","shape again"),
      ("formation","form + ation","the act of shaping"),("inform","in (into) + form","give shape / knowledge")],
     ["transform","uniform","perform","reform","inform"]),

    ("struct", "build", "Latin", "struct", "STRUCT means 'build.' A structure is something built. To construct is to build together. To destroy is to un-build.",
     [("construct","con (together) + struct","build together"),("structure","struct + ure","something built"),
      ("destruct","de (down) + struct","tear down / un-build"),("instruct","in (into) + struct","build knowledge into"),
      ("obstruct","ob (against) + struct","build against / block"),("reconstruct","re (again) + construct","build again")],
     ["construct","structure","destruct","instruct","obstruct"]),

    ("rupt", "break", "Latin", "rupt", "RUPT means 'break.' An erupting volcano breaks open. A corrupt person is morally broken. A disruption breaks the flow.",
     [("erupt","e (out) + rupt","break out"),("rupture","rupt + ure","a break or tear"),
      ("interrupt","inter (between) + rupt","break between"),("corrupt","cor (completely) + rupt","completely broken / dishonest"),
      ("disrupt","dis (apart) + rupt","break apart"),("abrupt","ab (off) + rupt","broken off — sudden")],
     ["erupt","rupture","interrupt","corrupt","disrupt"]),

    ("ject", "throw", "Latin", "ject", "JECT means 'throw.' An ejector throws something out. To reject is to throw back. A projector throws light forward.",
     [("eject","e (out) + ject","throw out"),("reject","re (back) + ject","throw back / refuse"),
      ("project","pro (forward) + ject","throw forward"),("inject","in (into) + ject","throw into"),
      ("subject","sub (under) + ject","throw under / topic under discussion"),("object","ob (against) + ject","throw against / protest")],
     ["eject","reject","project","inject","subject"]),

    ("tract", "pull, draw", "Latin", "tract", "TRACT means 'pull' or 'draw.' A tractor pulls. To attract is to pull toward. A contract pulls people together.",
     [("tractor","tract + or","machine that pulls"),("attract","at (to) + tract","pull toward"),
      ("contract","con (together) + tract","pull together / agreement"),("extract","ex (out) + tract","pull out"),
      ("retract","re (back) + tract","pull back / take back"),("subtract","sub (under) + tract","pull under / take away")],
     ["tractor","attract","contract","extract","subtract"]),

    ("scrib/script", "write", "Latin", "scrib/script", "SCRIB and SCRIPT mean 'write.' To scribble is to write quickly. A script is what's written for a play. To describe is to write about.",
     [("describe","de (down) + scribe","write down / explain"),("script","script","something written"),
      ("scribble","scrib + ble","write carelessly"),("subscribe","sub (under) + scribe","write under / sign up"),
      ("manuscript","manu (hand) + script","written by hand"),("prescription","pre (before) + script + ion","written beforehand")],
     ["describe","script","scribble","manuscript","prescription"]),

    ("mit/miss", "send", "Latin", "mit/miss", "MIT and MISS mean 'send.' A missile is sent through the air. To admit is to send in. A mission is something you're sent to do.",
     [("submit","sub (under) + mit","send under / give in"),("mission","miss + ion","a sending / task"),
      ("transmit","trans (across) + mit","send across"),("admit","ad (to) + mit","send in / allow in"),
      ("dismiss","dis (away) + miss","send away"),("remit","re (back) + mit","send back / pay")],
     ["submit","mission","transmit","dismiss","admit"]),

    ("vid/vis", "see", "Latin", "vid/vis", "VID and VIS mean 'see.' A video lets you see. A visor lets you see through. To visit is to go see someone.",
     [("vision","vis + ion","the act of seeing"),("video","vid + eo","I see"),("visible","vis + ible","able to be seen"),
      ("visit","vis + it","go to see"),("evidence","e (out) + vid + ence","that which is seen / proof"),
      ("supervise","super (over) + vise","see over / manage")],
     ["vision","video","visible","visit","supervise"]),

    ("graph", "write", "Greek", "graph", "GRAPH means 'write' (Greek). A graph shows data in writing. A biography is a written life story. A phonograph writes sound.",
     [("autograph","auto (self) + graph","self-written / signature"),("photograph","photo (light) + graph","light-writing"),
      ("telegraph","tele (far) + graph","far-writing"),("geography","geo (earth) + graph + y","earth-writing / map-making"),
      ("biography","bio (life) + graph + y","life-writing"),("paragraph","para (beside) + graph","written beside")],
     ["autograph","photograph","telegraph","biography","paragraph"]),

    ("phon", "sound", "Greek", "phon", "PHON means 'sound' (Greek). A telephone carries sound from far away. A microphone makes small sounds big.",
     [("telephone","tele (far) + phon + e","far-sound"),("microphone","micro (small) + phon + e","small-sound amplifier"),
      ("phonics","phon + ics","science of sounds"),("symphony","sym (together) + phon + y","sounds together / orchestra"),
      ("phonograph","phono + graph","sound-writer"),("euphonic","eu (good) + phon + ic","good-sounding")],
     ["telephone","microphone","phonics","symphony","phonograph"]),

    ("bio", "life", "Greek", "bio", "BIO means 'life' (Greek). Biology is the study of life. A biography is a written life.",
     [("biology","bio + logy (study)","study of life"),("biography","bio + graph + y","written life-story"),
      ("biosphere","bio + sphere","life-sphere / Earth's living parts"),("antibiotic","anti (against) + bio + tic","against-life / kills bacteria"),
      ("biodegradable","bio + de (down) + grad + able","able to be broken down by life"),("symbiosis","sym (together) + bio + sis","living together")],
     ["biology","biography","biosphere","antibiotic","symbiosis"]),

    ("geo", "earth", "Greek", "geo", "GEO means 'earth' (Greek). Geography writes about the earth. Geology studies the earth.",
     [("geography","geo + graph + y","earth-writing / map study"),("geology","geo + logy","earth-study / rocks"),
      ("geometry","geo + metry (measure)","earth-measuring"),("geode","geo + de","earth-stone with crystals inside"),
      ("geocentric","geo + centr + ic","earth-centered"),("geothermal","geo + therm + al","earth-heat")],
     ["geography","geology","geometry","geode","geothermal"]),

    ("therm", "heat", "Greek", "therm", "THERM means 'heat' (Greek). A thermometer measures heat. Thermal means related to heat.",
     [("thermometer","thermo + meter (measure)","heat-measurer"),("thermal","therm + al","relating to heat"),
      ("thermostat","thermo + stat (standing)","heat-regulator"),("hypothermia","hypo (under) + therm + ia","under-heat / dangerously cold"),
      ("thermodynamics","thermo + dynam + ics","heat-power science"),("exothermic","exo (out) + therm + ic","heat-releasing")],
     ["thermometer","thermal","thermostat","hypothermia","exothermic"]),

    ("meter", "measure", "Greek", "meter/metr", "METER means 'measure' (Greek). A speedometer measures speed. A centimeter is a hundredth of a meter.",
     [("thermometer","thermo + meter","heat-measurer"),("speedometer","speedo + meter","speed-measurer"),
      ("diameter","dia (across) + meter","measure across"),("centimeter","centi (hundred) + meter","hundredth-measure"),
      ("symmetry","sym (together) + metry","measured together / balance"),("metric","metr + ic","related to measurement")],
     ["thermometer","diameter","centimeter","symmetry","metric"]),

    ("scope", "see", "Greek", "scope", "SCOPE means 'see' (Greek). A telescope sees far. A microscope sees small things. A periscope sees around.",
     [("telescope","tele (far) + scope","far-seer"),("microscope","micro (small) + scope","small-seer"),
      ("periscope","peri (around) + scope","around-seer"),("kaleidoscope","kalos (beautiful) + eidos + scope","beautiful-form seer"),
      ("horoscope","horo (hour) + scope","hour-seer / astrology"),("stethoscope","stetho (chest) + scope","chest-seer / doctor's tool")],
     ["telescope","microscope","periscope","kaleidoscope","horoscope"]),

    ("auto/tele", "self/far", "Greek", "auto/tele", "AUTO means 'self.' TELE means 'far' (Greek). An automobile moves by itself. A television sees far.",
     [("automatic","auto + mat (thinking) + ic","self-thinking / self-operating"),("automobile","auto + mobile (moving)","self-moving / car"),
      ("autograph","auto + graph","self-write / signature"),("telescope","tele + scope","far-see"),
      ("telephone","tele + phon + e","far-sound"),("telegraph","tele + graph","far-write")],
     ["automatic","automobile","autograph","telescope","telephone"]),

    ("micro/chron", "small/time", "Greek", "micro/chron", "MICRO means 'small.' CHRON means 'time' (Greek). A microbe is a small living thing. A chronicle records time.",
     [("microscope","micro + scope","small-seer"),("microphone","micro + phon + e","small-sound amplifier"),
      ("microbe","micro + be (life)","small life"),("chronic","chron + ic","lasting over time"),
      ("chronicle","chron + icle","record of time / history"),("synchronize","syn (same) + chron + ize","make same-time / coordinate")],
     ["microscope","microphone","microbe","chronic","synchronize"]),

    ("photo/logy", "light/study", "Greek", "photo/logy", "PHOTO means 'light.' LOGY means 'study of' (Greek). Photography is light-writing. Biology is the study of life.",
     [("photograph","photo + graph","light-write"),("photosynthesis","photo + syn (together) + thesis","light-putting-together / how plants eat"),
      ("photocopy","photo + copy","light-copy"),("biology","bio + logy","life-study"),
      ("geology","geo + logy","earth-study"),("technology","techno (skill) + logy","skill-study")],
     ["photograph","photosynthesis","biology","geology","technology"]),
]

# ── TEMPLATES ───────────────────────────────────────────────────────

ROOT_TMP = """# Lesson {n}: Root {display} — "{meaning}"

**Stage 5** · Lesson {n} · morphology

---

## Warm-Up: Phonogram Flash Review

> Flash all 75 phonograms. Under 2 seconds each!

---

## New Learning: The Root **{display}**

### Where It Comes From

**{display}** is a **{origin}** root that means **"{meaning}"**.

{description}

### Word Builder

| Word | Prefix | Root | Suffix | Meaning |
|------|--------|------|--------|---------|
{word_table}

---

## Spelling Analysis

| Word | Phonograms | Say-to-Spell |
|------|-----------|-------------|
{spelling}

---

## Word Detective

Fill in the blanks with a **{display}** word:

{detective}

---

## Quick Check

1. What does **{display}** mean? *({meaning})*
2. Build a new word using {display} + a prefix you know.
3. How does knowing roots help you read? *(You can figure out what unfamiliar words mean!)*

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: Find 3 words with **{display}** in a book. Write each and its meaning.*
"""

REVIEW5_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · review

---

## Warm-Up: Speed Flash

> Flash all 75 phonograms. Under 2 seconds each!

---

## {g1}

{gb1}

---

## {g2}

{gb2}

---

## {g3}

{gb3}

---

## Root Challenge

Spell these words from dictation. Name the root in each:

> {challenge}

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: {home}*
"""

VOCAB_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · vocabulary

---

## Warm-Up: Word of the Day

> Today's word: **{word}** — {definition}

---

## New Learning: {focus}

{body}

---

## Apply It

{apply}

---

## Reading

> {reading}

---

## Quick Check

{check}

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: {home}*
"""

FLUENCY_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · fluency

---

## Warm-Up: Phonogram Flash Review

> Flash all 75 phonograms. Speed is the goal!

---

## Fluency Practice: {focus}

{body}

---

## Timed Reading

Read this passage aloud 3 times. Time yourself each time. Try to get faster while staying accurate.

{passage}

| Reading | Time | Errors | Notes |
|---------|------|--------|-------|
| 1st | ___:___ | ___ | |
| 2nd | ___:___ | ___ | |
| 3rd | ___:___ | ___ | |

---

## Quick Check

1. What improved between your first and third reading?
2. What words were hardest?
3. Read the passage aloud one more time for a family member!

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: Read the passage aloud 2 more times tonight!*
"""

COMP_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · composition

---

## Warm-Up: Spelling Review

Write these words from dictation:

> {spell_words}

---

## Writing Lesson: {focus}

{body}

---

## Your Turn

{prompt}

---

## Check Your Work

- [ ] Did you sound out each word?
- [ ] Did you apply spelling rules?
- [ ] Did you use capital letters and periods?
- [ ] Did you read it back to check it makes sense?

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: {home}*
"""

GRAMMAR_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · grammar

---

## Warm-Up: Quick Write

Write one sentence about something you did yesterday. Underline the noun (who/what). Circle the verb (what happened).

---

## Grammar Lesson: {focus}

{body}

---

## Practice

{practice}

---

## Apply in Writing

Write 3 sentences that follow today's grammar pattern:

1. 
2. 
3. 

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: {home}*
"""

READER5_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · reader

---

## Story: {stitle}

{story}

---

## After Reading

{talk}

---

**Next lesson:** Lesson {nn}: {ntitle}

---

*Practice at home: Read this aloud to your family!*
"""

ASSESS5_TMP = """# Lesson {n}: {title}

**Stage 5** · Lesson {n} · assessment

---

## Overview

{overview}

---

## Part 1: Root Knowledge

Match each root to its meaning:

| Root | Meaning | ✓ |
|------|---------|---|
{root_check}

**Score:** __ / {root_total}

---

## Part 2: Word Reading (Timed)

Read these words aloud. Goal: under 30 seconds, 0 errors.

| Word | ✓ | Word | ✓ |
|------|---|------|---|
{read_check}

**Score:** __ / {read_total}

---

## Part 3: Spelling (Dictation)

| Word | ✓ |
|------|---|
{spell_check}

**Score:** __ / {spell_total}

---

## Part 4: Writing

Write a paragraph (4-6 sentences) on this topic: {topic}

Checklist:
- [ ] Complete sentences
- [ ] Correct spelling
- [ ] Capital letters and punctuation
- [ ] Makes sense when read aloud

**Score:** __ / 4

---

## Results

| Section | Score | Pass? |
|---------|-------|-------|
| Roots | __/{root_total} | |
| Reading | __/{read_total} | |
| Spelling | __/{spell_total} | |
| Writing | __/4 | |

**Overall:** __/{{overall_total}}

## Next Steps

{next}

---

*You've completed all 5 stages! You now know all 75 basic phonograms, 31 spelling rules, and can decode 98% of English words. Congratulations!*
"""

# ── HELPERS ─────────────────────────────────────────────────────────

def nt(n):
    t = {
        1:"Review Stage 4",2:"Root: dict",3:"Root: duct",4:"Root: spect",
        5:"Root: port",6:"Root: form",7:"Root: struct",8:"Root: rupt",
        9:"Root: ject",10:"Root: tract",11:"Root: scrib/script",
        12:"Root: mit/miss",13:"Root: vid/vis",14:"Latin Roots Review 1",
        15:"Root: graph",16:"Root: phon",17:"Root: bio",18:"Root: geo",
        19:"Root: therm",20:"Root: meter",21:"Root: scope",
        22:"Roots: auto + tele",23:"Roots: micro + chron",
        24:"Roots: photo + logy",25:"Greek Roots Review",
        26:"All Roots Review",
        27:"Vocab: Tier 2 Words",28:"Vocab: Synonyms",
        29:"Vocab: Word Relationships",
        30:"Fluency: Repeated Reading",31:"Fluency: Phrasing",
        32:"Fluency: Reading Rate",
        33:"Composition: Sentences",34:"Composition: Paragraphs",
        35:"Composition: Spelling in Writing",
        36:"Grammar: Parts of Speech",37:"Grammar: Sentence Types",
        38:"Grammar: Punctuation",
        39:"Reader: Ostriches",40:"Stage 5 Mastery Check",
    }
    return t.get(n, f"Lesson {n}")

# ── BUILDERS ────────────────────────────────────────────────────────

def build_root(n, root, meaning, origin, display, description, examples, spell_words, nn):
    # Simple word table from examples
    word_table = "\n".join(f"| {e[0]} | {e[1]} | {e[2]} |" for e in examples)
    
    spelling = "\n".join(f"| {w} | (sound out) | /{w}/ |" for w in spell_words[:5])
    
    # Detective questions
    det_words = [e[0] for e in examples[:4]]
    detective = f"""1. The teacher asked us to ___ the experiment carefully. (conduct? inspect?) — *inspect*
2. A ___ is someone who watches a game. (spectator? prospect?) — *spectator*
3. We should ___ our elders. (respect? suspect?) — *respect*
4. The fireworks were an amazing ___! (spectacle? inspect?) — *spectacle*"""
    
    # Generic detective for roots
    if len(det_words) >= 3:
        detective = f"1. I need to {det_words[0]} this word. *(Write it!)*\n2. A {det_words[1]} is an amazing thing to see.\n3. Everyone should {det_words[2]} the rules."
    else:
        detective = f"1. Use **{display}** in a sentence.\n2. What does **{display}** tell you about a word you've never seen before?\n3. Find a **{display}** word in a book and write it here."
    
    return ROOT_TMP.format(n=n, root=root, meaning=meaning, origin=origin, display=display,
        description=description, word_table=word_table, spelling=spelling,
        detective=detective, nn=nn, ntitle=nt(nn))

def build_root_lesson(n, idx, nn):
    r = ROOTS[idx]
    return build_root(n, r[0], r[1], r[2], r[3], r[4], r[5], r[6], nn)

def build_review5(n, title, g1, gb1, g2, gb2, g3, gb3, challenge, home, nn):
    return REVIEW5_TMP.format(n=n, title=title, g1=g1, gb1=gb1, g2=g2, gb2=gb2, g3=g3, gb3=gb3,
        challenge=", ".join(challenge), home=home, nn=nn, ntitle=nt(nn))

def build_vocab(n, title, focus, word, definition, body, apply_section, reading, check, home, nn):
    return VOCAB_TMP.format(n=n, title=title, focus=focus, word=word, definition=definition,
        body=body, apply=apply_section, reading=reading, check=check, home=home, nn=nn, ntitle=nt(nn))

def build_fluency(n, title, focus, body, passage, nn):
    return FLUENCY_TMP.format(n=n, title=title, focus=focus, body=body, passage=passage, nn=nn, ntitle=nt(nn))

def build_comp(n, title, focus, body, prompt, spell_words, home, nn):
    return COMP_TMP.format(n=n, title=title, focus=focus, body=body, prompt=prompt,
        spell_words=", ".join(spell_words), home=home, nn=nn, ntitle=nt(nn))

def build_grammar(n, title, focus, body, practice, home, nn):
    return GRAMMAR_TMP.format(n=n, title=title, focus=focus, body=body, practice=practice,
        home=home, nn=nn, ntitle=nt(nn))

# ── CONTENT ─────────────────────────────────────────────────────────

def gen_review_s4():
    return REVIEW5_TMP.format(n=1, title="Review Stage 4 Concepts", nn=2, ntitle=nt(2),
        g1="Schwa & Say-to-Spell", gb1="Say-to-spell: about, seven, pencil, love, mother, dollar, doctor, animal, family, chocolate. Which rule applies to each?",
        g2="Suffixing Rules", gb2="Write the -ing or -ed form: make, hop, run, cry, carry, study, bake. Name the rule for each (13, 14, 15, or 16).",
        g3="Latin /sh/ & Morphology", gb3="Spell: nation, special, vision, musician, teacher, careful, submarine, disagree. Name the root or prefix/suffix in each.",
        challenge="about, making, hopping, nation, special, beautiful, dictionary, transport, inspect",
        home="Review all flashcards from Stages 1-4!")

def gen_vocab_27():
    return VOCAB_TMP.format(n=27, nn=28, ntitle=nt(28),
        title="Vocabulary: Tier 2 Words in Context", focus="Tier 2 Vocabulary",
        word="analyze", definition="to examine carefully and in detail",
        body="""### What Are Tier 2 Words?

Tier 2 words are words that appear across many different subjects and books, but aren't everyday conversation words. They're the 'academic' words that help you understand science, history, and literature.

| Tier | Description | Examples |
|------|------------|----------|
| Tier 1 | Everyday spoken words | dog, run, happy, big |
| Tier 2 | Academic, cross-subject words | analyze, compare, contrast, describe |
| Tier 3 | Subject-specific words | phonogram, bioluminescence, photosynthesis |

Today's Tier 2 words:

| Word | Meaning | Example |
|------|---------|---------|
| analyze | examine carefully | "Analyze the spelling of 'nation.'" |
| compare | find similarities | "Compare 'nation' and 'action' — what's the same?" |
| contrast | find differences | "Contrast 'special' and 'social' — how are they different?" |
| describe | tell about in detail | "Describe how silent E works." |
| explain | make clear | "Explain Rule 17." |""",
        apply="""Use each word in a sentence about spelling or reading:

1. analyze: _________________________________
2. compare: _________________________________
3. contrast: _________________________________
4. describe: _________________________________
5. explain: _________________________________""",
        reading="Analyze the spelling of 'transport.' Compare it to 'portable.' Contrast the prefixes. Describe how the root 'port' works. Explain the meaning of each word.",
        check="1. What is a Tier 2 word? *(An academic word used across many subjects.)*\n2. Give a new example of a Tier 2 word.\n3. Use 'analyze' in a sentence.",
        home="Find 3 Tier 2 words in a book. Write them and their meanings.")

def gen_vocab_28():
    return VOCAB_TMP.format(n=28, nn=29, ntitle=nt(29),
        title="Vocabulary: Synonyms and Antonyms", focus="Synonyms & Antonyms",
        word="synonym", definition="a word with the same or similar meaning",
        body="""### Synonyms = Same

Synonyms are words that mean the same (or almost the same) thing.

| Word | Synonym |
|------|---------|
| big | large, huge, enormous |
| small | tiny, little, miniature |
| happy | glad, joyful, cheerful |
| sad | unhappy, gloomy, miserable |
| fast | quick, rapid, swift |
| smart | clever, intelligent, bright |

### Antonyms = Opposite

Antonyms are words with opposite meanings.

| Word | Antonym |
|------|---------|
| big | small |
| happy | sad |
| fast | slow |
| hot | cold |
| light | dark |
| open | closed |

### Why Synonyms and Antonyms Matter

Using different words makes your writing more interesting! Instead of 'The big dog was big and had a big bark,' try 'The enormous dog was huge and had a gigantic bark.'""",
        apply="""Find a synonym AND an antonym for each:

| Word | Synonym | Antonym |
|------|---------|---------|
| quick | | |
| strong | | |
| quiet | | |
| bright | | |
| brave | | |""",
        reading="The enormous elephant was not small. The joyful child was not sad. The rapid train was not slow. The brilliant light was not dark.",
        check="1. What is a synonym? *(A word with the same/similar meaning.)*\n2. What is an antonym? *(A word with opposite meaning.)*\n3. Give a synonym AND antonym for 'big.'",
        home="Find 5 synonym pairs and 5 antonym pairs in a book.")

def gen_vocab_29():
    return VOCAB_TMP.format(n=29, nn=30, ntitle=nt(30),
        title="Vocabulary: Word Relationships", focus="Word Relationships",
        word="relationship", definition="how two things are connected",
        body="""### How Words Connect

Words can relate to each other in different ways:

| Relationship | Example | Explanation |
|-------------|---------|-------------|
| Synonyms | big/large | Same meaning |
| Antonyms | hot/cold | Opposite meaning |
| Part-Whole | finger/hand | A finger is PART of a hand |
| Category | apple/fruit | An apple is a TYPE of fruit |
| Function | hammer/nail | A hammer is USED WITH a nail |
| Degree | warm/hot/scalding | Different levels of heat |

### Practice: Name the Relationship

| Pair | Relationship |
|------|-------------|
| dog/animal | category |
| wheel/car | part-whole |
| happy/sad | antonym |
| tiny/huge | antonym (degree) |
| pen/paper | function |
| run/jog | synonym (degree) |""",
        apply="""Name the relationship for each pair:

1. teacher/school — _______________
2. car/vehicle — _______________
3. whisper/scream — _______________
4. leaf/tree — _______________
5. pencil/write — _______________""",
        reading="A dog is a type of animal. A finger is part of a hand. A hammer is used with a nail. Warm and hot show different degrees of heat.",
        check="1. Name 3 types of word relationships.\n2. What's the relationship between 'oak' and 'tree'? *(Category — an oak is a type of tree.)*\n3. Invent your own word pair and name the relationship.",
        home="Find 5 word pairs in a book and name their relationship.")

def gen_fluency_30():
    return FLUENCY_TMP.format(n=30, nn=31, ntitle=nt(31),
        title="Fluency: Repeated Reading", focus="Repeated Reading",
        body="""### What Is Repeated Reading?

Reading the same passage several times helps you get faster, smoother, and more accurate. Each time you read, your brain recognizes more words automatically.

### How to Practice

1. Read the passage once. Time yourself.
2. Read it again. Try to beat your time.
3. Read it a third time. Focus on smooth, natural reading — not just speed!""",
        passage="""**The Discovery**

Dr. Maria Santiago made an important discovery in her laboratory. For years, she had been inspecting microscopic organisms from deep ocean vents. These tiny life forms lived in complete darkness, under enormous pressure, at temperatures that would destroy most living things.

One day, Dr. Santiago noticed something extraordinary. One of the organisms produced a brilliant blue light when she introduced a specific compound. This bioluminescent reaction was unlike anything previously documented.

"This could transform our understanding of deep-sea biology," she wrote in her notebook.

Dr. Santiago submitted her findings to a scientific journal. The report described how the organism's light-producing structure could potentially be used in medical imaging technology.

The discovery attracted international attention. Newspapers reported on "The Deep Sea's Nightlight." Scientists from around the world requested samples. A new chapter in marine biology had begun.

And it all started with careful observation and patient inspection of the smallest ocean creatures.""",
)

def gen_fluency_31():
    return FLUENCY_TMP.format(n=31, nn=32, ntitle=nt(32),
        title="Fluency: Phrasing and Expression", focus="Phrasing & Expression",
        body="""### Reading with Expression

Fluent readers don't sound like robots. They:
- Group words into meaningful phrases
- Change their voice for questions, excitement, sadness
- Pause at commas and periods
- Emphasize important words

### Practice These Phrases

Read each line smoothly, as one phrase:

- Over the mountains
- Through the deep forest
- With great excitement
- After the storm passed
- Before the sun rose""",
        passage="""**The Storm**

The sky grew dark. The wind began to howl. (pause — build tension)

Suddenly, lightning split the sky! (excitement) Thunder crashed like a thousand drums. The rain poured down in sheets, washing the dusty streets clean.

"Get inside!" called Mother. "Quickly now!" (urgency)

The children ran through the garden gate, their feet splashing in the fresh puddles. They burst through the kitchen door, laughing and dripping wet.

"Did you see that lightning?" asked Theo, his eyes wide.

"It was magnificent!" exclaimed Lily. "Absolutely magnificent!"

The storm raged for an hour. Then, as suddenly as it began, it stopped. The clouds parted. The sun emerged.

"Look!" whispered Lily, pointing at the sky.

A perfect rainbow stretched from horizon to horizon — a silent promise after the storm's fury.

(Read the last line slowly, with wonder.)""",
)

def gen_fluency_32():
    return FLUENCY_TMP.format(n=32, nn=33, ntitle=nt(33),
        title="Fluency: Reading Rate", focus="Reading Rate",
        body="""### Finding the Right Speed

Good readers adjust their speed:
- **Faster** for easy, familiar text
- **Slower** for challenging, unfamiliar text
- **Medium** for most reading

### Rate Goals (Words Per Minute)

| Grade | Fall | Spring |
|-------|------|--------|
| Grade 1 | — | 40-60 |
| Grade 2 | 50-80 | 80-100 |
| Grade 3 | 70-100 | 100-130 |

### How to Calculate

1. Count the words in the passage below (150 words)
2. Time your reading in seconds
3. WPM = (words ÷ seconds) × 60

Example: 150 words ÷ 90 seconds = 1.67 × 60 = 100 WPM""",
        passage="""**The Elephant's Memory** (150 words)

Elephants have remarkable memories. Scientists have conducted extensive research on elephant cognition, and the results are extraordinary. An elephant can remember the location of water holes it visited decades ago. It can recognize individual humans it met years before. It remembers other elephants — even after long separations.

In one famous study, researchers played recorded calls of elephants that had died. The living elephants responded with clear signs of recognition and distress. They remembered their lost family members.

This incredible memory serves a vital purpose. In the harsh African savanna, remembering where to find water during a drought means the difference between life and death. The matriarch — the oldest female — leads the herd using her accumulated knowledge of the landscape.

Elephants teach us that intelligence takes many forms. Their wisdom is written not in books, but in the living memory passed from generation to generation.""",
)

def gen_comp_33():
    return COMP_TMP.format(n=33, nn=34, ntitle=nt(34),
        title="Composition: Sentence Building", focus="Sentence Building",
        body="""### What Makes a Complete Sentence?

Every sentence needs:
1. **A subject** (who or what)
2. **A verb** (what happened / what they did)
3. **A complete thought**

| Fragment | Complete Sentence |
|----------|-------------------|
| The big dog | The big dog ran fast. |
| Running quickly | The cat was running quickly. |
| In the park | We played in the park. |
| Because it rained | We stayed inside because it rained. |

### Building Longer Sentences

Add details: **when, where, why, how**

| Short | With Details |
|-------|-------------|
| The dog barked. | The enormous brown dog barked loudly at the mailman. |
| She read. | She read an exciting book about dinosaurs in her cozy room. |""",
        prompt="""Build each fragment into a complete sentence with details:

1. The bird sang ________________________________________________
2. My friend ________________________________________________
3. During the storm ________________________________________________
4. The scientist ________________________________________________
5. Under the bridge ________________________________________________""",
        spell_words=["about","making","inspect","transport","dictionary","beautiful"],
        home="Write 5 complete sentences about your day. Add details to each one!")

def gen_comp_34():
    return COMP_TMP.format(n=34, nn=35, ntitle=nt(35),
        title="Composition: Paragraph Writing", focus="Paragraph Writing",
        body="""### What Is a Paragraph?

A paragraph is a group of sentences about ONE topic.

**Parts of a paragraph:**
1. **Topic sentence** — tells what the paragraph is about
2. **Supporting sentences** — give details, examples, facts
3. **Closing sentence** — wraps it up

### Example Paragraph

**Elephants have remarkable memories.** Scientists have found that elephants can remember water holes from decades ago. They recognize elephants and humans they haven't seen in years. One study showed elephants responding to recorded calls of deceased family members. **This extraordinary memory helps elephants survive in harsh environments.**""",
        prompt="""Write a paragraph about ONE of these topics:

1. Your favorite animal
2. A place you would like to visit
3. Something you learned in reading lessons

Use at least 4 sentences. Include a topic sentence and a closing sentence.""",
        spell_words=["elephant","remarkable","scientist","recognize","extraordinary"],
        home="Write a paragraph about your day. Make sure it has a topic sentence and a closing sentence!")

def gen_comp_35():
    return COMP_TMP.format(n=35, nn=36, ntitle=nt(36),
        title="Composition: Apply Spelling Rules in Writing", focus="Spelling Rules in Writing",
        body="""### Writing Is Spelling Practice!

When you write, use ALL the spelling tools you've learned:
1. Sound out each word
2. Use say-to-spell for tricky words
3. Apply the 31 rules
4. Check for silent E, double letters, Latin /sh/

### Before You Write: Think

- Which phonograms will I need?
- Are there any tricky schwa vowels?
- Is there a suffix? (Drop E? Double? Y→I?)

### After You Write: Check

1. Read each word aloud — does it look right?
2. Underline any words you're unsure about
3. Say-to-spell the uncertain words
4. Fix any mistakes you find""",
        prompt="""Write 5 sentences about a discovery or invention. Use at least 3 words from this list:

transport, inspect, describe, dictionary, beautiful, action, special, vision, automatic

After writing, check each word using the steps above.""",
        spell_words=["discovery","invention","describe","transport","automatic","special"],
        home="Write a short story (4-5 sentences). Check every word for correct spelling!")

def gen_grammar_36():
    return GRAMMAR_TMP.format(n=36, nn=37, ntitle=nt(37),
        title="Grammar: Parts of Speech Review", focus="Parts of Speech",
        body="""### The 8 Parts of Speech

| Part | What It Does | Examples |
|------|-------------|----------|
| **Noun** | Person, place, thing, idea | dog, park, happiness |
| **Verb** | Action or state of being | run, is, think |
| **Adjective** | Describes a noun | big, blue, happy |
| **Adverb** | Describes a verb/adjective/adverb | quickly, very, well |
| **Pronoun** | Replaces a noun | he, she, it, they |
| **Preposition** | Shows position/relationship | in, on, under, between |
| **Conjunction** | Joins words/sentences | and, but, or, because |
| **Interjection** | Shows emotion | Wow! Oh! Oops! |

### Find Each Part of Speech

"The happy scientist quickly inspected the specimen under the microscope, and she exclaimed, 'Wow!'"

| Word | Part of Speech |
|------|---------------|
| scientist | noun |
| happy | adjective |
| quickly | adverb |
| inspected | verb |
| under | preposition |
| and | conjunction |
| Wow! | interjection |
| she | pronoun |""",
        practice="""Label each word: The (___) enormous (___) elephant (___) slowly (___) walked (___) through (___) the (___) jungle (___).

Answers: article, adjective, noun, adverb, verb, preposition, article, noun""",
        home="Write 3 sentences. Label every part of speech in each one!")

def gen_grammar_37():
    return GRAMMAR_TMP.format(n=37, nn=38, ntitle=nt(38),
        title="Grammar: Sentence Types", focus="Sentence Types",
        body="""### Four Types of Sentences

| Type | Purpose | Ends With | Example |
|------|---------|-----------|---------|
| Declarative | States a fact | Period (.) | The elephant is enormous. |
| Interrogative | Asks a question | Question mark (?) | Is the elephant enormous? |
| Exclamatory | Shows strong feeling | Exclamation (!) | What an enormous elephant! |
| Imperative | Gives a command | Period (.) or (!) | Look at the enormous elephant. |

### Identify Each Type

1. How do elephants remember water holes? — *interrogative*
2. Elephants have remarkable memories. — *declarative*
3. What an incredible memory! — *exclamatory*
4. Tell me about elephant memory. — *imperative*""",
        practice="""Write one of each sentence type about your favorite animal:

1. Declarative: ________________________________________________
2. Interrogative: ________________________________________________
3. Exclamatory: ________________________________________________
4. Imperative: ________________________________________________""",
        home="Find one of each sentence type in a book. Write them down!")

def gen_grammar_38():
    return GRAMMAR_TMP.format(n=38, nn=39, ntitle=nt(39),
        title="Grammar: Punctuation", focus="Punctuation",
        body="""### Punctuation Marks

| Mark | Name | Use |
|------|------|-----|
| . | Period | End of statement or command |
| ? | Question Mark | End of question |
| ! | Exclamation Mark | End of exclamation |
| , | Comma | Pause, list separator |
| " " | Quotation Marks | Around spoken words |
| ' | Apostrophe | Possession (dog's) or contraction (can't) |

### Fix the Punctuation

1. the dog barked loudly → The dog barked loudly.
2. where is the elephant → Where is the elephant?
3. what an incredible discovery → What an incredible discovery!
4. i need pencils paper and a ruler → I need pencils, paper, and a ruler.
5. she said i love reading → She said, "I love reading."
6. the dogs bone is buried → The dog's bone is buried.""",
        practice="""Add correct punctuation:

1. Dr Santiago made a discovery ____
2. Did she inspect the organism ____
3. What a brilliant blue light ____
4. She said this is extraordinary ____ ____
5. The scientists notebook was full ____ ____""",
        home="Write 5 sentences using all 5 punctuation marks correctly!")

def gen_ostrich_reader():
    return READER5_TMP.format(n=39, nn=40, ntitle=nt(40),
        title="Reader: Ostriches", stitle="Ostriches: The Giants of the Bird World",
        story="""<div class="reader-page">
<div class="reader-text">

**Ostriches: The Giants of the Bird World**

Ostriches are the largest birds on Earth. An adult ostrich can stand over 8 feet tall and weigh more than 300 pounds. That's taller than a professional basketball player and heavier than a lion!

Despite their enormous size, ostriches cannot fly. Their wings are too small to lift their heavy bodies. But what they lack in flight, they make up for in speed.

An ostrich can run at speeds up to 45 miles per hour. That's faster than most horses! Their long, powerful legs can cover 16 feet in a single stride. When threatened, an ostrich can deliver a kick strong enough to injure a lion.

Ostriches live in the grasslands and savannas of Africa. They travel in groups called flocks, sometimes with zebras and antelopes. With their excellent eyesight — they can spot movement from over two miles away — ostriches serve as lookouts for the entire group.

The ostrich's diet consists mainly of plants, seeds, and insects. They will also swallow small stones and pebbles, which help grind up food in their stomach. An ostrich can go for days without drinking water, getting moisture from the plants they eat.

Contrary to popular belief, ostriches do not bury their heads in the sand. This myth probably started because ostriches lay their eggs in shallow holes in the ground and sometimes put their heads low to turn the eggs. From a distance, it looks like the head is buried!

Ostriches lay the largest eggs of any living bird — each one weighs about 3 pounds, equivalent to two dozen chicken eggs. The shell is so thick and strong that a grown person can stand on it without breaking it.

Ostriches have been domesticated on farms around the world. Their feathers are used for decoration and dusters. Their skin makes fine leather. Their meat is lean and healthy. But in the wild, these magnificent giants continue to race across the African plains — living proof that you don't need to fly to be extraordinary.

The End.

</div>
<div class="reader-sidebar">

### Spelling Aid

**Roots in this passage:**
- transport — Port (carry)
- domesticated — Dom (house)
- extraordinary — Extra (beyond) + ordin (order)
- inspect — Spect (see)

**Challenge words:**
- savannas — double N
- equivalent — Latin: equi (equal) + val (worth)
- magnificent — Latin: magnus (great)

</div>
</div>""",
        talk="1. How fast can an ostrich run? *(Up to 45 mph!)*\n2. Why can't ostriches fly? *(Their wings are too small for their heavy bodies.)*\n3. Find words with Latin/Greek roots in the passage.",
)

def gen_final_assessment():
    return ASSESS5_TMP.format(n=40, title="Stage 5 Mastery Check",
        overview="Final assessment for the entire curriculum. Tests morphology knowledge, reading fluency, spelling accuracy, and writing.",
        root_check="| dict | | ☐ |\n| duct | | ☐ |\n| spect | | ☐ |\n| port | | ☐ |\n| rupt | | ☐ |\n| ject | | ☐ |\n| tract | | ☐ |\n| scrib | | ☐ |\n| mit/miss | | ☐ |\n| graph | | ☐ |\n| phon | | ☐ |\n| bio | | ☐ |\n| geo | | ☐ |\n| therm | | ☐ |\n| meter | | ☐ |\n| scope | | ☐ |\n| auto | | ☐ |\n| tele | | ☐ |",
        root_total=18,
        read_check="| transport | ☐ | | inspect | ☐ |\n| microscope | ☐ | | telephone | ☐ |\n| biography | ☐ | | automatic | ☐ |\n| structure | ☐ | | dictionary | ☐ |\n| eruption | ☐ | | photograph | ☐ |\n| describe | ☐ | | thermostat | ☐ |",
        read_total=12,
        spell_check="| transport | ☐ |\n| dictionary | ☐ |\n| microscope | ☐ |\n| telephone | ☐ |\n| biography | ☐ |\n| automatic | ☐ |\n| structure | ☐ |\n| inspect | ☐ |\n| photograph | ☐ |\n| describe | ☐ |",
        spell_total=10,
        topic="Write a paragraph about an animal that interests you. Use at least 3 words with Latin or Greek roots. Check your spelling!",
        next="If ≥85%: You've completed the full curriculum! Celebrate this achievement. If weaker, review specific root lessons.",
    )

# ── MAIN ────────────────────────────────────────────────────────────

def generate():
    # 2-13: Latin Roots Set 1
    for i in range(12):
        n, nn = 1+i, 2+i
        yield n, build_root_lesson(n, i, nn)
    
    # 14: Latin Roots Review
    yield 13, build_review5(13, "Latin Roots Review Set 1",
        "Match Root to Meaning",
        "dict (say), duct (lead), spect (see), port (carry), form (shape), struct (build), rupt (break), ject (throw), tract (pull), scrib (write), mit/miss (send), vid/vis (see)",
        "Root Detective",
        "Which root is in: dictionary? (dict) transport? (port) inspect? (spect) construct? (struct) erupt? (rupt) eject? (ject) mission? (miss) visible? (vis)",
        "Spell with Roots",
        "Write: predict, conduct, spectator, portable, transform, structure, interrupt, reject, attract, describe, submit, vision.",
        ["predict","conduct","spectator","portable","transform","structure","interrupt","reject","attract","describe"],
        "Review all 12 Latin roots flashcards!", 15)

    # 15-24: Greek Roots
    for i in range(12, 22):
        n = 2 + i  # 15 through 24
        nn = n + 1
        yield n, build_root_lesson(n, i, nn)

    # 25: Greek Roots Review
    yield 24, build_review5(24, "Greek Roots Review",
        "Match Root to Meaning",
        "graph (write), phon (sound), bio (life), geo (earth), therm (heat), meter (measure), scope (see), auto (self), tele (far), micro (small), chron (time), photo (light), logy (study)",
        "Root Detective",
        "Which root is in: photograph? (graph + photo) biology? (bio + logy) thermometer? (therm + meter) telescope? (tele + scope) geography? (geo + graph)",
        "Spell with Roots",
        "Write: photograph, biology, thermometer, telescope, geography, automatic, microphone, chronicle.",
        ["photograph","biology","thermometer","telescope","geography","automatic","microphone"],
        "Review all 13 Greek roots flashcards!", 26)

    # 26: All Roots Review
    yield 25, build_review5(25, "All Roots Review",
        "Latin vs Greek",
        "Sort: dict (L), graph (G), spect (L), phon (G), port (L), bio (G), rupt (L), geo (G), ject (L), meter (G).",
        "Word Build Challenge",
        "Build a word containing: spect (inspect), port (transport), graph (photograph), phon (telephone), rupt (interrupt), bio (biology), duct (conduct), scope (microscope).",
        "Root Meaning Speed Round",
        "Adult says root, child says meaning. Go fast! dict, duct, spect, port, form, struct, rupt, ject, tract, scrib, mit, vis, graph, phon, bio, geo, therm, meter, scope, auto, tele, micro, chron, photo, logy.",
        ["predict","conduct","inspect","transport","transform","destruct","eject","attract","describe","submit","photograph","biology","thermometer","telescope","automatic"],
        "You know 25 Latin and Greek roots! That unlocks thousands of words.", 27)

    # 27-29: Vocabulary
    yield 26, gen_vocab_27()
    yield 27, gen_vocab_28()
    yield 28, gen_vocab_29()

    # 30-32: Fluency
    yield 29, gen_fluency_30()
    yield 30, gen_fluency_31()
    yield 31, gen_fluency_32()

    # 33-35: Composition
    yield 32, gen_comp_33()
    yield 33, gen_comp_34()
    yield 34, gen_comp_35()

    # 36-38: Grammar
    yield 35, gen_grammar_36()
    yield 36, gen_grammar_37()
    yield 37, gen_grammar_38()

    # 39: Reader
    yield 38, gen_ostrich_reader()

    # 40: Assessment
    yield 39, gen_final_assessment()

# ── SLUGS ───────────────────────────────────────────────────────────

S = {
    
    1:"root-dict",2:"root-duct",3:"root-spect",4:"root-port",
    5:"root-form",6:"root-struct",7:"root-rupt",8:"root-ject",
    9:"root-tract",10:"root-scrib",11:"root-mit-miss",12:"root-vid-vis",
    13:"latin-review-1",
    14:"root-graph",15:"root-phon",16:"root-bio",17:"root-geo",
    18:"root-therm",19:"root-meter",20:"root-scope",
    21:"root-auto-tele",22:"root-micro-chron",23:"root-photo-logy",
    24:"greek-review-1",
    25:"all-roots-review",
    26:"vocab-1",27:"vocab-2",28:"vocab-3",
    29:"fluency-1",30:"fluency-2",31:"fluency-3",
    32:"composition-1",33:"composition-2",34:"composition-3",
    35:"grammar-1",36:"grammar-2",37:"grammar-3",
    38:"reader-7",39:"assessment-8",
}

def main():
    for num, content in generate():
        slug = S.get(num, f"lesson-{num:03d}")
        (OUT / f"{slug}.md").write_text(content, encoding="utf-8")
        print(f"  lessons/stage-5/{slug}.md")
    print(f"\nDone! 40 lessons in lessons/stage-5/")

if __name__ == "__main__":
    main()
