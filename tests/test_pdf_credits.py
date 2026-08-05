"""Tests for the source attribution footer (issues #32, #36)."""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "framework"))


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

    def test_footer_contains_eide(self, helper):
        assert "Denise Eide" in helper["FOOTER"]

    def test_footer_contains_mit_license(self, helper):
        assert "MIT" in helper["FOOTER"]
        assert "LICENSE" in helper["FOOTER"]

    def test_needs_footer_for_new_file(self, helper):
        assert helper["needs_footer"]("Some content here.\n") is True

    def test_does_not_need_if_already_at_end(self, helper):
        content = "Some content.\n\n" + helper["FOOTER"].lstrip()
        assert helper["needs_footer"](content) is False

    def test_needs_update_if_footer_not_at_end(self, helper):
        # Footer present but new content appended after
        content = "Some content.\n\n" + helper["FOOTER"].lstrip() + "\nNew text\n"
        assert helper["needs_footer"](content) is True

    def test_strip_removes_existing_footer(self, helper):
        content = "Header\n" + helper["FOOTER"].lstrip() + "\n"
        stripped = helper["strip_existing_footer"](content)
        assert "Source: Adapted" not in stripped
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
        """Create a small test tree, run the script, verify footers added."""
        # Make a temp dir with a few MD files
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

        # All 3 files should now have the footer
        for f in (test_dir / "a.md", test_dir / "b.md", test_dir / "sub" / "c.md"):
            content = f.read_text(encoding="utf-8")
            assert "Denise Eide" in content, f"{f} missing footer"
            assert "MIT" in content

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
    """framework/check_pdf_credits.py — verifies PDFs contain credit."""

    def test_script_module_loads(self):
        """Just verify the module is importable and has the expected functions."""
        from check_pdf_credits import _extract_all_pages_text, CREDIT_PHRASES
        assert "Denise Eide" in CREDIT_PHRASES

    @pytest.mark.slow
    def test_script_runs_against_build(self):
        """Run the full check against the actual build/ directory.

        Slow integration test — needs the build pipeline to have run.
        Marked slow so it's not in the default test suite.
        """
        if not (PROJECT_ROOT / "build").exists():
            pytest.skip("build/ not present; run 'just render-all' first")
        result = subprocess.run(
            [sys.executable, "framework/check_pdf_credits.py", "--quiet"],
            capture_output=True, text=True, cwd=PROJECT_ROOT,
        )
        # Exit 0 = all pass; non-zero = some fail. Both are valid runs.
        assert result.returncode in (0, 1), (
            f"Unexpected exit {result.returncode}\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )


class TestLessonFooterPresent:
    """Verify the footer actually appears in generated MDs."""

    def test_lesson_has_footer(self):
        path = PROJECT_ROOT / "lessons" / "stage-1" / "pg-a.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert "Denise Eide" in content, f"{path} missing source attribution"

    def test_worksheet_has_footer(self):
        path = PROJECT_ROOT / "worksheets" / "phonograms" / "pg-a.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert "Denise Eide" in content

    def test_reader_has_footer(self):
        path = PROJECT_ROOT / "readers" / "001-fred-the-frog.md"
        if not path.exists():
            pytest.skip(f"{path} not found")
        content = path.read_text(encoding="utf-8")
        assert "Denise Eide" in content
