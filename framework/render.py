#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
render.py — Convert Logic of English lesson markdown files to printable PDF.

Usage:
    python render.py lessons/stage-1/002-phonogram-a.md
    python render.py --stage 2
    python render.py --all --jobs 4              # parallel render
    python render.py --all --skip-existing       # incremental (skip up-to-date PDFs)
    python render.py --curriculum

Output:
    Same directory as source, with .pdf extension.
    Stage/curriculum renders go to build/ directory.

Incremental builds:
    Use --skip-existing to skip PDFs whose mtime is newer than the source MD.
    Safe for iteration: edit a few MDs, re-run, only changed lessons re-render.
    Default jobs=4 — override with --jobs N or set jobs env var.
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

# Issue #24: single source of truth for build version. Read VERSION at
# import time and inject into PAGE_CSS so the page-1 footer carries it.
# We read the file directly to avoid an import-cycle dependency on the
# framework.version module being importable (render.py is invoked both as
# `python render.py` and `python -m framework.render`).
_VERSION = (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip()
_FOOTER_TEXT = f"OpenPhonograms v{_VERSION} \u00b7 MIT licensed"

# Per-stage title for running header on every lesson page.
STAGE_TITLES = {
    1: "Phonemic Awareness & First Phonograms",
    2: "Short Vowels & Multi-Letter Phonograms",
    3: "Silent E & Vowel Teams",
    4: "Schwa, Suffixing & Morphology",
    5: "Roots, Fluency & Composition",
}
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
    /* Issue #24: pages 2+ get no footer; only the first page does. */
    @bottom-left { content: ""; }
}

/* Issue #24: page-1-only version footer. */
@page :first {
    @bottom-left {
        content: "FOOTER_FNORD";
        font-family: "Atkinson Hyperlegible", sans-serif;
        font-size: 7pt;
        color: #aaa;
    }
}

@page worksheet {
    size: letter;
    margin: 0.5in;
    @bottom-center {
        content: counter(page);
        font-family: "Atkinson Hyperlegible", sans-serif;
        font-size: 9pt;
        color: #888;
    }
    @bottom-left { content: ""; }
}

@page worksheet :first {
    @bottom-left {
        content: "FOOTER_FNORD";
        font-family: "Atkinson Hyperlegible", sans-serif;
        font-size: 7pt;
        color: #aaa;
    }
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

/* ── Density classes ──────────────────────────────────────────────────
   Teacher-facing and admin material should be dense (smaller fonts,
   tighter line-height). Use these as wrappers or body classes.

   In a lesson MD:
     <details class="teacher-script">    — collapsible adult content
     <div class="teacher-only">           — non-collapsible adult content
     <div class="reference-card">         — single-page reference cards

   On the body for fully-admin docs:
     body.administrative   — nav PDFs (start-here, scope, index)
     body.handbook         — stage handbooks (dense teacher binder)
     body.index            — master index / TOC

   Combined with stage (e.g. lesson in a stage-2 pack rendered inline
   inside a stage-2 handbook), the body.handbook font wins. */
.teacher-script {
    font-size: 11pt;
    line-height: 1.35;
    color: #333;
    background: #fafaf6;
    border-left: 3px solid #888;
    padding: 0.6em 0.9em;
    margin: 0.8em 0;
    border-radius: 0 4px 4px 0;
    page-break-inside: auto;
}
.teacher-script > summary {
    font-weight: bold;
    font-size: 12pt;
    color: var(--accent);
    margin-bottom: 0.4em;
    list-style: none;
}
.teacher-script > summary::-webkit-details-marker { display: none; }
.teacher-script > summary::before {
    content: "📖 ";
    margin-right: 0.3em;
}
.teacher-script > summary::after {
    content: " — Teacher Script";
    font-weight: normal;
    font-style: italic;
    color: #666;
    font-size: 10pt;
}
.teacher-script h1, .teacher-script h2, .teacher-script h3 {
    color: var(--accent);
    margin: 0.6em 0 0.3em;
}
.teacher-script h2 { font-size: 13pt; border-bottom: 1px solid #ddd; }
.teacher-script h3 { font-size: 11pt; }
.teacher-script p { margin: 0.3em 0; }
.teacher-script ul, .teacher-script ol { margin: 0.3em 0 0.3em 1.5em; }
.teacher-script table { font-size: 10pt; margin: 0.4em 0; }
.teacher-script .phonogram { font-size: 36pt; margin: 0.3em 0; padding: 0.2em; }

.teacher-only {
    font-size: 11pt;
    line-height: 1.4;
    color: #444;
    border-left: 2px solid #c8c8c8;
    padding: 0.4em 0.8em;
    margin: 0.6em 0;
    background: #fefefa;
}

.reference-card {
    /* A printable take-home card. Compact, single-page. */
    font-size: 12pt;
    line-height: 1.4;
    border: 2px solid var(--accent);
    border-radius: 8px;
    padding: 0.8em 1em;
    margin: 0.5em 0;
    page-break-inside: avoid;
}
.reference-card h1, .reference-card h2, .reference-card h3 {
    color: var(--accent);
    margin: 0.3em 0;
}
.reference-card h1 { font-size: 22pt; }
.reference-card h2 { font-size: 14pt; border-bottom: 1px solid #ddd; }
.reference-card h3 { font-size: 11pt; }
.reference-card .phonogram,
.reference-card .phonogram-letter {
    font-size: 48pt;
    margin: 0.2em 0;
    padding: 0.2em;
}

body.administrative {
    font-size: 10pt;
    line-height: 1.4;
    color: var(--ink);
}
body.administrative h1 { font-size: 18pt; margin-top: 0; }
body.administrative h2 { font-size: 13pt; margin-top: 1em; }
body.administrative h3 { font-size: 11pt; }
body.administrative p { margin: 0.3em 0; }
body.administrative table { font-size: 9pt; margin: 0.5em 0; }
body.administrative ul, body.administrative ol { margin: 0.2em 0 0.2em 1.5em; }
body.administrative .phonogram { font-size: 36pt; }

body.handbook {
    font-size: 11pt;
    line-height: 1.4;
    color: var(--ink);
}
body.handbook h1 { font-size: 18pt; margin-top: 0; }
body.handbook h2 { font-size: 13pt; margin-top: 1em; }
body.handbook h3 { font-size: 11pt; }
body.handbook p { margin: 0.3em 0; }
body.handbook table { font-size: 10pt; margin: 0.5em 0; }
body.handbook .phonogram { font-size: 48pt; }
body.handbook .phonogram-letter { font-size: 56pt; }
body.handbook .teacher-script { font-size: 10pt; padding: 0.4em 0.7em; }

body.index {
    font-size: 9pt;
    line-height: 1.35;
    color: var(--ink);
}
body.index h1 { font-size: 16pt; margin-top: 0; }
body.index h2 { font-size: 11pt; margin-top: 0.8em; }
body.index h3 { font-size: 10pt; }
body.index p { margin: 0.2em 0; }
body.index table { font-size: 8pt; margin: 0.3em 0; }
body.index ul, body.index ol { margin: 0.1em 0 0.1em 1.2em; }

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

/* Constrain images so they do not blow up to full-page size in print. */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0.5em auto;
}

/* Reader cover page: distinct visual treatment so the reader is easy to
   identify on a shelf. See issue #19. */

/* Branded cover header (logo + class tagline) — used by handbook, lesson
   pack, certificate, navigation, and any other cover. See issue #15. */
.brand-cover {
    text-align: center;
    padding: 1.5em 1em 1em 1em;
    border-bottom: 3px solid #2a5c8a;
    margin-bottom: 1em;
}
.brand-cover img,
.brand-cover svg {
    max-width: 280px;
    height: auto;
    margin: 0 auto 0.5em auto;
    display: block;
}
.brand-cover .tagline {
    font-family: Georgia, serif;
    font-size: 11pt;
    color: #4a7caa;
    font-style: italic;
    letter-spacing: 0.05em;
}

.reader .reader-cover {
    text-align: center;
    padding: 2.5em 1.5em;
    border: 3px solid #2a5c8a;
    border-radius: 12px;
    margin: 1em auto;
    max-width: 85%;
    page-break-after: always;
    break-after: page;
}
.reader .reader-cover h1 {
    font-size: 36pt;
    color: #2a5c8a;
    margin: 0.3em 0 0.2em 0;
    border-bottom: 2px solid #2a5c8a;
    padding-bottom: 0.2em;
}
.reader .reader-cover p {
    color: #444;
    font-size: 12pt;
    margin: 0.4em 0;
}

/* Reader layout: two-column with sidebar. The forced page break on
   .reader-page is scoped under .reader body class so lesson HTML can't
   accidentally trigger it (see issue #26). Sub-elements (text/sidebar)
   carry no page-break risk and remain unscoped. */
.reader .reader-page {
    display: flex;
    gap: 1em;
    page-break-after: always;
    break-after: page;
}
/* Reader H2 ("Page N") widow-protection: scoped override so the global
   H2 widow rules don't force the "Page N" header onto its own page when
   the prior .reader-page ends near a page boundary.

   Root cause (see issue #52):
     - The cover or prior .reader-page has `page-break-after: always`,
       forcing a fresh page after it.
     - The H2 inherits `page-break-after: avoid` from the global rule.
     - When H2 + warmup-box + .reader-page don't fit on the new page,
       WeasyPrint honors `avoid` by moving the WHOLE H2 group to the next
       page, leaving the freshly-broken page empty.
     - Conversely on subsequent pages, H2 + a tall .reader-page can't
       share the page, so H2 stays alone.

   Override: allow breaks before AND after H2 inside .reader so the H2
   can stand alone on its own page (forced by the prior element's
   page-break-after:always) and the rest of the page content follows on
   the next page. See issue #52. */
.reader h2 {
    page-break-before: auto;
    page-break-after: auto;
    break-before: auto;
    break-after: auto;
}
/* Reader warmup-box: allow it to split across pages inside .reader so it
   doesn't force the H2 + warmup-box + .reader-page block onto a single
   (impossibly tall) page. Without this, the unbreakable warmup-box stranding
   creates the "Page N" orphan page. The visual cost is minimal: the
   warmup-box is short enough to either fit on a page or split cleanly.
   See issue #52. */
.reader .warmup-box {
    page-break-inside: auto;
    break-inside: auto;
}
/* Reader .reader-page: prefer to flow with the preceding H2 "Page N" so the
   H2 doesn't orphan on its own page when the reader-page is tall enough
   to push the H2 onto a separate page. We honor the explicit
   `<div class="page-break">` markers in hand-crafted MDs (stage-1) by
   keeping `page-break-after: always` on those. For taller reader-pages
   (e.g. stage-2+ with sidebars), set break-before: auto so the prior H2
   can travel with the page top via standard flow.
   See issue #52. */
/* (removed: the .reader .reader-page break-before override did not help
   with the H2-orphan issue and is left out for now. The H2 + warmup-box
   overrides are sufficient for the hand-crafted stage-1/2 readers.) */
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
""".replace("FOOTER_FNORD", _FOOTER_TEXT)

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

    # Inject "Printable pack" callout for lesson files. See issue #11.
    # Adds a small box at the bottom of every lesson page with the path to
    # the matching lesson pack PDF (the printable bundle). Clickable relative
    # link works in PDF readers that support internal+external PDF refs.
    if "lessons" in str(md_file).replace("\\", "/") and "/stage-" in str(md_file).replace("\\", "/"):
        pack_match = re.search(r"lessons/stage-(\d+)/([a-z0-9\-]+)\.md$", str(md_file).replace("\\", "/"))
        if pack_match:
            stage_n = pack_match.group(1)
            lesson_slug = pack_match.group(2)
            pack_path = f"../../packs/stage-{stage_n}/{lesson_slug}.pdf"
            callout = (
                f'<div class="lesson-pack-callout" style="margin-top: 1em; padding: 0.6em 0.8em; background: #f4f1e8; border-left: 4px solid #2a5c8a; font-size: 10pt;">'
                f'<strong>\U0001f4c4 Printable pack:</strong> '
                f'<a href="{pack_path}" style="color: #2a5c8a; text-decoration: none; font-weight: 600;">packs/stage-{stage_n}/{lesson_slug}.pdf</a>'
                f' &mdash; lesson + worksheet + flash cards'
                f'</div>'
            )
            html += callout

    return html


def _stage_from_path(md_path: Path) -> int | None:
    """Detect stage (1-5) from 'lessons/stage-N/' or 'worksheets/stage-N/' segments."""
    for part in md_path.parts:
        m = __import__("re").match(r"stage-([1-5])$", part)
        if m:
            return int(m.group(1))
    return None


def render_md_to_pdf(md_path: Path, output_path: Path, doc_type: str = "lesson", body_class: str | None = None):
    """Render a single markdown file to PDF.

    Safe to call from a worker process — imports are lazy, no shared state.

    Args:
        md_path: Path to the markdown source.
        output_path: Path where the PDF will be written.
        doc_type: 'lesson' (default), 'worksheet', or 'reader' — selects
            page sizing + body class.
        body_class: Optional explicit body class to override detection,
            e.g. 'administrative', 'handbook', 'index'. Used by
            navigation/handbook generators that don't want per-stage sizing.
    """
    # Lazy weasyprint import: this is expensive (~1-2s) and we only want
    # to pay the cost when actually rendering, not at module import time.
    from weasyprint import HTML

    md_text = md_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_text, md_path)

    # Compose body classes: doc-type + per-stage age-graded sizing,
    # OR an explicit body_class override (admin/handbook/index).
    classes = []
    if body_class:
        # explicit override wins (e.g. 'administrative', 'handbook', 'index')
        classes.append(body_class)
    else:
        if doc_type == "worksheet":
            classes.append("worksheet")
        elif doc_type == "reader":
            classes.append("reader")
        stage = _stage_from_path(md_path)
        if stage is not None:
            classes.append(f"stage-{stage}")
    body_class_attr = f' class="{" ".join(classes)}"' if classes else ""
    body_style_attr = ""

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
        rel = output_path
    log.info(f"  OK {rel}")


def render_html_to_pdf(html: str, output_path: Path, body_class: str | None = None) -> None:
    """Render a complete HTML string to PDF with PAGE_CSS injected.

    Use for non-markdown artifacts (certificates, indexes, placement tests,
    quick checks) that already have their own HTML+inline CSS. This wrapper
    ensures the unified @page CSS, font, and footer treatment are applied.

    The caller's HTML must include <!DOCTYPE html><html><head>...<style>...</style></head>
    so this function only injects PAGE_CSS into the <style> tag.
    If the caller's HTML has its own <style>, this function merges by
    prepending PAGE_CSS to the existing <style> content.
    """
    from weasyprint import HTML as WHTML

    # Inject PAGE_CSS into the caller's <style> block (or create one)
    if "<style>" in html and "</style>" in html:
        html = html.replace("<style>", f"<style>{PAGE_CSS}\n", 1)
    else:
        # No <style> tag — inject one into <head>
        if "<head>" in html:
            html = html.replace("<head>", f"<head><style>{PAGE_CSS}</style>", 1)
        else:
            html = html.replace("<html>", f"<html><head><style>{PAGE_CSS}</style></head>", 1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    WHTML(string=html, base_url=str(PROJECT_ROOT) + "/").write_pdf(str(output_path))
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


def _collect_render_jobs(
    stage: int | None = None,
    skip_existing: bool = False,
) -> list[tuple[Path, Path, str]]:
    """Enumerate (md_path, pdf_path, doc_type) for the requested scope.

    For stage=all (stage=None), iterate all 5 stages. Missing MDs are skipped
    with a logged warning — caller decides whether to fail.

    When skip_existing=True, PDFs newer than their source MD are dropped
    from the job list (incremental build). The PDF's mtime is compared
    against the MD's mtime — a PDF is "fresh" if pdf_mtime >= md_mtime.
    """
    jobs: list[tuple[Path, Path, str]] = []
    skipped = 0
    stages = range(stage, stage + 1) if stage else range(1, 6)
    for s in stages:
        for lesson in get_lessons_for_stage(s):
            md_path = LESSONS_DIR / f"stage-{s}" / f"{lesson['lesson_id']}.md"
            if not md_path.exists():
                log.warning(f"MISSING: {md_path.relative_to(PROJECT_ROOT)} (run generate.py first)")
                continue
            pdf_path = BUILD_DIR / f"stage-{s}" / f"{lesson['lesson_id']}.pdf"
            if skip_existing and pdf_path.exists() and pdf_path.stat().st_mtime >= md_path.stat().st_mtime:
                skipped += 1
                continue
            jobs.append((md_path, pdf_path, "lesson"))
    if skip_existing and skipped:
        log.info(f"skip-existing: {skipped} PDFs up-to-date, {len(jobs)} to render")
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
    import time as _time
    _t0 = _time.perf_counter()
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

    elapsed = _time.perf_counter() - _t0
    rate = ok / elapsed if elapsed > 0 else 0.0
    log.info(f"{label}: {ok} ok, {fail} failed, {elapsed:.1f}s ({rate:.2f} files/s, {n_workers} workers)")
    return ok, fail


def cmd_render_stage(stage: int, jobs: int = 1, skip_existing: bool = False):
    phase(f"Render Stage {stage}")
    jobs_list = _collect_render_jobs(stage, skip_existing=skip_existing)
    if not jobs_list:
        log.info(f"Stage {stage}: nothing to render (all up-to-date)")
        return
    log.info(f"Rendering Stage {stage}: {len(jobs_list)} lessons")
    ok, fail = _run_parallel_jobs(jobs_list, jobs, f"render-stage-{stage}")
    if fail:
        sys.exit(1)


def cmd_render_all(jobs: int = 1, skip_existing: bool = False):
    phase("Render All Lessons")
    jobs_list = _collect_render_jobs(skip_existing=skip_existing)
    if not jobs_list:
        log.info("All stages: nothing to render (all up-to-date)")
        return
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
        "--jobs", "-j", type=int, default=4,
        help="Parallel worker processes (default: 4). Stage/all only.",
    )
    parser.add_argument(
        "--skip-existing", action="store_true",
        help="Skip PDFs whose mtime is newer than source MD (incremental build).",
    )
    args = parser.parse_args()

    if args.file:
        cmd_render_single(args.file)
    elif args.stage:
        cmd_render_stage(args.stage, jobs=args.jobs, skip_existing=args.skip_existing)
    elif args.all:
        cmd_render_all(jobs=args.jobs, skip_existing=args.skip_existing)
    elif args.curriculum:
        cmd_render_curriculum()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
