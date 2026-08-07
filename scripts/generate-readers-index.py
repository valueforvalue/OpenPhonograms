# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate a clickable index of all decodable readers.

Output: build/handbook/readers-index.pdf
"""

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from framework.render import render_html_to_pdf
READERS_DIR = ROOT / "readers"
OUT_DIR = ROOT / "build" / "handbook"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CSS = """
@page { size: letter; margin: 0.75in; @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 9pt; color: #555; } @bottom-left { content: "OpenPhonograms · MIT licensed"; font-family: Georgia, serif; font-size: 7pt; color: #aaa; } }
body { font-family: Georgia, "Times New Roman", serif; font-size: 11pt; line-height: 1.5; color: #222; }
h1 { font-size: 22pt; color: #2a5c8a; margin: 0 0 0.3em 0; border-bottom: 3px solid #2a5c8a; padding-bottom: 0.3em; bookmark-level: 1; }
h2 { font-size: 15pt; color: #2a5c8a; margin-top: 1.2em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; bookmark-level: 2; }
.meta { color: #555; font-size: 9pt; margin-bottom: 1em; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 11pt; }
th, td { border-bottom: 1px solid #ccc; padding: 5pt 8pt; text-align: left; }
th { background: #f0f4f8; font-weight: bold; }
a { color: #2a5c8a; text-decoration: none; border-bottom: 1px dotted #2a5c8a; }
code { background: #f4f0e8; padding: 1px 4px; border-radius: 2px; font-family: "Courier New", monospace; font-size: 10pt; }
"""


def find_readers() -> list[dict]:
    """Find all reader MD files and group by stage."""
    readers = []
    for path in sorted(READERS_DIR.glob("*.md")):
        # Filename like "001-fred-the-frog.md"
        stem = path.stem
        parts = stem.split("-", 1)
        if len(parts) < 2 or not parts[0].isdigit():
            continue
        num = int(parts[0])
        slug = parts[1]

        # Read first line for title
        text = path.read_text(encoding="utf-8")
        title = text.split("\n", 1)[0].lstrip("# ").strip() if text else slug

        # Determine stage from filename prefix or content
        # Stage 2 readers are 001-013, Stage 3 are 014-?
        # Better: use stage subdir or read first 10 lines for "Stage X" mention
        stage = 2  # default
        for line in text.split("\n")[:15]:
            if "Stage 2" in line:
                stage = 2
            elif "Stage 3" in line:
                stage = 3
            elif "Stage 4" in line:
                stage = 4
            elif "Stage 5" in line:
                stage = 5

        readers.append({"num": num, "slug": slug, "title": title, "stage": stage, "path": path})

    readers.sort(key=lambda r: r["num"])
    return readers


def main():
    readers = find_readers()
    by_stage = {}
    for r in readers:
        by_stage.setdefault(r["stage"], []).append(r)

    rows_html = ""
    for stage in sorted(by_stage.keys()):
        rows_html += f"<tr><td colspan='4' style='background:#e8f4f8;font-weight:bold;'>Stage {stage} ({len(by_stage[stage])} readers)</td></tr>\n"
        for r in by_stage[stage]:
            num = r["num"]
            slug = r["slug"]
            title = r["title"]
            pdf_rel = f"08-Decodable-Readers/{num:03d}-{slug}.pdf"
            rows_html += f"<tr><td><code>{num:03d}</code></td><td><a href='{pdf_rel}'>{title}</a></td><td><code>{slug}</code></td><td>Stage {r['stage']}</td></tr>\n"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<h1>Decodable Readers — Index</h1>
<div class="meta">All {len(readers)} decodable readers in this release. Click any title to open the PDF.</div>

<p>Every reader uses only phonograms taught at-or-before the stage noted. Stage 2 readers use single-letter PGs and early multi-letter PGs (sh, th, ck, ee). Stage 3 readers introduce multi-syllable words. Stage 4-5 readers use morphology and advanced vocabulary.</p>

<table>
<tr><th style="width:3em;">#</th><th>Title</th><th>Slug</th><th>Stage</th></tr>
{rows_html}
</table>

<p><em>Open-source. MIT licensed. Phonograms drawn from the public-domain phonics tradition (1800s onward).</em></p>

</body></html>"""

    md_path = OUT_DIR / "readers-index.md"
    md_path.write_text(html, encoding="utf-8")

    pdf_path = md_path.with_suffix(".pdf")
    render_html_to_pdf(html, pdf_path, body_class="index")
    md_path.unlink(missing_ok=True)
    print(f"  OK  {pdf_path.relative_to(ROOT)}  ({len(readers)} readers indexed)")


if __name__ == "__main__":
    main()
