"""Single source of truth for spelling rules.

31 rules covering the full Logic of English methodology. Each rule
carries:
  - name:  human-readable rule name
  - words: 10-15 decodable example words that illustrate the rule

Rule numbering follows Denise Eide's *Uncovering the Logic of English*
(2012). Rules 1-31 are taught across Stages 2-4.

Stage mapping (RULE_STAGE) lives alongside. Used by:
  - scripts/generate-worksheets.py  (rule practice worksheets)
  - scripts/generate-readers.py     (per-page Spelling Aid sidebars, #20)
  - scripts/generate-animal-readers.py (same)
  - tests/test_catalog.py            (catalog consistency)

The original source data was inlined in scripts/generate-worksheets.py.
This module extracts it for shared use and single source of truth.
"""

RULES: dict[str, dict] = {
    "1": {"name": "C softens to /s/ before E, I, Y", "words": ["cent","city","cycle","face","ice","dance","since","rice","mice","nice","pace","race","lace","place","space"]},
    "2": {"name": "G may soften to /j/ before E, I, Y", "words": ["gem","giant","gym","age","cage","page","huge","large","change","strange","danger","ginger","gentle","giraffe","engine"]},
    "3": {"name": "No English word ends in I, U, V, or J", "words": ["have","give","live","love","blue","true","clue","day","play","boy","toy","new","few","saw","law"]},
    "4": {"name": "A E O U say long at end of syllable", "words": ["go","no","so","he","me","she","we","be","baby","open","music","paper","even","unit","menu"]},
    "5": {"name": "I and Y at end of syllable say /ĭ/ or /ī/", "words": ["item","bicycle","by","my","gym","cry","sky","try","fly","dry","fry","shy","why","spy","reply"]},
    "6": {"name": "Y says /ī/ at end of one-syllable word", "words": ["by","my","cry","fly","sky","try","why","shy","dry","fry","pry","spy","sly","thy","ply"]},
    "7": {"name": "I and Y may say /ē/", "words": ["baby","happy","funny","candy","silly","marine","radio","police","very","many","only","family","city","party","study"]},
    "8": {"name": "I and O may say /ī/ /ō/ before two consonants", "words": ["find","kind","mind","child","wild","blind","old","cold","most","post","bolt","told","gold","hold","roll"]},
    "9": {"name": "AY for /ā/ at end", "words": ["day","say","way","may","pay","play","stay","tray","spray","gray","pray","today","always","away","today"]},
    "10": {"name": "A says /ä/", "words": ["father","wash","watch","papa","mama","bra","spa","ma","pa","want","wash","what","was","swap","wand"]},
    "11": {"name": "Q always needs U", "words": ["queen","quit","quick","quack","quilt","quest","quiet","quite","quote","quart","quake","square","squad","quill","squat"]},
    "12": {"name": "Silent E — nine reasons", "words": ["make","have","race","cage","size","prize","house","these","come"]},
    "13": {"name": "Drop Silent E for vowel suffix", "words": ["make","hope","drive","use","bake","write","change","price","chase","create","invite","raise","surprise","excuse","amuse"]},
    "14": {"name": "Double consonant for vowel suffix", "words": ["run","hop","swim","sit","get","cut","bat","hit","let","nap","plan","shop","skip","step","trip"]},
    "15": {"name": "Y changes to I", "words": ["baby","cry","happy","carry","fly","try","easy","heavy","lucky","plenty","ready","silly","sleepy","tidy","worry"]},
    "16": {"name": "Two I's cannot be adjacent", "words": ["rain","play","wait","train","brain","grain","chain","drain","plain","stain","stay","tray","spray","today","main"]},
    "17": {"name": "Latin /sh/ — TI, CI, SI", "words": ["nation","station","special","official","session","mission","vision","action","motion","fraction","musician","electric","politician","precious","delicious"]},
    "18": {"name": "SH placement", "words": ["ship","wish","cash","dish","wash","fish","fresh","brush","crash","smash","splash","trash","fashion","machine","bruise"]},
    "19": {"name": "Past tense -ED", "words": ["jumped","walked","talked","helped","liked","asked","played","looked","stopped","called","showed","rained","stayed","fished","planted"]},
    "20": {"name": "-ED sounds (/ed/, /d/, /t/)", "words": ["wanted","rested","tested","planted","played","called","showed","rained","stayed","fished","jumped","looked","helped","stopped","asked"]},
    "21": {"name": "Plural nouns", "words": ["cats","dogs","dishes","boxes","churches","buses","foxes","babies","ladies","ponies","wolves","leaves","knives","lives","wives"]},
    "22": {"name": "3rd person singular verbs", "words": ["runs","jumps","sings","swims","plays","walks","talks","helps","looks","stops","asks","wants","needs","likes","makes"]},
    "23": {"name": "Prefix AL-", "words": ["also","always","almost","alone","along","already","aloud","alright","although","altogether"]},
    "24": {"name": "Suffix -FUL", "words": ["joyful","helpful","careful","thankful","peaceful","playful","useful","hopeful","spiteful","truthful","harmful","artful","awful","boastful","doubtful"]},
    "25": {"name": "DGE after short vowel", "words": ["bridge","edge","fudge","judge","badge","lodge","ledge","dodge","nudge","ridge","wedge","hedge","pledge","sledge","trudge"]},
    "26": {"name": "CK after short vowel", "words": ["back","sick","duck","neck","lock","rock","sock","pack","pick","kick","tick","tuck","luck","muck","deck"]},
    "27": {"name": "TCH after short/broad vowel", "words": ["catch","match","patch","latch","batch","hatch","watch","kitchen","pitcher","butcher","witch","fetch","hitch","ditch","notch"]},
    "28": {"name": "GH phonograms (silent, /f/, /g/)", "words": ["high","light","night","right","sight","fight","eight","weight","ghost","though","through","thought","laugh","rough","tough"]},
    "29": {"name": "F vs V vs FE spelling", "words": ["leaf","calf","half","wolf","knife","life","wife","have","love","give","live","save","wave","drive","brave"]},
    "30": {"name": "Double or single final consonant", "words": ["of","bel","mis","tal","ful","gras","plan","step","shop","trip","swim","skip","flat","shop","drop"]},
    "31": {"name": "Schwa in unstressed syllables", "words": ["about","sofa","comma","taken","happen","letter","mother","father","water","number","paper","problem","open","family","away"]},
}


# ── Stage mapping (from lesson-catalog.csv) ──

RULE_STAGE: dict[str, int] = {
    "11": 1,
    "26": 2, "3": 2, "9": 2, "20": 2, "4": 2, "28": 2, "30": 2,
    "12": 3, "1": 3, "2": 3, "25": 3, "27": 3, "5": 3, "6": 3,
    "7": 3, "8": 3, "10": 3, "31": 3,
    "13": 4, "14": 4, "15": 4, "16": 4, "17": 4, "18": 4, "23": 4,
    "24": 4, "19": 4, "21": 4, "22": 4, "29": 4,
}


# ── Aggregations ──

def all_rules() -> dict[str, dict]:
    """Return the full rule catalog."""
    return dict(RULES)


def rules_for_words(words: list[str]) -> list[str]:
    """Return rule numbers whose example words overlap with the given words.

    Used to detect which rules a story text is demonstrating (for the
    Spelling Aid sidebar in decodable readers, issue #22).
    """
    text_words = {w.lower().strip(".,!?;:") for w in words}
    matches = []
    for num, data in RULES.items():
        if any(w in text_words for w in data["words"]):
            matches.append(num)
    return matches


def words_using_phonogram(pg: str, words: list[str]) -> list[str]:
    """Return the subset of given words that contain the phonogram pg.

    Used to show example words in Spelling Aid sidebars (issue #20).
    """
    matches = []
    for w in words:
        wl = w.lower().strip(".,!?;:")
        if pg in wl:
            matches.append(wl)
    return matches[:3]  # Limit to 3 examples for compact display
