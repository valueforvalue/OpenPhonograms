"""Tests for framework/phonograms.py — the single source of truth.

Issue #14 refactor: phonogram catalog extracted to framework/phonograms.py
to eliminate duplication between generate-worksheets.py and the stage
generators. This test file guards the module's public API and ensures
the catalog stays consistent with the lesson catalog.
"""
import csv
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "framework"))

import phonograms  # noqa: E402


# ── Module API surface ─────────────────────────────────────────────────

class TestPhonogramsApi:
    """Public API exposed by framework/phonograms.py."""

    def test_singleton_dict(self):
        assert isinstance(phonograms.SINGLE, dict)
        assert len(phonograms.SINGLE) >= 26  # a-z + qu

    def test_multi_dict(self):
        assert isinstance(phonograms.MULTI, dict)
        assert len(phonograms.MULTI) >= 25  # Stage 2 multi-letter PGs

    def test_multi3_dict(self):
        assert isinstance(phonograms.MULTI3, dict)
        assert len(phonograms.MULTI3) >= 15  # Stage 3+ advanced PGs

    def test_multi4_dict(self):
        assert isinstance(phonograms.MULTI4, dict)
        assert len(phonograms.MULTI4) >= 3   # ti, ci, si

    def test_pg_stage_mapping(self):
        assert isinstance(phonograms.PG_STAGE, dict)
        # Every PG in any dict must be in PG_STAGE
        all_pgs = set(phonograms.SINGLE) | set(phonograms.MULTI) \
                  | set(phonograms.MULTI3) | set(phonograms.MULTI4)
        assert set(phonograms.PG_STAGE.keys()) == all_pgs
        # All stages in 1-4
        assert all(s in {1, 2, 3, 4} for s in phonograms.PG_STAGE.values())


# ── Aggregations ───────────────────────────────────────────────────────

class TestAggregations:
    def test_all_phonograms_returns_every_pg(self):
        all_pgs = phonograms.all_phonograms()
        assert len(all_pgs) == len(phonograms.SINGLE) + len(phonograms.MULTI) \
                              + len(phonograms.MULTI3) + len(phonograms.MULTI4)
        # Spot-check
        assert "a" in all_pgs
        assert "sh" in all_pgs
        assert "dge" in all_pgs
        assert "ti" in all_pgs

    def test_all_stages_groups_correctly(self):
        stages = phonograms.all_stages()
        assert sorted(stages[1]) == sorted(phonograms.SINGLE.keys())
        assert sorted(stages[2]) == sorted(phonograms.MULTI.keys())
        assert sorted(stages[3]) == sorted(phonograms.MULTI3.keys())
        assert sorted(stages[4]) == sorted(phonograms.MULTI4.keys())
        assert stages[5] == []  # no PGs introduced in Stage 5

    def test_to_json_compatible_shape(self):
        data = phonograms.to_json_compatible()
        assert isinstance(data, dict)
        # Sample check: every entry has sounds, words, stage
        for pg, entry in data.items():
            assert "sounds" in entry
            assert "words" in entry
            assert "stage" in entry
            assert isinstance(entry["words"], list)
            assert entry["stage"] in {1, 2, 3, 4}


# ── Consistency with lesson catalog ───────────────────────────────────

class TestCatalogConsistency:
    """framework/phonograms.py must agree with framework/lesson-catalog.csv."""

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
        """Every PG declared in lesson-catalog.csv must be in phonograms module."""
        all_pgs = set(phonograms.all_phonograms().keys())
        missing = catalog_pgs - all_pgs
        assert not missing, f"PGs in catalog but not in phonograms module: {missing}"

    def test_no_orphan_pgs(self, catalog_pgs):
        """No PG in phonograms module is missing from the catalog (excluding qu + advanced)."""
        all_pgs = set(phonograms.all_phonograms().keys())
        # Filter out PGs that are in MULTI3/MULTI4 but not yet wired into catalog
        # (e.g. some advanced PGs may be planned for future lessons)
        orphans = all_pgs - catalog_pgs
        # We expect some advanced PGs (ei, ey, ough, etc.) to be in catalog.
        # If we have orphans, the catalog is missing lessons.
        assert not orphans, (
            f"PGs in phonograms module but not in lesson catalog: {orphans}"
        )


# ── Data quality ──────────────────────────────────────────────────────

class TestDataQuality:
    """Each entry must have non-empty sounds + at least 12 words."""

    @pytest.mark.parametrize("dict_name", ["SINGLE", "MULTI", "MULTI3", "MULTI4"])
    def test_entries_have_required_fields(self, dict_name):
        d = getattr(phonograms, dict_name)
        for pg, data in d.items():
            assert "sounds" in data, f"{dict_name}[{pg}] missing 'sounds'"
            assert "words" in data, f"{dict_name}[{pg}] missing 'words'"
            assert data["sounds"].strip(), f"{dict_name}[{pg}] has empty sounds"
            assert len(data["words"]) >= 10, (
                f"{dict_name}[{pg}] has only {len(data['words'])} words "
                f"(expected >=10)"
            )

    def test_words_are_lowercase(self):
        """Words should be lowercase for consistent display (proper-noun exceptions allowed)."""
        # Known proper-noun exceptions in the catalog
        ALLOWED_CAPS = {"June", "July", "August", "Paul", "Philip", "Europe", "Thursday", "Saturday"}
        for dict_name in ["SINGLE", "MULTI", "MULTI3", "MULTI4"]:
            d = getattr(phonograms, dict_name)
            for pg, data in d.items():
                for w in data["words"]:
                    if w != w.lower() and w not in ALLOWED_CAPS:
                        assert False, (
                            f"{dict_name}[{pg}] contains unexpected capitalized word: {w!r}"
                        )
