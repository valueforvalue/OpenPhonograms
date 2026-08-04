#!/usr/bin/env python3
"""Build release.zip — all PDFs + game + audio, organized by stage and type."""
import zipfile, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

GROUPS = {
    "01-phonemic-awareness": ["pa-"],
    "02-phonograms": ["pg-"],
    "03-word-building": ["vc-", "cvc-", "ccvc", "cvcc", "open-syllables", "short-", "long-vowels", "vowels-"],
    "05-spelling-analysis": ["spell-"],
    "06-rules": ["rule-", "silent-e-"],
    "07-syllable-division": ["syllables-"],
    "08-high-frequency-words": ["hf-words-", "vocab-"],
    "09-readers": ["reader-"],
    "10-reviews": ["review-", "silent-letter-review", "all-roots-review", "rule-review", "latin-review", "greek-review", "morph-review", "suffixing-review"],
    "11-handwriting": ["handwriting-"],
    "12-fluency": ["fluency-"],
    "13-composition": ["composition-"],
    "14-grammar": ["grammar-"],
    "15-roots-morphology": ["root-", "prefix-", "suffix-", "latin-sh", "schwa-", "irregular-"],
    "16-assessments": ["assessment-"],
}

def group_of(filename: str) -> str:
    base = Path(filename).stem
    for group, prefixes in GROUPS.items():
        for p in prefixes:
            if base.startswith(p):
                return group
    return "99-other"

def main():
    out = ROOT / "release.zip"
    zf = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)

    # 1. PDFs from build/
    if not BUILD.exists():
        print("Run: python framework/render.py --all  (generates build/)")
        return
    for pdf in sorted(BUILD.rglob("*.pdf")):
        parent = pdf.parent.name
        if parent == "build":
            zf.write(pdf, f"pdfs/{pdf.name}")
        elif parent == "readers":
            zf.write(pdf, f"pdfs/readers/{pdf.name}")
        elif "worksheets" in str(pdf):
            rel = pdf.relative_to(BUILD / "worksheets")
            zf.write(pdf, f"pdfs/worksheets/{rel}")
        else:
            grp = group_of(pdf.name)
            zf.write(pdf, f"pdfs/{parent}/{grp}/{pdf.name}")

    # 2. Game + audio
    game_html = ROOT / "games" / "phonogram-trainer.html"
    audio_dir = ROOT / "games" / "audio"
    if game_html.exists():
        zf.write(game_html, "game/phonogram-trainer.html")
    if audio_dir.exists():
        for mp3 in sorted(audio_dir.glob("*.mp3")):
            zf.write(mp3, f"game/audio/{mp3.name}")

    zf.close()
    size = os.path.getsize(out) / (1024 * 1024)
    uncat = sum(1 for n in zf.namelist() if "99-other" in n)
    print(f"{out.name}: {size:.1f} MB, {len(zf.namelist())} files")
    if uncat:
        print(f"  ⚠ {uncat} uncategorized files (99-other)")

if __name__ == "__main__":
    main()
