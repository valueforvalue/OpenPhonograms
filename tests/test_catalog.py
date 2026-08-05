"""Tests for the lesson catalog (framework/lesson-catalog.csv).

The catalog is the source of truth for:
- Stage ordering (1-5)
- Lesson numbering within each stage
- New phonograms/rules introduced at each lesson
- Image and reader references

Every test here is a regression check on the catalog's internal consistency.
"""
import csv
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def catalog():
    with open(PROJECT_ROOT / "framework" / "lesson-catalog.csv",
              encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_catalog_has_required_columns(catalog):
    if not catalog:
        pytest.skip("catalog empty")
    required = {"stage", "lesson_num", "lesson_id", "title", "type",
                "new_phonogram", "new_rule", "word_list", "reader",
                "image_needed"}
    assert required.issubset(set(catalog[0].keys())), (
        f"Missing columns: {required - set(catalog[0].keys())}"
    )


def test_every_lesson_has_unique_id(catalog):
    ids = [r["lesson_id"] for r in catalog]
    assert len(ids) == len(set(ids)), f"Duplicate lesson_ids: {ids}"


def test_stages_are_1_through_5(catalog):
    stages = {int(r["stage"]) for r in catalog}
    assert stages.issubset({1, 2, 3, 4, 5}), f"Invalid stages: {stages}"


def test_lesson_numbers_are_positive_integers(catalog):
    for r in catalog:
        ln = int(r["lesson_num"])
        assert ln > 0, f"Bad lesson_num {ln} in {r['lesson_id']}"


def test_phonogram_intro_lessons_have_new_phonogram(catalog):
    """Lessons typed 'phonogram-intro' must declare a new phonogram."""
    bad = []
    for r in catalog:
        if r["type"] == "phonogram-intro" and not r["new_phonogram"].strip():
            bad.append(r["lesson_id"])
    assert not bad, f"phonogram-intro lessons without new_phonogram: {bad}"


def test_rule_intro_lessons_have_new_rule(catalog):
    """Lessons typed 'rule-intro' must declare a new rule."""
    bad = []
    for r in catalog:
        if r["type"] == "rule-intro" and not r["new_rule"].strip():
            bad.append(r["lesson_id"])
    assert not bad, f"rule-intro lessons without new_rule: {bad}"


def test_all_lessons_have_corresponding_md(catalog):
    """Every catalog lesson should have a corresponding MD file."""
    missing = []
    for r in catalog:
        md_path = PROJECT_ROOT / "lessons" / f"stage-{r['stage']}" / f"{r['lesson_id']}.md"
        if not md_path.exists():
            missing.append(str(md_path.relative_to(PROJECT_ROOT)))
    assert not missing, f"Missing MD files:\n  " + "\n  ".join(missing[:10])


def test_phonogram_ids_match_worksheet_filenames(catalog):
    """Phonograms declared in catalog should match pg-{id}.md worksheets."""
    pgs = {r["new_phonogram"].strip() for r in catalog if r["new_phonogram"].strip()}
    missing = []
    for pg in pgs:
        if not (PROJECT_ROOT / "worksheets" / "phonograms" / f"pg-{pg}.md").exists():
            missing.append(pg)
    assert not missing, f"Phonograms without worksheets: {missing}"


def test_total_lessons_meets_expected_count(catalog):
    """Sanity check — curriculum claims 248 lessons across 5 stages."""
    total = len(catalog)
    assert total >= 240, f"Catalog has only {total} lessons (expected ~248)"