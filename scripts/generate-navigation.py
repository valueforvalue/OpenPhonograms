"""Generate top-level navigation PDFs for the release ZIP.

Produces (in build/handbook/):
  00-Start-Here.pdf               — orientation for new users
  01-Index-and-Table-of-Contents.pdf — master TOC with hyperlinks
  02-Scope-and-Sequence.pdf        — combined curriculum map
  04-Quick-Reference-Phonograms.pdf
  04-Quick-Reference-Spelling-Rules.pdf
  04-Quick-Reference-Spelling-Analysis.pdf

All have PDF bookmarks for navigation.

Usage:
  python scripts/generate-navigation.py [--no-render]
"""

import argparse
import csv
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "framework" / "lesson-catalog.csv"
OUT_DIR = ROOT / "build" / "handbook"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Common CSS for all navigation PDFs
CSS = """
@page { size: letter; margin: 0.75in; @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 9pt; color: #555; } }
body { font-family: Georgia, "Times New Roman", serif; font-size: 12pt; line-height: 1.6; color: #222; }
h1 { font-size: 26pt; color: #2a5c8a; margin: 0 0 0.3em 0; border-bottom: 3px solid #2a5c8a; padding-bottom: 0.3em; bookmark-level: 1; page-break-before: avoid; }
h2 { font-size: 18pt; color: #2a5c8a; margin-top: 1.5em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; bookmark-level: 2; page-break-after: avoid; }
h3 { font-size: 14pt; color: #2a5c8a; margin-top: 1.2em; bookmark-level: 3; page-break-after: avoid; }
h4 { font-size: 12pt; color: #333; margin-top: 1em; bookmark-level: 4; }
.meta { color: #555; font-size: 10pt; margin-bottom: 1.5em; }
a { color: #2a5c8a; text-decoration: none; border-bottom: 1px dotted #2a5c8a; }
a:hover { background: #f0f4f8; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 11pt; }
th, td { border-bottom: 1px solid #ccc; padding: 5pt 8pt; text-align: left; vertical-align: top; }
th { background: #f0f4f8; font-weight: bold; }
code { background: #f4f0e8; padding: 1px 4px; border-radius: 2px; font-family: "Courier New", monospace; font-size: 11pt; }
ul, ol { margin: 0.5em 0; padding-left: 1.5em; }
li { margin: 0.2em 0; }
.hero { background: linear-gradient(135deg, #2a5c8a 0%, #4a7caa 100%); color: white; padding: 1.5em; border-radius: 8px; margin: 1em 0; }
.hero h1 { color: white; border-bottom: 3px solid white; }
.hero p { color: rgba(255,255,255,0.95); }
.callout { background: #f8f4e8; padding: 0.8em 1em; border-left: 4px solid #c8a832; margin: 1em 0; }
.success { background: #e8f4e8; padding: 0.8em 1em; border-left: 4px solid #4a8a3a; margin: 1em 0; }
.toc-item { display: flex; justify-content: space-between; padding: 0.4em 0; border-bottom: 1px dotted #ccc; }
.toc-item .title { font-weight: bold; }
.toc-item .page { color: #555; font-family: "Courier New", monospace; font-size: 10pt; }
"""


def load_catalog() -> list[dict]:
    with open(CATALOG, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_pdf(html: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    from weasyprint import HTML as WHTML
    WHTML(filename=str(out_path)).write_pdf(str(out_path.with_suffix(".pdf")))


def make_start_here() -> Path:
    """00-Start-Here.pdf — orientation for first-time users."""
    out = OUT_DIR / "00-Start-Here.md"
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<div class="hero">
<h1>Welcome to Uncovering the Logic of English</h1>
<p>An open-source adaptation of Denise Eide's phonogram-and-rules reading curriculum.</p>
</div>

<div class="meta">Edition 1.0 · 248 lessons · 75 phonograms · 31 spelling rules · 5 stages (Pre-K through Grade 3+)</div>

<h2>What is this curriculum?</h2>
<p>A complete, print-first reading curriculum based on <em>Uncovering the Logic of English</em> by Denise Eide. Every lesson, worksheet, and reader is generated from version-controlled data — no DRM, no internet required, no locked PDFs.</p>

<p>The methodology: <strong>spelling drives reading</strong>. Children learn the 75 phonograms (sound-units) and 31 spelling rules that govern 98% of English words. They practice a 5-step <em>Spelling Analysis</em> routine that turns spelling into a decoding tool for reading.</p>

<h2>How to use this release</h2>

<h3>1. Read this PDF (you're doing it)</h3>
<p>You're holding the orientation document. It explains what's in the release and how to navigate.</p>

<h3>2. Skim the Index</h3>
<p>Open <a href="01-Index-and-Table-of-Contents.pdf">01-Index-and-Table-of-Contents.pdf</a>. It's a clickable map of every PDF in this release. Bookmarks at the left of any PDF reader let you jump to sections.</p>

<h3>3. Try the placement test</h3>
<p>Open <a href="09-Quick-Checks/placement-test.pdf">09-Quick-Checks/placement-test.pdf</a>. It's an oral, JS-scored diagnostic that tells you which stage to begin. (Print it; tick boxes as your child responds; the scoring works in any browser.)</p>

<h3>4. Read the Teacher's Guide for your stage</h3>
<p>Each stage folder (<a href="06-Lesson-Packs/stage-1/00-stage-1-cover.pdf">06-Lesson-Packs/stage-1/</a>, etc.) opens with a cover page explaining what's in that stage and a checklist of what to print.</p>

<h3>5. Print the phonogram chart and spelling rules poster</h3>
<p>Print <a href="04-Quick-Reference/04-Quick-Reference-Phonograms.pdf">04-Quick-Reference-Phonograms.pdf</a> for the wall. Print <a href="04-Quick-Reference/04-Quick-Reference-Spelling-Rules.pdf">04-Quick-Reference-Spelling-Rules.pdf</a> as a desk reference.</p>

<h3>6. Open lesson pack #1 and start teaching</h3>
<p>Each lesson PDF is a self-contained unit: cover page with prep checklist → teacher script → worksheet → flash cards for review. Print one pack at a time.</p>

<div class="callout">
<strong>Tip:</strong> The phonogram trainer web game (<a href="11-Game/phonogram-trainer.html">11-Game/phonogram-trainer.html</a>) is a great reward activity and a way for kids to practice independently. It works offline.
</div>

<h2>What's in this release</h2>

<table>
<tr><th>Folder</th><th>Contents</th></tr>
<tr><td>04-Quick-Reference/</td><td>Phonogram chart, spelling rules, spelling analysis routine</td></tr>
<tr><td>05-Teacher-Handbooks/</td><td>5 bound-book-style PDFs (one per stage), 248 lessons with bookmarks</td></tr>
<tr><td>06-Lesson-Packs/</td><td>248 per-lesson bundles (cover + lesson + worksheet + flash cards), one folder per stage</td></tr>
<tr><td>07-Worksheets/</td><td>178 standalone practice sheets (phonograms, rules, cards, blank)</td></tr>
<tr><td>08-Decodable-Readers/</td><td>25 decodable story PDFs + index</td></tr>
<tr><td>09-Quick-Checks/</td><td>Placement test + 5 stage quick-check PDFs (informal diagnostics)</td></tr>
<tr><td>10-Assessments/</td><td>Stage mastery assessments (8 total)</td></tr>
<tr><td>11-Game/</td><td>Phonogram trainer (4 modes: Flash, Match, Speed, Browse, Spell)</td></tr>
<tr><td>12-Audio/</td><td>74 phonogram MP3s (neural TTS)</td></tr>
<tr><td>13-Certificates/</td><td>Printable completion certificates (one per stage)</td></tr>
</table>

<h2>Stages at a glance</h2>

<table>
<tr><th>Stage</th><th>Age</th><th>Lessons</th><th>Focus</th></tr>
<tr><td>1</td><td>Pre-K (4-5)</td><td>48</td><td>Phonemic awareness + 26 single-letter phonograms</td></tr>
<tr><td>2</td><td>K (5-6)</td><td>56</td><td>CVC words + 25 multi-letter phonograms + 6 rules</td></tr>
<tr><td>3</td><td>Gr 1 (6-7)</td><td>56</td><td>Silent E (9 reasons) + 17 PGs + 9 rules + syllable division</td></tr>
<tr><td>4</td><td>Gr 2 (7-8)</td><td>48</td><td>Schwa, suffixing, Latin /sh/, morphology</td></tr>
<tr><td>5</td><td>Gr 3+ (8+)</td><td>40</td><td>25 roots + fluency + composition + grammar</td></tr>
<tr><td><strong>Total</strong></td><td></td><td><strong>248</strong></td><td></td></tr>
</table>

<h2>Methodology — six core ideas</h2>

<ol>
<li><strong>Speech-to-print, not print-to-speech.</strong> Start with the sound; find the written form.</li>
<li><strong>Teach ALL sounds from the start.</strong> "a says /ă/ /ā/ /ä/" — never "a says /ă/" with more later.</li>
<li><strong>Spelling drives reading.</strong> The 5-step Spelling Analysis is the core routine.</li>
<li><strong>No sight words.</strong> Every English word can be decoded with phonograms + rules.</li>
<li><strong>Say-to-Spell is not optional.</strong> Multi-syllable words need deliberate mispronunciation to hear their spelling.</li>
<li><strong>One new thing per lesson.</strong> Never two phonograms or two rules in one lesson.</li>
</ol>

<div class="success">
<strong>Open the index to begin →</strong> <a href="01-Index-and-Table-of-Contents.pdf">01-Index-and-Table-of-Contents.pdf</a>
</div>

<h2>Print and bind</h2>

<p>For classroom use, follow the <a href="binding-instructions.pdf">Workbook Binding Instructions</a> to organize the release ZIP into 3-ring binders per stage. Printable spine labels, tab labels, and a stage-by-stage print job guide included.</p>

</body></html>"""
    out.write_text(html, encoding="utf-8")
    return out


def make_master_index() -> Path:
    """01-Index-and-Table-of-Contents.pdf — master TOC linking to every major section."""
    catalog = load_catalog()
    out = OUT_DIR / "01-Index-and-Table-of-Contents.md"

    # Group lessons by stage
    by_stage = {1: [], 2: [], 3: [], 4: [], 5: []}
    for row in catalog:
        by_stage[int(row["stage"])].append(row)

    sections = []

    for stage in range(1, 6):
        rows = by_stage[stage]
        lessons_html = ""
        for row in rows:
            stage_n = row["stage"]
            ln = int(row["lesson_num"])
            lid = row["lesson_id"]
            title = row["title"]
            ltype = row["type"]
            pack_rel = f"06-Lesson-Packs/stage-{stage_n}/lesson-{ln:02d}-{lid}.pdf"
            lessons_html += f"""
<tr>
  <td><code>{ln}</code></td>
  <td><a href="{pack_rel}">{title}</a></td>
  <td><code>{ltype}</code></td>
</tr>"""

        sections.append(f"""
<h2 id="stage-{stage}">Stage {stage} ({len(rows)} lessons)</h2>
<table>
<tr><th style="width:3em;">#</th><th>Lesson</th><th>Type</th></tr>
{lessons_html}
</table>""")

    sections_html = "\n".join(sections)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<h1>Index &amp; Table of Contents</h1>
<div class="meta">Click any link to jump to that document. PDF bookmarks in the left sidebar also work.</div>

<h2>Navigation</h2>

<div class="toc-item"><span class="title"><a href="00-Start-Here.pdf">Start Here</a></span><span class="page">→ orientation for new users</span></div>
<div class="toc-item"><span class="title"><a href="02-Scope-and-Sequence.pdf">Scope &amp; Sequence</a></span><span class="page">→ full curriculum map</span></div>
<div class="toc-item"><span class="title"><a href="09-Quick-Checks/placement-test.pdf">Placement Test</a></span><span class="page">→ which stage to start at</span></div>
<div class="toc-item"><span class="title"><a href="binding-instructions.pdf">Binding Instructions</a></span><span class="page">→ organize into 3-ring binders</span></div>

<h2>Quick Reference</h2>

<div class="toc-item"><span class="title"><a href="04-Quick-Reference/04-Quick-Reference-Phonograms.pdf">Phonograms</a></span><span class="page">→ all 75 PGs at a glance</span></div>
<div class="toc-item"><span class="title"><a href="04-Quick-Reference/04-Quick-Reference-Spelling-Rules.pdf">Spelling Rules</a></span><span class="page">→ all 31 rules with examples</span></div>
<div class="toc-item"><span class="title"><a href="04-Quick-Reference/04-Quick-Reference-Spelling-Analysis.pdf">Spelling Analysis Routine</a></span><span class="page">→ 5-step poster</span></div>

<h2>Teacher Handbooks (per stage)</h2>

<div class="toc-item"><span class="title"><a href="05-Teacher-Handbooks/stage-1-handbook.pdf">Stage 1 Handbook</a></span><span class="page">→ Pre-K, 48 lessons, single bound PDF</span></div>
<div class="toc-item"><span class="title"><a href="05-Teacher-Handbooks/stage-2-handbook.pdf">Stage 2 Handbook</a></span><span class="page">→ K, 56 lessons</span></div>
<div class="toc-item"><span class="title"><a href="05-Teacher-Handbooks/stage-3-handbook.pdf">Stage 3 Handbook</a></span><span class="page">→ Grade 1, 56 lessons</span></div>
<div class="toc-item"><span class="title"><a href="05-Teacher-Handbooks/stage-4-handbook.pdf">Stage 4 Handbook</a></span><span class="page">→ Grade 2, 48 lessons</span></div>
<div class="toc-item"><span class="title"><a href="05-Teacher-Handbooks/stage-5-handbook.pdf">Stage 5 Handbook</a></span><span class="page">→ Grade 3+, 40 lessons</span></div>

<h2>Lesson Packs (per-lesson bundles)</h2>

<p>Each lesson has a PDF pack containing: cover page with prep checklist, the teacher script, the matched worksheet, flash cards for review. Click into your stage below.</p>

{sections_html}

<h2 id="worksheets">Worksheets</h2>

<div class="toc-item"><span class="title">Phonogram practice</span><span class="page"><a href="07-Worksheets/phonograms/">07-Worksheets/phonograms/</a> — 72 sheets (browse the folder)</span></div>
<div class="toc-item"><span class="title">Spelling rule practice</span><span class="page"><a href="07-Worksheets/rules/">07-Worksheets/rules/</a> — 31 sheets (browse the folder)</span></div>
<div class="toc-item"><span class="title">Flash cards (cut-out)</span><span class="page"><a href="07-Worksheets/cards/">07-Worksheets/cards/</a> — 19 sheets (browse the folder)</span></div>
<div class="toc-item"><span class="title">Blank templates</span><span class="page"><a href="07-Worksheets/blank/">07-Worksheets/blank/</a> — 3 sheets (browse the folder)</span></div>

<h2 id="readers">Decodable Readers</h2>

<div class="toc-item"><span class="title"><a href="08-Decodable-Readers/readers-index.pdf">Readers index</a></span><span class="page">→ all 25 stories with clickable links</span></div>
<div class="toc-item"><span class="title">Individual readers</span><span class="page">08-Decodable-Readers/ folder — 25 story PDFs</span></div>

<h2 id="quick-checks">Quick Checks &amp; Placement</h2>

<div class="toc-item"><span class="title">Placement test</span><span class="page"><a href="09-Quick-Checks/placement-test.pdf">09-Quick-Checks/placement-test.pdf</a></span></div>
<div class="toc-item"><span class="title">Quick check — Stage 1</span><span class="page"><a href="09-Quick-Checks/quick-check-stage-1.pdf">09-Quick-Checks/quick-check-stage-1.pdf</a></span></div>
<div class="toc-item"><span class="title">Quick check — Stage 2</span><span class="page"><a href="09-Quick-Checks/quick-check-stage-2.pdf">09-Quick-Checks/quick-check-stage-2.pdf</a></span></div>
<div class="toc-item"><span class="title">Quick check — Stage 3</span><span class="page"><a href="09-Quick-Checks/quick-check-stage-3.pdf">09-Quick-Checks/quick-check-stage-3.pdf</a></span></div>
<div class="toc-item"><span class="title">Quick check — Stage 4</span><span class="page"><a href="09-Quick-Checks/quick-check-stage-4.pdf">09-Quick-Checks/quick-check-stage-4.pdf</a></span></div>
<div class="toc-item"><span class="title">Quick check — Stage 5</span><span class="page"><a href="09-Quick-Checks/quick-check-stage-5.pdf">09-Quick-Checks/quick-check-stage-5.pdf</a></span></div>

<h2 id="assessments">Assessments</h2>

<div class="toc-item"><span class="title">Stage 1 mastery check</span><span class="page">Lesson 48</span></div>
<div class="toc-item"><span class="title">Stage 2 mid + mastery</span><span class="page">Lessons 24, 56</span></div>
<div class="toc-item"><span class="title">Stage 3 mid + mastery</span><span class="page">Lessons 24, 56</span></div>
<div class="toc-item"><span class="title">Stage 4 mid + mastery</span><span class="page">Lessons 13, 48</span></div>
<div class="toc-item"><span class="title">Stage 5 mastery</span><span class="page">Lesson 40</span></div>

<h2 id="extras">Extras</h2>

<div class="toc-item"><span class="title"><a href="11-Game/phonogram-trainer.html">Phonogram Trainer (web game)</a></span><span class="page">→ 5 modes: Flash, Match, Speed, Browse, Spell</span></div>
<div class="toc-item"><span class="title"><a href="12-Audio/">Phonogram audio MP3s</a></span><span class="page">→ 74 neural-TTS MP3s</span></div>
<div class="toc-item"><span class="title"><a href="13-Certificates/certificate-stage-1.pdf">Certificate — Stage 1</a></span><span class="page">→ printable completion certificate</span></div>
<div class="toc-item"><span class="title"><a href="13-Certificates/certificate-stage-2.pdf">Certificate — Stage 2</a></span><span class="page">→ printable completion certificate</span></div>
<div class="toc-item"><span class="title"><a href="13-Certificates/certificate-stage-3.pdf">Certificate — Stage 3</a></span><span class="page">→ printable completion certificate</span></div>
<div class="toc-item"><span class="title"><a href="13-Certificates/certificate-stage-4.pdf">Certificate — Stage 4</a></span><span class="page">→ printable completion certificate</span></div>
<div class="toc-item"><span class="title"><a href="13-Certificates/certificate-stage-5.pdf">Certificate — Stage 5</a></span><span class="page">→ printable completion certificate</span></div>

</body></html>"""
    out.write_text(html, encoding="utf-8")
    return out


def make_scope_sequence() -> Path:
    """02-Scope-and-Sequence.pdf — full curriculum map."""
    catalog = load_catalog()
    out = OUT_DIR / "02-Scope-and-Sequence.md"

    # Count phonograms introduced by stage
    pgs_by_stage = {1: set(), 2: set(), 3: set(), 4: set(), 5: set()}
    rules_by_stage = {1: set(), 2: set(), 3: set(), 4: set(), 5: set()}
    for row in catalog:
        s = int(row["stage"])
        pg = (row.get("new_phonogram") or "").strip()
        if pg:
            pgs_by_stage[s].add(pg)
        rule = (row.get("new_rule") or "").strip()
        if rule:
            import re
            for r in re.split(r"[,+]", rule):
                r = re.split(r"\.", r, maxsplit=1)[0]
                if "-" in r:
                    m = re.match(r"^(\d+)-(\d+)$", r)
                    if m:
                        for n in range(int(m.group(1)), int(m.group(2)) + 1):
                            rules_by_stage[s].add(str(n))
                else:
                    rules_by_stage[s].add(r)

    stages = [
        (1, "Pre-K (4-5)", "Phonemic awareness + 26 single-letter phonograms",
         "Stage 1 develops the auditory foundation. Children learn to hear, blend, and segment sounds before letters are introduced. Then 26 single-letter phonograms are taught in 5 groups, with one phonemic-awareness lesson between each group.",
         "48 lessons"),
        (2, "K (5-6)", "CVC words + 25 multi-letter phonograms + 6 rules",
         "Stage 2 introduces 25 multi-letter phonograms (sh, th, ck, ee, ng, ar, or, er, oi, oy, ai, ay, ch, wh, ea, ow, ou, oo, ed, igh, aw, au, ir, ur, oa, ear) plus the first spelling rules (CK, No I/U/V/J, AY, Long at end, -ED, GH, Floss). Children practice Spelling Analysis on 3-5 words per lesson.",
         "56 lessons"),
        (3, "Grade 1 (6-7)", "Silent E (9 reasons) + 17 PGs + 9 rules + syllables",
         "Stage 3 covers the 9 reasons for Silent E, then 17 advanced phonograms (dge, tch, kn, gn, wr, eigh, ei, ey, ph, gh, ough, augh, ew, ui, eu, wor, ie). Syllable division rules introduced. Say-to-Spell method used for multi-syllable words from Lesson 47 onward.",
         "56 lessons"),
        (4, "Grade 2 (7-8)", "Schwa + suffixing + Latin /sh/ + morphology",
         "Stage 4 begins with the schwa deep dive (Rule 31), then suffixing rules (13-16: Drop E, double consonant, Y→I, two I's). Latin /sh/ phonograms (ti, ci, si) with Rules 17-18. Morphology: 4 prefix pairs + 6 suffix pairs.",
         "48 lessons"),
        (5, "Grade 3+ (8+)", "25 roots + fluency + composition + grammar",
         "Stage 5 teaches 25 Latin/Greek roots across 12+10+3 sets. Fluency drills, sentence and paragraph composition, parts of speech, and punctuation. Final reader is an informational passage on ostriches.",
         "40 lessons"),
    ]

    sections = []
    for stage, age, focus, desc, lesson_count in stages:
        pgs = sorted(pgs_by_stage[stage])
        rules = sorted(rules_by_stage[stage], key=lambda r: (len(r), r))
        pgs_html = ", ".join(pgs) if pgs else "(none — phonemic awareness only)"
        rules_html = ", ".join(f"Rule {r}" for r in rules) if rules else "(none)"

        sections.append(f"""
<h2 id="stage-{stage}">Stage {stage} — {age}</h2>
<p><strong>Focus:</strong> {focus}<br>
<strong>Lessons:</strong> {lesson_count}</p>

<p>{desc}</p>

<h3>New phonograms introduced ({len(pgs)}):</h3>
<p>{pgs_html}</p>

<h3>New rules introduced ({len(rules)}):</h3>
<p>{rules_html}</p>
""")

    sections_html = "\n".join(sections)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<h1>Scope &amp; Sequence</h1>
<div class="meta">The complete curriculum at a glance — what's taught when across all 5 stages.</div>

<h2>Overview</h2>

<table>
<tr><th>Stage</th><th>Age</th><th>Lessons</th><th>Focus</th></tr>
<tr><td><a href="#stage-1">1</a></td><td>Pre-K (4-5)</td><td>48</td><td>Phonemic awareness + 26 single-letter phonograms</td></tr>
<tr><td><a href="#stage-2">2</a></td><td>K (5-6)</td><td>56</td><td>CVC words + 25 multi-letter PGs + 6 rules</td></tr>
<tr><td><a href="#stage-3">3</a></td><td>Gr 1 (6-7)</td><td>56</td><td>Silent E (9 reasons) + 17 PGs + 9 rules + syllables</td></tr>
<tr><td><a href="#stage-4">4</a></td><td>Gr 2 (7-8)</td><td>48</td><td>Schwa, suffixing, Latin /sh/, morphology</td></tr>
<tr><td><a href="#stage-5">5</a></td><td>Gr 3+ (8+)</td><td>40</td><td>25 roots + fluency + composition + grammar</td></tr>
<tr><td><strong>Total</strong></td><td></td><td><strong>248</strong></td><td></td></tr>
</table>

<p><strong>Total scope:</strong> 75 phonograms (26 single-letter + 49 multi-letter), 31 spelling rules, 8 assessments, 25 decodable readers, 178 worksheets, 15 quick-checks, 1 placement test.</p>

{sections_html}

<h2>Methodology — six core ideas</h2>

<ol>
<li><strong>Speech-to-print, not print-to-speech.</strong> Start with the sound; find the written form.</li>
<li><strong>Teach ALL sounds from the start.</strong> "a says /ă/ /ā/ /ä/" — never "a says /ă/" with more later.</li>
<li><strong>Spelling drives reading.</strong> The 5-step Spelling Analysis is the core routine.</li>
<li><strong>No sight words.</strong> Every English word can be decoded with phonograms + rules.</li>
<li><strong>Say-to-Spell is not optional.</strong> Multi-syllable words need deliberate mispronunciation to hear their spelling.</li>
<li><strong>One new thing per lesson.</strong> Never two phonograms or two rules in one lesson.</li>
</ol>

<p><em>For the full methodology, see <a href="01-Index-and-Table-of-Contents.pdf">the Index</a> for links to the teacher handbooks per stage.</em></p>

</body></html>"""
    out.write_text(html, encoding="utf-8")
    return out


def make_quick_refs() -> list[Path]:
    """Quick-reference PDFs (phonograms, rules, spelling analysis)."""
    outs = []

    # Phonogram chart — simplified 75-PG list
    pg_list = []
    single_pgs = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","qu","r","s","t","u","v","w","x","y","z"]
    multi_pgs = ["sh","th","ck","ee","ng","ar","or","er","oi","oy","ai","ay","ch","wh","ea","ow","ou","oo","ed","igh","aw","au","ir","ur","oa","ear","dge","tch","kn","gn","wr","eigh","ei","ey","ph","gh","ough","augh","ew","ui","eu","wor","ie","ti","ci","si"]

    rows = ""
    for pg in single_pgs:
        rows += f"<tr><td><code>{pg}</code></td><td>single-letter</td></tr>\n"
    for pg in multi_pgs:
        rows += f"<tr><td><code>{pg}</code></td><td>multi-letter</td></tr>\n"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<h1>Phonograms Quick Reference</h1>
<div class="meta">All 75 phonograms at a glance. For sounds and example words, see the teacher handbook for your stage.</div>

<h2>Single-letter phonograms (26)</h2>
<table>
<tr><th>Phonogram</th><th>Type</th></tr>
{rows[:26*2]}
</table>

<h2>Multi-letter phonograms (49)</h2>
<table>
<tr><th>Phonogram</th><th>Type</th></tr>
{rows[26*2:]}
</table>

<p><em>Source methodology: <a href="https://logicofenglish.com/">Uncovering the Logic of English</a> by Denise Eide.</em></p>

</body></html>"""
    out = OUT_DIR / "04-Quick-Reference-Phonograms.md"
    out.write_text(html, encoding="utf-8")
    outs.append(out)

    # Spelling rules — list of 31
    rule_descs = [
        ("1", "C softens to /s/ before E, I, Y"),
        ("2", "G may soften to /j/ before E, I, Y"),
        ("3", "No English word ends in I, U, V, or J"),
        ("4", "A E O U say long at end of syllable"),
        ("5", "I and Y at end of syllable say /ĭ/ or /ī/"),
        ("6", "Y says /ī/ at end of one-syllable word"),
        ("7", "I and Y may say /ē/"),
        ("8", "I and O may say /ī/ /ō/ before two consonants"),
        ("9", "AY spells /ā/ at end of base word"),
        ("10", "A says /ä/ at end, after W, before L"),
        ("11", "Q always needs U"),
        ("12", "Silent E (9 reasons)"),
        ("13", "Drop silent E for vowel suffix"),
        ("14", "Double consonant (1-1-1 rule)"),
        ("15", "Y changes to I before suffix"),
        ("16", "Two I's cannot be adjacent"),
        ("17", "TI CI SI spell /sh/ in Latin words"),
        ("18", "SH at beginning/end of base word"),
        ("19", "Past tense formed with -ED"),
        ("20", "Three sounds of -ED (/ed/, /d/, /t/)"),
        ("21", "Plural -S and -ES"),
        ("22", "3rd person singular -S and -ES"),
        ("23", "AL- prefix has one L"),
        ("24", "-FUL suffix has one L"),
        ("25", "DGE after short vowel"),
        ("26", "CK after short vowel"),
        ("27", "TCH after short vowel"),
        ("28", "GH phonograms (silent, voiced, /f/)"),
        ("29", "Z not S at beginning for /z/"),
        ("30", "Double F L S (Floss Rule)"),
        ("31", "Schwa in unstressed syllables"),
    ]
    rows = ""
    for num, desc in rule_descs:
        rows += f"<tr><td><code>Rule {num}</code></td><td>{desc}</td></tr>\n"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<h1>Spelling Rules Quick Reference</h1>
<div class="meta">All 31 spelling rules at a glance. For examples and exceptions, see the teacher handbook for your stage.</div>

<table>
<tr><th style="width:5em;">Rule</th><th>Description</th></tr>
{rows}
</table>

<p><em>Source methodology: <a href="https://logicofenglish.com/">Uncovering the Logic of English</a> by Denise Eide.</em></p>

</body></html>"""
    out = OUT_DIR / "04-Quick-Reference-Spelling-Rules.md"
    out.write_text(html, encoding="utf-8")
    outs.append(out)

    # Spelling analysis routine poster
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<h1>Spelling Analysis — 5-Step Routine</h1>
<div class="meta">The core routine used in every lesson. Print this poster and keep it visible.</div>

<h2>For every word being spelled</h2>

<table>
<tr><th style="width:3em;">Step</th><th>Teacher</th><th>Student</th></tr>
<tr>
  <td><strong>1</strong></td>
  <td>Say the word. Use it in a sentence.</td>
  <td>Listen. Repeat the word.</td>
</tr>
<tr>
  <td><strong>2</strong></td>
  <td>Hold up fingers (one per sound).</td>
  <td>Segment the word into individual sounds.</td>
</tr>
<tr>
  <td><strong>3</strong></td>
  <td>Watch the student write.</td>
  <td>Write the phonograms for each sound.</td>
</tr>
<tr>
  <td><strong>4</strong></td>
  <td>"What rules? Underline multi-letter phonograms."</td>
  <td>Identify phonograms + rules used.</td>
</tr>
<tr>
  <td><strong>5</strong></td>
  <td>"Read it sound by sound, then blend."</td>
  <td>Sound out, then blend and read.</td>
</tr>
</table>

<h2>Say-to-Spell (Stages 3+)</h2>
<p>For multi-syllable words with schwa:</p>
<ol>
<li>Say the word normally.</li>
<li>Pronounce with clear vowels (e.g., <code>about</code> → <code>ā-bout</code>).</li>
<li>Segment.</li>
<li>Write.</li>
<li>Read the word normally.</li>
</ol>

<div class="callout">
<strong>Why this works:</strong> Spelling Analysis uses the auditory skills (segmenting) plus the visual skills (writing phonograms) plus the analytical skills (rules). Three modalities engaged = strong memory.
</div>

</body></html>"""
    out = OUT_DIR / "04-Quick-Reference-Spelling-Analysis.md"
    out.write_text(html, encoding="utf-8")
    outs.append(out)

    return outs


def render_md_to_pdf(md_path: Path):
    from weasyprint import HTML as WHTML
    pdf_path = md_path.with_suffix(".pdf")
    WHTML(filename=str(md_path)).write_pdf(str(pdf_path))


def main():
    parser = argparse.ArgumentParser(description="Generate navigation PDFs")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering")
    args = parser.parse_args()

    print("==> Generating navigation PDFs")
    files = []
    files.append(make_start_here())
    print(f"  OK  00-Start-Here.md")
    files.append(make_master_index())
    print(f"  OK  01-Index-and-Table-of-Contents.md")
    files.append(make_scope_sequence())
    print(f"  OK  02-Scope-and-Sequence.md")
    for f in make_quick_refs():
        files.append(f)
        print(f"  OK  {f.name}")

    if args.no_render:
        return

    print("\n==> Rendering navigation PDFs")
    for f in files:
        render_md_to_pdf(f)
        print(f"  OK  {f.with_suffix('.pdf').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
