# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate interim quick-check HTMLs for each stage.

Quick-checks are informal printable diagnostic pages teachers can use between
lessons to catch problems early. 3 per stage (early/mid/late), ~10 questions
each, content drawn from PGs/rules taught by that checkpoint.

Output: reference/quick-check-stage-{N}-{early|mid|late}.html
        (one combined page per stage at reference/quick-check-stage-{N}.html)

Run once. Idempotent — overwrites existing files.

Usage:
  python scripts/generate-quick-checks.py
"""

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
import csv

CATALOG = ROOT / "framework" / "lesson-catalog.csv"
REF_DIR = ROOT / "reference"


def load_catalog() -> list[dict]:
    with open(CATALOG, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Stage-level data: phonograms introduced, rules introduced
# Hand-curated from TEACHER-GUIDE per-stage overview.
STAGE_DATA = {
    1: {
        "name": "Pre-K (4-5): Phonemic awareness + first 26 phonograms",
        "checkpoints": {
            "early": {"after_lesson": 16, "title": "Quick Check 1 — Phonograms a-s",
                      "pgs": ["a", "d", "g", "c", "o", "qu", "s"],
                      "skills": ["phonogram flash (all sounds)", "blend CVC (3 phonograms)", "identify first sound"]},
            "mid": {"after_lesson": 30, "title": "Quick Check 2 — Phonograms a-m",
                     "pgs": ["a", "d", "g", "c", "o", "qu", "s", "t", "i", "p", "u", "j", "r", "n", "m"],
                     "skills": ["phonogram flash (all sounds)", "blend CVC", "segment CVC", "identify middle sound"]},
            "late": {"after_lesson": 43, "title": "Quick Check 3 — All 26 phonograms",
                     "pgs": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "qu", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
                     "skills": ["phonogram flash (all sounds, 2 sec)", "blend any CVC", "segment any CVC", "identify any sound position"]},
        },
    },
    2: {
        "name": "K (5-6): CVC words + multi-letter phonograms",
        "checkpoints": {
            "early": {"after_lesson": 14, "title": "Quick Check 1 — sh, th, ck",
                      "pgs": ["sh", "th", "ck", "ee"],
                      "rules": ["26"],
                      "skills": ["phonogram flash", "read CVC + sh words", "spell sh/th/ck words"]},
            "mid": {"after_lesson": 30, "title": "Quick Check 2 — First 10 multi-letter PGs",
                     "pgs": ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy"],
                     "rules": ["26", "3", "9"],
                     "skills": ["phonogram flash (all 36)", "spell with multi-letter PGs", "apply Rule 3 (no I/U/V/J)"]},
            "late": {"after_lesson": 50, "title": "Quick Check 3 — All multi-letter PGs",
                     "pgs": ["sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy", "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh", "aw", "au", "ir", "ur", "oa", "ear"],
                     "rules": ["26", "3", "9", "4", "20", "28", "30"],
                     "skills": ["phonogram flash (all 51)", "spell CVC/CCVC/CVCC", "apply all 6 rules"]},
        },
    },
    3: {
        "name": "Gr 1 (6-7): Silent E + vowel teams",
        "checkpoints": {
            "early": {"after_lesson": 16, "title": "Quick Check 1 — Silent E reasons 1-4",
                      "rules": ["12.1", "12.2", "12.3", "12.4"],
                      "skills": ["name each Silent E reason", "spell silent E words"]},
            "mid": {"after_lesson": 36, "title": "Quick Check 2 — Silent E + vowel teams",
                     "rules": ["12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.7", "12.8", "12.9", "1", "2"],
                     "skills": ["name all 9 Silent E reasons", "soften C/G (Rules 1-2)", "spell dge/tch/kn words"]},
            "late": {"after_lesson": 50, "title": "Quick Check 3 — All Stage 3",
                     "pgs": ["dge", "tch", "kn", "gn", "wr", "eigh", "ei", "ey", "ph", "gh", "ough", "augh", "ew", "ui", "eu", "wor", "ie"],
                     "rules": ["12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.7", "12.8", "12.9", "1", "2", "5", "6", "7", "8", "10"],
                     "skills": ["phonogram flash (all 68)", "apply all 9 Silent E reasons", "syllable division"]},
        },
    },
    4: {
        "name": "Gr 2 (7-8): Schwa, suffixing, Latin /sh/",
        "checkpoints": {
            "early": {"after_lesson": 12, "title": "Quick Check 1 — Schwa + Drop E",
                      "rules": ["31", "13"],
                      "skills": ["identify schwa", "say-to-spell", "drop silent E for suffix"]},
            "mid": {"after_lesson": 28, "title": "Quick Check 2 — Suffixing + Latin /sh/",
                     "pgs": ["ti", "ci", "si"],
                     "rules": ["13", "14", "15", "16", "17", "18"],
                     "skills": ["apply suffixing rules", "spell ti/ci/si words", "Rules 17-18 (Latin /sh/)"]},
            "late": {"after_lesson": 44, "title": "Quick Check 3 — All Stage 4",
                     "pgs": ["ti", "ci", "si"],
                     "rules": ["13", "14", "15", "16", "17", "18", "23", "24", "19", "20", "21", "22", "29"],
                     "skills": ["apply all suffixing rules", "morphology (prefixes/suffixes)", "Latin /sh/", "all Stage 4 rules"]},
        },
    },
    5: {
        "name": "Gr 3+ (8+): Roots, fluency, composition",
        "checkpoints": {
            "early": {"after_lesson": 14, "title": "Quick Check 1 — Latin roots",
                      "skills": ["define Latin roots taught so far", "spell words with root"]},
            "mid": {"after_lesson": 26, "title": "Quick Check 2 — Latin + Greek roots",
                     "skills": ["define Latin + Greek roots", "spell words with roots"]},
            "late": {"after_lesson": 38, "title": "Quick Check 3 — All Stage 5",
                     "skills": ["define all 25 roots", "fluency (WPM)", "write paragraph using roots"]},
        },
    },
}


def render_quick_check(stage: int, slot: str, data: dict, stage_data: dict) -> str:
    """Generate HTML for a single quick-check page."""
    title = data["title"]
    pgs = data.get("pgs", [])
    rules = data.get("rules", [])
    skills = data["skills"]
    after_lesson = data["after_lesson"]

    pgs_html = ", ".join(pgs) if pgs else "All phonograms taught so far in this stage"
    rules_html = ", ".join(rules) if rules else "All rules introduced so far"

    skills_html = "\n".join(f"<li>{s}</li>" for s in skills)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — Stage {stage}</title>
<style>
@page {{ size: letter; margin: 0.5in; }}
body {{ font-family: Georgia, "Times New Roman", serif; font-size: 12pt; line-height: 1.5; color: #222; max-width: 7.5in; margin: 0 auto; }}
h1 {{ font-size: 20pt; margin: 0 0 0.2em 0; color: #2a5c8a; border-bottom: 2px solid #2a5c8a; padding-bottom: 0.2em; }}
h2 {{ font-size: 14pt; color: #2a5c8a; margin-top: 1.2em; }}
.meta {{ color: #555; font-size: 10pt; margin-bottom: 1.5em; }}
table {{ border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 11pt; }}
th, td {{ border-bottom: 1px solid #ccc; padding: 5pt 8pt; text-align: left; }}
th {{ background: #f0f4f8; font-weight: bold; }}
.checkbox {{ display: inline-block; width: 14px; height: 14px; border: 1px solid #888; }}
.section {{ page-break-inside: avoid; margin-bottom: 1.5em; }}
.instructions {{ background: #f8f4e8; padding: 0.6em 1em; border-left: 3px solid #c8a832; margin: 0.8em 0; font-style: italic; }}
.footer {{ font-size: 9pt; color: #777; margin-top: 2em; padding-top: 1em; border-top: 1px solid #ddd; }}
</style>
</head>
<body>

<h1>{title}</h1>
<div class="meta">
<strong>Stage {stage}</strong> · {stage_data['name']}<br>
Use after <strong>Lesson {after_lesson}</strong> · Informal diagnostic · ~10 minutes
</div>

<h2>What This Checks</h2>
<ul>{skills_html}</ul>

<h2>Scope</h2>
<p><strong>Phonograms covered:</strong> {pgs_html}</p>
<p><strong>Rules covered:</strong> {rules_html}</p>

<div class="instructions">
<strong>How to use:</strong> Work through each section with the child. Do not time strictly — this is informal. Mark any item the child hesitates on. If 2+ items in one section are weak, return to the lessons listed in the comments below.
</div>

<h2>Part 1: Phonogram Flash</h2>
<div class="section">
<table>
<tr><th>Phonogram</th><th>Sounds Expected</th><th>Pass</th><th>Notes</th></tr>
"""

    # Add 8 phonogram flash rows (random sample or first 8)
    sample_pgs = pgs[:8] if len(pgs) >= 8 else pgs
    # Pad with placeholder rows if fewer than 8 PGs
    while len(sample_pgs) < 8 and pgs:
        sample_pgs.append(pgs[len(sample_pgs) % len(pgs)])
    if not sample_pgs:
        sample_pgs = ["(all PGs)"] * 8

    for pg in sample_pgs[:8]:
        html += f'<tr><td><strong>{pg}</strong></td><td>all sounds</td><td><span class="checkbox"></span></td><td></td></tr>\n'

    html += """</table>
<p><em>Pass = child says ALL sounds within 2 seconds, no hesitation.</em></p>
</div>

<h2>Part 2: Decoding</h2>
<div class="section">
<table>
<tr><th>Word</th><th>Phonograms</th><th>Pass</th></tr>
"""

    # Generate 5 sample words (placeholder — teacher adapts)
    sample_words = {
        1: ["cat", "dog", "sun", "bed", "hop"],
        2: ["ship", "fish", "back", "park", "ring"],
        3: ["make", "have", "race", "cage", "knight"],
        4: ["nation", "action", "running", "happily", "unfair"],
        5: ["dictate", "transport", "inspect", "photograph", "biology"],
    }.get(stage, ["word1", "word2", "word3", "word4", "word5"])

    for w in sample_words:
        html += f'<tr><td>{w}</td><td>(analyze)</td><td><span class="checkbox"></span></td></tr>\n'

    html += """</table>
<p><em>Pass = child reads the word sound-by-sound and blends correctly.</em></p>
</div>

<h2>Part 3: Spelling (Dictation)</h2>
<div class="section">
<table>
<tr><th>Word</th><th>Child's Writing</th><th>Pass</th></tr>
"""

    for w in sample_words[:5]:
        html += f'<tr><td>{w}</td><td>&nbsp;</td><td><span class="checkbox"></span></td></tr>\n'

    html += """</table>
<p><em>Pass = child segments, writes, and reads back correctly.</em></p>
</div>

<h2>Part 4: Application</h2>
<div class="section">
"""

    if rules:
        html += "<p><strong>Apply the rule:</strong></p>\n<ol>"
        for rule in rules[:3]:
            html += f"<li>Write a word that follows Rule {rule}: ______________</li>\n"
        html += "</ol>\n"
    else:
        html += "<p><strong>Read aloud:</strong> Read the previous 2 decodable readers. Note any hesitations.</p>\n"

    html += "</div>\n\n"
    html += "<h2>Results Summary</h2>\n"
    html += "<table>\n"
    html += "<tr><th>Section</th><th>Score</th><th>Action if Weak</th></tr>\n"
    html += "<tr><td>Phonogram Flash</td><td>__/8</td><td>5-min daily flash drill on missed PGs</td></tr>\n"
    html += "<tr><td>Decoding</td><td>__/5</td><td>Return to sound-by-sound practice</td></tr>\n"
    html += "<tr><td>Spelling</td><td>__/5</td><td>Re-do Spelling Analysis on missed words</td></tr>\n"
    html += "<tr><td>Application</td><td>__/3</td><td>Re-teach missed rules/roots</td></tr>\n"
    html += "</table>\n\n"
    html += '<div class="footer">\n'
    html += f"Generated by <em>OpenPhonograms</em> · Quick-Check {stage}.{slot.capitalize()} · Use freely across students\n"
    html += "</div>\n\n"
    html += "</body>\n</html>\n"
    return html


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate quick-check HTMLs + PDFs")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering")
    args = parser.parse_args()

    print("==> Generating quick-check HTMLs")
    n = 0
    for stage, stage_data in STAGE_DATA.items():
        for slot, cp_data in stage_data["checkpoints"].items():
            html = render_quick_check(stage, slot, cp_data, stage_data)
            out = REF_DIR / f"quick-check-stage-{stage}-{slot}.html"
            out.write_text(html, encoding="utf-8")
            print(f"  OK  {out.relative_to(ROOT)}")
            n += 1
    print(f"\nDone: {n} quick-check HTMLs written")

    if args.no_render:
        return

    # Render each HTML to PDF, then merge 3 per stage into one combined PDF
    print("\n==> Rendering quick-check PDFs")
    try:
        from weasyprint import HTML as WHTML
        from pypdf import PdfWriter, PdfReader
    except ImportError as e:
        print(f"  SKIP  (missing dep: {e})")
        return

    out_dir = ROOT / "build" / "quick-checks"
    out_dir.mkdir(parents=True, exist_ok=True)
    for stage in range(1, 6):
        html_files = [REF_DIR / f"quick-check-stage-{stage}-{slot}.html" for slot in ["early", "mid", "late"]]
        pdf_files = []
        for hf in html_files:
            pdf_path = out_dir / (hf.stem + ".pdf")
            WHTML(filename=str(hf)).write_pdf(str(pdf_path))
            pdf_files.append(pdf_path)
        writer = PdfWriter()
        for pf in pdf_files:
            writer.append_pages_from_reader(PdfReader(str(pf)))
        combined = out_dir / f"quick-check-stage-{stage}.pdf"
        with open(combined, "wb") as f:
            writer.write(f)
        print(f"  OK  {combined.relative_to(ROOT)}  ({len(pdf_files)} pages merged)")


if __name__ == "__main__":
    main()
