#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
render.py — Convert Logic of English lesson markdown files to printable PDF.

Usage:
    python render.py lessons/stage-1/002-phonogram-a.md
    python render.py --stage 2
    python render.py --all
    python render.py --curriculum
    python render.py --stage 2 --jobs 4          # parallel render

Output:
    Same directory as source, with .pdf extension.
    Stage/curriculum renders go to build/ directory.
"""

import argparse
import csv
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

# Ensure framework package is importable when called as `python render.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_log import (
    get_logger,
    phase,
    Progress,
    WorkerLogQueue,
    set_worker_queue,
    attach_worker_handler,
    drain_worker_queue,
)

log = get_logger("render")

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

# Atkinson Hyperlegible (Braille Institute, 2019) — exaggerated character
# distinctiveness (b/d, 1/I/l, O/Q) makes it ideal for early readers.
# All weights embedded as @font-face so WeasyPrint can resolve locally.
PAGE_CSS = """
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("framework/fonts/AtkinsonHyperlegible-Regular.ttf") format("truetype");
    font-weight: 400;
    font-style: normal;
}
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("framework/fonts/AtkinsonHyperlegible-Italic.ttf") format("truetype");
    font-weight: 400;
    font-style: italic;
}
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("framework/fonts/AtkinsonHyperlegible-Bold.ttf") format("truetype");
    font-weight: 700;
    font-style: normal;
}
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("framework/fonts/AtkinsonHyperlegible-BoldItalic.ttf") format("truetype");
    font-weight: 700;
    font-style: italic;
}

/* Color palette — WCAG AA verified against cream background (#fffff8).
   Always pair color with weight/shape — never color-only. */
:root {
    --ink: #111111;        /* 18.8:1  body text */
    --accent: #2a5c8a;     /*  8.2:1  headings / consonant fallback */
    --vowel: #a8421a;      /*  5.7:1  vowels (rust) */
    --consonant: #2a7d2a;  /*  5.3:1  consonants (green) */
    --warn: #b8860b;       /*  4.6:1  caution — large text only */
    --muted: #555555;      /*  7.4:1  captions */
    --bg: #fffff8;         /* off-white */
    --card-bg: #f7f7f2;
    --rule-line: #dddddd;
    --warmup-bg: #eef6ff;
    --warmup-border: #b8d4f0;
}

@page {
    size: letter;
    margin: 0.75in 0.75in 0.9in 0.75in;
    @bottom-center {
        content: counter(page);
        font-family: "Atkinson Hyperlegible", sans-serif;
        font-size: 9pt;
        color: #888;
    }
}

@page worksheet {
    size: letter;
    margin: 0.5in;
}

body {
    font-family: "Atkinson Hyperlegible", Georgia, "Times New Roman", serif;
    font-size: 14pt;
    line-height: 1.7;
    color: var(--ink);
    background: var(--bg);
    orphans: 3;
    widows: 3;
}

body.worksheet {
    font-size: 12pt;
    line-height: 1.55;
}

body.reader {
    font-size: 20pt;
    line-height: 1.8;
}

/* Age-graded per-stage sizing. Stages 1-2 (4-7yo) get the largest text;
   sizes step down through the curriculum as readers gain fluency. */
body.stage-1, body.stage-1.worksheet { font-size: 19pt; line-height: 1.8; }
body.stage-2, body.stage-2.worksheet { font-size: 17pt; line-height: 1.7; }
body.stage-3, body.stage-3.worksheet { font-size: 15pt; line-height: 1.65; }
body.stage-4, body.stage-4.worksheet { font-size: 14pt; line-height: 1.6; }
body.stage-5, body.stage-5.worksheet { font-size: 13pt; line-height: 1.55; }
body.stage-1.reader { font-size: 22pt; }
body.stage-2.reader { font-size: 20pt; }
body.stage-3.reader { font-size: 18pt; line-height: 1.7; }
body.stage-4.reader { font-size: 16pt; line-height: 1.6; }
body.stage-5.reader { font-size: 15pt; line-height: 1.55; }

h1 {
    font-size: 24pt;
    margin-top: 0;
    page-break-before: avoid;
    break-after: avoid;
    color: var(--ink);
    letter-spacing: -0.01em;
}
h2 {
    font-size: 17pt;
    color: var(--accent);
    page-break-after: avoid;
    break-after: avoid;
    margin-top: 1.4em;
    border-bottom: 1px solid var(--rule-line);
    padding-bottom: 0.2em;
}
h3 {
    font-size: 13pt;
    page-break-after: avoid;
    break-after: avoid;
    color: #333;
    margin-top: 1.2em;
}

p { margin: 0.5em 0; }

a {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid var(--accent);
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 11pt;
    break-inside: avoid;
}
th, td {
    border-bottom: 1px solid var(--rule-line);
    padding: 6pt 8pt;
    text-align: left;
    vertical-align: top;
}
th {
    font-weight: bold;
    border-bottom-width: 2px;
    background: var(--card-bg);
    color: var(--accent);
}

/* Color-coded phonograms. Vowels → rust, consonants → green.
   Always bold + colored (never color-only) for color-blind safety. */
.phonogram {
    font-size: 72pt;
    font-weight: bold;
    color: var(--accent);
    text-align: center;
    display: block;
    margin: 1em 0;
    font-family: "Atkinson Hyperlegible", sans-serif;
    line-height: 1.1;
    border: 2px solid var(--accent);
    border-radius: 8px;
    padding: 0.4em;
    background: var(--bg);
    page-break-inside: avoid;
    break-inside: avoid;
}
.phonogram.vowel,
.phonogram-card.vowel,
.phonogram-letter.vowel {
    color: var(--vowel);
    border-color: var(--vowel);
    background: #fdf4ec;
}
.phonogram.consonant,
.phonogram-card.consonant,
.phonogram-letter.consonant {
    color: var(--consonant);
    border-color: var(--consonant);
    background: #ecf6ec;
}

.phonogram-card {
    border: 2px solid var(--accent);
    border-radius: 8px;
    padding: 1.2em 1.5em;
    margin: 1.5em 0;
    text-align: center;
    background: var(--bg);
    page-break-inside: avoid;
    break-inside: avoid;
}

.phonogram-letter {
    font-size: 72pt;
    font-weight: bold;
    color: var(--accent);
    font-family: "Atkinson Hyperlegible", sans-serif;
    line-height: 1;
    margin: 0.2em 0;
}

.phonogram-sounds {
    font-size: 14pt;
    color: var(--accent);
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
    background: var(--accent);
    color: white;
    border-radius: 3px;
    padding: 2pt 6pt;
    font-size: 9pt;
    font-weight: bold;
    margin-right: 4pt;
    font-family: "Atkinson Hyperlegible", sans-serif;
}

.step {
    margin: 1em 0;
    padding: 0.8em 1em;
    background: var(--card-bg);
    border-radius: 4px;
    page-break-inside: avoid;
    break-inside: avoid;
}

.step-num {
    font-weight: bold;
    color: var(--accent);
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Constrain images so they don't blow up to full-page size in print. */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0.5em auto;
}

/* Reader layout: two-column with sidebar */
.reader-page {
    display: flex;
    gap: 1em;
    page-break-after: always;
    break-after: page;
}
.reader-text {
    flex: 3;
}
.reader-sidebar {
    flex: 1;
    background: var(--card-bg);
    border: 1px solid var(--rule-line);
    border-radius: 6px;
    padding: 0.8em;
    font-size: 11pt;
}
.reader-sidebar h3 {
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0;
    color: var(--accent);
}

/* Warm-up box */
.warmup-box {
    background: var(--warmup-bg);
    border: 1px solid var(--warmup-border);
    border-radius: 6px;
    padding: 0.8em 1em;
    margin-bottom: 1em;
    page-break-inside: avoid;
    break-inside: avoid;
}
.warmup-box .title {
    font-weight: bold;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
}

/* Callout box — used for "Did you know?" sidebars etc. */
.callout {
    background: var(--card-bg);
    border-left: 4px solid var(--accent);
    border-radius: 4px;
    padding: 0.8em 1em;
    margin: 1em 0;
    page-break-inside: avoid;
    break-inside: avoid;
}
.callout.warn { border-left-color: var(--warn); }
.callout.vowel { border-left-color: var(--vowel); }
.callout.consonant { border-left-color: var(--consonant); }

/* Handwriting-rule paper (repeating gradient — infinitely scalable). */
.rule-paper {
    background-image: repeating-linear-gradient(
        transparent,
        transparent 23pt,
        var(--rule-line) 23pt,
        var(--rule-line) 24pt
    );
    min-height: 24pt;
    margin: 0.5em 0;
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
    break-inside: avoid;
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

.page-break { page-break-before: always; break-before: page; }
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
    # Pre-convert markdown images to HTML img tags so they work inside HTML divs.
    # Empty alt (alt="") marks images as decorative — screen readers and pdftotext
    # skip them, so image captions don't bleed into extracted text.
    # Also rewrite image src to be relative to PROJECT_ROOT so images resolve
    # regardless of where the markdown file lives.
    import re as _re
    def _rewrite_img_src(match):
        src = match.group(2)
        alt = match.group(1)
        if not src.startswith(('http://', 'https://', '/', 'data:')):
            # Try resolving relative to markdown file first, then fall back to PROJECT_ROOT
            # (source MDs often assume images are at project root even when MD lives in a subdir).
            candidate = (md_file.parent / src).resolve()
            if not candidate.exists():
                alt_candidate = (PROJECT_ROOT / src).resolve()
                if alt_candidate.exists():
                    candidate = alt_candidate
                else:
                    # Neither location has the file — keep original src AND alt so
                    # the downstream img_replacer can render a "missing image"
                    # placeholder with the alt text intact.
                    return f'<img src="{src}" alt="{alt}" />'
            try:
                rel = candidate.relative_to(PROJECT_ROOT)
                src = str(rel).replace('\\', '/')
            except ValueError:
                pass
            # Image exists — empty alt marks it as decorative so pdftotext doesn't
            # dump the alt into extracted text (see handoff notes for #11).
            return f'<img src="{src}" alt="" />'
        return f'<img src="{src}" alt="{alt}" />'
    md_text = _re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _rewrite_img_src, md_text)

    # python-markdown treats HTML block elements as opaque by default — markdown
    # inside <div class="reader-sidebar"> etc. would pass through as raw text.
    # Split on div boundaries, convert each chunk separately, reassemble.
    md = markdown.Markdown(extensions=["tables", "fenced_code", "codehilite", "toc", "md_in_html"])
    parts = _re.split(r'(</?div[^>]*>)', md_text)
    chunks = []
    for part in parts:
        md.reset()
        chunks.append(md.convert(part))
    html = ''.join(chunks)
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
    # Match either attribute order (markdown renders src then alt; some authors use alt then src).
    # img_replacer expects (alt, src) so the second pattern swaps via a wrapper that
    # returns full match for group(0) and the swapped values for group(1)/(2).
    def _swap(m):
        return img_replacer(m) if False else (
            img_replacer(type('M', (), {
                'group': lambda self, i, _m=m: (
                    _m.group(0) if i == 0
                    else (_m.group(2) if i == 1 else _m.group(1))
                ),
            })())
        )
    html = re.sub(r'<img[^>]*\salt="([^"]*)"[^>]*\bsrc="([^"]*)"[^>]*>', img_replacer, html)
    html = re.sub(r'<img[^>]*\bsrc="([^"]*)"[^>]*\salt="([^"]*)"[^>]*>', _swap, html)
    return html


def _stage_from_path(md_path: Path) -> int | None:
    """Detect stage (1-5) from 'lessons/stage-N/' or 'worksheets/stage-N/' segments."""
    for part in md_path.parts:
        m = __import__("re").match(r"stage-([1-5])$", part)
        if m:
            return int(m.group(1))
    return None


def render_md_to_pdf(md_path: Path, output_path: Path, doc_type: str = "lesson"):
    """Render a single markdown file to PDF.

    Safe to call from a worker process — imports are lazy, no shared state.

    Args:
        md_path: Path to the markdown source.
        output_path: Path where the PDF will be written.
        doc_type: 'lesson' (default), 'worksheet', or 'reader' — selects
            page sizing + body class.
    """
    # Lazy weasyprint import: this is expensive (~1-2s) and we only want
    # to pay the cost when actually rendering, not at module import time.
    from weasyprint import HTML

    md_text = md_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_text, md_path)

    # Compose body classes: doc-type + per-stage age-graded sizing.
    classes = []
    if doc_type == "worksheet":
        classes.append("worksheet")
    elif doc_type == "reader":
        classes.append("reader")
    stage = _stage_from_path(md_path)
    if stage is not None:
        classes.append(f"stage-{stage}")
    body_class_attr = f' class="{" ".join(classes)}"' if classes else ""

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>{PAGE_CSS}</style>
</head>
<body{body_class_attr}>
{body_html}
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # base_url=PROJECT_ROOT so rewritten image paths like 'images/foo.png' resolve
    # regardless of where the markdown file lives.
    HTML(string=full_html, base_url=str(PROJECT_ROOT) + "/").write_pdf(str(output_path))
    try:
        rel = output_path.relative_to(PROJECT_ROOT)
    except ValueError:
        rel = output_path  # outside project tree (e.g. tests)
    log.info(f"  OK {rel}")


def _render_worker(md_path_str: str, output_path_str: str, doc_type: str) -> str:
    """Worker entry point for ProcessPoolExecutor.

    Takes only strings (Path objects don't pickle cleanly across processes
    on Windows spawn). Returns the relative output path on success.
    """
    worker_log = get_logger("render.worker")
    attach_worker_handler(worker_log)
    try:
        render_md_to_pdf(Path(md_path_str), Path(output_path_str), doc_type)
        return output_path_str
    except Exception as exc:
        worker_log.error(f"FAIL {md_path_str}: {exc}", exc_info=True)
        raise


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
        log.error(f"file not found: {md_path}")
        sys.exit(1)
    output_path = md_path.with_suffix(".pdf")
    # Detect type
    doc_type = "lesson"
    if "worksheets" in str(md_path):
        doc_type = "worksheet"
    elif "readers" in str(md_path):
        doc_type = "reader"
    log.info(f"Rendering: {md_path}")
    render_md_to_pdf(md_path, output_path, doc_type)


def _collect_render_jobs(stage: int | None = None) -> list[tuple[Path, Path, str]]:
    """Enumerate (md_path, pdf_path, doc_type) for the requested scope.

    For stage=all (stage=None), iterate all 5 stages. Missing MDs are skipped
    with a logged warning — caller decides whether to fail.
    """
    jobs: list[tuple[Path, Path, str]] = []
    stages = range(stage, stage + 1) if stage else range(1, 6)
    for s in stages:
        for lesson in get_lessons_for_stage(s):
            md_path = LESSONS_DIR / f"stage-{s}" / f"{lesson['lesson_id']}.md"
            if not md_path.exists():
                log.warning(f"MISSING: {md_path.relative_to(PROJECT_ROOT)} (run generate.py first)")
                continue
            pdf_path = BUILD_DIR / f"stage-{s}" / f"{lesson['lesson_id']}.pdf"
            jobs.append((md_path, pdf_path, "lesson"))
    return jobs


def _run_parallel_jobs(
    jobs: list[tuple[Path, Path, str]],
    jobs_arg: int,
    label: str,
) -> tuple[int, int]:
    """Dispatch jobs to a process pool. Returns (ok_count, fail_count)."""
    if not jobs:
        return 0, 0

    n_workers = max(1, jobs_arg)
    queue = WorkerLogQueue()
    set_worker_queue(queue)

    log.info(f"{label}: {len(jobs)} files, {n_workers} workers")
    ok = 0
    fail = 0

    with Progress(label, total=len(jobs)) as progress:
        # spawn is required on Windows; default is fine on Linux/macOS.
        executor = ProcessPoolExecutor(max_workers=n_workers)
        try:
            futures = {
                executor.submit(_render_worker, str(md), str(pdf), dtype): (md, pdf)
                for md, pdf, dtype in jobs
            }
            for fut in as_completed(futures):
                drain_worker_queue(queue, log)
                md, _pdf = futures[fut]
                try:
                    fut.result()
                    ok += 1
                except Exception as exc:
                    log.error(f"FAIL {md}: {exc}")
                    fail += 1
                progress.tick()
                drain_worker_queue(queue, log)
        finally:
            executor.shutdown(wait=True)
            set_worker_queue(None)

    log.info(f"{label}: {ok} ok, {fail} failed")
    return ok, fail


def cmd_render_stage(stage: int, jobs: int = 1):
    phase(f"Render Stage {stage}")
    jobs_list = _collect_render_jobs(stage)
    log.info(f"Rendering Stage {stage}: {len(jobs_list)} lessons")
    ok, fail = _run_parallel_jobs(jobs_list, jobs, f"render-stage-{stage}")
    if fail:
        sys.exit(1)


def cmd_render_all(jobs: int = 1):
    phase("Render All Lessons")
    jobs_list = _collect_render_jobs()
    log.info(f"Rendering all {len(jobs_list)} lessons")
    ok, fail = _run_parallel_jobs(jobs_list, jobs, "render-all")
    if fail:
        sys.exit(1)


def cmd_render_curriculum():
    phase("Render Curriculum")
    md_path = PROJECT_ROOT / "curriculum.md"
    output_path = BUILD_DIR / "curriculum.pdf"
    log.info("Rendering full curriculum...")
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
    parser.add_argument(
        "--jobs", "-j", type=int, default=1,
        help="Parallel worker processes (default: 1 = serial). Stage/all only.",
    )
    args = parser.parse_args()

    if args.file:
        cmd_render_single(args.file)
    elif args.stage:
        cmd_render_stage(args.stage, jobs=args.jobs)
    elif args.all:
        cmd_render_all(jobs=args.jobs)
    elif args.curriculum:
        cmd_render_curriculum()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
