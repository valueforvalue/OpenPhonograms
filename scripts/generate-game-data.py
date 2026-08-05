#!/usr/bin/env python3
"""Generate the phonogram data + spell words for games/phonogram-trainer.html.

The game must be self-contained (offline HTML), so we embed the data
directly in the HTML via placeholder substitution. This script:
  1. Loads phonograms from framework/phonograms.py
  2. Builds SPELL_WORDS by combining per-PG word lists (a, b, c → "cat", "bat", ...)
  3. Builds PHONOGRAM_TILES for the Word Builder mode (each PG + its sounds)
  4. Writes a JSON block to scripts/_game_data.json for substitution

The HTML uses markers `/*__PHONOGRAM_DATA__*/` and `/*__SPELL_WORDS__*/`
that are replaced by sed-like substitution in a follow-up step, or by
running `python scripts/render-references.py` style substitution.

Run:
  python scripts/generate-game-data.py
  python scripts/inject-game-data.py    # updates games/phonogram-trainer.html
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "framework"))
import phonograms  # noqa: E402


# Common "easy sentences" used in Spell mode (one per word)
_SENTENCES = {
    "cat": "The cat sat on the mat.",
    "dog": "The dog runs in the park.",
    "sun": "The sun is hot.",
    "bed": "I sleep in my bed.",
    "hop": "The bunny can hop.",
    "big": "A big red ball.",
    "red": "The apple is red.",
    "pig": "The pig is pink.",
    "ship": "I see a ship on the sea.",
    "fish": "The fish swims fast.",
    "back": "Come back here.",
    "duck": "The duck quacks loud.",
    "tree": "The tree is tall.",
    "green": "The grass is green.",
    "see": "I can see the sun.",
    "sleep": "I sleep in bed.",
    "rain": "I love the rain.",
    "play": "The kids play outside.",
    "day": "It is a sunny day.",
    "stay": "Please stay right here.",
    "boat": "We ride in a boat.",
    "road": "The road is long.",
    "goat": "The goat eats grass.",
    "cake": "I bake a cake.",
    "make": "I can make a cake.",
    "time": "It is story time.",
    "ride": "I can ride a bike.",
    "bridge": "We cross the bridge.",
    "edge": "Stand back from the edge.",
    "match": "Strike a match to make fire.",
    "know": "I know the way.",
    "write": "I write with a pen.",
    "wrong": "That is the wrong way.",
    "through": "We walk through the park.",
    "thought": "I thought it was fun.",
    "new": "I see a new friend.",
    "few": "I have a few toys.",
    "nation": "We are one nation.",
    "special": "You are special.",
    "mission": "I have a mission today.",
    "vision": "I have a vision of the future.",
    "action": "Time for action.",
    "precious": "This is a precious gift.",
    "fraction": "One half is a fraction.",
    "schedule": "I have a busy schedule.",
    "machine": "The machine is loud.",
    "phone": "I talk on the phone.",
    "elephant": "The elephant is big.",
    "alphabet": "I learn the alphabet.",
    "ghost": "The ghost is white.",
    "light": "The light is bright.",
    "night": "The night is dark.",
    "high": "The bird flies high.",
    "sight": "I see a beautiful sight.",
    "tough": "This bread is tough.",
    "enough": "I have enough toys.",
    "caught": "The cat caught a mouse.",
    "taught": "Mom taught me a song.",
    "shoes": "I wear shoes on my feet.",
    "village": "I live in a small village.",
    "monkey": "The monkey climbs trees.",
    "happy": "I am happy today.",
    "funny": "That joke is funny.",
    "family": "I love my family.",
    "city": "I live in the city.",
    "lion": "The lion is strong.",
    "turtle": "The turtle is slow.",
    "rabbit": "The rabbit hops fast.",
    "horse": "The horse runs fast.",
    "eagle": "The eagle flies high.",
    "snake": "The snake is long.",
    "tiger": "The tiger is fierce.",
    "whale": "The whale is huge.",
    "mouse": "The mouse is small.",
    "goose": "The goose has a long neck.",
    "hen": "The hen sits on eggs.",
    "fox": "The fox is clever.",
    "frog": "The frog jumps high.",
    "owl": "The owl hoots at night.",
    "bear": "The bear is big.",
    "deer": "The deer runs in the woods.",
    "wolf": "The wolf howls at night.",
    "blue": "The sky is blue.",
    "true": "That is a true story.",
    "new": "I have a new book.",
    "few": "I have a few apples.",
    "cry": "The baby starts to cry.",
    "fly": "The bird can fly.",
    "try": "I will try my best.",
    "sky": "The sky is blue.",
    "by": "Stand by the door.",
    "baby": "The baby is sleeping.",
    "happy": "I am so happy.",
    "many": "I have many books.",
    "find": "I find my shoe.",
    "kind": "She is kind and nice.",
    "old": "The house is old.",
    "cold": "The ice is cold.",
    "told": "Mom told me a story.",
    "most": "Most kids like ice cream.",
    "wash": "I wash my hands.",
    "sauce": "I like tomato sauce.",
    "pause": "I pause to think.",
    "August": "August is a hot month.",
    "Paul": "Paul is my friend.",
    "law": "The law is fair.",
    "raw": "The meat is raw.",
    "saw": "I saw a bird.",
    "dawn": "We wake at dawn.",
    "yawn": "I yawn when I am tired.",
    "lawn": "The lawn is green.",
    "voice": "I hear a voice.",
    "coin": "I drop a coin.",
    "join": "Come join the game.",
    "boil": "I boil the water.",
    "point": "I point to the sky.",
    "toy": "I have a toy.",
    "boy": "The boy runs fast.",
    "joy": "I feel joy in my heart.",
    "noon": "We eat lunch at noon.",
    "moon": "The moon is bright.",
    "soon": "It will be soon.",
    "room": "I sleep in my room.",
    "book": "I read a book.",
    "look": "I look at the sky.",
    "took": "I took the book.",
    "good": "That is a good idea.",
    "foot": "I have one foot.",
    "food": "The food is hot.",
    "moon": "The moon glows at night.",
    "mood": "I am in a good mood.",
    "school": "I go to school.",
    "pool": "We swim in the pool.",
    "tool": "I need a tool.",
    "cool": "The water is cool.",
    "zoo": "We go to the zoo.",
    "zoo": "I see animals at the zoo.",
}


def build_spell_words():
    """Return list of {word, sentence, stage} dicts sourced from phonogram word lists."""
    seen = set()
    out = []
    for pg, data in phonograms.all_phonograms().items():
        stage = phonograms.PG_STAGE[pg]
        for word in data["words"]:
            w = word.lower()
            if w in seen:
                continue
            seen.add(w)
            sentence = _SENTENCES.get(w, f"The {w} is here.")
            out.append({"word": w, "sentence": sentence, "stage": stage})
    # Sort by stage then alpha
    out.sort(key=lambda w: (w["stage"], w["word"]))
    return out


def build_phonogram_tiles():
    """Return list of {pg, sounds, stage} for the Word Builder mode."""
    return [
        {"pg": pg, "sounds": data["sounds"], "stage": phonograms.PG_STAGE[pg]}
        for pg, data in phonograms.all_phonograms().items()
    ]


def main():
    spell_words = build_spell_words()
    pg_tiles = build_phonogram_tiles()
    out = {
        "spell_words": spell_words,
        "phonogram_tiles": pg_tiles,
    }
    out_path = ROOT / "scripts" / "_game_data.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"  OK  {out_path.relative_to(ROOT)}")
    print(f"      {len(spell_words)} spell words ({sum(1 for w in spell_words if w['stage']==1)} Stage 1, {sum(1 for w in spell_words if w['stage']==2)} Stage 2, {sum(1 for w in spell_words if w['stage']==3)} Stage 3, {sum(1 for w in spell_words if w['stage']==4)} Stage 4)")
    print(f"      {len(pg_tiles)} phonogram tiles")


if __name__ == "__main__":
    main()