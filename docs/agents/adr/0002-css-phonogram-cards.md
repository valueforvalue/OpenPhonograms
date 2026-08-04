# ADR 0002: CSS-Rendered Phonogram Cards

**Status:** Accepted  
**Date:** 2025-08-03  
**Supersedes:** None

## Context

Phonogram flash cards were initially planned as AI-generated images (PNG files). After generating 6 sample cards, it became clear that:

1. Text-based cards are higher quality (no rendering artifacts)
2. No AI generation needed (saves cost and iteration time)
3. CSS styling (Georgia font, navy #2a5c8a, bordered card) matches print aesthetic
4. Override path preserved: drop a PNG into `images/phonograms/<letter>.png` and render.py uses it

## Decision

Individual phonogram cards are pure text/CSS. Generated inline in lesson markdown via `<div class="phonogram">` blocks. Wall charts (`all-single.png`, `all-multi.png`) remain as images (large reference posters).

## Consequences

- Positive: Zero AI image cost for ~75 cards
- Positive: Always crisp at any print resolution
- Positive: Typography-consistent with print materials
- Negative: Requires CSS support in render path (weasyprint handles this)
- Negative: Cannot have illustrated phonogram cards (e.g., "a is for apple" with artwork)
