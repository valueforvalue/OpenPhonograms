#!/usr/bin/env python3
"""Render all reference/*.html files to PDF using WeasyPrint.

Output:
  build/handbook/<stem>.pdf  (alongside stage handbooks)

Why: the release ZIP includes a 04-Quick-Reference/ folder; teachers
without internet access can print the PDFs instead of opening HTMLs in
a browser.

Usage:
    python scripts/render-references.py
    python scripts/render-references.py --html diacritical-legend.html
"""
import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REF_DIR = ROOT / "reference"
ASSETS = ROOT / "assets"
BUILD = ROOT / "build" / "handbook"

try:
    from weasyprint import HTML
except ImportError:
    print("Error: weasyprint not installed. Install with: pip install weasyprint")
    sys.exit(2)

# Atkinson Hyperlegible @font-face — mirrors framework/render.py PAGE_CSS
# so reference PDFs match lesson PDFs in typography.
_FONT_FACE_CSS = """
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("../framework/fonts/AtkinsonHyperlegible-Regular.ttf") format("truetype");
    font-weight: 400; font-style: normal;
}
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("../framework/fonts/AtkinsonHyperlegible-Italic.ttf") format("truetype");
    font-weight: 400; font-style: italic;
}
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("../framework/fonts/AtkinsonHyperlegible-Bold.ttf") format("truetype");
    font-weight: 700; font-style: normal;
}
@font-face {
    font-family: "Atkinson Hyperlegible";
    src: url("../framework/fonts/AtkinsonHyperlegible-BoldItalic.ttf") format("truetype");
    font-weight: 700; font-style: italic;
}
"""


def render_html(html_path: Path, out_path: Path) -> bool:
    """Render a single HTML reference to PDF. Returns True on success."""
    try:
        html_text = html_path.read_text(encoding="utf-8")
        # Inject font @font-face right after <style> or before </head>
        # so WeasyPrint embeds Atkinson Hyperlegible.
        if "</style>" in html_text and "@font-face" not in html_text:
            html_text = html_text.replace(
                "</style>", f"{_FONT_FACE_CSS}</style>", 1)
        elif "</head>" in html_text:
            html_text = html_text.replace(
                "</head>",
                f"<style>{_FONT_FACE_CSS}</style></head>", 1)
        # base_url = REF_DIR so relative asset links (../assets/main.css, ../framework/fonts/) resolve
        HTML(string=html_text,
             base_url=str(REF_DIR) + "/").write_pdf(str(out_path))
        return True
    except Exception as e:
        print(f"  FAIL {html_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Render reference HTMLs to PDF")
    parser.add_argument("--html", help="Render only this file (e.g. glossary.html)")
    args = parser.parse_args()

    BUILD.mkdir(parents=True, exist_ok=True)
    targets = [REF_DIR / args.html] if args.html else sorted(REF_DIR.glob("*.html"))

    if not targets:
        print(f"No HTML files found in {REF_DIR}")
        return

    ok = 0
    for html in targets:
        if not html.exists():
            print(f"  MISSING: {html.name}")
            continue
        out = BUILD / (html.stem + ".pdf")
        if render_html(html, out):
            ok += 1
            print(f"  OK  {out.relative_to(ROOT)}")

    print(f"\nRendered {ok}/{len(targets)} reference PDFs")


if __name__ == "__main__":
    main()