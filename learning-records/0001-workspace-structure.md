# Learning Record 0001: Workspace Structure Design

## Date
2026-08-04

## Context
Setting up a teach-skill workspace to produce children's reading modules and teacher aids based on Denise Eide's *Uncovering the Logic of English*. The source material is a 48KB curriculum.md with full scope & sequence, 75 phonograms, 31 spelling rules, and methodology.

## Decision
Split output into two categories with the same shared assets:

1. **`reference/`** — Teacher aids: single-page HTML quick-references organized beginner→advanced (quickstart → phonogram chart → spelling rules → spelling analysis protocol → word lists → high-frequency words → troubleshooting → morpheme wall)

2. **`lessons/`** — Children's learning modules: numbered HTML files (`0001-xxxx.html`) that a parent walks through with the child. Each is interactive (click-to-reveal, write-boxes, quiz elements), self-contained, and completable in 15-20 minutes.

3. **`assets/main.css`** — Shared stylesheet for consistent look across all materials.

## Rationale
- Teacher aids need to be scannable mid-lesson — dense, tabular, with rule numbers and examples upfront.
- Children's lessons need progressive disclosure — one concept at a time, immediate feedback, celebration at end.
- Both share the same typographic system via `main.css` so the course feels like one product.
- HTML over Markdown because interactive elements (quizzes, reveal buttons, click-to-confirm-phonograms) require JavaScript.
- All offline-capable: no CDN dependencies, no build step, opens in any browser, prints cleanly.

## Key Insight
The phonogram chart teacher aid became the most complex reference — a responsive CSS grid of 75+ cards, each showing phonogram, sounds in frequency order, and example words. Getting the print layout right (fitting on 2-3 pages) required significant grid-tuning. Lesson learned: design for print first, then add interactivity for screen.

## Related
- `NOTES.md` — working task list
- `MISSION.md` — mission and constraints
- `RESOURCES.md` — trusted sources
