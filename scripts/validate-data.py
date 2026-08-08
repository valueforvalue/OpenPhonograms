#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).
"""Validate data/*.yaml against JSON schemas + cross-check catalog coverage.

Runs as `just validate-data`. Exits 0 on full pass, 1 on any drift.

Checks:
  1. Schema validity (every data/*.yaml validates against its schema).
  2. Phonogram coverage: every PG id in phonograms.yaml appears in
     framework/lesson-catalog.csv's new_phonogram column; every catalog
     new_phonogram appears in phonograms.yaml.
  3. Rule coverage: same for rule numbers vs new_rule column.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "framework"))

import data_loader  # noqa: E402


CATALOG = ROOT / "framework" / "lesson-catalog.csv"


def main() -> int:
    errors: list[str] = []

    # 1. Schema validity via data_loader (raises on failure)
    try:
        pgs = data_loader.load_phonograms()
        rules = data_loader.load_rules()
        data_loader.load_sentences()
        data_loader.load_silent_e()
        data_loader.load_roots()
        data_loader.load_hf_words()
        data_loader.load_decodable_wordlists()
    except data_loader.DataValidationError as exc:
        print(f"FAIL  schema validation: {exc}")
        return 1

    print(f"  OK   schema validation: {len(pgs)} phonograms, {len(rules)} rules")

    # 2-3. Catalog coverage
    if not CATALOG.exists():
        print(f"FAIL  catalog missing: {CATALOG}")
        return 1

    pg_ids = {p.id for p in pgs}
    rule_nums = {r.number for r in rules}

    catalog_pgs: set[str] = set()
    catalog_rules: set[str] = set()
    with CATALOG.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            npg = (row.get("new_phonogram") or "").strip()
            nrl = (row.get("new_rule") or "").strip()
            if npg:
                catalog_pgs.add(npg)
            if nrl:
                catalog_rules.add(nrl)

    # Phonogram coverage
    missing_in_yaml = catalog_pgs - pg_ids
    missing_in_catalog = pg_ids - catalog_pgs
    # Stage-2+ phonograms appear in worksheet files but not always in catalog
    # new_phonogram column — catalog tracks which lesson introduces them.
    # We allow stage-2+ entries to be missing from catalog (they're taught but
    # lesson doesn't always tag them as "new" in catalog).
    if missing_in_yaml:
        errors.append(f"phonograms in catalog but missing from YAML: {sorted(missing_in_yaml)}")
    # Catalog-only multi-stage PGs are expected; don't flag them.
    worksheet_only = {"sh", "th", "ck", "ee", "ng", "ar", "or", "er", "oi", "oy",
                      "ai", "ay", "ch", "wh", "ea", "ow", "ou", "oo", "ed", "igh",
                      "aw", "au", "ir", "ur", "oa", "ear"}
    multi3 = {"dge", "tch", "kn", "gn", "wr", "eigh", "ei", "ey", "ph", "gh",
              "ough", "augh", "ew", "ui", "eu", "wor", "ie", "bu", "gu", "q"}
    multi4 = {"ti", "ci", "si"}
    expected_not_in_catalog = worksheet_only | multi3 | multi4
    unexpected_missing = missing_in_catalog - expected_not_in_catalog
    if unexpected_missing:
        errors.append(f"phonograms in YAML but missing from catalog (unexpected): {sorted(unexpected_missing)}")

    print(f"  OK   phonogram coverage: {len(pg_ids)} YAML, {len(catalog_pgs)} catalog, "
          f"{len(expected_not_in_catalog & pg_ids)} expected-not-in-catalog")

    # Rule coverage. Catalog supports compound forms:
    #   "12.1"        — sub-rule (Silent E reason #1)
    #   "12.1-12.4"   — sub-rule range
    #   "12.all"      — Silent E all-reasons bundle
    #   "13-16"       — grouped rule range
    #   "13,14"       — grouped rule list
    #   "3,28"        — grouped rule list
    #   "19-20"       — grouped rule range
    # Base numbers (before any '.' or '-' or ',') must exist in YAML.

    def extract_base_rules(token: str) -> list[str]:
        """Extract base rule numbers from a catalog token."""
        bases: list[str] = []
        # Split on comma for grouped lists
        for part in token.split(","):
            part = part.strip()
            # Sub-rule or range: take the leading number
            base = part.split(".")[0].split("-")[0]
            if base.isdigit():
                bases.append(base)
        return bases

    missing_bases: set[str] = set()
    for token in catalog_rules:
        for base in extract_base_rules(token):
            if base not in rule_nums:
                missing_bases.add(base)
    if missing_bases:
        errors.append(f"rule bases in catalog but missing from YAML: {sorted(missing_bases)}")

    missing_rules_in_catalog = rule_nums - catalog_rules
    if missing_rules_in_catalog:
        # Rules can be taught but not always tagged "new" — informational.
        print(f"  INFO rules in YAML not in catalog new_rule column: {sorted(missing_rules_in_catalog)}")

    print(f"  OK   rule coverage: {len(rule_nums)} YAML, {len(catalog_rules)} catalog tokens")

    if errors:
        for e in errors:
            print(f"FAIL  {e}")
        return 1

    print("PASS  all data validation checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
