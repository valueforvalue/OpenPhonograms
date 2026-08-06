"""Tests for the standard footer injection + PDF credit check (issues #32, #36).

Post-rebrand (commit 1379999) the footer reads:
  *Open-source. MIT licensed. Phonograms are drawn from the public-domain
   phonics tradition (1800s onward).*

These tests assert that footer is present in lesson/worksheet/reader MD
files and that the PDF credit checker recognizes it.
"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "framework"))


# Phrases that confirm the standardized footer is present.
FOOTER_MARKERS = (
    "Open-source",
    "MIT licensed",
    "public-domain phonics tradition",
)


class TestInjectFooter:
    """framework/inject_footer.py — adds footer to MD files."""

    @pytest.fixture(scope="class")
    def helper(self):
        from inject_footer import needs_footer, strip_existing_footer, add_footer, FOOTER
        return {
            "needs_footer": needs_footer,
            "strip_existing_footer": strip_existing_footer,
            "add_footer": add_footer,
            "FOOTER": FOOTER,
        }

    def test_footer_contains_open_source_marker(self, helper):
        assert "Open-source" in helper["FOOTER"]
        assert "MIT licensed" in helper["FOOTER"]

    def test_footer_contains_mit_license(self, helper):
        assert "MIT" in helper["FOOTER"]
        assert "licensed" in helper["FOOTER"]

    def test_footer_no_longer_references_old_brand(self, helper):
        # Rebrand guard: the new footer must not mention the old brand.
        assert "Denise Eide" not in helper["FOOTER"]
        assert "Uncovering the Logic of English" not in helper["FOOTER"]

    def test_needs_footer_for_new_file(self, helper):
        assert helper["needs_footer"]("Some content here.\n") is True

    def test_does_not_need_if_already_at_end(self, helper):
        content = "Some content.\n\n" + helper["FOOTER"].lstrip()
        assert helper["needs_footer"](content) is False

    def test_needs_update_if_footer_not_at_end(self, helper):
        content = "Some content.\n\n" + helper["FOOTER"].lstrip() + "\nNew text\n"
        assert helper["needs_footer"](content) is True

    def test_strip_removes_existing_footer(self, helper):
        content = "Header\n" + helper["FOOTER"].lstrip() + "\n"
        stripped = helper["strip_existing_footer"](content)
        assert "Open-source" not in stripped
        assert "Header" in stripped

    def test_idempotent(self, helper, tmp_path):
        """Adding footer twice should produce same result as adding once."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nBody\n", encoding="utf-8")
        helper["add_footer"](test_file)
        first = test_file.read_text(encoding="utf-8")
        helper["add_footer"](test_file)
        second = test_file.read_text(encoding="utf-8")
        assert first == second


class TestInjectFooterScript:
    """framework/inject_footer.py as a CLI script."""

    def test_script_runs(self, tmp_path):
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        (test_dir / "a.md").write_text("# A\n\nBody\n", encoding="utf-8")
        (test_dir / "b.md").write_text("# B\n\nBody\n", encoding="utf-8")
        (test_dir / "sub").mkdir()
        (test_dir / "sub" / "c.md").write_text("# C\n\nBody\n", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "framework/inject_footer.py", str(test_dir)],
            capture_output=True, text=True, cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        for f in (test_dir / "a.md", test_dir / "b.md", test_dir / "sub" / "c.md"):
            content = f.read_text(encoding="utf-8")
            assert "Open-source" in content, f"{f} missing footer"
            assert "MIT licensed" in content

    def test_dry_run_does_not_modify(self, tmp_path):
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        test_file = test_dir / "a.md"
        original = "# A\n\nBody\n"
        test_file.write_text(original, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "framework/inject_footer.py", "--dry-run", str(test_dir)],
            capture_output=True, text=True, cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert test_file.read_text(encoding="utf-8") == original


class TestCheckPdfCredits:
    """framework/check_pdf_credits.py — verifies PDFs contain the footer."""

    def test_script_module_loads(self):
        from check_pdf_credits import _extract_all_pages_text, CREDIT_PHRASES
        # Post-rebrand the credit checker recognizes the new footer markers.
        assert "Open-source" in CREDIT_PHRASES
        assert "MIT licensed" in CREDIT_PHRASES
        # Guard: no longer checking for the old brand.
        assert "Denise Eide" not in CREDIT_PHRASES
        assert "Uncovering the Logic of English" not in CREDIT_PHRASES

    @pytest.mark.slow
    def test_script_runs_against_build(self):
        if not (PROJECT_ROOT / "build").exists():
            pytest.skip("build/ not present; run 'just render-all' first")
        result = subprocess.run(
            [sys.executable, "framework/check_pdf_credits.py", "--quiet"],
            capture_output=True, text=True, cwd=PROJECT_ROOT,
        )
        assert result.returncode in (0, 1), (
            f"Unexpected exit {result.returncode}\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )


class TestLessonFooterPresent:
    """Verify the footer actually appears in generated MDs."""

    @pytest.mark.parametrize("marker", FOOTER_MARKERS)
    def test_lesson_has_footer(self, marker):
        path = PROJECT_ROOT / "lessons" / "stage-1" / "pg-a.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert marker in content, f"{path} missing footer marker {marker!r}"

    @pytest.mark.parametrize("marker", FOOTER_MARKERS)
    def test_worksheet_has_footer(self, marker):
        path = PROJECT_ROOT / "worksheets" / "phonograms" / "pg-a.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert marker in content, f"{path} missing footer marker {marker!r}"

    @pytest.mark.parametrize("marker", FOOTER_MARKERS)
    def test_reader_has_footer(self, marker):
        path = PROJECT_ROOT / "readers" / "001-fred-the-frog.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert marker in content, f"{path} missing footer marker {marker!r}"
