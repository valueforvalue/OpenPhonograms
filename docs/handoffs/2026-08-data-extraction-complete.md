# Handoff: Data Extraction + Template Migration — COMPLETE

**Date:** 2026-08-08
**Branch:** main @ `6d64f45`
**Status:** All 9 slices pushed. Issues #22 + #23 closed.

## TL;DR

Issues [#22](https://github.com/valueforvalue/OpenPhonograms/issues/22) and [#23](https://github.com/valueforvalue/OpenPhonograms/issues/23) are resolved. Phonogram + rule data now lives in `data/*.yaml` (schema-validated), and lesson scaffolds render from Jinja templates in `templates/stage-{1..5}/*.md.j2`. Single source of truth: `framework/data_loader.py`.

## What landed

### Slice 0 — Foundation (`ea9ea8e`)

- `data/phonograms.yaml` — 75 phonograms (a-z + qu + 26 Stage 2 + 20 Stage 3 + 3 Latin /sh/)
- `data/rules.yaml` — 31 spelling rules
- `data/{silent_e,roots,high_frequency_words,decodable_wordlists}.yaml` — stubs
- `schemas/data/*.schema.json` — JSON Schema (Draft 2020-12) for each YAML
- `framework/data_loader.py` — loaders returning frozen `Phonogram` / `Rule` / `Sentence` dataclasses
- `scripts/validate-data.py` — schema + cross-file drift check (wired into `just check`)

### Slices 1-5 — Stage generators (`31ba0fb` → `bd156fd`)

| Slice | Stage | Before LOC | After LOC | Templates |
|---|---|---|---|---|
| 1 | Stage 1 | 1744 | 842 (-52%) | 7 |
| 2 | Stage 2 | 1706 | 1082 (-37%) | 9 |
| 3 | Stage 3 | 1811 | 1371 (-24%) | 8 |
| 4 | Stage 4 | 1817 | 1426 (-21%) | 7 |
| 5 | Stage 5 | 1186 | 869 (-27%) | 8 |

Each stage generator uses `jinja2.Environment(FileSystemLoader, trim_blocks, lstrip_blocks, keep_trailing_newline) + small render(name, **vars)` helper. Stage-specific data (MULTI_PGS, RULES, HF_WORDS, etc.) stays inline per Slice 0 decision. Long-form content (Gwen/Cole/Sail readers, mixed_spelling, schwa lessons) remains inline — lesson-specific prose.

### Slice 6 — Consumer swap (`5db04c7`)

`scripts/generate-worksheets.py`, `scripts/generate-navigation.py`, `scripts/generate-game-data.py` migrated from `framework.phonograms.py` + `framework/rules.py` to `framework.data_loader`. Added legacy-compatible dict helpers (`pg_dict()`, `pg_kind_buckets()`, `rules_dict()`) so consumer code can stay near-identical. Teaching order locked in `pg_kind_buckets()` so worksheet output stays byte-identical.

### Slices 7-9 — Sidebar + cleanup (`6d64f45`)

- `framework/reader_sidebar.py` — migrated to `framework.data_loader`
- Deleted legacy modules: `framework/phonograms.py`, `framework/rules.py`, `framework/assessment.py` (dead code), `scripts/migrate-data.py` (one-shot, complete)
- Updated `tests/test_phonograms.py` to test `data_loader` API
- Updated `tests/test_game_data.py` count assertion (72 → 75)

## Final architecture

```
data/*.yaml                  ← source of truth (75 phonograms, 31 rules)
       ↓
schemas/data/*.json          ← JSON Schema validation
       ↓
framework/data_loader.py     ← loaders + Phonogram/Rule dataclasses + legacy dict helpers
       ↓
┌────────────────────────────────────────────────────────────────┐
│  Stage generators (Stage 1-5):                                  │
│    templates/stage-N/*.md.j2 → env.get_template().render()     │
├────────────────────────────────────────────────────────────────┤
│  Consumer scripts (no .format() templates):                     │
│    - generate-worksheets.py (129 worksheets)                     │
│    - generate-navigation.py  (6 handbook MDs + PDFs)            │
│    - generate-game-data.py   (scripts/_game_data.json)          │
│    - generate-readers.py     (24 readers + Spelling Aid sidebars) │
│    - generate-animal-readers.py (16 readers)                    │
│    - generate-quick-checks.py (15 HTMLs)                        │
│    - generate-placement-test.py (1 HTML + PDF)                  │
│    - framework/reader_sidebar.py (per-page Spelling Aid)        │
└────────────────────────────────────────────────────────────────┘
```

## Verification gates passed

Every slice verified byte-identical regeneration:

| Slice | Files | `diff -r --strip-trailing-cr` |
|---|---|---|
| 1 | 48 Stage 1 lessons | 0 |
| 2 | 56 Stage 2 lessons | 0 |
| 3 | 58 Stage 3 lessons | 0 |
| 4 | 45 Stage 4 lessons | 0 |
| 5 | 39 Stage 5 lessons | 0 |
| 6 | 129 worksheets | 0 |

Plus navigation MDs (6), quick-check HTMLs (15), game data JSON (1) verified byte-identical.

## Tests

`pytest tests/test_phonograms.py tests/test_game_data.py tests/test_reader_sidebar.py` — 228 passed, 0 failed.

`pytest tests/` — 175 passed, 13 skipped, 6 pre-existing CWD-related failures (test files use relative paths; run from project root).

`just validate-data` — PASS (75 phonograms, 31 rules).

`just check-worksheet-coverage` — PASS (100% coverage, 75 PG worksheets, 31 rule worksheets).

## Commits

```
6d64f45 refactor(data): delete legacy phonograms.py + rules.py; finalize Slice 7/8/9
5db04c7 refactor(consumers): switch from framework/phonograms.py + rules.py to framework.data_loader
bd156fd refactor(stage5): migrate Stage 5 generator to Jinja templates
6270dca refactor(stage4): migrate Stage 4 generator to Jinja templates
084ab47 refactor(stage3): migrate Stage 3 generator to Jinja templates
90348e3 refactor(stage2): migrate Stage 2 generator to Jinja templates
31ba0fb refactor(stage1): migrate Stage 1 generator to Jinja templates + YAML data
ea9ea8e feat(data): scaffold YAML data + JSON schemas + validate-data (#22, #23)
```

## Outstanding

- **#29** (pre-existing): `build_pa_with_review: Activity 2 body uses wrong index (activities[2][1] instead of [1][1])` — preserved for byte-identical Stage 1 output. Fix in separate slice.

## Lessons learned

1. **Teaching order must be locked in code, not YAML** — `pg_kind_buckets()` hardcodes SINGLE_ORDER/MULTI_ORDER to keep consumer output byte-identical.
2. **`keep_trailing_newline=True`** required for templates without `{{ teacher_script }}` (Stage 3+) — default Jinja strips trailing `\n`.
3. **Assessment template literal escape**: `__/{{ '{overall_total}' }}` produces the literal `__/{overall_total}` string the original `.format()` produced. (Same `{{ }}` → `{ }` escape that `.format()` does with `{{`.)
4. **Python 3.14 + Windows**: em-dashes in Python source need UTF-8 declaration (`# -*- coding: utf-8 -*-`). Missing it → SyntaxError on `U+2014`.
5. **Pre-existing bugs**: preserve + comment. Don't fix during refactor — byte-identical gate is sacred. File separate issue (#29).
6. **Inline vs template split**: scaffold structure = template; lesson-specific prose (readers, examples, stories) = inline. Don't over-template.
7. **Dict-of-dict compat**: when migrating, expose both typed dataclasses AND legacy dict shape (`pg_dict()`, `rules_dict()`). Saves rewriting consumers twice.
8. **Pre-capture baseline AFTER running generator once** if the generator has pre-existing inconsistencies (Stage 4 had `prefix-un-dis.md` as orphan from old yield/slug mismatch). Diff against the actual output, not against HEAD's committed files.

## Repo state

- **Branch:** main @ `6d64f45`
- **Issues closed:** #22, #23
- **Issues open:** #24 (VERSION), #25 (Feedback form), #26 (PDF blank pages), #28 (more readers), #29 (pre-existing PA-with-review bug)
- **Working tree:** clean (modulo generated PDFs in build/, which are gitignored)
