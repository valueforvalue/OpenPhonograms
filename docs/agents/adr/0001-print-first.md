# ADR 0001: Print-First Design

**Status:** Accepted  
**Date:** 2025-08-03

## Context

The curriculum needed a delivery format. Options: web app, PDF, printed book, HTML.

## Decision

Print-first. All content authored in markdown, rendered to PDF via weasyprint. CSS targets letter-size paper with 0.75in margins. No JavaScript dependency for core content delivery.

## Consequences

- Positive: Offline-capable, no device required for use, photocopy-friendly worksheets
- Positive: Single source (markdown) → multiple outputs (PDF, HTML via browser print)
- Negative: Interactive features (audio, games) must be separate self-contained HTML files
- Negative: Table width constrained to ~6.5in (letter minus margins)
