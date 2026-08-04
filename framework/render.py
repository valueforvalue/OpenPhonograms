#!/usr/bin/env python3
"""
render.py — Convert Logic of English lesson markdown files to printable PDF.

Usage:
    python render.py lessons/stage-1/002-phonogram-a.md
    python render.py --stage 2
    python render.py --all
    python render.py --curriculum

Output:
    Same directory as source, with .pdf extension.
    Stage/curriculum renders go to build/ directory.
"""

import argparse
import csv
import os
import sys
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "lessons"
WORKSHEETS_DIR = PROJECT_ROOT / "worksheets"
READERS_DIR = PROJECT_ROOT / "readers"
IMAGES_DIR = PROJECT_ROOT / "images"
BUILD_DIR = PROJECT_ROOT / "build"
FRAMEWORK_DIR = PROJECT_ROOT / "framework"
TEMPLATES_DIR = FRAMEWORK_DIR / "templates"
CATALOG_PATH = FRAMEWORK_DIR / "lesson-catalog.csv"

PAGE_CSS = """
@page {
    size: letter;
    margin: 0.75in;
    @bottom-center {
        content: counter(page);
        font-family: Georgia, serif;
        font-size: 9pt;
        color: #888;
    }
}

@page worksheet {
    size: letter;
    margin: 0.5in;
}

body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 14pt;
    line-height: 1.7;
    color: #111;
}

body.worksheet {
    font-size: 12pt;
}

body.reader {
    font-size: 20pt;
    line-height: 1.8;
}

h1 { font-size: 22pt; margin-top: 0; page-break-before: avoid; }
h2 { font-size: 16pt; color: #2a5c8a; page-break-after: avoid; }
h3 { font-size: 13pt; page-break-after: avoid; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 11pt;
}
th, td {
    border-bottom: 1px solid #ddd;
    padding: 6pt 8pt;
    text-align: left;
    vertical-align: top;
}
th { font-weight: bold; border-bottom-width: 2px; background: #f7f7f2; }

.phonogram {
    font-size: 72pt;
    font-weight: bold;
    color: #2a5c8a;
    text-align: center;
    display: block;
    margin: 1em 0;
    font-family: Georgia, serif;
    line-height: 1.1;
    border: 2px solid #2a5c8a;
    border-radius: 8px;
    padding: 0.4em;
    background: #fffff8;
    page-break-inside: avoid;
}

.phonogram-card {
    border: 2px solid #2a5c8a;
    border-radius: 8px;
    padding: 1.2em 1.5em;
    margin: 1.5em 0;
    text-align: center;
    background: #fffff8;
    page-break-inside: avoid;
}

.phonogram-letter {
    font-size: 72pt;
    font-weight: bold;
    color: #2a5c8a;
    font-family: Georgia, serif;
    line-height: 1;
    margin: 0.2em 0;
}

.phonogram-sounds {
    font-size: 14pt;
    color: #2a5c8a;
    font-family: "Courier New", monospace;
    margin-top: 0.4em;
}

.sound { font-family: "Courier New", monospace; }
.sound::before { content: "/"; }
.sound::after { content: "/"; }

.word-list {
    font-family: "Courier New", monospace;
    font-size: 13pt;
}

.rule-badge {
    display: inline-block;
    background: #2a5c8a;
    color: white;
    border-radius: 3px;
    padding: 2pt 6pt;
    font-size: 9pt;
    font-weight: bold;
    margin-right: 4pt;
}

.step {
    margin: 1em 0;
    padding: 0.8em 1em;
    background: #f7f7f2;
    border-radius: 4px;
    page-break-inside: avoid;
}

.step-num {
    font-weight: bold;
    color: #2a5c8a;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Reader layout: two-column with sidebar */
.reader-page {
    display: flex;
    gap: 1em;
    page-break-after: always;
}
.reader-text {
    flex: 3;
}
.reader-sidebar {
    flex: 1;
    background: #f7f7f2;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 0.8em;
    font-size: 11pt;
}
.reader-sidebar h3 {
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0;
}

/* Warm-up box */
.warmup-box {
    background: #eef6ff;
    border: 1px solid #b8d4f0;
    border-radius: 6px;
    padding: 0.8em 1em;
    margin-bottom: 1em;
    page-break-inside: avoid;
}
.warmup-box .title {
    font-weight: bold;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #2a5c8a;
}

/* Image placeholder */
.img-placeholder {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 2em 1em;
    text-align: center;
    color: #999;
    font-style: italic;
    font-size: 11pt;
    margin: 1em 0;
    page-break-inside: avoid;
}
.img-placeholder .alt-text {
    font-weight: bold;
    color: #666;
    display: block;
    margin-bottom: 0.3em;
}
.img-placeholder .filename {
    font-family: "Courier New", monospace;
    font-size: 9pt;
    color: #aaa;
}

.page-break { page-break-before: always; }
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_image_path(src: str, md_file: Path) -> Path:
    """Resolve an image src relative to the markdown file or project root."""
    p = Path(src)
    if p.is_absolute():
        return p
    # Try relative to the markdown file first
    candidate = md_file.parent / p
    if candidate.exists():
        return candidate
    # Try relative to project root
    candidate = PROJECT_ROOT / p
    return candidate


def md_to_html(md_text: str, md_file: Path) -> str:
    """Convert markdown to HTML, handling image placeholders."""
    # Pre-convert markdown images to HTML img tags so they work inside HTML divs
    import re as _re
    md_text = _re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', md_text)
    
    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite", "toc", "md_in_html"],
    )
    # Wrap images that don't exist in placeholder divs
    import re
    def img_replacer(match):
        src = match.group(2)
        alt = match.group(1)
        img_path = resolve_image_path(src, md_file)
        if img_path.exists():
            return match.group(0)
        else:
            return (
                f'<div class="img-placeholder">'
                f'<span class="alt-text">{alt}</span>'
                f'<span class="filename">{src}</span>'
                f'<span>Image not yet generated — replace with real PNG</span>'
                f'</div>'
            )
    html = re.sub(r'<img\s+alt="([^"]*)"\s+src="([^"]*)".*?>', img_replacer, html)
    return html


def render_md_to_pdf(md_path: Path, output_path: Path, doc_type: str = "lesson"):
    """Render a single markdown file to PDF."""
    md_text = md_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_text, md_path)

    # Determine body class
    body_class = ""
    if doc_type == "worksheet":
        body_class = ' class="worksheet"'
    elif doc_type == "reader":
        body_class = ' class="reader"'

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>{PAGE_CSS}</style>
</head>
<body{body_class}>
{body_html}
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=full_html).write_pdf(str(output_path))
    print(f"  OK {output_path.relative_to(PROJECT_ROOT)}")


def get_lessons_for_stage(stage: int) -> list[dict]:
    """Return all lesson entries for a given stage from the catalog."""
    lessons = []
    with open(CATALOG_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["stage"]) == stage:
                lessons.append(row)
    return lessons


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_render_single(md_path_str: str):
    md_path = Path(md_path_str).resolve()
    if not md_path.exists():
        print(f"Error: file not found: {md_path}")
        sys.exit(1)
    output_path = md_path.with_suffix(".pdf")
    # Detect type
    doc_type = "lesson"
    if "worksheets" in str(md_path):
        doc_type = "worksheet"
    elif "readers" in str(md_path):
        doc_type = "reader"
    print(f"Rendering: {md_path.relative_to(PROJECT_ROOT)}")
    render_md_to_pdf(md_path, output_path, doc_type)


def cmd_render_stage(stage: int):
    lessons = get_lessons_for_stage(stage)
    print(f"Rendering Stage {stage}: {len(lessons)} lessons")
    for lesson in lessons:
        lesson_id = lesson["lesson_id"]
        stage_dir = LESSONS_DIR / f"stage-{stage}"
        md_path = stage_dir / f"{lesson_id}.md"
        if md_path.exists():
            output_path = BUILD_DIR / f"stage-{stage}" / f"{lesson_id}.pdf"
            render_md_to_pdf(md_path, output_path)
        else:
            print(f"  MISSING: {md_path.relative_to(PROJECT_ROOT)} (run generate.py first)")


def cmd_render_all():
    for stage in range(1, 6):
        cmd_render_stage(stage)


def cmd_render_curriculum():
    md_path = PROJECT_ROOT / "curriculum.md"
    output_path = BUILD_DIR / "curriculum.pdf"
    print(f"Rendering full curriculum...")
    render_md_to_pdf(md_path, output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Render Logic of English lessons to PDF")
    parser.add_argument("file", nargs="?", help="Single markdown file to render")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5], help="Render all lessons in a stage")
    parser.add_argument("--all", action="store_true", help="Render all lessons (all stages)")
    parser.add_argument("--curriculum", action="store_true", help="Render curriculum.md to PDF")
    args = parser.parse_args()

    if args.file:
        cmd_render_single(args.file)
    elif args.stage:
        cmd_render_stage(args.stage)
    elif args.all:
        cmd_render_all()
    elif args.curriculum:
        cmd_render_curriculum()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
