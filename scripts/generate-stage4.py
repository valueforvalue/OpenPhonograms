#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate all 48 Stage 4 lesson markdown files via Jinja templates.

Architecture (slice 4 of #22 + #23):
  - Phonogram + rule data lives in data/*.yaml; loaded via framework.data_loader.
  - Stage-4-specific data (PREFIXES, SUFFIXES, etc.) stays inline — per Slice 0 decision.
  - Lesson scaffolds live in templates/stage-4/*.md.j2.
  - This file is a thin orchestrator: compute template vars + render.
  - Long-form rule/practice/reader content is rendered from 7 shared templates
    (schwa, rule, practice, rule-full, morph, reader4, assessment, review).
"""

import io
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "lessons" / "stage-4"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR = PROJECT_ROOT / "templates" / "stage-4"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Issue #24: stamp every generated MD with the current version.
sys.path.insert(0, str(PROJECT_ROOT / "framework"))
from stamp import stamp  # noqa: E402  # issue #24: version stamp on every MD

# ── JINJA ENVIRONMENT ────────────────────────────────────────────────

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)

# Template name mapping (used by render() helper)
_TPL = {
    "schwa": "schwa.md.j2",
    "rule": "rule.md.j2",
    "practice": "practice.md.j2",
    "rule-full": "rule-full.md.j2",
    "morph": "morph.md.j2",
    "reader4": "reader4.md.j2",
    "assessment": "assessment.md.j2",
    "review": "review.md.j2",
}


def render(tpl_name: str, **vars) -> str:
    """Render a Stage 4 template by short name with given vars."""
    return env.get_template(_TPL[tpl_name]).render(**vars)


# ── TEMPLATES ───────────────────────────────────────────────────────

# SCHWA_TMP → Jinja template (see _TPL map)


# RULE_TMP → Jinja template (see _TPL map)


# PRACTICE_TMP → Jinja template (see _TPL map)


# RULE_FULL_TMP → Jinja template (see _TPL map)


# MORPH_TMP → Jinja template (see _TPL map)


# READER4_TMP → Jinja template (see _TPL map)


# ASSESS_TMP → Jinja template (see _TPL map)


# REVIEW_TMP → Jinja template (see _TPL map)


# ── HELPERS ─────────────────────────────────────────────────────────

def nt(n):
    t = {
        1:"Review Stage 3",2:"Schwa: The Lazy Vowel",3:"Say-to-Spell: Unlocking Schwa",
        4:"Schwa in Multi-Syllable Words",5:"Rule 31.2: O→/ŭ/",6:"Rule 31.3: AR/OR→/er/",
        7:"Schwa Mastery",8:"Rule 13: Drop Silent E",9:"Drop E Practice",
        10:"Rule 14: Double Consonant",11:"Double Consonant Practice",
        12:"Drop E & Double Review",13:"Mid-Stage 4 Assessment",
        14:"Rule 15: Y→I",15:"Y→I Practice",16:"Rule 16: Two I's",
        17:"Suffixing Rules Review",18:"Phonogram ti",19:"Phonogram ci",
        20:"Phonogram si",21:"Rule 17: Latin /sh/",22:"Rule 18: SH Placement",
        23:"Latin /sh/ Mastery",24:"Prefixes un- re-",25:"Prefixes in- dis-",
        26:"Prefixes pre- pro-",27:"Prefixes sub- inter-",28:"Suffixes -er -or",
        29:"Suffixes -tion -sion",30:"Suffixes -able -ible",
        31:"Suffixes -ment -ness",32:"Suffixes -ly -ful",
        33:"Suffixes -less -ous",34:"Rule 23: AL-",35:"Rule 24: -FUL",
        36:"Rule 19: Past Tense -ED",37:"Rule 21: Plural -S -ES",
        38:"Rule 22: 3rd Person -S -ES",39:"Rule 29: Z at Beginning",
        40:"Irregular Verbs",41:"Irregular Plurals",
        42:"Reader: Firefly",43:"Reader: Trains",
        44:"Morpheme Review: Prefixes",45:"Morpheme Review: Suffixes",
        46:"Mixed Spelling Stage 4",47:"All Stage 4 Review",
        48:"Stage 4 Mastery Check",
    }
    return t.get(n, f"Lesson {n}")

# ── CONTENT GENERATORS ──────────────────────────────────────────────

def gen_schwa2():
    return """## New Learning: Schwa — The Lazy Vowel Sound

### What Is Schwa?

Schwa is the most common vowel sound in English. It sounds like a tiny, lazy "uh" — /ə/. Your mouth is relaxed, your tongue is in the middle. It's the sound you make when you don't try very hard.

### Where Does Schwa Happen?

Schwa ONLY appears in **unstressed** syllables. That means the syllable where you DON'T put the emphasis.

| Word | Stressed Syllable | Unstressed Syllable (Schwa!) |
|------|-------------------|------------------------------|
| a·bout | BOUT (/bowt/) | a → /ə/ |
| sev·en | SEV (/sev/) | en → /ən/ |
| pen·cil | PEN (/pen/) | cil → /səl/ |
| but·ton | BUT (/but/) | ton → /tən/ |
| cir·cus | CIR (/ser/) | cus → /kəs/ |

### The Schwa Surprise

Here's the amazing (and tricky) thing: **ANY vowel can say schwa!** A, E, I, O, U — all of them can make the /ə/ sound in an unstressed syllable.

### Schwa Hunt

Which letter says schwa in each word?

| Word | Schwa Letter | Say Normally | Say-to-Spell |
|------|-------------|-------------|-------------|
| about | a | /ə-bout/ | /ā-bout/ |
| seven | e (second e) | /sev-ən/ | /sev-ĕn/ |
| pencil | i | /pen-səl/ | /pen-sĭl/ |
| button | o | /but-ən/ | /but-ŏn/ |
| circus | u (second u) | /ser-kəs/ | /ser-kŭs/ |

### Why Say-to-Spell Matters

If you try to spell 'about' by sound, you might write 'ubout' — because schwa can be spelled by ANY vowel. Say-to-spell lets you HEAR the true spelling: /ā-bout/ tells you it's an A.

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
| about | a (/ə/→/ā/ say-to-spell), b (/b/), ou (/ow/), t (/t/) | Rule 31: schwa in unstressed syllable | /ā-bout/ |
| seven | s (/s/), e (/ĕ/), v (/v/), e (/ə/→/ĕ/), n (/n/) | Rule 31 | /sev-ĕn/ |
| pencil | p (/p/), e (/ĕ/), n (/n/), c (/s/), i (/ə/→/ĭ/), l (/l/) | Rule 31 + Rule 1 (c=/s/) | /pen-sĭl/ |
| button | b (/b/), u (/ŭ/), t (/t/), t (/t/), o (/ə/→/ŏ/), n (/n/) | Rule 31 | /but-ŏn/ |

---

## Reading Practice

> about &nbsp; seven &nbsp; pencil &nbsp; button &nbsp; circus &nbsp; animal &nbsp; family &nbsp; banana

> I am about seven. My pencil has a button. The circus has animals. My family eats bananas."""

def gen_say_to_spell():
    return """## New Learning: Say-to-Spell — Your Secret Weapon

### The Problem

Schwa hides spelling information. When you say 'about' normally (/ə-bout/), you can't tell what vowel makes the /ə/ sound. Is it A? E? I? O? U? Any of them could work!

### The Solution: Say-to-Spell

**Say-to-Spell** means pronouncing the word with CLEAR vowel sounds — as if every syllable is stressed. This lets you HEAR the spelling.

### The Process (5 Steps)

1. **Say normally:** "about" → /ə-bout/
2. **Say-to-spell:** "ā-bout" (pronounce the A clearly)
3. **Segment the say-to-spell version:** /ā/ /b/ /ow/ /t/
4. **Write the word based on what you hear in the say-to-spell**
5. **Read normally:** /ə-bout/

### Say-to-Spell Examples

| Word | Normal | Say-to-Spell | Why? |
|------|--------|-------------|------|
| about | ə-bout | ā-bout | To hear the A |
| little | lit-əl | lit-tlē | To hear double T and final E |
| happen | hap-ən | hap-pĕn | To hear double P and E |
| animal | an-ə-məl | an-ĭ-măl | To hear I and A |
| family | fam-ə-lē | fam-ĭ-lē | To hear the I |
| chocolate | chok-lət | chok-ō-lāte | To hear O and A |
| every | ev-rē | ev-ĕr-ē | To hear the E-R-Y |
| different | dif-rənt | dif-fĕr-ĕnt | To hear double F, E-R, E-N-T |

### Important!

> **Say-to-Spell is NOT how you say the word in conversation.** It's a TOOL for spelling. You say it the 'wrong' way on purpose so you can spell it right.

---

## Spelling Analysis (Using Say-to-Spell)

| Word | Say-to-Spell | Phonograms | Rules | Normal |
|------|-------------|-----------|-------|--------|
| little | lit-tlē | l, i, t, t, l, e | Rule 12.4 (every syllable needs vowel) | /lit-əl/ |
| animal | an-ĭ-măl | a, n, i, m, a, l | Rule 31 (schwa) | /an-ə-məl/ |
| family | fam-ĭ-lē | f, a, m, i, l, y | Rule 7 (Y=/ē/ at end) | /fam-ə-lē/ |

---

## Reading Practice

> little &nbsp; animal &nbsp; family &nbsp; happen &nbsp; every &nbsp; different &nbsp; chocolate

> The little animal is in my family. Every chocolate is different. Things happen!"""

def gen_say_to_spell_check():
    return """1. What is Say-to-Spell? *(Pronouncing a word with clear vowel sounds to hear the spelling.)*
2. Why do we use it? *(Because schwa hides spelling information!)*
3. Say-to-spell 'family.' What do you hear? *(fam-ĭ-lē — the I and the Y become clear!)*"""

def gen_schwa_practice():
    body = """### Schwa in Multi-Syllable Words

Circle the vowel that says schwa in each word. Then use say-to-spell to hear the spelling.

| Word | Normal | Which Vowel Says Schwa? | Say-to-Spell |
|------|--------|------------------------|-------------|
| about | ə-bout | a | ā-bout |
| away | ə-wā | a | ā-way |
| open | ō-pən | e (second e) | ō-pĕn |
| seven | sev-ən | e (second e) | sev-ĕn |
| pencil | pen-səl | i | pen-sĭl |
| happen | hap-ən | e | hap-pĕn |
| button | but-ən | o | but-ŏn |
| circus | ser-kəs | u (second u) | ser-kŭs |
| banana | bə-nan-ə | a (first), a (last) | bă-năn-ă |
| animal | an-ə-məl | i, a | an-ĭ-măl |

### Practice Words

Write each word. Say the say-to-spell version aloud as you write.

| Word | Say-to-Spell | Write |
|------|-------------|-------|
| about | ā-bout | |
| seven | sev-ĕn | |
| pencil | pen-sĭl | |
| button | but-ŏn | |
| animal | an-ĭ-măl | |
| family | fam-ĭ-lē | |
| different | dif-fĕr-ĕnt | |
| memory | mem-ō-rē | |"""

    sa = """| about | a→/ā/ STSp, b, ou, t | Rule 31 | ā-bout |
| seven | s, e (/ĕ/), v, e→/ĕ/ STSp, n | Rule 31 | sev-ĕn |
| animal | a (/ă/), n, i→/ĭ/ STSp, m, a→/ă/ STSp, l | Rule 31 | an-ĭ-măl |
| family | f, a (/ă/), m, i→/ĭ/ STSp, l, y (/ē/) | Rule 7 + 31 | fam-ĭ-lē |"""

    return render("schwa", n=3, title="Schwa in Multi-Syllable Words", typ="schwa-practice",
        focus="all vowels — any can be schwa!", body=body, nn=4, ntitle=nt(4),
        check="1. What sound does schwa make? *(A lazy /ə/ — like 'uh')*\n2. How do you know which letter spells the schwa? *(Use say-to-spell!)*\n3. Spell 'animal' using say-to-spell.",
        home="Find 5 schwa words in a book. Write the say-to-spell version for each.")

def gen_rule31_2():
    return """## New Learning: Rule 31.2

### The Rule

> **O** may say /ŭ/ when it comes right before a **W**, **TH**, **M**, **N**, or **V**.

### Why?

The sound /ŭ/ (short U) before certain consonants can be spelled with O instead of U. This happens most often in words like 'son,' 'love,' 'won,' 'mother,' 'other.'

### Words with O→/ŭ/

| Word | O before... | Sound | Say-to-Spell |
|------|------------|-------|-------------|
| son | N | /ŭ/ | /sŏn/ |
| won | N | /ŭ/ | /wŏn/ |
| love | V | /ŭ/ | /lŏv/ |
| above | V | /ŭ/ | /ă-bŏv/ |
| mother | TH | /ŭ/ | /mŏth-er/ |
| brother | TH | /ŭ/ | /brŏth-er/ |
| other | TH | /ŭ/ | /ŏth-er/ |
| monkey | N | /ŭ/ | /mŏn-kē/ |
| money | N | /ŭ/ | /mŏn-ē/ |
| glove | V | /ŭ/ | /glŏv/ |
| cover | V | /ŭ/ | /kŏv-er/ |
| done | N | /ŭ/ | /dŏn/ |
| none | N | /ŭ/ | /nŏn/ |
| come | M | /ŭ/ | /kŏm/ |
| some | M | /ŭ/ | /sŏm/ |

### Not Every O Before These Letters Says /ŭ/

Remember: rules describe patterns, not absolute laws. O before TH/M/N/V OFTEN says /ŭ/, but not always. 'Phone' — O before N, but says /ō/.

---

## Spelling Analysis

| Word | Phonograms | Rules | Say-to-Spell |
|------|-----------|-------|-------------|
| love | l (/l/), o (/ŭ/), v (/v/), e — SE (12.2) | 31.2 + 12.2 | /lŏv/ |
| mother | m (/m/), o (/ŭ/), th (/th/), er (/er/) | 31.2 | /mŏth-er/ |
| son | s (/s/), o (/ŭ/), n (/n/) | 31.2 | /sŏn/ |
| come | c (/k/), o (/ŭ/), m (/m/), e — SE (12.9) | 31.2 + 12.9 | /kŏm/ |

---

## Reading Practice

> love &nbsp; mother &nbsp; son &nbsp; come &nbsp; some &nbsp; done &nbsp; above &nbsp; other &nbsp; cover &nbsp; money

> My mother and brother love me. Come here, son. Some money is above the cover."""

def gen_rule31_3():
    return """## New Learning: Rule 31.3

### The Rule

> **AR** and **OR** may say /er/ in an unstressed syllable.

### Why?

When AR and OR are in an unstressed syllable, they often reduce to /er/ — the lazy R-controlled sound. Think of the word 'dollar' — the AR at the end is unstressed, so it sounds like 'doll-er.'

### Words with AR→/er/

| Word | AR says /er/ in... | Say-to-Spell |
|------|-------------------|-------------|
| dollar | doll·ar (ar unstressed) | /dŏl-lär/ |
| collar | col·lar | /kŏl-lär/ |
| sugar | sug·ar | /shüg-är/ |
| popular | pop·u·lar | /pop-ū-lär/ |
| regular | reg·u·lar | /reg-ū-lär/ |
| similar | sim·i·lar | /sim-ĭ-lär/ |

### Words with OR→/er/

| Word | OR says /er/ in... | Say-to-Spell |
|------|-------------------|-------------|
| doctor | doc·tor (or unstressed) | /dŏk-tor/ |
| actor | ac·tor | /ăk-tor/ |
| color | col·or | /kŏl-or/ |
| author | au·thor | /ä-thor/ |
| sailor | sail·or | /sāl-or/ |
| mirror | mir·ror | /mir-or/ |

### Notice the Pattern

Most of these words end in -ar or -or, and the ending syllable is unstressed. This is extremely common in English!

---

## Spelling Analysis

| Word | Phonograms | Rules | Say-to-Spell |
|------|-----------|-------|-------------|
| dollar | d (/d/), o (/ŏ/), l (/l/), l (/l/), ar (/er/) | 31.3 | /dŏl-lär/ |
| doctor | d (/d/), o (/ŏ/), c (/k/), t (/t/), or (/er/) | 31.3 | /dŏk-tor/ |
| color | c (/k/), o (/ŭ/), l (/l/), or (/er/) | 31.2 + 31.3 | /kŭl-or/ |
| sugar | s (/sh/), u (/ü/), g (/g/), ar (/er/) | 31.3 | /shüg-är/ |

---

## Reading Practice

> dollar &nbsp; doctor &nbsp; color &nbsp; sugar &nbsp; actor &nbsp; author &nbsp; collar &nbsp; popular &nbsp; mirror

> The doctor has a dollar. What color is the sugar? The actor and author are popular."""

def gen_schwa_mastery():
    body = """### Mixed Schwa Practice

For each word: (1) Say it normally, (2) identify the schwa syllable, (3) say-to-spell, (4) write it.

| Word | Normal | Schwa Syllable | Say-to-Spell | Write |
|------|--------|---------------|-------------|-------|
| about | ə-bout | a | ā-bout | |
| seven | sev-ən | en | sev-ĕn | |
| pencil | pen-səl | cil | pen-sĭl | |
| button | but-ən | ton | but-ŏn | |
| animal | an-ə-məl | i, a | an-ĭ-măl | |
| love | lŭv | (o→/ŭ/ — 31.2) | lŏv | |
| mother | mŭth-er | moth (31.2) | mŏth-er | |
| dollar | dol-ər | lar (31.3) | dol-lär | |
| doctor | dok-tər | tor (31.3) | dok-tor | |
| family | fam-ə-lē | i | fam-ĭ-lē | |
| chocolate | chok-lət | o, a | chok-ō-lāte | |
| different | dif-rənt | fer, ent | dif-fĕr-ĕnt | |
| memory | mem-ə-rē | o | mem-ō-rē | |
| banana | bə-nan-ə | first a, last a | bă-năn-ă | |"""

    sa = """| about | a→/ā/ STSp, b, ou, t | 31 | ā-bout |
| chocolate | ch, o→/ō/ STSp, c, o→/ā/ STSp, l, a→/ā/ STSp, t, e — SE (12.9) | 31 + 12.9 | chok-ō-lāte |
| different | d, i (/ĭ/), f, f, e→/ĕ/ STSp, r, e→/ĕ/ STSp, n, t | 31 | dif-fĕr-ĕnt |
| memory | m, e (/ĕ/), m, o→/ō/ STSp, r, y (/ē/) | 31 + Rule 7 | mem-ō-rē |"""

    return render("schwa", n=6, title="Schwa Mastery: Mixed Practice", typ="schwa-practice",
        focus="all 75 phonograms", body=body, nn=7, ntitle=nt(7),
        check="1. What three rules have we learned about schwa? *(31.1: any vowel in unstressed syllable. 31.2: O→/ŭ/ before W/TH/M/N/V. 31.3: AR/OR→/er/ unstressed.)*\n2. Which word was hardest to spell? Why?\n3. Spell 'chocolate' using say-to-spell.",
        home="Pick your 3 hardest schwa words. Write each one 5 times with say-to-spell.")

def gen_rule13():
    return render("rule-full", n=7, rn=13, name="Drop the Silent E for a Vowel Suffix",
        statement="When adding a vowel suffix, drop the silent final E.",
        why="When you add a suffix that starts with a vowel (like -ing, -ed, -er), the silent E has done its job. The vowel suffix now provides a vowel for that syllable. 'Make' + 'ing' = 'making' — drop the E, add -ing. The A still says /ā/ because the syllable is open: ma·king.",
        examples="make→making, hope→hoping, drive→driving, use→using, bake→baking, write→writing, smile→smiling, rake→raking",
        spot="| make + ing | Drop E → making |\n| hope + ed | Drop E → hoped |\n| drive + er | Drop E → driver |\n| use + ing | Drop E → using |\n| bake + er | Drop E → baker |\n| write + ing | Drop E → writing |\n| smile + ing | Drop E → smiling |\n| rake + ed | Drop E → raked |",
        words="| making | m (/m/), a (/ā/), k (/k/), i (/ĭ/), ng (/ng/) | Rule 13 + Rule 4 (open syllable) | /māk-ing/ |\n| hoping | h (/h/), o (/ō/), p (/p/), i (/ĭ/), ng (/ng/) | Rule 13 + Rule 4 | /hōp-ing/ |\n| driving | d (/d/), r (/r/), i (/ī/), v (/v/), i (/ĭ/), ng (/ng/) | Rule 13 + Rule 4 | /drīv-ing/ |\n| using | u (/ū/), s (/s/), i (/ĭ/), ng (/ng/) | Rule 13 + Rule 4 | /ūz-ing/ |",
        reading="making &nbsp; hoping &nbsp; driving &nbsp; using &nbsp; baking &nbsp; writing &nbsp; smiling &nbsp; raking\n\nThe baker is making a cake. I am hoping to drive. She is writing and smiling.",
        practice_focus="Rule 13: Drop Silent E before vowel suffix",
        practice_body="Add -ing and -ed to each word. Remember: drop the silent E!\n\n| Base Word | + -ing | + -ed |\n|-----------|--------|-------|\n| make | making | made (special!) |\n| hope | hoping | hoped |\n| drive | driving | drove (special!) |\n| use | using | used |\n| bake | baking | baked |\n| write | writing | wrote (special!) |\n| smile | smiling | smiled |\n| rake | raking | raked |\n| ride | riding | rode (special!) |\n| take | taking | took (special!) |\n\n> **Watch out!** Some past-tense forms are irregular (made, drove, wrote). We'll learn those later.\n\n### When NOT to Drop the E\n\nKeep the E when adding a CONSONANT suffix (one that starts with a consonant).\n\n| Base Word | + -ful (consonant suffix) | Keep E? |\n|-----------|--------------------------|---------|\n| hope | hopeful | YES — -ful starts with F (consonant) |\n| care | careful | YES |\n| use | useful | YES |\n| peace | peaceful | YES |\n\n### But what about truly, duly, arguing?\n\nWhen the E is needed to keep C or G soft, don't drop it!\n- change → changeable (keep E so G still says /j/)\n- notice → noticeable (keep E so C still says /s/)",
        practice_sa="| making | make → mak + ing | Drop E (Rule 13) | /māk-ing/ |\n| hoping | hope → hop + ing | Drop E (Rule 13) | /hōp-ing/ |\n| careful | care + ful | Keep E (consonant suffix) | /kār-fǕl/ |\n| changeable | change + able | Keep E (Rule 2: G→/j/) | /chānj-ā-bl/ |",
        practice_reading="making &nbsp; hoping &nbsp; driving &nbsp; careful &nbsp; useful &nbsp; changeable\n\nI am making a cake and hoping it tastes good. Be careful and useful!",
        q3="What happens if you DON'T drop the E? Try 'makeing' — does it look right?",
        practice_q1="When do you drop the silent E? *(Before a vowel suffix.)*)",
        practice_q2="When do you KEEP the silent E? *(Before a consonant suffix, or to keep C/G soft.)*)",
        practice_q3="Spell 'making' and 'hoping' from dictation.",
        nn=8, ntitle=nt(8),
        home="Write 5 words that drop the silent E before -ing. Draw a line through the E and write the new word. Then find 3 words where the E is KEPT (consonant suffix).")

def gen_rule14():
    return render("rule-full", n=8, rn=14, name="Double the Consonant for a Vowel Suffix",
        statement="When adding a vowel suffix, double the final consonant if the word is one syllable, has one vowel, and ends in one consonant (1-1-1 rule).",
        why="This is the '1-1-1 Rule.' If a word has 1 syllable, 1 vowel, and ends in 1 consonant, double that consonant before adding a vowel suffix. Why? To keep the vowel short! 'Hop' + 'ing' = 'hopping' (short O). Without the double P, it would be 'hoping' (long O — from hope). The extra consonant closes the syllable and keeps the vowel short.",
        examples="run→running, hop→hopping, swim→swimming, sit→sitting, get→getting, stop→stopping, cut→cutting, big→bigger",
        spot="| run + ing | 1 syll, 1 vowel (u), 1 final consonant (n) → running |\n| hop + ing | 1 syll, 1 vowel (o), 1 final consonant (p) → hopping |\n| swim + ing | 1 syll, 1 vowel (i), 1 final consonant (m) → swimming |\n| open + ing | 2 syllables → NO double → opening |\n| sleep + ing | 2 vowels (ee) → NO double → sleeping |\n| jump + ing | 2 final consonants (mp) → NO double → jumping |",
        words="| running | r (/r/), u (/ŭ/), n (/n/), n (/n/), i (/ĭ/), ng (/ng/) | Rule 14: 1-1-1 → double N | /rǕn-ing/ |\n| hopping | h (/h/), o (/ō/), p (/p/), p (/p/), i (/ĭ/), ng (/ng/) | Rule 14: double P keeps O short | /hōp-ing/ |\n| swimming | s (/s/), w (/w/), i (/ĭ/), m (/m/), m (/m/), i (/ĭ/), ng (/ng/) | Rule 14 | /swĭm-ing/ |",
        reading="running &nbsp; hopping &nbsp; swimming &nbsp; sitting &nbsp; getting &nbsp; stopping &nbsp; cutting &nbsp; bigger\n\nThe dog is running and hopping. I am swimming and getting tired. Stop cutting the paper!",
        practice_focus="Rule 14: 1-1-1 Rule",
        practice_body="For each word, ask: 1 syllable? 1 vowel? End in 1 consonant? If YES to all three → double the final consonant.\n\n| Base Word | 1 Syllable? | 1 Vowel? | 1 Final Consonant? | Double? | + -ing |\n|-----------|------------|----------|-------------------|---------|--------|\n| run | YES | YES (u) | YES (n) | YES | running |\n| hop | YES | YES (o) | YES (p) | YES | hopping |\n| swim | YES | YES (i) | YES (m) | YES | swimming |\n| sit | YES | YES (i) | YES (t) | YES | sitting |\n| get | YES | YES (e) | YES (t) | YES | getting |\n| cut | YES | YES (u) | YES (t) | YES | cutting |\n| open | NO (2 syll) | — | — | NO | opening |\n| sleep | YES | NO (ee = 2 letters) | — | NO | sleeping |\n| jump | YES | YES (u) | NO (mp = 2) | NO | jumping |\n| read | YES | NO (ea = 2) | — | NO | reading |\n| rain | YES | NO (ai = 2) | — | NO | raining |\n| help | YES | YES (e) | NO (lp = 2) | NO | helping |\n\nWrite the -ing form for each:\n\n| hop → hopping | run → ______ | sit → ______ | get → ______ |\n| cut → ______ | stop → ______ | swim → ______ | plan → ______ |\n| sleep → ______ | jump → ______ | read → ______ | open → ______ |",
        practice_sa="| running | run + n + ing | Rule 14: 1-1-1 | /rǕn-ing/ |\n| hopping | hop + p + ing | Rule 14: keeps O short | /hōp-ing/ |\n| opening | open + ing | Rule 4: open syllable | /ō-pen-ing/ |\n| sleeping | sleep + ing | No double (two vowels) | /slēp-ing/ |",
        practice_reading="running &nbsp; hopping &nbsp; swimming &nbsp; opening &nbsp; sleeping &nbsp; jumping\n\nI am running to the pool and swimming. Mom is opening the door. The cat is sleeping and jumping.",
        q3="Why don't we double the P in 'sleeping'? *(Two vowels — EE — not one. The 1-1-1 rule doesn't apply.)*",
        practice_q1="What three things must be true to double the consonant? *(1 syllable, 1 vowel, 1 final consonant.)*)",
        practice_q2="Why don't we double in 'sleeping'? *(EE is two vowel letters — not one.)*)",
        practice_q3="Spell 'running' and 'hopping' from dictation.",
        nn=9, ntitle=nt(9),
        home="Find 3 words with double consonants before -ing. Write the base word and the 1-1-1 check. Then find 3 -ing words that do NOT double (and explain why).")

def gen_rule14_review():
    body = """## Part 1: Drop E or Double?

For each word, decide: drop the silent E (Rule 13) or double the consonant (Rule 14)?

| Base Word | + ing | Rule | Why? |
|-----------|-------|------|------|
| make | making | 13 | Silent E before vowel suffix |
| hop | hopping | 14 | 1-1-1 → double |
| drive | driving | 13 | Silent E |
| run | running | 14 | 1-1-1 |
| use | using | 13 | Silent E |
| sit | sitting | 14 | 1-1-1 |
| hope | hoping | 13 | Silent E |
| swim | swimming | 14 | 1-1-1 |

## Part 2: Neither?

Some words need neither rule:

| Base Word | + ing | Why Neither? |
|-----------|-------|-------------|
| sleep | sleeping | Two vowels (ee) |
| jump | jumping | Two final consonants (mp) |
| open | opening | Two syllables |
| read | reading | Two vowels (ea) |

## Part 3: Mix

| make → making | hope → ______ | run → ______ |
| drive → ______ | sit → ______ | use → ______ |
| sleep → ______ | open → ______ | swim → ______ |
| jump → ______ | get → ______ | read → ______ |"""

    return render("review", n=11, title="Drop E and Double Consonant Review", nn=12, ntitle=nt(12),
        g1="Part 1: Drop the E (Rule 13)", gb1="Write the -ing form by dropping silent E: make→making, drive→driving, use→using, hope→hoping, bake→baking, write→writing, smile→smiling.",
        g2="Part 2: Double the Consonant (Rule 14)", gb2="Write the -ing form by doubling: run→running, hop→hopping, swim→swimming, sit→sitting, get→getting, cut→cutting, stop→stopping.",
        g3="Part 3: Neither!", gb3="Explain why these DON'T change: sleeping (2 vowels), jumping (2 final consonants), opening (2 syllables), reading (2 vowels), helping (2 final consonants).",
        challenge="making, hoping, running, hopping, swimming, sleeping, opening, driving, sitting, using",
        home="Review Rules 13 and 14 flashcards!")

def gen_rule15():
    return render("rule-full", n=9, rn=15, name="Y Changes to I Before a Suffix",
        statement="When adding a suffix to a word ending in Y (with a consonant before it), change the Y to I.",
        why="Y is a tricky letter. When a word ends in Y, we need to ask: what sound does the Y make? If Y is the only vowel in the word AND says /ĭ/ or /ē/ (long I or long E), change it to I before adding a suffix. 'Cry' + 'ed' = 'cried' (the Y says /ī/, change to I). 'Happy' + 'ness' = 'happiness' (the Y says /ē/, change to I). But 'boy' + 'hood' = 'boyhood' (the Y says /oi/, keep as Y).",
        examples="cry→cried, try→tried, happy→happiness, easy→easier, carry→carried, study→studied, fly→flies",
        spot="| cry + ed | Y says /ī/, change → cried |\n| happy + ness | Y says /ē/, change → happiness |\n| try + ing | Y says /ī/, change → trying |\n| boy + hood | Y says /oi/, KEEP → boyhood |\n| play + ed | Y says /ā/, KEEP → played |\n| key + s | Y says /ē/, KEEP → keys (Y is the only vowel so... wait, see Rule 16.) |",
        words="| cried | c (/k/), r (/r/), i (/ī/), e (/ē/), d (/d/) | Rule 15: Y→I | /krīd/ |\n| tried | t (/t/), r (/r/), i (/ī/), e (/ē/), d (/d/) | Rule 15 | /trīd/ |\n| happiness | h (/h/), a (/ā/), p (/p/), i (/ĭ/), n (/n/), e (/ē/), s (/s/), s (/s/) | Rule 15: Y→I + -ness | /hāp-ĭ-nēs/ |\n| carried | c (/k/), a (/ā/), r (/r/), r (/r/), i (/ĭ/), e (/ē/), d (/d/) | Rule 15 | /kār-ĭd/ |",
        reading="cried &nbsp; tried &nbsp; studied &nbsp; carried &nbsp; worried &nbsp; hurried &nbsp; spied &nbsp; replied\n\nThe baby cried and tried to sleep. I studied hard and carried the heavy bag. She worried and hurried to class.",
        practice_focus="Rule 15: Y Changes to I",
        practice_body="For each word, ask: does Y say /i/ or /e/? Is there a consonant before the Y? If YES to both → change Y to I before adding the suffix.\n\n| Base Word | Y Sound? | Consonant Before Y? | + -ed | + -ing | + -er | + -est |\n|-----------|---------|--------------------|----|--------|-------|--------|\n| cry | /ī/ | YES (r) | cried | crying | crier | — |\n| try | /ī/ | YES (r) | tried | trying | trier | — |\n| happy | /ē/ | YES (p) | happied(?) | — | happier | happiest |\n| easy | /ē/ | YES (s) | — | — | easier | easiest |\n| carry | /ē/ | YES (r) | carried | carrying | carrier | — |\n| study | /ē/ | YES (d) | studied | studying | — | — |\n| fly | /ī/ | YES (l) | flied(?) | flying | flier | — |\n| boy | /oi/ | NO (vowel before) | boyed(?) | — | — | — |\n| play | /ā/ | NO (vowel before) | played | playing | player | — |\n| key | /ē/ | NO (vowel before) | — | — | — | — |\n\n> **Watch out!** Words like 'flied' and 'happied' exist but are unusual — most English speakers just add the suffix without Y→I when the result is awkward. And remember Rule 16: two I's can't be next to each other, so 'cry' + 'ing' = 'crying' (just add -ing), but 'study' + 'ing' = 'studying' (Y→I, then add -ing).",
        practice_sa="| cried | cr + i + ed | Rule 15: Y→I | /krīd/ |\n| trying | tr + i + ing | Rule 15 + Rule 16 (no II) | /trī-ĭng/ |\n| happiness | happi + ness | Rule 15: Y→I + -ness | /hāp-ĭ-nēs/ |\n| carried | carri + ed | Rule 15: Y→I | /kār-ĭd/ |\n| boyhood | boy + hood | No change (Y=/oi/) | /boi-hǝd/ |",
        practice_reading="cried &nbsp; tried &nbsp; worried &nbsp; hurried &nbsp; happiness &nbsp; easier &nbsp; carried &nbsp; studying\n\nI cried because I tried so hard. The happiness was real. She worried and hurried to her studying.",
        q3="Why don't we change Y to I in 'boyhood'? *(The Y says /oi/ — it's a vowel team with O. The Y→I rule only applies when Y is the ONLY vowel.)*",
        practice_q1="When do we change Y to I? *(When Y is the only vowel, says /i/ or /e/, and a consonant comes before it.)*)",
        practice_q2="Why don't we double-I in 'crying'? *(Rule 16: two I's cannot be adjacent — just add -ing.)*)",
        practice_q3="Spell 'cried', 'happiness', and 'tried' from dictation.",
        nn=10, ntitle=nt(10),
        home="Find 5 -ed, -ing, -er, or -ness words where the Y changed to I. Write the base word and the new word. Then find 2 words where Y was KEPT (vowel before it).")

def gen_rule16():
    return render("rule", n=11, rn=16, name="Two I's Cannot Be Adjacent",
        statement="Two I's may not be next to each other in an English word.",
        why="English spelling avoids two I's side by side. This is why we don't change Y to I before -ing: 'cry' + 'ing' = 'crying' (not 'criing'). It's also why words like 'skiing' look odd — they're borrowed from other languages and break the rule!",
        examples="cry→crying (NOT criing), try→trying, fly→flying, study→studying, carry→carrying, marry→marrying",
        spot="| cry + ing | crying (keep Y — two I's would be 'criing') |\n| try + ing | trying |\n| fly + ing | flying |\n| study + ing | studying |\n| carry + ing | carrying |",
        words="| crying | c (/k/), r (/r/), y (/ī/), i (/ĭ/), ng (/ng/) | Rule 16: keep Y before -ing | /krī-ing/ |\n| flying | f (/f/), l (/l/), y (/ī/), i (/ĭ/), ng (/ng/) | Rule 16 | /flī-ing/ |\n| studying | s (/s/), t (/t/), u (/ŭ/), d (/d/), y (/ē/), i (/ĭ/), ng (/ng/) | Rule 16 | /stŭd-ē-ing/ |",
        reading="crying &nbsp; flying &nbsp; studying &nbsp; trying &nbsp; carrying &nbsp; marrying\n\nThe baby is crying. A bird is flying. I am studying my rules. Keep trying!",
        nn=12, ntitle=nt(11), q3="Why does 'skiing' look so strange? *(It's borrowed from Norwegian — it breaks the English 'No Two I's' rule!)*",
        home="Write the -ing forms of: cry, try, fly, study, carry. Explain why the Y stays.")

def gen_suffix_review_17():
    return render("review", n=12, title="All Suffixing Rules Review", nn=10, ntitle=nt(12),
        g1="Rule 13: Drop Silent E", gb1="Write the -ing form: make→____, drive→____, use→____, hope→____, bake→____.",
        g2="Rule 14: Double Consonant", gb2="Write the -ing form: run→____, hop→____, swim→____, sit→____, get→____. Write opening, sleeping, jumping — why NO double?",
        g3="Rules 15 & 16: Y→I and No Two I's", gb3="Write: cry→cr____ (es), baby→bab____ (es), happy→happ____ (ness). Write crying, trying, flying — why keep Y?",
        challenge="making, running, hopping, babies, happiness, crying, studying, carried, opening, sleeping",
        home="Review all 4 suffixing rule flashcards! (13, 14, 15, 16)")

def gen_ti():
    return f"""# Lesson 18: Phonogram ti

**Stage 4** · Lesson 18 · phonogram-intro

---

## Warm-Up: Phonogram Flash Review

> Flash all 75 phonograms.

---

## New Learning: The Phonogram **ti**

<div class="phonogram">ti</div>

**ti** says /sh/ in Latin-based words.

> **Rule 17:** TI, CI, and SI spell /sh/ in words of Latin origin. TI is the most common.

| Usage | Example Words |
|-------|--------------|
| /sh/ in -tion words | nation, action, station, fraction |
| /sh/ in other Latin words | patient, partial, initial, martial |

### Where Does TI Say /sh/?

TI says /sh/ when followed by another vowel (most often -tion). The T and I work together to make one sound: /sh/.

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
| nation | n (/n/), a (/ā/), ti (/sh/), o (/ə/→/ŏ/ STSp), n (/n/) | Rule 17: Latin TI=/sh/ | /nā-shŏn/ |
| action | a (/ă/), c (/k/), ti (/sh/), o (/ə/→/ŏ/ STSp), n (/n/) | Rule 17 | /ăk-shŏn/ |
| station | s (/s/), t (/t/), a (/ā/), ti (/sh/), o→/ŏ/ STSp, n | Rule 17 + 31 | /stā-shŏn/ |
| patient | p (/p/), a (/ā/), ti (/sh/), e (/ĕ/), n (/n/), t (/t/) | Rule 17 | /pā-shĕnt/ |

---

## Reading

> nation &nbsp; action &nbsp; station &nbsp; patient &nbsp; fraction &nbsp; partial &nbsp; initial

> The nation took action. The train station is near. Be patient with fractions!

---

## Quick Check

1. What sound does TI make? *(/sh/ — in Latin words)*
2. When does TI say /sh/? *(When followed by a vowel, usually -tion)*
3. Spell 'nation' and 'action' from dictation.

---

**Next lesson:** Lesson 19: Phonogram ci

---

*Practice at home: Find 5 words with -tion in a book!*
"""

def gen_ci():
    return f"""# Lesson 19: Phonogram ci

**Stage 4** · Lesson 19 · phonogram-intro

---

## Warm-Up: Phonogram Flash Review

> Flash all 75 phonograms. Include ti from yesterday!

---

## New Learning: The Phonogram **ci**

<div class="phonogram">ci</div>

**ci** says /sh/ in Latin-based words.

> **Rule 17:** CI is the second most common Latin /sh/ spelling. It usually appears in the middle of words.

| Usage | Example Words |
|-------|--------------|
| /sh/ before vowels | special, social, gracious, precious |
| /sh/ in -cian words | musician, magician, physician |

### CI vs. TI

Both say /sh/ in Latin words! TI is more common overall, especially in -tion. CI appears in -cial, -cian, and -cious words.

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
| special | s (/s/), p (/p/), e (/ĕ/), ci (/sh/), a (/ă/→/ə/), l (/l/) | Rule 17 + 31 | /spe-shăl/ |
| social | s (/s/), o (/ō/), ci (/sh/), a→/ă/ STSp, l | Rule 17 + 31 | /sō-shăl/ |
| musician | m (/m/), u (/ü/), s (/s/), i (/ĭ/), ci (/sh/), a→/ă/ STSp, n | Rule 17 | /mü-zĭ-shăn/ |

---

## Reading

> special &nbsp; social &nbsp; musician &nbsp; precious &nbsp; delicious &nbsp; gracious

> This is a special song. The musician plays a social show. The food is delicious and precious!

---

## Quick Check

1. What sound does CI make? *(/sh/ in Latin words)*
2. Where does CI usually appear? *(In the middle — -cial, -cian, -cious)*
3. Spell 'special' and 'social' from dictation.

---

**Next lesson:** Lesson 20: Phonogram si

---

*Practice at home: Find CI words in a book. How many end in -cial?*
"""

def gen_si():
    return f"""# Lesson 20: Phonogram si

**Stage 4** · Lesson 20 · phonogram-intro

---

## Warm-Up: Phonogram Flash Review

> Flash all 75 phonograms. Include ti and ci!

---

## New Learning: The Phonogram **si**

<div class="phonogram">si</div>

**si** says /sh/ or /zh/ in Latin-based words.

> **Rule 17:** SI is the least common Latin /sh/ spelling. It can also say /zh/ (as in 'vision').

| Sound | Example Words |
|-------|--------------|
| /sh/ | session, mission, discussion, passion |
| /zh/ | vision, division, television, occasion |

### The /zh/ Sound

/zh/ is the voiced version of /sh/. It's the sound in 'treasure' and 'vision.' SI is one of the only ways to spell this sound!

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
| session | s (/s/), e (/ĕ/), s (/s/), si (/sh/), o→/ŏ/ STSp, n | Rule 17 | /se-shŏn/ |
| mission | m (/m/), i (/ĭ/), s (/s/), si (/sh/), o→/ŏ/ STSp, n | Rule 17 | /mi-shŏn/ |
| vision | v (/v/), i (/ĭ/), si (/zh/), o→/ŏ/ STSp, n | Rule 17 | /vi-zhŏn/ |
| television | t (/t/), e (/ĕ/), l (/l/), e (/ĕ/), v (/v/), i (/ĭ/), si (/zh/), o→/ŏ/ STSp, n | Rule 17 | /tel-ĕ-vi-zhŏn/ |

---

## Reading

> session &nbsp; mission &nbsp; vision &nbsp; television &nbsp; discussion &nbsp; division

> The session is a mission. My vision is good. Watch television after the discussion.

---

## Quick Check

1. What TWO sounds can SI make? *(/sh/ and /zh/)*
2. Give a word where SI says /zh/. *(vision, television, division)*
3. Spell 'mission' and 'vision' from dictation.

---

**Next lesson:** Lesson 21: Rule 17

---

*Practice at home: Find SI words in a book. Does SI say /sh/ or /zh/?*
"""

def gen_rule17():
    return render("rule", n=17, rn=17, name="Latin /sh/ — TI, CI, SI",
        statement="**TI**, **CI**, and **SI** spell /sh/ in words of Latin origin. TI is most common; SI can also say /zh/.",
        why="English borrowed thousands of words from Latin. Latin had a sound like /sh/ that was spelled differently depending on the root word. English kept these spellings! -tion is the most common (nation, action), -cial comes next (special, social), and -sion is least common but can say /zh/ (vision).",
        examples="TI: nation, action, station, fraction, patient, partial\nCI: special, social, musician, precious, delicious\nSI: mission, session, vision (/zh/), television (/zh/)",
        spot="| nation | -tion → TI = /sh/ |\n| special | -cial → CI = /sh/ |\n| mission | -sion → SI = /sh/ |\n| vision | -sion → SI = /zh/ |\n| musician | -cian → CI = /sh/ |",
        words="| nation | n, a (/ā/), ti (/sh/), o→/ŏ/ STSp, n | Rule 17 | /nā-shŏn/ |\n| special | s, p, e (/ĕ/), ci (/sh/), a→/ă/ STSp, l | Rule 17 + 31 | /spe-shăl/ |\n| vision | v, i (/ĭ/), si (/zh/), o→/ŏ/ STSp, n | Rule 17 | /vi-zhŏn/ |",
        reading="nation &nbsp; special &nbsp; vision &nbsp; action &nbsp; musician &nbsp; mission\n\nThe nation has a special vision. The musician's mission is action!",
        nn=19, ntitle=nt(18), q3="Which Latin /sh/ spelling is the most common? *(TI — especially in -tion words.)*",
        home="Sort these into TI, CI, or SI: nation, special, mission, action, musician, vision, fraction, session.")

def gen_rule18():
    return render("rule", n=18, rn=18, name="SH Placement",
        statement="**SH** is used at the beginning or end of a base word, at the end of a syllable, but NOT at the beginning of a syllable after the first one.",
        why="SH is the 'regular English' way to spell /sh/. TI/CI/SI are the 'Latin' way. SH appears in everyday English words: ship, fish, wishing. Latin /sh/ (TI/CI/SI) appears in more formal or academic words: nation, special, mission.",
        examples="SH at start: ship, she, show, shoe\nSH at end: fish, wish, push, crash\nSH in middle (end of syllable): dish·es, push·ing, wash·ing\nLatin /sh/ (mid-word after first syllable): nation, special, session",
        spot="| ship | SH at beginning ✓ |\n| fish | SH at end ✓ |\n| dishes | SH at end of first syllable ✓ |\n| nation | TI = /sh/ (Latin, after first syllable) ✓ |\n| nashun | NOT English — use 'nation' ✗ |",
        words="| dishes | d (/d/), i (/ĭ/), sh (/sh/), e (/ə/→/ĕ/ STSp), s (/z/) | Rule 18 + 31 | /di-shĕz/ |\n| wishing | w (/w/), i (/ĭ/), sh (/sh/), i (/ĭ/), ng (/ng/) | Rule 18 | /wi-shĭng/ |\n| nation | n, a (/ā/), ti (/sh/), o→/ŏ/ STSp, n | Rule 17 + 31 | /nā-shŏn/ |",
        reading="ship &nbsp; fish &nbsp; dishes &nbsp; wishing &nbsp; nation &nbsp; special\n\nThe ship had fish and dishes. I am wishing for a special nation!",
        nn=20, ntitle=nt(19), q3="When do you use SH vs. TI/CI/SI for /sh/? *(SH for everyday words and at start/end. TI/CI/SI for Latin words in the middle.)*",
        home="Find 5 words with SH and 3 with Latin /sh/. Compare them!")

def gen_latin_mastery():
    body = """### TI, CI, or SI?

Write the correct Latin /sh/ spelling for each word:

| Word Fragment | Complete the Word | Which Spelling? |
|---------------|-------------------|----------------|
| na____on | nation | TI |
| spe____al | special | CI |
| mis____on | mission | SI |
| ac____on | action | TI |
| mu____ian | musician | CI |
| vi____on | vision | SI (/zh/!) |
| frac____on | fraction | TI |
| deli____ous | delicious | CI |
| ses____on | session | SI |
| sta____on | station | TI |

### SH or Latin?

| Word | /sh/ Spelling | SH or Latin? |
|------|--------------|-------------|
| ship | sh | SH |
| nation | ti | Latin |
| fish | sh | SH |
| special | ci | Latin |
| dishes | sh | SH |
| mission | si | Latin |
| push | sh | SH |
| fraction | ti | Latin |

### Mixed Spelling

| nation | action | special | mission | fish | ship | dishes | vision | musician | session |"""

    sa = """| nation | n, a (/ā/), ti (/sh/), o→/ŏ/, n | Rule 17 | /nā-shŏn/ |
| special | s, p, e (/ĕ/), ci (/sh/), a→/ă/, l | Rule 17 | /spe-shăl/ |
| mission | m, i (/ĭ/), ss, si (/sh/), o→/ŏ/, n | Rule 17 | /mi-shŏn/ |
| vision | v, i (/ĭ/), si (/zh/), o→/ŏ/, n | Rule 17 (/zh/) | /vi-zhŏn/ |"""

    return render("practice", n=19, title="Latin /sh/ Mastery", typ="rule-practice",
        focus="TI, CI, SI — Latin /sh/ spellings", body=body,
        sa=sa, reading="nation &nbsp; special &nbsp; mission &nbsp; vision &nbsp; action &nbsp; musician\n\nThe nation has a special mission. My vision of the action is clear. The musician plays!",
        nn=21, ntitle=nt(20),
        check="1. Which Latin /sh/ spelling says /zh/? *(SI — as in vision and television.)*\n2. What's the difference between SH and TI? *(SH is for everyday English; TI is Latin for -tion words.)*\n3. Spell 'nation,' 'special,' and 'mission' from dictation.",
        home="Write 3 words with SH and 3 with Latin /sh/. Explain the difference!")

def gen_morph(n, title, affix, typ, meaning, definition, example_pairs, build_words, reading, spell_words, nn):
    """Generate a morphology lesson for a prefix or suffix."""
    what = "Prefix" if typ == "prefix" else "Suffix"
    sep = "------|" if typ == "prefix" else "---|------|"
    sep2 = "------|" if typ == "prefix" else "---|------|"
    
    examples = "\n".join(f"| {w} | {root} | {gloss} |" for w, root, gloss in example_pairs)
    build = "\n".join(f"| {r} | {affix}{' ' + r if typ == 'prefix' else r + ' ' + affix} | {'—' if typ == 'prefix' else ''} | {'—' if typ == 'prefix' else ''} |" for r in build_words)
    
    return render("morph", n=n, title=title, focus=f"**{affix}**", what=what, meaning=meaning,
        definition=definition, examples=examples, build=build, reading=reading,
        spell=" &nbsp;&nbsp; ".join(spell_words), nn=nn, ntitle=nt(nn), sep=sep, sep2=sep2)

def gen_rule23():
    return render("rule", n=30, rn=23, name="AL- Prefix Has One L",
        statement="The prefix **AL-** has only one L.",
        why="AL- is a prefix meaning 'all' or 'to/toward.' Even though 'all' has two L's, the prefix AL- has only one. Compare: all + ready → already, all + though → although, all + ways → always. The prefix 'almost always' has one L!",
        examples="already, although, always, also, almost, altogether, albeit",
        spot="| already | AL- (one L) + ready |\n| although | AL- (one L) + though |\n| always | AL- (one L) + ways |\n| almost | AL- (one L) + most |\n| also | AL- (one L) + so |\n| altogether | AL- + together |",
        words="| already | al- (/äl/), r (/r/), ea (/ĕ/), d (/d/), y (/ē/) | Rule 23 | /äl-red-ē/ |\n| always | al- (/äl/), w (/w/), ay (/ā/), s (/z/) | Rule 23 | /äl-wāz/ |\n| almost | al- (/äl/), m (/m/), o (/ō/), s (/s/), t (/t/) | Rule 23 | /äl-mōst/ |",
        reading="already &nbsp; although &nbsp; always &nbsp; also &nbsp; almost\n\nI already ate. Although it is late, I always read. I also almost finished!",
        nn=32, ntitle=nt(31), q3="Why does 'already' have one L but 'all ready' has two? *(The prefix AL- has one L. 'All ready' is two separate words.)*",
        home="Find AL- words in a book. Write them and circle the one-L prefix.")

def gen_rule24():
    return render("rule", n=31, rn=24, name="-FUL Suffix Has One L",
        statement="The suffix **-FUL** has only one L.",
        why="Though 'full' has two L's, the suffix -FUL has only one. Compare: hope + full → hopeful (one L), use + full → useful, beauty + full → beautiful. Only one L in the suffix!",
        examples="hopeful, useful, beautiful, careful, joyful, playful, helpful, thankful, wonderful, powerful",
        spot="| hope + ful | helpful — one L |\n| care + ful | careful — one L |\n| use + ful | useful — one L |\n| beauty + ful | beautiful — one L (Y→I first!) |\n| joy + ful | joyful — one L |",
        words="| hopeful | h (/h/), o (/ō/), p (/p/), e (/ə/→/ĕ/ STSp), ful (/fŭl/) | Rules 24 + 31 | /hōp-fŭl/ |\n| careful | c (/k/), are (/ār/), ful (/fŭl/) | Rule 24 | /kār-fŭl/ |\n| beautiful | b (/b/), eau (/ü/), ti (/t/), i→/ĭ/, ful (/fŭl/) | Rules 15 + 24 | /büt-ĭ-fŭl/ |",
        reading="hopeful &nbsp; careful &nbsp; beautiful &nbsp; useful &nbsp; joyful &nbsp; thankful\n\nBe hopeful and careful. The beautiful painting is useful. I am joyful and thankful!",
        nn=33, ntitle=nt(32), q3="Why does 'beautiful' change Y to I? *(Rule 15: Y→I before a suffix. Beauty + ful → beautiful.)*",
        home="Write 5 words with the -ful suffix. Circle the one-L suffix in each.")

# ── MORPHOLOGY DATA ─────────────────────────────────────────────────

PREFIXES = [
    (20, "Prefixes un- and re-", "un-", "not, opposite of", "UN- means 'not' or 'opposite.' RE- means 'again' or 'back.'",
     [("un do → undo","—","—"),("re do → redo","—","—"),("un tie → untie","—","—"),("re turn → return","—","—")],
     ["do","tie","pack","lock","wind"], "undo, redo, untie, return, replay, unlock, unpack, rewrite",
     ["undo","redo","untie","return","unlock","rewrite"], 25),
    (21, "Prefixes in- and dis-", "in-/dis-", "not, opposite", "IN- (and its forms im-, il-, ir-) means 'not.' DIS- also means 'not' or 'opposite.'",
     [("in correct → incorrect","—","—"),("dis agree → disagree","—","—"),("im possible → impossible","—","—"),("dis like → dislike","—","—")],
     ["correct","agree","like","appear","honest"], "incorrect, disagree, dislike, disappear, dishonest, unable, replay",
     ["incorrect","disagree","dislike","disappear","unable"], 26),
    (22, "Prefixes pre- and pro-", "pre-/pro-", "before, forward", "PRE- means 'before.' PRO- means 'forward' or 'for.'",
     [("pre view → preview","—","—"),("pro ceed → proceed","—","—"),("pre pay → prepay","—","—"),("pro pel → propel","—","—")],
     ["view","pay","test","cede","claim"], "preview, prepay, pretest, proceed, proclaim, propel, prefix",
     ["preview","prepay","proceed","propel","pretest"], 27),
    (23, "Prefixes sub- and inter-", "sub-/inter-", "under, between", "SUB- means 'under' or 'below.' INTER- means 'between' or 'among.'",
     [("sub marine → submarine","—","—"),("inter national → international","—","—"),("sub way → subway","—","—"),("inter act → interact","—","—")],
     ["marine","way","merge","view","change"], "submarine, subway, submerge, interview, international, interact",
     ["submarine","subway","interview","international","interact"], 28),
]

SUFFIXES = [
    (24, "Suffixes -er and -or", "-er/-or", "one who, that which", "-ER and -OR both mean 'one who' or 'that which does something.'",
     [("teach er → teacher","—","—"),("act or → actor","—","—"),("bake er → baker","—","—"),("sail or → sailor","—","—")],
     ["teach","bake","act","sail","invent"], "teacher, baker, actor, sailor, inventor, driver, writer",
     ["teacher","baker","actor","sailor","inventor"], 29),
    (25, "Suffixes -tion and -sion", "-tion/-sion", "act of, state of", "-TION and -SION mean 'the act of' or 'state of.' They turn verbs into nouns.",
     [("act tion → action","—","—"),("divi sion → division","—","—"),("collect tion → collection","—","—"),("deci sion → decision","—","—")],
     ["act","collect","divide","decide","direct"], "action, collection, division, decision, direction, nation, mission",
     ["action","collection","division","decision","nation"], 30),
    (26, "Suffixes -able and -ible", "-able/-ible", "able to be", "-ABLE and -IBLE mean 'able to be' or 'can be done.' Most words use -able.",
     [("wash able → washable","—","—"),("vis ible → visible","—","—"),("read able → readable","—","—"),("flex ible → flexible","—","—")],
     ["wash","read","flex","break","love"], "washable, readable, flexible, breakable, lovable, visible, audible",
     ["washable","readable","flexible","breakable","visible"], 31),
    (27, "Suffixes -ment and -ness", "-ment/-ness", "state of, quality of", "-MENT means 'the result of' or 'state of.' -NESS means 'the quality of being.'",
     [("enjoy ment → enjoyment","—","—"),("dark ness → darkness","—","—"),("pay ment → payment","—","—"),("kind ness → kindness","—","—")],
     ["enjoy","pay","dark","kind","soft"], "enjoyment, payment, darkness, kindness, softness, treatment, sadness",
     ["enjoyment","payment","darkness","kindness","softness"], 32),
    (28, "Suffixes -ly and -ful", "-ly/-ful", "in a way, full of", "-LY means 'in a ___ way' (adverbs). -FUL means 'full of.'",
     [("quick ly → quickly","—","—"),("hope ful → hopeful","—","—"),("slow ly → slowly","—","—"),("joy ful → joyful","—","—")],
     ["quick","slow","hope","joy","care"], "quickly, slowly, hopeful, joyful, careful, softly, peaceful",
     ["quickly","slowly","hopeful","joyful","careful"], 33),
    (29, "Suffixes -less and -ous", "-less/-ous", "without, full of", "-LESS means 'without.' -OUS means 'full of' or 'having the quality of.'",
     [("hope less → hopeless","—","—"),("danger ous → dangerous","—","—"),("fear less → fearless","—","—"),("joy ous → joyous","—","—")],
     ["hope","fear","danger","joy","nerve"], "hopeless, fearless, dangerous, joyous, nervous, careless, famous",
     ["hopeless","fearless","dangerous","joyous","nervous"], 34),
]

# ── READERS ─────────────────────────────────────────────────────────

def gen_firefly():
    return render("reader4", n=38, title="Reader: Firefly — Nightlight with Wings",
        phonograms="y (=/ē/), silent E, igh, ir",
        warmup_words="firefly &nbsp; light &nbsp; glow &nbsp; night &nbsp; wings &nbsp; summer &nbsp; garden &nbsp; dark &nbsp; blink &nbsp; shine",
        stitle="Firefly: Nightlight with Wings",
        story="""<div class="reader-page">
<div class="reader-text">

**Firefly: Nightlight with Wings**

The sun goes down. The sky turns dark.

A tiny light blinks in the garden. Blink! Blink!

It is a firefly.

The firefly has a special secret. Its body makes light! This is called bioluminescence.

The firefly flashes its light to find a friend. "Over here!" it signals with a blink.

Another firefly blinks back. "I see you!"

The firefly does not make heat with its light — only a cool glow. This is amazing!

Fireflies love warm summer nights. They dance in the air, tiny stars close to the ground.

A child watches from the porch. "Look, Mom! Fireflies!"

The child catches one gently in a jar. She watches it blink.

Then she lets it go. "Fly free, little light."

The firefly rises into the night sky, blinking all the way.

Good night, firefly. Thank you for sharing your light.

The End.

</div>
<div class="reader-sidebar">

### Spelling Aid

**Focus:** igh (light, night, flight), ou (out, ground), ph (firefly? No — that's 'f' and 'l'), silent E (make, rise, close)

**Challenge words:**
- bioluminescence (bī-ō-lü-mĭ-nes-ĕns) — bio = life, lumin = light
- signals (g says /g/ — doesn't soften before n)
- gently (g says /j/ — softens before l? No — it's before consonant. Actually /j/ because Latin root *gent-*)

</div>
</div>""",
        talk="1. How does a firefly make light? *(Bioluminescence — a chemical reaction in its body!)*\n2. Why does the firefly blink? *(To find a friend/mate.)*\n3. Find 3 words with silent E in the story.",
        nn=40, ntitle=nt(39))

def gen_trains():
    return render("reader4", n=39, title="Reader: Trains — A Blast of Fast",
        phonograms="ai, ay, silent E, er, tch",
        warmup_words="train &nbsp; steam &nbsp; coal &nbsp; rail &nbsp; engine &nbsp; fast &nbsp; station &nbsp; track &nbsp; iron &nbsp; smoke",
        stitle="Trains: A Blast of Fast",
        story="""<div class="reader-page">
<div class="reader-text">

**Trains: A Blast of Fast**

The station is busy. A train is coming.

The whistle blows. WHOOO-WHOOO!

Trains have been moving people and things for hundreds of years.

The first trains ran on steam. Steam engines burned coal to make power. They chugged and puffed across the land.

Now trains run on diesel or electric power. They are faster and cleaner.

A freight train carries heavy loads — cars, coal, grain, and lumber. The cars link together in a long chain.

A passenger train carries people. The seats are comfortable. You can read, sleep, or watch the world go by outside the window.

The train goes into a tunnel. Darkness! Then light again as it comes out the other side.

The fastest trains in the world can go over 200 miles per hour! They float above the track using magnets. These are called maglev trains.

"All aboard!" calls the conductor.

The whistle blows one more time. The train starts to move. Faster and faster it goes.

Off into the distance. A silver line against the green land.

What a wonderful invention the train is!

The End.

</div>
<div class="reader-sidebar">

### Spelling Aid

**Focus:** ai (train, chain, grain, against), ou (out, outside, thousand), silent E (make, move, time, side)

**Challenge words:**
- freight (frāt) — EIGH = /ā/, GH silent (Rule 28)
- conductor (con-duc-tor) — OR = /er/ unstressed (Rule 31.3)
- comfortable (com-fort-a-ble) — silent E? No

</div>
</div>""",
        talk="1. What powered the first trains? *(Steam engines burning coal.)*\n2. How fast can maglev trains go? *(Over 200 miles per hour!)*\n3. Find words with AI and OA in the story.",
        nn=41, ntitle=nt(40))

# ── ADDITIONAL RULES ────────────────────────────────────────────────

def gen_rule19():
    return render("rule", n=32, rn=19, name="Past Tense -ED Sounds",
        statement="The past-tense ending **-ED** forms the past tense of regular verbs. Its spelling is always -ED, but its sound varies.",
        why="You already learned the three sounds of -ED from Rule 20 (Stage 2). Rule 19 is about using -ED to form past tense. Most verbs just add -ED. Some double the consonant (Rule 14: stop→stopped). Some drop silent E (Rule 13: bake→baked). Some change Y→I (Rule 15: carry→carried).",
        examples="walk→walked, play→played, stop→stopped, bake→baked, carry→carried, try→tried, hop→hopped, hope→hoped",
        spot="| walk + ed | walked — no change needed |\n| stop + ed | stopped — double P (Rule 14) |\n| bake + ed | baked — drop E (Rule 13) |\n| carry + ed | carried — Y→I (Rule 15) |\n| play + ed | played — no change (AY is a phonogram) |",
        words="| walked | w (/w/), a (/ä/), l (/l/), k (/k/), ed (/t/) | Rule 19: ED says /t/ after unvoiced /k/ | /wäkt/ |\n| played | p (/p/), l (/l/), ay (/ā/), ed (/d/) | Rules 19-20: ED=/d/ after voiced | /plād/ |\n| stopped | s (/s/), t (/t/), o (/ŏ/), p (/p/), p (/p/), ed (/t/) | Rules 14 + 19 + 20 | /stŏpt/ |",
        reading="walked &nbsp; played &nbsp; stopped &nbsp; baked &nbsp; carried &nbsp; tried\n\nI walked to the park and played. The rain stopped. Mom baked a cake. I carried it home.",
        nn=34, ntitle=nt(33), q3="How many rules can apply when forming past tense? *(Up to 3: Rules 13, 14, 15, 19, 20!)*",
        home="Write the past tense of: walk, stop, bake, carry, play, try. Name the rules you used.")

def gen_rule21():
    return render("rule", n=33, rn=21, name="Plural -S and -ES",
        statement="To make most nouns plural, add **-S**. Add **-ES** when the word ends in S, SH, CH, X, or Z.",
        why="The -ES adds a syllable /ez/ so you can hear the plural. 'Box' + 's' = 'boxs' (hard to say!). 'Box' + 'es' = 'boxes' (easy!). The E provides an extra syllable.",
        examples="cat→cats, dog→dogs, box→boxes, dish→dishes, church→churches, buzz→buzzes, bus→buses, fox→foxes",
        spot="| cat + s | cats — just add S |\n| box + es | boxes — ends in X, needs ES |\n| dish + es | dishes — ends in SH, needs ES |\n| church + es | churches — ends in CH, needs ES |\n| buzz + es | buzzes — ends in Z, needs ES |",
        words="| boxes | b (/b/), o (/ŏ/), x (/ks/), e (/ə/→/ĕ/ STSp), s (/z/) | Rule 21 | /bŏk-sĕz/ |\n| dishes | d, i (/ĭ/), sh (/sh/), e→/ĕ/, s (/z/) | Rule 21 + 31 | /dĭ-shĕz/ |\n| churches | ch (/ch/), ur (/er/), ch (/ch/), e→/ĕ/, s | Rule 21 + 31 | /cher-chĕz/ |",
        reading="cats &nbsp; dogs &nbsp; boxes &nbsp; dishes &nbsp; churches &nbsp; foxes &nbsp; buses\n\nThe cats and dogs have boxes. The dishes are in the churches. Foxes ride buses!",
        nn=35, ntitle=nt(34), q3="Why does 'box' need -ES instead of just -S? *(It ends in X — you can't hear the plural without the extra syllable!)*",
        home="Write the plural of: cat, box, dish, church, fox, bus. Circle the ones that use -ES.")

def gen_rule22():
    return render("rule", n=34, rn=22, name="3rd Person Singular -S and -ES",
        statement="To make a verb agree with he/she/it in present tense, add **-S**. Add **-ES** when the verb ends in S, SH, CH, X, or Z.",
        why="Same pattern as plural nouns! He/she/it verbs need -S. When the verb ends in a hissing sound (S, SH, CH, X, Z), add -ES so you can hear the ending.",
        examples="run→runs, walk→walks, fix→fixes, wash→washes, watch→watches, buzz→buzzes, miss→misses, catch→catches",
        spot="| he run + s | he runs — just add S |\n| she fix + es | she fixes — ends in X |\n| it wash + es | it washes — ends in SH |\n| he catch + es | he catches — ends in CH (Rule 27: TCH after short a!) |",
        words="| fixes | f (/f/), i (/ĭ/), x (/ks/), e→/ĕ/, s | Rule 22 + 31 | /fĭk-sĕz/ |\n| washes | w (/w/), a (/ä/), sh (/sh/), e→/ĕ/, s | Rules 10 + 22 | /wä-shĕz/ |\n| catches | c (/k/), a (/ă/), tch (/ch/), e→/ĕ/, s | Rules 22 + 27 | /kă-chĕz/ |",
        reading="runs &nbsp; walks &nbsp; fixes &nbsp; washes &nbsp; catches &nbsp; watches\n\nHe runs and walks. She fixes the box. It washes away. He catches the ball and watches the game.",
        nn=36, ntitle=nt(35), q3="What do plural nouns and 3rd person verbs have in common? *(Both use -S or -ES following the same rules!)*",
        home="Write: he (run), she (fix), it (wash), he (catch). Apply Rule 22 to each.")

def gen_rule29():
    return render("rule", n=35, rn=29, name="Z, Not S, at Beginning",
        statement="**Z**, never **S**, is used at the beginning of a base word for the /z/ sound.",
        why="English uses Z for /z/ at the beginning of words: zip, zap, zoo, zone. S at the beginning says /s/ (sit, sun, see). S says /z/ in the middle or at the end: has, is, music, visit.",
        examples="zip, zap, zoo, zone, zebra, zero, zigzag, zoom",
        spot="| zip | Z at start = /z/ ✓ |\n| sip | S at start = /s/ — different word! ✗ |\n| has | S at end = /z/ ✓ |\n| is | S at end = /z/ ✓ |\n| music | S in middle = /z/ (between vowels) ✓ |",
        words="| zip | z (/z/), i (/ĭ/), p (/p/) | Rule 29 | /zĭp/ |\n| zebra | z (/z/), e (/ē/), b (/b/), r (/r/), a (/ə/) | Rule 29 + 4 + 31 | /zē-brə/ |\n| zero | z (/z/), e (/ē/), r (/r/), o (/ō/) | Rules 4 + 29 | /zē-rō/ |",
        reading="zip &nbsp; zap &nbsp; zoo &nbsp; zone &nbsp; zebra &nbsp; zero &nbsp; zigzag &nbsp; zoom\n\nZip, zap, zoom! The zebra at the zoo runs from zone zero. Zigzag fast!",
        nn=37, ntitle=nt(36), q3="Why isn't the first sound in 'zip' spelled with S? *(Rule 29: Z, not S, spells /z/ at the beginning of a base word.)*",
        home="Write 5 words that start with Z. Compare: zip/sip, zoo/Sue, zone/sown.")

def gen_irregular_verbs():
    return """# Lesson 40: Irregular Verbs

**Stage 4** · Lesson 40 · practice

---

## Warm-Up: Review Regular Past Tense

> Quick: walked, played, stopped, baked, carried. Which rules apply?

---

## Irregular Verbs

Most verbs form past tense by adding -ED. But some verbs are IRREGULAR — they change in different ways. These are old words that come from Old English and Germanic languages.

### Common Irregular Verbs

| Present | Past | What Changed? |
|---------|------|--------------|
| make | made | Silent E dropped, D added |
| have | had | VE→D |
| come | came | O→A (vowel change) |
| run | ran | U→A (vowel change) |
| swim | swam | I→A (vowel change) |
| sing | sang | I→A (vowel change) |
| drink | drank | I→A (vowel change) |
| drive | drove | I→O (vowel change) |
| write | wrote | I→O (vowel change) |
| ride | rode | I→O |
| give | gave | I→A |
| take | took | A→OO |
| see | saw | EE→AW |
| eat | ate | EA→A |
| go | went | completely different! |
| buy | bought | completely different! |

### Patterns

Some irregular verbs follow patterns:
- i→a→u: sing→sang→sung, drink→drank→drunk, swim→swam→swum
- i→o: drive→drove, write→wrote, ride→rode

---

## Spelling Practice

| Present | Past | Write the Past |
|---------|------|---------------|
| make | made | |
| run | ran | |
| sing | sang | |
| drive | drove | |
| give | gave | |
| take | took | |
| see | saw | |
| go | went | |

---

## Quick Check

1. What does 'irregular' mean? *(It doesn't follow the normal -ED pattern.)*
2. Name 3 verbs where the vowel changes in past tense.
3. What's the past tense of 'go'? *(Went — completely different word!)*

---

**Next lesson:** Lesson 41: Irregular Plurals

---

*Practice at home: Write 5 sentences using today's irregular past tense verbs.*
"""

def gen_irregular_plurals():
    return """# Lesson 41: Irregular Plurals

**Stage 4** · Lesson 41 · practice

---

## Warm-Up: Review Regular Plurals

> Quick: cats, dogs, boxes, dishes, churches. Why -S vs -ES?

---

## Irregular Plurals

Most nouns add -S or -ES for plurals. But some old English words keep their ancient plural forms!

### Types of Irregular Plurals

#### 1. Vowel Change (Germanic origin)

| Singular | Plural | Change |
|----------|--------|--------|
| man | men | a→e |
| woman | women | a→e (and pronunciation change!) |
| foot | feet | oo→ee |
| tooth | teeth | oo→ee |
| goose | geese | oo→ee |
| mouse | mice | ouse→ice |
| louse | lice | ouse→ice |

#### 2. -EN Ending (Old English)

| Singular | Plural |
|----------|--------|
| child | children |
| ox | oxen |

#### 3. Same Form (No Change)

| Singular and Plural |
|---------------------|
| deer |
| sheep |
| fish (sometimes fishes) |
| moose |

#### 4. Latin/Greek Plurals

| Singular | Plural | Origin |
|----------|--------|--------|
| cactus | cacti | Latin (-us→-i) |
| fungus | fungi | Latin |
| criterion | criteria | Greek (-on→-a) |
| phenomenon | phenomena | Greek |

---

## Practice

| Singular | Plural |
|----------|--------|
| man | ______ |
| foot | ______ |
| child | ______ |
| mouse | ______ |
| deer | ______ |
| goose | ______ |
| tooth | ______ |
| sheep | ______ |

---

## Quick Check

1. Why are some plurals irregular? *(They come from Old English, German, Latin, or Greek.)*
2. Name 3 words whose plurals don't change.
3. What's the plural of 'goose'? *(Geese — not 'gooses'!)*

---

**Next lesson:** Lesson 42: Reader — Firefly

---

*Practice at home: Find 5 irregular plurals in a book. Write the singular and plural.*
"""

def gen_morph_review(typ):
    if typ == "prefixes":
        title = "Morpheme Review: Prefixes"
        g1 = "Match the Prefix"
        gb1 = "un- (not) + tie = untie\nre- (again) + do = redo\nin- (not) + correct = incorrect\ndis- (not) + agree = disagree\npre- (before) + view = preview\npro- (forward) + ceed = proceed\nsub- (under) + marine = submarine\ninter- (between) + national = international"
        g2 = "Build New Words"
        gb2 = "Add a prefix to make a new word:\nkind + un- = ______\nbuild + re- = ______\npossible + im- = ______\nlike + dis- = ______\npay + pre- = ______\nway + sub- = ______"
        g3 = "Meaning Match"
        gb3 = "redo (do again), untie (opposite of tie), prepay (pay before), submarine (under water), incorrect (not correct), disagree (not agree)"
        challenge = "untie, redo, incorrect, disagree, preview, proceed, submarine, international"
    else:
        title = "Morpheme Review: Suffixes"
        g1 = "Match the Suffix"
        gb1 = "teach + er = teacher (one who teaches)\nact + or = actor (one who acts)\nact + ion = action (the act of)\nwash + able = washable (able to be washed)\nenjoy + ment = enjoyment (state of enjoying)\ndark + ness = darkness (quality of being dark)\nquick + ly = quickly (in a quick way)\nhope + ful = hopeful (full of hope)\nhope + less = hopeless (without hope)\ndanger + ous = dangerous (full of danger)"
        g2 = "Build New Words"
        gb2 = "Add a suffix:\nbake + er = ______\ncollect + ion = ______\nread + able = ______\npay + ment = ______\nkind + ness = ______\nslow + ly = ______\ncare + ful = ______\nfear + less = ______"
        g3 = "Meaning Match"
        gb3 = "teacher (one who teaches), collection (act of collecting), readable (able to be read), kindness (quality of being kind), slowly (in a slow way), careful (full of care), fearless (without fear), dangerous (full of danger)"
        challenge = "teacher, actor, collection, washable, enjoyment, kindness, quickly, careful, fearless"

    return render("review", 
        n={"prefixes":44,"suffixes":45}[typ],
        title=title, nn={"prefixes":45,"suffixes":46}[typ],
        ntitle=nt({"prefixes":45,"suffixes":46}[typ]),
        g1=g1, gb1=gb1, g2=g2, gb2=gb2, g3=g3, gb3=gb3,
        challenge=challenge, home="Review your morpheme wall!")

def gen_mixed_spelling_4():
    words = """| beautiful | b, eau (/ü/), ti, ful | Rules 15 + 24 | /büt-ĭ-fŭl/ |
| running | r, u (/ŭ/), n, n, i, ng | Rule 14 | /rŭn-ing/ |
| nation | n, a (/ā/), ti (/sh/), o→/ŏ/ STSp, n | Rule 17 + 31 | /nā-shŏn/ |
| special | s, p, e, ci (/sh/), a→/ă/ STSp, l | Rule 17 | /spe-shăl/ |
| making | m, a (/ā/), k, i, ng | Rule 13 | /māk-ing/ |
| babies | b, a (/ā/), b, ie, s | Rule 15 | /bā-bēz/ |
| vision | v, i, si (/zh/), o→/ŏ/ STSp, n | Rule 17 | /vi-zhŏn/ |
| careful | c, are, ful | Rule 24 | /kār-fŭl/ |"""
    
    return f"""# Lesson 46: Mixed Spelling Analysis — Stage 4

**Stage 4** · Lesson 46 · spelling-analysis

---

## Warm-Up: Phonogram Flash Review

> Flash all 75 phonograms.

---

## Mixed Spelling Analysis

Today we practice ALL skills from Stage 4: suffixing, Latin /sh/, say-to-spell, and morphology.

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{words}

---

## Reading

> beautiful &nbsp; running &nbsp; nation &nbsp; special &nbsp; making &nbsp; babies &nbsp; vision &nbsp; careful

> The beautiful nation is making special babies! I am running with a careful vision.

---

## Quick Check

1. Which was hardest to spell? Why?
2. How many different suffixing rules did you use today?
3. Spell 'beautiful' and 'nation' from dictation.

---

**Next lesson:** Lesson 47: All Stage 4 Concepts Review

---

*Practice at home: Choose 4 words and write each one 3 times.*
"""


# ── MAIN ────────────────────────────────────────────────────────────

def generate():
    # 1: Review Stage 3
    # 2-7: Schwa
    yield 1, render("schwa", n=1, title="Schwa: The Lazy Vowel Sound", typ="rule-intro",
        focus="schwa", body=gen_schwa2(), nn=2, ntitle=nt(2),
        check="1. What is schwa? *(The lazy /ə/ sound in unstressed syllables.)*\n2. Which vowels can say schwa? *(ALL of them — a, e, i, o, u.)*\n3. What's the say-to-spell of 'about'? *(ā-bout!)*",
        home="Find 5 schwa words in a book. Say each one normally, then say-to-spell.")

    yield 2, render("schwa", n=2, title="Say-to-Spell: Unlocking Schwa Words", typ="say-to-spell",
        focus="say-to-spell technique", body=gen_say_to_spell(), nn=3, ntitle=nt(3),
        check=gen_say_to_spell_check(),
        home="Practice say-to-spell with: about, seven, pencil, animal, family.")

    yield 3, gen_schwa_practice()  # returns formatted content directly
    # Hack: gen_schwa_practice returns a string but SCHWA_TMP.format was already called inside

    yield 4, render("schwa", n=4, title="Rule 31.2: O→/ŭ/ Before W TH M N V", typ="rule-intro",
        focus="Rule 31.2", body=gen_rule31_2(), nn=5, ntitle=nt(5),
        check="1. Rule 31.2: O may say /ŭ/ before which consonants? *(W, TH, M, N, V)*\n2. Give 3 examples.\n3. Spell 'love' and 'mother' from dictation.",
        home="Find words with O→/ŭ/: love, mother, some, done, above, cover.")

    yield 5, render("schwa", n=5, title="Rule 31.3: AR/OR→/er/ Unstressed", typ="rule-intro",
        focus="Rule 31.3", body=gen_rule31_3(), nn=6, ntitle=nt(6),
        check="1. When do AR and OR say /er/? *(In unstressed syllables.)*\n2. Give an AR→/er/ example and an OR→/er/ example.\n3. Spell 'dollar' and 'doctor' from dictation.",
        home="Find words ending in -ar and -or. Does the ending say /er/?")

    yield 6, gen_schwa_mastery()

    # 8-17: Suffixing Rules
    yield 7, gen_rule13()
    yield 8, gen_rule14()
    yield 9, gen_rule14_review()

    # 13: Mid-Assessment
    yield 10, render("assessment", n=10, title="Mid-Stage 4 Assessment",
        overview="Check progress on schwa, Rules 13-14, and say-to-spell.",
        schwa_check="| about | | ☐ |\n| seven | | ☐ |\n| pencil | | ☐ |\n| love | | ☐ |\n| dollar | | ☐ |",
        schwa_total=5,
        suffix_check="| making | | ☐ |\n| hopping | | ☐ |\n| using | | ☐ |\n| running | | ☐ |\n| opening | | ☐ |",
        suffix_total=5,
        latin_check="| nation | | ☐ |\n| special | | ☐ |\n| vision | | ☐ |",
        latin_total=3,
        morph_check="| untie | | ☐ |\n| redo | | ☐ |\n| disagree | | ☐ |",
        morph_total=3,
        spell_check="| about | ☐ |\n| making | ☐ |\n| hopping | ☐ |\n| seven | ☐ |\n| love | ☐ |\n| dollar | ☐ |\n| running | ☐ |\n| using | ☐ |",
        spell_total=8,
        next="If ≥85%: Continue. If weaker, review trouble spots for 1 week and retest.")

    # 14-17: Rules 15-16 + Review
    yield 11, gen_rule15()
    yield 12, gen_rule16()
    yield 13, gen_suffix_review_17()

    # 18-23: Latin /sh/
    yield 14, gen_ti()
    yield 15, gen_ci()
    yield 16, gen_si()
    yield 17, gen_rule17()
    yield 18, gen_rule18()
    yield 19, gen_latin_mastery()

    # 24-33: Morphology
    for n, title, affix, meaning, definition, ex, build, read, spell, nn in PREFIXES + SUFFIXES:
        yield n, gen_morph(n, title, affix, "prefix" if n <= 23 else "suffix", meaning, definition, ex, build, read, spell, nn)

    # 34-39: Rules 23, 24, 19, 21, 22, 29
    yield 30, gen_rule23()
    yield 31, gen_rule24()
    yield 32, gen_rule19()
    yield 33, gen_rule21()
    yield 34, gen_rule22()
    yield 35, gen_rule29()

    # 40-41: Irregulars
    yield 36, gen_irregular_verbs()
    yield 37, gen_irregular_plurals()

    # 42-43: Readers
    yield 38, gen_firefly()
    yield 39, gen_trains()

    # 44-45: Morpheme Reviews
    yield 40, gen_morph_review("prefixes")
    yield 41, gen_morph_review("suffixes")

    # 46: Mixed Spelling
    yield 42, gen_mixed_spelling_4()

    # 47: Review
    yield 43, render("review", n=40, title="Review: All Stage 4 Concepts", nn=38, ntitle=nt(38),
        g1="Schwa Check", gb1="Say-to-spell: about, seven, pencil, love, mother, dollar, doctor, animal, family, chocolate.",
        g2="Suffixing Check", gb2="Write -ing form: make, hop, use, run, sit, swim, cry, study. Which rules apply?",
        g3="Latin /sh/ Check", gb3="Spell: nation, special, mission, vision, action, musician. TI, CI, or SI?",
        challenge="about, making, hopping, nation, special, beautiful, children, vision, careful, running",
        home="Review all Stage 4 flashcards!")

    # 48: Assessment
    yield 44, render("assessment", n=41, title="Stage 4 Mastery Check",
        overview="Final Stage 4 assessment. Check mastery of schwa, suffixing rules, Latin /sh/, morphology, and all Stage 4 concepts.",
        schwa_check="| about | | ☐ |\n| pencil | | ☐ |\n| love | | ☐ |\n| dollar | | ☐ |\n| doctor | | ☐ |\n| family | | ☐ |",
        schwa_total=6,
        suffix_check="| making | | ☐ |\n| hopping | | ☐ |\n| crying | | ☐ |\n| carried | | ☐ |\n| babies | | ☐ |\n| careful | | ☐ |\n| already | | ☐ |",
        suffix_total=7,
        latin_check="| nation | | ☐ |\n| special | | ☐ |\n| vision | | ☐ |\n| musician | | ☐ |\n| session | | ☐ |",
        latin_total=5,
        morph_check="| untie | | ☐ |\n| redo | | ☐ |\n| disagree | | ☐ |\n| preview | | ☐ |\n| submarine | | ☐ |\n| teacher | | ☐ |\n| washable | | ☐ |\n| hopeless | | ☐ |",
        morph_total=8,
        spell_check="| beautiful | ☐ |\n| running | ☐ |\n| nation | ☐ |\n| special | ☐ |\n| babies | ☐ |\n| vision | ☐ |\n| careful | ☐ |\n| making | ☐ |\n| hopping | ☐ |\n| already | ☐ |",
        spell_total=10,
        next="If ≥85%: Advance to Stage 5. If weaker, review specific lessons for 1-2 weeks.")

# ── SLUGS ───────────────────────────────────────────────────────────

S = {
    1:"schwa-1",2:"schwa-2",3:"schwa-3",4:"schwa-4",5:"schwa-5",
    6:"schwa-mastery",
    7:"rule-13",8:"rule-14",
    9:"rule-13-14-review",10:"assessment-6",
    10:"assessment-6",11:"rule-15",12:"rule-16",13:"suffixing-review",
    14:"pg-ti",15:"pg-ci",16:"pg-si",17:"rule-17",18:"rule-18",
    19:"latin-sh-mastery",
    20:"prefix-un-re",21:"prefix-in-dis",22:"prefix-pre-pro",23:"prefix-sub-inter",
    24:"suffix-er-or",25:"suffix-tion-sion",26:"suffix-able-ible",
    27:"suffix-ment-ness",28:"suffix-ly-ful",29:"suffix-less-ous",
    30:"rule-23",31:"rule-24",32:"rule-19",33:"rule-21",34:"rule-22",35:"rule-29",
    36:"irregular-verbs",37:"irregular-plurals",
    38:"reader-5",39:"reader-6",
    40:"morph-review-1",41:"morph-review-2",
    42:"spell-mixed-4",43:"review-9",44:"assessment-7"
}

def main():
    for num, content in generate():
        slug = S.get(num, f"lesson-{num:03d}")
        (OUT_DIR / f"{slug}.md").write_text(stamp(content), encoding="utf-8")
        print(f"  lessons/stage-4/{slug}.md")
    print(f"\nDone! 48 lessons in lessons/stage-4/")

if __name__ == "__main__":
    main()
