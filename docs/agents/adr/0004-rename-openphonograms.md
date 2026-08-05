# ADR-0004: Rename project to "OpenPhonograms"

- **Status:** Accepted (2026-08-05)
- **Closes:** #39, #40
- **Deciders:** Jeremy Morris (project owner)
- **Reviewed by:** No legal counsel (decision deferred for now)

## Context

The project is an open-source adaptation of *Uncovering the Logic of
English* by Denise Eide (2012). The current name directly borrows the
source book's title, which creates two issues:

1. **Trademark risk:** "Logic of English" is an active trademark of
   Logic of English, Inc. The full title "Uncovering the Logic of
   English" is also part of their brand. Using it as a project name
   suggests an official or endorsed connection that doesn't exist.
2. **Confusing attribution:** Readers see the project name and may
   assume it's an official Logic of English product. The current
   trademark disclaimer in NOTICE + README mitigates but doesn't
   eliminate the confusion.

## Decision

**Rename the project from "Uncovering the Logic of English" to
"OpenPhonograms".** This follows the "Open Phonograms" direction from
#40 (fully distinct name, option 3 in #39) and the precedent set by
LibreOffice / OpenBSD (fork/adaptation projects that choose distinct
names to avoid TM conflicts).

The new name:
- Describes what the project IS (a phonogram-based reading curriculum)
- Uses the generic "Open" prefix to signal community/open-source
- Contains no trademarked terms
- Is short and memorable

## What changes

- Project self-references: README, AGENTS.md, curriculum.md, all docs
- File titles: README.md, docs/BUILD.md, docs/USE.md, etc.
- Code-level references: docstrings, comments, file headers
- Game HTML title: `Phonogram Trainer — OpenPhonograms`
- NOTICE file: project name in the header

## What does NOT change

The **source attribution** must continue to name the source book by
its full title, as required by the SIL OFL notice (for the bundled
Atkinson Hyperlegible font) and the project LICENSE. The footer:

> *Source: Adapted from the methodology of Uncovering the Logic of
> English by Denise Eide. License: MIT — see LICENSE.*

...remains unchanged. The project name in footers/attribution is now
"OpenPhonograms" (the new project name), and the source methodology
remains "Uncovering the Logic of English" (the source book).

Citation format (in NOTICE, curriculum.md, etc.):

> Eide, Denise. *Uncovering the Logic of English: A Common-Sense
> Approach to Reading and Spelling.* 2nd ed. Logic of English, Inc.,
> 2012.

...remains unchanged.

## Trademark disclaimer (strengthened)

NOTICE adds a clearer disclaimer:

> OpenPhonograms is NOT affiliated with, endorsed by, or sponsored by
> Logic of English, Inc. "Logic of English" and "Uncovering the Logic
> of English" are trademarks of Logic of English, Inc. This project is
> an independent, open-source adaptation of the methodology described in
> the source book.

## Alternatives considered

- **"Open Logic of English"** (option 2 in #39): contains the TM
  "Logic of English". Would require explicit permission from LoE, Inc.
  or rely on narrow nominative fair use. Rejected as TM risk.
- **"Open LoE"** (option 4 in #39): same TM problem, even shorter.
- **Keep "Uncovering the Logic of English"** (option 1 in #39): cheapest
  but trademark risk remains, attribution confusion persists.

## Risks and mitigations

- **Loss of descriptive connection:** "OpenPhonograms" is less
  descriptive of the source. Mitigated by clear NOTICE + README
  attribution to the source book.
- **GitHub repo URL change:** breaks inbound links. Mitigated by GitHub's
  built-in redirect on rename.
- **PDF releases in the wild:** old PDFs are named after the old
  project. New PDFs will use "OpenPhonograms" branding. No re-issue
  of old PDFs is needed since they're correctly attributed to the
  source book.

## Followup actions

- [ ] Bulk rename across MD/Python/HTML files (~1400 occurrences)
- [ ] Update game HTML title
- [ ] Re-render all PDFs (`just render-all`)
- [ ] Verify all PDFs pass `just check-pdf-credits`
- [ ] Update GitHub repo name (out of scope of this repo)
- [ ] Add CHANGELOG entry noting the rename

## Notes

This is a strategic decision, not a legal one. If Logic of English,
Inc. ever objects to the use of "OpenPhonograms" (e.g., claims it
sounds too similar to their product line), we may need to rename
again. The current name is generic enough that this is unlikely.
