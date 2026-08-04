"""Cross-reference validator for phonogram and rule worksheets.

Checks:
  1. Every phonogram taught in the catalog has a matching pg-*.md worksheet.
  2. Every spelling rule in the catalog has a matching rule-*.md worksheet.
  3. Every worksheet file corresponds to a phonogram/rule actually taught.

Exit codes:
  0 = all checks pass
  1 = coverage gap (worksheet missing for a PG/rule)
  2 = orphan (worksheet exists but no lesson teaches it)

Usage:
  python scripts/check-worksheet-coverage.py
  python scripts/check-worksheet-coverage.py --quiet    # only print problems
"""

import argparse
import csv
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "framework" / "lesson-catalog.csv"
PG_WS_DIR = ROOT / "worksheets" / "phonograms"
RULE_WS_DIR = ROOT / "worksheets" / "rules"


def load_catalog() -> list[dict]:
    with open(CATALOG, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description="Validate worksheet coverage")
    parser.add_argument("--quiet", action="store_true", help="Only print problems")
    args = parser.parse_args()

    if not CATALOG.exists():
        print(f"Error: catalog not found at {CATALOG}")
        sys.exit(2)

    catalog = load_catalog()

    # Collect all phonograms and rules actually taught in lessons
    pgs_taught = set()
    rules_taught = set()
    for row in catalog:
        pg = (row.get("new_phonogram") or "").strip()
        if pg:
            pgs_taught.add(pg)
        rule = (row.get("new_rule") or "").strip()
        if rule:
            # Expand rule spec into individual rule numbers.
            # Examples:
            #   '12'       -> {'12'}
            #   '12.1'     -> {'12'}      (sub-rule maps to parent)
            #   '12.all'   -> {'12'}
            #   '17,18'    -> {'17', '18'}
            #   '19-20'    -> {'19', '20'}
            #   '13-14'    -> {'13', '14'}
            #   '1+2'      -> {'1', '2'}
            parts = re.split(r"[,+]", rule)
            for part in parts:
                # Strip sub-rule: '12.1' -> '12'
                base = re.split(r"\.", part, maxsplit=1)[0]
                # Range: '13-14' -> '13', '14'
                if "-" in base:
                    m = re.match(r"^(\d+)-(\d+)$", base)
                    if m:
                        lo, hi = int(m.group(1)), int(m.group(2))
                        for n in range(lo, hi + 1):
                            rules_taught.add(str(n))
                    else:
                        rules_taught.add(base)
                else:
                    rules_taught.add(base)

    # Collect existing worksheets
    pg_worksheets = {p.stem.replace("pg-", "") for p in PG_WS_DIR.glob("pg-*.md")}
    rule_worksheets = {p.stem.replace("rule-", "") for p in RULE_WS_DIR.glob("rule-*.md")}

    # Coverage gaps (catalog has PG/rule but no worksheet)
    missing_pg = pgs_taught - pg_worksheets
    missing_rule = rules_taught - rule_worksheets

    # Orphans (worksheet exists but no catalog entry)
    orphan_pg = pg_worksheets - pgs_taught
    orphan_rule = rule_worksheets - rules_taught

    if not args.quiet:
        print(f"==> Worksheet coverage check")
        print(f"  Catalog phonograms taught:  {len(pgs_taught)}")
        print(f"  Phonogram worksheets:       {len(pg_worksheets)}")
        print(f"  Catalog rules taught:       {len(rules_taught)}")
        print(f"  Rule worksheets:            {len(rule_worksheets)}")

    problems = []

    if missing_pg:
        problems.append(("MISSING-PG", sorted(missing_pg)))
    if missing_rule:
        problems.append(("MISSING-RULE", sorted(missing_rule)))
    if orphan_pg:
        problems.append(("ORPHAN-PG", sorted(orphan_pg)))
    if orphan_rule:
        problems.append(("ORPHAN-RULE", sorted(orphan_rule)))

    if not args.quiet and not problems:
        print(f"\n  Coverage: 100%")

    if problems:
        if not args.quiet:
            print()
            print("Problems:")
        for kind, items in problems:
            label = {
                "MISSING-PG": "MISSING-PG",
                "MISSING-RULE": "MISSING-RULE",
                "ORPHAN-PG": "ORPHAN-PG",
                "ORPHAN-RULE": "ORPHAN-RULE",
            }[kind]
            print(f"  {label}  ({len(items)}): {', '.join(items)}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
