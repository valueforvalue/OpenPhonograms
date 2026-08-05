#!/usr/bin/env python3
"""Inject generated game data into games/phonogram-trainer.html.

Reads scripts/_game_data.json and substitutes two placeholders in the
game HTML:
  // __PHONOGRAM_DATA_BEGIN__ ... __PHONOGRAM_DATA_END__
  // __SPELL_WORDS_BEGIN__ ... __SPELL_WORDS_END__

Run after scripts/generate-game-data.py:
  python scripts/generate-game-data.py
  python scripts/inject-game-data.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME_HTML = ROOT / "games" / "phonogram-trainer.html"
DATA_JSON = ROOT / "scripts" / "_game_data.json"

# Marker blocks in the HTML that this script replaces
PHONOGRAM_BEGIN = "// __PHONOGRAM_DATA_BEGIN__"
PHONOGRAM_END = "// __PHONOGRAM_DATA_END__"
SPELL_BEGIN = "// __SPELL_WORDS_BEGIN__"
SPELL_END = "// __SPELL_WORDS_END__"


def main():
    if not DATA_JSON.exists():
        print("Error: scripts/_game_data.json missing. Run generate-game-data.py first.")
        sys.exit(1)
    if not GAME_HTML.exists():
        print(f"Error: {GAME_HTML} not found")
        sys.exit(1)

    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    html = GAME_HTML.read_text(encoding="utf-8")

    # Build the new PHONOGRAMS array
    pg_lines = ["const PHONOGRAMS = ["]
    for tile in data["phonogram_tiles"]:
        # Use double-quoted JSON, escape single quotes
        sounds = tile["sounds"].replace("'", "\\'")
        speak = f"{tile['pg']}, example word"
        pg_lines.append(
            f"  {{pg:\"{tile['pg']}\",sounds:\"{sounds}\","
            f"speak:\"{speak}\",stage:{tile['stage']},type:\"multi\"}},"
        )
    pg_lines.append("];")
    new_phonograms = "\n".join(pg_lines)

    # Build the new SPELL_WORDS array
    sw_lines = ["const SPELL_WORDS = ["]
    for w in data["spell_words"]:
        sentence = w["sentence"].replace('"', '\\"')
        sw_lines.append(
            f"  {{word:\"{w['word']}\", sentence:\"{sentence}\", stage:{w['stage']}}},"
        )
    sw_lines.append("];")
    new_spell_words = "\n".join(sw_lines)

    # Substitute placeholders
    def replace_block(content, begin, end, new_text):
        b_idx = content.find(begin)
        if b_idx < 0:
            return content, f"begin marker not found: {begin}"
        e_idx = content.find(end, b_idx)
        if e_idx < 0:
            return content, f"end marker not found: {end}"
        return (
            content[:b_idx + len(begin)] + "\n" + new_text + "\n" + content[e_idx:],
            None,
        )

    html, err = replace_block(html, PHONOGRAM_BEGIN, PHONOGRAM_END, new_phonograms)
    if err:
        print(f"Error: {err}")
        print(f"  (Add the marker pair {PHONOGRAM_BEGIN!r} / {PHONOGRAM_END!r} "
              f"around the PHONOGRAMS array literal in the HTML.)")
        sys.exit(1)

    html, err = replace_block(html, SPELL_BEGIN, SPELL_END, new_spell_words)
    if err:
        print(f"Error: {err}")
        print(f"  (Add the marker pair {SPELL_BEGIN!r} / {SPELL_END!r} "
              f"around the SPELL_WORDS array literal in the HTML.)")
        sys.exit(1)

    GAME_HTML.write_text(html, encoding="utf-8")
    n_pg = len(data["phonogram_tiles"])
    n_sw = len(data["spell_words"])
    print(f"  OK  {GAME_HTML.relative_to(ROOT)}")
    print(f"      Injected {n_pg} phonograms + {n_sw} spell words")


if __name__ == "__main__":
    main()