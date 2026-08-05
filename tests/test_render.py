"""Tests for framework/render.py — markdown→PDF conversion pipeline."""
from pathlib import Path

import pytest


# ── resolve_image_path ─────────────────────────────────────────────────

class TestResolveImagePath:
    """Test image src → absolute Path resolution."""

    def test_absolute_path_returned_unchanged(self, project_root, render_module):
        abs_path = project_root / "images" / "animals" / "frog.png"
        result = render_module.resolve_image_path(str(abs_path), project_root / "lessons" / "stage-1" / "x.md")
        assert result == abs_path

    def test_relative_to_md_file(self, tmp_path, project_root, render_module):
        # Create a fake image next to the MD
        md = tmp_path / "lesson.md"
        img = tmp_path / "images" / "pic.png"
        img.parent.mkdir()
        img.write_bytes(b"x")
        result = render_module.resolve_image_path("images/pic.png", md)
        assert result == img

    def test_fallback_to_project_root(self, project_root, render_module):
        # The image does NOT exist next to the MD but DOES exist at project root
        md = project_root / "lessons" / "stage-1" / "x.md"
        result = render_module.resolve_image_path("images/animals/frog.png", md)
        # Should resolve to project_root/images/animals/frog.png
        assert result == project_root / "images" / "animals" / "frog.png"

    def test_nonexistent_returns_best_guess(self, project_root, render_module):
        # Even when file doesn't exist, returns the fallback path
        md = project_root / "lessons" / "stage-1" / "x.md"
        result = render_module.resolve_image_path("images/missing.png", md)
        assert result == project_root / "images" / "missing.png"


# ── _stage_from_path ───────────────────────────────────────────────────

class TestStageFromPath:
    """Test stage detection from path segments."""

    @pytest.mark.parametrize("path,expected", [
        ("lessons/stage-1/pg-a.md", 1),
        ("lessons/stage-2/pg-sh.md", 2),
        ("lessons/stage-5/reader-7.md", 5),
        ("worksheets/phonograms/stage-3/pg-tch.md", 3),
        ("readers/stage-4/009-the-invention.md", 4),
        ("lessons/stage-9/should-not-match.md", None),  # out of range
        ("lessons/foo/bar.md", None),                    # no stage-N segment
    ])
    def test_stage_detection(self, render_module, path, expected):
        result = render_module._stage_from_path(Path(path))
        assert result == expected


# ── md_to_html ─────────────────────────────────────────────────────────

class TestMdToHtml:
    """Test markdown → HTML conversion with image handling."""

    def test_basic_markdown(self, project_root, render_module):
        md_file = project_root / "lessons" / "stage-1" / "test.md"
        result = render_module.md_to_html("# Hello\n\nThis is **bold**.", md_file)
        assert "Hello" in result
        assert "<strong>bold</strong>" in result or "<b>bold</b>" in result

    def test_image_gets_empty_alt(self, project_root, render_module):
        """Images are rendered with alt='' to prevent pdftotext bleed-through."""
        md_file = project_root / "lessons" / "stage-1" / "test.md"
        result = render_module.md_to_html("![A frog](images/animals/frog.png)", md_file)
        assert '<img' in result
        assert 'alt=""' in result

    def test_image_src_rewritten_to_project_root(self, project_root, render_module):
        """Image src is rewritten to be relative to PROJECT_ROOT."""
        md_file = project_root / "lessons" / "stage-1" / "test.md"
        result = render_module.md_to_html("![frog](images/animals/frog.png)", md_file)
        assert 'src="images/animals/frog.png"' in result

    def test_external_image_src_unchanged(self, project_root, render_module):
        md_file = project_root / "lessons" / "stage-1" / "test.md"
        result = render_module.md_to_html("![web](https://example.com/x.png)", md_file)
        assert 'https://example.com/x.png' in result

    def test_missing_image_renders_placeholder(self, project_root, render_module):
        md_file = project_root / "lessons" / "stage-1" / "test.md"
        result = render_module.md_to_html("![A cute frog](images/does-not-exist.png)", md_file)
        assert "img-placeholder" in result
        assert "does-not-exist.png" in result
        assert "A cute frog" in result  # alt text preserved in placeholder

    def test_markdown_inside_div_block(self, project_root, render_module):
        """Markdown inside <div> tags should render (not be passed through raw)."""
        md_file = project_root / "lessons" / "stage-1" / "test.md"
        md = """<div class="callout">

### A heading inside

Some **bold** text.

</div>"""
        result = render_module.md_to_html(md, md_file)
        # Without the div-splitting fix, "### A heading inside" would appear as raw text
        assert "<h3>" in result or "<strong>" in result


# ── render_md_to_pdf ───────────────────────────────────────────────────

class TestRenderMdToPdf:
    """Test end-to-end markdown → PDF rendering."""

    def test_renders_simple_markdown_to_pdf(self, project_root, render_module, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("# Test\n\nHello **world**.", encoding="utf-8")
        pdf = tmp_path / "test.pdf"
        render_module.render_md_to_pdf(md, pdf)
        assert pdf.exists()
        assert pdf.stat().st_size > 100  # not empty

    def test_body_class_includes_stage_and_type(self, project_root, render_module, tmp_path):
        """Render output HTML should include both stage-N + worksheet/reader classes."""
        # Indirect: use a stage-2 reader path
        md = tmp_path / "stage-2" / "lesson.md"
        md.parent.mkdir()
        md.write_text("# Test", encoding="utf-8")
        # We can't easily inspect full_html without mocking; instead check that
        # the function runs without error with combined classes.
        pdf = tmp_path / "out.pdf"
        render_module.render_md_to_pdf(md, pdf, doc_type="reader")
        assert pdf.exists()

    def test_pdf_contains_atkinson_font(self, project_root, render_module, tmp_path):
        """Rendered PDF embeds Atkinson Hyperlegible via @font-face."""
        try:
            import pypdf
        except ImportError:
            pytest.skip("pypdf not installed")
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        pdf = tmp_path / "test.pdf"
        render_module.render_md_to_pdf(md, pdf)
        reader = pypdf.PdfReader(str(pdf))
        fonts = set()
        for page in reader.pages:
            for f in page["/Resources"].get("/Font", {}).values():
                fonts.add(f.get_object()["/BaseFont"])
        assert any("Atkinson-Hyperlegible" in f for f in fonts), \
            f"PDF missing Atkinson Hyperlegible font. Found: {fonts}"


# ── PAGE_CSS structural checks ─────────────────────────────────────────

class TestPageCss:
    """Smoke checks on the CSS string itself."""

    def test_page_css_is_non_empty(self, render_module):
        assert len(render_module.PAGE_CSS) > 1000

    def test_page_css_includes_atkinson(self, render_module):
        assert "Atkinson" in render_module.PAGE_CSS

    def test_page_css_includes_wcag_colors(self, render_module):
        # WCAG AA palette (issue #27)
        assert "#a8421a" in render_module.PAGE_CSS  # vowel rust
        assert "#2a7d2a" in render_module.PAGE_CSS  # consonant green
        assert "#2a5c8a" in render_module.PAGE_CSS  # accent

    def test_page_css_includes_per_stage_sizing(self, render_module):
        for s in range(1, 6):
            assert f"body.stage-{s}" in render_module.PAGE_CSS

    def test_page_css_includes_phonogram_color_classes(self, render_module):
        assert ".phonogram.vowel" in render_module.PAGE_CSS
        assert ".phonogram.consonant" in render_module.PAGE_CSS