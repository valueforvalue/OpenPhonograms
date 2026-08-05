"""Single source of truth for phonogram data.

This module owns the canonical phonogram catalog: 26 single-letter PGs
(taught in Stage 1), 26 multi-letter PGs (Stage 2), and 20 advanced
multi-letter PGs (Stage 3+). Each entry carries:
  - sounds:   IPA notation, primary sound first
  - words:    15-20 decodable example words

Stage-to-PG mapping (which stage each phonogram is taught in) lives in
PG_STAGE. Rules 1-31 live in rules.py (separate file).

Consumers:
  - scripts/generate-worksheets.py  (single + multi + multi3 worksheets)
  - scripts/generate-stage3.py      (Stage 3 lesson content)
  - games/phonogram-trainer.html    (future: import via JSON dump)
  - framework/render.py             (when iterating phonogram colors)

To regenerate: this file is hand-edited by content team. The validate
script (scripts/check-worksheet-coverage.py) verifies phonograms declared
in the lesson catalog match entries here.
"""

# ── Single-letter phonograms (26 total, taught in Stage 1) ──

SINGLE: dict[str, dict] = {
    "a": {"sounds": "/ă/ /ā/ /ä/", "words": ["at","cat","hat","bat","rat","sat","mat","fat","pat","cap","map","nap","tap","lap","gap","bag","tag","rag","wag","had"]},
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

# ── Multi-letter phonograms taught in Stage 2 (26 total) ──

MULTI: dict[str, dict] = {
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

# ── Advanced multi-letter phonograms taught in Stage 3+ (17 total) ──

MULTI3: dict[str, dict] = {
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

# ── Latin /sh/ spellings (3 PGs, taught in Stage 4) ──

MULTI4: dict[str, dict] = {
    "ti": {"sounds": "/sh/", "words": ["nation","station","action","motion","fraction","patient","partial","initial","essential","subtle","gracious","fictional","national","vibration","migration","rotation","creation","operation","celebration"]},
    "ci": {"sounds": "/sh/", "words": ["special","social","official","musician","electric","politician","racial","crucial","precious","delicious","malicious","artificial","conscious","fancied","glacier","spacious","vicious","audacious","vivacious","efficient"]},
    "si": {"sounds": "/sh/", "words": ["session","mission","vision","passion","version","tension","extension","dimension","explosion","confusion","division","decision","collision","occasion","emulsion","mansion","pension","suspension","comprehension","apprehension"]},
}


# ── Stage mapping (single source of truth for PG → stage) ──

PG_STAGE: dict[str, int] = {
    **{k: 1 for k in SINGLE.keys()},                 # 27 single-letter PGs (a-z + qu)
    **{k: 2 for k in MULTI.keys()},                  # 26 multi-letter Stage 2 PGs
    **{k: 3 for k in MULTI3.keys()},                 # 17 advanced Stage 3 PGs
    **{k: 4 for k in MULTI4.keys()},                 # 3 Latin /sh/ Stage 4 PGs
}


# ── Aggregations ──

def all_phonograms() -> dict[str, dict]:
    """Return the full phonogram catalog (SINGLE + MULTI + MULTI3 + MULTI4)."""
    return {**SINGLE, **MULTI, **MULTI3, **MULTI4}


def all_stages() -> dict[int, list[str]]:
    """Return stage → list of phonograms taught in that stage."""
    out: dict[int, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}
    for pg, stage in PG_STAGE.items():
        out[stage].append(pg)
    return out


def to_json_compatible() -> dict:
    """Dump catalog as JSON-compatible dict for the web game (future).

    Returns {pg: {"sounds": str, "words": list[str], "stage": int}}.
    """
    return {
        pg: {"sounds": data["sounds"], "words": data["words"], "stage": PG_STAGE[pg]}
        for pg, data in all_phonograms().items()
    }