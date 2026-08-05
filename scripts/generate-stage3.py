#!/usr/bin/env python3
"""Generate all 56 Stage 3 lesson markdown files."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "lessons" / "stage-3"
OUT.mkdir(parents=True, exist_ok=True)

# ── SILENT E REASONS ────────────────────────────────────────────────

SILENT_E = {
    "12.1": {
        "num": "12.1", "name": "Vowel Says Its Long Sound",
        "statement": "The Silent Final E makes the vowel say its long sound.",
        "why": "This is the most common reason for silent E. In 'cap,' the A says /ă/. Add silent E → 'cape' — now A says /ā/. The E at the end reaches back over the consonant and tells the vowel: 'Say your name!'",
        "examples": "cap→cape, mat→mate, pin→pine, hop→hope, cub→cube, pet→Pete, sit→site, not→note, cut→cute, tap→tape",
        "words": ["make","time","rope","cube","these","tape","hope","pine","cape","cute"],
    },
    "12.2": {
        "num": "12.2", "name": "No V or U at the End",
        "statement": "English words do not end in V or U. Silent E is added to prevent this.",
        "why": "Rule 3 says no word ends in V or U. So we add a silent E: 'hav' becomes 'have,' 'tru' becomes 'true.' The E isn't changing the vowel sound here — it's just following the rule.",
        "examples": "have, give, live, love, solve, twelve, blue, true, clue, due, glue, argue, rescue, value",
        "words": ["have","give","live","blue","true","love","clue","twelve"],
    },
    "12.3": {
        "num": "12.3", "name": "C Says /s/ and G Says /j/",
        "statement": "Silent E lets C say /s/ and G say /j/.",
        "why": "C says /s/ before E, and G may say /j/ before E. But what if the E needs to be silent? We add a silent E after the C or G, and another letter between them. In 'dance,' the C sees E (across the N) and says /s/. In 'change,' the G sees E and says /j/.",
        "examples": "dance, prince, since, chance, fence, change, large, charge, huge, stage, page, cage",
        "words": ["dance","prince","change","large","since","fence","stage","page"],
    },
    "12.4": {
        "num": "12.4", "name": "Every Syllable Needs a Vowel",
        "statement": "Every syllable must have a vowel. Silent E provides the vowel for the final syllable.",
        "why": "In words like 'little,' 'table,' and 'puzzle,' the final syllable (tle, ble, zle) needs a vowel. The E is that vowel! Without it, we'd have 'littl' — and every syllable needs a vowel.",
        "examples": "little, table, candle, puzzle, apple, bubble, rifle, title, simple, purple, single, handle",
        "words": ["little","table","candle","puzzle","apple","bubble","rifle","purple"],
    },
    "12.5": {
        "num": "12.5", "name": "Keep S from Looking Plural",
        "statement": "Silent E is added to words ending in S to show they are not plural.",
        "why": "In 'house' and 'goose,' the silent E tells us 'this is NOT a plural — there is only one house, one goose.' Without the E, 'hous' and 'goos' would look like plurals of *hou* and *goo*.",
        "examples": "house, goose, moose, mouse, please, tease, cheese, noise",
        "words": ["house","goose","mouse","please","cheese","noise","moose","tease"],
    },
    "12.6": {
        "num": "12.6", "name": "Make the Word Look Bigger",
        "statement": "Silent E is added to very short content words to make them look 'complete.'",
        "why": "Very short words look odd in English. 'Pi,' 'ri,' 'aw' — these look incomplete. Adding a silent E makes them look like real English words: pie, rye, awe, owe, bye, dye.",
        "examples": "pie, rye, awe, owe, bye, dye, lye, ewe",
        "words": ["pie","rye","awe","owe","bye","dye"],
    },
    "12.7": {
        "num": "12.7", "name": "TH Voiced",
        "statement": "Silent E clarifies that TH is voiced (/th/ as in 'this'), not unvoiced (/th/ as in 'thin').",
        "why": "At the end of a word, TH is usually unvoiced (bath, path). When TH is voiced, we add silent E to mark it: bathe, clothe, breathe, teethe.",
        "examples": "bathe, clothe, breathe, teethe, soothe, loathe, seethe, writhe",
        "words": ["bathe","clothe","breathe","teethe","soothe"],
    },
    "12.8": {
        "num": "12.8", "name": "Clarify Meaning",
        "statement": "Silent E distinguishes between homophones — words that sound the same but mean different things.",
        "why": "Some words sound identical but need different spellings to show different meanings: by/bye, or/ore, aw/awe. The silent E marks the difference.",
        "examples": "by/bye, or/ore, aw/awe, ow/owe, pleas/please, laps/lapse",
        "words": ["bye","ore","awe","owe","please","lapse"],
    },
    "12.9": {
        "num": "12.9", "name": "Unseen Reason",
        "statement": "Some words have a silent E for historical reasons we no longer hear.",
        "why": "English has changed over time. Words like 'come,' 'some,' 'done,' 'none' once had sounds we no longer pronounce. The silent E remains as a fossil of the older pronunciation. We don't always know exactly why, but the E IS doing a job — even if we can no longer see or hear exactly what it is.",
        "examples": "come, some, done, none, gone, one, love, above, have (some overlap with 12.2)",
        "words": ["come","some","done","none","gone","one","love","above"],
    },
}

# ── STAGE 3 MULTI-LETTER PHONOGRAMS ─────────────────────────────────

MULTI3 = {
    "dge": {
        "sounds": "/j/",
        "sc": 1,
        "examples": [("j","bridge, edge, fudge, judge")],
        "tip": "DGE is a three-letter /j/ used ONLY after a short vowel. If the vowel is long or there's a consonant before, use GE instead (cage, large).",
        "rule": "Rule 25: DGE is used only after a single vowel which says its short sound.",
        "words": [("bridge","b (/b/), r (/r/), i (/ĭ/), dge (/j/)","Rule 25: DGE after short i","/brĭj/"),
                  ("edge","e (/ĕ/), dge (/j/)","Rule 25","/ĕj/"),
                  ("judge","j (/j/), u (/ŭ/), dge (/j/)","Rule 25","/jŭj/")],
    },
    "tch": {
        "sounds": "/ch/",
        "sc": 1,
        "examples": [("ch","catch, watch, match, pitch")],
        "tip": "TCH is a three-letter /ch/ used ONLY after a short vowel (or broad A in 'watch'). Compare: 'rich' (consonant before CH — no TCH) vs. 'catch' (short A — TCH).",
        "rule": "Rule 27: TCH is used only after a single vowel which says its short or broad sound.",
        "words": [("catch","c (/k/), a (/ă/), tch (/ch/)","Rule 27: TCH after short a","/kăch/"),
                  ("watch","w (/w/), a (/ä/), tch (/ch/)","Rule 27: TCH after broad a","/wäch/"),
                  ("pitch","p (/p/), i (/ĭ/), tch (/ch/)","Rule 27","/pĭch/")],
    },
    "kn": {
        "sounds": "/n/",
        "sc": 1,
        "examples": [("n","know, knee, knife, knock")],
        "tip": "KN is a two-letter /n/ used only at the BEGINNING of a word. The K is silent. This comes from Old English where the K was once pronounced.",
        "words": [("know","kn (/n/), ow (/ō/)","KN = two-letter /n/","/nō/"),
                  ("knee","kn (/n/), ee (/ē/)","KN at start","/nē/"),
                  ("knock","kn (/n/), o (/ŏ/), ck (/k/)","KN + CK in same word","/nŏk/")],
    },
    "gn": {
        "sounds": "/n/",
        "sc": 1,
        "examples": [("n","sign, gnat, gnaw, design")],
        "tip": "GN is a two-letter /n/. At the beginning of a word, the G is silent (gnat, gnaw). In the middle or end, GN says /n/ (sign, design).",
        "words": [("sign","s (/s/), i (/ī/), gn (/n/)","GN at end — G silent","/sīn/"),
                  ("gnat","gn (/n/), a (/ă/), t (/t/)","GN at start","/năt/"),
                  ("gnaw","gn (/n/), aw (/ä/)","GN at start","/nä/")],
    },
    "wr": {
        "sounds": "/r/",
        "sc": 1,
        "examples": [("r","write, wrong, wrist, wrap")],
        "tip": "WR is a two-letter /r/. The W is silent. Think of it as the 'writing R' — it appears in words about writing! (write, wrote, written, wrist, wrap, wreck)",
        "words": [("write","wr (/r/), i (/ī/), t (/t/), e — silent E (12.1)","WR + silent E","/rīt/"),
                  ("wrong","wr (/r/), o (/ŏ/), ng (/ng/)","WR at start","/rŏng/"),
                  ("wrap","wr (/r/), a (/ă/), p (/p/)","WR at start","/răp/")],
    },
    "eigh": {
        "sounds": "/ā/",
        "sc": 1,
        "examples": [("ā","eight, neighbor, weight, freight")],
        "tip": "EIGH is a four-letter /ā/. The GH is silent here (Rule 28). Think: 'E-I-G-H spells /ā/!' as in 'eight.'",
        "rule": "Rule 28: GH is often silent after I.",
        "words": [("eight","eigh (/ā/), t (/t/)","Rule 28: GH silent","/āt/"),
                  ("neighbor","n (/n/), eigh (/ā/), b (/b/), or (/or/)","Rule 28","nā-bor"),
                  ("weigh","w (/w/), eigh (/ā/)","Rule 28","/wā/")],
    },
    "ei": {
        "sounds": "/ē/ /ā/ /ī/",
        "sc": 3,
        "examples": [("ē","ceiling, receive, deceive"),("ā","vein, rein, feign"),("ī","feisty, heist, seismic")],
        "tip": "EI has three sounds: /ē/ (most common in Latin-based words), /ā/ (in a few words), /ī/ (rare — only a handful). It follows Rule 1/2 patterns with C and G.",
        "words": [("ceiling","c (/s/), ei (/ē/), l (/l/), i (/ĭ/), ng (/ng/)","Rule 1: C=/s/ before EI","sē-lĭng"),
                  ("vein","v (/v/), ei (/ā/), n (/n/)","EI=/ā/ (rare)","/vān/"),
                  ("feisty","f (/f/), ei (/ī/), s (/s/), t (/t/), y (/ē/)","EI=/ī/ (rare)","fī-stē")],
    },
    "ey": {
        "sounds": "/ā/ /ē/",
        "sc": 2,
        "examples": [("ā","they, hey, prey, obey"),("ē","key, valley, money, turkey")],
        "tip": "EY has two sounds: /ā/ (as in 'they') and /ē/ (as in 'key' or at the end of multi-syllable words like 'valley'). When unstressed at the end, it usually says /ē/.",
        "words": [("they","th (/th/), ey (/ā/)","EY=/ā/","/thā/"),
                  ("key","k (/k/), ey (/ē/)","EY=/ē/","/kē/"),
                  ("valley","v (/v/), a (/ă/), l (/l/), l (/l/), ey (/ē/)","Y unstressed = /ē/","văl-ē")],
    },
    "ph": {
        "sounds": "/f/",
        "sc": 1,
        "examples": [("f","phone, graph, dolphin, elephant")],
        "tip": "PH is a two-letter /f/ that comes from Greek. Most English words with PH are Greek in origin. It's like an ancient 'F'!",
        "words": [("phone","ph (/f/), o (/ō/), n (/n/), e — silent E (12.1)","PH = /f/ (Greek)","/fōn/"),
                  ("graph","g (/g/), r (/r/), a (/ă/), ph (/f/)","PH at end","/grăf/"),
                  ("dolphin","d (/d/), o (/ŏ/), l (/l/), ph (/f/), i (/ĭ/), n (/n/)","PH in middle","dŏl-fĭn")],
    },
    "gh": {
        "sounds": "/g/",
        "sc": 1,
        "examples": [("g","ghost, ghastly, ghetto")],
        "tip": "GH at the BEGINNING of a word says /g/. This is different from GH at the end (which is often silent — Rule 28). Only a few words use GH at the start, and they all have a spooky feel! (ghost, ghastly, ghoul)",
        "words": [("ghost","gh (/g/), o (/ō/), s (/s/), t (/t/)","GH=/g/ at start","/gōst/"),
                  ("ghastly","gh (/g/), a (/ă/), s (/s/), t (/t/), l (/l/), y (/ē/)","GH=/g/ at start","găst-lē"),
                  ("ghoul","gh (/g/), ou (/ü/), l (/l/)","GH=/g/ at start","/gül/")],
    },
    "ough": {
        "sounds": "/ō/ /ö/ /ow/ /ŭf/ /äf/ /ü/",
        "sc": 6,
        "examples": [("ō","though, although"),("ö","through"),("ow","cough, trough"),("ŭf","rough, tough, enough"),("äf","bought, fought, thought"),("ü","through")],
        "tip": "OUGH is the wildest phonogram — it has SIX sounds! /ō/ (though), /ö/ (through), /ow/ (cough), /ŭf/ (rough), /äf/ (bought), /ü/ (through). GH is doing different things in each one (Rule 28). You'll learn these through practice.",
        "rule": "Rule 28: GH can be silent, say /f/, or affect the vowel.",
        "words": [("though","th (/th/), ough (/ō/)","Rule 28: GH silent","/thō/"),
                  ("through","th (/th/), r (/r/), ough (/ü/)","Rule 28","/thrü/"),
                  ("rough","r (/r/), ough (/ŭf/)","GH=/f/","/rŭf/")],
    },
    "augh": {
        "sounds": "/ä/ /ăf/",
        "sc": 2,
        "examples": [("ä","caught, taught, daughter"),("ăf","laugh, draught")],
        "tip": "AUGH has two sounds: /ä/ (most common, as in 'caught') and /ăf/ (only in 'laugh' and a few others). The GH affects the sound (Rule 28).",
        "rule": "Rule 28: GH after AU usually says /f/ or is silent.",
        "words": [("caught","c (/k/), augh (/ä/), t (/t/)","Rule 28","/kät/"),
                  ("taught","t (/t/), augh (/ä/), t (/t/)","Rule 28","/tät/"),
                  ("laugh","l (/l/), augh (/ăf/)","GH=/f/","/lăf/")],
    },
    "ew": {
        "sounds": "/ü/ /ö/",
        "sc": 2,
        "examples": [("ü","few, new, grew, chew"),("ö","sew")],
        "tip": "EW says /ü/ (as in 'few') most of the time. Only 'sew' uses the /ö/ sound. EW is always at the end of a word or syllable.",
        "words": [("few","f (/f/), ew (/ü/)","EW at end","/fü/"),
                  ("new","n (/n/), ew (/ü/)","EW at end","/nü/"),
                  ("grew","g (/g/), r (/r/), ew (/ü/)","EW at end","/grü/")],
    },
    "ui": {
        "sounds": "/ü/ /ö/",
        "sc": 2,
        "examples": [("ü","fruit, suit, juice"),("ö","build, guild")],
        "tip": "UI says /ü/ (as in 'fruit') in most words. In 'build,' it says /ö/. UI always has another letter after it — it never ends a word.",
        "words": [("fruit","f (/f/), r (/r/), ui (/ü/), t (/t/)","UI=/ü/","/früt/"),
                  ("suit","s (/s/), ui (/ü/), t (/t/)","UI=/ü/","/süt/"),
                  ("build","b (/b/), ui (/ö/), l (/l/), d (/d/)","UI=/ö/ (unusual)","/bĭld/")],
    },
    "eu": {
        "sounds": "/ü/ /ö/",
        "sc": 2,
        "examples": [("ü","neutral, feud, eucalyptus"),("ö","—")],
        "tip": "EU says /ü/ in most words (neutral, feud). It appears in words of Greek and Latin origin. EU is never at the end of an English word.",
        "words": [("neutral","n (/n/), eu (/ü/), t (/t/), r (/r/), a (/ă/), l (/l/)","EU=/ü/","nü-trăl"),
                  ("feud","f (/f/), eu (/ü/), d (/d/)","EU=/ü/","/füd/"),
                  ("Europe","Eu (/ü/), r (/r/), o (/ō/), p (/p/), e — silent E (12.1)","EU at start","Yü-rōp")],
    },
    "wor": {
        "sounds": "/wer/",
        "sc": 1,
        "examples": [("wer","work, world, worm, worth")],
        "tip": "WOR is a special phonogram where the W changes the sound of OR. Instead of /or/, it says /wer/. Think: 'W+OR = /wer/' as in 'work' and 'world.'",
        "words": [("work","wor (/wer/), k (/k/)","WOR — W changes OR","/werk/"),
                  ("world","wor (/wer/), l (/l/), d (/d/)","WOR","/werld/"),
                  ("worm","wor (/wer/), m (/m/)","WOR","/werm/")],
    },
    "ie": {
        "sounds": "/ē/ /ī/",
        "sc": 2,
        "examples": [("ē","field, piece, chief, believe"),("ī","pie, tie, lie, die")],
        "tip": "IE has two sounds: /ē/ (most common, as in 'field') and /ī/ (at the end of words, as in 'pie'). At the end of a word, IE always says /ī/ with a silent E.",
        "words": [("field","f (/f/), ie (/ē/), l (/l/), d (/d/)","IE=/ē/ in middle","/fēld/"),
                  ("pie","p (/p/), ie (/ī/)","IE=/ī/ at end","/pī/"),
                  ("chief","ch (/ch/), ie (/ē/), f (/f/)","IE=/ē/","/chēf/")],
    },
}

# ── STAGE 3 RULES ───────────────────────────────────────────────────

RULES3 = {
    "1": {
        "num": 1, "name": "C Softens to /s/ Before E, I, or Y",
        "statement": "**C** always softens to /s/ when followed by **E**, **I**, or **Y**. Otherwise, **C** says /k/.",
        "explanation": "C has two sounds: /k/ (hard) and /s/ (soft). When E, I, or Y follows C, it ALWAYS softens to /s/. When A, O, U, or a consonant follows, C says /k/. This is completely reliable — no exceptions!",
        "examples": "cent, city, cycle, face, ice, dance (C=/s/) · cat, cot, cup, clip, crab (C=/k/)",
        "words": ["cent","city","cycle","face","ice","dance","since","cat","cot","cup"],
    },
    "2": {
        "num": 2, "name": "G May Soften to /j/ Before E, I, or Y",
        "statement": "**G** *may* soften to /j/ only when followed by **E**, **I**, or **Y**. Otherwise, **G** says /g/.",
        "explanation": "G MAY (not always) soften to /j/ before E, I, or Y. In 'gem,' G says /j/. But in 'get' and 'give,' G says /g/ even though E and I follow. You have to try both sounds!",
        "examples": "gem, giant, gym, change, large (G=/j/) · go, gap, gum, get, give, girl (G=/g/ — doesn't soften)",
        "words": ["gem","giant","gym","change","large","get","give","go","gap","gum"],
    },
    "5": {
        "num": 5, "name": "I and Y at End of Syllable",
        "statement": "**I** and **Y** may say /ĭ/ or /ī/ at the end of a syllable.",
        "explanation": "At the end of a syllable, I and Y can say either their short sound (/ĭ/) or long sound (/ī/). In 'i·tem,' the I at the end of the first syllable says /ī/. In 'in·di·vid·u·al,' the I endings say /ĭ/. Y works the same way.",
        "examples": "i/tem (I=/ī/), bi/cy/cle (Y=/ĭ/ first, then silent), by (Y=/ī/), gym (Y=/ĭ/)",
        "words": ["item","bicycle","by","my","gym","cry","sky","try"],
    },
    "6": {
        "num": 6, "name": "Y Says /ī/ at End of One-Syllable Word",
        "statement": "When a one-syllable word ends in a single-vowel **Y**, it always says /ī/.",
        "explanation": "This is one of the most reliable rules! If a word has one syllable and ends in Y (as the only vowel), Y says /ī/. by, my, cry, fly, sky, try, why, shy, dry, fry.",
        "examples": "by, my, cry, fly, sky, try, why, shy, dry, fry, pry, spy",
        "words": ["by","my","cry","fly","sky","try","why","shy","dry"],
    },
    "7": {
        "num": 7, "name": "I and Y May Say /ē/",
        "statement": "**Y** says /ē/ only in an unstressed syllable at the end of a multi-syllable word. **I** may say /ē/ with a silent E, at end of syllable, and in foreign words.",
        "explanation": "Y at the end of a long word usually says /ē/: baby, happy, funny, candy. I says /ē/ in words like marine (silent E), radio (end of syllable), and spaghetti (Italian origin).",
        "examples": "baby, happy, funny, candy, silly (Y=/ē/) · marine, police (I=/ē/ with silent E) · radio, audio (I=/ē/) · spaghetti (I=/ē/ foreign)",
        "words": ["baby","happy","funny","candy","marine","radio","police","spaghetti"],
    },
    "8": {
        "num": 8, "name": "I and O Before Two Consonants",
        "statement": "**I** and **O** may say /ī/ and /ō/ when followed by two consonants.",
        "explanation": "In words like 'find,' 'kind,' 'mind' — the I says /ī/ even though it's followed by two consonants (which would normally make a short vowel). Same with O: 'old,' 'most,' 'post.'",
        "examples": "find, kind, mind, child, wild, blind (I=/ī/) · old, cold, most, post, bolt, roll (O=/ō/)",
        "words": ["find","kind","mind","child","wild","old","cold","most","post"],
    },
    "10": {
        "num": 10, "name": "A Says /ä/",
        "statement": "When a word ends with the phonogram **A**, it says /ä/. **A** may also say /ä/ after a **W** or before an **L**.",
        "explanation": "At the end of a word, A says /ä/ (spa, ma, pa). After W, A says /ä/ (water, watch, want). Before L, A often says /ä/ (ball, tall, fall, all, call).",
        "examples": "spa, ma, pa (end) · water, watch, want, wash (after W) · ball, tall, fall, all, call, small (before L)",
        "words": ["spa","water","watch","want","ball","tall","fall","all","call"],
    },
    "25": {
        "num": 25, "name": "DGE After Short Vowel",
        "statement": "**DGE** is used only after a single vowel which says its short sound.",
        "explanation": "DGE says /j/. It is used after a short vowel: bridge, edge, fudge, judge. If the vowel is long or a consonant precedes, use GE: cage, large, range.",
        "examples": "bridge, edge, fudge, judge, badge, ledge (DGE after short) · cage, page, large, charge (GE after long or consonant)",
        "words": ["bridge","edge","fudge","judge","badge","cage","page","large"],
    },
    "27": {
        "num": 27, "name": "TCH After Short Vowel",
        "statement": "**TCH** is used only after a single vowel which says its short or broad sound.",
        "explanation": "TCH says /ch/. It follows a short vowel (catch, pitch) or broad A (watch). If a consonant precedes, use CH: inch, bench, lunch.",
        "examples": "catch, pitch, fetch, notch, Dutch (TCH after short) · watch (TCH after broad A) · inch, lunch, bench (CH after consonant)",
        "words": ["catch","pitch","fetch","notch","watch","inch","lunch","bench"],
    },
    "28": {
        "num": 28, "name": "GH Phonograms",
        "statement": "**GH** is often silent after **I** and before **T**. It can also say /f/ or be part of a phonogram.",
        "explanation": "GH is a chameleon! In IGH, it's silent. In EIGH, it's silent. In OUGH, it can be silent (though), say /f/ (rough), or affect the vowel. In AUGH, it says /f/ or is silent. At the beginning of a word, GH says /g/ (ghost).",
        "examples": "light, high (IGH — GH silent) · eight, neighbor (EIGH — GH silent) · though (GH silent), through (GH silent), rough (GH=/f/), cough (GH=/f/) · laugh (GH=/f/) · ghost (GH=/g/ at start)",
        "words": ["light","eight","though","through","rough","cough","laugh","ghost"],
    },
    "31": {
        "num": 31, "name": "Schwa",
        "statement": "Any vowel may say the schwa sound /ə/ in an unstressed syllable.",
        "explanation": "Schwa is the most common vowel sound in English — the lazy /ə/ (like a tiny 'uh'). It happens in unstressed syllables and can be spelled by ANY vowel. This is why say-to-spell is so important!",
        "examples": "about (a=/ə/), seven (e=/ə/), pencil (i=/ə/), button (o=/ə/), circus (u=/ə/)",
        "words": ["about","seven","pencil","button","circus","animal","banana","family"],
    },
}

# ── SYLLABLE DIVISION DATA ──────────────────────────────────────────

SYLLABLE_LESSONS = {
    "compound": {
        "title": "Compound Words",
        "description": "Compound words are the easiest to divide — just split between the two smaller words! sun+set, rain+bow, in+to.",
        "words": ["sunset","rainbow","into","backpack","himself","bathtub","sailboat","popcorn","football","bedroom"],
        "check": "sunset",
    },
    "vccv": {
        "title": "VCCV Pattern",
        "description": "When two consonants stand between two vowels (VCCV), divide between the consonants. rab/bit, bas/ket, pic/nic. The first syllable is closed, so the vowel is short.",
        "words": ["rabbit","basket","picnic","muffin","puppet","tennis","lesson","pillow","butter","kitten"],
        "check": "rabbit",
    },
    "vcv": {
        "title": "VCV Pattern",
        "description": "When one consonant stands between two vowels (VCV), try dividing AFTER the first vowel (making an open syllable with a long vowel). If that doesn't sound right, divide BEFORE the consonant. ba/by (open) vs. cab/in (closed).",
        "words": ["baby","tiger","open","music","paper","seven","river","cabin","robin","lemon"],
        "check": "baby",
    },
    "cle": {
        "title": "Consonant + LE",
        "description": "When a word ends in a consonant + LE, the LE forms its own syllable. ta/ble, puz/zle, can/dle. The E is there because every syllable needs a vowel (Rule 12.4).",
        "words": ["table","puzzle","candle","apple","little","bubble","rifle","title","simple","purple","handle","single"],
        "check": "table",
    },
}

# ── HF WORDS ────────────────────────────────────────────────────────

HF4 = [
    ("where","WH says /hw/. ERE says /ār/ — E says /ā/ (open syllable), R-controlled. Say-to-spell: /hwār/."),
    ("there","TH says voiced /th/. ERE says /ār/ — same pattern as 'where.' Compare: where, there, here."),
    ("their","TH voiced. EIR — EI says /ā/ like in 'vein,' R-controlled. Say-to-spell: /thār/."),
    ("were","W says /w/. ERE says /er/ — a special case. Compare: were vs. where (same letters, different sounds!). Say-to-spell: /wār/ to remember the E, read as /wer/."),
    ("here","H says /h/. ERE says /ēr/ — E says /ē/ (open syllable). Say-to-spell: /hēr/."),
]

HF5 = [
    ("once","O says /wŭ/ — a rare case where O says /wŭ/. N says /n/. C says /s/ (Rule 1, before E). E is silent (Rule 12.9). Say-to-spell: /ōns/."),
    ("two","TW says /tw/. O says /ö/. The W is doing double duty. Say-to-spell: /twō/."),
    ("does","D says /d/. OE says /ŭ/ — unusual! S says /z/. Say-to-spell: /dōz/."),
    ("any","A says /ĕ/ — unusual! N says /n/. Y says /ē/ at end (Rule 7). Say-to-spell: /ānē/."),
    ("many","M says /m/. A says /ĕ/ (like 'any'). N says /n/. Y says /ē/. Say-to-spell: /mānē/."),
]

# ── TEMPLATES ───────────────────────────────────────────────────────

SILENT_E_TEMPLATE = """# Lesson {num}: Silent E Reason {rnum} — {name}

**Stage 3** · Lesson {num} · rule-intro

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

| Review all 75 phonograms |
|--------------------------|
| All a-z + sh, th, ck, ee, ng, ar, or, er, oi, oy, ai, ay, ch, wh, ea, ow, ou, oo, ed, igh, aw, au, ir, ur, oa, ear |

---

## New Learning: Silent E Reason {rnum}

### The Reason

> **{statement}**

### Why?

{why}

### Words That Follow This Rule

| Word | How Silent E Works Here |
|------|------------------------|
{word_analysis}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

---

## Reading Practice

Read these words sound by sound:

> {read_words}

Read these sentences:

> {sentences}

---

## Quick Check

1. What is Silent E Reason {rnum}? *(Explain in your own words.)*
2. Give an example word that follows this reason.
3. What would the word be WITHOUT the silent E?

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find 3 words in a book that follow Silent E Reason {rnum}.*
"""

MULTI3_TEMPLATE = """# Lesson {num}: Phonogram {pg}

**Stage 3** · Lesson {num} · phonogram-intro

---

## Warm-Up: Phonogram Flash Review

> Flash all known phonograms. Child says ALL sounds within 2 seconds.

| All known phonograms |
|----------------------|
| a-z + sh, th, ck, ee, ng, ar, or, er, oi, oy, ai, ay, ch, wh, ea, ow, ou, oo, ed, igh, aw, au, ir, ur, oa, ear{extra_known} |

---

## New Learning: The Phonogram **{pg}**

<div class="phonogram">{pg}</div>

**{pg}** says {sc} sound{s_plural}: {sounds}

{tip}

{rule_section}
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

> {read_words}

> {sentences}

---

## Quick Check

1. What does **{pg}** say? *({sounds})*
2. Is {pg} used at the beginning, middle, or end of words?
3. Write the word "{check_word}" from dictation.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Flash your **{pg}** card. Find **{pg}** in a book.*
"""

RULE3_TEMPLATE = """# Lesson {num}: Rule {rnum} — {name}

**Stage 3** · Lesson {num} · rule-intro

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

| All known phonograms |
|----------------------|
| a-z + sh, th, ck, ee, ng, ar, or, er, oi, oy, ai, ay, ch, wh, ea, ow, ou, oo, ed, igh, aw, au, ir, ur, oa, ear{extra_known} |

---

## New Learning: Rule {rnum}

### The Rule

> **{statement}**

### Why This Rule Matters

{explanation}

### Examples

{examples}

### Spot the Rule

| Word | How Rule {rnum} Applies |
|------|--------------------------|
{spot_rows}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

---

## Reading Practice

> {read_words}

> {sentences}

---

## Quick Check

1. What is Rule {rnum}? *(Restate in your own words.)*
2. Give an example where the rule applies.
3. Give an example where the rule does NOT apply (if there is one).

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find 3 words that follow Rule {rnum}. Write them down!*
"""

SYLLABLE_TEMPLATE = """# Lesson {num}: {title}

**Stage 3** · Lesson {num} · syllable-division

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

| All known phonograms |
|----------------------|
| a-z + all multi-letter learned so far |

---

## New Learning: {stitle}

### What Are Syllables?

A syllable is a word part with ONE vowel sound. Every syllable has exactly one vowel sound. When we read long words, we break them into syllables.

### How to Divide: {stitle}

{description}

### Let's Divide

For each word, say it slowly, clap the syllables, then write each syllable:

| Word | How Many Syllables? | Divided | First Syllable Vowel Sound | Second Syllable Vowel Sound |
|------|--------------------|---------|---------------------------|----------------------------|
{divide_rows}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

---

## Reading Practice

> {read_words}

> {sentences}

---

## Quick Check

1. How do you divide {pattern_words}? *(Describe the pattern.)*
2. How many vowel sounds are in a 2-syllable word? *(2 — one per syllable!)*
3. Divide the word "{check}" into syllables and spell each one.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find 3 two-syllable words in a book. Clap the syllables and try to divide them.*
"""

HF3_TEMPLATE = """# Lesson {num}: High-Frequency Words — Set {setn}

**Stage 3** · Lesson {num} · hf-word

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

| All known phonograms |
|----------------------|
| a-z + all multi-letter learned so far |

---

## Important Reminder

These are NOT sight words. Every one can be explained with phonograms and rules. Say-to-spell helps you hear the spelling!

---

## Today's Words

{word_sections}

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{spelling_rows}

---

## Reading Practice

> {sentences}

---

## Dictation

Adult reads these sentences. Child writes them.

> {dictation}

---

## Quick Check

1. Why is say-to-spell important for these words? *(Because the normal pronunciation hides the spelling!)*
2. Which word was hardest to explain? Why?
3. Spell "{check}" from dictation.

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Find today's words in a book. Write each one and underline the tricky phonograms.*
"""

REVIEW3_TEMPLATE = """# Lesson {num}: {title}

**Stage 3** · Lesson {num} · review

---

## Warm-Up: Speed Flash

> Flash ALL phonograms. Goal: under 2 seconds per card.

---

## {game1_title}

{game1}

---

## {game2_title}

{game2}

---

## {game3_title}

{game3}

---

## Spelling Challenge

Spell these words from dictation:

> {challenge_words}

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: {home_practice}*
"""

READER3_TEMPLATE = """# Lesson {num}: {title}

**Stage 3** · Lesson {num} · reader

---

## Story: {story_title}

{content}

---

## Quick Check

{talk}

---

**Next lesson:** Lesson {next_num}: {next_title}

---

*Practice at home: Read this story aloud!*
"""

ASSESSMENT3_TEMPLATE = """# Lesson {num}: {title}

**Stage 3** · Lesson {num} · assessment

---

## Overview

{overview}

---

## Part 1: Phonogram Sounds

| Phonogram | Sounds | ✓ |
|-----------|--------|---|
{pg_check}

**Score:** __ / {pg_total}

---

## Part 2: Silent E — Name That Reason

| Word | Which Reason? (12.x) | ✓ |
|------|---------------------|---|
{se_check}

**Score:** __ / {se_total}

---

## Part 3: Word Reading

| Word | ✓ |
|------|---|
{read_check}

**Score:** __ / {read_total}

---

## Part 4: Spelling (Dictation)

| Word | ✓ |
|------|---|
{spell_check}

**Score:** __ / {spell_total}

---

## Part 5: Rule Knowledge

| Rule | Question | ✓ |
|------|----------|---|
{rule_check}

**Score:** __ / {rule_total}

---

## Results

| Section | Score | Pass? |
|---------|-------|-------|
| Phonograms | __/{pg_total} | |
| Silent E | __/{se_total} | |
| Reading | __/{read_total} | |
| Spelling | __/{spell_total} | |
| Rules | __/{rule_total} | |

**Overall:** __/{{overall_total}}

## Next Steps

{next_steps}

---

*Great work! You're more than halfway through learning all 75 phonograms!*
"""

# ── HELPERS ─────────────────────────────────────────────────────────

def nt(n):
    titles_3 = {
        1:"Review Stage 2",2:"Long Vowel Sounds",3:"SE 1: Vowel Long",4:"SE 2: No V/U End",
        5:"SE 3: C→/s/ G→/j/",6:"SE 4: Syllable Needs Vowel",7:"SE Review 12.1-4",
        8:"SE 5: Not Plural",9:"SE 6: Look Bigger",10:"SE 7: TH Voiced",
        11:"SE 8: Clarify Meaning",12:"SE 9: Unseen Reason",13:"SE: Name That Reason",
        14:"Rule 1: C Softens",15:"Rule 2: G Softens",16:"Spelling: ce ci ge gi",
        17:"Phonogram dge",18:"Phonogram tch",19:"Review: dge tch",
        20:"Phonogram kn",21:"Phonogram gn",22:"Phonogram wr",23:"Review: kn gn wr",
        24:"Mid-Stage 3 Assessment",25:"Phonogram eigh",26:"Phonogram ei",
        27:"Phonogram ey",28:"Phonogram ph",29:"Phonogram gh",
        30:"Phonogram ough",31:"Phonogram augh",32:"Rule 28: GH",
        33:"Phonogram ew",34:"Phonogram ui",35:"Phonogram eu",
        36:"Rule 5: I/Y End Syllable",37:"Rule 6: Y=/ī/ One-Syllable",
        38:"Rule 7: I/Y May Say /ē/",39:"Rule 8: I/O Before Two Consonants",
        40:"Rule 10: A Says /ä/",41:"Phonogram wor",42:"Phonogram ie",
        43:"Syllables: Compound",44:"Syllables: VCCV",45:"Syllables: VCV",
        46:"Syllables: C+LE",47:"Schwa",48:"Reader: Gwen",49:"Reader: Cole",
        50:"Mixed Spelling",51:"Phonogram Review",52:"Rules Review",
        53:"HF Words 4",54:"HF Words 5",55:"Reader: Sail Box",56:"Stage 3 Mastery",
    }
    return titles_3.get(n, f"Lesson {n}")

# ── BUILDERS ────────────────────────────────────────────────────────

def build_silent_e(num, key):
    se = SILENT_E[key]
    words = se["words"]
    word_analysis = "\n".join(f"| {w} | (explain how SE reason {se['num']} applies) |" for w in words[:8])
    spelling_rows = "\n".join(f"| {w} | (sound out) | SE {se['num']} | /{w}/ |" for w in words[:5])
    return SILENT_E_TEMPLATE.format(
        num=num, rnum=se["num"], name=se["name"], statement=se["statement"],
        why=se["why"], word_analysis=word_analysis, spelling_rows=spelling_rows,
        read_words=" &nbsp;&nbsp; ".join(words),
        sentences=f"I will {words[0]} this. The {words[1]} is here. Can you {words[2]}?",
        next_num=num+1, next_title=nt(num+1),
    )

def build_multi3(num, pg):
    d = MULTI3[pg]
    sc = d["sc"]
    s_plural = "s" if sc > 1 else ""
    example_rows = "\n".join(f"| /{e[0]}/ | {e[1]} |" for e in d["examples"])
    tip = d["tip"]
    rule = d.get("rule")
    rule_section = f"\n> **Rule:** {rule}\n" if rule else ""
    wdata = d["words"]
    word_rows = "\n".join(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in wdata)
    read_words = " &nbsp;&nbsp; ".join(w[0] for w in wdata)
    sentences = f"The {wdata[0][0]} is here. I see a {wdata[1][0] if len(wdata)>1 else wdata[0][0]}."
    # Track what's been introduced so far
    intro_order = ["dge","tch","kn","gn","wr","eigh","ei","ey","ph","gh","ough","augh","ew","ui","eu","wor","ie"]
    idx = intro_order.index(pg) if pg in intro_order else -1
    extra = ""
    if idx > 0:
        prev = intro_order[:idx]
        extra = ", " + ", ".join(prev)
    return MULTI3_TEMPLATE.format(
        num=num, pg=pg, sc=sc, s_plural=s_plural, sounds=d["sounds"],
        tip=tip, rule_section=rule_section, example_rows=example_rows,
        word_rows=word_rows, read_words=read_words, sentences=sentences,
        check_word=wdata[0][0], extra_known=extra,
        next_num=num+1, next_title=nt(num+1),
    )

def build_rule3(num, key):
    r = RULES3[key]
    rn = r["num"]
    words = r["words"]
    spot_rows = "\n".join(f"| {w} | (describe how Rule {rn} applies) |" for w in words[:8])
    spelling_rows = "\n".join(f"| {w} | (sound out) | Rule {rn} | /{w}/ |" for w in words[:5])
    return RULE3_TEMPLATE.format(
        num=num, rnum=rn, name=r["name"], statement=r["statement"],
        explanation=r["explanation"], examples=r["examples"],
        spot_rows=spot_rows, spelling_rows=spelling_rows,
        read_words=" &nbsp;&nbsp; ".join(words),
        sentences=f"The {words[0]} is big. I see a {words[1]}. The {words[2] if len(words)>2 else words[0]} runs.",
        extra_known="",
        next_num=num+1, next_title=nt(num+1),
    )

def build_syllable(num, key):
    d = SYLLABLE_LESSONS[key]
    words = d["words"]
    divide_rows = "\n".join(
        f"| {w} | {len(w)//3+1} | {w[:len(w)//2]}/{w[len(w)//2:]} | — | — |"
        for w in words[:8]
    )
    spelling_rows = "\n".join(
        f"| {w} | (sound out each syllable) | — | {w} |" for w in words[:4]
    )
    pattern_words = d["title"]
    return SYLLABLE_TEMPLATE.format(
        num=num, title=f"Syllable Division: {d['title']}",
        stitle=d["title"], description=d["description"],
        divide_rows=divide_rows, spelling_rows=spelling_rows,
        read_words=" &nbsp;&nbsp; ".join(words),
        sentences=f"The {words[0]} is here. I see a {words[1] if len(words)>1 else words[0]}.",
        pattern_words=pattern_words,
        check=d["check"],
        next_num=num+1, next_title=nt(num+1),
    )

def build_hf3(num, setn, wdata, sentences, dictation, check):
    sections = ""
    for w, ex in wdata:
        sections += f"### {w}\n\n{ex}\n\n"
    spelling_rows = "\n".join(f"| {w} | (see above) | (see above) | (see above) |" for w,_ in wdata)
    return HF3_TEMPLATE.format(
        num=num, setn=setn, word_sections=sections,
        spelling_rows=spelling_rows, sentences=sentences,
        dictation=dictation, check=check,
        next_num=num+1, next_title=nt(num+1),
    )

def build_review3(num, title, g1_title, g1, g2_title, g2, g3_title, g3, challenge, home):
    return REVIEW3_TEMPLATE.format(
        num=num, title=title,
        game1_title=g1_title, game1=g1,
        game2_title=g2_title, game2=g2,
        game3_title=g3_title, game3=g3,
        challenge_words=", ".join(challenge),
        home_practice=home,
        next_num=num+1, next_title=nt(num+1),
    )


# ── MAIN ────────────────────────────────────────────────────────────

def generate():
    # 1: Review Stage 2
    yield 1, build_review3(1, "Review Stage 2 Phonograms and Rules",
        "Fast Flash",
        "Flash these multi-letter phonograms: sh, th, ck, ee, ng, ar, or, er, oi, oy, ai, ay, ch, wh, ea, ow, ou, oo, ed, igh, aw, au, ir, ur, oa, ear. Say ALL sounds for each.",
        "Rule Roundup",
        "Name these rules:\n- Rule 26 (CK after short vowel)\n- Rule 3 (No I, U, V, J at end)\n- Rule 9 (AY at end)\n- Rule 4 (Long at end of syllable)\n- Rule 20 (Three sounds of -ED)\n- Rule 30 (Floss Rule — double F, L, S)",
        "Word Build Challenge",
        "Adult says a word. Child writes it and circles any multi-letter phonograms: ship, back, rain, day, light, boat, girl, hurt, coin, book.",
        ["ship","back","rain","day","light","boat","girl","hurt","coin"], "Flash all cards today!")

    # 2: Long Vowels
    yield 2, build_long_vowels()

    # 3-6: Silent E reasons 12.1-12.4
    for i, key in enumerate(["12.1","12.2","12.3","12.4"]):
        yield 3+i, build_silent_e(3+i, key)

    # 7: SE Review 12.1-4
    yield 7, build_review3(7, "Silent E Review: Reasons 12.1–12.4",
        "Name That Reason",
        "Adult says a word. Child names which Silent E reason (12.1, 12.2, 12.3, or 12.4) applies.\n\ntape → 12.1 (vowel says long)\nhave → 12.2 (no V at end)\ndance → 12.3 (C says /s/)\nlittle → 12.4 (syllable needs vowel)\nmake → 12.1\nblue → 12.2\nchange → 12.3\ntable → 12.4",
        "Word Sort",
        "Sort these words into four columns by reason: make, have, dance, little, hope, give, since, apple, cube, live, prince, candle, these, solve, fence, bubble.",
        "Challenge: Change It",
        "Adult says a word without silent E. Child adds silent E and says which reason: cap→cape (12.1), giv→give (12.2), lac→lace (12.3), littl→little (12.4).",
        ["make","have","dance","little","hope","give","since","table"], "Review reasons 12.1-12.4 at home!")

    # 8-12: Silent E reasons 12.5-12.9
    for i, key in enumerate(["12.5","12.6","12.7","12.8","12.9"]):
        yield 8+i, build_silent_e(8+i, key)

    # 13: Name That Reason practice
    yield 13, build_se_practice()

    # 14-16: Rules 1, 2 + Spelling
    yield 14, build_rule3(14, "1")
    yield 15, build_rule3(15, "2")
    yield 16, build_se_ce_ge_spelling()

    # 17-23: dge, tch, kn, gn, wr + reviews
    yield 17, build_multi3(17, "dge")
    yield 18, build_multi3(18, "tch")
    yield 19, build_review3(19, "Review: DGE and TCH",
        "DGE or GE?",
        "Adult says a word. Child decides: DGE or GE?\n\nbridge (DGE — short i)\ncage (GE — long a)\nfudge (DGE — short u)\nlarge (GE — consonant r before)\nedge (DGE — short e)\nhuge (GE — long u)",
        "TCH or CH?",
        "Same game for TCH/CH:\n\ncatch (TCH — short a)\ninch (CH — consonant n before)\npitch (TCH — short i)\nlunch (CH — consonant n before)\nnotch (TCH — short o)",
        "Build It",
        "Write: bridge, edge, catch, watch, large, inch. Underline DGE/TCH/GE/CH.",
        ["bridge","catch","large","watch","edge","inch"], "Find TCH and DGE words in a book!")

    yield 20, build_multi3(20, "kn")
    yield 21, build_multi3(21, "gn")
    yield 22, build_multi3(22, "wr")

    yield 23, build_review3(23, "Review: Silent Letter Phonograms kn gn wr",
        "Silent Letter Hunt",
        "Which letter is silent?\n\nknife → K is silent\nsign → G is silent\nwrite → W is silent\nknee → K\ngnat → G\nwrong → W\nknow → K\ndesign → G\nwrist → W",
        "Read the Word",
        "Adult writes these words. Child reads them aloud: know, sign, write, knee, gnat, wrong, knock, design, wrap, gnaw.",
        "Dictation Challenge",
        "Adult says a word. Child writes it: know, sign, write, knee, wrap, wrong.",
        ["know","sign","write","knee","gnat","wrap"], "Write each kn/gn/wr word 3 times!")

    # 24: Mid-Assessment
    yield 24, build_mid3()

    # 25-35: More PGs + Rule 28
    for num, pg in [(25,"eigh"),(26,"ei"),(27,"ey"),(28,"ph"),(29,"gh"),(30,"ough"),(31,"augh")]:
        yield num, build_multi3(num, pg)
    yield 32, build_rule3(32, "28")
    for num, pg in [(33,"ew"),(34,"ui"),(35,"eu")]:
        yield num, build_multi3(num, pg)

    # 36-40: Rules 5,6,7,8,10
    for num, key in [(36,"5"),(37,"6"),(38,"7"),(39,"8"),(40,"10")]:
        yield num, build_rule3(num, key)

    # 41-42: wor, ie
    yield 41, build_multi3(41, "wor")
    yield 42, build_multi3(42, "ie")

    # 43-46: Syllable Division
    yield 43, build_syllable(43, "compound")
    yield 44, build_syllable(44, "vccv")
    yield 45, build_syllable(45, "vcv")
    yield 46, build_syllable(46, "cle")

    # 47: Schwa
    yield 47, build_rule3(47, "31")

    # 48-49: Readers
    yield 48, build_gwen()
    yield 49, build_cole()

    # 50: Mixed Spelling
    yield 50, build_mixed_spelling()

    # 51-52: Reviews
    pg_list_3 = "dge, tch, kn, gn, wr, eigh, ei, ey, ph, gh, ough, augh, ew, ui, eu, wor, ie"
    yield 51, build_review3(51, "Review: All Stage 3 Phonograms",
        "Speed Flash", f"Flash ALL 75 phonograms. Focus on new ones: {pg_list_3}.",
        "Phonogram Bingo",
        "Pick 9 phonograms. Adult calls sounds. Cross off matching phonograms. Get 3 in a row to win!",
        "Most Sounds Award",
        "Which Stage 3 phonogram has the most sounds? (ough — 6 sounds!) Name all 6.",
        ["bridge","catch","know","sign","write","eight","phone","ghost","though","caught","few","fruit","work","field"], "Flash all cards!")

    yield 52, build_review3(52, "All Stage 3 Rules Review",
        "Rule Speed Round",
        "Adult says a rule number. Child states the rule:\n\n1 (C softens before E I Y)\n2 (G may soften before E I Y)\n5 (I/Y at end of syllable)\n6 (Y=/ī/ in one-syllable)\n7 (I/Y may say /ē/)\n8 (I/O before two consonants)\n10 (A=/ä/ at end, after W, before L)\n25 (DGE after short vowel)\n27 (TCH after short vowel)\n28 (GH phonograms)\n31 (Schwa in unstressed syllables)",
        "Which Rule?",
        "Adult says a word. Child names all rules that apply.\n\nbridge → Rule 25 (DGE after short vowel)\ncatch → Rule 27 (TCH after short vowel)\ncent → Rule 1 (C softens)\ngem → Rule 2 (G softens)\nby → Rule 6 (Y=/ī/)\nbaby → Rule 7 (Y=/ē/)\nfind → Rule 8 (I before two consonants)\nwater → Rule 10 (A=/ä/ after W)\nlaugh → Rule 28 (GH=/f/)",
        "Spelling Challenge",
        "Apply the rules to spell: dance, large, bridge, catch, by, baby, find, water, laugh, light.",
        ["dance","large","bridge","catch","by","baby","find","water","laugh","light"], "Review your rule flashcards!")

    # 53-54: HF Words
    yield 53, build_hf3(53, 4, HF4,
        "Where is the cat? There is a dog! Their hats are red. We were in the park. Come here!",
        "Where is the dog? We were in the park. Come here now!",
        "where")
    yield 54, build_hf3(54, 5, HF5,
        "I read it once. Two cats ran. Does the dog bark? Any cat can jump. Many dogs play.",
        "I went once. Two cats ran. Does it bark?",
        "once")

    # 55: Sail Box reader
    yield 55, build_sail()

    # 56: Assessment
    yield 56, build_final3()


def build_long_vowels():
    return """# Lesson 2: Long Vowel Sounds

**Stage 3** · Lesson 2 · vowel-concept

---

## Warm-Up: Short Vowel Review

> Adult says: "Say the short sound of each vowel." Child responds.

| Vowel | Short Sound | Example |
|-------|------------|---------|
| a | /ă/ | cat, hat |
| e | /ĕ/ | bed, red |
| i | /ĭ/ | sit, big |
| o | /ŏ/ | hot, dog |
| u | /ŭ/ | cup, sun |

---

## New Learning: The Long Vowel Sounds

### Vowels Have TWO Main Sounds

Each vowel has at least two sounds: a **short** sound and a **long** sound. The long sound is just the vowel's NAME.

| Vowel | Short Sound | Long Sound (Name) | Short Example | Long Example |
|-------|------------|-------------------|---------------|-------------|
| a | /ă/ | /ā/ | cat | cake, make, day |
| e | /ĕ/ | /ē/ | bed | these, see, tree |
| i | /ĭ/ | /ī/ | sit | time, light, by |
| o | /ŏ/ | /ō/ | dog | hope, boat, go |
| u | /ŭ/ | /ū/ | cup | cube, few, unit |

### The Macron Mark —

When a vowel says its long sound, we mark it with a **macron** (—) — a straight line above the letter.

> ˘ = short &nbsp;&nbsp;|&nbsp;&nbsp; — = long

### How Do We Know When a Vowel Is Long?

Several clues tell us:
1. **Silent E** — The E at the end makes the vowel long (cake, time, hope)
2. **Open syllable** — Vowel at end of syllable says its long sound (go, he, ba·by)
3. **Vowel teams** — Two vowels together often make the first one long (rain, boat, see)

We'll learn ALL of these in Stage 3!

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
| make | m (/m/), a (/ā/), k (/k/), e — silent E (12.1) | SE 12.1: vowel says long | /māk/ |
| time | t (/t/), i (/ī/), m (/m/), e — silent E (12.1) | SE 12.1 | /tīm/ |
| go | g (/g/), o (/ō/) | Rule 4: open syllable | /gō/ |

---

## Quick Check

1. What is a long vowel sound? *(The vowel says its name.)*
2. What mark shows a long vowel? *(A macron —)*
3. Name a clue that tells you a vowel is long. *(Silent E, open syllable, or vowel team.)*

---

**Next lesson:** Lesson 3: Silent E Reason 1

---

*Practice at home: Find 5 words with long vowels in a book.*
"""

def build_se_practice():
    return """# Lesson 13: Silent E — Name That Reason

**Stage 3** · Lesson 13 · practice

---

## Warm-Up: Silent E Flash

> Adult flashes words written on cards. Child reads the word and names which Silent E reason applies.

---

## Practice: Name That Reason

For each word, identify which Silent E reason (12.1–12.9) applies. Some words could fit more than one!

| Word | Reason(s) | Why? |
|------|-----------|------|
| tape | 12.1 | Vowel says long |
| have | 12.2 | No V at end |
| dance | 12.3 | C says /s/ before E |
| little | 12.4 | Syllable needs vowel |
| house | 12.5 | Not plural — S doesn't mean plural |
| pie | 12.6 | Word looks too short without E |
| bathe | 12.7 | TH is voiced |
| bye | 12.8 | Clarify meaning (vs. by) |
| come | 12.9 | Unseen/historical reason |
| make | 12.1 | Vowel says long |
| give | 12.2 | No V at end |
| change | 12.3 | G says /j/ before E |
| table | 12.4 | Syllable needs vowel |
| please | 12.5 | Not plural |
| owe | 12.6 + 12.8 | Looks bigger AND clarifies meaning |
| some | 12.9 | Unseen reason |

---

## Mixed Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
| cape | c (/k/), a (/ā/), p (/p/), e — SE (12.1) | SE 12.1 | /kāp/ |
| live | l (/l/), i (/ĭ/), v (/v/), e — SE (12.2) | SE 12.2 | /lĭv/ |
| fence | f (/f/), e (/ĕ/), n (/n/), c (/s/), e — SE (12.3) | SE 12.3 + Rule 1 | /fĕns/ |
| candle | c (/k/), a (/ă/), n (/n/), d (/d/), le — SE (12.4) | SE 12.4 | căn-dl |

---

## Quick Check

1. Which Silent E reason is most common? *(12.1 — vowel says long)*
2. Which reason explains 'have' and 'give'? *(12.2 — no V at end)*
3. Spell 'bridge' — is DGE a Silent E word? *(Yes — DGE uses silent E after Rule 25!)*

---

**Next lesson:** Lesson 14: Rule 1 — C Softens

---

*Practice at home: Find 10 silent E words in a book. Name the reason for each!*
"""

def build_se_ce_ge_spelling():
    words = [
        ("cent","c (/s/), e (/ĕ/), n (/n/), t (/t/)","Rule 1: C=/s/ before E","/sĕnt/"),
        ("gem","g (/j/), e (/ĕ/), m (/m/)","Rule 2: G=/j/ before E","/jĕm/"),
        ("face","f (/f/), a (/ā/), c (/s/), e — SE (12.1/12.3)","Rules 1 + 12.1","/fās/"),
        ("change","ch (/ch/), a (/ā/), n (/n/), g (/j/), e — SE (12.3)","Rule 2 + SE 12.3","/chānj/"),
        ("since","s (/s/), i (/ĭ/), n (/n/), c (/s/), e — SE (12.3)","Rule 1 + SE 12.3","/sĭns/"),
    ]
    rows = "\n".join(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in words)
    return f"""# Lesson 16: Spelling Analysis — ce ci ge gi

**Stage 3** · Lesson 16 · spelling-analysis

---

## Warm-Up: Phonogram Flash Review

> Quick flash of all known phonograms.

---

## Rules in Action: C Softens, G May Soften

Today we practice spelling words where C says /s/ and G says /j/.

### Rule 1: C always softens to /s/ before E, I, or Y.

### Rule 2: G may soften to /j/ before E, I, or Y.

---

## Spelling Analysis

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{rows}

---

## Reading Practice

> cent &nbsp;&nbsp; gem &nbsp;&nbsp; face &nbsp;&nbsp; change &nbsp;&nbsp; since &nbsp;&nbsp; city &nbsp;&nbsp; giant &nbsp;&nbsp; cage

> The cent is in the case. I see a gem. Can you change it? I have been here since then.

---

## Quick Check

1. When does C say /s/? *(Before E, I, or Y — Rule 1)*
2. When does G say /j/? *(It MAY before E, I, or Y — Rule 2)*
3. Spell 'cent' and 'gem' from dictation.

---

**Next lesson:** Lesson 17: Phonogram dge

---

*Practice at home: Find words with ce, ci, ge, gi in a book.*
"""

def build_gwen():
    return """# Lesson 48: Gwen Gives a Gift

**Stage 3** · Lesson 48 · reader

---

## Warm-Up: Phonogram Flash Review

> Quick flash of phonograms used in today's story.

| Phonograms to review |
|----------------------|
| g (both sounds), silent E, ee, ai, ay, ow |

---

## Warm-Up Words — Read These First

Read each word sound by sound BEFORE reading the story:

> Gwen &nbsp; Grace &nbsp; gift &nbsp; goat &nbsp; goose &nbsp; green &nbsp; gives &nbsp; golden &nbsp; gate &nbsp; grass

---

## Story: Gwen Gives a Gift

<div class="reader-page">

<div class="reader-text">

**Gwen Gives a Gift**

Gwen the goose has a gift.

The gift is for her best friend, Grace.

Grace is a goat. She lives on the farm with Gwen.

Gwen wraps the gift in green paper. She ties it with a big bow.

"Where is Grace?" Gwen asks.

Grace is at the gate. She is eating grass.

"Grace!" calls Gwen. "I have a gift for you!"

Grace looks up. Her eyes get wide.

"A gift? For me?"

Gwen gives the gift to Grace. Grace tears the paper.

Inside is a golden bell!

Grace rings the bell. Ding! Ding!

"I love it!" says Grace. "Thank you, Gwen!"

Gwen grins. "You are welcome, Grace."

The two friends sit in the grass. The sun is warm. The bell shines.

What a good day.

The End.

</div>

<div class="reader-sidebar">

### Spelling Aid

**Focus phonograms:** g (both sounds), silent E, ee, ai, ay, ow

**Rule check:**
- 'Gwen' — G says /g/ (doesn't soften before w)
- 'Grace' — G says /g/ (doesn't soften before r)
- 'gem' — G says /j/ (softens before e)
- 'gives' — G says /g/ (doesn't soften — exception!)
- 'Grace' — C says /k/ (before consonant)

**Say-to-Spell:** Give = /gĭv/ to hear the short I. Friend = /frēnd/ to hear the IE.

</div>

</div>

---

## Quick Check

1. What gift did Gwen give Grace? *(A golden bell!)*
2. How many G words can you find in the story? *(Gwen, goose, gift, Grace, goat, green, grass, gives, gets, golden, grins, good — 12!)*
3. Which G's say /g/ and which say /j/? *(All say /g/ in this story except 'gem' which isn't here, but 'gift' and 'gives' are exceptions to the softening rule.)*

---

**Next lesson:** Lesson 49: Cole and His Bike

---

*Practice at home: Read this story aloud to a family member!*
"""

def build_cole():
    return """# Lesson 49: Cole and His Bike

**Stage 3** · Lesson 49 · reader

---

## Warm-Up: Phonogram Flash Review

> Quick flash of phonograms used in today's story.

| Phonograms to review |
|----------------------|
| silent E, ie, ai, ay, ck |

---

## Warm-Up Words — Read These First

Read each word sound by sound BEFORE reading the story:

> Cole &nbsp; Kate &nbsp; bike &nbsp; rides &nbsp; hill &nbsp; fast &nbsp; red &nbsp; friend &nbsp; share &nbsp; calls

---

## Story: Cole and His Bike

<div class="reader-page">

<div class="reader-text">

**Cole and His Bike**

Cole has a bike. It is red and fast.

Cole rides his bike to the park. He rides up the hill. He rides down the hill.

Whee! Cole goes fast!

At the park, Cole sees his friend Kate.

"Hi, Kate!" calls Cole.

"Hi, Cole! I like your bike," says Kate. "Can I ride it?"

Cole stops. He thinks. He likes his bike. But Kate is his friend.

"You can ride it," says Cole. "Be safe!"

Kate gets on the bike. She rides around the park.

"This is fun!" Kate yells. "Thank you, Cole!"

"It's a good bike," Cole says. "We can share it."

Cole and Kate take turns. Cole rides. Kate rides. Cole rides again.

When the sun sets, they go home. Cole waves to Kate.

"See you next time!"

The End.

</div>

<div class="reader-sidebar">

### Spelling Aid

**Focus phonograms:** silent E (make says /ā/), oo, ai, ay, igh

**Rule check:**
- 'bike' — Silent E 12.1 (i says /ī/)
- 'rides' — Silent E 12.1 (i says /ī/) + S
- 'like' — Silent E 12.1 (i says /ī/)
- 'safe' — Silent E 12.1 (a says /ā/), 12.3? No — F is between A and E
- 'home' — Silent E 12.1 (o says /ō/)
- 'share' — Silent E 12.1 (a says /ā/)
- 'turns' — UR says /er/
- 'Cole' — C says /k/, O says /ō/ (open syllable), silent E (12.1? No, the E is making O long through the L)
- 'friend' — IE says /ĕ/ (unusual!), say-to-spell: /frēnd/

**Say-to-Spell:** friend = /frēnd/, bike = /bīk/, nice = /nīs/

</div>

</div>

---

## Quick Check

1. What does Cole share with Kate? *(His bike!)*
2. Find 3 silent E words in the story. *(bike, rides, like, safe, home, take, share, waves, time)*
3. Why does 'Cole' end with silent E? *(The E makes the O say /ō/ — SE 12.1)*

---

**Next lesson:** Lesson 50: Mixed Spelling Analysis

---

*Practice at home: Read this story aloud!*
"""

def build_sail():
    return """# Lesson 55: The Sail Box

**Stage 3** · Lesson 55 · reader

---

## Warm-Up: Phonogram Flash Review

> Quick flash of phonograms used in today's story.

| Phonograms to review |
|----------------------|
| silent E (all 9 reasons), ai, ay, dge, tch |

---

## Warm-Up Words — Read These First

Read each word sound by sound BEFORE reading the story:

> Jake &nbsp; sail &nbsp; boat &nbsp; box &nbsp; shed &nbsp; blue &nbsp; paint &nbsp; folds &nbsp; tapes &nbsp; finds

---

## Story: The Sail Box

<div class="reader-page">

<div class="reader-text">

**The Sail Box**

Jake finds a big box in the shed. The box is brown and old.

"What can I make with this box?" Jake thinks.

Jake has an idea. He will make a boat!

Jake takes the box outside. He folds the sides to make a point. He tapes them tight.

"This will be the sail," Jake says. He finds a white cloth and a long stick.

Jake paints the box blue. The paint smells strange. It drips on his shirt.

Mom sees Jake. "What are you making?"

"A sail boat! I will sail it on the pond."

Mom smiles. "That is a fine boat. Be safe at the pond."

Jake takes the boat to the pond. He sets it on the water.

The boat floats! The white sail catches the wind.

"Wow!" Jake shouts. "It really works!"

The boat drifts across the pond. Jake runs along the edge to keep up.

When the sun goes down, Jake brings the boat home. He is tired but proud.

What a grand day.

The End.

</div>

<div class="reader-sidebar">

### Spelling Aid

**Focus phonograms:** ai (sail, paint, rain), silent E (make, fine, home), igh (tight, night), ou (outside, shouts), ea (idea, really), ck (back, stick)

**Rule check:**
- 'makes' — Silent E 12.1 (a says /ā/)
- 'sail' — AI says /ā/, never at end (Rule 3)
- 'tight' — IGH says /ī/, GH silent (Rule 28)
- 'floats' — OA says /ō/
- 'edge' — DGE after short e (Rule 25)
- 'paints' — AI says /ā/, never at end
- 'boat' — OA says /ō/
- 'drifts' — silent E? No — the S is just plural. 'drift' has a consonant blend.

</div>

</div>

---

## Quick Check

1. What does Jake make from the box? *(A sail boat!)*
2. Find a word with AI. Find a word with OA. *(sail/paint/rain; boat/floats)*
3. Why does 'edge' use DGE? *(Rule 25: DGE after short vowel e)*

---

**Next lesson:** Lesson 56: Stage 3 Mastery Check

---

*Practice at home: Read this story aloud! Then try to build your own boat from a box!*
"""

def build_mixed_spelling():
    words = [
        ("bridge","b (/b/), r (/r/), i (/ĭ/), dge (/j/)","Rule 25","/brĭj/"),
        ("caught","c (/k/), augh (/ä/), t (/t/)","Rule 28","/kät/"),
        ("though","th (/th/), ough (/ō/)","Rule 28","/thō/"),
        ("phone","ph (/f/), o (/ō/), n (/n/), e — SE (12.1)","PH = /f/","/fōn/"),
        ("few","f (/f/), ew (/ü/)","EW at end","/fü/"),
        ("fruit","f (/f/), r (/r/), ui (/ü/), t (/t/)","UI=/ü/","/früt/"),
        ("work","wor (/wer/), k (/k/)","WOR = /wer/","/werk/"),
        ("field","f (/f/), ie (/ē/), l (/l/), d (/d/)","IE=/ē/","/fēld/"),
    ]
    bonus = [
        ("eight","eigh (/ā/), t (/t/)","Rule 28","/āt/"),
        ("laugh","l (/l/), augh (/ăf/)","Rule 28","/lăf/"),
        ("neutral","n (/n/), eu (/ü/), t (/t/), r (/r/), a (/ă/), l (/l/)","EU=/ü/","nü-trăl"),
    ]
    rows = "\n".join(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in words)
    brows = "\n".join(f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} |" for w in bonus)
    return f"""# Lesson 50: Mixed Spelling Analysis — Stage 3

**Stage 3** · Lesson 50 · spelling-analysis

---

## Warm-Up: Phonogram Flash Review

> Flash ALL 75 phonograms.

---

## Mixed Spelling Analysis

Today we practice ALL the spelling skills from Stage 3: silent E, new phonograms, new rules.

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{rows}

---

## Bonus Challenge

| Word | Phonograms Used | Rules Applied | Say-to-Spell |
|------|----------------|---------------|--------------|
{brows}

---

## Reading Practice

> The bridge is old. I caught the ball. Though it rained, we played. My phone rang. A few birds flew. The fruit is sweet. We work hard. The field is green.

---

## Quick Check

1. Which phonogram had the most sounds today? *(ough — multiple sounds)*
2. Which word was hardest to spell? Why?
3. Spell 'bridge' and 'caught' from dictation.

---

**Next lesson:** Lesson 51: All Stage 3 Phonograms Review

---

*Practice at home: Choose 3 words from today. Write each one 3 times.*
"""

def build_mid3():
    return ASSESSMENT3_TEMPLATE.format(
        num=24, title="Mid-Stage 3 Assessment",
        overview="Check progress on Silent E (reasons 1-4), first 5 new multi-letter PGs, and Rules 1-2.",
        pg_check="| a | /ă/ /ā/ /ä/ | ☐ |\n| c | /k/ /s/ | ☐ |\n| g | /g/ /j/ | ☐ |\n| sh | /sh/ | ☐ |\n| th | /th/ (2) | ☐ |\n| ck | /k/ | ☐ |\n| ee | /ē/ | ☐ |\n| oi | /oi/ | ☐ |\n| oy | /oi/ | ☐ |\n| ai | /ā/ | ☐ |\n| ay | /ā/ | ☐ |\n| dge | /j/ | ☐ |\n| tch | /ch/ | ☐ |\n| kn | /n/ | ☐ |\n| gn | /n/ | ☐ |\n| wr | /r/ | ☐ |",
        pg_total=16,
        se_check="| tape | ☐ |\n| have | ☐ |\n| dance | ☐ |\n| little | ☐ |\n| make | ☐ |\n| give | ☐ |\n| change | ☐ |\n| table | ☐ |",
        se_total=8,
        read_check="| make | ☐ |\n| have | ☐ |\n| dance | ☐ |\n| little | ☐ |\n| bridge | ☐ |\n| catch | ☐ |\n| know | ☐ |\n| sign | ☐ |\n| write | ☐ |\n| cent | ☐ |",
        read_total=10,
        spell_check="| make | ☐ |\n| have | ☐ |\n| dance | ☐ |\n| bridge | ☐ |\n| catch | ☐ |\n| know | ☐ |\n| write | ☐ |\n| cent | ☐ |",
        spell_total=8,
        rule_check="| SE 12.1 | What does silent E do to the vowel? | ☐ |\n| SE 12.2 | Why do 'have' and 'give' have silent E? | ☐ |\n| SE 12.4 | Why does 'little' end in silent E? | ☐ |\n| Rule 1 | When does C say /s/? | ☐ |\n| Rule 25 | When do we use DGE? | ☐ |\n| Rule 27 | When do we use TCH? | ☐ |",
        rule_total=6,
        next_steps="If ≥85%: Continue to second half of Stage 3. If weaker, review trouble spots.",
    )

def build_final3():
    return ASSESSMENT3_TEMPLATE.format(
        num=56, title="Stage 3 Mastery Check",
        overview="Final Stage 3 assessment. Check mastery of all Silent E reasons, 21 new multi-letter phonograms, syllable division, and all Stage 3 rules.",
        pg_check="| dge | /j/ | ☐ |\n| tch | /ch/ | ☐ |\n| kn | /n/ | ☐ |\n| gn | /n/ | ☐ |\n| wr | /r/ | ☐ |\n| eigh | /ā/ | ☐ |\n| ei | /ē/ /ā/ /ī/ | ☐ |\n| ey | /ā/ /ē/ | ☐ |\n| ph | /f/ | ☐ |\n| gh | /g/ | ☐ |\n| ough | /ō/ /ö/ /ow/ /ŭf/ /äf/ /ü/ | ☐ |\n| augh | /ä/ /ăf/ | ☐ |\n| ew | /ü/ /ö/ | ☐ |\n| ui | /ü/ /ö/ | ☐ |\n| eu | /ü/ /ö/ | ☐ |\n| wor | /wer/ | ☐ |\n| ie | /ē/ /ī/ | ☐ |",
        pg_total=17,
        se_check="| tape | ☐ |\n| have | ☐ |\n| dance | ☐ |\n| little | ☐ |\n| house | ☐ |\n| pie | ☐ |\n| bathe | ☐ |\n| bye | ☐ |\n| come | ☐ |",
        se_total=9,
        read_check="| bridge | ☐ |\n| catch | ☐ |\n| know | ☐ |\n| write | ☐ |\n| eight | ☐ |\n| phone | ☐ |\n| though | ☐ |\n| caught | ☐ |\n| few | ☐ |\n| fruit | ☐ |\n| work | ☐ |\n| field | ☐ |",
        read_total=12,
        spell_check="| bridge | ☐ |\n| catch | ☐ |\n| know | ☐ |\n| write | ☐ |\n| eight | ☐ |\n| phone | ☐ |\n| though | ☐ |\n| caught | ☐ |\n| fruit | ☐ |\n| field | ☐ |",
        spell_total=10,
        rule_check="| SE 12.1-9 | Name 5 of the 9 silent E reasons. | ☐ |\n| Rule 1 | When does C say /s/? | ☐ |\n| Rule 2 | When does G say /j/? | ☐ |\n| Rule 6 | What does Y say in 'by'? | ☐ |\n| Rule 7 | What does Y say in 'baby'? | ☐ |\n| Rule 8 | Why does I say /ī/ in 'find'? | ☐ |\n| Rule 25 | When to use DGE? | ☐ |\n| Rule 28 | What can GH do? | ☐ |\n| Rule 31 | What is schwa? | ☐ |",
        rule_total=9,
        next_steps="If ≥85%: Move to Stage 4! If weaker, review specific trouble areas and retest in 1-2 weeks.",
    )

# ── WRITE ───────────────────────────────────────────────────────────

S = {
    1:"review-stage2",2:"long-vowels",
    3:"silent-e-1",4:"silent-e-2",5:"silent-e-3",6:"silent-e-4",
    7:"silent-e-review-1",8:"silent-e-5",9:"silent-e-6",10:"silent-e-7",
    11:"silent-e-8",12:"silent-e-9",13:"silent-e-mastery",
    14:"rule-1",15:"rule-2",16:"spell-ce-ci-ge",
    17:"pg-dge",18:"pg-tch",19:"rule-25-27",
    20:"pg-kn",21:"pg-gn",22:"pg-wr",23:"silent-letter-review",
    24:"assessment-4",
    25:"pg-eigh",26:"pg-ei",27:"pg-ey",28:"pg-ph",29:"pg-gh",
    30:"pg-ough",31:"pg-augh",32:"rule-28",
    33:"pg-ew",34:"pg-ui",35:"pg-eu",
    36:"rule-5",37:"rule-6",38:"rule-7",39:"rule-8",40:"rule-10",
    41:"pg-wor",42:"pg-ie",
    43:"syllables-1",44:"syllables-2",45:"syllables-3",46:"syllables-4",
    47:"rule-31",
    48:"reader-2",49:"reader-3",
    50:"spell-mixed-3",
    51:"review-8",52:"rule-review-3",
    53:"hf-words-4",54:"hf-words-5",
    55:"reader-4",56:"assessment-5",
}

def main():
    for num, content in generate():
        slug = S.get(num, f"lesson-{num:03d}")
        (OUT / f"{slug}.md").write_text(content, encoding="utf-8")
        print(f"  lessons/stage-3/{slug}.md")
    print(f"\nDone! 56 lessons in lessons/stage-3/")

if __name__ == "__main__":
    main()
