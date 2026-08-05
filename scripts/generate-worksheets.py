#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate student worksheets: phonogram practice, rule practice, flash cards, game cards."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "worksheets"

# Import phonogram data from the canonical source (framework/phonograms.py).
# See framework/phonograms.py for the single source of truth.
import sys
sys.path.insert(0, str(ROOT / "framework"))
from phonograms import SINGLE, MULTI, MULTI3, MULTI4, PG_STAGE  # noqa: E402

# Create subdirectories
for d in ["phonograms", "rules", "cards", "handwriting", "blank"]:
    (OUT / d).mkdir(parents=True, exist_ok=True)
# Stage-grouped subdirectories are created lazily (only when content lands there)
# to avoid empty stage-N/ dirs polluting the release ZIP.

# Phonogram data (SINGLE, MULTI, MULTI3, MULTI4, PG_STAGE) imported from
# framework/phonograms.py at the top of this file.

# Rule → stage mapping (from lesson-catalog.csv)
RULE_STAGE = {
    "26":2,"3":2,"9":2,"20":2,"4":2,"28":2,"30":2,
    "12":3,"1":3,"2":3,"25":3,"27":3,"5":3,"6":3,"7":3,"8":3,"10":3,"31":3,
    "13":4,"14":4,"15":4,"16":4,"17":4,"18":4,"23":4,"24":4,"19":4,"21":4,"22":4,"29":4,
}

RULES_WORDS = {
    "1": {"name": "C softens to /s/ before E, I, Y", "words": ["cent","city","cycle","face","ice","dance","since","rice","mice","nice","pace","race","lace","place","space"]},
    "2": {"name": "G may soften to /j/ before E, I, Y", "words": ["gem","giant","gym","age","cage","page","huge","large","change","strange","danger","ginger","gentle","giraffe","engine"]},
    "3": {"name": "No English word ends in I, U, V, or J", "words": ["have","give","live","love","blue","true","clue","day","play","boy","toy","new","few","saw","law"]},
    "4": {"name": "A E O U say long at end of syllable", "words": ["go","no","so","he","me","she","we","be","baby","open","music","paper","even","unit","menu"]},
    "5": {"name": "I and Y at end of syllable say /ĭ/ or /ī/", "words": ["item","bicycle","by","my","gym","cry","sky","try","fly","dry","fry","shy","why","spy","reply"]},
    "6": {"name": "Y says /ī/ at end of one-syllable word", "words": ["by","my","cry","fly","sky","try","why","shy","dry","fry","pry","spy","sly","thy","ply"]},
    "7": {"name": "I and Y may say /ē/", "words": ["baby","happy","funny","candy","silly","marine","radio","police","very","many","only","family","city","party","study"]},
    "8": {"name": "I and O may say /ī/ /ō/ before two consonants", "words": ["find","kind","mind","child","wild","blind","old","cold","most","post","bolt","told","gold","hold","roll"]},
    "9": {"name": "AY spells /ā/ at end of base word", "words": ["day","say","way","may","pay","lay","ray","bay","hay","clay","play","stay","gray","tray","pray"]},
    "10": {"name": "A says /ä/ at end, after W, before L", "words": ["spa","water","watch","want","wash","ball","tall","fall","all","call","small","wall","walk","talk","halt"]},
    "11": {"name": "Q always needs U", "words": ["queen","quit","quick","quack","quilt","quiz","quest","quiet","quite","quote","quarter","question","squish","squash","squeeze"]},
    "12": {"name": "Silent E (9 reasons)", "words": ["make","have","give","live","love","nice","race","page","cage","size","prize","house","mouse","those","three"]},
    "13": {"name": "Drop silent E for vowel suffix", "words": ["making","hoping","driving","using","baking","writing","smiling","raking","riding","taking","shining","taping","waving","saving"]},
    "14": {"name": "Double consonant (1-1-1 rule)", "words": ["running","hopping","swimming","sitting","getting","cutting","stopping","planning","begging","jogging","shopping","clapping"]},
    "15": {"name": "Y changes to I before suffix", "words": ["babies","cries","tries","flies","carried","happiness","beautiful","funnier","laziest","earlier","dried","spied","hurried"]},
    "16": {"name": "Two I's cannot be adjacent", "words": ["crying","trying","flying","studying","carrying","marrying","hurrying","worrying","copying","varying"]},
    "17": {"name": "TI CI SI spell /sh/ in Latin words", "words": ["nation","action","station","special","social","musician","mission","session","vision","fraction","precious","delicious"]},
    "18": {"name": "SH at beginning/end of base word", "words": ["ship","fish","wish","dish","push","crash","flash","she","shut","shop","dashes","wishing","fishes","splashes","crashes"]},
    "19": {"name": "Past tense formed with -ED", "words": ["walked","played","stopped","baked","carried","tried","hopped","hoped","planned","called","needed","wanted"]},
    "20": {"name": "Three sounds of -ED", "words": ["wanted","needed","rested","played","called","showed","fished","jumped","looked","stopped","asked","liked","walked","talked","worked"]},
    "21": {"name": "Plural -S and -ES", "words": ["cats","dogs","boxes","dishes","churches","foxes","buses","houses","pages","races","bridges","catches","wishes","judges","dishes"]},
    "22": {"name": "3rd person singular -S and -ES", "words": ["runs","walks","fixes","washes","catches","watches","misses","goes","does","has","is","plays","stays","tries","carries"]},
    "23": {"name": "AL- prefix has one L", "words": ["already","although","always","also","almost","altogether","alright","albeit","almighty"]},
    "24": {"name": "-FUL suffix has one L", "words": ["hopeful","careful","useful","joyful","playful","helpful","thankful","wonderful","powerful","beautiful","graceful","peaceful"]},
    "25": {"name": "DGE after short vowel", "words": ["bridge","edge","fudge","judge","badge","lodge","ledge","dodge","ridge","wedge","pledge","sledge","trudge"]},
    "26": {"name": "CK after short vowel", "words": ["back","sick","duck","neck","lock","rock","sock","pack","pick","kick","tick","tuck","check","click","stick"]},
    "27": {"name": "TCH after short vowel", "words": ["catch","match","patch","latch","batch","hatch","notch","ditch","hitch","pitch","witch","fetch","stretch","scratch"]},
    "28": {"name": "GH phonograms", "words": ["light","night","right","eight","weigh","though","through","rough","tough","laugh","caught","taught","ghost","high","sigh"]},
    "29": {"name": "Z not S at beginning for /z/", "words": ["zip","zap","zoo","zone","zero","zebra","zigzag","zoom","zesty","zipper","zinc","zany","zillion"]},
    "30": {"name": "Double F L S (Floss Rule)", "words": ["off","cliff","stuff","bell","fill","tall","full","miss","grass","class","kiss","dress","glass","buzz","fizz"]},
    "31": {"name": "Schwa in unstressed syllables", "words": ["about","seven","pencil","button","circus","animal","family","banana","chocolate","different","memory","happen"]},
}

# ── TEMPLATES ───────────────────────────────────────────────────────

PG_WORKSHEET = """# Phonogram Practice: {pg}

**Sounds:** {sounds}

---

<div class="phonogram-card">

<div class="phonogram-letter">{pg}</div>

<div class="phonogram-sounds">{sounds}</div>

</div>

## Part 1: Write the Phonogram

Write **{pg}** five times. Say its sounds as you write.

| | | | | |
|--|--|--|--|--|
| | | | | |

---

## Part 2: Circle the Phonogram

Circle every **{pg}** in these words:

> {circle_words}

---

## Part 3: Fill in the Missing Phonogram

Write **{pg}** to complete each word:

{fill_blanks}

---

## Part 4: Spelling Practice

An adult will dictate these words. Write each one:

1. _______________ &nbsp;&nbsp; 2. _______________ &nbsp;&nbsp; 3. _______________

4. _______________ &nbsp;&nbsp; 5. _______________ &nbsp;&nbsp; 6. _______________

---

## Part 5: Write a Sentence

Write a sentence using a word with **{pg}**:

> _______________________________________________

---

**Name:** _______________ &nbsp;&nbsp; **Date:** _______________
"""

RULE_WORKSHEET = """# Rule {num} Practice: {name}

---

## The Rule

> {statement}

---

## Part 1: Find the Rule

Circle the words that follow Rule {num}:

> {circle_words}

---

## Part 2: Apply the Rule

Write the correct form:

{apply_section}

---

## Part 3: Spelling Practice

An adult will dictate these words. Write each one:

1. _______________ &nbsp;&nbsp; 2. _______________ &nbsp;&nbsp; 3. _______________

4. _______________ &nbsp;&nbsp; 5. _______________ &nbsp;&nbsp; 6. _______________

---

## Part 4: Write Two Sentences

Write two sentences using words that follow Rule {num}:

1. _______________________________________________

2. _______________________________________________

---

**Name:** _______________ &nbsp;&nbsp; **Date:** _______________
"""

FLASH_CARD_SHEET = """# Phonogram Flash Cards — {title}

Cut along the dotted lines. Practice daily!

---

{cards}

---

**Instructions:** Flash one card at a time. Child says ALL sounds within 2 seconds.
Sort into "fast" and "needs practice" piles.
"""

# ── GENERATORS ──────────────────────────────────────────────────────

def generate_pg_worksheets():
    """One worksheet per phonogram (75 total: 27 single + 26 multi + 17 stage3 + 3 Latin /sh/)."""
    count = 0
    for pg, data in {**SINGLE, **MULTI, **MULTI3, **MULTI4}.items():
        words = data["words"][:12]
        circle = " &nbsp;&nbsp; ".join(words[:8])
        # Fill blanks: remove PG from each word
        blanks = []
        for w in words[:6]:
            if pg in w:
                blanked = w.replace(pg, "____")
                blanks.append(f"- {blanked} &nbsp; → &nbsp; _______________")
        fill = "\n".join(blanks[:5])
        
        content = PG_WORKSHEET.format(pg=pg, sounds=data["sounds"], circle_words=circle, fill_blanks=fill)
        (OUT / "phonograms" / f"pg-{pg}.md").write_text(content, encoding="utf-8")
        stage = PG_STAGE.get(pg, 2)
        stage_dir = OUT / "phonograms" / f"stage-{stage}"
        stage_dir.mkdir(parents=True, exist_ok=True)
        (stage_dir / f"pg-{pg}.md").write_text(content, encoding="utf-8")
        count += 1
    return count

def generate_rule_worksheets():
    """One worksheet per major rule."""
    count = 0
    for rnum, data in RULES_WORDS.items():
        words = data["words"]
        circle = " &nbsp;&nbsp; ".join(words[:10])
        
        # Apply section varies by rule
        if rnum == "13":
            apply_sec = "Add -ing:\n\nmake → ___________ &nbsp; hope → ___________ &nbsp; drive → ___________\n\nuse → ___________ &nbsp; bake → ___________ &nbsp; write → ___________"
        elif rnum == "12":
            apply_sec = "Name the Silent E reason (12.1-12.9):\n\nmake (long a) → ___________ &nbsp; have (no V/U) → ___________\n\nrace (C→/s/) → ___________ &nbsp; cage (G→/j/) → ___________\n\nsize (no plural) → ___________ &nbsp; prize (look bigger) → ___________\n\nhouse (TH voiced /z/) → ___________ &nbsp; these (clarify) → ___________\n\ncome (unseen) → ___________"
        elif rnum == "14":
            apply_sec = "Add -ing:\n\nrun → ___________ &nbsp; hop → ___________ &nbsp; swim → ___________\n\nsit → ___________ &nbsp; get → ___________ &nbsp; cut → ___________"
        elif rnum == "15":
            apply_sec = "Make plural or add suffix:\n\nbaby + es → ___________ &nbsp; cry + ed → ___________\n\nhappy + ness → ___________ &nbsp; carry + ed → ___________"
        elif rnum == "6":
            apply_sec = "Write the one-syllable word that matches:\n\n/bī/ → ___________ &nbsp; /mī/ → ___________ &nbsp; /krī/ → ___________\n\n/flī/ → ___________ &nbsp; /skī/ → ___________ &nbsp; /drī/ → ___________"
        elif rnum == "21" or rnum == "22":
            apply_sec = "Make plural (or 3rd person):\n\ncat → ___________ &nbsp; box → ___________ &nbsp; dish → ___________\n\nchurch → ___________ &nbsp; bus → ___________ &nbsp; fox → ___________"
        elif rnum == "20":
            apply_sec = "Sort by -ED sound:\n\n/ed/ (wanted): ___________ ___________\n/d/ (played): ___________ ___________\n/t/ (fished): ___________ ___________"
        elif rnum == "25":
            apply_sec = "DGE or GE?\n\nbr i dge (short i → DGE) &nbsp; ca ge (long a → GE)\n\nfu ___ (short u) &nbsp; la ___ (long a) &nbsp; e ___ (short e)"
        elif rnum == "26":
            apply_sec = "CK or K?\n\nba ___ (short a → CK) &nbsp; du ___ (short u → CK)\n\nsee ___ (long e → K) &nbsp; boo ___ (OO → K)"
        elif rnum == "27":
            apply_sec = "TCH or CH?\n\nca ___ (short a → TCH) &nbsp; wa ___ (broad a → TCH)\n\nin ___ (consonant n → CH) &nbsp; lun ___ (consonant n → CH)"
        elif rnum == "30":
            apply_sec = "Double or single?\n\nof_ → ___________ &nbsp; bel_ → ___________ &nbsp; mis_ → ___________\n\ntal_ → ___________ &nbsp; ful_ → ___________ &nbsp; gras_ → ___________"
        else:
            apply_sec = "Write each word and underline where the rule applies:\n\n" + " &nbsp;&nbsp; ".join(words[:5]) + "\n\n_______________ &nbsp; _______________ &nbsp; _______________ &nbsp; _______________ &nbsp; _______________"
        
        content = RULE_WORKSHEET.format(
            num=rnum, name=data["name"], statement=data["name"],
            circle_words=circle, apply_section=apply_sec)
        (OUT / "rules" / f"rule-{rnum}.md").write_text(content, encoding="utf-8")
        stage = RULE_STAGE.get(rnum, 3)
        stage_dir = OUT / "rules" / f"stage-{stage}"
        stage_dir.mkdir(parents=True, exist_ok=True)
        (stage_dir / f"rule-{rnum}.md").write_text(content, encoding="utf-8")
        count += 1
    return count

def generate_flash_cards():
    """Printable phonogram flash card sheets. Each batch also writes a stage mirror."""
    count = 0
    # Single-letter cards (4 per page, 7 pages) — Stage 1
    singles = list(SINGLE.keys())
    for page in range(0, len(singles), 4):
        batch = singles[page:page+4]
        cards = ""
        for pg in batch:
            sounds = SINGLE[pg]["sounds"]
            cards += f"""<div class="phonogram-card" style="display:inline-block; width:45%; margin:2%; border:2px solid #2a5c8a; border-radius:8px; padding:20px; text-align:center; page-break-inside:avoid;">
<div class="phonogram-letter" style="font-size:60pt; font-weight:bold; color:#2a5c8a; font-family:Georgia,serif;">{pg}</div>
<div class="phonogram-sounds" style="font-size:12pt; color:#555;">{sounds}</div>
</div>\n"""

        content = FLASH_CARD_SHEET.format(
            title=f"Single-Letter Phonograms (Page {(page//4)+1} of 7)",
            cards=cards)
        (OUT / "cards" / f"flash-singles-{(page//4)+1}.md").write_text(content, encoding="utf-8")
        singles_stage_dir = OUT / "cards" / "stage-1"
        singles_stage_dir.mkdir(parents=True, exist_ok=True)
        (singles_stage_dir / f"flash-singles-{(page//4)+1}.md").write_text(content, encoding="utf-8")
        count += 1

    # Multi-letter cards (4 per page) — Stage 2 (MULTI PGs)
    multis_s2 = list(MULTI.keys())
    for page in range(0, len(multis_s2), 4):
        batch = multis_s2[page:page+4]
        cards = ""
        for pg in batch:
            data = MULTI.get(pg, {"sounds": "—"})
            sounds = data["sounds"]
            cards += f"""<div class="phonogram-card" style="display:inline-block; width:45%; margin:2%; border:2px solid #2a5c8a; border-radius:8px; padding:20px; text-align:center; page-break-inside:avoid;">
<div class="phonogram-letter" style="font-size:48pt; font-weight:bold; color:#2a5c8a; font-family:Georgia,serif;">{pg}</div>
<div class="phonogram-sounds" style="font-size:10pt; color:#555;">{sounds}</div>
</div>\n"""

        content = FLASH_CARD_SHEET.format(
            title=f"Multi-Letter Phonograms (Stage 2 — Page {(page//4)+1} of {(len(multis_s2)//4)+1})",
            cards=cards)
        (OUT / "cards" / f"flash-multi-{(page//4)+1}.md").write_text(content, encoding="utf-8")
        s2 = OUT / "cards" / "stage-2"
        s2.mkdir(parents=True, exist_ok=True)
        (s2 / f"flash-multi-{(page//4)+1}.md").write_text(content, encoding="utf-8")
        count += 1

    # Multi-letter cards — Stage 3+ (advanced PGs + Latin /sh/ from Stage 4)
    multis_s3plus = list(MULTI3.keys()) + list(MULTI4.keys())
    for page in range(0, len(multis_s3plus), 4):
        batch = multis_s3plus[page:page+4]
        cards = ""
        for pg in batch:
            data = {**MULTI3, **MULTI4}.get(pg, {"sounds": "—"})
            sounds = data["sounds"]
            cards += f"""<div class="phonogram-card" style="display:inline-block; width:45%; margin:2%; border:2px solid #2a5c8a; border-radius:8px; padding:20px; text-align:center; page-break-inside:avoid;">
<div class="phonogram-letter" style="font-size:48pt; font-weight:bold; color:#2a5c8a; font-family:Georgia,serif;">{pg}</div>
<div class="phonogram-sounds" style="font-size:10pt; color:#555;">{sounds}</div>
</div>\n"""

        content = FLASH_CARD_SHEET.format(
            title=f"Advanced Phonograms (Stage 3+ — Page {(page//4)+1} of {(len(multis_s3plus)//4)+1})",
            cards=cards)
        # Continue flat numbering so existing pack references don't break
        flat_idx = (page // 4) + 1 + (len(multis_s2) // 4)
        (OUT / "cards" / f"flash-multi-{flat_idx}.md").write_text(content, encoding="utf-8")
        # Stage 3 mirror for most, Stage 4 for ti/ci/si — use PG_STAGE from
        # framework/phonograms.py as the source of truth (issue #14).
        if any(PG_STAGE.get(pg) == 4 for pg in batch):
            stage = 4
        else:
            stage = 3
        s_adv = OUT / "cards" / f"stage-{stage}"
        s_adv.mkdir(parents=True, exist_ok=True)
        (s_adv / f"flash-multi-{flat_idx}.md").write_text(content, encoding="utf-8")
        count += 1

    return count

def generate_blank_templates():
    """Reusable blank worksheet templates."""
    # Blank spelling analysis
    blank_sa = """# Spelling Analysis Worksheet

**Word List:** _______________

---

## 5-Step Spelling Analysis

For each word, follow: Hear & Say → Segment → Write → Analyze → Read

| Word | Write the Word | Underline Multi-Letter PGs | Rules Used | Say-to-Spell |
|------|---------------|---------------------------|------------|-------------|
| 1. | | | | |
| 2. | | | | |
| 3. | | | | |
| 4. | | | | |
| 5. | | | | |
| 6. | | | | |
| 7. | | | | |
| 8. | | | | |

---

**Name:** _______________ &nbsp;&nbsp; **Date:** _______________
"""
    (OUT / "blank" / "spelling-analysis.md").write_text(blank_sa, encoding="utf-8")
    
    # Blank handwriting
    blank_hw = """# Handwriting Practice

**Letters:** _______________

---

Write each letter 5 times. Say its sounds as you write.

| Letter | | | | | |
|--------|--|--|--|--|--|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

---

Write these words:

_______________ &nbsp;&nbsp; _______________ &nbsp;&nbsp; _______________

_______________ &nbsp;&nbsp; _______________ &nbsp;&nbsp; _______________

---

**Name:** _______________ &nbsp;&nbsp; **Date:** _______________
"""
    (OUT / "blank" / "handwriting.md").write_text(blank_hw, encoding="utf-8")
    
    # Blank reading log
    blank_rl = """# Reading Log

**Week of:** _______________

---

| Day | Title | Minutes | Words I Needed Help With |
|-----|-------|---------|--------------------------|
| Mon | | | |
| Tue | | | |
| Wed | | | |
| Thu | | | |
| Fri | | | |
| Sat | | | |
| Sun | | | |

---

**My favorite book this week:** _______________

**New words I learned:** _______________

---

**Name:** _______________
"""
    (OUT / "blank" / "reading-log.md").write_text(blank_rl, encoding="utf-8")
    return 3

# ── MAIN ────────────────────────────────────────────────────────────

def main():
    pg_count = generate_pg_worksheets()
    print(f"  {pg_count} phonogram worksheets → worksheets/phonograms/")
    
    rule_count = generate_rule_worksheets()
    print(f"  {rule_count} rule worksheets → worksheets/rules/")
    
    card_count = generate_flash_cards()
    print(f"  {card_count} phonogram flash cards → worksheets/cards/ ({(len(SINGLE)//4)+1} single + {(len(MULTI)+len(MULTI3))//4+1} multi sheets)")
    
    blank_count = generate_blank_templates()
    print(f"  {blank_count} blank templates → worksheets/blank/")
    
    total = pg_count + rule_count + card_count + blank_count
    print(f"\nTotal: {total} printable files generated")

if __name__ == "__main__":
    main()
