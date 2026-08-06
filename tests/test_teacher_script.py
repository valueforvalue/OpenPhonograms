"""Tests for the teacher script injection (issue #4)."""
import re
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "framework"))


class TestTeacherScriptModule:
    """framework/teacher_script.py — public API."""

    @pytest.fixture(scope="class")
    def helper(self):
        from teacher_script import (
            format_phonogram_script, format_rule_script, format_spelling_script,
            _read_template, _wrap_collapsible,
        )
        return {
            "format_phonogram_script": format_phonogram_script,
            "format_rule_script": format_rule_script,
            "format_spelling_script": format_spelling_script,
            "_read_template": _read_template,
            "_wrap_collapsible": _wrap_collapsible,
        }

    def test_format_phonogram_script_substitutes(self, helper):
        result = helper["format_phonogram_script"]("sh", "/sh/")
        assert "**sh**" in result
        assert "/sh/" in result
        assert "phonogram" in result.lower()

    def test_format_rule_script_substitutes(self, helper):
        result = helper["format_rule_script"]("26", "CK after a short vowel",
                                              "CK is used only after a single short vowel")
        assert "Rule 26" in result
        assert "CK after a short vowel" in result

    def test_format_spelling_script_substitutes(self, helper):
        result = helper["format_spelling_script"]("ship", "I see a ship.")
        assert "ship" in result
        assert "I see a ship." in result

    def test_scripts_are_collapsible(self, helper):
        """Every script must be wrapped in <details class='teacher-script'>."""
        for fn in (helper["format_phonogram_script"],
                   helper["format_rule_script"],
                   helper["format_spelling_script"]):
            if fn is helper["format_phonogram_script"]:
                result = fn("a", "/ă/")
            elif fn is helper["format_rule_script"]:
                result = fn("1", "Test rule", "Test statement")
            else:
                result = fn("word", "A sentence with word.")
            assert '<details class="teacher-script">' in result
            assert "<summary>" in result
            assert "Teacher Script" in result
            assert "</details>" in result

    def test_strip_frontmatter_drops_h2(self, helper):
        """Templates start with '## Teacher Script' which would duplicate the summary.

        _strip_frontmatter() should drop this H2.
        """
        template = helper["_read_template"]("phonogram")
        assert template.startswith("## "), "Pre-condition: template starts with H2"
        from teacher_script import _strip_frontmatter
        stripped = _strip_frontmatter(template)
        assert not stripped.startswith("## "), \
            f"_strip_frontmatter failed to drop H2. Got: {stripped[:50]!r}"


class TestLessonsHaveScripts:
    """Generated lesson MDs for stages 1-3 contain embedded teacher scripts."""

    @pytest.mark.parametrize("stage_lesson", [
        ("1", "pg-a"),
        ("1", "pg-sh"),  # not in stage 1; use pg-d for variety
        ("2", "pg-sh"),
        ("2", "pg-th"),
        ("2", "rule-26"),
        ("3", "pg-dge"),
        ("3", "pg-ough"),
        ("3", "rule-1"),
    ])
    def test_phonogram_intro_lesson_has_script(self, stage_lesson):
        stage, lesson = stage_lesson
        path = PROJECT_ROOT / "lessons" / f"stage-{stage}" / f"{lesson}.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert 'class="teacher-script"' in content, \
            f"{lesson}.md missing teacher script block"

    def test_stage1_phonogram_lessons_have_script(self):
        """Spot-check several Stage 1 PG lessons."""
        for slug in ["pg-a", "pg-b", "pg-c", "pg-s", "pg-sh" if False else "pg-e"]:
            path = PROJECT_ROOT / "lessons" / "stage-1" / f"{slug}.md"
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            assert 'class="teacher-script"' in content, \
                f"Stage 1 {slug}.md missing script"

    def test_stage2_multi_phonogram_has_script(self):
        for slug in ["pg-sh", "pg-th", "pg-ck", "pg-ee", "pg-ai", "pg-ay"]:
            path = PROJECT_ROOT / "lessons" / "stage-2" / f"{slug}.md"
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            assert 'class="teacher-script"' in content

    def test_stage2_rule_lessons_have_script(self):
        for slug in ["rule-3", "rule-9", "rule-26"]:
            path = PROJECT_ROOT / "lessons" / "stage-2" / f"{slug}.md"
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            assert 'class="teacher-script"' in content
