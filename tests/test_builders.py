"""Tests for build scripts that combine PDFs into stage-level + release outputs.

These tests are marked 'slow' and excluded by default. Run them with:
    pytest tests/test_builders.py -v
or:
    just test-slow

Reason: builders depend on previously-rendered PDFs (build/ directory must
be populated by `just render-all` first) and are slow to run.
"""
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Mark all tests in this module as 'slow' — deselect with '-m "not slow"'
pytestmark = pytest.mark.slow


class TestBuildStagePdf:
    """build-stage-pdf.py merges per-stage PDFs."""

    def test_stage_2_combined_pdf_exists(self):
        path = PROJECT_ROOT / "build" / "stage-2.pdf"
        if not path.exists():
            pytest.skip("Stage 2 combined PDF not yet built")
        assert path.exists()
        assert path.stat().st_size > 1000

    def test_empty_stages_skip_empty_outputs(self):
        """Stage 1 has no readers; -readers.pdf must not exist."""
        path = PROJECT_ROOT / "build" / "stage-1-readers.pdf"
        assert not path.exists(), "stage-1-readers.pdf should be skipped"

    def test_merged_pdfs_have_real_pages(self):
        try:
            import pypdf
        except ImportError:
            pytest.skip("pypdf not installed")
        for stage in range(1, 6):
            for suffix in ("", "-worksheets", "-readers"):
                path = PROJECT_ROOT / "build" / f"stage-{stage}{suffix}.pdf"
                if not path.exists():
                    continue
                r = pypdf.PdfReader(str(path))
                assert len(r.pages) > 0, f"{path} has 0 pages"


class TestBuildReleaseZip:
    """build-release.py assembles release.zip."""

    def test_release_zip_assembles(self):
        zip_path = PROJECT_ROOT / "release.zip"
        if not zip_path.exists():
            pytest.skip("release.zip not yet built (run `just release`)")

    def test_release_zip_contains_stage_pdfs(self):
        """The release ZIP should include the per-stage merged PDFs (issue #25)."""
        zip_path = PROJECT_ROOT / "release.zip"
        if not zip_path.exists():
            pytest.skip("release.zip not yet built")
        import zipfile
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        for stage in range(1, 6):
            # At least the worksheets PDF (which exists for stages 1-4)
            ws_pdf = PROJECT_ROOT / "build" / f"stage-{stage}-worksheets.pdf"
            if ws_pdf.exists():
                assert any(f"stage-{stage}-worksheets.pdf" in n for n in names), \
                    f"release.zip missing stage-{stage}-worksheets.pdf"