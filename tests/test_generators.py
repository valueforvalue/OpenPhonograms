"""Smoke tests for content generators.

Every generator script must:
  1. Be parseable Python (no syntax errors)
  2. Have a callable main() function
  3. Produce expected on-disk output (verified by `just gen-...` + `just check-...`)

Note: We intentionally do NOT call main() from pytest. Generators write to
stdout via print() and can interfere with pytest's stdio capture on Windows.
This file's tests focus on (1) syntax, (2) presence of main(), and
(3) on-disk output verification.
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


SCRIPTS_THAT_HAVE_MAIN = [
    "generate-worksheets.py",
    "generate-readers.py",
    "generate-animal-readers.py",
    "generate-stage-handbook.py",
    "build-stage-pdf.py",
    "build-release.py",
    "generate-navigation.py",
    "generate-quick-checks.py",
    "generate-placement-test.py",
    "generate-binding-instructions.py",
    "generate-certificates.py",
    "generate-readers-index.py",
    "copy-assessments.py",
    "render-extras.py",
    "render-references.py",
]


@pytest.mark.parametrize("script", SCRIPTS_THAT_HAVE_MAIN)
def test_script_is_valid_python(script):
    """Every generator/builder script must parse as valid Python."""
    path = SCRIPTS_DIR / script
    if not path.exists():
        pytest.skip(f"{script} not found")
    src = path.read_text(encoding="utf-8")
    try:
        ast.parse(src, filename=script)
    except SyntaxError as e:
        pytest.fail(f"{script} has syntax error: {e}")


@pytest.mark.parametrize("script", SCRIPTS_THAT_HAVE_MAIN)
def test_script_defines_main(script):
    """Every generator/builder script must define a main() function."""
    path = SCRIPTS_DIR / script
    if not path.exists():
        pytest.skip(f"{script} not found")
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=script)
    func_names = {node.name for node in ast.walk(tree)
                  if isinstance(node, ast.FunctionDef)}
    assert "main" in func_names, f"{script} missing def main()"


@pytest.mark.parametrize("script", SCRIPTS_THAT_HAVE_MAIN)
def test_script_has_if_name_main_guard(script):
    """Every generator/builder script must guard main() with `if __name__ == '__main__'`."""
    path = SCRIPTS_DIR / script
    if not path.exists():
        pytest.skip(f"{script} not found")
    src = path.read_text(encoding="utf-8")
    assert "__name__" in src and "__main__" in src, \
        f"{script} missing `if __name__ == '__main__'` guard"


# ── on-disk output (after `just gen-...` has run) ─────────────────────

class TestWorksheetOutput:
    """Verify expected worksheets exist after gen-worksheets has run."""

    def test_phonogram_worksheets_created(self):
        pgs = list(Path("worksheets/phonograms").glob("pg-*.md"))
        assert len(pgs) >= 72, f"Expected ≥72 phonogram worksheets, got {len(pgs)}"

    def test_rule_worksheets_created(self):
        rules = list(Path("worksheets/rules").glob("rule-*.md"))
        assert len(rules) >= 31, f"Expected ≥31 rule worksheets, got {len(rules)}"

    def test_flash_cards_created(self):
        cards = list(Path("worksheets/cards").glob("flash-*.md"))
        assert len(cards) >= 15, f"Expected ≥15 flash cards, got {len(cards)}"

    def test_stage_grouped_mirrors_exist(self):
        """Stage-N/ subdirs must exist after generator runs."""
        for s in range(1, 6):
            for sub in ["phonograms", "rules", "cards"]:
                d = Path(f"worksheets/{sub}/stage-{s}")
                if d.exists():
                    md_files = list(d.glob("*.md"))
                    assert len(md_files) > 0, f"{d} is empty"

    def test_phonogram_worksheet_schema(self):
        sample = Path("worksheets/phonograms/pg-sh.md")
        if not sample.exists():
            pytest.skip("pg-sh.md not generated")
        content = sample.read_text(encoding="utf-8")
        assert content.startswith("# Phonogram"), f"Bad header: {content[:50]}"
        assert "Sounds" in content or "sounds" in content


class TestReaderOutput:
    """Verify expected readers exist after gen-readers + gen-animal-readers."""

    def test_readers_in_flat_layout(self):
        flat = [p for p in Path("readers").glob("*.md")]
        assert len(flat) >= 24, f"Expected ≥24 readers, got {len(flat)}"

    def test_readers_in_stage_layout(self):
        for s in range(2, 6):
            d = Path(f"readers/stage-{s}")
            if d.exists():
                assert any(d.glob("*.md")), f"{d} is empty"


class TestRenderPipeline:
    """Render a known-good MD via direct Python call (not subprocess)."""

    def test_render_a_real_reader(self, tmp_path):
        src = Path("readers/001-fred-the-frog.md")
        if not src.exists():
            pytest.skip("001-fred-the-frog.md missing")
        # Add framework/ to sys.path locally for this test
        import sys as _sys
        _sys.path.insert(0, str(PROJECT_ROOT / "framework"))
        from render import render_md_to_pdf  # type: ignore
        pdf = tmp_path / "out.pdf"
        render_md_to_pdf(src, pdf, doc_type="reader")
        assert pdf.exists()
        assert pdf.stat().st_size > 5000