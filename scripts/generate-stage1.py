#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate all 48 Stage 1 lesson markdown files with real educational content."""

import os, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "lessons" / "stage-1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Teacher script injection (issue #4)
sys.path.insert(0, str(PROJECT_ROOT / "framework"))
from teacher_script import format_phonogram_script  # noqa: E402

# ── PHONOGRAM DATA ──────────────────────────────────────────────────

PHONOGRAMS = {
    "a": {
        "sounds": "/ă/ /ā/ /ä/",
        "sound_count": 3,
        "examples": [("ă", "at, cat, hat"), ("ā", "nation, acorn"), ("ä", "father, spa")],
        "vowel": True,
        "writing": [
            "Start at the midline.",
            "Curve around to make a circle (counter-clockwise).",
            "Go up and down in a straight line.",
        ],
        "group": 1,
    },
    "d": {
        "sounds": "/d/",
        "sound_count": 1,
        "examples": [("d", "dog, dad, dig")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Curve around to make a circle (counter-clockwise).",
            "Go up high, then straight down.",
        ],
        "group": 1,
    },
    "g": {
        "sounds": "/g/ /j/",
        "sound_count": 2,
        "examples": [("g", "go, get, gum"), ("j", "gem, giant, gym")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Curve around to make a circle (counter-clockwise).",
            "Go up, then curve down below the line into a tail.",
        ],
        "group": 1,
    },
    "c": {
        "sounds": "/k/ /s/",
        "sound_count": 2,
        "examples": [("k", "cat, cot, cup"), ("s", "cent, city, cycle")],
        "vowel": False,
        "writing": [
            "Start just below the midline.",
            "Curve around to make most of a circle (counter-clockwise).",
            "Leave a small opening on the right side.",
        ],
        "group": 1,
    },
    "o": {
        "sounds": "/ŏ/ /ō/ /ö/",
        "sound_count": 3,
        "examples": [("ŏ", "on, odd, hot"), ("ō", "go, no, so"), ("ö", "to, do, who")],
        "vowel": True,
        "writing": [
            "Start at the midline.",
            "Curve around to make a circle (counter-clockwise).",
            "Close the circle neatly.",
        ],
        "group": 1,
    },
    "qu": {
        "sounds": "/kw/",
        "sound_count": 1,
        "examples": [("kw", "queen, quit, quick")],
        "vowel": False,
        "writing": [
            "Q: Start at the midline. Curve around to make a circle.",
            "Then draw a short diagonal line from the circle outward.",
            "U: Start at the midline, curve down and back up.",
            "Q always needs U. They are a team!",
        ],
        "group": 1,
        "rule": "Rule 11: Q always needs a U. U is not a vowel here.",
    },
    "s": {
        "sounds": "/s/ /z/",
        "sound_count": 2,
        "examples": [("s", "sit, sun, see"), ("z", "is, has, as")],
        "vowel": False,
        "writing": [
            "Start just below the midline.",
            "Curve left, then right, like a snake.",
            "End at the baseline.",
        ],
        "group": 2,
    },
    "t": {
        "sounds": "/t/",
        "sound_count": 1,
        "examples": [("t", "top, tap, ten")],
        "vowel": False,
        "writing": [
            "Start at the top line.",
            "Draw a straight line down.",
            "Lift your pencil and cross it in the middle.",
        ],
        "group": 2,
    },
    "i": {
        "sounds": "/ĭ/ /ī/ /ē/",
        "sound_count": 3,
        "examples": [("ĭ", "it, in, sit"), ("ī", "item, silent"), ("ē", "radio, onion")],
        "vowel": True,
        "writing": [
            "Start at the midline.",
            "Draw a straight line down.",
            "Dot it at the top.",
        ],
        "group": 2,
    },
    "p": {
        "sounds": "/p/",
        "sound_count": 1,
        "examples": [("p", "pat, pen, pop")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a straight line down below the baseline.",
            "Go back up and curve around to make a circle at the top.",
        ],
        "group": 2,
    },
    "u": {
        "sounds": "/ŭ/ /ū/ /ö/",
        "sound_count": 3,
        "examples": [("ŭ", "up, cut, run"), ("ū", "unit, music"), ("ö", "put, push")],
        "vowel": True,
        "writing": [
            "Start at the midline.",
            "Curve down, then back up.",
            "Draw a straight line down.",
        ],
        "group": 2,
    },
    "j": {
        "sounds": "/j/",
        "sound_count": 1,
        "examples": [("j", "jam, jet, jump")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a straight line down below the baseline.",
            "Curve the bottom to the left into a hook.",
            "Dot it at the top.",
        ],
        "group": 2,
    },
    "r": {
        "sounds": "/r/",
        "sound_count": 1,
        "examples": [("r", "red, run, rat")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a straight line down.",
            "Go back up and curve over to the right.",
        ],
        "group": 3,
    },
    "n": {
        "sounds": "/n/",
        "sound_count": 1,
        "examples": [("n", "net, not, nap")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a straight line down.",
            "Go back up and curve over like a hill.",
            "Come straight down.",
        ],
        "group": 3,
    },
    "m": {
        "sounds": "/m/",
        "sound_count": 1,
        "examples": [("m", "man, map, mom")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a straight line down.",
            "Go back up and make one hill.",
            "Then make a second hill and come straight down.",
        ],
        "group": 3,
    },
    "e": {
        "sounds": "/ĕ/ /ē/",
        "sound_count": 2,
        "examples": [("ĕ", "end, egg, pet"), ("ē", "even, he, me")],
        "vowel": True,
        "writing": [
            "Start in the middle of the space.",
            "Draw a short straight line across.",
            "Curve around and up.",
        ],
        "group": 3,
    },
    "l": {
        "sounds": "/l/",
        "sound_count": 1,
        "examples": [("l", "leg, log, lap")],
        "vowel": False,
        "writing": [
            "Start at the top line.",
            "Draw a straight line down.",
        ],
        "group": 3,
    },
    "b": {
        "sounds": "/b/",
        "sound_count": 1,
        "examples": [("b", "big, bat, bed")],
        "vowel": False,
        "writing": [
            "Start at the top line.",
            "Draw a straight line down.",
            "Go back up to the midline and curve around to make a circle.",
        ],
        "group": 3,
    },
    "h": {
        "sounds": "/h/",
        "sound_count": 1,
        "examples": [("h", "hat, hot, hen")],
        "vowel": False,
        "writing": [
            "Start at the top line.",
            "Draw a straight line down.",
            "Go back up and curve over to make a hump.",
        ],
        "group": 4,
    },
    "k": {
        "sounds": "/k/",
        "sound_count": 1,
        "examples": [("k", "kit, king, kiss")],
        "vowel": False,
        "writing": [
            "Start at the top line.",
            "Draw a straight line down.",
            "From the middle, draw a line slanting in, then slanting out.",
        ],
        "group": 4,
    },
    "f": {
        "sounds": "/f/",
        "sound_count": 1,
        "examples": [("f", "fun, fan, fit")],
        "vowel": False,
        "writing": [
            "Start at the top line.",
            "Curve around and come straight down.",
            "Cross it in the middle.",
        ],
        "group": 4,
    },
    "v": {
        "sounds": "/v/",
        "sound_count": 1,
        "examples": [("v", "van, vet, vine")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a slanted line down to the right.",
            "Then slant up to the right.",
        ],
        "group": 4,
    },
    "w": {
        "sounds": "/w/",
        "sound_count": 1,
        "examples": [("w", "wet, win, wag")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Slant down, up, down, up — like two mountain peaks.",
        ],
        "group": 4,
    },
    "x": {
        "sounds": "/ks/ /z/",
        "sound_count": 2,
        "examples": [("ks", "box, fix, ox"), ("z", "xylophone")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a line slanting down to the right.",
            "Lift your pencil.",
            "Draw a line slanting down to the left, crossing the first line.",
        ],
        "group": 4,
    },
    "y": {
        "sounds": "/y/ /ĭ/ /ī/ /ē/",
        "sound_count": 4,
        "examples": [("y", "yes, yet, yell"), ("ĭ", "gym, myth"), ("ī", "by, my, fly"), ("ē", "baby, funny")],
        "vowel": True,
        "writing": [
            "Start at the midline.",
            "Draw a short slanted line down.",
            "Then a long slanted line down below the baseline.",
        ],
        "group": 5,
    },
    "z": {
        "sounds": "/z/",
        "sound_count": 1,
        "examples": [("z", "zip, zap, zoo")],
        "vowel": False,
        "writing": [
            "Start at the midline.",
            "Draw a line straight across.",
            "Slant down to the left.",
            "Draw a line straight across the bottom.",
        ],
        "group": 5,
    },
}

# ── LESSON DATA ─────────────────────────────────────────────────────

def group_phonograms(lesson_num, all_up_to):
    """Return phonograms taught up to this lesson, grouped by review set."""
    taught_order = list(PHONOGRAMS.keys())  # order: a,d,g,c,o,qu,s,t,i,p,u,j,r,n,m,e,l,b,h,k,f,v,w,x,y,z
    taught = taught_order[:all_up_to]
    if not taught:
        return []
    # Group into sets of ~6
    groups = []
    for i in range(0, len(taught), 6):
        groups.append(taught[i:i+6])
    return groups

def known_phonograms(lesson_num, all_up_to):
    """Comma-separated list of phonograms known up to this lesson."""
    taught_order = list(PHONOGRAMS.keys())
    taught = taught_order[:all_up_to]
    return ", ".join(taught) if taught else "(none yet — today's is your first!)"

def spelling_words_for(phonogram, all_up_to=0):
    """Return 3 CVC-friendly words using the given phonogram for Stage 1 spelling analysis.
    Uses 'at' style analysis where the teacher guides for consonants not yet taught."""
    words = {
        "a": [("at", "a (/ă/), t (/t/)", "Short vowel — closed syllable", "/ăt/"),
              ("am", "a (/ă/), m (/m/)", "Short vowel — closed syllable", "/ăm/"),
              ("an", "a (/ă/), n (/n/)", "Short vowel — closed syllable", "/ăn/")],
        "d": [("ad", "a (/ă/), d (/d/)", "Short vowel — closed syllable", "/ăd/"),
              ("dad", "d (/d/), a (/ă/), d (/d/)", "Short vowel — closed syllable", "/dăd/"),
              ("add", "a (/ă/), d (/d/), d (/d/)", "Short vowel — closed syllable", "/ăd/")],
        "g": [("ag", "a (/ă/), g (/g/)", "Short vowel — closed syllable", "/ăg/"),
              ("gad", "g (/g/), a (/ă/), d (/d/)", "Short vowel — closed syllable", "/găd/"),
              ("dad", "d (/d/), a (/ă/), d (/d/)", "Short vowel — closed syllable", "/dăd/")],
        "c": [("cat", "c (/k/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/kăt/"),
              ("cad", "c (/k/), a (/ă/), d (/d/)", "Short vowel — closed syllable", "/kăd/"),
              ("cot", "c (/k/), o (/ŏ/), t (/t/)", "Short vowel — closed syllable", "/kŏt/")],
        "o": [("on", "o (/ŏ/), n (/n/)", "Short vowel — closed syllable", "/ŏn/"),
              ("odd", "o (/ŏ/), d (/d/), d (/d/)", "Short vowel — closed syllable", "/ŏd/"),
              ("got", "g (/g/), o (/ŏ/), t (/t/)", "Short vowel — closed syllable", "/gŏt/")],
        "qu": [("quit", "qu (/kw/), i (/ĭ/), t (/t/)", "Rule 11: Q needs U", "/kwĭt/"),
               ("quack", "qu (/kw/), a (/ă/), ck (/k/)", "Rule 11: Q needs U", "/kwăk/"),
               ("quilt", "qu (/kw/), i (/ĭ/), l (/l/), t (/t/)", "Rule 11: Q needs U", "/kwĭlt/")],
        "s": [("sat", "s (/s/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/săt/"),
              ("sad", "s (/s/), a (/ă/), d (/d/)", "Short vowel — closed syllable", "/săd/"),
              ("sag", "s (/s/), a (/ă/), g (/g/)", "Short vowel — closed syllable", "/săg/")],
        "t": [("tag", "t (/t/), a (/ă/), g (/g/)", "Short vowel — closed syllable", "/tăg/"),
              ("top", "t (/t/), o (/ŏ/), p (/p/)", "Short vowel — closed syllable", "/tŏp/"),
              ("at", "a (/ă/), t (/t/)", "Short vowel — closed syllable", "/ăt/")],
        "i": [("it", "i (/ĭ/), t (/t/)", "Short vowel — closed syllable", "/ĭt/"),
              ("sit", "s (/s/), i (/ĭ/), t (/t/)", "Short vowel — closed syllable", "/sĭt/"),
              ("dig", "d (/d/), i (/ĭ/), g (/g/)", "Short vowel — closed syllable", "/dĭg/")],
        "p": [("pat", "p (/p/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/păt/"),
              ("pot", "p (/p/), o (/ŏ/), t (/t/)", "Short vowel — closed syllable", "/pŏt/"),
              ("pip", "p (/p/), i (/ĭ/), p (/p/)", "Short vowel — closed syllable", "/pĭp/")],
        "u": [("up", "u (/ŭ/), p (/p/)", "Short vowel — closed syllable", "/ŭp/"),
              ("cut", "c (/k/), u (/ŭ/), t (/t/)", "Short vowel — closed syllable", "/kŭt/"),
              ("sun", "s (/s/), u (/ŭ/), n (/n/)", "Short vowel — closed syllable", "/sŭn/")],
        "j": [("jam", "j (/j/), a (/ă/), m (/m/)", "Short vowel — closed syllable", "/jăm/"),
              ("jog", "j (/j/), o (/ŏ/), g (/g/)", "Short vowel — closed syllable", "/jŏg/"),
              ("jug", "j (/j/), u (/ŭ/), g (/g/)", "Short vowel — closed syllable", "/jŭg/")],
        "r": [("rat", "r (/r/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/răt/"),
              ("rug", "r (/r/), u (/ŭ/), g (/g/)", "Short vowel — closed syllable", "/rŭg/"),
              ("ran", "r (/r/), a (/ă/), n (/n/)", "Short vowel — closed syllable", "/răn/")],
        "n": [("nap", "n (/n/), a (/ă/), p (/p/)", "Short vowel — closed syllable", "/năp/"),
              ("not", "n (/n/), o (/ŏ/), t (/t/)", "Short vowel — closed syllable", "/nŏt/"),
              ("net", "n (/n/), e (/ĕ/), t (/t/)", "Short vowel — closed syllable", "/nĕt/")],
        "m": [("map", "m (/m/), a (/ă/), p (/p/)", "Short vowel — closed syllable", "/măp/"),
              ("mom", "m (/m/), o (/ŏ/), m (/m/)", "Short vowel — closed syllable", "/mŏm/"),
              ("man", "m (/m/), a (/ă/), n (/n/)", "Short vowel — closed syllable", "/măn/")],
        "e": [("ed", "e (/ĕ/), d (/d/)", "Short vowel — closed syllable", "/ĕd/"),
              ("pet", "p (/p/), e (/ĕ/), t (/t/)", "Short vowel — closed syllable", "/pĕt/"),
              ("red", "r (/r/), e (/ĕ/), d (/d/)", "Short vowel — closed syllable", "/rĕd/")],
        "l": [("lap", "l (/l/), a (/ă/), p (/p/)", "Short vowel — closed syllable", "/lăp/"),
              ("leg", "l (/l/), e (/ĕ/), g (/g/)", "Short vowel — closed syllable", "/lĕg/"),
              ("lot", "l (/l/), o (/ŏ/), t (/t/)", "Short vowel — closed syllable", "/lŏt/")],
        "b": [("bat", "b (/b/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/băt/"),
              ("big", "b (/b/), i (/ĭ/), g (/g/)", "Short vowel — closed syllable", "/bĭg/"),
              ("bed", "b (/b/), e (/ĕ/), d (/d/)", "Short vowel — closed syllable", "/bĕd/")],
        "h": [("hat", "h (/h/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/hăt/"),
              ("hot", "h (/h/), o (/ŏ/), t (/t/)", "Short vowel — closed syllable", "/hŏt/"),
              ("him", "h (/h/), i (/ĭ/), m (/m/)", "Short vowel — closed syllable", "/hĭm/")],
        "k": [("kit", "k (/k/), i (/ĭ/), t (/t/)", "Short vowel — closed syllable", "/kĭt/"),
              ("kin", "k (/k/), i (/ĭ/), n (/n/)", "Short vowel — closed syllable", "/kĭn/"),
              ("kid", "k (/k/), i (/ĭ/), d (/d/)", "Short vowel — closed syllable", "/kĭd/")],
        "f": [("fan", "f (/f/), a (/ă/), n (/n/)", "Short vowel — closed syllable", "/făn/"),
              ("fin", "f (/f/), i (/ĭ/), n (/n/)", "Short vowel — closed syllable", "/fĭn/"),
              ("fun", "f (/f/), u (/ŭ/), n (/n/)", "Short vowel — closed syllable", "/fŭn/")],
        "v": [("van", "v (/v/), a (/ă/), n (/n/)", "Short vowel — closed syllable", "/văn/"),
              ("vet", "v (/v/), e (/ĕ/), t (/t/)", "Short vowel — closed syllable", "/vĕt/"),
              ("vat", "v (/v/), a (/ă/), t (/t/)", "Short vowel — closed syllable", "/văt/")],
        "w": [("wet", "w (/w/), e (/ĕ/), t (/t/)", "Short vowel — closed syllable", "/wĕt/"),
              ("win", "w (/w/), i (/ĭ/), n (/n/)", "Short vowel — closed syllable", "/wĭn/"),
              ("wag", "w (/w/), a (/ă/), g (/g/)", "Short vowel — closed syllable", "/wăg/")],
        "x": [("ax", "a (/ă/), x (/ks/)", "Short vowel — closed syllable", "/ăks/"),
              ("ox", "o (/ŏ/), x (/ks/)", "Short vowel — closed syllable", "/ŏks/"),
              ("fix", "f (/f/), i (/ĭ/), x (/ks/)", "Short vowel — closed syllable", "/fĭks/")],
        "y": [("yes", "y (/y/), e (/ĕ/), s (/s/)", "Short vowel — closed syllable", "/yĕs/"),
              ("yet", "y (/y/), e (/ĕ/), t (/t/)", "Short vowel — closed syllable", "/yĕt/"),
              ("yip", "y (/y/), i (/ĭ/), p (/p/)", "Short vowel — closed syllable", "/yĭp/")],
        "z": [("zip", "z (/z/), i (/ĭ/), p (/p/)", "Short vowel — closed syllable", "/zĭp/"),
              ("zap", "z (/z/), a (/ă/), p (/p/)", "Short vowel — closed syllable", "/zăp/"),
              ("zig", "z (/z/), i (/ĭ/), g (/g/)", "Short vowel — closed syllable", "/zĭg/")],
    }
    return words.get(phonogram, [("—", "—", "—", "—")])

def get_read_words(phonogram, limit=6):
    """Reading practice words using the phonogram."""
    words = {
        "a": ["at", "am", "an", "ad", "ag"],
        "d": ["ad", "dad", "add", "sad", "mad"],
        "g": ["ag", "gad", "tag", "bag", "rag"],
        "c": ["cat", "cad", "cot", "cop", "cap"],
        "o": ["on", "odd", "got", "not", "dot"],
        "qu": ["quit", "quiz", "quack"],
        "s": ["sat", "sad", "sag", "sit", "set"],
        "t": ["tag", "top", "at", "it", "tap"],
        "i": ["it", "sit", "dig", "in", "if"],
        "p": ["pat", "pot", "pip", "pan", "pop"],
        "u": ["up", "cut", "sun", "fun", "run"],
        "j": ["jam", "jog", "jug", "jet", "job"],
        "r": ["rat", "rug", "ran", "red", "rip"],
        "n": ["nap", "not", "net", "nut", "nip"],
        "m": ["map", "mom", "man", "mat", "mud"],
        "e": ["ed", "pet", "red", "get", "set"],
        "l": ["lap", "leg", "lot", "lip", "log"],
        "b": ["bat", "big", "bed", "bug", "bag"],
        "h": ["hat", "hot", "him", "hop", "hum"],
        "k": ["kit", "kin", "kid", "kiss", "king"],
        "f": ["fan", "fin", "fun", "fit", "fat"],
        "v": ["van", "vet", "vat", "vim", "vig"],
        "w": ["wet", "win", "wag", "wit", "web"],
        "x": ["ax", "ox", "fix", "box", "mix"],
        "y": ["yes", "yet", "yip", "yam", "yell"],
        "z": ["zip", "zap", "zig", "zag", "zed"],
    }
    return words.get(phonogram, ["—"])

# ── TEMPLATES ───────────────────────────────────────────────────────

PHONOGRAM_REVIEW_HEADER = """## Warm-Up: Phonogram Flash Review

> Adult: Flash previously taught phonogram cards. Child says ALL sounds within 2 seconds. Mark any slow ones for extra practice.

| Phonograms to review |
|----------------------|
| {review_phonograms} |

"""

PHONOGRAM_INTRO_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 1** · Lesson {lesson_num} · phonogram-intro

---

{review_section}
---

## New Learning: Your New Phonogram — {pg}

### The Phonogram **{pg}**

<div class="phonogram">{pg}</div>

**{pg}** says {sound_count} sound{plural}: {sounds}

| Sound | Example Words |
|-------|--------------|
{example_rows}

> **Important:** Always teach ALL sounds from the start. Never teach "{pg} says /{first_sound}/" and add more later. The child must know that **{pg}** can say {sound_count} different thing{plural}.

{rule_note}
### How to Write **{pg}**

{writing_steps}

> Write **{pg}** three times on your whiteboard or in a sand tray. Say "{sounds}" each time you write it.

{vowel_note}
---

## Spelling Analysis

Follow the 5-step routine for each word:

1. **Hear & Say** — Adult says the word, uses it in a sentence. Child repeats.
2. **Segment** — Child breaks the word into individual sounds. Adult holds up fingers (1 finger = 1-letter phonogram).
3. **Write** — Child writes the word while sounding it out.
4. **Analyze** — Underline multi-letter phonograms. Name any spelling rules.
5. **Read** — Child reads the word sound by sound, then blends.

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{word_rows}

---

## Reading Practice

Read these words sound by sound, then blend:

> {read_words}

---

## Handwriting Practice

Write each letter once. Say its sounds as you write.

| {pg} | {pg} | {pg} | {pg} | {pg} |
|---|---|---|---|---|

---

## Quick Check

1. What did you learn today? *(A new phonogram: {pg})*
2. What sounds does **{pg}** say? *({sounds})*
3. Write the word "{first_word}" from dictation.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Flash your new **{pg}** card 5 times. Find **{pg}** in a book or on a sign.*

{teacher_script}
"""

PA_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 1** · Lesson {lesson_num} · phonemic-awareness

---

## Warm-Up: Listening Game

> Adult: Say these directions. Child listens and follows along.

{activity_description}

---

## Activity 1: {activity_1_title}

{activity_1_body}

---

## Activity 2: {activity_2_title}

{activity_2_body}

---

## Activity 3: {activity_3_title}

{activity_3_body}

---

## Let's Move!

{movement_activity}

---

## Quick Check

{quick_check}

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: {home_practice}*
"""

REVIEW_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 1** · Lesson {lesson_num} · review

---

## Warm-Up: Fast Flash

> Adult: Flash ALL phonograms from Group {group_num}. Child says ALL sounds for each within 2 seconds. Go faster each round!

| Phonograms to review |
|----------------------|
| {review_phonograms} |

---

## Game 1: Phonogram Hunt

Adult says a sound (like /ă/). Child finds the phonogram card that makes that sound from the pile. Do this for all sounds in Group {group_num}.

**Can you find the phonogram that says...**

{sound_hunt_list}

---

## Game 2: Write the Sound

Adult says a sound. Child writes the phonogram on the whiteboard. No peeking at the cards!

> Write the phonogram for: {write_sounds}

---

## Game 3: Mixed-Up Match

Spread all Group {group_num} cards face-up. Adult says a word. Child touches the card for the FIRST sound in that word.

| Word | First Sound | Correct Card |
|------|------------|--------------|
{match_rows}

---

## Bonus: Speed Round!

Can you say ALL {count} phonograms from Group {group_num} with their sounds in under 30 seconds? Try it!

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Play the "Phonogram Hunt" game with a family member!*
"""

ASSESSMENT_TEMPLATE = """# Lesson {lesson_num}: Stage 1 Mastery Check

**Stage 1** · Lesson {lesson_num} · assessment

---

## Assessment Overview

This mastery check verifies the child is ready for Stage 2. The child should demonstrate each skill confidently — not perfectly, but reliably. If any section is weak, revisit those lessons before moving on.

---

## Part 1: Phonogram Sounds

> Flash each a-z phonogram card. Child says ALL sounds in frequency order within 2 seconds.

| Phonogram | Sounds to Say | ✓ / Needs Work |
|-----------|--------------|----------------|
{phonogram_checklist}

**Pass:** {pass_count} / 26 phonograms correct

> Passing score: 22+ / 26. Mark any slow/unconfident phonograms for review.

---

## Part 2: Write Phonograms from Sounds

> Adult says a sound. Child writes the phonogram. Check lowercase letter formation.

| Sound | Letter | ✓ / Needs Work |
|-------|--------|----------------|
{write_checklist}

---

## Part 3: Blending (Oral)

> Adult says sounds. Child blends into a word. No writing — spoken only.

| Sounds | ✓ / Needs Work |
|--------|----------------|
{blend_checklist}

---

## Part 4: Segmenting (Oral)

> Adult says a word. Child segments into individual sounds. Use the "finger method" — hold up one finger per sound.

| Word | ✓ / Needs Work |
|------|----------------|
{segment_checklist}

---

## Part 5: Sound Identification

> Adult says a word. Identify the first, last, or middle sound.

| Word | Find | Answer | ✓ / Needs Work |
|------|------|--------|----------------|
{sound_id_checklist}

---

## Results

| Section | Score | Pass? |
|---------|-------|-------|
| Phonogram Sounds | {sound_score}/26 | {sound_pass} |
| Write Phonograms | {write_score}/16 | {write_pass} |
| Blending | {blend_score}/5 | {blend_pass} |
| Segmenting | {seg_score}/5 | {seg_pass} |
| Sound Identification | {id_score}/6 | {id_pass} |

**Overall:** {overall}

---

## Next Steps

{next_steps}

---

*You completed Stage 1! Celebrate with a special reading together.*
"""

SPECIAL_VOWELS_TEMPLATE = """# Lesson {lesson_num}: Meet the Vowels

**Stage 1** · Lesson {lesson_num} · vowel-concept

---

## Warm-Up: Phonogram Flash Review

> Flash all 26 a-z phonograms. Quick review — focus on speed!

| Phonograms to review |
|----------------------|
| All 26: a, d, g, c, o, qu, s, t, i, p, u, j, r, n, m, e, l, b, h, k, f, v, w, x, y, z |

---

## New Learning: What Is a Vowel?

### Sing It or Block It?

You have learned 26 phonograms. Some of them are **vowels** and some are **consonants**. Here is how to tell the difference:

- **Vowels:** You can SING them. Your mouth is open. Your lips, tongue, and teeth don't block the sound. You can control how loud or soft they are.
- **Consonants:** Sounds blocked by your lips, tongue, or teeth. You usually can't sing them or control their volume.

### Let's Test Each Sound

Adult says each sound below. Child puts a hand on their throat and says it too. Decide: vowel or consonant?

| Sound | Vowel or Consonant? | Why? |
|-------|--------------------|------|
| /ă/ | Vowel | Mouth open, can sing it |
| /b/ | Consonant | Lips block the sound |
| /k/ | Consonant | Tongue blocks at back of mouth |
| /d/ | Consonant | Tongue taps behind teeth |
| /ĕ/ | Vowel | Mouth open, can sing it |
| /f/ | Consonant | Teeth on lip block air |
| /g/ | Consonant | Tongue blocks at back of mouth |
| /h/ | Consonant | Breath released — no singing! |
| /ĭ/ | Vowel | Mouth open, can sing it |
| /j/ | Consonant | Tongue blocks the sound |
| /l/ | Consonant | Tongue tip touches roof |
| /m/ | Consonant | Lips together — hum through nose |
| /n/ | Consonant | Tongue tip touches roof — hum through nose |
| /ŏ/ | Vowel | Mouth open, can sing it |
| /p/ | Consonant | Lips pop open |
| /r/ | Consonant | Tongue curls back |
| /s/ | Consonant | Tongue hisses near teeth |
| /t/ | Consonant | Tongue taps behind teeth |
| /ŭ/ | Vowel | Mouth open, can sing it |
| /v/ | Consonant | Teeth on lip with buzz |
| /w/ | Consonant | Lips round then release |
| /ks/ | Consonant | Two sounds — both blocked |
| /y/ | Consonant or Vowel! | /y/ sound is consonant; its other 3 sounds are vowels |
| /z/ | Consonant | Tongue buzzes near teeth |

### Count the Vowels

How many pure vowel sounds did we find? **5: a, e, i, o, u**

**Y** is special — it can be a vowel or a consonant:
- /y/ (as in *yes*) — consonant (tongue blocks)
- /ĭ/ (as in *gym*) — vowel
- /ī/ (as in *by*) — vowel
- /ē/ (as in *baby*) — vowel

Three of Y's four sounds are vowels!

---

## Spelling Practice

| Word | Vowels in This Word | How Do You Know? |
|------|--------------------|------------------|
{spelling_rows}

---

## Quick Check

1. What is a vowel? *(A sound you can sing; mouth is open; lips/tongue/teeth don't block it)*
2. What is a consonant? *(A sound blocked by lips, tongue, or teeth)*
3. Name all the vowels. *(A, E, I, O, U — and sometimes Y)*
4. Which letter can be BOTH a vowel and a consonant? *(Y)*

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find 5 things in the house. Say their names. Count the vowels in each word!*
"""

SPECIAL_HANDWRITING_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 1** · Lesson {lesson_num} · handwriting

---

## Warm-Up: Finger Exercises

{hand_warmup}

---

## {letter_group} Letters

{letter_list}

### How to Write Each Letter

{writing_instructions}

---

## Practice Page

Write each letter 3 times on your whiteboard. Say its sounds as you write.

{letter_grid}

---

## Letter Hunt

Find these letters in a book or on a sign. Tell an adult what sounds they can make.

{letter_hunt}

---

## Challenge: Write Your Name

Can you write your first name? Sound it out. Use the letters you know!

---

## Quick Check

1. Which letter group is easiest for you to write?
2. Which letter needs more practice?
3. Write the phonogram for /{challenge_sound}/ from dictation.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Write one row of each letter group letter in a notebook.*
"""

SPECIAL_PA_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 1** · Lesson {lesson_num} · phonemic-awareness

---

## Warm-Up: Phonogram Flash Review

> Flash known phonograms. Child says ALL sounds within 2 seconds.

| Phonograms to review |
|----------------------|
| {review_phonograms} |

---

## Activity 1: {activity_1_title}

{activity_1_body}

---

## Activity 2: {activity_2_title}

{activity_2_body}

---

## Activity 3: {activity_3_title}

{activity_3_body}

---

## Let's Move!

{movement_activity}

---

## Quick Check

{quick_check}

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: {home_practice}*
"""

# ── BUILDERS ────────────────────────────────────────────────────────

def build_phonogram_intro(num, pg_data, next_num, next_title):
    pg = pg_data["pg"]
    pgd = PHONOGRAMS[pg]
    sounds = pgd["sounds"]
    first_sound = sounds.split("/")[1].split("/")[0]
    sc = pgd["sound_count"]
    plural = "s" if sc > 1 else ""
    examples = pgd["examples"]
    example_rows = "\n".join(f"| /{e[0]}/ | {e[1]} |" for e in examples)
    writing_steps = "\n".join(f"{i+1}. {s}" for i, s in enumerate(pgd["writing"]))

    # Rule note
    rule_note = ""
    if "rule" in pgd:
        rule_note = f"\n> **Spelling Rule:** {pgd['rule']}\n"
    elif pg == "c":
        rule_note = "\n> **Tip:** C says /k/ most often and /s/ less often. The first sound (/k/) is the most common.\n"
    elif pg == "g":
        rule_note = "\n> **Tip:** G says /g/ most often and /j/ less often. G usually says /j/ only before E, I, or Y.\n"

    # Vowel note
    vowel_note = ""
    if pgd["vowel"]:
        vowel_note = f"\n### Vowel or Consonant?\n\n**{pg}** is a **vowel**. You can sing it! Your mouth is open. Your lips, tongue, and teeth don't block the sound.\n"
    else:
        vowel_note = f"\n### Vowel or Consonant?\n\n**{pg}** is a **consonant**. The sound is blocked by your tongue or lips. Try saying /{first_sound}/ — what blocks the air?\n"

    # Spelling words
    words = spelling_words_for(pg)
    word_rows = "\n".join(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in words)

    # Read words
    read_words = " &nbsp;&nbsp; ".join(get_read_words(pg))

    # Review phonograms
    taught_order = list(PHONOGRAMS.keys())
    idx = taught_order.index(pg)
    known = taught_order[:idx]
    review_phonograms = ", ".join(known) if known else "(This is your first phonogram lesson! No review today.)"
    if not known:
        review_section = """## Warm-Up: Phonogram Flash Review

> Adult: Flash previously taught phonogram cards. Child says ALL sounds within 2 seconds.

| Phonograms to review |
|----------------------|
| (This is your first phonogram lesson! Skip review today.) |

"""
    else:
        review_section = PHONOGRAM_REVIEW_HEADER.format(review_phonograms=review_phonograms)

    return PHONOGRAM_INTRO_TEMPLATE.format(
        lesson_num=num,
        title=f"Phonogram {pg}",
        pg=pg,
        sounds=sounds,
        sound_count=sc,
        plural=plural,
        first_sound=first_sound,
        example_rows=example_rows,
        writing_steps=writing_steps,
        rule_note=rule_note,
        vowel_note=vowel_note,
        word_rows=word_rows,
        read_words=read_words,
        first_word=words[0][0] if words else pg,
        next_num=next_num,
        next_title=next_title,
        review_section=review_section,
        teacher_script=format_phonogram_script(pg, sounds),
    )


def build_pa(num, slug, title, desc, activities, movement, quick_check, home_practice, next_num, next_title):
    return PA_TEMPLATE.format(
        lesson_num=num,
        title=title,
        activity_description=desc,
        activity_1_title=activities[0][0],
        activity_1_body=activities[0][1],
        activity_2_title=activities[1][0],
        activity_2_body=activities[1][1],
        activity_3_title=activities[2][0],
        activity_3_body=activities[2][1],
        movement_activity=movement,
        quick_check=quick_check,
        home_practice=home_practice,
        next_num=next_num,
        next_title=next_title,
        teacher_script="",
    )


def build_pa_with_review(num, slug, title, desc, activities, movement, quick_check, home_practice,
                         review_pgs, next_num, next_title):
    review_str = ", ".join(review_pgs)
    return SPECIAL_PA_TEMPLATE.format(
        lesson_num=num,
        title=title,
        review_phonograms=review_str,
        activity_1_title=activities[0][0],
        activity_1_body=activities[0][1],
        activity_2_title=activities[1][0],
        activity_2_body=activities[2][1],
        activity_3_title=activities[3][0] if len(activities) > 3 else activities[2][0],
        activity_3_body=activities[3][1] if len(activities) > 3 else activities[2][1],
        movement_activity=movement,
        quick_check=quick_check,
        home_practice=home_practice,
        next_num=next_num,
        next_title=next_title,
        teacher_script="",
    )


def build_review(num, group_num, group_pgs, all_pg_list, next_num, next_title):
    count = len(group_pgs)
    sound_hunt = "\n".join(f"- Find the phonogram that says **{PHONOGRAMS[p]['sounds']}**" for p in group_pgs)
    
    # Write sounds: pick the first sound of each
    write_sounds = ", ".join(PHONOGRAMS[p]["sounds"].split()[0] for p in group_pgs)
    
    # Match rows: random words with first sounds from group_pgs
    match_words = {
        "a": ("apple", "/ă/", "a"),
        "d": ("dog", "/d/", "d"),
        "g": ("goat", "/g/", "g"),
        "c": ("cat", "/k/", "c"),
        "o": ("octopus", "/ŏ/", "o"),
        "qu": ("queen", "/kw/", "qu"),
        "s": ("sun", "/s/", "s"),
        "t": ("top", "/t/", "t"),
        "i": ("igloo", "/ĭ/", "i"),
        "p": ("pig", "/p/", "p"),
        "u": ("umbrella", "/ŭ/", "u"),
        "j": ("jump", "/j/", "j"),
        "r": ("red", "/r/", "r"),
        "n": ("nest", "/n/", "n"),
        "m": ("man", "/m/", "m"),
        "e": ("egg", "/ĕ/", "e"),
        "l": ("leg", "/l/", "l"),
        "b": ("bat", "/b/", "b"),
        "h": ("hat", "/h/", "h"),
        "k": ("kite", "/k/", "k"),
        "f": ("fish", "/f/", "f"),
        "v": ("van", "/v/", "v"),
        "w": ("wet", "/w/", "w"),
        "x": ("box", "/ks/", "x"),
        "y": ("yes", "/y/", "y"),
        "z": ("zipper", "/z/", "z"),
    }
    match_rows = "\n".join(
        f"| {match_words[p][0]} | {match_words[p][1]} | {match_words[p][2]} |"
        for p in group_pgs if p in match_words
    )

    return REVIEW_TEMPLATE.format(
        lesson_num=num,
        title=title_for(num, all_pg_list),
        group_num=group_num,
        review_phonograms=", ".join(group_pgs),
        sound_hunt_list=sound_hunt,
        write_sounds=write_sounds,
        count=count,
        match_rows=match_rows,
        next_num=next_num,
        next_title=next_title,
        teacher_script="",
    )


def title_for(num, pg_list):
    """Look up title from catalog."""
    titles = {
        1: "Sounds Around Us", 2: "Voiced and Unvoiced Sounds",
        3: "Blending Compound Words", 4: "Blending Syllables",
        5: "Onset and Rime", 6: "Blending CVC Words",
        7: "Segmenting CVC Words", 8: "First Sounds in Words",
        9: "Phonogram a", 10: "Phonogram d", 11: "Phonogram g",
        12: "Phonogram c", 13: "Phonogram o", 14: "Phonogram qu",
        15: "Review: Group 1 Phonograms",
        16: "Phonogram s", 17: "Phonogram t", 18: "Phonogram i",
        19: "Phonogram p", 20: "Phonogram u", 21: "Phonogram j",
        22: "Review: Group 2 Phonograms",
        23: "Last Sounds in Words",
        24: "Phonogram r", 25: "Phonogram n", 26: "Phonogram m",
        27: "Phonogram e", 28: "Phonogram l", 29: "Phonogram b",
        30: "Review: Group 3 Phonograms",
        31: "Middle Sounds in Words",
        32: "Phonogram h", 33: "Phonogram k", 34: "Phonogram f",
        35: "Phonogram v", 36: "Phonogram w", 37: "Phonogram x",
        38: "Review: Group 4 Phonograms",
        39: "Phonogram y", 40: "Phonogram z",
        41: "Sound Swapping Game", 42: "Meet the Vowels",
        43: "All 26 Phonograms Review",
        44: "Blending with Consonant Blends", 45: "Blending Two-Syllable Words",
        46: "Handwriting: Clockface Letters", 47: "Handwriting: Straight-start Letters",
        48: "Stage 1 Mastery Check",
    }
    return titles.get(num, f"Lesson {num}")


def next_for(num):
    """Return (next_num, next_title)"""
    n = num + 1
    return n, title_for(n, [])


# ── MAIN: GENERATE ALL LESSONS ──────────────────────────────────────

def generate_all():
    taught_order = list(PHONOGRAMS.keys())
    pg_index = 0

    # ── Lessons 1-8: Phonemic Awareness ──

    yield 1, build_pa(1, "pa-01", "Sounds Around Us",
        "Close your eyes for one minute. What do you hear? Birds? A car? A clock ticking?",
        [
            ("Guess the Sound", 
             "Adult makes a sound behind their back (clap, tap pencil, crinkle paper, snap fingers, whistle). "
             "Child closes eyes and guesses what made the sound.\n\n"
             "Try these sounds:\n- Clap hands\n- Tap a pencil on a table\n- Crinkle a piece of paper\n- Snap your fingers\n- Hum a note\n- Stamp your foot\n- Ring a bell (if you have one)\n- Close a book"),
            ("Loud or Soft?",
             "Adult makes the same sound at different volumes. Child says 'loud' or 'soft.'\n\n"
             "Switch roles! Child makes sounds and adult guesses loud or soft."),
            ("Sound Walk",
             "Walk around the house together. Stop in each room and listen for 15 seconds. "
             "Name every sound you hear. Count them up!\n\n"
             "Which room had the most sounds? Which room was the quietest?"),
        ],
        "Stand up and be a sound machine! Adult names an animal. Child makes its sound. "
        "Switch — child names the animal and adult makes the sound. See who can do 10 animals in a row!",
        "1. What was the loudest sound you heard today?\n"
        "2. What was the softest sound?\n"
        "3. Close your eyes right now. What do you hear?",
        "Close your eyes before bed tonight. Name 5 sounds you hear.",
        2, title_for(2, []))

    yield 2, build_pa(2, "pa-02", "Voiced and Unvoiced Sounds",
        "Put your hand on your throat. Say /z/ like a buzzing bee. Feel the buzz? That's your voice! Now say /s/ like a snake. No buzz!",
        [
            ("Voice On, Voice Off",
             "Adult says these sounds one at a time. Child puts a hand on their throat and says 'buzzing' if they feel vibration, 'quiet' if they don't.\n\n"
             "/z/ (buzzing) — /s/ (quiet)\n"
             "/v/ (buzzing) — /f/ (quiet)\n"
             "/b/ (buzzing) — /p/ (quiet)\n"
             "/d/ (buzzing) — /t/ (quiet)\n"
             "/g/ (buzzing) — /k/ (quiet)\n"
             "/th/ as in *this* (buzzing) — /th/ as in *thin* (quiet)\n\n"
             "Pairs like these are called 'voiced' (buzzing) and 'unvoiced' (quiet)."),
            ("Who Am I?",
             "Adult says either a voiced or unvoiced sound. Child guesses which one it is: 'voiced' or 'unvoiced' — then makes the opposite!\n\n"
             "Mix it up with these sounds: /z/ /s/ /v/ /f/ /b/ /p/ /d/ /t/"),
            ("Throat Detective",
             "Adult says everyday words slowly. Child feels their throat for each sound. "
             "Which sounds buzz? Which don't?\n\n"
             "Words to try: mop, zip, fan, big, sit, dog, hat, van"),
        ],
        "Be a buzzing bee! Fly around the room saying /z/ /z/ /z/. Then be a quiet snake — slither and say /s/ /s/ /s/. "
        "Switch back and forth: BEE /z/ ... SNAKE /s/ ... BEE /z/ ... SNAKE /s/!",
        "1. Put your hand on your throat. Say /b/. Is it voiced or unvoiced? *(Voiced — it buzzes!)*\n"
        "2. Say /p/. Is it voiced or unvoiced? *(Unvoiced — no buzz)*\n"
        "3. /b/ and /p/ are a pair. What's different about them? *(Your voice is ON for /b/ and OFF for /p/)*",
        "Play 'Voice On, Voice Off' with a family member at dinner.",
        3, title_for(3, []))

    yield 3, build_pa(3, "pa-03", "Blending Compound Words",
        "I'm going to say two small words with a pause. You put them together into one big word! Ready?",
        [
            ("Compound Detective",
             "Adult says: 'What word do you get when you put *cup* and *cake* together?' Child says: 'cupcake!'\n\n"
             "Try these:\n- cup ... cake → cupcake\n- sun ... shine → sunshine\n- rain ... bow → rainbow\n- pop ... corn → popcorn\n- foot ... ball → football\n- pan ... cake → pancake\n- bed ... room → bedroom\n- air ... plane → airplane\n- snow ... man → snowman\n- tooth ... brush → toothbrush"),
            ("Break It Apart",
             "Now go backwards! Adult says the whole compound word. Child breaks it into two parts.\n\n"
             "Try:\n- doghouse → dog + house\n- mailbox → mail + box\n- sailboat → sail + boat\n- bluebird → blue + bird\n- sunset → sun + set\n- backpack → back + pack\n- lunchbox → lunch + box"),
            ("Make Your Own",
             "Adult says: 'What if we put DOG and HOUSE together? What would a doghouse be?'\n"
             "Child thinks of new compound words. They don't have to be real — this is a game!\n\n"
             "Funny combos: cat + fish = catfish (real!), cow + bird = cowbird (real!), fish + cake = fishcake?!"),
        ],
        "Stand up! Adult says a compound word. If it's real, jump once. If it's made up, spin around. "
        "Go fast: cupcake (jump!), cowcake (spin!), rainbow (jump!), rainmouse (spin!)",
        "1. What two words make 'sunshine'? *(sun + shine)*\n"
        "2. What new word do you get from 'bed' + 'room'? *(bedroom)*\n"
        "3. Make up a silly compound word! What two words did you use?",
        "Look around the house. How many compound words can you find? (bathroom, doorbell, bookshelf, etc.)",
        4, title_for(4, []))

    yield 4, build_pa(4, "pa-04", "Blending Syllables",
        "Now we'll blend bigger word parts called syllables. These aren't whole words by themselves, but when we put them together, they make a word!",
        [
            ("Clap the Parts",
             "Adult says a word in slow syllables. Child blends them into one word.\n\n"
             "Start with 2 syllables:\n- kin ... der → (no, that's part of) kin-der-gar-ten → kindergarten\n"
             "Try these 2-syllable words:\n- ta ... ble → table\n- pen ... cil → pencil\n- pa ... per → paper\n- kit ... ten → kitten\n- hap ... py → happy\n- win ... dow → window"),
            ("Three-Part Challenge",
             "Now try 3 syllables!\n\n"
             "- el ... e ... phant → elephant\n- ba ... na ... na → banana\n- to ... ma ... to → tomato\n- bi ... cy ... cle → bicycle\n- oc ... to ... pus → octopus\n- um ... brel ... la → umbrella"),
            ("Syllable Count",
             "Adult says a word at normal speed. Child claps once for each syllable.\n\n"
             "1 clap: dog, cat, fish, sun, bed\n"
             "2 claps: ta-ble, pen-cil, kit-ten\n"
             "3 claps: el-e-phant, ba-na-na\n"
             "4 claps: kin-der-gar-ten"),
        ],
        "March around the room! Each step = one syllable. Adult calls out words, child marches the syllables. "
        "'El' (step) 'e' (step) 'phant' (step)!",
        "1. Clap 'water.' How many syllables? *(2: wa-ter)*\n"
        "2. Clap 'butterfly.' How many? *(3: but-ter-fly)*\n"
        "3. Say a word with 2 syllables. Say a different word with 3 syllables.",
        "At meals, clap the syllables in food words: piz-za (2), spa-ghet-ti (3), milk (1).",
        5, title_for(5, []))

    yield 5, build_pa(5, "pa-05", "Onset and Rime",
        "Today we're going to play with the beginning sound of a word (the 'onset') and the rest of the word (the 'rime'). Ready?",
        [
            ("First Sound, Rest of the Word",
             "Adult says: '/k/ ... /at/'. Put them together: 'cat!'\n\n"
             "Try these:\n- /k/ ... /at/ → cat\n- /h/ ... /at/ → hat\n- /b/ ... /at/ → bat\n- /f/ ... /at/ → fat\n- /m/ ... /at/ → mat\n- /r/ ... /at/ → rat\n- /s/ ... /at/ → sat\n\n"
             "Notice: all these words end with /at/! The only thing that changes is the first sound."),
            ("Rhyme Time",
             "Adult says a word family ending. Child adds different first sounds to make real words.\n\n"
             "/at/ family: c-at, h-at, b-at, f-at, m-at, r-at, s-at, p-at\n"
             "/op/ family: h-op, p-op, t-op, m-op, st-op, dr-op\n"
             "/ig/ family: b-ig, d-ig, p-ig, w-ig, tw-ig, j-ig\n\n"
             "How many real words can you make with /at/?"),
            ("Mystery Word",
             "Adult says a word in onset-rime: '/d/ ... /og/. What word?' Child answers: 'dog!'\n\n"
             "Take turns being the 'mystery word maker' and the guesser."),
        ],
        "Stand in a circle (or just stand up). Adult says an /at/ word. Everyone hops! "
        "Adult says a non-/at/ word. Everyone freezes. Go fast!",
        "1. Put together /f/ + /at/. What word? *(fat)*\n"
        "2. Put together /s/ + /un/. What word? *(sun)*\n"
        "3. What changes when you go from 'cat' to 'hat'? *(Only the first sound!)*",
        "Play 'Mystery Word' in the car. Adult says /p/ ... /ark/ and child guesses 'park!'",
        6, title_for(6, []))

    yield 6, build_pa(6, "pa-06", "Blending CVC Words",
        "Today we put THREE sounds together! /k/ /ă/ /t/ — can you hear the word?",
        [
            ("Three-Sound Blending",
             "Adult says each sound separately with a short pause. Child blends them into a word.\n\n"
             "Start with continuous first sounds (these are easier to blend):\n"
             "- /m/ /ă/ /t/ → mat\n- /s/ /ă/ /t/ → sat\n- /f/ /ă/ /n/ → fan\n- /r/ /ă/ /n/ → ran\n- /n/ /ă/ /p/ → nap\n- /m/ /ŏ/ /m/ → mom\n- /s/ /ŭ/ /n/ → sun\n"
             "\nNow try with stop sounds at the beginning (harder):\n"
             "- /k/ /ă/ /t/ → cat\n- /d/ /ŏ/ /g/ → dog\n- /p/ /ĭ/ /g/ → pig\n- /t/ /ŏ/ /p/ → top"),
            ("Stretch It Out",
             "Adult says a word VERY slowly, stretching each sound. Child says it fast.\n\n"
             "Adult: /sssssssss/ /ăăăăăă/ /tttttttt/ ... Child: 'sat!'\n"
             "This helps the child hear how sounds slide together. Do this for 5-8 words."),
            ("Speed Round",
             "Now go fast! Adult says three sounds quickly. Child blurts the word.\n"
             "Ready? /d/ /o/ /g/ → dog! /b/ /e/ /d/ → bed! /h/ /o/ /p/ → hop!\n"
             "Try 10 rapid-fire blends."),
        ],
        "Adult says three sounds. If they make a real word, child jumps. If they make a nonsense word, child sits down. "
        "/k/ /ă/ /t/ (JUMP — cat is real!) ... /z/ /ŏ/ /b/ (SIT — zob isn't real!)",
        "1. Blend /h/ /ă/ /t/. What word? *(hat)*\n"
        "2. Blend /d/ /ĭ/ /g/. What word? *(dig)*\n"
        "3. Why do we start blending with 'continuous' sounds like /m/ and /s/? *(Because you can stretch them out!)*",
        "Play the blending game while waiting anywhere — the grocery line, the car, the doctor's office.",
        7, title_for(7, []))

    yield 7, build_pa(7, "pa-07", "Segmenting CVC Words",
        "Now we go the other way! I'll say a whole word, and you break it apart into its sounds. This is how we learn to spell!",
        [
            ("Finger Tapping",
             "Adult says a word. Child repeats it, then taps one finger per sound.\n\n"
             "Model: Adult says 'cat.' Holds up 3 fingers. Touch one finger per sound: /k/ /ă/ /t/.\n\n"
             "Child's turn:\n- dog (3 fingers: /d/ /ŏ/ /g/)\n- sit (3 fingers: /s/ /ĭ/ /t/)\n- up (2 fingers: /ŭ/ /p/)\n- hat (3 fingers: /h/ /ă/ /t/)\n- man (3 fingers: /m/ /ă/ /n/)\n- bed (3 fingers: /b/ /ĕ/ /d/)\n- fish (3 fingers: /f/ /ĭ/ /sh/)"),
            ("Count the Sounds",
             "Adult says a word. Child counts the sounds on their fingers.\n\n"
             "2 sounds: am, at, up, in, on, go\n"
             "3 sounds: cat, dog, pig, sun, bed, hat, run, hop\n"
             "4 sounds: stop, frog, clap, skip, hand"),
            ("Sound-by-Sound",
             "Adult says a word. Child says each sound separately, slowly.\n\n"
             "Adult: 'Tell me every sound in *map*.'\n"
             "Child: '/m/ ... /ă/ ... /p/'\n\n"
             "Try: map, net, cup, dig, fog, pen, hug, fit, sad, mop"),
        ],
        "Be a robot! Adult says a word. Child walks like a robot, saying one sound per step: /d/ (step) /o/ (step) /g/ (step). "
        "Then speed up and blend: 'dog!'",
        "1. How many sounds in 'dog'? *(3: /d/ /ŏ/ /g/)*\n"
        "2. Segment 'bed.' What sounds? *(/b/ /ĕ/ /d/)*\n"
        "3. Why is segmenting important? *(It helps us spell — we write one phonogram per sound!)*",
        "At dinner, everyone segments a word from the meal: /m/ /ĭ/ /l/ /k/ → milk!",
        8, title_for(8, []))

    yield 8, build_pa(8, "pa-08", "First Sounds in Words",
        "Let's practice hearing the FIRST sound in words. This is one of the most important reading skills!",
        [
            ("What's the First Sound?",
             "Adult says a word. Child says just the first sound.\n\n"
             "dog → /d/\ncat → /k/\nfish → /f/\nsun → /s/\nman → /m/\nhat → /h/\ntop → /t/\nrun → /r/\nbed → /b/\npig → /p/\n"
             "\nGo faster once the child gets it!"),
            ("First Sound Match",
             "Adult says 'I'm thinking of a word that starts with /b/.' "
             "Child guesses words that start with /b/ (bat, ball, big, bed, bug...).\n\n"
             "Then switch — child picks a sound and adult guesses words.\n\n"
             "Try: /s/ (sun, sit, sad, sip), /m/ (man, map, mat, mom), /t/ (top, tap, ten, tub)"),
            ("Odd One Out",
             "Adult says three words. Two start with the same sound. One doesn't. Child finds the odd one.\n\n"
             "- dog, cat, dad (cat — starts with /k/, not /d/)\n"
             "- sun, sit, mop (mop — starts with /m/, not /s/)\n"
             "- hat, bat, hop (bat — starts with /b/, not /h/)\n"
             "- fan, dog, fish (dog — starts with /d/, not /f/)\n"
             "- rug, red, big (big — starts with /b/, not /r/)"),
        ],
        "Scavenger hunt! Find something in the room that starts with /b/ (book?), /k/ (cup?), /s/ (sock?). "
        "Bring it back to the adult and say its first sound!",
        "1. What's the first sound in 'mom'? *(/m/)*\n"
        "2. Which word doesn't belong: hat, dog, hop? *(dog — starts with /d/, not /h/)*\n"
        "3. Name three things that start with /s/.",
        "Play 'I Spy' with sounds! 'I spy something that starts with /b/...'",
        9, title_for(9, []))

    # ── Lessons 9-14: Group 1 Phonograms ──

    group1 = [("a", 9), ("d", 10), ("g", 11), ("c", 12), ("o", 13), ("qu", 14)]
    for i, (pg, num) in enumerate(group1):
        is_last = i == len(group1) - 1
        next_num = 15 if is_last else group1[i+1][1]
        next_title = "Review: Group 1 Phonograms" if is_last else f"Phonogram {group1[i+1][0]}"
        yield num, build_phonogram_intro(num, {"pg": pg}, next_num, next_title)

    # ── Lesson 15: Review Group 1 ──
    yield 15, build_review(15, 1, ["a","d","g","c","o","qu"], taught_order, 16, "Phonogram s")

    # ── Lessons 16-21: Group 2 Phonograms ──

    group2 = [("s", 16), ("t", 17), ("i", 18), ("p", 19), ("u", 20), ("j", 21)]
    for i, (pg, num) in enumerate(group2):
        is_last = i == len(group2) - 1
        next_num = 22 if is_last else group2[i+1][1]
        next_title = "Review: Group 2 Phonograms" if is_last else f"Phonogram {group2[i+1][0]}"
        yield num, build_phonogram_intro(num, {"pg": pg}, next_num, next_title)

    # ── Lesson 22: Review Group 2 ──
    yield 22, build_review(22, 2, ["s","t","i","p","u","j"], taught_order, 23, "Last Sounds in Words")

    # ── Lesson 23: PA - Last Sounds ──
    review_pgs_list = ["a","d","g","c","o","qu","s","t","i","p","u","j"]
    yield 23, build_pa_with_review(23, "pa-09", "Last Sounds in Words",
        "We've practiced finding the FIRST sound. Now let's find the LAST sound!",
        [
            ("What's the Last Sound?",
             "Adult says a word. Child says just the last sound.\n\n"
             "cat → /t/\ndog → /g/\ncup → /p/\nhat → /t/\nbed → /d/\nbig → /g/\nsun → /n/\nhop → /p/\n\n"
             "Go faster!"),
            ("Last Sound Match",
             "Adult says a sound. Child thinks of words that END with that sound.\n\n"
             "Words ending with /t/: cat, hat, bat, sit, hot, net, pot\n"
             "Words ending with /d/: bed, red, sad, mad, hid\n"
             "Words ending with /g/: dog, bag, big, dig, hug"),
            ("First OR Last?",
             "Adult says a word, then either 'first' or 'last.' "
             "Child says the corresponding sound.\n\n"
             "dog—FIRST → /d/    dog—LAST → /g/\ncat—FIRST → /k/    cat—LAST → /t/\nsun—FIRST → /s/     sun—LAST → /n/"),
        ],
        "Adult says a word. If it ends with /t/, child touches their TOES. If it ends with /d/, child touches their HEAD. "
        "If another sound, spin around!",
        "1. What's the last sound in 'cat'? *(/t/)*\n"
        "2. What's the last sound in 'dog'? *(/g/)*\n"
        "3. Name three words that end with /t/.",
        "On a walk, play: 'I see a tree. What's the last sound in tree?'",
        review_pgs_list, 24, "Phonogram r")

    # ── Lessons 24-29: Group 3 Phonograms ──

    group3 = [("r", 24), ("n", 25), ("m", 26), ("e", 27), ("l", 28), ("b", 29)]
    for i, (pg, num) in enumerate(group3):
        is_last = i == len(group3) - 1
        next_num = 30 if is_last else group3[i+1][1]
        next_title = "Review: Group 3 Phonograms" if is_last else f"Phonogram {group3[i+1][0]}"
        yield num, build_phonogram_intro(num, {"pg": pg}, next_num, next_title)

    # ── Lesson 30: Review Group 3 ──
    yield 30, build_review(30, 3, ["r","n","m","e","l","b"], taught_order, 31, "Middle Sounds in Words")

    # ── Lesson 31: PA - Middle Sounds ──
    rp = ["a","d","g","c","o","qu","s","t","i","p","u","j","r","n","m","e","l","b"]
    yield 31, build_pa_with_review(31, "pa-10", "Middle Sounds in Words",
        "The middle sound is the trickiest! We'll practice finding the sound in the middle of CVC words.",
        [
            ("Find the Middle",
             "Adult says a CVC word slowly. Child identifies the middle sound.\n\n"
             "cat → /ă/\ndog → /ŏ/\nsit → /ĭ/\nbed → /ĕ/\ncup → /ŭ/\nhat → /ă/\nbig → /ĭ/\nhop → /ŏ/\n\n"
             "Tip: The middle sound is always a vowel! Say it slowly and listen."),
            ("Which Vowel?",
             "Adult says a word. Child says which vowel sound is in the middle.\n\n"
             "man → /ă/    men → /ĕ/    pin → /ĭ/    pop → /ŏ/    fun → /ŭ/\n"
             "dad → /ă/    red → /ĕ/    win → /ĭ/    not → /ŏ/    sun → /ŭ/"),
            ("Change the Middle",
             "Adult: 'Say /k/ /ă/ /t/ — cat. Now change /ă/ to /ŭ/. What word?'\nChild: 'cut!'\n\n"
             "Try these:\n- cat → cut (/ă/ to /ŭ/)\n- big → bag (/ĭ/ to /ă/)\n- hop → hip (/ŏ/ to /ĭ/)\n- bed → bad (/ĕ/ to /ă/)\n- cup → cap (/ŭ/ to /ă/)"),
        ],
        "Vowel dance! Adult says /ă/, child makes an 'A' shape with arms. /ŏ/ = make 'O' with mouth. "
        "/ĭ/ = short and quick like a dot. /ĕ/ = hands open like 'eh!'. /ŭ/ = point UP!",
        "1. What's the middle sound in 'cat'? *(/ă/)*\n"
        "2. Change the middle sound of 'hat' from /ă/ to /ĭ/. What word? *(hit)*\n"
        "3. Why are middle sounds harder to hear? *(They're between two other sounds — you have to listen carefully!)*",
        "Say words around the house: 'lamp' — middle sound? /ă/. 'desk' — middle sound? /ĕ/.",
        rp, 32, "Phonogram h")

    # ── Lessons 32-37: Group 4 Phonograms ──

    group4 = [("h", 32), ("k", 33), ("f", 34), ("v", 35), ("w", 36), ("x", 37)]
    for i, (pg, num) in enumerate(group4):
        is_last = i == len(group4) - 1
        next_num = 38 if is_last else group4[i+1][1]
        next_title = "Review: Group 4 Phonograms" if is_last else f"Phonogram {group4[i+1][0]}"
        yield num, build_phonogram_intro(num, {"pg": pg}, next_num, next_title)

    # ── Lesson 38: Review Group 4 ──
    yield 38, build_review(38, 4, ["h","k","f","v","w","x"], taught_order, 39, "Phonogram y")

    # ── Lessons 39-40: Group 5 Phonograms ──

    yield 39, build_phonogram_intro(39, {"pg": "y"}, 40, "Phonogram z")
    yield 40, build_phonogram_intro(40, {"pg": "z"}, 41, "Sound Swapping Game")

    # ── Lesson 41: PA - Sound Swapping ──
    all_26 = ["a","d","g","c","o","qu","s","t","i","p","u","j","r","n","m","e","l","b","h","k","f","v","w","x","y","z"]
    yield 41, build_pa_with_review(41, "pa-11", "Sound Swapping Game",
        "You know all 26 phonograms now! Let's play with sounds — change one sound and make a new word.",
        [
            ("Change the First Sound",
             "Adult: 'Say *cat*. Now change /k/ to /b/. What word?'\nChild: 'bat!'\n\n"
             "cat → bat, hat, mat, rat, sat, fat, pat\n"
             "dog → hog, log, fog, jog\n"
             "sun → run, fun, bun, nun"),
            ("Change the Last Sound",
             "Adult: 'Say *cat*. Now change /t/ to /p/. What word?'\nChild: 'cap!'\n\n"
             "cat → cap, can, cab\n"
             "dog → dot, doll\n"
             "bed → bet, beg, bell"),
            ("Chain Game",
             "Change one sound at a time to make a chain of new words.\n\n"
             "cat → hat → hit → hip → hop → hog → dog → dig → big → bag → bat → cat (back where we started!)\n\n"
             "How many links can you make?"),
        ],
        "Word ladder game: Each step change one sound. Adult starts with 'cat.' "
        "Child changes one sound and takes a step forward. Keep going until you reach 'dog'!",
        "1. Change the first sound of 'cat' to /h/. What word? *(hat)*\n"
        "2. Change the last sound of 'dog' to /t/. What word? *(dot)*\n"
        "3. Make a chain: cat → hat → hit. What sound changed each time?",
        "Play 'Sound Swap' in the car. Start with any 3-sound word and see how many new words you can make!",
        all_26, 42, "Meet the Vowels")

    # ── Lesson 42: Vowels ──
    vowel_spelling_rows = (
        "| cat | a | /ă/ — mouth open, can sing it |\n"
        "| dog | o | /ŏ/ — mouth open, can sing it |\n"
        "| sit | i | /ĭ/ — mouth open, can sing it |\n"
        "| bed | e | /ĕ/ — mouth open, can sing it |\n"
        "| cup | u | /ŭ/ — mouth open, can sing it |\n"
        "| by | y | /ī/ — vowel sound! |\n"
        "| baby | y | /ē/ — vowel sound! |\n"
        "| gym | y | /ĭ/ — vowel sound! |"
    )
    yield 42, SPECIAL_VOWELS_TEMPLATE.format(
        lesson_num=42, spelling_rows=vowel_spelling_rows,
        next_num=43, next_title="All 26 Phonograms Review",
        teacher_script="",
    )

    # ── Lesson 43: ALL 26 Review ──
    yield 43, build_review(43, "ALL", all_26, taught_order, 44, "Blending with Consonant Blends")

    # ── Lesson 44: PA - Consonant Blends ──
    yield 44, build_pa_with_review(44, "pa-12", "Blending with Consonant Blends",
        "Now we blend words that start with TWO consonants together, like 'stop' and 'frog'!",
        [
            ("Two Sounds Together",
             "Adult says a word with a consonant blend at the start. Child blends.\n\n"
             "L-blends: /s/ /l/ /ĭ/ /p/ → slip, /k/ /l/ /ă/ /p/ → clap, /f/ /l/ /ă/ /g/ → flag\n"
             "R-blends: /s/ /t/ /ŏ/ /p/ → stop, /f/ /r/ /ŏ/ /g/ → frog, /d/ /r/ /ŏ/ /p/ → drop\n"
             "S-blends: /s/ /t/ /ĕ/ /p/ → step, /s/ /w/ /ĭ/ /m/ → swim, /s/ /n/ /ă/ /p/ → snap"),
            ("Blend First, Then Add",
             "Adult: 'Say /s/ /t/ together — /st/. Now add /ŏ/ /p/. What word?'\nChild: 'stop!'\n\n"
             "/st/ + /ŏ/ /p/ → stop\n/sp/ + /ĭ/ /n/ → spin\n/sl/ + /ĭ/ /p/ → slip\n/fl/ + /ă/ /g/ → flag"),
            ("Blend Hunt",
             "Which of these start with a blend? Child identifies:\n\n"
             "cat (no blend — single sound)\nstop (yes! /st/ blend)\ndog (no blend)\nfrog (yes! /fr/ blend)\nclap (yes! /kl/ blend)\nsun (no blend)"),
        ],
        "Blend-freeze! Adult says words. If the word starts with a blend, child FREEZES like a statue. "
        "If it doesn't, child keeps moving. 'stop' — FREEZE! 'cat' — keep moving! 'frog' — FREEZE!",
        "1. Blend /s/ /t/ /ŏ/ /p/. What word? *(stop)*\n"
        "2. What two sounds blend together at the start of 'frog'? *(/f/ and /r/)*\n"
        "3. Does 'cat' start with a blend? *(No — just /k/)*",
        "Look in a book. Find 3 words that start with a consonant blend.",
        all_26, 45, "Blending Two-Syllable Words")

    # ── Lesson 45: PA - Two-Syllable ──
    yield 45, build_pa_with_review(45, "pa-13", "Blending Two-Syllable Words",
        "You're getting so good at blending! Now let's blend words with TWO syllables.",
        [
            ("Syllable Blending",
             "Adult says two syllables with a pause. Child blends into one word.\n\n"
             "win ... dow → window\nkit ... ten → kitten\nhap ... py → happy\npen ... cil → pencil\nrab ... bit → rabbit\nsun ... set → sunset\nsun ... shine → sunshine\nback ... pack → backpack"),
            ("Count and Blend",
             "Adult says a word. Child claps the syllables, then blends them.\n\n"
             "2 syllables: table, paper, water, mother, father, sister, brother\n"
             "3 syllables: elephant, banana, tomato, butterfly, dinosaur"),
            ("Two-Syllable Challenge",
             "Adult says each syllable of a word separately. Child blends, then segments the whole word into individual sounds.\n\n"
             "Adult: 'pen...cil' — Child: 'pencil!' — Now segment: /p/ /ĕ/ /n/ /s/ /ĭ/ /l/\n"
             "Adult: 'rab...bit' — Child: 'rabbit!' — Now segment: /r/ /ă/ /b/ /ĭ/ /t/"),
        ],
        "Clap and blend! Adult says a two-syllable word. Child claps once per syllable, "
        "then jumps and says the whole word. 'win' (clap) 'dow' (clap) → JUMP → 'window!'",
        "1. Blend 'rab' + 'bit'. What word? *(rabbit)*\n"
        "2. How many syllables in 'butterfly'? *(3: but-ter-fly)*\n"
        "3. Segment 'pencil' into individual sounds. *(/p/ /ĕ/ /n/ /s/ /ĭ/ /l/)*",
        "Practice two-syllable blending with animal names: ti-ger, ze-bra, pan-da, mon-key.",
        all_26, 46, "Handwriting: Clockface Letters")

    # ── Lesson 46: Handwriting Clockface ──
    clockface_letters = "a, d, g, c, o, qu, s"
    yield 46, SPECIAL_HANDWRITING_TEMPLATE.format(
        lesson_num=46, title="Handwriting: Clockface Letters",
        hand_warmup="Shake out your hands. Wiggle your fingers. Touch each finger to your thumb — index, middle, ring, pinky. Now draw big circles in the air with your finger!",
        letter_group=f"## Clockface Letters\n\nThese letters all start with a curve — like the face of a clock! The letters are: **{clockface_letters}**",
        letter_list="",
        writing_instructions=(
            "### a\nStart at the midline. Curve around like a clock going counter-clockwise. Go up and down in a straight line.\n\n"
            "### d\nStart at the midline. Curve around like a clock. Go up high, then straight down.\n\n"
            "### g\nStart at the midline. Curve around like a clock. Go up, then curve down into a tail below the line.\n\n"
            "### c\nStart just below the midline. Curve around like most of a clock. Leave a small opening.\n\n"
            "### o\nStart at the midline. Curve around like a clock. Close the circle neatly.\n\n"
            "### qu\nq: Curve around like a clock, then a short diagonal line. u: Curve down and back up. They are a team!\n\n"
            "### s\nStart just below the midline. Curve left, then right, like a snake."
        ),
        letter_grid="| a | a | a | a | a |\n| d | d | d | d | d |\n| g | g | g | g | g |\n| c | c | c | c | c |\n| o | o | o | o | o |\n| qu | qu | qu | qu | qu |\n| s | s | s | s | s |",
        letter_hunt="Find any clockface letter in a book. Which ones did you find?",
        challenge_sound="ă",
        next_num=47, next_title="Handwriting: Straight-start Letters",
        teacher_script="",
    )

    # ── Lesson 47: Handwriting Straight-start ──
    straight_letters = "t, i, p, u, j, r, n, m, l, b, h, k, f"
    yield 47, SPECIAL_HANDWRITING_TEMPLATE.format(
        lesson_num=47, title="Handwriting: Straight-start Letters",
        hand_warmup="Trace a straight line from top to bottom in the air 5 times. Trace a line from left to right 5 times. Now make big circles with both hands!",
        letter_group=f"## Straight-Start Letters\n\nThese letters all start with a straight line down. The letters are: **{straight_letters}**",
        letter_list="",
        writing_instructions=(
            "### t\nStart at the top line. Straight line down. Cross in the middle.\n\n"
            "### i\nStart at the midline. Straight line down. Dot at the top.\n\n"
            "### p\nStart at the midline. Straight line down below the baseline. Go back up and make a circle.\n\n"
            "### u\nStart at the midline. Curve down, then back up. Straight line down.\n\n"
            "### j\nStart at the midline. Straight down below baseline. Hook left. Dot at top.\n\n"
            "### r\nStart at the midline. Straight line down. Go back up and curve over.\n\n"
            "### n\nStart at the midline. Straight down. Go back up and make a hill.\n\n"
            "### m\nStart at the midline. Straight down. Go back up and make TWO hills.\n\n"
            "### l\nStart at the top line. Straight line down.\n\n"
            "### b\nStart at the top line. Straight line down. Go back up to midline and make a circle.\n\n"
            "### h\nStart at the top line. Straight line down. Go back up and make a hump.\n\n"
            "### k\nStart at the top line. Straight line down. From the middle, slant in then out.\n\n"
            "### f\nStart at the top line. Curve around and straight down. Cross in the middle."
        ),
        letter_grid="| t | t | t | t | t |\n| i | i | i | i | i |\n| p | p | p | p | p |\n| u | u | u | u | u |\n| j | j | j | j | j |\n| r | r | r | r | r |\n| n | n | n | n | n |\n| m | m | m | m | m |\n| l | l | l | l | l |\n| b | b | b | b | b |\n| h | h | h | h | h |\n| k | k | k | k | k |\n| f | f | f | f | f |",
        letter_hunt="Find any straight-start letter in a book. Count how many you can find in one page!",
        challenge_sound="t",
        next_num=48, next_title="Stage 1 Mastery Check",
        teacher_script="",
    )

    # ── Lesson 48: Assessment ──
    yield 48, build_assessment()

    # ── Lesson 49 (hidden): vowel-z — extra handwriting for diag finish
    yield 47, None  # already covered


def build_assessment():
    phonogram_checklist = "\n".join(
        f"| {p} | {PHONOGRAMS[p]['sounds']} | ☐ |"
        for p in list(PHONOGRAMS.keys())
    )
    write_checklist = (
        "| /ă/ | a | ☐ |\n| /d/ | d | ☐ |\n| /g/ | g | ☐ |\n| /k/ | c | ☐ |\n"
        "| /ŏ/ | o | ☐ |\n| /kw/ | qu | ☐ |\n| /s/ | s | ☐ |\n| /t/ | t | ☐ |\n"
        "| /ĭ/ | i | ☐ |\n| /p/ | p | ☐ |\n| /ŭ/ | u | ☐ |\n| /j/ | j | ☐ |\n"
        "| /m/ | m | ☐ |\n| /n/ | n | ☐ |\n| /b/ | b | ☐ |\n| /f/ | f | ☐ |"
    )
    blend_checklist = (
        "| /s/ /ă/ /t/ → sat | ☐ |\n"
        "| /d/ /ŏ/ /g/ → dog | ☐ |\n"
        "| /h/ /ĭ/ /m/ → him | ☐ |\n"
        "| /f/ /ŭ/ /n/ → fun | ☐ |\n"
        "| /r/ /ĕ/ /d/ → red | ☐ |"
    )
    segment_checklist = (
        "| cat → /k/ /ă/ /t/ | ☐ |\n"
        "| dog → /d/ /ŏ/ /g/ | ☐ |\n"
        "| bed → /b/ /ĕ/ /d/ | ☐ |\n"
        "| sun → /s/ /ŭ/ /n/ | ☐ |\n"
        "| hop → /h/ /ŏ/ /p/ | ☐ |"
    )
    sound_id_checklist = (
        "| cat | first | /k/ | ☐ |\n"
        "| dog | last | /g/ | ☐ |\n"
        "| bed | middle | /ĕ/ | ☐ |\n"
        "| sun | first | /s/ | ☐ |\n"
        "| hop | last | /p/ | ☐ |\n"
        "| big | middle | /ĭ/ | ☐ |"
    )
    return ASSESSMENT_TEMPLATE.format(
        lesson_num=48,
        phonogram_checklist=phonogram_checklist,
        pass_count="__",
        write_checklist=write_checklist,
        blend_checklist=blend_checklist,
        segment_checklist=segment_checklist,
        sound_id_checklist=sound_id_checklist,
        sound_score="__", write_score="__", blend_score="__", seg_score="__", id_score="__",
        sound_pass="__", write_pass="__", blend_pass="__", seg_pass="__", id_pass="__",
        overall="__",
        next_steps="If all sections pass: Move to Stage 2! If any section is weak, return to those lessons and re-test in 1-2 weeks.",
        teacher_script="",
    )


# ── WRITE FILES ─────────────────────────────────────────────────────

def main():
    for num, content in generate_all():
        if content is None:
            continue
        # Map lesson number to filename slug
        slugs = {
            1: "pa-01-sounds-around-us", 2: "pa-02-voiced-unvoiced", 3: "pa-03-blend-compound",
            4: "pa-04-blend-syllables", 5: "pa-05-onset-rime", 6: "pa-06-blend-cvc",
            7: "pa-07-segment-cvc", 8: "pa-08-initial-sounds",
            9: "pg-a", 10: "pg-d", 11: "pg-g", 12: "pg-c", 13: "pg-o", 14: "pg-qu",
            15: "review-1",
            16: "pg-s", 17: "pg-t", 18: "pg-i", 19: "pg-p", 20: "pg-u", 21: "pg-j",
            22: "review-2",
            23: "pa-09-final-sounds",
            24: "pg-r", 25: "pg-n", 26: "pg-m", 27: "pg-e", 28: "pg-l", 29: "pg-b",
            30: "review-3",
            31: "pa-10-medial-sounds",
            32: "pg-h", 33: "pg-k", 34: "pg-f", 35: "pg-v", 36: "pg-w", 37: "pg-x",
            38: "review-4",
            39: "pg-y", 40: "pg-z",
            41: "pa-11-sound-swap",
            42: "vowels-1",
            43: "review-5",
            44: "pa-12-blends", 45: "pa-13-two-syllable",
            46: "handwriting-1", 47: "handwriting-2",
            48: "assessment-1",
        }
        slug = slugs.get(num, f"lesson-{num:03d}")
        filepath = OUT_DIR / f"{slug}.md"
        filepath.write_text(content, encoding="utf-8")
        print(f"  Wrote: {filepath.relative_to(PROJECT_ROOT)}")

    print(f"\nDone! {len(slugs)} lessons written to {OUT_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
