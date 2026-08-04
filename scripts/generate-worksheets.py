#!/usr/bin/env python3
"""Generate student worksheets: phonogram practice, rule practice, flash cards, game cards."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "worksheets"

# Create subdirectories
for d in ["phonograms", "rules", "cards", "handwriting", "blank"]:
    (OUT / d).mkdir(parents=True, exist_ok=True)

# ── PHONOGRAM DATA ──────────────────────────────────────────────────

SINGLE = {
    "a": {"sounds": "/ă/ /ā/ /ä/", "words": ["at","cat","hat","bat","rat","sat","mat","fat","pat","cap","map","nap","tap","lap","gap","bag","tag","rag","wag","had","mad","sad","dad"]},
    "b": {"sounds": "/b/", "words": ["bat","big","bed","bug","bag","bit","bet","but","bun","bad","box","bell","ball","bump","bend","best","boat","book","boy","brown"]},
    "c": {"sounds": "/k/ /s/", "words": ["cat","cot","cup","cap","cab","cub","cop","cut","cent","city","cycle","face","ice","dance","rice","mice","nice","pace","race","lace"]},
    "d": {"sounds": "/d/", "words": ["dog","dad","dig","dug","dot","dim","dip","dash","dish","desk","drum","drop","dress","drink","door","dark","day","deep","dear","down"]},
    "e": {"sounds": "/ĕ/ /ē/", "words": ["bed","red","fed","led","get","set","let","met","pet","vet","wet","hen","pen","ten","men","leg","beg","yes","egg","end"]},
    "f": {"sounds": "/f/", "words": ["fun","fan","fin","fit","fat","fig","fog","fox","fix","fish","fast","frog","flag","from","free","food","feet","five","four","full"]},
    "g": {"sounds": "/g/ /j/", "words": ["go","get","got","gut","gap","gas","gum","gig","gem","giant","gym","age","cage","page","huge","large","change","strange","gentle","ginger"]},
    "h": {"sounds": "/h/", "words": ["hat","hot","hen","hog","hug","hip","hop","hum","ham","him","her","his","has","had","hand","help","hill","home","hope","house"]},
    "i": {"sounds": "/ĭ/ /ī/ /ē/", "words": ["it","in","if","is","sit","fit","hit","bit","pit","big","dig","fig","pig","rig","wig","him","dim","pin","fin","tin"]},
    "j": {"sounds": "/j/", "words": ["jam","jet","jog","jug","job","jump","just","joke","jelly","judge","join","joy","jar","jack","June","July","jacket","jingle","jungle"]},
    "k": {"sounds": "/k/", "words": ["kit","kin","kid","kiss","king","keep","kept","kind","kite","knee","knock","know","knife","knot","knit","kayak","kitten","kettle","kernel"]},
    "l": {"sounds": "/l/", "words": ["leg","log","lap","lip","lot","lit","let","lad","led","lid","lamp","land","last","left","lift","love","live","long","look","like"]},
    "m": {"sounds": "/m/", "words": ["man","map","mat","mop","mud","mom","men","met","mix","mill","milk","make","made","much","must","most","more","many","may","my"]},
    "n": {"sounds": "/n/", "words": ["net","not","nut","nap","nip","nod","new","now","name","nine","nice","near","need","next","night","nose","note","number","never","nothing"]},
    "o": {"sounds": "/ŏ/ /ō/ /ö/", "words": ["on","off","odd","got","hot","not","pot","dot","lot","cot","go","no","so","old","open","over","only","both","most","post"]},
    "p": {"sounds": "/p/", "words": ["pat","pot","pet","pit","put","pan","pen","pin","pop","pup","pick","pack","play","please","plant","print","park","part","pass","pull"]},
    "qu": {"sounds": "/kw/", "words": ["queen","quit","quick","quack","quilt","quiz","quest","quiet","quite","quote","quarter","question","quench","quiver","quail","quarry"]},
    "r": {"sounds": "/r/", "words": ["rat","red","rug","run","ran","rip","rob","rub","rest","rain","read","ride","road","rock","room","right","round","river","rabbit","rainbow"]},
    "s": {"sounds": "/s/ /z/", "words": ["sat","sit","set","sun","sad","sip","sop","sap","see","say","saw","has","is","his","as","use","rose","nose","these","those"]},
    "t": {"sounds": "/t/", "words": ["top","tap","tip","tag","tub","ten","ton","tan","tell","take","time","tree","train","truck","turn","true","try","two","to","too"]},
    "u": {"sounds": "/ŭ/ /ū/ /ö/", "words": ["up","us","cut","hut","nut","rug","bug","hug","jug","mug","fun","run","sun","bun","cup","pup","put","push","pull","full"]},
    "v": {"sounds": "/v/", "words": ["van","vet","vat","vim","vig","vine","vote","very","visit","voice","view","valley","value","village","vegetable","vacuum","victory","violin","volcano"]},
    "w": {"sounds": "/w/", "words": ["wet","win","wag","wit","web","was","way","went","want","well","will","with","wish","work","word","world","water","watch","white"]},
    "x": {"sounds": "/ks/ /z/", "words": ["ax","ox","box","fox","fix","mix","six","tax","wax","next","text","exit","exam","extra","expert","expect","explain","explore","extreme"]},
    "y": {"sounds": "/y/ /ĭ/ /ī/ /ē/", "words": ["yes","yet","yell","yip","yam","yak","by","my","cry","fly","sky","try","why","gym","myth","baby","happy","funny","silly","very"]},
    "z": {"sounds": "/z/", "words": ["zip","zap","zig","zag","zed","zoo","zone","zero","zoom","zebra","zesty","zipper","zigzag","pizza","puzzle","dizzy","fuzzy","buzz","fizz","jazz"]},
}

MULTI = {
    "sh": {"sounds": "/sh/", "words": ["ship","fish","wish","dash","rush","hush","gush","mush","push","bush","dish","wash","cash","lash","mash","shed","shop","shot","shut","shall"]},
    "th": {"sounds": "/th/ (voiced) /th/ (unvoiced)", "words": ["this","that","them","then","with","thin","path","bath","math","moth","both","than","these","those","there","their","thing","think","thank","three"]},
    "ck": {"sounds": "/k/", "words": ["back","sick","duck","neck","lock","rock","sock","pack","pick","kick","tick","tuck","luck","muck","deck","peck","check","click","stick","truck"]},
    "ee": {"sounds": "/ē/", "words": ["see","bee","fee","free","tree","three","green","sheep","sleep","keep","deep","jeep","need","feed","seed","weed","week","meet","feet","sweet"]},
    "ng": {"sounds": "/ng/", "words": ["sing","ring","king","long","song","bang","hang","rang","sang","wing","bring","thing","spring","string","strong","wrong","young","along","among","during"]},
    "ar": {"sounds": "/är/", "words": ["car","far","bar","jar","tar","star","war","art","arm","are","card","hard","yard","bark","dark","mark","park","part","start","smart"]},
    "or": {"sounds": "/or/", "words": ["for","or","nor","corn","born","horn","torn","worn","form","sort","short","sport","north","horse","force","fork","pork","storm","story","morning"]},
    "er": {"sounds": "/er/", "words": ["her","per","sister","brother","mother","father","water","under","over","never","ever","very","after","better","letter","number","other","paper","river","summer"]},
    "oi": {"sounds": "/oi/", "words": ["coin","oil","join","soil","boil","foil","toil","coil","voice","noise","point","poison","toilet","avoid","spoil","choice","rejoice"]},
    "oy": {"sounds": "/oi/", "words": ["boy","toy","joy","soy","coy","ploy","enjoy","destroy","annoy","employ","decoy","alloy","convoy","deploy","cowboy","oyster","royal","loyal"]},
    "ai": {"sounds": "/ā/", "words": ["rain","pain","main","gain","vain","train","brain","grain","plain","stain","chain","drain","sail","tail","nail","mail","fail","hail","jail","pail"]},
    "ay": {"sounds": "/ā/", "words": ["day","say","way","may","pay","lay","ray","bay","hay","clay","play","stay","gray","tray","pray","spray","today","always","away","maybe"]},
    "ch": {"sounds": "/ch/ /k/ /sh/", "words": ["chin","chip","chop","chat","much","such","rich","which","child","chance","change","chain","chair","chalk","charm","school","echo","chef","machine","brochure"]},
    "wh": {"sounds": "/hw/", "words": ["when","what","why","where","which","white","whale","wheel","wheat","while","whisper","whistle","whether","whoever","whole","whose","whom"]},
    "ea": {"sounds": "/ē/ /ĕ/ /ā/", "words": ["eat","each","read","lead","bead","bean","lean","mean","clean","dream","head","dead","bread","spread","ready","heavy","great","break","steak","bear"]},
    "ow": {"sounds": "/ow/ /ō/", "words": ["cow","how","now","bow","wow","pow","brown","crown","down","town","clown","frown","snow","grow","low","row","show","slow","blow","flow"]},
    "ou": {"sounds": "/ow/ /ō/ /ö/ /ŭ/", "words": ["out","our","hour","loud","proud","cloud","sound","found","round","ground","you","group","soup","through","though","touch","young","double","trouble","couple"]},
    "oo": {"sounds": "/ö/ /ü/ /ō/", "words": ["book","look","took","cook","hook","good","wood","foot","stood","food","moon","soon","room","zoo","too","cool","pool","school","door","floor"]},
    "ed": {"sounds": "/ed/ /d/ /t/", "words": ["wanted","needed","rested","tested","planted","played","called","showed","rained","stayed","fished","jumped","looked","helped","stopped","asked","liked","walked","talked","worked"]},
    "igh": {"sounds": "/ī/", "words": ["light","night","right","sight","tight","might","fight","high","sigh","thigh","bright","fright","flight","slight","delight","tonight","sunlight","daylight","midnight","highlight"]},
    "aw": {"sounds": "/ä/", "words": ["saw","law","raw","paw","jaw","caw","draw","claw","flaw","gnaw","slaw","straw","thaw","squaw","dawn","fawn","lawn","pawn","yawn","awful"]},
    "au": {"sounds": "/ä/", "words": ["cause","pause","sauce","fault","vault","haul","Paul","August","author","autumn","launch","haunt","taunt","daunt","gaunt","jaunt","astronaut","applause","exhaust","caution"]},
    "ir": {"sounds": "/er/", "words": ["girl","bird","dirt","fir","firm","first","sir","stir","thirst","third","shirt","skirt","squirt","birth","circle","circus","thirty","thirteen","dirty","swirl"]},
    "ur": {"sounds": "/er/", "words": ["hurt","turn","burn","fur","curb","curl","curt","nurse","purse","purple","burst","church","curve","surf","turf","Thursday","Saturday","furniture","further","return"]},
    "oa": {"sounds": "/ō/", "words": ["boat","coat","goat","moat","float","road","load","toad","soap","oak","soak","goal","coal","foal","roam","loan","moan","groan","coast","coach"]},
    "ear": {"sounds": "/er/", "words": ["earn","learn","earth","early","heard","pearl","search","earnest","rehearse","earthquake","ear","dear","fear","gear","hear","near","rear","tear","year","clear"]},
}

# Bridge PGs from Stage 3+
MULTI3 = {
    "dge": {"sounds": "/j/", "words": ["bridge","edge","fudge","judge","badge","lodge","ledge","dodge","nudge","ridge","wedge","hedge","pledge","sledge","dredge","trudge","smudge","grudge"]},
    "tch": {"sounds": "/ch/", "words": ["catch","match","patch","latch","batch","hatch","notch","ditch","hitch","pitch","witch","fetch","stretch","scratch","kitchen","butcher","pitcher","catcher","watcher"]},
    "kn": {"sounds": "/n/", "words": ["know","knee","knife","knock","knot","knit","knew","knob","knack","kneel","knight","knowledge","knitting","knuckle","knapsack"]},
    "gn": {"sounds": "/n/", "words": ["sign","gnat","gnaw","gnash","design","resign","assign","campaign","foreign","reign","align","benign","malign","sovereign","condign"]},
    "wr": {"sounds": "/r/", "words": ["write","wrong","wrap","wrist","wreck","wren","wrench","wrinkle","wrangle","wreath","wrestle","wrote","written","writer","wrapping"]},
    "eigh": {"sounds": "/ā/", "words": ["eight","weigh","weight","neigh","sleigh","freight","neighbor","eighteen","eighty","height","sleight","inveigh"]},
    "ei": {"sounds": "/ē/ /ā/ /ī/", "words": ["ceiling","receive","deceive","perceive","vein","rein","feign","feisty","heist","seismic","protein","either","neither","leisure","seize"]},
    "ey": {"sounds": "/ā/ /ē/", "words": ["they","hey","prey","obey","convey","survey","key","valley","money","honey","monkey","turkey","donkey","kidney","chimney"]},
    "ph": {"sounds": "/f/", "words": ["phone","graph","photo","phrase","sphere","Philip","trophy","dolphin","elephant","alphabet","paragraph","telephone","microphone","autograph","photograph"]},
    "gh": {"sounds": "/g/", "words": ["ghost","ghastly","ghetto","ghoul","spaghetti","ghostly","ghoulish","afghan","dinghy","sorghum"]},
    "ough": {"sounds": "/ō/ /ö/ /ow/ /ŭf/ /äf/", "words": ["though","through","cough","rough","tough","enough","bought","fought","sought","thought","dough","although","thorough","borough","breakthrough"]},
    "augh": {"sounds": "/ä/ /ăf/", "words": ["caught","taught","naught","haughty","daughter","slaughter","laugh","laughter","draught","draughty"]},
    "ew": {"sounds": "/ü/ /ö/", "words": ["few","new","grew","blew","flew","drew","crew","stew","chew","threw","knew","newspaper","renew","nephew","jewelry"]},
    "ui": {"sounds": "/ü/ /ö/", "words": ["fruit","suit","juice","build","guild","guilt","biscuit","circuit","cruise","bruise","pursuit","suitable","nuisance","recruit"]},
    "eu": {"sounds": "/ü/", "words": ["neutral","feud","Europe","eucalyptus","pneumonia","therapeutic","leukemia","pseudonym","eulogy","euphoria"]},
    "wor": {"sounds": "/wer/", "words": ["work","word","world","worm","worse","worst","worth","worship","worthy","workshop","network","homework","fireworks","typewriter"]},
    "ie": {"sounds": "/ē/ /ī/", "words": ["field","piece","chief","brief","grief","thief","believe","achieve","relieve","shield","pie","tie","lie","die","fries","cries","dries","tries","flies","spies"]},
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
    """One worksheet per phonogram (75 total)."""
    count = 0
    for pg, data in {**SINGLE, **MULTI, **MULTI3}.items():
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
        count += 1
    return count

def generate_flash_cards():
    """Printable phonogram flash card sheets."""
    # Single-letter cards (4 per page, 7 pages)
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
    
    # Multi-letter cards (4 per page)
    multis = list(MULTI.keys()) + list(MULTI3.keys())
    for page in range(0, len(multis), 4):
        batch = multis[page:page+4]
        cards = ""
        for pg in batch:
            data = {**MULTI, **MULTI3}.get(pg, {"sounds": "—"})
            sounds = data["sounds"]
            cards += f"""<div class="phonogram-card" style="display:inline-block; width:45%; margin:2%; border:2px solid #2a5c8a; border-radius:8px; padding:20px; text-align:center; page-break-inside:avoid;">
<div class="phonogram-letter" style="font-size:48pt; font-weight:bold; color:#2a5c8a; font-family:Georgia,serif;">{pg}</div>
<div class="phonogram-sounds" style="font-size:10pt; color:#555;">{sounds}</div>
</div>\n"""
        
        content = FLASH_CARD_SHEET.format(
            title=f"Multi-Letter Phonograms (Page {(page//4)+1} of {(len(multis)//4)+1})",
            cards=cards)
        (OUT / "cards" / f"flash-multi-{(page//4)+1}.md").write_text(content, encoding="utf-8")
    
    return len(singles) + len(multis)

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
