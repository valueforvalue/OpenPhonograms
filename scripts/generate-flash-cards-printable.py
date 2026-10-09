#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate double-sided printable phonogram flash cards (one PDF per stage).

Each stage PDF is designed for duplex printing on letter paper:
  - Side A (odd pages): phonogram symbol, all sounds, rule reference
  - Side B (even pages): just the phonogram symbol (clean, for memory drills)
  - Dashed cut lines around each card
  - Cards per page: 4 (2×2 grid, ~3.5×4.75in cutout)

Pages are ordered for duplex: A-pg1, B-pg1, A-pg2, B-pg2, ...
When printed double-sided (flip on long edge), front/back align for cutting.

Usage:
  python scripts/generate-flash-cards-printable.py [--stage N] [--no-render]

Output: build/flash-cards/stage-N-printable-cards.pdf
"""

import argparse
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from framework.data_loader import load_phonograms, load_rules

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "flash-cards"
BUILD.mkdir(parents=True, exist_ok=True)

# ── Rule references keyed by phonogram ────────────────────────────────────
# Maps phonogram ids to relevant rule numbers. Only phonogram-specific
# spelling rules are listed — general rules (syllable, suffix, plural, etc.)
# are omitted since they apply broadly, not to a single phonogram.
PG_RULES: dict[str, list[str]] = {
    "c":   ["1"],    # C softens to /s/ before E, I, Y
    "g":   ["2"],    # G may soften to /j/ before E, I, Y
    "qu":  ["11"],   # Q always needs U
    "ay":  ["9"],    # AY for /ā/ at end
    "ck":  ["26"],   # CK after short vowel
    "dge": ["25"],   # DGE after short vowel
    "tch": ["27"],   # TCH after short/broad vowel
    "ti":  ["17"],   # Latin /sh/ — TI, CI, SI
    "ci":  ["17"],
    "si":  ["17"],
    "igh": ["28"],   # GH phonograms
    "eigh": ["28"],
    "augh": ["28"],
    "ough": ["28"],
    "silent_e": ["12"],  # Silent E — nine reasons
}

# ── CSS ───────────────────────────────────────────────────────────────────

PAGE_CSS = """
@page {
    size: letter;
    margin: 0.4in;
}
body {
    font-family: "Atkinson Hyperlegible", "Georgia", serif;
    margin: 0;
    padding: 0;
}
.card-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 0.25in;
    width: 100%;
    height: calc(11in - 0.8in - 0.25in);  /* page content (10.2in) minus inter-row gap (0.25in) */
    box-sizing: border-box;
    break-after: page;
    page-break-after: always;  /* legacy alias for older renderers */
}
.card-grid:last-child {
    break-after: auto;
    page-break-after: auto;
}
/* Tiny print-instructions banner shown only on page 1 of each stage PDF.
   Page 1 grid uses .first-page which trims card height so cards fit
   alongside the banner without changing card widths. */
.print-instructions {
    font-size: 7pt;
    color: #666;
    text-align: center;
    margin: 0 auto 0.08in auto;
    padding-bottom: 0.04in;
    border-bottom: 1px dotted #999;
    width: 100%;
    line-height: 1.2;
}
.print-instructions strong { color: #333; }
.card-grid.first-page {
    height: calc(11in - 0.8in - 0.25in - 0.3in); /* shrink for banner (0.3in incl. margins) */
    margin-top: 0;
}
.card-grid.first-page .card {
    padding: 0.2in;  /* tighter card padding so content fits smaller card */
}

/* Side B content is mirrored left-to-right in the PDF so that short-edge
   duplex printing aligns each card behind its Side A counterpart. When the
   sheet is flipped to view the back side, left and right swap; pre-mirroring
   Side B cancels that flip and leaves each card directly behind its Side A
   position. */
.card-grid.side-b {
    transform: scaleX(-1);
    transform-origin: center center;
}
.card-grid.side-b .card .pg,
.card-grid.side-b .card .ex-block {
    /* Counter-mirror card content so letters aren't backwards */
    transform: scaleX(-1);
    display: inline-block;
}
.card {
    border: 2px dashed #888;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0.3in;
    box-sizing: border-box;
    position: relative;
}
/* Side A styling */
.card-side-a .pg {
    font-size: 64pt;
    font-weight: 700;
    color: #2a5c8a;
    line-height: 1.1;
    margin-bottom: 0.2em;
}
.card-side-a .sounds {
    font-size: 16pt;
    color: #555;
    font-family: "Courier New", monospace;
    margin-bottom: 0.3em;
}
.card-side-a .rule-ref {
    font-size: 9pt;
    color: #888;
    font-style: italic;
    margin-top: auto;
    padding-top: 0.3em;
    border-top: 1px solid #ddd;
    width: 100%;
}
/* Side B styling — phonogram + example words */
.card-side-b .pg {
    font-size: 80pt;
    font-weight: 700;
    color: #2a5c8a;
    line-height: 1.1;
}
.card-side-b .ex-block {
    margin-top: 0.2em;
    font-size: 14pt;
    color: #444;
    line-height: 1.35;
}
.card-side-b .ex-block .ex {
    font-family: "Courier New", monospace;
}
/* Vowel / consonant color variants on side A */
.card.vowel .pg { color: #a8421a; }
.card.consonant .pg { color: #2a7d2a; }
/* Side B always navy regardless of vowel/consonant */
.card-side-b .pg {
    color: #2a5c8a !important;
}
/* Multi-letter phonograms: slightly smaller on side A to fit */
.card.multi .pg { font-size: 48pt; }
.card-side-b.multi .pg { font-size: 56pt; }
"""

# ── Card HTML builders ────────────────────────────────────────────────────


def build_card_side_a(pg, rules_lookup: dict[str, str]) -> str:
    """Side A: phonogram + sounds + rule reference."""
    is_vowel = pg.vowel
    is_multi = pg.kind != "single"
    kind_class = "vowel" if is_vowel else "consonant"
    if is_multi:
        kind_class += " multi"

    rule_nums = PG_RULES.get(pg.id, [])
    rule_text = ""
    if rule_nums:
        rule_names = []
        for rn in rule_nums:
            if rn in rules_lookup:
                rule_names.append(f"Rule {rn}: {rules_lookup[rn]}")
        if rule_names:
            rule_text = "; ".join(rule_names)

    return f"""<div class="card {kind_class} card-side-a">
    <div class="pg">{pg.id}</div>
    <div class="sounds">{pg.sounds}</div>
    {f'<div class="rule-ref">{rule_text}</div>' if rule_text else '<div class="rule-ref"></div>'}
</div>"""


def build_card_side_b(pg) -> str:
    """Side B: phonogram + one example word per distinct sound."""
    is_multi = pg.kind != "single"
    multi_class = "multi" if is_multi else ""
    ex_lines = ""
    if pg.examples:
        ex_lines = "\n".join(
            f'<div class="ex">{words.split(",")[0].strip()}</div>'
            for _, words in pg.examples
        )
    elif pg.words:
        ex_lines = f'<div class="ex">{pg.words[0]}</div>'
    ex_block = f'<div class="ex-block">{ex_lines}</div>' if ex_lines else ""
    return f"""<div class="card {multi_class} card-side-b">
    <div class="pg">{pg.id}</div>
    {ex_block}
</div>"""


def build_page(cards_html: str, side: str, *, show_instructions: bool = False) -> str:
    """Wrap cards in a page grid. `show_instructions` adds a tiny print
    banner above the grid (page 1 only). The banner is a sibling div, not
    inside the grid, so the 2×2 layout is unaffected."""
    side_class = f" side-{side.lower()}" if side.lower() == "b" else ""
    page_class = " first-page" if show_instructions else ""
    banner = ""
    if show_instructions:
        banner = ('<div class="print-instructions">'
                  'Print <strong>double-sided, flip on long edge</strong>. '
                  'Cut along dashed lines. Side A = phonogram + sounds + rule; '
                  'Side B = phonogram + example words (for memory drills).</div>')
    return f"""{banner}<div class="card-grid{side_class}{page_class}">
{cards_html}
</div>"""


# ── Main generator ────────────────────────────────────────────────────────


def generate_stage_pdf(stage: int, no_render: bool = False) -> Path | None:
    """Generate double-sided flash card PDF for one stage."""
    from weasyprint import HTML as WHTML

    # Load phonograms for this stage, ordered by group/id
    all_pgs = load_phonograms()
    stage_pgs = [p for p in all_pgs if p.stage == stage]

    if not stage_pgs:
        print(f"  Stage {stage}: no phonograms — skipping")
        return None

    # Load rules for lookup
    rules_lookup: dict[str, str] = {}
    for r in load_rules():
        rules_lookup[r.number] = r.name

    CARDS_PER_PAGE = 4

    # Build pages: side A then side B for each group of 4 cards.
    # The very first page of each stage shows a tiny print-instructions banner.
    html_pages: list[str] = []
    first_page = True
    for i in range(0, len(stage_pgs), CARDS_PER_PAGE):
        batch = stage_pgs[i:i + CARDS_PER_PAGE]

        # Side A
        side_a_cards = "\n".join(build_card_side_a(pg, rules_lookup) for pg in batch)
        html_pages.append(build_page(side_a_cards, "A", show_instructions=first_page))

        # Side B — same card positions for duplex alignment
        side_b_cards = "\n".join(build_card_side_b(pg) for pg in batch)
        html_pages.append(build_page(side_b_cards, "B"))

        first_page = False

    # Assemble full HTML document
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>{PAGE_CSS}</style></head>
<body>
{"".join(html_pages)}
</body></html>"""

    out_path = BUILD / f"stage-{stage}-printable-cards.pdf"
    WHTML(string=full_html).write_pdf(str(out_path))

    total_cards = len(stage_pgs)
    total_pages = len(html_pages)
    print(f"  Stage {stage}: {total_cards} cards, {total_pages} pages → {out_path.relative_to(ROOT)}")
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate double-sided printable phonogram flash cards per stage"
    )
    parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4, 5],
                        help="Build only one stage (default: all)")
    parser.add_argument("--no-render", action="store_true",
                        help="Skip PDF rendering (HTML only)")
    args = parser.parse_args()

    stages = [args.stage] if args.stage else [1, 2, 3, 4, 5]

    print("==> Generating double-sided printable flash cards")
    for s in stages:
        generate_stage_pdf(s, no_render=args.no_render)
    print(f"\nDone! Output in {BUILD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
