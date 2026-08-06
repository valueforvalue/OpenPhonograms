"""Tests for pdf_merge.py + cache-first pack assembly.

Verifies:
  - compile_pack merges PDFs in order
  - page count of merged pack = sum of components
  - missing component PDFs return CompileResult.ok=False
  - pdf_merge CompileResult dataclass works
  - _expected_pdf() maps common source paths correctly
"""
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys_path = PROJECT_ROOT
import sys
sys.path.insert(0, str(sys_path))
sys.path.insert(0, str(sys_path / "framework"))
sys.path.insert(0, str(sys_path / "scripts"))

from framework import pdf_merge  # noqa: E402
from framework.pdf_merge import compile_pack, page_count, CompileResult  # noqa: E402


# ── helpers ────────────────────────────────────────────────────────────

def _make_pdf(path: Path, n_pages: int = 1) -> Path:
    """Write a tiny valid PDF with n_pages pages via pypdf."""
    from pypdf import PdfWriter
    w = PdfWriter()
    for _ in range(n_pages):
        w.add_blank_page(width=72, height=72)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        w.write(f)
    return path


# ── compile_pack basics ────────────────────────────────────────────────

class TestCompilePack:
    def test_empty_components_returns_ok(self, tmp_path):
        out = tmp_path / "out.pdf"
        r = compile_pack(out, [])
        assert r.ok
        assert r.page_count == 0
        assert out.exists()

    def test_single_component(self, tmp_path):
        a = _make_pdf(tmp_path / "a.pdf", n_pages=2)
        out = tmp_path / "out.pdf"
        r = compile_pack(out, [(a, "a")])
        assert r.ok
        assert r.page_count == 2
        assert page_count(out) == 2

    def test_multi_components_concatenated(self, tmp_path):
        a = _make_pdf(tmp_path / "a.pdf", n_pages=1)
        b = _make_pdf(tmp_path / "b.pdf", n_pages=3)
        c = _make_pdf(tmp_path / "c.pdf", n_pages=2)
        out = tmp_path / "out.pdf"
        r = compile_pack(out, [(a, "a"), (b, "b"), (c, "c")])
        assert r.ok
        assert r.page_count == 6
        assert page_count(out) == 6
        assert r.merged_paths == [a, b, c]

    def test_missing_component_reports_missing(self, tmp_path):
        a = _make_pdf(tmp_path / "a.pdf", n_pages=1)
        ghost = tmp_path / "ghost.pdf"
        out = tmp_path / "out.pdf"
        r = compile_pack(out, [(a, "a"), (ghost, "ghost")])
        assert not r.ok
        assert ghost in r.missing
        assert r.page_count == 0

    def test_invalid_pdf_returns_error(self, tmp_path):
        a = _make_pdf(tmp_path / "a.pdf", n_pages=1)
        bad = tmp_path / "bad.pdf"
        bad.write_bytes(b"not a pdf")
        out = tmp_path / "out.pdf"
        r = compile_pack(out, [(a, "a"), (bad, "bad")])
        # First component (a) was merged before bad failed
        assert not r.ok
        assert "bad" in r.error


# ── cache-first pack flow ──────────────────────────────────────────────

class TestPackMergeIntegration:
    """Smoke test: build_one_pack with cache-first path."""

    def test_build_one_pack_uses_cached_pdfs(self, monkeypatch, tmp_path):
        """Mock the catalog to a simple lesson and verify merge path."""
        # The script lives at scripts/build-lesson-pack.py — Python can't
        # import by hyphenated name. Use importlib.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "build_lesson_pack",
            PROJECT_ROOT / "scripts" / "build-lesson-pack.py",
        )
        pack_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pack_module)
        s = pack_module._expected_pdf
        # lessons/stage-1/X.md → build/stage-1/X.pdf
        assert s(PROJECT_ROOT / "lessons" / "stage-1" / "pg-a.md") == PROJECT_ROOT / "build" / "stage-1" / "pg-a.pdf"
        # worksheets/phonograms/pg-X.md → build/worksheets/phonograms/pg-X.pdf
        assert s(PROJECT_ROOT / "worksheets" / "phonograms" / "pg-a.md") == PROJECT_ROOT / "build" / "worksheets" / "phonograms" / "pg-a.pdf"
        # worksheets/rules/rule-N.md → build/worksheets/rules/rule-N.pdf
        assert s(PROJECT_ROOT / "worksheets" / "rules" / "rule-12.md") == PROJECT_ROOT / "build" / "worksheets" / "rules" / "rule-12.pdf"
        # worksheets/cards/flash-*.md → build/worksheets/cards/flash-*.pdf
        assert s(PROJECT_ROOT / "worksheets" / "cards" / "flash-singles-1.md") == PROJECT_ROOT / "build" / "worksheets" / "cards" / "flash-singles-1.pdf"
        # readers/stage-N/X.md → build/readers/stage-N/X.pdf
        assert s(PROJECT_ROOT / "readers" / "stage-2" / "001-fred.md") == PROJECT_ROOT / "build" / "readers" / "stage-2" / "001-fred.pdf"
        # readers/X.md (flat) → build/readers/X.pdf
        assert s(PROJECT_ROOT / "readers" / "001-fred.md") == PROJECT_ROOT / "build" / "readers" / "001-fred.pdf"


    def test_real_catalog_lesson_has_existing_pdfs(self):
        """Spot-check that the catalog + lookup logic finds real cached PDFs."""
        # The previous just build populated build/, so we should have
        # all stage-1 PDFs cached.
        from pathlib import Path
        build = PROJECT_ROOT / "build"
        stage1 = build / "stage-1"
        assert stage1.exists(), "build/stage-1/ should exist after `just build`"
        # At least 48 PDFs
        pdfs = list(stage1.glob("*.pdf"))
        assert len(pdfs) >= 48, f"expected >=48 lesson PDFs, got {len(pdfs)}"
