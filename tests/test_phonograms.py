"""Tests for framework/data_loader.py - the YAML-backed single source of truth.

Issue #22/#23 refactor: phonogram + rule catalogs extracted from
data/phonograms.yaml + rules.yaml (YAML source), loaded via
framework/data_loader. This test file guards the loaders' public API
and ensures the catalog stays consistent with the lesson catalog.
"""

import csv
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "framework"))

from data_loader import (  # noqa: E402
    Phonogram, Rule,
    load_phonograms, load_rules,
    pg_dict, pg_stage_dict, pg_stage_buckets, pg_kind_buckets,
    rules_dict, rules_by_number,
)


# ── Loader API surface ─────────────────────────────────────────────────

class TestPhonogramsLoader:
    """Public API exposed by framework/data_loader for phonograms."""

    def test_load_phonograms_returns_tuple(self):
        pgs = load_phonograms()
        assert isinstance(pgs, tuple)
        assert len(pgs) >= 75  # 76 with qu, but spec is 75+

    def test_phonogram_dataclass_fields(self):
        """Every entry must be a Phonogram dataclass with id, sounds, words, stage."""
        for p in load_phonograms():
            assert isinstance(p, Phonogram)
            assert isinstance(p.id, str) and p.id
            assert isinstance(p.sounds, str) and p.sounds.strip()
            assert isinstance(p.words, tuple) and len(p.words) >= 10
            assert p.stage in {1, 2, 3, 4, 5}

    def test_pg_dict_shape(self):
        """pg_dict() returns {pg_id: {sounds, words, stage}}."""
        d = pg_dict()
        assert isinstance(d, dict)
        assert "a" in d
        assert d["a"]["sounds"] == "/ă/ /ā/ /ä/"
        assert isinstance(d["a"]["words"], list)

    def test_pg_kind_buckets_split(self):
        """pg_kind_buckets() splits by kind (single/multi/multi3/multi4)."""
        b = pg_kind_buckets()
        assert set(b.keys()) == {"single", "multi", "multi3", "multi4"}
        assert len(b["single"]) >= 26  # a-z + qu
        assert len(b["multi"]) >= 25  # Stage 2
        assert len(b["multi3"]) >= 15  # Stage 3+
        assert len(b["multi4"]) >= 3   # ti, ci, si

    def test_pg_stage_dict_and_buckets(self):
        """pg_stage_dict() and pg_stage_buckets() agree."""
        sd = pg_stage_dict()
        sb = pg_stage_buckets()
        for pg, stage in sd.items():
            assert pg in sb[stage]

    def test_kind_ordering_preserved(self):
        """Teaching order matches legacy SINGLE/MULTI ordering."""
        # Teaching order is locked in pg_kind_buckets()
        b = pg_kind_buckets()
        # SINGLE should be a-z + qu (qu between p and r)
        singles = list(b["single"].keys())
        assert singles[0] == "a" and singles[-1] == "z"
        # qu appears between p and r
        assert "qu" in singles
        assert singles.index("p") < singles.index("qu") < singles.index("r")
        # MULTI starts with sh, th, ck (Stage 2 first wave)
        assert list(b["multi"].keys())[:3] == ["sh", "th", "ck"]


class TestRulesLoader:
    """Public API exposed by framework/data_loader for rules."""

    def test_load_rules_returns_tuple(self):
        rules = load_rules()
        assert isinstance(rules, tuple)
        assert len(rules) == 31

    def test_rule_dataclass_fields(self):
        for r in load_rules():
            assert isinstance(r, Rule)
            assert isinstance(r.number, str)
            assert isinstance(r.name, str) and r.name
            assert isinstance(r.words, tuple) and len(r.words) >= 5
            assert r.stage in {1, 2, 3, 4}

    def test_rules_dict_shape(self):
        d = rules_dict()
        assert isinstance(d, dict)
        assert "1" in d and "31" in d
        assert d["3"]["name"].startswith("No English word")

    def test_rules_by_number(self):
        d = rules_by_number()
        assert "3" in d
        assert d["3"].number == "3"


# ── Consistency with lesson catalog ───────────────────────────────────

class TestCatalogConsistency:
    """data/*.yaml must agree with framework/lesson-catalog.csv."""

    @pytest.fixture(scope="class")
    def catalog_pgs(self):
        pgs = set()
        with open(PROJECT_ROOT / "framework" / "lesson-catalog.csv",
                  encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                pg = row.get("new_phonogram", "").strip()
                if pg:
                    pgs.add(pg)
        return pgs

    def test_all_catalog_pgs_have_entries(self, catalog_pgs):
        """Every PG declared in lesson-catalog.csv must be in YAML."""
        all_pgs = set(pg_dict().keys())
        missing = catalog_pgs - all_pgs
        assert not missing, f"PGs in catalog but not in YAML: {missing}"

    def test_no_orphan_pgs(self, catalog_pgs):
        """No PG in YAML is missing from the catalog."""
        all_pgs = set(pg_dict().keys())
        orphans = all_pgs - catalog_pgs
        assert not orphans, f"PGs in YAML but not in lesson catalog: {orphans}"


# ── Data quality ──────────────────────────────────────────────────────

class TestDataQuality:
    """Each entry must have non-empty sounds + at least 10 words."""

    @pytest.mark.parametrize("kind", ["single", "multi", "multi3", "multi4"])
    def test_entries_have_required_fields(self, kind):
        for pg, data in pg_kind_buckets()[kind].items():
            assert data["sounds"].strip(), f"{kind}[{pg}] has empty sounds"
            assert len(data["words"]) >= 10, (
                f"{kind}[{pg}] has only {len(data['words'])} words "
                f"(expected >=10)"
            )

    def test_words_are_lowercase(self):
        """Words should be lowercase for consistent display (proper-noun exceptions allowed)."""
        ALLOWED_CAPS = {"June", "July", "August", "Paul", "Philip", "Europe", "Thursday", "Saturday", "Iraq", "Iraqi"}
        for kind in ["single", "multi", "multi3", "multi4"]:
            for pg, data in pg_kind_buckets()[kind].items():
                for w in data["words"]:
                    if w != w.lower() and w not in ALLOWED_CAPS:
                        pytest.fail(
                            f"{kind}[{pg}] contains unexpected capitalized word: {w!r}"
                        )
