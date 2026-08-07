# ADR 0003: Generator Scripts as Source of Truth

**Status:** Accepted  
**Date:** 2025-08-03

## Context

244 lessons, 148 worksheets, 16 readers, 75 phonogram flash cards. Hand-authoring each file is error-prone and slow. Changes to content schema require updating hundreds of files.

## Decision

Python generator scripts in `scripts/` are the source of truth for all generated content. Output markdown files in `lessons/`, `worksheets/`, `readers/` must not be hand-edited. To change content, change the generator and regenerate.

Generator scripts:
- `scripts/generate-stage1.py` through `generate-stage5.py` — 244 lessons
- `scripts/generate-worksheets.py` — 148 worksheets, flash cards, templates
- `scripts/generate-readers.py` — 9 standalone readers
- `scripts/generate-audio-edge.py` — audio pack for web game

Hand-authored exceptions (no generator):
- `TEACHER-GUIDE.md`, `AGENTS.md`, `CONTEXT.md`
- `curriculum.md`
- `reference/*.html`
- `games/phonogram-trainer.html`
- `framework/render.py`, `framework/image-check.py`

## Consequences

- Positive: Single change propagates to all affected files
- Positive: Content consistency guaranteed (same data, same template)
- Positive: Regeneration is fast and idempotent
- Negative: Generator complexity (template bugs affect many files)
- Negative: Must regenerate after generator changes (drift risk if forgotten)
- Mitigation: `framework/render.py --all` includes a drift check for missing files
