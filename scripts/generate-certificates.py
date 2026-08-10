# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate printable completion certificates (one per stage).

Each certificate is a single-page PDF with a decorative border, the stage
name, and lines for student name + date + teacher signature.

Usage:
  python scripts/generate-certificates.py [--no-render]
"""

import argparse
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from framework.render import render_html_to_pdf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "build" / "handbook"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STAGE_NAMES = {
    1: ("Stage 1: Phonemic Awareness & First Phonograms", "Pre-K (4-5)"),
    2: ("Stage 2: CVC Words & First Multi-Letter Phonograms", "Kindergarten (5-6)"),
    3: ("Stage 3: Silent E & Vowel Teams", "Grade 1 (6-7)"),
    4: ("Stage 4: Suffixing, Latin /sh/ & Morphology", "Grade 2 (7-8)"),
    5: ("Stage 5: Roots, Fluency & Composition", "Grade 3+ (8+)"),
}


def make_certificate(stage: int) -> str:
    """Generate the HTML for a stage certificate."""
    title, age = STAGE_NAMES[stage]
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
@page {{ size: letter landscape; margin: 0.5in; }}
@page :first {{ margin-top: 0.5in; @top-center {{ content: none; }} @bottom-left {{ content: none; }} }}
body {{
  font-family: Georgia, "Times New Roman", serif;
  text-align: center;
  padding: 1em;
  background: linear-gradient(135deg, #fefefe 0%, #f8f4e8 100%);
}}
.cert {{
  border: 8px double #2a5c8a;
  padding: 2em 1em;
  margin: 0.5em auto;
  max-width: 9in;
  background: white;
  position: relative;
}}
.cert::before {{
  content: "";
  position: absolute;
  top: 8px; left: 8px; right: 8px; bottom: 8px;
  border: 2px solid #c8a832;
  pointer-events: none;
}}
.header {{
  font-size: 16pt;
  color: #555;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  margin-bottom: 0.5em;
}}
.title {{
  font-size: 38pt;
  color: #2a5c8a;
  margin: 0.2em 0;
  font-weight: bold;
}}
.subtitle {{
  font-size: 14pt;
  color: #555;
  margin-bottom: 1em;
}}
.body {{
  font-size: 14pt;
  margin: 1.5em 0;
  line-height: 1.8;
}}
.name-line {{
  border-bottom: 2px solid #2a5c8a;
  width: 60%;
  margin: 1em auto;
  font-size: 22pt;
  color: #2a5c8a;
  font-style: italic;
  padding-bottom: 4pt;
}}
.footer {{
  margin-top: 2em;
  display: flex;
  justify-content: space-around;
  font-size: 11pt;
  color: #555;
}}
.signature {{
  border-top: 1px solid #555;
  padding-top: 4pt;
  width: 3in;
  text-align: center;
}}
.footer-stamp {{
  margin-top: 1em;
  font-size: 9pt;
  color: #888;
  letter-spacing: 0.2em;
}}
</style></head>
<body>

<div class="cert">
  <div class="header">Certificate of Completion</div>
  <div class="title">{title}</div>
  <div class="subtitle">OpenPhonograms · {age}</div>

  <div class="body">
    This certifies that
    <div class="name-line">&nbsp;</div>
    has successfully completed all lessons, assessments, and decodable readers of <strong>{title}</strong>, demonstrating mastery of phonograms, spelling rules, and reading skills.
  </div>

  <div class="footer">
    <div class="signature">Date</div>
    <div class="signature">Teacher / Parent Signature</div>
  </div>

  <div class="footer-stamp">OPENPHONOGRAMS · OPEN-SOURCE CURRICULUM</div>
</div>

</body></html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate completion certificates")
    parser.add_argument("--no-render", action="store_true", help="Skip PDF rendering")
    args = parser.parse_args()

    print("==> Generating certificates")
    for stage in range(1, 6):
        html = make_certificate(stage)
        md_path = OUT_DIR / f"certificate-stage-{stage}.md"
        md_path.write_text(html, encoding="utf-8")

        if not args.no_render:
            pdf_path = md_path.with_suffix(".pdf")
            render_html_to_pdf(html, pdf_path, body_class="certificate")
            md_path.unlink(missing_ok=True)
            print(f"  OK  {pdf_path.relative_to(ROOT)}")
        else:
            print(f"  OK  {md_path.relative_to(ROOT)}")

    print("\nDone: 5 certificates")


if __name__ == "__main__":
    main()
