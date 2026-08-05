# Copyright Review — Uncovering the Logic of English

**Date:** 2026-08-05
**Scope:** Full curriculum scan (lessons, worksheets, readers, game, website, code, assets, fonts)
**Reviewer:** AI agent (pi / MiniMax-M3)
**Sources audited:** 248 lessons, 31 rule intros, 75 phonograms, 25 decodable readers, 178 worksheets, framework code, the `phonogram-trainer.html` game, all docs, fonts, and bundled images.

---

## Headline

**No high-risk copyright issues found in the lesson content itself.** The phonogram tables, rule descriptions, rule explanations, and decodable readers are all original prose; the methodology facts (75 phonograms, 31 rules, 44 phonemes, the nine Silent-E reasons) are functional statements of how English spelling works and cannot be copyrighted. LoE's coined methodology terms ("Say-to-Spell", "Spelling Analysis", "Speech-to-Print") are used with attribution, and brief coined phrase labels are not copyrightable expression.

The **real gaps are infrastructural, not content**:

1. **No top-level `LICENSE` file** even though README says "MIT" and the release ZIP ships an MIT badge.
2. **Bundled SIL OFL font without `OFL.txt`** — Atkinson Hyperlegible is OFL-licensed and the OFL text must accompany the `*.ttf` distribution.
3. **`TEACHER-GUIDE.md` has no attribution/license block** despite being the primary teacher-facing document.
4. **Lesson/workheet generation template has no methodology footer** — generated PDFs are silent on source.
5. **No image provenance** for 35 PNGs in `images/`.
6. **No SPDX/copyright headers** in any of the 15+ Python files.
7. **`## By Denise Eide` heading in `curriculum.md`** reads like authorship rather than source citation.

---

## Severity Summary

| Severity | Count | Examples |
|---|---|---|
| HIGH | 4 | Missing `LICENSE`, missing font OFL, missing teacher-guide attribution, ambiguous `# By Denise Eide` heading |
| MEDIUM | 7 | README vague license, no Python SPDX, missing lesson-template footer, no game license, no image provenance, no PDF credit spot-check, missing `NOTICE` |
| LOW | 5 | `docs/USE.md` / `docs/BUILD.md` no footer, `CONTEXT.md`/`MISSION.md`/`NOTES.md` no footer, `justfile` no SPDX, `CHANGELOG.md` no footer |
| INFO | 5 | `AGENTS.md`, `.github/`, `.rpiv/`, `learning-records/`, `prompts.txt` — no license needed |

---

## Detailed Findings

### 1. [HIGH] No top-level `LICENSE` file

- **File:** `C:/Development/UncoveringtheLogic/` (root)
- **State:** No `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `NOTICE`, or `COPYING` file anywhere in the tree.
- **Evidence:** README has a `## License` section but does not name the license; `docs/index.html` says "MIT license" but the root has no LICENSE file; `scripts/build-release.py` writes a MIT statement into the release ZIP's README but no file in-tree matches it.
- **Risk:** Public repository with substantial curriculum content (248 lessons, methodology, code) and an implied MIT license but no binding LICENSE file. GitHub cannot auto-detect license. Potential downstream users cannot verify rights.
- **Action:** Add `LICENSE` (MIT) at repo root with standard MIT text + copyright year. Add `NOTICE` crediting Denise Eide / Logic of English for the methodology and the Braille Institute for the bundled font.

### 2. [HIGH] Bundled SIL OFL font missing `OFL.txt`

- **Files:** `framework/fonts/AtkinsonHyperlegible-Regular.ttf`, `*-Italic.ttf`, `*-Bold.ttf`, `*-BoldItalic.ttf`
- **State:** Atkinson Hyperlegible is © Braille Institute of America, licensed under SIL Open Font License 1.1. The font files are committed to the repo (and presumably shipped in the release ZIP) but **no `OFL.txt` is bundled anywhere** (none in `framework/fonts/`, none in `assets/`, none at root).
- **Risk:** SIL OFL requires the license text to accompany the font distribution. Shipping the `.ttf` files without `OFL.txt` violates the OFL.
- **Action:** Add `framework/fonts/OFL.txt` containing the full SIL OFL 1.1 text. Add `framework/fonts/AUTHORS.txt` crediting Braille Institute. Note the font license in `README.md` License section.

### 3. [HIGH] `TEACHER-GUIDE.md` has no attribution or license block

- **File:** `C:/Development/UncoveringtheLogic/TEACHER-GUIDE.md` (19 KB, 433 lines)
- **State:** Zero occurrences of `license`, `copyright`, `©`, `attribution`, or any source citation. The document is the primary teacher-facing instructional guide and contains methodology derived from Logic of English without any on-file credit.
- **Risk:** Distribution-facing document with Eide-derived methodology and no credit. Notable omission given the rest of the repo's attribution discipline.
- **Action:** Add a `## Attribution & License` section at the end (or top) crediting Denise Eide / Logic of English and pointing to the LICENSE file.

### 4. [HIGH] `curriculum.md` heading `## By Denise Eide` reads like authorship

- **File:** `C:/Development/UncoveringtheLogic/curriculum.md` lines 1–3
- **Quote:** `# Teach Your Child to Read: A Curriculum Based on *Uncovering the Logic of English*` / `## By Denise Eide`
- **State:** The first-section heading `## By Denise Eide` reads as if Denise Eide authored *this* document, when in fact this is an *adaptation* of her methodology. The footer at lines 1185–1196 correctly cites the source book, but the opening heading is ambiguous.
- **Risk:** Misleading attribution. Could be read as Eide authoring this adaptation, which is not the case.
- **Action:** Change `## By Denise Eide` to `## Adapted from the methodology of Denise Eide` or similar. Add an explicit license line near the top referencing `LICENSE` and `NOTICE`.

### 5. [MEDIUM] `README.md` License section is vague

- **File:** `C:/Development/UncoveringtheLogic/README.md` lines 124–136
- **State:** Has `## License` and `## Credits` sections. Credits nicely cite Denise Eide and the broader LoE resource list. The License section says "open-source adaptation... released for educational use" but does **not** name MIT, does not point to a `LICENSE` file (none exists), and does not acknowledge the bundled font.
- **Action:** Replace the License section with: `Released under the MIT License — see [LICENSE](LICENSE). Methodology © Denise Eide / Logic of English. Bundled font Atkinson Hyperlegible © Braille Institute of America, licensed under SIL OFL 1.1 — see framework/fonts/OFL.txt.`

### 6. [MEDIUM] No SPDX/copyright headers in any Python file

- **Files:** `framework/render.py`, `framework/generate.py`, `framework/image-check.py`; all `scripts/generate-*.py`, `scripts/build-*.py`, `scripts/check-*.py`; `games/generate-audio-edge.py`.
- **State:** None of the 15+ Python files have SPDX headers, copyright lines, or author blocks. Each file starts with a triple-quoted module docstring describing usage but never declares license.
- **Action:** Add a one-line SPDX header to each file (or to a small set of entry points if the project prefers minimal):
  ```python
  # SPDX-License-Identifier: MIT
  # Copyright (c) 2026 <author>. Adapted from the methodology of Uncovering the Logic of English (Denise Eide).
  ```

### 7. [MEDIUM] Lesson template and 248 generated lessons are silent on source

- **Files:** `framework/templates/lesson-template.md` (and likely `worksheet-template.md`, `reader-template.md`). The 248 `lessons/stage-*/lesson-*.md` files.
- **State:** `packs/stage-*/lesson-*.md` files do carry a footer `*Pack generated for the *Uncovering the Logic of English* curriculum.*` (added by `scripts/build-lesson-pack.py`), but the **underlying lesson files** in `lessons/` carry no such attribution. Grep for `Uncovering the Logic of English` in `lessons/stage-*.md` returns no matches outside the catalog.
- **Action:** Extend `framework/templates/lesson-template.md` (and worksheet/reader templates) with a footer:
  ```markdown
  *Source: Adapted from the methodology of Uncovering the Logic of English by Denise Eide. License: MIT — see LICENSE.*
  ```
  Regenerate lessons so the footer is present in every generated artifact, including PDFs.

### 8. [MEDIUM] `games/phonogram-trainer.html` has no license header

- **File:** `C:/Development/UncoveringtheLogic/games/phonogram-trainer.html` (734 lines)
- **State:** Title says "Phonogram Trainer — Logic of English" but there is no SPDX header, no `<meta name="license">`, no footer comment. Grep for `license|©|attribution|jquery|bootstrap|cdn|unpkg|jsdelivr` returns zero matches — the file is fully self-contained (no third-party JS/CSS to attribute).
- **Action:** Add a top-of-file comment:
  ```html
  <!-- SPDX-License-Identifier: MIT -->
  <!-- Adapted from the methodology of Uncovering the Logic of English (Denise Eide). -->
  ```

### 9. [MEDIUM] `images/` has no provenance file

- **Files:** `images/animals/*.png` (24 files), `images/illustrations/*.png` (8 files), `images/misc/diacritical-marks.png`, `images/phonograms/all-single.png`, `images/phonograms/all-multi.png`, `images/phonogram_worksheet_template.pdf` — 35 total assets.
- **State:** Grep for `copyright|©|attribution|license|credit` over `images/`, `assets/`, `games/` returns zero matches. No `SOURCES.md` or `image-manifest.csv` license column. PNGs appear to be generated programmatically (likely from an upstream image generator script that is not in the repo).
- **Action:** Create `images/SOURCES.md` with: AI generator used (and version/date), prompt style, license for the generated images, any third-party sources. Add a `license` column to `framework/image-manifest.csv`.

### 10. [MEDIUM] PDFs not programmatically checked for embedded credits

- **Files:** `TEACHER-GUIDE.pdf` (~65 KB) plus an estimated ~500 PDFs across `build/`, `packs/`, and `release.zip`.
- **State:** PDF text is FlateDecode-compressed; raw `grep` finds no embedded license/copyright strings. Without a programmatic check, we cannot verify that rendered PDFs carry the methodology footer.
- **Action:** Add a `just check-pdf-credits` recipe that uses `pypdf` to extract text from the first page of a sample PDF and asserts it contains "Denise Eide" or "Uncovering the Logic of English". Reference: the justfile already calls `pypdf` for the rotation check.

### 11. [LOW] `docs/USE.md` and `docs/BUILD.md` no footer

- **Files:** `docs/USE.md`, `docs/BUILD.md`
- **State:** `docs/BUILD.md` line 37 has a `Source: [Uncovering the Logic of English](...)` link — good. `docs/USE.md` has no license/attribution section. `docs/index.html` (the landing page) is well-formed — best example in the repo (lines 243–263).
- **Action:** Add a one-line footer to `docs/USE.md` and `docs/BUILD.md`:
  ```markdown
  *License: MIT — see [LICENSE](../LICENSE). Methodology © Denise Eide / Logic of English.*
  ```

### 12. [LOW] `CONTEXT.md`, `MISSION.md`, `NOTES.md` no footer

- **State:** `CONTEXT.md` references "LoE" in domain glossary context; `MISSION.md` line 1 says "Mission: Teach Reading Through the Logic of English"; `NOTES.md` mentions "LoE" in passing. None have a license/attribution footer.
- **Action:** Add a one-line footer to each pointing to `LICENSE` and `NOTICE`. Style only; not a copyright gap.

### 13. [LOW] `justfile` no SPDX header

- **File:** `C:/Development/UncoveringtheLogic/justfile` (16 KB)
- **State:** First lines are `# justfile — Uncovering the Logic of English` / `# Print-first curriculum build pipeline`. No license.
- **Action:** Add `# SPDX-License-Identifier: MIT` at the top. Style.

### 14. [LOW] `CHANGELOG.md` no footer

- **File:** `C:/Development/UncoveringtheLogic/CHANGELOG.md` (1.8 KB)
- **State:** Pure version history. Conventional CHANGELOGs don't need a license, but a one-line footer would aid discoverability.
- **Action:** Optional footer: `*Open-source adaptation of Uncovering the Logic of English by Denise Eide. License: MIT — see LICENSE.*`

### 15. [INFO] Items that are fine

- **`AGENTS.md`, `.github/`, `.rpiv/`, `learning-records/`, `prompts.txt`** — no license needed.
- **`docs/agents/learning/logic-of-english.md`** — internal context, not distribution-facing.
- **`docs/index.html`** — well-formed license + credits section; best example in repo.
- **`RESOURCES.md`** — proper academic citations of Eide book and Ouellette 2017 paper.
- **`games/phonogram-trainer.html`** — fully self-contained; no third-party CDN libraries to attribute.
- **`docs/agents/adr/*.md`** — internal architecture decisions, not distributable.
- **`phonogram-trainer.html`** — self-contained (no CDN/JS libraries).

---

## Quoted Source Material Audit (content audit)

The second pass scanned all 248 lessons, 31 rule intros, 75 phonograms, 25 decodable readers, 178 worksheets, and the narrative docs (`curriculum.md`, `TEACHER-GUIDE.md`, `README.md`, `MISSION.md`, etc.) for extended prose quotations from copyrighted sources.

**No HIGH or MEDIUM risk findings.** The phonogram tables, rule descriptions, and high-frequency word explanations are all short, functional statements of fact about English spelling — the kind of factual content that is not copyrightable. The decodable readers are entirely original prose.

Specific items reviewed and assessed:

| Item | Source | Finding |
|---|---|---|
| Phonogram sounds (e.g., "A says /a/, /ay/, /ah/") | Standard phonics methodology | **INFO** — factual mappings |
| "75 phonograms / 31 rules / 44 phonemes / 106 tools" | LoE marketing thesis | **LOW** — short factual counts |
| "98% of English words follow patterns" | LoE marketing | **LOW** — statistical claim, not copyrightable |
| Nine Silent E reasons (12.1–12.9) | LoE framework | **LOW** — short functional labels, framework not copyrightable |
| "Say-to-Spell" | LoE coined term | **LOW** — coined phrase, used with attribution |
| "Speech-to-print, not print-to-speech" | LoE pedagogical thesis | **LOW** — two-sentence statement of widely-held phonics distinction |
| Spelling Analysis 5-step routine | LoE routine | **LOW** — labeled framework, brief descriptions |
| 25 decodable readers | Original prose | **INFO** — no passages from copyrighted children's literature |
| Latin/Greek root meanings | Standard etymology | **INFO** — facts |
| Phonemic awareness activities | Standard pedagogy | **LOW** — original instructional text |

---

## Trademark Audit

- **"Logic of English"** — used throughout in nominative fair-use form ("Adapted from *Uncovering the Logic of English* by Denise Eide", "LoE methodology"). All occurrences are attributive.
- **"Denise Eide"** — consistently credited as the methodology author.
- **"Uncovering the Logic of English"** — this is the title of Eide's book and also the project name. This is borderline; the project is a direct adaptation of the book, so calling the project "Uncovering the Logic of English — Open-Source Curriculum" is defensible as fair use (descriptive use of the source title to indicate origin). However, the project README does not include a trademark disclaimer. **Recommend:** add a one-line disclaimer to `README.md`:
  > "Logic of English® and *Uncovering the Logic of English* are trademarks of Logic of English, Inc. This project is an unaffiliated open-source adaptation and is not endorsed by Logic of English, Inc."
- **"Foundations", "Essentials", "Phonograms", "Spelling Rules"** — used descriptively in `framework/README.md` to compare scope against LoE's product line. Acceptable as descriptive comparative use.
- **No `®` or `™` markers** present anywhere — opportunity to add proper attribution to the trademark holder.

---

## Recommended Remediation Order

1. **Create `LICENSE`** (MIT) at repo root, and **`NOTICE`** crediting Eide + Braille Institute.
2. **Bundle `framework/fonts/OFL.txt`** with the SIL OFL 1.1 text.
3. **Add `## Attribution & License` footer** to `TEACHER-GUIDE.md`, and resolve the `## By Denise Eide` ambiguity in `curriculum.md`.
4. **Update `README.md` License section** to name MIT and point at `LICENSE`.
5. **Add SPDX headers** to all Python files (or at least the three framework entry points).
6. **Extend lesson/worksheet/reader templates** with a methodology footer so generated PDFs carry attribution.
7. **Add license header** to `games/phonogram-trainer.html`.
8. **Create `images/SOURCES.md`** documenting image provenance.
9. **Add `just check-pdf-credits` recipe** that verifies rendered PDFs embed attribution.
10. **Add trademark disclaimer** to `README.md`.
11. **Add SPDX header** to `justfile` and one-line footers to `docs/USE.md`, `docs/BUILD.md`, `CONTEXT.md`, `MISSION.md`, `NOTES.md`, `CHANGELOG.md`.

---

## What Is Fine

- The phonogram content (sounds, mapping tables) is factual and not copyrightable.
- The 25 decodable readers are entirely original prose.
- The 75 phonogram worksheets and 31 rule worksheets are short practice templates.
- The `docs/index.html` landing page is the best-licensed document in the repo.
- `RESOURCES.md` has proper academic citations.
- The `phonogram-trainer.html` game uses no third-party libraries.
- The `packs/` build pipeline already adds a "Uncovering the Logic of English" footer to generated packs.
- Methodology is consistently attributed to Denise Eide in narrative docs.

---

## Summary

The lesson content itself is clean — no extended prose quotations from copyrighted sources, no children's literature in the decodable readers, all phonogram/rule descriptions are original prose. The gaps are all in the **license and attribution infrastructure** that surrounds the content. None of them are severe enough to warrant taking the curriculum offline, but several (missing `LICENSE`, missing `OFL.txt`) should be fixed before any public release to other users.
