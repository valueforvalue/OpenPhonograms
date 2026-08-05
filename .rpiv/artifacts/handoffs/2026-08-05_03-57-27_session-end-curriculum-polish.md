---
date: 2026-08-05T03:57:21+0000
author: Jeremy Morris
commit: ad78fcdb8b493fac5ff4a3572fe3b5ccefa2bc21
branch: master
repository: UncoveringtheLogic
topic: "Curriculum polish session — readers, packs, handbook TOC, image rendering"
tags: [pdf-rendering, reader-content, design, accessibility]
status: complete
last_updated: 2026-08-05T03:57:21+0000
last_updated_by: Jeremy Morris
type: feature_development
---

# Handoff: Curriculum Polish Session — Readers, Packs, Handbook, Images

## Task(s)

This session focused on cleaning up rendering quality and content across the Uncovering the Logic of English curriculum. Eight issues closed; five new issues filed for follow-up.

**Completed:**
- Issue #1: Missing phonogram worksheets for bu/gu/ti/ci/si (partial ship — bu/gu out of scope per LoE methodology)
- Issue #2: Reader warm-ups missing in Stages 3-5 (regression fixed at commit 27382e9)
- Issue #3: Interim quick-check assessments (15 HTMLs shipped)
- Issue #6: PDF table overflow checker (scripts/check-table-overflow.py)
- Issue #9: All markdown renderable to PDF (full audit done)
- Issue #11: Reader images in PDFs (CRITICAL fix — images were silently dropped, see Learnings)
- Issue #15: Stage 1 handbook TOC (TOC now in all 5 handbooks)
- Issue #18: Markdown in div blocks broken (renderer fix at commit b9ebcfa)
- Issue #16 partial: Stage 2 readers 002-006 rewritten with engaging plots (commit ad78fcd)
- Issue #19 partial: Lesson packs now include at-a-glance reference card (commit ea29d2b)

**Work in progress:**
- Issue #16: 19 more readers (007-025) still need rewrites
- Issue #19: Packs could use more differentiation (parent letter, differentiation tips)
- Issue #24: 12 orphan PNGs fixed (commit 587421d), see commit history

**New issues filed this session:**
- #25: Reorganize worksheets + readers by stage with merged per-stage PDFs
- #26: Add diacritical marks legend + key terms glossary
- #27: Refresh typography and visual design (Atkinson Hyperlegible research ready)

**Planned but not started:**
- Issue #12: build-release.py CLI flags
- Issue #13: Test suite for Python scripts
- Issue #14: Codebase design review

## Critical References

- `framework/render.py` — central markdown-to-PDF renderer (heavy edits this session)
- `framework/lesson-catalog.csv` — source of truth for stage + lesson metadata
- `scripts/generate-stage-handbook.py` — produces stage handbooks with TOC
- `scripts/build-lesson-pack.py` — produces lesson packs (at-a-glance card added)

## Recent changes

7 commits this session (latest first):
- `ad78fcd` feat: rewrite Stage 2 readers 002-006 with engaging plots (scripts/generate-readers.py + 5 reader .md files)
- `ea29d2b` feat: add at-a-glance reference card to every lesson pack (scripts/build-lesson-pack.py:171-380)
- `67cafd6` feat: add in-document Table of Contents to all 5 stage handbooks (scripts/generate-stage-handbook.py)
- `587421d` fix: embed images in PDFs + wire 12 orphan illustrations (framework/render.py, scripts/check-image-coverage.py, multiple reader/lesson MDs)
- `9f53fd9` fix: image alt text confuses pdftotext extraction (framework/render.py:254-262)
- `b9ebcfa` fix: parse markdown inside HTML div blocks (framework/render.py:253-275)
- `27382e9` fix: inject warm-up sections into Stages 3-4 reader lessons (scripts/generate-stage3.py + stage4.py)

## Learnings

**CRITICAL bugs discovered and fixed:**

1. **All images were silently dropped from PDFs.** Two separate bugs combined:
   - `framework/render.py` used `HTML(string=full_html)` without `base_url` — weasyprint silently skips image embeds when base URL isn't set
   - Image paths in source MD assumed next-to-md but images live at project root (e.g. `readers/001.md` references `images/animals/frog.png` but actual file is at `images/animals/frog.png` from project root)
   - Fix in commit 587421d: pass `base_url=PROJECT_ROOT`, rewrite image src via `_rewrite_img_src()` with fallback to project root
   - **Before fix: 0 images embedded in 450 PDFs. After fix: 135 images embedded.**

2. **Markdown inside `<div>` blocks didn't render.** python-markdown treats HTML block elements as opaque by default, so `### heading` and `**bold**` inside `<div class="reader-sidebar">` etc. passed through as raw text.
   - Fix: preprocessor that splits on `</?div[^>]*>` boundaries, runs markdown on each chunk separately, then reassembles
   - See framework/render.py:253-275

3. **Image alt text confuses pdftotext.** When markdown images had descriptive alt text, pdftotext extracted the alt and dumped it as visible text in the sidebar — making it look like stray story fragments.
   - Fix: render all images with `alt=""` (decorative marker). Visual rendering unaffected; only the alt attribute changes.

4. **`<div class="page-break">` was redundant.** Combined with `.reader-page { page-break-after: always }` it doubled page breaks in 001-fred-the-frog. Plus underscore fill-in lines `_______________________________________________` became `<hr />` (more page breaks).
   - Fix: removed page-break divs from 001, replaced long underscore sequences with em-dashes in fill-in lines

**Other patterns discovered:**

- Stage 1-2 readers (002-007) had 14-line repetitive text with minimal plot. 220-260 words is the right target. Constraint per reader is strict: only phonograms taught up to "After Lesson N" are decodable. **E.g. After Lesson 14** = before L15 (ee), so no "ee" words allowed yet. This makes Stage 2 rewrites the hardest work.
- Lesson packs already include cover + lesson + worksheet + flash cards + reader + home practice. Original #19 issue was wrong about "pack is just a copy of lesson PDF" — packs are comprehensive. The "differentiation" gap was the at-a-glance card (added).
- Stage handbooks render with `weasyprint.HTML(filename=...)` directly (not via render.py), so CSS must be inline in the markdown cover. Inline `<style>.page-break { page-break-before: always; }</style>` works.

## Artifacts

**Files modified in this session (code):**
- `framework/render.py:253-300` — image src rewriting + base_url + md-in-div fix + alt="" + img max-width CSS
- `framework/render.py:170-175` — img max-width CSS rule added
- `scripts/build-lesson-pack.py:240-380` — at-a-glance card builder
- `scripts/generate-stage-handbook.py` — added make_toc(), SECTION_ORDER, TYPE_LABELS dicts + inline CSS
- `scripts/generate-stage3.py:1327,1414,1501` — warm-up blocks in build_gwen, build_cole, build_sail
- `scripts/generate-stage4.py:217-329` — READER4_TMP + gen_firefly, gen_trains warm-ups
- `scripts/generate-readers.py:13-216` — rewrote Stage 2 reader dicts

**Files modified in this session (content):**
- `readers/001-fred-the-frog.md` — removed redundant page-breaks, replaced underscores with em-dashes
- `readers/002-dash-the-fish.md` through `readers/006-the-cake-bake.md` — rewrote with engaging plots
- `readers/006-the-cake-bake.md` — cover image added
- `lessons/stage-{2,3,4,5}/reader-*.md` — warm-up sections + cover illustrations (gwen-goose-gift, cole-bike, sail-box, firefly-night, train, ostrich-running)
- `lessons/stage-2/pg-ir.md` — added bird.png cover image
- `lessons/stage-3/reader-2.md` — added goose.png
- `lessons/stage-4/reader-5.md` — added firefly.png
- `lessons/stage-5/reader-7.md` — added ostrich.png
- `curriculum.md` — added diacritical-marks.png and all-multi.png references

**New files:**
- `scripts/check-image-coverage.py` — orphan + missing image detector

**Research outputs:**
- Web search research on typography/PDF design saved in temp file (path on agent system). Captured in issue #27.

## Action Items & Next Steps

1. **Issue #27 typography refresh** (highest priority next):
   - Download Atkinson Hyperlegible TTF from brailleinstitute.org/freefont
   - Place in `framework/fonts/` or `assets/fonts/`
   - Rewrite `framework/render.py` PAGE_CSS using research findings (Atkinson Hyperlegible, color-coded phonograms rust/green, 4-color palette, age-graded sizing)
   - Update `assets/main.css` (currently uses Charter/Georgia)
   - Regenerate all 248 lessons + 72 worksheets + 25 readers + 5 handbooks
   - Verify PDFs render correctly with new fonts
   - ~2-3 hours of work

2. **Issue #16 finish Stage 3-5 readers** (007-025):
   - 007 Bridge already has decent arc (light polish needed)
   - 008 Storm, 009 Invention have decent structure (light polish)
   - 010-025 animal readers (16 files in scripts/generate-animal-readers.py) are repetitive 100-180 words — need real plots
   - Decodability constraint per "After Lesson N" must be checked for each
   - See Stage 2 pattern in scripts/generate-readers.py:13-216 for reference

3. **Issue #25 worksheet/readers reorganization**:
   - Stage folders for phonograms, rules, cards, readers
   - Per-file PDFs in stage folders + per-stage merged PDFs
   - Generator changes in scripts/generate-worksheets.py
   - Stage info from framework/lesson-catalog.csv column 5

4. **Issue #26 glossary + diacritical legend**:
   - reference/diacritical-legend.html
   - reference/glossary.html
   - Same self-contained style as existing reference/phonogram-chart.html

5. **Issue #13 test suite**:
   - pytest for scripts/, framework/render.py
   - Render sample lesson/worksheet/reader → verify output

6. **Issue #12 build-release.py CLI flags**:
   - argparse for --lessons, --readers, --worksheets, --stage, --output
   - ~30 min of work

## Other Notes

- All fixes validated via `just check` pipeline (drift 248/248 OK, overflow check, image coverage 100%)
- TEACHER-GUIDE.pdf has pre-existing 6.9pt overflow on page 3 (not from this session — predates changes)
- `build/` directory is regenerated as part of `just all`. Don't commit PDFs — they're artifacts.
- Untracked PDFs in working tree (lesson-embedded reader PDFs and pack PDFs) should NOT be committed — they're output of scripts.
- pypdfium2 not installed in the default Python — only overflow checker needs it
- pypdf IS installed and works for image detection in PDFs
- pdftotext is at /mingw64/bin/pdftotext, useful for verifying rendered content
- WeasyPrint works fine with current PATH setup; GTK3 runtime is at C:\Program Files\GTK3-Runtime Win64\bin
- To verify images embedded in PDF: `python -c "import pypdf; r=pypdf.PdfReader('file.pdf'); print(sum(1 for page in r.pages for n,o in page['/Resources'].get('/XObject',{}).items() if (o.get_object() if hasattr(o,'get_object') else o).get('/Subtype')=='/Image'))"`

**Resume command for next session:** read this file, then start with issue #27 (typography refresh) since it has full research captured in the issue body.