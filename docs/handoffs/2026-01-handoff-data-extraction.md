# Handoff: Data Extraction + Template Migration (#22, #23)

**Date:** 2026-01-30
**Branch:** main
**Last commit:** `31ba0fb`
**Status:** Slice 1 of 9 complete. Slice 0 + 1 pushed to main. Remaining: Slices 2–9.

## TL;DR

Two paired refactors in flight:

- **#22** Extract phonogram + rule data to YAML single source of truth
- **#23** Replace f-string lesson scaffolds with Jinja templates

Done: Slice 0 (infrastructure) + Slice 1 (Stage 1 generator). Stage 1 produces byte-identical output via Jinja templates loading from YAML data.

## What ships

### Slices pushed (committed to main)

**Slice 0** — `ea9ea8e` — `feat(data): scaffold YAML data + JSON schemas + validate-data`

- `data/phonograms.yaml` — 75 phonograms (a-p, qu, r-y, z; `q` alone is taught only via `qu`)
- `data/rules.yaml` — 31 spelling rules
- `data/sentences.yaml` — 132 curated game sentences
- `data/{silent_e,roots,high_frequency_words,decodable_wordlists}.yaml` — stubs (empty lists, schema-valid)
- `schemas/data/*.schema.json` — JSON Schema (Draft 2020-12) for each YAML file
- `framework/data_loader.py` — `load_phonograms()`, `load_rules()`, etc., returning frozen dataclasses; validates against schemas; raises `DataValidationError` on drift
- `framework/requirements.txt` — added `jsonschema>=4.20`
- `framework/phonograms.py` — docstring only (no behavior change)
- `framework/rules.py` — added `"11": 1` to `RULE_STAGE` (Rule 11 taught alongside `qu` in Stage 1 lesson 14)
- `templates/{lesson,phonogram,rule}.md.j2` — generic scaffolds (not yet consumed by any generator)
- `scripts/migrate-data.py` — one-shot: read Python constants → emit YAML. Idempotent. Run once on main.
- `scripts/validate-data.py` — schema validation + catalog coverage. Wired as `just validate-data`. `just check` now runs it.
- `justfile` — `validate-data` and `migrate-data` recipes added

**Slice 1** — `31ba0fb` — `refactor(stage1): migrate Stage 1 generator to Jinja templates + YAML data`

- `scripts/generate-stage1.py` — 1744 → 842 LOC (-52%)
- `templates/stage-1/*.md.j2` — 7 templates: `phonogram-intro`, `phonemic-awareness`, `phonemic-awareness-with-review`, `review`, `vowel-concept`, `handwriting`, `assessment`
- **Byte-identical verified**: all 48 Stage 1 lessons regenerate identically
- Stage-1 phonograms now loaded from `framework.data_loader.load_phonograms()`
- Per-PG teaching data (writing steps, spelling/reading word lists, review match words) stays inline in generator — that's stage-specific content, not catalog data

### Follow-up issue filed

- **#29** "Fix build_pa_with_review: Activity 2 body uses wrong index" — pre-existing bug preserved for byte-identical output. Tracked for separate PR.

## What remains

Per the phased plan, 7 more slices:

| Slice | Title | Est LOC | Risk |
|-------|-------|---------|------|
| 2 | Stage 2 Jinja migration | ~1700 | Medium |
| 3 | Stage 3 Jinja migration | ~1800 | Medium |
| 4 | Stage 4 Jinja migration | ~1800 | Medium |
| 5 | Stage 5 Jinja migration | ~1200 | Medium |
| 6 | Worksheets consumer swap | ~30 | Low |
| 7 | Navigation/assessment/sidebar/quick-checks/placement-test consumer swap | ~50 | Low |
| 8 | Game data YAML→JSON shim | ~30 | Low |
| 9 | Delete `framework/phonograms.py` + `framework/rules.py` data blocks | cleanup | Low |

Each slice gated by byte-identical output diff against its stage.

## Architecture (so future work doesn't have to rediscover)

### Data flow

```
data/*.yaml  →  framework/data_loader.py  →  generators  →  lessons/*.md
       ↑                                       ↑
       │                                       │
   validate-data.py                       Jinja templates
   (schema + catalog                      (templates/stage-N/)
    coverage)
```

### Key files

- `framework/data_loader.py` — single entry point for data access. Stage 1 already uses it. Slices 2–8 should switch their generators to use it.
- `framework/phonograms.py` + `framework/rules.py` — OLD canonical data. Will be deleted in Slice 9. Currently still imported by downstream consumers (worksheets, navigation, assessment, sidebar, game-data).
- `templates/stage-1/` — Stage 1 lesson templates (7 files). Each stage will get its own `templates/stage-N/` directory.
- `scripts/validate-data.py` — runs in CI via `just check`. Cross-checks YAML ↔ catalog CSV. Exit 1 on drift.
- `framework/render.py` — markdown → WeasyPrint PDF. Templates produce **markdown**, not HTML — preserves existing pipeline.
- `framework/templates/` — existing teacher-script templates (PDF output). Separate from `templates/` (top-level) which is for lesson MD output. Don't conflate them.

### Stage-specific data still inline

Each `generate-stageN.py` keeps some data inline that's not in `data/phonograms.yaml`:

- Stage 1: `SPELLING_WORDS`, `READ_WORDS`, `MATCH_WORDS` dicts in `generate-stage1.py`
- Stage 2: `HF_WORDS_SET1/2/3`, `PG_SPELLING_WORDS`, `VC_WORDS`, `CVC_*` lists (per stage-2 plan)
- Stage 3: `SILENT_E` (9 sub-rules of Rule 12 — `data/silent_e.yaml` stub)
- Stage 5: `ROOTS` (22 Latin/Greek roots — `data/roots.yaml` stub)

These belong in YAML when content is finalized. For now, kept inline so each stage slice stays focused on Jinja migration.

### Decisions locked (don't revisit)

1. **Schema validation in CI** (`just validate-data` runs in `just check`)
2. **One YAML file with `stage:` field** (not per-stage split)
3. **Delete `framework/phonograms.py` + `rules.py` shims immediately** — no re-export layer
4. **Byte-identical gate per stage** — `diff -r --strip-trailing-cr .baseline/stage-N lessons/stage-N` must be empty
5. **Templates output markdown** (not HTML) — preserves `framework/render.py` pipeline
6. **76 phonograms confirmed correct count** — `qu` in SINGLE brings total to 76 (was 75). `q` alone is taught only as part of `qu`. AGENTS.md drift-watch note: "75 phonograms" is loose; actual is 76.

## Open questions resolved

| Question | Answer | Locked at |
|----------|--------|-----------|
| Schema validation? | Yes, in CI | Slice 0 design |
| One YAML file or split? | One file with `stage:` field | Slice 0 design |
| Shim strategy? | Delete immediately | Slice 0 design |
| Phonogram count? | 76 (with `qu` in SINGLE) | Slice 0 bug fix |
| `roots.yaml` + HF words source? | Empty stubs OK | Slice 0 design |
| `teacher_script` injection? | Template-level `{% include %}` | Slice 0 design |

## Patterns learned

When resuming Slice 2+:

1. **Capture baseline**: `cp -r lessons/stage-N .baseline/stage-N` before refactor
2. **Diff after regen**: `diff -r --strip-trailing-cr .baseline/stage-N lessons/stage-N` — must be empty (excluding whitespace/CRLF)
3. **Jinja CRLF gotcha**: `templates/stage-N/*.md.j2` use LF; generator writes LF; git autocrlf converts on commit. Use `diff --strip-trailing-cr` to compare.
4. **Trailing blank line**: phonogram-intro lessons (with `format_phonogram_script()` injection) end with `\n\n`; PA/review/etc. end with `\n`. Detect via `if content.endswith("details>")` in generator. See `scripts/generate-stage1.py:main()`.
5. **Pre-existing bugs**: `build_pa_with_review` had `activity_2_body=activities[2][1]` — preserved with comment for follow-up. Slice 2+ may find more; replicate byte-identical and file separate issue.
6. **Stage teaching order**: Stage 1 uses explicit sequence `["a", "d", "g", "c", "o", "qu", ...]`, not alphabetical from YAML. Define `STAGE_N_ORDER` const in generator.

## Resume checklist

To pick up Slice 2:

1. `cp -r lessons/stage-2 .baseline/stage-2`
2. Read `scripts/generate-stage2.py` end-to-end; map template + builder functions (similar shape to stage 1)
3. Create `templates/stage-2/*.md.j2` (1 per lesson type)
4. Refactor `generate-stage2.py` to use Jinja + `framework.data_loader`
5. `python scripts/generate-stage2.py` + `diff -r --strip-trailing-cr .baseline/stage-2 lessons/stage-2` → empty
6. Commit + push with same conventional-commits pattern
7. Proceed to Slice 3

## Repo state

- **Branch:** main @ `31ba0fb`
- **Working tree:** clean
- **Open issues:** 7 total (28, 27, 26, 25, 24, 23, 22 + #29 bug + 22 originals)
- **Issue #22, #23 status:** 0/9 slices remaining (1/9 complete: Slice 0 + Slice 1). Slice 0 + 1 closed/merged.
- **Pending review:** none — all changes pushed

## File paths summary

```
data/
├── phonograms.yaml          (75 phonograms)
├── rules.yaml               (31 rules)
├── sentences.yaml           (132 game sentences)
├── silent_e.yaml            (stub)
├── roots.yaml               (stub)
├── high_frequency_words.yaml (stub)
└── decodable_wordlists.yaml (stub)

schemas/data/
└── *.schema.json            (7 files)

framework/
├── data_loader.py           (NEW — single entry point)
├── phonograms.py            (docstring fix only)
└── rules.py                 (Rule 11 stage 1 added)

templates/
├── lesson.md.j2             (generic, not yet consumed)
├── phonogram.md.j2          (generic, not yet consumed)
├── rule.md.j2               (generic, not yet consumed)
└── stage-1/                 (7 templates, consumed by stage 1)

scripts/
├── generate-stage1.py       (refactored: 842 LOC, was 1744)
├── generate-stage{2,3,4,5}.py  (NOT YET — slices 2-5)
├── generate-worksheets.py   (uses old phonograms.py — slice 6)
├── generate-navigation.py   (uses old — slice 7)
├── generate-game-data.py    (uses old — slice 8)
├── check-worksheet-coverage.py  (uses old — slice 9)
├── check-drift.py           (unaffected)
├── validate-data.py         (NEW — CI gate)
└── migrate-data.py          (NEW — one-shot)
```
