# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate printable binding instructions PDF.

Tells teachers how to organize the release ZIP into physical 3-ring binders
per stage, with dividers and printable spine labels.

Output: build/handbook/binding-instructions.pdf

Usage:
  python scripts/generate-binding-instructions.py
"""

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from framework.render import render_html_to_pdf

OUT_DIR = ROOT / "build" / "handbook"
OUT_DIR.mkdir(parents=True, exist_ok=True)


HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
@page { size: letter; margin: 0.75in; @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 9pt; color: #555; } }
body { font-family: Georgia, "Times New Roman", serif; font-size: 12pt; line-height: 1.6; color: #222; }
h1 { font-size: 26pt; color: #2a5c8a; margin: 0 0 0.3em 0; border-bottom: 3px solid #2a5c8a; padding-bottom: 0.3em; bookmark-level: 1; }
h2 { font-size: 18pt; color: #2a5c8a; margin-top: 1.5em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; bookmark-level: 2; page-break-after: avoid; }
h3 { font-size: 14pt; color: #2a5c8a; margin-top: 1.2em; bookmark-level: 3; page-break-after: avoid; }
.meta { color: #555; font-size: 10pt; margin-bottom: 1.5em; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 11pt; }
th, td { border-bottom: 1px solid #ccc; padding: 5pt 8pt; text-align: left; vertical-align: top; }
th { background: #f0f4f8; font-weight: bold; }
code { background: #f4f0e8; padding: 1px 4px; border-radius: 2px; font-family: "Courier New", monospace; font-size: 10pt; }
.callout { background: #f8f4e8; padding: 0.8em 1em; border-left: 4px solid #c8a832; margin: 1em 0; }
.success { background: #e8f4e8; padding: 0.8em 1em; border-left: 4px solid #4a8a3a; margin: 1em 0; }
.binder-label {
  border: 2px dashed #555;
  padding: 1em;
  margin: 1em 0;
  font-family: "Courier New", monospace;
  font-size: 14pt;
  text-align: center;
  background: #fdfdfb;
}
.divider-list { columns: 2; column-gap: 2em; }
.divider-list li { break-inside: avoid; }
.tab-template {
  border: 1px solid #888;
  display: inline-block;
  padding: 0.4em 1em;
  margin: 0.2em;
  font-family: "Courier New", monospace;
  font-size: 10pt;
  background: #fafafa;
}
</style></head>
<body>

<h1>Workbook Binding Instructions</h1>
<div class="meta">How to organize the release ZIP into physical 3-ring binders — one per stage — for daily classroom use.</div>

<h2>What you need</h2>

<table>
<tr><th>Item</th><th>Quantity</th><th>Notes</th></tr>
<tr><td>3-ring binder, 1.5"</td><td>5 (one per stage)</td><td>Or use larger binders (2-3") if you plan to keep all 248 lesson packs</td></tr>
<tr><td>3-hole punch</td><td>1</td><td>For lesson pack and worksheet pages</td></tr>
<tr><td>Binder dividers, 5-tab</td><td>5 sets</td><td>Plastic with pockets are more durable</td></tr>
<tr><td>Sheet protectors</td><td>1 pack of 50</td><td>For the reference charts and quick-reference pages</td></tr>
<tr><td>Printer + ink/toner</td><td>—</td><td>Print double-sided when possible</td></tr>
<tr><td>Card stock</td><td>20-30 sheets</td><td>For flash cards and certificates</td></tr>
<tr><td>Labels or tape</td><td>—</td><td>For spine labels (see templates below)</td></tr>
</table>

<div class="callout">
<strong>Time estimate:</strong> ~3-4 hours total to set up all 5 binders. Spread over a weekend. After setup, each new lesson pack = ~2 minutes to punch and insert.
</div>

<h2>Binder 1: Stage 1 (Pre-K, 48 lessons)</h2>

<p><strong>Binder label:</strong></p>
<div class="binder-label">STAGE 1<br>Pre-K (4-5)<br>Phonemic Awareness + First Phonograms<br>48 lessons</div>

<p><strong>Tab dividers (in order):</strong></p>
<ol class="divider-list">
<li><strong>Quick Reference</strong> — phonogram chart, spelling rules (later stages), spelling analysis routine</li>
<li><strong>Scope &amp; Sequence</strong> — one-page overview of Stage 1</li>
<li><strong>Lesson Packs</strong> — 48 packs in numerical order (lesson-01 through lesson-48)</li>
<li><strong>Worksheets</strong> — phonogram practice sheets, blank templates</li>
<li><strong>Readers</strong> — Stage 2+ readers (none in Stage 1)</li>
<li><strong>Quick Checks &amp; Assessments</strong> — quick-check-stage-1, assessment-1</li>
<li><strong>Misc</strong> — certificate (blank), notes</li>
</ol>

<h3>Print job for Stage 1 setup</h3>

<table>
<tr><th>What</th><th>Source</th><th>Pages</th></tr>
<tr><td>Phonogram chart</td><td><code>04-Quick-Reference/04-Quick-Reference-Phonograms.pdf</code></td><td>1 (or 2-3 for poster)</td></tr>
<tr><td>Stage 1 cover page</td><td>First page of <code>05-Teacher-Handbooks/stage-1-handbook.pdf</code></td><td>1</td></tr>
<tr><td>Lesson packs</td><td><code>06-Lesson-Packs/stage-1/</code></td><td>~400 pages</td></tr>
<tr><td>Quick-check</td><td><code>09-Quick-Checks/quick-check-stage-1.pdf</code></td><td>3</td></tr>
<tr><td>Assessment</td><td><code>10-Assessments/assessment-1.pdf</code></td><td>~5</td></tr>
<tr><td>Certificate (blank)</td><td><code>13-Certificates/certificate-stage-1.pdf</code></td><td>1 (card stock)</td></tr>
</table>

<h2>Binders 2-5: Stages 2-5</h2>

<p>Same structure as Stage 1, with one important addition per binder:</p>

<ul>
<li><strong>Stage 2:</strong> Add 8 readers from <code>08-Decodable-Readers/</code> (or relevant subset). 56 lessons.</li>
<li><strong>Stage 3:</strong> Add 3 readers + spelling rules quick reference. 56 lessons.</li>
<li><strong>Stage 4:</strong> Add 2 readers. 48 lessons.</li>
<li><strong>Stage 5:</strong> Add 1 reader (Ostriches). 40 lessons.</li>
</ul>

<p>Stages 2-5 also include the spelling rules quick reference in their <code>04-Quick-Reference/</code>.</p>

<h2>Spine labels (print and tape)</h2>

<p>Print this page on card stock. Cut along the dashed lines. Tape one label to each binder spine.</p>

<div class="binder-label">STAGE 1 — Pre-K</div>
<div class="binder-label">STAGE 2 — K</div>
<div class="binder-label">STAGE 3 — Grade 1</div>
<div class="binder-label">STAGE 4 — Grade 2</div>
<div class="binder-label">STAGE 5 — Grade 3+</div>

<h2>Divider tab labels (print and trim)</h2>

<p>Print this section on card stock. Cut out each tab. Glue to the divider tabs.</p>

<div style="margin: 1em 0;">
<span class="tab-template">Quick Reference</span>
<span class="tab-template">Scope &amp; Sequence</span>
<span class="tab-template">Lesson Packs</span>
<span class="tab-template">Worksheets</span>
<span class="tab-template">Readers</span>
<span class="tab-template">Quick Checks</span>
<span class="tab-template">Assessments</span>
<span class="tab-template">Certificate</span>
</div>

<h2>Sheet protector cheat sheet</h2>

<p>Use sheet protectors for items that get touched often:</p>

<ul>
<li><strong>Definitely:</strong> Phonogram chart, spelling rules poster, spelling analysis routine poster — these get read daily</li>
<li><strong>Yes:</strong> Stage cover pages, scope &amp; sequence, placement test</li>
<li><strong>Maybe:</strong> Quick-checks (if used often)</li>
<li><strong>No:</strong> Lesson packs (they leave the binder to be taught from), worksheets (consumed by student)</li>
</ul>

<h2>Card stock priorities</h2>

<p>Print these on card stock (most-used, longest-lasting first):</p>

<ol>
<li>Flash cards (<code>07-Worksheets/cards/</code>) — daily use</li>
<li>Certificate template (one blank per stage) — printed ahead of stage completion</li>
<li>Phonogram chart — wall reference</li>
<li>Spelling rules poster — desk reference</li>
</ol>

<h2>Weekly maintenance</h2>

<ul>
<li><strong>After each lesson:</strong> Mark the lesson pack with a sticky tab to track progress through the binder tabs</li>
<li><strong>Monthly:</strong> Update the stage cover page with date completed (write on the cover)</li>
<li><strong>Per stage:</strong> Move lesson packs from "Lesson Packs" tab to a separate "Completed" tab (saves space)</li>
<li><strong>Per year:</strong> Print a fresh phonogram chart if it's getting worn</li>
</ul>

<h2>Multi-child / classroom setup</h2>

<p>If you teach multiple children through the same stage, duplicate the lesson packs you need:</p>

<ul>
<li><strong>One family:</strong> Use one binder. Each child writes their name on worksheets. Worksheets stay in the binder for the year.</li>
<li><strong>One classroom (15+ kids):</strong> Print lesson packs 2-3 copies of each (one for teacher + one for the student to keep). Or print the lesson script once (in teacher binder) and photocopy just the worksheet for each student.</li>
<li><strong>Co-op (multiple families, one binder):</strong> Print lesson packs and worksheets for each participating family. Share the teacher binder only.</li>
</ul>

<div class="success">
<strong>Final tip:</strong> After completing each stage, take 30 minutes to reorganize: move lesson packs to "Completed", pull the next stage's binder forward, file the completed stage in a separate "Completed" shelf or box. You'll thank yourself later.
</div>

</body></html>"""


def main():
    out = OUT_DIR / "binding-instructions.md"
    out.write_text(HTML, encoding="utf-8")

    pdf = out.with_suffix(".pdf")
    render_html_to_pdf(HTML, pdf, body_class="index")
    out.unlink(missing_ok=True)
    print(f"  OK  {pdf.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
