# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate a placement test HTML for new students.

Teacher reads items aloud, child responds. JavaScript scores each section and
recommends a starting stage.

Output: reference/placement-test.html
        build/quick-checks/placement-test.pdf

Run once. Idempotent.

Usage:
  python scripts/generate-placement-test.py
  python scripts/generate-placement-test.py --no-render
"""

import io
import os
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from framework.render import render_html_to_pdf

REF_DIR = ROOT / "reference"
OUT_DIR = ROOT / "build" / "quick-checks"


# Test items per section. Each section has 6 items + 1 demo (not scored).
# Items are oral — teacher reads aloud, child responds orally.
SECTIONS = [
    {
        "id": "phonemic-awareness",
        "title": "Section 1: Phonemic Awareness",
        "stage_if_pass": "Stage 1 Lesson 9+",
        "diagnosis": "Tests whether the child can hear, blend, and segment sounds in spoken words — the foundation of all reading. No letters involved; purely oral.",
        "remediation": "If fewer than 5/6 items pass: start at Stage 1 Lesson 1 (Sounds Around Us). Child needs explicit phonemic-awareness work before letter-sound instruction.",
        "items": [
            ("blend", "cat", "/k/ /ă/ /t/", "Word: cat. Blend: k-ă-t. Now YOU blend: 'sun'."),
            ("blend", "big", "/b/ /ĭ/ /g/", "Word: big. Blend: b-ĭ-g. Now YOU blend: 'red'."),
            ("blend", "shop", "/sh/ /ŏ/ /p/", "Word: shop. Blend: sh-ŏ-p. Now YOU blend: 'jump'."),
            ("segment", "fish", "/f/ /ĭ/ /sh/", "Word: fish. Segment: f-ĭ-sh. Now YOU segment: 'lamp'."),
            ("segment", "stop", "/s/ /t/ /ŏ/ /p/", "Word: stop. Segment: s-t-ŏ-p. Now YOU segment: 'hand'."),
            ("identify_first", "jump", "/j/", "Word: jump. First sound: /j/. Now YOU try: 'kick'. First sound?"),
        ],
    },
    {
        "id": "phonograms-single",
        "title": "Section 2: Single-Letter Phonograms",
        "stage_if_pass": "Stage 2 Lesson 1+",
        "diagnosis": "Tests single-letter phonogram knowledge (a-z). Can the child recall all sounds for each letter on flash? Can they read simple CVC words?",
        "remediation": "If phonogram flash items fail: revisit Stage 1 Lessons 9-43. If CVC reading fails: revisit Stage 1 Lessons 6-8 (blending) and 44-45 (consonant blends).",
        "items": [
            ("pg_flash", "a", "3 sounds", "Flash 'a'. Child says all sounds."),
            ("pg_flash", "g", "2 sounds", "Flash 'g'. Child says all sounds."),
            ("pg_flash", "i", "3 sounds", "Flash 'i'. Child says all sounds."),
            ("read_cvc", "hat", "h-ă-t", "Read this word: hat. Sound it out."),
            ("read_cvc", "dog", "d-ŏ-g", "Read this word: dog. Sound it out."),
            ("read_cvc", "fun", "f-ŭ-n", "Read this word: fun. Sound it out."),
        ],
    },
    {
        "id": "phonograms-multi",
        "title": "Section 3: Multi-Letter Phonograms",
        "stage_if_pass": "Stage 3 Lesson 1+",
        "diagnosis": "Multi-letter phonograms (sh, th, ck, ee, ng, etc.) are introduced in Stage 2. This section checks whether the child has automatic recall.",
        "remediation": "If multi-letter PG flash fails: revisit Stage 2 Lessons 10-21 (multi-letter PG intros). If word reading fails: revisit Stage 2 Lessons 22-30 (review + practice).",
        "items": [
            ("pg_flash", "sh", "1 sound", "Flash 'sh'. Child says sound."),
            ("pg_flash", "th", "2 sounds", "Flash 'th'. Child says BOTH sounds."),
            ("pg_flash", "ck", "1 sound", "Flash 'ck'. Child says sound."),
            ("read", "ship", "sh-ĭ-p", "Read this word: ship."),
            ("read", "back", "b-ă-ck", "Read this word: back."),
            ("read", "think", "th-ĭ-nk", "Read this word: think."),
        ],
    },
    {
        "id": "silent-e-and-advanced",
        "title": "Section 4: Silent E & Advanced",
        "stage_if_pass": "Stage 4+",
        "diagnosis": "Tests advanced decoding: silent E reasoning, complex multi-letter PGs (ti = /sh/), and say-to-spell strategy. Requires fluent PG knowledge.",
        "remediation": "If silent E items fail: revisit Stage 3 Lessons 1-20. If advanced PG items fail: revisit Stage 4 Lessons on Latin /sh/, morphology, suffixing.",
        "items": [
            ("read", "make", "m-ā-k (silent E)", "Read this word: make. Why is the 'a' long? (Silent E)"),
            ("read", "have", "h-ă-v (silent E but short a)", "Read this word: have. Why is the 'a' short? (Rule 12.2: no V/U at end)"),
            ("read", "knight", "kn-ī-t (silent k)", "Read this word: knight. Why is the 'k' silent?"),
            ("spell", "name", "n-ā-m", "Spell this word: name. (Silent E makes 'a' long)"),
            ("read", "nation", "n-ā-sh-ŭ-n (ti = /sh/)", "Read this word: nation. What does 'ti' say?"),
            ("say_to_spell", "about", "ă-bout", "How would you say-to-spell 'about' to hear the vowels?"),
        ],
    },
]


def render_html() -> str:
    """Generate the placement test HTML."""
    sections_html = ""
    for sec_idx, sec in enumerate(SECTIONS):
        items_html = ""
        for i, (kind, word, answer, prompt) in enumerate(sec["items"]):
            qid = f"q{sec_idx}_{i}"
            items_html += f"""
        <div class="item">
          <label class="item-prompt">
            <input type="checkbox" id="{qid}" class="score-box">
            <span class="item-text">{prompt}</span>
          </label>
          <div class="item-meta">
            <strong>Word:</strong> <code>{word}</code> &middot;
            <strong>Expected:</strong> <code>{answer}</code> &middot;
            <strong>Type:</strong> <code>{kind}</code>
          </div>
        </div>"""

        sections_html += f"""
      <section id="{sec['id']}" class="section">
        <h2>{sec['title']}</h2>
        <p class="section-info">
          <strong>Passing all 6 items here means child is ready for: {sec['stage_if_pass']}</strong><br>
          {len(sec['items'])} items &middot; No time limit &middot; Read aloud to child
        </p>
        <p class="diagnosis">{sec.get('diagnosis', '')}</p>
        {items_html}
        <div class="section-result" id="result-{sec['id']}"></div>
      </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Placement Test — OpenPhonograms</title>
<style>
@page {{ size: letter; margin: 0.5in; @bottom-left {{ content: "OpenPhonograms · MIT licensed"; font-family: Georgia, serif; font-size: 7pt; color: #aaa; }} }}
body {{ font-family: Georgia, "Times New Roman", serif; font-size: 12pt; line-height: 1.5; color: #222; max-width: 7.5in; margin: 0 auto; }}
h1 {{ font-size: 22pt; margin: 0 0 0.2em 0; color: #2a5c8a; border-bottom: 3px solid #2a5c8a; padding-bottom: 0.3em; }}
h2 {{ font-size: 16pt; color: #2a5c8a; margin-top: 1.5em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }}
.meta {{ color: #555; font-size: 10pt; margin-bottom: 1.5em; }}
.section {{ page-break-inside: avoid; margin-bottom: 2em; padding: 0.5em; border: 1px solid #ddd; border-radius: 6px; }}
.diagnosis {{ font-size: 10pt; color: #444; margin: 0.4em 0 0.8em 0; font-style: italic; }}
.section-info {{ background: #f0f4f8; padding: 0.6em 1em; border-radius: 4px; font-size: 11pt; margin: 0.5em 0; }}
.item {{ margin: 0.6em 0; padding: 0.4em 0.6em; border-left: 3px solid transparent; }}
.item.passed {{ border-left-color: #4a8a3a; }}
.item.failed {{ border-left-color: #c8a832; }}
.item-prompt {{ display: flex; align-items: flex-start; gap: 0.6em; cursor: pointer; }}
.score-box {{ width: 18px; height: 18px; margin-top: 4px; flex-shrink: 0; }}
.item-text {{ flex: 1; }}
.item-meta {{ margin-left: 30px; margin-top: 0.2em; font-size: 10pt; color: #555; }}
.item-meta code {{ background: #f4f0e8; padding: 0 4px; border-radius: 2px; font-family: "Courier New", monospace; }}
.section-result {{ margin-top: 0.8em; padding: 0.6em; background: #f8f4e8; border-radius: 4px; font-size: 11pt; min-height: 1.2em; }}
.section-result.recommend {{ background: #e8f4e8; border: 2px solid #4a8a3a; font-weight: bold; }}
code {{ background: #f4f0e8; padding: 1px 4px; border-radius: 2px; font-family: "Courier New", monospace; }}
.controls {{ margin: 1em 0; padding: 1em; background: #2a5c8a; color: white; border-radius: 6px; text-align: center; }}
button {{ background: white; color: #2a5c8a; border: 0; padding: 8px 16px; font-size: 12pt; font-weight: bold; border-radius: 4px; cursor: pointer; margin: 0 4px; }}
button:hover {{ background: #f0f4f8; }}
.footer {{ font-size: 9pt; color: #777; margin-top: 2em; padding-top: 1em; border-top: 1px solid #ddd; }}
@media print {{ .controls, .section-result, #recommendation {{ display: none; }} }}
</style>
</head>
<body>

<h1>Placement Test</h1>
<div class="meta">
<strong>Purpose:</strong> Determine which stage a new student should begin.<br>
<strong>Time:</strong> 15-20 minutes total (oral; child does not need to read or write).<br>
<strong>Format:</strong> Read items aloud, check each one the child answers correctly. Click "Score All Sections" or print and score by hand.
</div>

<div style="background: #f0f4f8; padding: 0.8em 1em; margin-bottom: 1em; border-radius: 4px; font-size: 11pt;">
<strong>Quick section map:</strong><br>
<strong>Section 1</strong> &mdash; Phonemic awareness (oral blending/segmenting). Pass &rarr; ready for letter-sound work.<br>
<strong>Section 2</strong> &mdash; Single-letter phonograms + CVC reading. Pass &rarr; ready for multi-letter PGs.<br>
<strong>Section 3</strong> &mdash; Multi-letter phonograms (sh, th, ck, ee, etc.). Pass &rarr; ready for silent E + advanced.<br>
<strong>Section 4</strong> &mdash; Silent E + advanced PGs + say-to-spell. Pass &rarr; ready for Stage 4-5.
</div>

<div class="controls">
  <button onclick="scoreAll()">Score All Sections</button>
  <button onclick="resetAll()">Reset</button>
  <button onclick="window.print()">Print</button>
</div>

<div id="recommendation" class="section-result" style="font-size: 14pt; margin-bottom: 1em;"></div>

{sections_html}

<div class="controls">
  <button onclick="scoreAll()">Score All Sections</button>
  <button onclick="resetAll()">Reset</button>
  <button onclick="window.print()">Print</button>
</div>

<div class="footer">
From the <em>OpenPhonograms</em> curriculum (MIT licensed) &middot; Placement test &middot; Score manually or click "Score All Sections"
</div>

<script>
function scoreAll() {{
  const sections = {str([s['id'] for s in SECTIONS]).replace("'", '"')};
  const recommendations = {str([s['stage_if_pass'] for s in SECTIONS]).replace("'", '"')};
  let bestStage = 'Stage 1 Lesson 1-8 (Phonemic Awareness only)';
  let bestIdx = -1;
  let details = [];

  sections.forEach((sid, idx) => {{
    const sec = document.getElementById(sid);
    const boxes = sec.querySelectorAll('.score-box');
    let passed = 0;
    boxes.forEach((b, i) => {{
      const item = b.closest('.item');
      item.classList.remove('passed', 'failed');
      if (b.checked) {{
        item.classList.add('passed');
        passed++;
      }} else {{
        item.classList.add('failed');
      }}
    }});
    const total = boxes.length;
    const pct = (passed / total * 100).toFixed(0);
    const resultEl = document.getElementById('result-' + sid);
    resultEl.classList.remove('recommend');
    if (passed === total) {{
      resultEl.classList.add('recommend');
      resultEl.innerHTML = `<strong>✓ Section passed: ${{passed}}/${{total}} (${{pct}}%)</strong> &mdash; Child is ready for ${{recommendations[idx]}}.`;
      bestIdx = idx;
    }} else {{
      resultEl.innerHTML = `Section score: ${{passed}}/${{total}} (${{pct}}%) &mdash; Needs work. Read the diagnosis above and remediate before moving on.`;
    }}
    details.push(`${{idx + 1}}: ${{passed}}/${{total}}`);
  }});

  const rec = document.getElementById('recommendation');
  if (bestIdx >= 0) {{
    rec.classList.add('recommend');
    rec.innerHTML = `<strong>RECOMMENDATION:</strong> Start at ${{recommendations[bestIdx]}}. (Section ${{bestIdx + 1}} fully passed.)`;
  }} else {{
    rec.innerHTML = `<strong>RECOMMENDATION:</strong> Start at Stage 1 Lesson 1-8 (Phonemic Awareness). (No sections fully passed; review each section's skills first.)`;
  }}
}}

function resetAll() {{
  document.querySelectorAll('.score-box').forEach(b => b.checked = false);
  document.querySelectorAll('.item').forEach(item => item.classList.remove('passed', 'failed'));
  document.querySelectorAll('.section-result').forEach(r => {{ r.classList.remove('recommend'); r.innerHTML = ''; }});
  document.getElementById('recommendation').classList.remove('recommend');
  document.getElementById('recommendation').innerHTML = '';
}}
</script>

</body>
</html>
"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate placement test")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering")
    args = parser.parse_args()

    print("==> Generating placement test HTML")
    html = render_html()
    out = REF_DIR / "placement-test.html"
    out.write_text(html, encoding="utf-8")
    print(f"  OK  {out.relative_to(ROOT)}")

    if args.no_render:
        return

    print("\n==> Rendering placement test PDF")
    try:
        from framework.render import render_html_to_pdf
    except ImportError as e:
        print(f"  SKIP  (missing dep: {e})")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf = OUT_DIR / "placement-test.pdf"
    render_html_to_pdf(open(out, encoding="utf-8").read(), pdf, body_class="index")
    print(f"  OK  {pdf.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
