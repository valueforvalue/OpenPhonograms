#!/usr/bin/env python3
"""Generate all 56 Stage 2 lesson markdown files with real educational content."""

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "lessons" / "stage-2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── PHONOGRAM DATA ──────────────────────────────────────────────────

# Single-letter phonograms (all 26 are known from Stage 1)
SINGLE_PGS = {
    "a": {"sounds": "/ă/ /ā/ /ä/", "vowel": True},
    "b": {"sounds": "/b/", "vowel": False},
    "c": {"sounds": "/k/ /s/", "vowel": False},
    "d": {"sounds": "/d/", "vowel": False},
    "e": {"sounds": "/ĕ/ /ē/", "vowel": True},
    "f": {"sounds": "/f/", "vowel": False},
    "g": {"sounds": "/g/ /j/", "vowel": False},
    "h": {"sounds": "/h/", "vowel": False},
    "i": {"sounds": "/ĭ/ /ī/ /ē/", "vowel": True},
    "j": {"sounds": "/j/", "vowel": False},
    "k": {"sounds": "/k/", "vowel": False},
    "l": {"sounds": "/l/", "vowel": False},
    "m": {"sounds": "/m/", "vowel": False},
    "n": {"sounds": "/n/", "vowel": False},
    "o": {"sounds": "/ŏ/ /ō/ /ö/", "vowel": True},
    "p": {"sounds": "/p/", "vowel": False},
    "qu": {"sounds": "/kw/", "vowel": False},
    "r": {"sounds": "/r/", "vowel": False},
    "s": {"sounds": "/s/ /z/", "vowel": False},
    "t": {"sounds": "/t/", "vowel": False},
    "u": {"sounds": "/ŭ/ /ū/ /ö/", "vowel": True},
    "v": {"sounds": "/v/", "vowel": False},
    "w": {"sounds": "/w/", "vowel": False},
    "x": {"sounds": "/ks/ /z/", "vowel": False},
    "y": {"sounds": "/y/ /ĭ/ /ī/ /ē/", "vowel": True},
    "z": {"sounds": "/z/", "vowel": False},
}

# Multi-letter phonograms introduced in Stage 2
MULTI_PGS = {
    "sh": {
        "sounds": "/sh/",
        "sound_count": 1,
        "examples": [("sh", "ship, fish, wish, dash")],
        "tip": "SH is a two-letter phonogram. Both letters work together to make one sound!",
        "rule": None,
    },
    "th": {
        "sounds": "/th/ (voiced) /th/ (unvoiced)",
        "sound_count": 2,
        "examples": [("th (voiced)", "this, that, them"), ("th (unvoiced)", "thin, with, path")],
        "tip": "TH has TWO sounds: buzzing (voiced, as in 'this') and quiet (unvoiced, as in 'thin'). Put your hand on your throat to tell them apart!",
        "rule": None,
    },
    "ck": {
        "sounds": "/k/",
        "sound_count": 1,
        "examples": [("k", "back, stick, duck, clock")],
        "tip": "CK is a two-letter /k/ used ONLY after a short vowel. It never comes at the beginning of a word.",
        "rule": "Rule 26: CK is used only after a single vowel which says its short sound. Never at the beginning.",
    },
    "ee": {
        "sounds": "/ē/",
        "sound_count": 1,
        "examples": [("ē", "see, green, feet, tree")],
        "tip": "Double E always says /ē/. It's one of the most reliable phonograms in English!",
        "rule": None,
    },
    "ng": {
        "sounds": "/ng/",
        "sound_count": 1,
        "examples": [("ng", "sing, long, ring, song")],
        "tip": "NG is a nasal sound — the air comes through your nose. It's one sound, even though it uses two letters.",
        "rule": None,
    },
    "ar": {
        "sounds": "/är/",
        "sound_count": 1,
        "examples": [("är", "car, farm, star, dark")],
        "tip": "AR is an R-controlled vowel. The R changes the sound of the A.",
        "rule": None,
    },
    "or": {
        "sounds": "/or/",
        "sound_count": 1,
        "examples": [("or", "for, corn, sort, horse")],
        "tip": "OR is an R-controlled vowel. The R changes the sound of the O.",
        "rule": None,
    },
    "er": {
        "sounds": "/er/",
        "sound_count": 1,
        "examples": [("er", "her, sister, under, never")],
        "tip": "ER says /er/ as in 'her'. This is the most common spelling of the /er/ sound. It appears at the end of many words.",
        "rule": None,
    },
    "oi": {
        "sounds": "/oi/",
        "sound_count": 1,
        "examples": [("oi", "coin, oil, join, soil")],
        "tip": "OI says /oi/. It is NEVER used at the end of an English word (because of Rule 3).",
        "rule": "Rule 3: No English word ends in I, U, V, or J. This is why we use OI in the middle and OY at the end.",
    },
    "oy": {
        "sounds": "/oi/",
        "sound_count": 1,
        "examples": [("oi", "boy, toy, enjoy, destroy")],
        "tip": "OY says /oi/ and is used at the END of a base word (because of Rule 3).",
        "rule": "Rule 3: No English word ends in I. Since /oi/ can't end with I, we use OY.",
    },
    "ai": {
        "sounds": "/ā/",
        "sound_count": 1,
        "examples": [("ā", "rain, paint, sail, train")],
        "tip": "AI is a two-letter /ā/. It is NEVER used at the end of an English word (Rule 3).",
        "rule": "Rule 3: No English word ends in I. AI never ends a word. Use AY instead.",
    },
    "ay": {
        "sounds": "/ā/",
        "sound_count": 1,
        "examples": [("ā", "day, play, stay, may")],
        "tip": "AY says /ā/ and is used at the END of a base word.",
        "rule": "Rule 9: AY usually spells the sound /ā/ at the end of a base word.",
    },
    "ch": {
        "sounds": "/ch/ /k/ /sh/",
        "sound_count": 3,
        "examples": [("ch", "chin, much, chip"), ("k", "school, echo, chemist"), ("sh", "chef, machine, brochure")],
        "tip": "CH has three sounds! /ch/ is most common (English words). /k/ comes from Greek words. /sh/ comes from French words.",
        "rule": None,
    },
    "wh": {
        "sounds": "/hw/",
        "sound_count": 1,
        "examples": [("hw", "when, which, white, whale")],
        "tip": "WH says /hw/. Blow a little air when you say it — you should feel it on your hand.",
        "rule": None,
    },
    "ea": {
        "sounds": "/ē/ /ĕ/ /ā/",
        "sound_count": 3,
        "examples": [("ē", "eat, read, team"), ("ĕ", "head, bread, weather"), ("ā", "great, break, steak")],
        "tip": "EA has three sounds! /ē/ is most common. /ĕ/ is the second sound. /ā/ is rare — only a few words use it.",
        "rule": None,
    },
    "ow": {
        "sounds": "/ow/ /ō/",
        "sound_count": 2,
        "examples": [("ow", "cow, how, now, brown"), ("ō", "snow, grow, low, show")],
        "tip": "OW has two sounds: /ow/ as in 'cow' and /ō/ as in 'snow'. You need to try both to figure out which one works.",
        "rule": None,
    },
    "ou": {
        "sounds": "/ow/ /ō/ /ö/ /ŭ/",
        "sound_count": 4,
        "examples": [("ow", "out, house, round"), ("ō", "soul, four, pour"), ("ö", "you, group, soup"), ("ŭ", "touch, young, double")],
        "tip": "OU has four sounds! /ow/ is most common. Try each sound when you read a new OU word.",
        "rule": None,
    },
    "oo": {
        "sounds": "/ö/ /ü/ /ō/",
        "sound_count": 3,
        "examples": [("ö", "book, look, foot, good"), ("ü", "food, moon, soon, too"), ("ō", "floor, door")],
        "tip": "OO has three sounds. /ö/ (as in 'book') and /ü/ (as in 'food') are most common.",
        "rule": None,
    },
    "ed": {
        "sounds": "/ed/ /d/ /t/",
        "sound_count": 3,
        "examples": [("ed", "wanted, needed, rented"), ("d", "played, called, showed"), ("t", "fished, jumped, looked")],
        "tip": "ED is a verb ending. It has three sounds: /ed/ after d/t, /d/ after voiced sounds, /t/ after unvoiced sounds.",
        "rule": "Rule 20: The past-tense ending -ED says /ed/ after D or T, /d/ after a voiced sound, and /t/ after an unvoiced consonant.",
    },
    "igh": {
        "sounds": "/ī/",
        "sound_count": 1,
        "examples": [("ī", "light, high, night, right")],
        "tip": "IGH is a three-letter /ī/. The GH is silent here.",
        "rule": "Rule 28: GH is often silent after I.",
    },
    "aw": {
        "sounds": "/ä/",
        "sound_count": 1,
        "examples": [("ä", "saw, draw, law, straw")],
        "tip": "AW says /ä/ and is used at the END of a base word (Rule 3).",
        "rule": "Rule 3: No English word ends in U. AW ends many words.",
    },
    "au": {
        "sounds": "/ä/",
        "sound_count": 1,
        "examples": [("ä", "cause, author, autumn, haul")],
        "tip": "AU says /ä/ and is NEVER used at the end of an English word (Rule 3).",
        "rule": "Rule 3 + 28: AU never at end. Some AU words have silent GH after.",
    },
    "ir": {
        "sounds": "/er/",
        "sound_count": 1,
        "examples": [("er", "girl, bird, first, shirt")],
        "tip": "IR says /er/ as in 'first'. This is one of five ways to spell the /er/ sound (er, ir, ur, ear, wor).",
        "rule": None,
    },
    "ur": {
        "sounds": "/er/",
        "sound_count": 1,
        "examples": [("er", "hurt, turn, burn, church")],
        "tip": "UR says /er/ as in 'nurse'. Like IR and ER, it's an R-controlled vowel.",
        "rule": None,
    },
    "oa": {
        "sounds": "/ō/",
        "sound_count": 1,
        "examples": [("ō", "boat, road, soap, goat")],
        "tip": "OA is a two-letter /ō/. It is NEVER at the end of an English word (Rule 3).",
        "rule": "Rule 3: No English word ends in A? Actually, OA doesn't end words because of how English spelling works.",
    },
    "ear": {
        "sounds": "/er/",
        "sound_count": 1,
        "examples": [("er", "learn, earth, early, heard")],
        "tip": "EAR says /er/ as in 'early'. Another way to spell the /er/ sound!",
        "rule": None,
    },
}

# Known multi-letter PGs at each lesson (indexed by lesson num)
# After each multi-letter PG intro lesson, it becomes "known"
KNOWN_MULTI_AFTER = {
    10: [],       # After lesson 10, no multi-letter PGs yet
    11: [],
    12: ["sh"],
    13: ["sh", "th"],
    14: ["sh", "th", "ck"],
    15: ["sh", "th", "ck"],
    16: ["sh", "th", "ck", "ee"],
    17: ["sh", "th", "ck", "ee"],
    18: ["sh", "th", "ck", "ee"],
    19: ["sh", "th", "ck", "ee"],
    20: ["sh", "th", "ck", "ee", "ng"],
    21: ["sh", "th", "ck", "ee", "ng", "ar"],
    22: ["sh", "th", "ck", "ee", "ng", "ar", "or"],
    23: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er"],
    25: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er"],
    26: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi"],
    27: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy"],
    28: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy"],
    29: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai"],
    30: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay"],
    32: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay"],
    33: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch"],
    34: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh"],
    35: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea"],
    36: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea"],
    37: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow"],
    38: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou"],
    40: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou"],
    41: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo"],
    42: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed"],
    43: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed"],
    44: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh"],
    45: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw"],
    46: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au"],
    47: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir"],
    48: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir", "ur"],
    49: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir", "ur"],
    50: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir", "ur", "oa"],
    51: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir", "ur", "oa", "ear"],
    55: ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir", "ur", "oa", "ear"],
}

def known_multi_for(num):
    """Get multi-letter PGs known at this lesson num."""
    for threshold in sorted(KNOWN_MULTI_AFTER.keys(), reverse=True):
        if num >= threshold:
            return KNOWN_MULTI_AFTER[threshold]
    return []

# ── SPELLING RULES ──────────────────────────────────────────────────

RULES = {
    "3": {
        "number": 3,
        "name": "No English Word Ends in I, U, V, or J",
        "statement": "English words do not end in **I**, **U**, **V**, or **J**.",
        "explanation": "This rule explains so many spellings! Because words cannot end in I, we use Y instead (boy, day). Because words cannot end in U, we use W at the end (saw, new). Because words cannot end in V, we add silent E (have, give). This is one of the most important spelling rules.",
        "examples": "have, give, blue (silent E protects V/U) · boy, day, play (Y replaces I) · saw, law (W replaces U)",
        "words_for_spelling": ["have", "give", "day", "play", "boy", "saw"],
    },
    "4": {
        "number": 4,
        "name": "A E O U at End of Syllable Say Long Sound",
        "statement": "**A**, **E**, **O**, and **U** usually say their long sounds at the end of a syllable.",
        "explanation": "In an OPEN syllable (a syllable that ends with a vowel), the vowel says its long sound. For example, in 'ba·by', the first syllable 'ba' ends with A, so A says /ā/. In 'go', the syllable ends with O, so O says /ō/.",
        "examples": "ba·by (A says /ā/) · e·ven (E says /ē/) · go (O says /ō/) · u·nit (U says /ū/) · mu·sic · o·pen · pa·per",
        "words_for_spelling": ["go", "no", "so", "he", "me", "she", "baby", "open"],
    },
    "9": {
        "number": 9,
        "name": "AY at End of Base Word",
        "statement": "**AY** usually spells the sound /ā/ at the end of a base word.",
        "explanation": "Because of Rule 3 (no word ends in I), AI can't end a word. So we use AY instead. AI is used in the middle, AY at the end.",
        "examples": "day, play, stay, may, say, way (AY at end) · rain, paint, train (AI in middle)",
        "words_for_spelling": ["day", "play", "stay", "may", "ray", "say", "rain", "train"],
    },
    "20": {
        "number": 20,
        "name": "Three Sounds of -ED",
        "statement": "The past-tense ending **-ED** says /ed/ after **D** or **T**, /d/ after a voiced sound, and /t/ after an unvoiced consonant.",
        "explanation": "ED marks past tense, but it doesn't always say /ed/. After D or T, you hear the full /ed/ syllable (wanted, needed). After voiced consonants, it says /d/ (played, called). After unvoiced consonants, it says /t/ (fished, jumped).",
        "examples": "/ed/: wanted, needed, rented · /d/: played, called, showed · /t/: fished, jumped, looked",
        "words_for_spelling": ["wanted", "played", "fished", "jumped", "called", "looked", "needed"],
    },
    "26": {
        "number": 26,
        "name": "CK After Short Vowel",
        "statement": "**CK** is used only after a single vowel which says its short sound.",
        "explanation": "CK never comes at the beginning of a word. It is used after a short vowel to spell /k/. Compare: 'back' (CK after short a) vs. 'bake' (silent E makes a long). CK is a two-letter phonogram — both C and K work together.",
        "examples": "back, stick, duck, clock, neck (CK after short vowel) · milk, ask, desk (/k/ after consonant — NO CK)",
        "words_for_spelling": ["back", "stick", "duck", "clock", "neck", "sick", "pack"],
    },
    "28": {
        "number": 28,
        "name": "GH Phonograms",
        "statement": "**GH** is often silent after **I** and before **T**.",
        "explanation": "In IGH, the GH is silent — the three letters work together to say /ī/. In EIGH, the GH is also silent — four letters say /ā/. In AUGH and OUGH, the GH can make different sounds or be silent.",
        "examples": "light, high, night (IGH — GH silent) · eight, neighbor (EIGH — GH silent) · laugh (AUGH — GH says /f/) · though (OUGH — GH silent)",
        "words_for_spelling": ["light", "night", "right", "high", "bright"],
    },
    "30": {
        "number": 30,
        "name": "Double F, L, S (Floss Rule)",
        "statement": "In a one-syllable word, double the final **F**, **L**, or **S** after a single vowel.",
        "explanation": "This is sometimes called the 'Floss Rule.' After a short vowel in a one-syllable word, if the word ends in F, L, or S, double it! off, bell, miss, staff, full, grass.",
        "examples": "off, cliff, stuff (FF) · bell, fill, tall, full (LL) · miss, grass, class, kiss (SS)",
        "words_for_spelling": ["off", "bell", "miss", "fill", "grass", "tell", "class"],
    },
}

# ── HIGH-FREQUENCY WORDS ────────────────────────────────────────────

HF_WORDS_SET1 = [
    ("the", "TH says voiced /th/. E says /ē/ at end of syllable, but in fast speech it softens to schwa (/ə/). Say-to-spell: /thē/."),
    ("a", "A says /ā/ at end of syllable. In a sentence, unstressed a softens to /ə/. Say-to-spell: /ā/."),
    ("is", "I says /ĭ/. S says /z/ at the end of this word (it often says /z/ between vowels or at the end). Say-to-spell: /ĭz/."),
    ("of", "O says /ŭ/ in this word (a special case). F says /v/ — yes, /v/! Say-to-spell: /ŏv/."),
    ("to", "O says /ö/ — its broad sound. Say-to-spell: /tö/."),
]

HF_WORDS_SET2 = [
    ("do", "O says /ö/ — just like 'to'. Say-to-spell: /dö/."),
    ("was", "W before A: A says /ä/ (Rule 10). S says /z/ at the end. Say-to-spell: /wŏz/."),
    ("has", "A says /ă/. S says /z/ at the end. Say-to-spell: /hăz/."),
    ("said", "AI says /ĕ/ here — this is one of very few words where AI says /ĕ/. Say-to-spell: /sād/ to remember the AI."),
    ("you", "OU says /ö/ here. It's a very common word. Say-to-spell: /yō/."),
]

HF_WORDS_SET3 = [
    ("are", "A says /ä/ (Rule 10, before R). Silent E. AR rows /är/. Say-to-spell: /är/."),
    ("have", "A says /ă/. Silent E is here because of Rule 3 — no English word ends in V. Say-to-spell: /hăv/."),
    ("give", "Short I says /ĭ/. G says /g/ (it may soften before I, but doesn't here). Silent E because of Rule 3 (no V at end). Say-to-spell: /gĭv/."),
    ("come", "O says /ŭ/. Silent E is Rule 12.9 — the unseen reason. Say-to-spell: /kōm/ to remember the O, then read as /kŭm/."),
    ("some", "O says /ŭ/. Silent E — Rule 12.9. Say-to-spell: /sōm/ to remember O."),
]

# ── WORD LISTS ──────────────────────────────────────────────────────

VC_WORDS = ["at", "in", "on", "up", "it", "am", "an", "ad", "if"]
CVC_CONTINUANT = ["man", "fan", "run", "sun", "sit", "fit", "mat", "map", "nap", "rat", "ran", "rim", "fin", "fun", "net", "men", "lit", "lip", "rip", "nut"]
CVC_STOP = ["cat", "dog", "pot", "big", "tap", "cup", "bat", "pat", "top", "cot", "dot", "got", "bit", "put", "cut", "gut", "pet", "bet", "tip", "dip"]
CVC_ALL = ["jam", "web", "fox", "zip", "quit", "box", "fix", "mix", "six", "job", "wet", "yes", "van", "kid", "wig", "bag", "tag", "log", "fog", "jug", "mud", "bed", "red", "led", "fed"]
CCVC_BLENDS = ["stop", "frog", "glad", "swim", "crab", "slip", "spot", "trip", "drip", "snap", "flag", "clip", "grab", "drop", "spin", "step", "twin", "plan", "brag", "sled"]
CVCC_BLENDS = ["hand", "milk", "fast", "jump", "nest", "help", "belt", "desk", "mask", "lamp", "sand", "send", "tent", "went", "just", "must", "list", "lost", "bump", "camp"]
CCVCC_BLENDS = ["plant", "stamp", "blend", "crust", "trust", "print", "spend", "frost", "blast", "twist", "slant", "brand", "crisp", "plump", "stump"]

# Words for spelling analysis with multi-letter PGs
PG_SPELLING_WORDS = {
    "sh": [("ship", "sh (/sh/), i (/ĭ/), p (/p/)", "sh = two-letter phonogram", "/shĭp/"),
           ("fish", "f (/f/), i (/ĭ/), sh (/sh/)", "sh at end", "/fĭsh/"),
           ("dash", "d (/d/), a (/ă/), sh (/sh/)", "sh at end", "/dăsh/")],
    "th": [("this", "th (/th/ voiced), i (/ĭ/), s (/s/)", "th voiced — buzz on", "/thĭs/"),
           ("thin", "th (/th/ unvoiced), i (/ĭ/), n (/n/)", "th unvoiced — no buzz", "/thĭn/"),
           ("with", "w (/w/), i (/ĭ/), th (/th/ unvoiced)", "th at end", "/wĭth/")],
    "ck": [("back", "b (/b/), a (/ă/), ck (/k/)", "Rule 26: CK after short vowel", "/băk/"),
           ("duck", "d (/d/), u (/ŭ/), ck (/k/)", "Rule 26: CK after short ŭ", "/dŭk/"),
           ("sick", "s (/s/), i (/ĭ/), ck (/k/)", "Rule 26: CK after short ĭ", "/sĭk/")],
    "ee": [("see", "s (/s/), ee (/ē/)", "Double E always /ē/", "/sē/"),
           ("feet", "f (/f/), ee (/ē/), t (/t/)", "Double E always /ē/", "/fēt/"),
           ("green", "g (/g/), r (/r/), ee (/ē/), n (/n/)", "Double E always /ē/", "/grēn/")],
    "ng": [("sing", "s (/s/), i (/ĭ/), ng (/ng/)", "ng = one nasal sound", "/sĭng/"),
           ("long", "l (/l/), o (/ŏ/), ng (/ng/)", "ng at end", "/lŏng/"),
           ("ring", "r (/r/), i (/ĭ/), ng (/ng/)", "ng after short i", "/rĭng/")],
    "ar": [("car", "c (/k/), ar (/är/)", "AR = R-controlled A", "/kär/"),
           ("farm", "f (/f/), ar (/är/), m (/m/)", "AR in middle", "/färm/"),
           ("star", "s (/s/), t (/t/), ar (/är/)", "AR at end", "/stär/")],
    "or": [("for", "f (/f/), or (/or/)", "OR = R-controlled O", "/for/"),
           ("corn", "c (/k/), or (/or/), n (/n/)", "OR in middle", "/korn/"),
           ("sort", "s (/s/), or (/or/), t (/t/)", "OR before t", "/sort/")],
    "er": [("her", "h (/h/), er (/er/)", "ER at end", "/her/"),
           ("sister", "s (/s/), i (/ĭ/), s (/s/), t (/t/), er (/er/)", "ER at end", "sĭs-ter"),
           ("under", "u (/ŭ/), n (/n/), d (/d/), er (/er/)", "ER at end", "ŭn-der")],
    "oi": [("coin", "c (/k/), oi (/oi/), n (/n/)", "OI — never at end", "/koin/"),
           ("oil", "oi (/oi/), l (/l/)", "OI at start", "/oil/"),
           ("join", "j (/j/), oi (/oi/), n (/n/)", "OI in middle", "/join/")],
    "oy": [("boy", "b (/b/), oy (/oi/)", "OY at end — Rule 3", "/boi/"),
           ("toy", "t (/t/), oy (/oi/)", "OY at end", "/toi/"),
           ("enjoy", "e (/ĕ/), n (/n/), j (/j/), oy (/oi/)", "OY at end of base", "en-joy")],
    "ai": [("rain", "r (/r/), ai (/ā/), n (/n/)", "AI never at end — Rule 3", "/rān/"),
           ("sail", "s (/s/), ai (/ā/), l (/l/)", "AI in middle", "/sāl/"),
           ("train", "t (/t/), r (/r/), ai (/ā/), n (/n/)", "AI in middle", "/trān/")],
    "ay": [("day", "d (/d/), ay (/ā/)", "AY at end — Rule 9", "/dā/"),
           ("play", "p (/p/), l (/l/), ay (/ā/)", "AY at end", "/plā/"),
           ("stay", "s (/s/), t (/t/), ay (/ā/)", "AY at end", "/stā/")],
    "ch": [("chin", "ch (/ch/), i (/ĭ/), n (/n/)", "CH = /ch/ (most common)", "/chĭn/"),
           ("much", "m (/m/), u (/ŭ/), ch (/ch/)", "CH at end", "/mŭch/"),
           ("school", "s (/s/), ch (/k/), oo (/ü/), l (/l/)", "CH says /k/ (Greek)", "skül")],
    "wh": [("when", "wh (/hw/), e (/ĕ/), n (/n/)", "WH always /hw/", "/hwĕn/"),
           ("which", "wh (/hw/), i (/ĭ/), ch (/ch/)", "WH + CH in same word!", "/hwĭch/"),
           ("white", "wh (/hw/), i (/ī/), t (/t/), e — silent E (12.1)", "WH + silent E", "/hwīt/")],
    "ea": [("eat", "ea (/ē/), t (/t/)", "EA = /ē/ (most common)", "/ēt/"),
           ("head", "h (/h/), ea (/ĕ/), d (/d/)", "EA = /ĕ/ (second sound)", "/hĕd/"),
           ("great", "g (/g/), r (/r/), ea (/ā/), t (/t/)", "EA = /ā/ (rare!)", "/grāt/")],
    "ow": [("cow", "c (/k/), ow (/ow/)", "OW = /ow/", "/kow/"),
           ("snow", "s (/s/), n (/n/), ow (/ō/)", "OW = /ō/ (second sound)", "/snō/"),
           ("how", "h (/h/), ow (/ow/)", "OW = /ow/", "/how/")],
    "ou": [("out", "ou (/ow/), t (/t/)", "OU = /ow/ (most common)", "/owt/"),
           ("you", "y (/y/), ou (/ö/)", "OU = /ö/", "/yö/"),
           ("touch", "t (/t/), ou (/ŭ/), ch (/ch/)", "OU = /ŭ/", "/tŭch/")],
    "oo": [("book", "b (/b/), oo (/ö/), k (/k/)", "OO = /ö/", "/bök/"),
           ("food", "f (/f/), oo (/ü/), d (/d/)", "OO = /ü/", "/füd/"),
           ("floor", "f (/f/), l (/l/), oo (/ō/), r (/r/)", "OO = /ō/ (rare!)", "/flōr/")],
    "ed": [("wanted", "w (/w/), a (/ŏ/), n (/n/), t (/t/), ed (/ed/)", "ED = /ed/ after D/T", "wŏn-ted"),
           ("played", "p (/p/), l (/l/), ay (/ā/), ed (/d/)", "ED = /d/ after voiced", "/plād/"),
           ("fished", "f (/f/), i (/ĭ/), sh (/sh/), ed (/t/)", "ED = /t/ after unvoiced", "/fĭsht/")],
    "igh": [("light", "l (/l/), igh (/ī/), t (/t/)", "Rule 28: GH silent after I", "/līt/"),
            ("night", "n (/n/), igh (/ī/), t (/t/)", "Rule 28: GH silent", "/nīt/"),
            ("right", "r (/r/), igh (/ī/), t (/t/)", "Rule 28: GH silent", "/rīt/")],
    "aw": [("saw", "s (/s/), aw (/ä/)", "AW at end — Rule 3", "/sä/"),
           ("draw", "d (/d/), r (/r/), aw (/ä/)", "AW at end", "/drä/"),
           ("law", "l (/l/), aw (/ä/)", "AW at end", "/lä/")],
    "au": [("cause", "c (/k/), au (/ä/), s (/s/), e — silent E (12.9)", "AU never at end", "/käz/"),
           ("haul", "h (/h/), au (/ä/), l (/l/)", "AU in middle", "/häl/"),
           ("August", "au (/ä/), g (/g/), u (/ŭ/), s (/s/), t (/t/)", "AU at start", "ä-gŭst")],
    "ir": [("girl", "g (/g/), ir (/er/), l (/l/)", "IR = /er/", "/gerl/"),
           ("bird", "b (/b/), ir (/er/), d (/d/)", "IR = /er/", "/berd/"),
           ("first", "f (/f/), ir (/er/), s (/s/), t (/t/)", "IR = /er/", "/ferst/")],
    "ur": [("hurt", "h (/h/), ur (/er/), t (/t/)", "UR = /er/", "/hert/"),
           ("turn", "t (/t/), ur (/er/), n (/n/)", "UR = /er/", "/tern/"),
           ("burn", "b (/b/), ur (/er/), n (/n/)", "UR = /er/", "/bern/")],
    "oa": [("boat", "b (/b/), oa (/ō/), t (/t/)", "OA = /ō/, never at end", "/bōt/"),
           ("road", "r (/r/), oa (/ō/), d (/d/)", "OA in middle", "/rōd/"),
           ("soap", "s (/s/), oa (/ō/), p (/p/)", "OA in middle", "/sōp/")],
    "ear": [("learn", "l (/l/), ear (/er/), n (/n/)", "EAR = /er/", "/lern/"),
            ("earth", "ear (/er/), th (/th/)", "EAR = /er/", "/erth/"),
            ("early", "ear (/er/), l (/l/), y (/ē/)", "EAR = /er/ at start", "er-lē")],
}

# ── TEMPLATES ───────────────────────────────────────────────────────

SHORT_VOWEL_TEMPLATE = """# Lesson {lesson_num}: Short Vowel {vowel_upper} — /{vowel_sound}/

**Stage 2** · Lesson {lesson_num} · vowel-concept

---

## Warm-Up: Phonogram Flash Review

> Flash all 26 a-z phonograms. Child says ALL sounds within 2 seconds. Focus especially on **{vowel}**.

| Review all a-z |
|----------------|
| a, d, g, c, o, qu, s, t, i, p, u, j, r, n, m, e, l, b, h, k, f, v, w, x, y, z |

---

## New Learning: The Short Sound of **{vowel_upper}**

### Meet /{vowel_sound}/

**{vowel_upper}** has multiple sounds. The short sound of **{vowel}** is /{vowel_sound}/.

{vowel_description}

<div class="phonogram">{vowel}</div>

### The Breve Mark ˘

When {vowel} says its short sound /{vowel_sound}/, we can mark it with a **breve** (˘) — a little smile above the letter. This helps us remember it's the short sound.

> {vowel}̄  = long &nbsp;&nbsp;|&nbsp;&nbsp; {vowel}̆ = short (breve)

### Short {vowel_upper} Words

| Word | Sounds | Meaning |
|------|--------|---------|
{word_table}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

> **At this stage:** The teacher may need to help by saying each sound slowly. Child writes one phonogram at a time, saying the sound as they write.

---

## Reading Practice

Read these words sound by sound, then blend:

> {read_words}

---

## Dictation

Adult reads these sentences aloud. Child writes them.

> {dictation}

---

## Quick Check

1. What is the short sound of **{vowel}**? *(/{vowel_sound}/)*
2. What mark do we use to show a short vowel? *(A breve ˘ — like a smile)*
3. Say a word with short /{vowel_sound}/ that we haven't used today.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find {items} things in your house with the short /{vowel_sound}/ sound.*
"""

MULTI_PG_TEMPLATE = """# Lesson {lesson_num}: Phonogram {pg}

**Stage 2** · Lesson {lesson_num} · phonogram-intro

---

## Warm-Up: Phonogram Flash Review

> Flash all known phonograms (a-z + multi-letter). Child says ALL sounds within 2 seconds.

| Phonograms to review |
|----------------------|
| All 26 single: a, d, g, c, o, qu, s, t, i, p, u, j, r, n, m, e, l, b, h, k, f, v, w, x, y, z |

| Multi-letter so far |
|---------------------|
| {known_multi} |

---

## New Learning: The Phonogram **{pg}**

### What Is **{pg}**?

<div class="phonogram">{pg}</div>

**{pg}** says {sound_count} sound{s_plural}: {sounds}

{tip}

{rule_section}
### Sound Table

| Sound | Example Words |
|-------|--------------|
{example_rows}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{word_rows}

---

## Reading Practice

Read these words sound by sound, then blend:

> {read_words}

Read these sentences:

> {sentences}

---

## Handwriting Practice

Write each word once. Underline the **{pg}** in each word.

{write_words}

---

## Quick Check

1. What did you learn today? *(The phonogram {pg} — it says {sounds})*
2. Is {pg} a single-letter or multi-letter phonogram? *(Multi-letter — {letter_count} letters that make one sound!)*
{extra_questions}
---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Flash your **{pg}** card 5 times. Find **{pg}** in a book — how many can you find?*
"""

RULE_TEMPLATE = """# Lesson {lesson_num}: Rule {rule_num} — {rule_name}

**Stage 2** · Lesson {lesson_num} · rule-intro

---

## Warm-Up: Phonogram Flash Review

> Flash all known phonograms. Child says ALL sounds within 2 seconds.

| Phonograms to review |
|----------------------|
| All a-z + {multi_list} |

---

## New Learning: Rule {rule_num}

### The Rule

> **{rule_statement}**

### Why This Rule Exists

{explanation}

### Examples

{examples}

### Let's Find the Rule in Action

For each word below, identify how Rule {rule_num} applies:

| Word | How Rule {rule_num} Works Here |
|------|-------------------------------|
{analysis_rows}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{word_rows}

---

## Reading Practice

Read these words sound by sound:

> {read_words}

---

## Quick Check

1. What is Rule {rule_num}? *(Restate in your own words.)*
2. Why does English need Rule {rule_num}? *(Explain the reason.)*
3. Give an example of Rule {rule_num} that we haven't used today.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find 3 words in a book that follow Rule {rule_num}. Write them down!*
"""

HF_WORD_TEMPLATE = """# Lesson {lesson_num}: High-Frequency Words — Set {set_num}

**Stage 2** · Lesson {lesson_num} · hf-word

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

| Review all known |
|------------------|
| {multi_list} |

---

## Important: These Are NOT Sight Words

In many reading programs, these words are called "sight words" — words you just memorize. In Logic of English, **every word can be explained.** You are going to learn WHY each word is spelled the way it is.

> **There are no true sight words.** Every word follows the rules when you know all the phonograms and spelling rules.

---

## Today's High-Frequency Words

These words appear in books ALL the time. Learning them now makes reading easier!

{word_sections}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

---

## Reading Practice

Read these sentences containing our high-frequency words:

> {sentences}

---

## Dictation

Adult reads these sentences. Child writes them.

> {dictation_sentences}

---

## Quick Check

1. Why don't we call these "sight words"? *(Because every word can be explained with phonograms and rules!)*
2. What is say-to-spell and why do we use it? *(Say-to-spell is pronouncing a word with clear vowel sounds to help us remember its spelling.)*
3. Spell "{check_word}" from dictation.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find today's words in a book. Count how many times you see each one!*
"""

REVIEW_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 2** · Lesson {lesson_num} · review

---

## Warm-Up: Speed Flash

> Flash ALL phonograms learned so far. Goal: child says ALL sounds within 2 seconds per card.

| Phonograms to review |
|----------------------|
| {pg_list} |

---

## Game 1: Phonogram Bingo

Pick 6 phonograms from the list above and write one in each box of a 3×2 grid on your whiteboard. Adult calls out a SOUND. If you have the phonogram that makes that sound, cross it off!

| ☐ | ☐ | ☐ |
|---|---|---|
| ☐ | ☐ | ☐ |

---

## Game 2: Build the Word

Adult says a word. Child builds it using phonogram tiles (or writes it). Underline any multi-letter phonograms.

| Word | Multi-letter PG? | Rules? |
|------|-----------------|--------|
{game2_rows}

---

## Game 3: Which One Wins?

Adult says two phonograms. Child picks the one that makes a given sound.

{sound_choices}

---

## Spelling Challenge

Spell these words from dictation. Take your time — sound each one out.

> {challenge_words}

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Play "Which One Wins?" with a family member!*
"""

WORD_BUILD_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 2** · Lesson {lesson_num} · word-building

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

| Phonograms to review |
|----------------------|
| All 26 a-z |

---

## New Learning: {learning_title}

### What We're Building Today

{description}

{variation_note}
### Word Builder Chart

For each word, say the sounds, then write the phonograms:

| Word | Sound 1 | Sound 2 | Sound 3 | Sound 4 | Phonograms |
|------|---------|---------|---------|---------|------------|
{word_builder_rows}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

---

## Reading Practice

Read these words sound by sound, then blend:

> {read_words}

Read these sentences:

> {sentences}

---

## Quick Check

1. What pattern did we practice today? *(Answers vary — child describes the word pattern.)*
2. Build the word "{check_word}" — tell me each sound, then write it.
3. What do you notice about all the vowel sounds in today's words? *(They are short vowels!)*

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Build 3 words from today's pattern on your whiteboard.*
"""

SPELLING_ANALYSIS_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 2** · Lesson {lesson_num} · spelling-analysis

---

## Warm-Up: Phonogram Flash Review

> Flash all known phonograms. Focus on {focus_pgs}.

| Phonograms to review |
|----------------------|
| All 26 a-z + {multi_list} |

---

## Spelling Analysis Routine

Follow the 5-step routine for EVERY word:

1. **Hear & Say** — Adult says the word, uses it in a sentence. Child repeats.
2. **Segment** — Child breaks the word into individual sounds. Adult holds up fingers (1 finger = 1-letter PG, 2 fingers = multi-letter).
3. **Write** — Child writes the word while sounding it out.
4. **Analyze** — Underline multi-letter phonograms. Name any spelling rules.
5. **Read** — Child reads the word sound by sound, then blends.

---

## Spelling Analysis: {focus_title}

{intro_text}

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{word_rows}

---

## Bonus Words (Challenge!)

If you spelled all the main words correctly, try these:

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{bonus_rows}

---

## Reading Practice

Read these sentences:

> {sentences}

---

## Quick Check

1. Which multi-letter phonogram did we use most today?
2. What new rule(s) did you apply?
3. Spell "{check_word}" from dictation.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Choose 2 words from today's lesson. Spell them for a family member and explain the phonograms you used.*
"""

READER_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 2** · Lesson {lesson_num} · reader

---

## Warm-Up: Phonogram Flash Review

> Quick flash of phonograms used in today's story.

| Phonograms to review |
|----------------------|
| {review_pgs} |

---

## Warm-Up Words — Read These First

Read each word sound by sound BEFORE reading the story:

> {warmup_words}

---

## Story: {story_title}

{story_text}

---

## After Reading: Talk About It

{talk_about}

---

## Spelling Practice

Find these words in the story. Write them and underline the phonograms:

| Word from Story | Phonograms |
|-----------------|------------|
{story_words_table}

---

## Quick Check

1. What was the story about?
2. What new phonogram did you see in the story?
3. Write your favorite word from the story. Underline its phonograms.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Read this story aloud to a family member!*
"""

ASSESSMENT_TEMPLATE = """# Lesson {lesson_num}: {title}

**Stage 2** · Lesson {lesson_num} · assessment

---

## Assessment Overview

{overview}

---

## Part 1: Phonogram Sounds

> Flash each phonogram card. Child says ALL sounds in frequency order within 2 seconds.

| Phonogram | Sounds | ✓ / Needs Work |
|-----------|--------|----------------|
{pg_checklist}

**Score:** __ / {pg_total}

---

## Part 2: Word Reading

> Child reads each word aloud. Sound-by-sound blending is OK.

| Word | ✓ |
|------|---|
{reading_checklist}

**Score:** __ / {reading_total}

---

## Part 3: Spelling (Dictation)

> Adult dictates each word. Child writes it independently.

| Word | ✓ |
|------|---|
{spelling_checklist}

**Score:** __ / {spelling_total}

---

## Part 4: Rule Knowledge

> Adult asks the question. Child explains in their own words.

| Rule | Question | ✓ / Needs Work |
|------|----------|----------------|
{rule_checklist}

**Score:** __ / {rule_total}

---

## Results

| Section | Score | Pass? |
|---------|-------|-------|
| Phonogram Sounds | __ / {pg_total} | |
| Word Reading | __ / {reading_total} | |
| Spelling | __ / {spelling_total} | |
| Rule Knowledge | __ / {rule_total} | |

**Overall:** __ / {overall_total}

---

## Next Steps

{next_steps}

---

*Great work! Every assessment shows what you've learned and what to practice next.*
"""

# ── HELPERS ─────────────────────────────────────────────────────────

def known_multi_str(num):
    multi = known_multi_for(num)
    if not multi:
        return "(No multi-letter phonograms yet)"
    return ", ".join(multi)

def multi_list_str(num):
    multi = known_multi_for(num)
    if not multi:
        return "(none yet)"
    return ", ".join(multi)

def next_title(num):
    titles = {
        1: "Review Stage 1 Phonograms", 2: "Short Vowel a", 3: "Short Vowel i",
        4: "Short Vowel o", 5: "Short Vowel u", 6: "Short Vowel e",
        7: "VC Words", 8: "CVC with Continuant Consonants",
        9: "CVC with Stop Consonants", 10: "All CVC Combinations",
        11: "Phonogram sh", 12: "Phonogram th", 13: "Phonogram ck",
        14: "Spelling Analysis: sh th ck", 15: "Phonogram ee",
        16: "CCVC Blends", 17: "CVCC Blends", 18: "CCVCC Blends",
        19: "Phonogram ng", 20: "Phonogram ar", 21: "Phonogram or",
        22: "Phonogram er", 23: "Review: First 8 Multi-Letter",
        24: "Mid-Stage 2 Assessment", 25: "Phonogram oi",
        26: "Phonogram oy", 27: "Rule 3: No I U V J at End",
        28: "Phonogram ai", 29: "Phonogram ay",
        30: "Rule 9: AY at End", 31: "Spelling: oi oy ai ay",
        32: "Phonogram ch", 33: "Phonogram wh", 34: "Phonogram ea",
        35: "Spelling: ch wh ea", 36: "Phonogram ow",
        37: "Phonogram ou", 38: "Rule 4: Long at End",
        39: "Open Syllables", 40: "Phonogram oo",
        41: "Phonogram ed", 42: "Rule 20: -ED",
        43: "Phonogram igh", 44: "Phonogram aw", 45: "Phonogram au",
        46: "Phonogram ir", 47: "Phonogram ur",
        48: "Review: ow to ur", 49: "Phonogram oa",
        50: "Phonogram ear", 51: "HF Words Set 1",
        52: "HF Words Set 2", 53: "HF Words Set 3",
        54: "Rule 30: Floss Rule", 55: "Reader: Fred the Frog",
        56: "Stage 2 Mastery Check",
    }
    return titles.get(num, f"Lesson {num}")

def next_num(num):
    return num + 1

# ── BUILDERS ────────────────────────────────────────────────────────

def build_short_vowel(num, vowel, vsound, description, words_list, vtype="default"):
    vowel_upper = vowel.upper()
    word_table = "\n".join(f"| {w} | {' '.join('/'+c+'/' for c in w)} | — |" for w in words_list[:8])
    read_words = " &nbsp;&nbsp; ".join(words_list)

    spelling_words = words_list[:3]
    spelling_rows = "\n".join(
        f"| {w} | {', '.join(p + ' (/' + vsound + '/)' if p == vowel else p + ' (/' + p + '/)' for p in w)} | Short vowel — closed syllable | /{''.join(w)}/ |"
        for w in spelling_words
    )

    items = "3" if len(words_list) <= 5 else "5"
    dictation = "The " + words_list[0] + " is big." if words_list else ""

    return SHORT_VOWEL_TEMPLATE.format(
        lesson_num=num, vowel_upper=vowel_upper, vowel_sound=vsound, vowel=vowel,
        vowel_description=description, word_table=word_table,
        spelling_rows=spelling_rows, read_words=read_words,
        dictation=dictation, items=items,
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )

def build_multi_pg(num, pg):
    d = MULTI_PGS[pg]
    sounds = d["sounds"]
    sc = d["sound_count"]
    s_plural = "s" if sc > 1 else ""
    examples = d["examples"]
    example_rows = "\n".join(f"| /{e[0]}/ | {e[1]} |" for e in examples)
    tip = d["tip"]
    rule = d.get("rule")

    rule_section = ""
    if rule:
        rule_section = f"\n> **Spelling Rule:** {rule}\n"

    words = PG_SPELLING_WORDS.get(pg, [("—", "—", "—", "—")])
    word_rows = "\n".join(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in words)

    read_words = " &nbsp;&nbsp; ".join(w[0] for w in words)
    sentences = "The " + words[0][0] + " is here." if words else ""
    write_words = " &nbsp;&nbsp; ".join(w[0] for w in words)

    extra_q = ""
    if rule:
        extra_q = f"3. What rule did we learn with {pg}? *(Restate in your own words.)*\n"
    else:
        extra_q = f"3. What is the most common sound of {pg}? *({sounds.split()[0]})*\n"

    return MULTI_PG_TEMPLATE.format(
        lesson_num=num, pg=pg, sounds=sounds, sound_count=sc, s_plural=s_plural,
        example_rows=example_rows, tip=tip, rule_section=rule_section,
        word_rows=word_rows, read_words=read_words, sentences=sentences,
        write_words=write_words, known_multi=known_multi_str(num),
        letter_count=len(pg), extra_questions=extra_q,
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )

def build_rule(num, rule_key):
    r = RULES[rule_key]
    rn = r["number"]
    words = r.get("words_for_spelling", [])

    analysis_rows = "\n".join(
        f"| {w} | Rule {rn} applies because... |" for w in words[:6]
    )

    word_rows = "\n".join(
        f"| {w} | (sound out) | Rule {rn} | /{w}/ |" for w in words[:4]
    )

    return RULE_TEMPLATE.format(
        lesson_num=num, rule_num=rn, rule_name=r["name"],
        rule_statement=r["statement"], explanation=r["explanation"],
        examples=r["examples"], analysis_rows=analysis_rows,
        word_rows=word_rows, read_words=" &nbsp;&nbsp; ".join(words),
        multi_list=multi_list_str(num),
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )

def build_hf_words(num, set_num, words_data, sentences, dictation_sentences, check_word):
    word_sections = ""
    for w, explanation in words_data:
        word_sections += f"### {w}\n\n{explanation}\n\n"

    spelling_rows = "\n".join(
        f"| {w} | (see explanation above) | (see above) | (see above) |"
        for w, _ in words_data
    )

    return HF_WORD_TEMPLATE.format(
        lesson_num=num, set_num=set_num, word_sections=word_sections,
        spelling_rows=spelling_rows, sentences=sentences,
        dictation_sentences=dictation_sentences, check_word=check_word,
        multi_list=multi_list_str(num),
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )

def build_word_building(num, title, learning_title, description, words, variation_note="", check_word=""):
    word_builder_rows = "\n".join(
        f"| {w} | {' | '.join('/'+c+'/' for c in w)} | {' | '.join(c for c in w)} |" if len(w) == 3 else
        f"| {w} | {' | '.join('/'+c+'/' for c in w)} | {' | '.join(c for c in w)} |"
        for w in words[:10]
    )

    spelling_words = words[:3]
    spelling_rows = "\n".join(
        f"| {w} | {', '.join(p + ' (/' + p + '/)' for p in w)} | Short vowel | /{''.join(w)}/ |"
        for w in spelling_words
    )

    sentences = f"{words[0]} and {words[1]} are fun." if len(words) >= 2 else ""
    cw = check_word or (words[0] if words else "cat")

    return WORD_BUILD_TEMPLATE.format(
        lesson_num=num, title=title, learning_title=learning_title,
        description=description, variation_note=variation_note,
        word_builder_rows=word_builder_rows, spelling_rows=spelling_rows,
        read_words=" &nbsp;&nbsp; ".join(words[:12]), sentences=sentences,
        check_word=cw,
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )

def build_spelling_analysis(num, title, focus_title, focus_pgs, intro, words_data, bonus_words, sentences, check_word):
    word_rows = "\n".join(
        f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in words_data
    )
    bonus_rows = "\n".join(
        f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in bonus_words
    )
    return SPELLING_ANALYSIS_TEMPLATE.format(
        lesson_num=num, title=title, focus_title=focus_title,
        focus_pgs=focus_pgs, intro_text=intro,
        word_rows=word_rows, bonus_rows=bonus_rows,
        sentences=sentences, check_word=check_word,
        multi_list=multi_list_str(num),
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )

def build_review(num, title, pgs, game2_rows, sound_choices, challenge_words):
    return REVIEW_TEMPLATE.format(
        lesson_num=num, title=title, pg_list=", ".join(pgs),
        game2_rows=game2_rows, sound_choices=sound_choices,
        challenge_words=", ".join(challenge_words),
        next_num=next_num(num), next_title=next_title(next_num(num)),
    )


# ── MAIN GENERATOR ──────────────────────────────────────────────────

def generate_all():
    # ── Lesson 1: Review Stage 1 Phonograms ──
    yield 1, build_review(
        1, "Review Stage 1 Phonograms",
        ["a","d","g","c","o","qu","s","t","i","p","u","j","r","n","m","e","l","b","h","k","f","v","w","x","y","z"],
        "| cat | c, a, t | No — all single |\n| ship | sh, i, p | Yes — sh! |\n| dog | d, o, g | No |\n| quit | qu, i, t | Yes — qu! |",
        "- /ă/ — a or o? *a!*\n- /k/ — c or k? *Both can!*\n- /j/ — j or g? *Both can!*\n- /kw/ — q alone, qu, or k? *qu!*",
        ["cat", "dog", "sun", "quit", "jam", "zip"]
    )

    # ── Lessons 2-6: Short Vowels ──
    yield 2, build_short_vowel(2, "a", "ă",
        "The short sound of A is /ă/ — like the first sound in 'apple.' Your mouth is open, your tongue is low. Try singing it: /ăăăă/. You can't hold it as long as /ā/, can you? That's why it's called 'short.'",
        ["cat","hat","bat","rat","sat","mat","fat","pat","cap","map","tap","lap","nap","sap","gap","bag","tag","rag","wag","sag","had","bad","mad","sad","dad","pad","lad","fad"])

    yield 3, build_short_vowel(3, "i", "ĭ",
        "The short sound of I is /ĭ/ — like the first sound in 'igloo.' Your mouth is slightly open, your tongue is high in the front. Most children find /ĭ/ easier to say than /ĕ/. Say it: /ĭ/ (short and crisp!).",
        ["sit","fit","hit","bit","pit","lit","kit","wit","it","in","if","is","big","dig","fig","pig","rig","wig","jig","him","rim","dim","Tim","Jim","pin","fin","tin","win","bin","sin","tip","hip","lip","rip","sip","zip"])

    yield 4, build_short_vowel(4, "o", "ŏ",
        "The short sound of O is /ŏ/ — like the first sound in 'octopus.' Your mouth makes a round circle. Imagine you're surprised: 'O!' but shorter. Say it: /ŏ/.",
        ["hot","pot","not","got","dot","lot","rot","cot","jot","top","hop","pop","mop","cop","bop","dog","log","fog","hog","jog","bog","on","ox","box","fox","sox","mom","Tom","rod","nod","sod","pod","cod","god"])

    yield 5, build_short_vowel(5, "u", "ŭ",
        "The short sound of U is /ŭ/ — like the first sound in 'up' or 'umbrella.' Your mouth is relaxed and slightly open. Point UP when you say /ŭ/!",
        ["up","cup","pup","sup","us","bus","mud","bud","dud","bug","rug","hug","jug","lug","tug","mug","dug","fun","run","sun","bun","gun","nun","pun","cut","hut","nut","rut","but","gut","jut","tut","put","hum","gum","sum","mum","rum"])

    yield 6, build_short_vowel(6, "e", "ĕ",
        "The short sound of E is /ĕ/ — like the first sound in 'egg' or 'elephant.' Your mouth is open a little. This is often the hardest short vowel for children, so practice it often! Think of a creaky door: 'ehhh.' Say it: /ĕ/.",
        ["bed","red","fed","led","wed","Ted","Ned","get","set","let","met","pet","vet","wet","jet","net","bet","yet","hen","pen","ten","men","den","Ben","Ken","Len","leg","peg","beg","Meg","peg","hem","gem","them"])

    # ── Lessons 7-10: Word Building ──
    yield 7, build_word_building(7, "VC Words: at in on up it", "Two-Letter Words",
        "Today we build the smallest real words — just two letters: a vowel and a consonant (VC). These are the foundation of all reading!",
        VC_WORDS, check_word="at")

    yield 8, build_word_building(8, "CVC with Continuant Consonants", "CVC Words — Easy First Sounds",
        "Continuant consonants are sounds you can STRETCH: /m/, /n/, /f/, /s/, /l/, /r/. Words that start with these are easier to blend because you can hold the first sound while your brain finds the next one.",
        CVC_CONTINUANT,
        variation_note="> **Tip:** Stretch the first sound: /mmmmmm/ /ă/ /n/ → man. It's much easier than stopping and starting.\n",
        check_word="man")

    yield 9, build_word_building(9, "CVC with Stop Consonants", "CVC Words — Stop Sounds",
        "Stop consonants are sounds you CAN'T stretch: /k/, /d/, /g/, /p/, /t/, /b/. Words that start with these are harder to blend. Don't add 'uh' (/ə/) to the end — say /k/ not /kuh/!",
        CVC_STOP,
        variation_note="> **Tip:** Don't add 'uh' to stop sounds! /k/ is crisp and quick — not /kuh/. Say the sound, then go straight to the next one.\n",
        check_word="cat")

    yield 10, build_word_building(10, "All CVC Combinations", "All CVC Words Together",
        "Now we can read ANY CVC word with short vowels! Today we practice mixing continuant and stop consonants with all five short vowels.",
        CVC_ALL[:15],
        variation_note="> **You can now read over 500 CVC words!** Every new phonogram you learn unlocks hundreds more.\n",
        check_word="jam")

    # ── Lessons 11-22: Multi-Letter Phonograms (First Wave) ──

    pg_sequence = [
        (11, "sh"), (12, "th"), (13, "ck"),
        (15, "ee"), (19, "ng"), (20, "ar"), (21, "or"), (22, "er"),
    ]
    for num, pg in pg_sequence:
        yield num, build_multi_pg(num, pg)

    # ── Lesson 14: Spelling Analysis sh th ck ──
    sa_words_14 = [
        ("ship", "sh (/sh/), i (/ĭ/), p (/p/)", "sh = two letters", "/shĭp/"),
        ("that", "th (/th/ voiced), a (/ă/), t (/t/)", "th voiced", "/thăt/"),
        ("back", "b (/b/), a (/ă/), ck (/k/)", "Rule 26: CK after short vowel", "/băk/"),
        ("fish", "f (/f/), i (/ĭ/), sh (/sh/)", "sh at end", "/fĭsh/"),
        ("duck", "d (/d/), u (/ŭ/), ck (/k/)", "Rule 26", "/dŭk/"),
    ]
    yield 14, build_spelling_analysis(14, "Spelling Analysis: sh th ck",
        "sh, th, ck", "sh, th, ck",
        "Today we practice spelling with our first three multi-letter phonograms. Use the 5-step routine for each word.",
        sa_words_14,
        [("thin", "th (/th/ unvoiced), i (/ĭ/), n (/n/)", "th unvoiced — no buzz", "/thĭn/"),
         ("stick", "s (/s/), t (/t/), i (/ĭ/), ck (/k/)", "Rule 26", "/stĭk/")],
        "The ship is big. That duck is back. I fish with Dad.",
        "ship")

    # ── Lessons 16-18: Consonant Blends ──
    yield 16, build_word_building(16, "CCVC: Beginning Blends", "Words That Start with Two Consonants",
        "When two consonants come together at the start of a word, we blend them quickly. The first consonant 'slides' into the second. Try /s/ + /l/ = /sl/ — now add /ĭ/ /p/ = slip!",
        CCVC_BLENDS,
        variation_note="> **Blend tip:** Say the first two sounds together quickly: /st/, /fr/, /sl/, /cr/, /sw/. Then add the rest.\n",
        check_word="stop")

    yield 17, build_word_building(17, "CVCC: Ending Blends", "Words That End with Two Consonants",
        "Consonant blends can also come at the END of words. Listen carefully for both final sounds — they can be tricky! /h/ /ă/ /n/ /d/ → hand.",
        CVCC_BLENDS,
        variation_note="> **Listen carefully:** The last two sounds are separate — don't skip one! 'hand' has 4 sounds: /h/ /ă/ /n/ /d/.\n",
        check_word="hand")

    yield 18, build_word_building(18, "CCVCC: Both Blends", "Blends at BOTH Ends!",
        "The ultimate blending challenge — words with consonant blends at the beginning AND the end. Five sounds to blend! /p/ /l/ /ă/ /n/ /t/ → plant.",
        CCVCC_BLENDS,
        variation_note="> **Five sounds!** These are the longest one-syllable words: /s/+/t/+/ă/+/m/+/p/ = stamp. Count them on your fingers.\n",
        check_word="plant")

    # ── Lesson 23: Review first wave ──
    first_wave_pgs = ["sh","th","ck","ee","ng","ar","or","er"]
    yield 23, build_review(23, "Review: sh th ck ee ng ar or er",
        sorted(list(SINGLE_PGS.keys())) + first_wave_pgs,
        "| ship | sh + i + p | sh |\n| back | b + a + ck | ck — Rule 26 |\n| see | s + ee | ee — always /ē/ |\n| sing | s + i + ng | ng |\n| car | c + ar | ar = R-controlled |\n| for | f + or | or = R-controlled |\n| her | h + er | er at end |",
        "- /sh/ — sh or s? *sh!*\n- /ē/ — ee or e? *ee!*\n- /ng/ — ng or n? *ng!*\n- /är/ — ar or a? *ar!*\n- /er/ — er, ir, or ur? *er is most common!*",
        ["ship","that","back","see","sing","car","for","her"])

    # ── Lesson 24: Mid-Stage 2 Assessment ──
    yield 24, build_mid_assessment()

    # ── Lessons 25-50: Second Wave Multi-Letter PGs + Rules ──

    second_wave = [
        (25, "oi"), (26, "oy"),
        (28, "ai"), (29, "ay"),
        (32, "ch"), (33, "wh"), (34, "ea"),
        (36, "ow"), (37, "ou"),
        (40, "oo"), (41, "ed"),
        (43, "igh"), (44, "aw"), (45, "au"),
        (46, "ir"), (47, "ur"),
        (49, "oa"), (50, "ear"),
    ]
    for num, pg in second_wave:
        yield num, build_multi_pg(num, pg)

    # ── Lesson 27: Rule 3 ──
    yield 27, build_rule(27, "3")

    # ── Lesson 30: Rule 9 ──
    yield 30, build_rule(30, "9")

    # ── Lesson 31: Spelling Analysis oi oy ai ay ──
    sa_words_31 = [
        ("coin", "c (/k/), oi (/oi/), n (/n/)", "OI never at end — Rule 3", "/koin/"),
        ("boy", "b (/b/), oy (/oi/)", "OY at end — Rule 3", "/boi/"),
        ("rain", "r (/r/), ai (/ā/), n (/n/)", "AI never at end — Rule 3", "/rān/"),
        ("day", "d (/d/), ay (/ā/)", "AY at end — Rule 9", "/dā/"),
        ("toy", "t (/t/), oy (/oi/)", "OY at end", "/toi/"),
    ]
    yield 31, build_spelling_analysis(31, "Spelling Analysis: oi oy ai ay",
        "oi, oy, ai, ay", "oi/oy and ai/ay Pairs",
        "Each of these pairs makes the same sound — one is for the middle of a word, one is for the end. Rule 3 explains why!",
        sa_words_31,
        [("join", "j (/j/), oi (/oi/), n (/n/)", "OI in middle", "/join/"),
         ("stay", "s (/s/), t (/t/), ay (/ā/)", "AY at end", "/stā/")],
        "The boy has a coin. It rains all day. Stay and play!",
        "boy")

    # ── Lesson 35: Spelling Analysis ch wh ea ──
    sa_words_35 = [
        ("chin", "ch (/ch/), i (/ĭ/), n (/n/)", "CH = /ch/", "/chĭn/"),
        ("when", "wh (/hw/), e (/ĕ/), n (/n/)", "WH = /hw/", "/hwĕn/"),
        ("eat", "ea (/ē/), t (/t/)", "EA = /ē/", "/ēt/"),
        ("head", "h (/h/), ea (/ĕ/), d (/d/)", "EA = /ĕ/ (second sound)", "/hĕd/"),
        ("much", "m (/m/), u (/ŭ/), ch (/ch/)", "CH at end", "/mŭch/"),
    ]
    yield 35, build_spelling_analysis(35, "Spelling Analysis: ch wh ea",
        "ch, wh, ea", "ch, wh, ea",
        "CH has three sounds (but /ch/ is most common). WH says /hw/. EA has three sounds (/ē/ is most common).",
        sa_words_35,
        [("school", "s (/s/), ch (/k/), oo (/ü/), l (/l/)", "CH = /k/ (Greek)", "skül"),
         ("white", "wh (/hw/), i (/ī/), t (/t/), e — silent E", "WH + silent E", "/hwīt/")],
        "When do we eat? Much food is on the chin. My head is big!",
        "when")

    # ── Lesson 38: Rule 4 ──
    yield 38, build_rule(38, "4")

    # ── Lesson 39: Open Syllables ──
    yield 39, build_word_building(39, "Open Syllable Words", "When a Syllable Ends with a Vowel",
        "An open syllable ends with a vowel. The vowel says its LONG sound! go, he, me, no, so, she, we, be. This is Rule 4 in action.",
        ["go","no","so","he","me","she","we","be","hi","by","my","try","fly","sky","cry","dry","fry","why","baby","lady","lazy","crazy","tiny"],
        variation_note="> **Open = vowel not 'closed' by a consonant.** In 'go,' the syllable ends with O, so O says /ō/. In 'got,' the T closes the syllable, so O says /ŏ/.\n",
        check_word="go")

    # ── Lesson 42: Rule 20 ──
    yield 42, build_rule(42, "20")

    # ── Lesson 48: Review Second Wave ──
    second_wave_pgs = ["ow","ou","oo","ed","igh","aw","au","ir","ur","oa","ear"]
    yield 48, build_review(48, "Review: ow ou oo ed igh aw au ir ur oa ear",
        sorted(list(SINGLE_PGS.keys())) + first_wave_pgs + second_wave_pgs,
        "| cow | c + ow | OW = /ow/ |\n| out | ou + t | OU = /ow/ |\n| book | b + oo + k | OO = /ö/ |\n| played | p + l + ay + ed | ED = /d/ |\n| light | l + igh + t | Rule 28 |\n| saw | s + aw | AW at end |\n| girl | g + ir + l | IR = /er/ |\n| hurt | h + ur + t | UR = /er/ |",
        "- /ow/ — ow or ou? *Both can!*\n- /er/ — er, ir, or ur? *All three!*\n- /ō/ — oa or ow? *oa in middle, ow often at end.*\n- /ä/ — aw or au? *aw at end, au in middle.*",
        ["cow","out","book","played","light","saw","cause","girl","hurt","boat","learn"])

    # ── Lessons 51-53: High-Frequency Words ──
    yield 51, build_hf_words(51, 1, HF_WORDS_SET1,
        "The cat is big. I see a dog. The sun is hot.",
        "The cat is big. A dog is here.",
        "the")

    yield 52, build_hf_words(52, 2, HF_WORDS_SET2,
        "Do you see the cat? He was in the bed. Has the dog run? She said yes!",
        "Do you see the dog? She said yes.",
        "you")

    yield 53, build_hf_words(53, 3, HF_WORDS_SET3,
        "We are at the park. I have a big hat. Come and give it to me. Some dogs run fast.",
        "We are at home. Come and have some fun.",
        "have")

    # ── Lesson 54: Rule 30 (Floss Rule) ──
    yield 54, build_rule(54, "30")

    # ── Lesson 55: Fred the Frog (Reader) ──
    yield 55, build_fred_reader()

    # ── Lesson 56: Stage 2 Mastery Check ──
    yield 56, build_final_assessment()


def build_mid_assessment():
    pgs = list(SINGLE_PGS.keys()) + ["sh","th","ck","ee","ng","ar","or","er"]
    pg_checks = "\n".join(
        f"| {p} | {SINGLE_PGS.get(p, MULTI_PGS.get(p, {}).get('sounds', '—'))} | ☐ |"
        for p in pgs if p in SINGLE_PGS or p in MULTI_PGS
    )
    return ASSESSMENT_TEMPLATE.format(
        lesson_num=24, title="Mid-Stage 2 Assessment",
        overview="This mid-point check verifies the child is on track. Focus on CVC accuracy, first multi-letter phonograms, and blending with blends.",
        pg_checklist=pg_checks, pg_total=34,
        reading_checklist="| cat | ☐ |\n| ship | ☐ |\n| back | ☐ |\n| see | ☐ |\n| stop | ☐ |\n| hand | ☐ |\n| sing | ☐ |\n| car | ☐ |\n| for | ☐ |\n| her | ☐ |",
        reading_total=10,
        spelling_checklist="| cat | ☐ |\n| ship | ☐ |\n| back | ☐ |\n| see | ☐ |\n| stop | ☐ |\n| that | ☐ |\n| sing | ☐ |\n| car | ☐ |",
        spelling_total=8,
        rule_checklist="| Rule 26 | When do we use CK instead of K? | ☐ |\n| Short vowels | Name the five short vowel sounds. | ☐ |",
        rule_total=2,
        overall_total=54,
        next_steps="If ≥85%: Continue to second half of Stage 2. If weaker, review trouble spots for 1-2 weeks and retest.",
    )

def build_final_assessment():
    pgs = list(SINGLE_PGS.keys()) + list(MULTI_PGS.keys())
    pg_checks = "\n".join(
        f"| {p} | {SINGLE_PGS.get(p, MULTI_PGS.get(p, {}).get('sounds', '—'))} | ☐ |"
        for p in pgs
    )
    return ASSESSMENT_TEMPLATE.format(
        lesson_num=56, title="Stage 2 Mastery Check",
        overview="This final assessment checks readiness for Stage 3. The child should demonstrate CVC/CCVC/CVCC proficiency, know 26 multi-letter phonograms, and apply Rules 3, 4, 6, 9, 11, 20, 26, 30.",
        pg_checklist=pg_checks, pg_total=len(pgs),
        reading_checklist="| ship | ☐ |\n| back | ☐ |\n| green | ☐ |\n| stop | ☐ |\n| hand | ☐ |\n| coin | ☐ |\n| boy | ☐ |\n| rain | ☐ |\n| day | ☐ |\n| light | ☐ |\n| boat | ☐ |\n| hurt | ☐ |",
        reading_total=12,
        spelling_checklist="| ship | ☐ |\n| back | ☐ |\n| see | ☐ |\n| stop | ☐ |\n| day | ☐ |\n| coin | ☐ |\n| light | ☐ |\n| boat | ☐ |\n| hurt | ☐ |\n| play | ☐ |",
        spelling_total=10,
        rule_checklist="| Rule 26 | When do we use CK? | ☐ |\n| Rule 3 | What four letters can't end words? | ☐ |\n| Rule 9 | When do we use AY? | ☐ |\n| Rule 4 | What happens to vowels at end of syllable? | ☐ |\n| Rule 20 | What are the three sounds of -ED? | ☐ |\n| Rule 30 | What is the Floss Rule? | ☐ |",
        rule_total=6,
        overall_total=len(pgs)+28,
        next_steps="If all sections pass: Move to Stage 3! If any section is weak, return to those specific lessons and re-test in 1-2 weeks. Passing score: 85%+",
    )

def build_fred_reader():
    story = """<div class="reader-page">

<div class="reader-text">

**Fred the Frog**

Fred is a frog. Fred sits on a log.

The log is in the pond. The sun is hot.

Fred jumps off the log. SPLASH!

Fred swims in the pond. The water is cool.

Fred sees a bug. The bug is on a rock.

Fred hops to the rock. The bug zips away!

Fred is sad. No bug for Fred.

Then Fred sees a big, fat fly. The fly is on the log.

Fred hops back to the log. He stops. He waits.

ZAP! Fred gets the fly!

Yum, yum! Fred is a happy frog.

The End.

</div>

<div class="reader-sidebar">

### Spelling Aid

**New phonograms in this story:** sh, th, ck, ee, ng

**Sounds:** sh = /sh/, th = /th/, ck = /k/, ee = /ē/, ng = /ng/

**Rule check:**
- CK in 'back': Rule 26 (after short vowel)
- OO in 'cool': /ü/ sound
- EE in 'sees', 'green': always /ē/

**Say-to-Spell tip:** Say /frŏg/ to hear the short O.

### Story Stats
- **Total words:** 112
- **Unique words:** 53
- **Decodable:** ~95%
- **HF words used:** the, a, is, of, no, he

</div>

</div>"""

    return READER_TEMPLATE.format(
        lesson_num=55, title="Reader: Fred the Frog",
        review_pgs="f, r, o, g, sh, th, ck, ee, ng, s, l, p, n, d, h, j, w, c, b, z, y",
        warmup_words="Fred &nbsp; frog &nbsp; log &nbsp; sits &nbsp; pond &nbsp; jumps &nbsp; splash &nbsp; swims &nbsp; cool &nbsp; sees &nbsp; bug &nbsp; rock &nbsp; hops &nbsp; zips &nbsp; fat &nbsp; fly &nbsp; back &nbsp; waits &nbsp; gets &nbsp; happy",
        story_title="Fred the Frog",
        story_text=story,
        talk_about="1. Where does Fred sit at the start?\n2. Why does Fred jump into the pond?\n3. What happens when Fred tries to catch the bug?\n4. How does Fred feel at the end? Why?\n5. Can you find a word with CK in it? (back) Which rule explains it?",
        story_words_table="| frog | f (/f/), r (/r/), o (/ŏ/), g (/g/) |\n| splash | s (/s/), p (/p/), l (/l/), a (/ă/), sh (/sh/) |\n| cool | c (/k/), oo (/ü/), l (/l/) |\n| back | b (/b/), a (/ă/), ck (/k/) |\n| happy | h (/h/), a (/ă/), p (/p/), p (/p/), y (/ē/) |",
        next_num=56, next_title="Stage 2 Mastery Check",
    )


# ── WRITE ───────────────────────────────────────────────────────────

def main():
    for num, content in generate_all():
        slugs = {
            1: "review-stage1", 2: "short-a", 3: "short-i", 4: "short-o", 5: "short-u", 6: "short-e",
            7: "vc-words", 8: "cvc-continuant", 9: "cvc-stop", 10: "cvc-all",
            11: "pg-sh", 12: "pg-th", 13: "pg-ck",
            14: "spell-sh-th-ck",
            15: "pg-ee",
            16: "ccvc-blends", 17: "cvcc-blends", 18: "ccvcc-blends",
            19: "pg-ng", 20: "pg-ar", 21: "pg-or", 22: "pg-er",
            23: "review-6",
            24: "assessment-2",
            25: "pg-oi", 26: "pg-oy", 27: "rule-3",
            28: "pg-ai", 29: "pg-ay", 30: "rule-9",
            31: "spell-oi-oy-ai-ay",
            32: "pg-ch", 33: "pg-wh", 34: "pg-ea",
            35: "spell-ch-wh-ea",
            36: "pg-ow", 37: "pg-ou", 38: "rule-4",
            39: "open-syllables",
            40: "pg-oo", 41: "pg-ed", 42: "rule-20",
            43: "pg-igh", 44: "pg-aw", 45: "pg-au",
            46: "pg-ir", 47: "pg-ur",
            48: "review-7",
            49: "pg-oa", 50: "pg-ear",
            51: "hf-words-1", 52: "hf-words-2", 53: "hf-words-3",
            54: "rule-30",
            55: "reader-1",
            56: "assessment-3",
        }
        slug = slugs.get(num, f"lesson-{num:03d}")
        filepath = OUT_DIR / f"{slug}.md"
        filepath.write_text(content, encoding="utf-8")
        print(f"  {filepath.relative_to(PROJECT_ROOT)}")

    print(f"\nDone! 56 lessons written to {OUT_DIR.relative_to(PROJECT_ROOT)}")

if __name__ == "__main__":
    main()
