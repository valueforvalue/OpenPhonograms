#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Render all reference/*.html files to PDF using WeasyPrint.

Output:
  build/handbook/<stem>.pdf  (alongside stage handbooks)

Why: the release ZIP includes a 04-Quick-Reference/ folder; teachers
without internet access can print the PDFs instead of opening HTMLs in
a browser.

Usage:
    python scripts/render-references.py
    python scripts/render-references.py --html diacritical-legend.html
    python scripts/render-references.py --jobs 4
"""
import argparse
import io
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REF_DIR = ROOT / "reference"
ASSETS = ROOT / "assets"
BUILD = ROOT / "build" / "handbook"

sys.path.insert(0, str(ROOT))
from framework.build_log import (
    get_logger, phase, Progress, WorkerLogQueue,
    set_worker_queue, drain_worker_queue, attach_worker_handler,
)

log = get_logger("render-references")

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
        from weasyprint import HTML
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
        log.error(f"FAIL {html_path.name}: {e}")
        return False


def _ref_worker(html_path_str: str, out_path_str: str) -> str:
    """Worker entry point for ProcessPoolExecutor."""
    worker_log = get_logger("render-references.worker")
    attach_worker_handler(worker_log)
    try:
        render_html(Path(html_path_str), Path(out_path_str))
        return out_path_str
    except Exception as exc:
        worker_log.error(f"FAIL {html_path_str}: {exc}", exc_info=True)
        raise


def main():
    parser = argparse.ArgumentParser(description="Render reference HTMLs to PDF")
    parser.add_argument("--html", help="Render only this file (e.g. glossary.html)")
    parser.add_argument("--jobs", "-j", type=int, default=4, help="Parallel worker processes (default: 4)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip PDFs whose mtime is newer than source HTML.")
    args = parser.parse_args()

    try:
        from weasyprint import HTML  # noqa: F401  -- eager check
    except ImportError:
        log.error("weasyprint not installed. Install with: pip install weasyprint")
        sys.exit(2)

    phase("Render Reference HTMLs")
    BUILD.mkdir(parents=True, exist_ok=True)
    targets = [REF_DIR / args.html] if args.html else sorted(REF_DIR.glob("*.html"))

    if not targets:
        log.info(f"No HTML files found in {REF_DIR}")
        return

    # Filter + materialize jobs up-front
    jobs: list[tuple[Path, Path]] = []
    skipped = 0
    for html in targets:
        if not html.exists():
            log.warning(f"MISSING: {html.name}")
            continue
        pdf = BUILD / (html.stem + ".pdf")
        if args.skip_existing and pdf.exists() and pdf.stat().st_mtime >= html.stat().st_mtime:
            skipped += 1
            continue
        jobs.append((html, pdf))

    if args.skip_existing and skipped:
        log.info(f"skip-existing: {skipped} PDFs up-to-date, {len(jobs)} to render")
    if not jobs:
        log.info("nothing to render" + (" (all up-to-date)" if args.skip_existing else ""))
        return

    ok = 0
    fail = 0
    if args.jobs > 1:
        queue = WorkerLogQueue()
        set_worker_queue(queue)
        workers = max(1, args.jobs)
        log.info(f"render-references: {len(jobs)} files, {workers} workers")
        with Progress("render-references", total=len(jobs)) as progress:
            executor = ProcessPoolExecutor(max_workers=workers)
            try:
                futures = [
                    executor.submit(_ref_worker, str(html), str(pdf))
                    for html, pdf in jobs
                ]
                for fut in as_completed(futures):
                    drain_worker_queue(queue, log)
                    try:
                        fut.result()
                        ok += 1
                    except Exception as exc:
                        log.error(f"FAIL: {exc}")
                        fail += 1
                    progress.tick()
                    drain_worker_queue(queue, log)
            finally:
                executor.shutdown(wait=True)
                set_worker_queue(None)
    else:
        for html, pdf in jobs:
            if render_html(html, pdf):
                ok += 1
            else:
                fail += 1

    log.info(f"rendered {ok}/{len(jobs)} reference PDFs (fail={fail})")


if __name__ == "__main__":
    main()