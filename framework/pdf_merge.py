# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
pdf_merge.py — Combine multiple PDFs into a single pack via pypdf.

Also provides render_and_split() — render a batch of markdown files
as ONE PDF, then split by top-level bookmarks into per-unit PDFs.

Why this exists:
  build-lesson-pack.py previously re-rendered every component (cover,
  lesson, worksheet, cards, reader) into ONE combined MD and rendered
  that once. That made the pack independent — but it ignored the
  already-rendered PDFs in build/ and re-did all the work.

  This module lets us merge the pre-rendered PDFs instead. The cover
  page is still freshly rendered (it's pack-specific). All other
  components are reused from build/.

Public API:
  compile_pack(out_path, components) -> CompileResult
    components: list of (path, label) tuples in order
    returns CompileResult(ok, page_count, missing, merged_paths)

  render_and_split(md_paths, title_to_path, ...):
    Render a batch of markdown files into one PDF, then split by
    top-level PDF bookmark into per-unit PDFs. Much faster than
    rendering each file individually (avoids per-file Pango/font
    scan cost on Windows). See function docstring for details.
"""

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional


@dataclass
class CompileResult:
    ok: bool
    page_count: int = 0
    missing: list[Path] = field(default_factory=list)
    merged_paths: list[Path] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class SplitResult:
    ok: bool
    units: list[tuple[str, Path]] = field(default_factory=list)
    render_seconds: float = 0.0
    split_seconds: float = 0.0
    error: Optional[str] = None


def compile_pack(out_path: Path, components: list[tuple[Path, str]]) -> CompileResult:
    """Merge a list of PDFs into one output file.

    Args:
        out_path: where to write the merged PDF.
        components: ordered list of (pdf_path, label) tuples. Only the
            pdf_path is used; label is reserved for human-readable
            reporting via logging.

    Returns:
        CompileResult with page count, missing files, and paths merged.
        ok=False if any component is missing OR the merge raises.
    """
    from pypdf import PdfWriter, PdfReader

    missing = [p for p, _ in components if not p.exists()]
    if missing:
        return CompileResult(
            ok=False,
            missing=missing,
            error=f"{len(missing)} component(s) missing",
        )

    writer = PdfWriter()
    page_count = 0
    merged: list[Path] = []

    for pdf_path, label in components:
        try:
            reader = PdfReader(str(pdf_path))
            for page in reader.pages:
                writer.add_page(page)
                page_count += 1
            merged.append(pdf_path)
        except Exception as exc:
            return CompileResult(
                ok=False,
                page_count=page_count,
                missing=missing,
                merged_paths=merged,
                error=f"failed to merge {pdf_path.name} ({label}): {exc}",
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(out_path, "wb") as f:
            writer.write(f)
    except Exception as exc:
        return CompileResult(
            ok=False,
            page_count=page_count,
            missing=missing,
            merged_paths=merged,
            error=f"failed to write {out_path}: {exc}",
        )

    return CompileResult(
        ok=True,
        page_count=page_count,
        missing=[],
        merged_paths=merged,
    )


def page_count(pdf_path: Path) -> int:
    """Read-only page count for parity tests."""
    from pypdf import PdfReader
    if not pdf_path.exists():
        return 0
    return len(PdfReader(str(pdf_path)).pages)


# Lazy logger (don't create at import time — keep this module cheap).
log_split = logging.getLogger("pdf_merge.split")


def render_and_split(
    md_paths: list[Path],
    title_to_path: Callable[[str], Optional[Path]],
    *,
    combined_pdf: Path,
    body_class: str | None = None,
    toc_html: str | None = None,
) -> SplitResult:
    """Render a batch of MDs as ONE PDF, split by H1 bookmark into per-unit PDFs.

    Why batch: WeasyPrint + Pango's font scan costs ~10s per render on
    Windows (Pango scans all 859 installed system fonts). Rendering 48
    lessons individually = ~8 min. Rendering them as ONE document = ~30s.
    We pay one Pango scan instead of N.

    Mechanism:
    - Each MD file's H1s become WeasyPrint's bookmarks (top-level = H1,
      nested = H2/H3).
    - We render all MDs as one combined HTML doc.
    - pypdf walks the outline. Each top-level bookmark is a candidate
      unit. The caller decides which H1s map to output files via
      `title_to_path` (return None to skip).
    - We split pages between consecutive bookmarks into per-unit PDFs.
    - H2/H3 nested under H1 stay with the unit (not split separately).

    Args:
        md_paths: ordered list of MD files to render. Order preserved
            in the combined PDF and in resulting per-unit PDFs.
        title_to_path: fn(title_str) -> Path | None.
            If None for a title, that unit is skipped in the split.
            Caller uses this to map H1 title to output filename and
            to filter which H1s are unit boundaries (return None for
            the ones that should be ignored, e.g. at-a-glance H1s).
        combined_pdf: temp path for the combined PDF.
        body_class: CSS body class for the combined doc (e.g. "stage-1").
        toc_html: optional HTML for a clickable TOC page inserted before
            the first lesson. Usable as a standalone PDF.

    Returns:
        SplitResult with units written, timing, and any errors.
    """
    from framework.render import render_html_to_pdf, md_to_html
    from pypdf import PdfReader, PdfWriter
    import re

    if not md_paths:
        return SplitResult(ok=True)

    combined_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Build combined HTML — each MD becomes a <section>, each starts
    # with an H1 that WeasyPrint picks up as a top-level bookmark.
    sections: list[str] = []
    if toc_html:
        sections.append(f'<section class="toc">{toc_html}</section>')
    for md_path in md_paths:
        md_text = md_path.read_text(encoding="utf-8")
        body_html = md_to_html(md_text, md_path)
        # Anchor ID for TOC linking: section-lesson-NN-slug
        anchor = f"section-{md_path.stem}"
        sections.append(f'<section id="{anchor}">{body_html}</section>')

    class_attr = f' class="{body_class}"' if body_class else ""
    # In the batch-render case, we want each unit (section) to start on
    # a fresh page so the bookmark-based split lines up cleanly. Only
    # the FIRST h1 of each section needs the forced break; subsequent
    # h1s inside a section (at-a-glance, lesson, worksheet, cards,
    # reader, home practice) already separate via explicit
    # `<div class="page-break">` markers in build-lesson-pack.py.
    # Forcing breaks on every h1 doubles the breaks and produces blank
    # pages between every sub-section (issue #35). Restrict to the
    # first h1 of each section so unit boundaries stay clean without
    # multiplying blanks within a pack.
    batch_css = (
        "<style>"
        "h1 { bookmark-level: none; }"
        "section > h1:first-of-type { page-break-before: always; bookmark-level: 1; }"
        "h2, h3, h4, h5, h6 { bookmark-level: none; }"
        ".toc h1 { font-size: 22pt; color: #2a5c8a; border-bottom: 3px solid #2a5c8a; "
        "padding-bottom: 0.3em; margin-bottom: 0.5em; }"
        ".toc-list { font-size: 11pt; }"
        ".toc-row { margin: 0.3em 0; padding: 0.2em 0; "
        "border-bottom: 1px dotted #ccc; }"
        ".toc-num { font-weight: bold; color: #555; margin-right: 0.8em; "
        "min-width: 5em; display: inline-block; }"
        ".toc a { color: #2a5c8a; text-decoration: none; }"
        ".toc a:hover { text-decoration: underline; }"
        "</style>"
    )
    full_html = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        f'{batch_css}</head>'
        f'<body{class_attr}>{"".join(sections)}</body></html>'
    )

    # Render the combined doc
    t0 = time.perf_counter()
    try:
        render_html_to_pdf(full_html, combined_pdf, body_class=body_class)
    except Exception as exc:
        return SplitResult(ok=False, error=f"render failed: {exc}")
    render_seconds = time.perf_counter() - t0

    # Split by bookmark
    t0 = time.perf_counter()
    try:
        reader = PdfReader(str(combined_pdf))
        outline = reader.outline
    except Exception as exc:
        return SplitResult(
            ok=False,
            render_seconds=render_seconds,
            error=f"read outline failed: {exc}",
        )

    # Walk outline; capture (title, page_idx) for top-level items only.
    # pypdf's outline is a list of Destination | list. Top-level = depth 0.
    # Nested list = depth 1+ (sub-headings inside the unit).
    unit_starts: list[tuple[str, int]] = []

    def walk(items, depth=0):
        if not isinstance(items, list):
            return
        for item in items:
            if isinstance(item, list):
                walk(item, depth + 1)
            else:
                title = item.title or ""
                title_clean = re.sub(r"<[^>]+>", "", title).strip()
                try:
                    page_idx = reader.get_destination_page_number(item)
                except Exception:
                    page_idx = 0
                if depth == 0:
                    unit_starts.append((title_clean, page_idx))
                # No recursion into Destination's children — pypdf's
                # list-based outline already represents them as nested
                # lists at depth 1+.

    walk(outline)

    if not unit_starts:
        return SplitResult(
            ok=False,
            render_seconds=render_seconds,
            error="no top-level bookmarks found — H1 headings missing?",
        )

    total_pages = len(reader.pages)
    units: list[tuple[str, Path]] = []
    written_keys: set[Path] = set()

    # Compute the next-unit-start for each entry. We need this because
    # the outline may contain H1s that are sub-units of the current unit
    # (e.g. "Lesson Pack" + "At-a-glance" + "Lesson" all share the same
    # physical pack). Only the H1s that map to output paths are "real"
    # unit boundaries. The end of unit N is the start of the next real unit.
    real_starts: list[tuple[str, int, Path]] = []
    for title, start_page in unit_starts:
        target = title_to_path(title)
        if target is None:
            continue
        if target in written_keys:
            log_split.warning(f"duplicate H1 '{title[:60]}' -> skipping")
            continue
        written_keys.add(target)
        real_starts.append((title, start_page, target))

    for idx, (title, start_page, target) in enumerate(real_starts):
        if idx + 1 < len(real_starts):
            end_page = real_starts[idx + 1][1]
        else:
            end_page = total_pages

        if end_page <= start_page:
            log_split.warning(
                f"empty unit '{title[:60]}' (start={start_page} end={end_page})"
            )
            continue

        writer = PdfWriter()
        for p in range(start_page, end_page):
            writer.add_page(reader.pages[p])
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "wb") as f:
            writer.write(f)
        units.append((title, target))

    split_seconds = time.perf_counter() - t0

    return SplitResult(
        ok=True,
        units=units,
        render_seconds=render_seconds,
        split_seconds=split_seconds,
    )


def relativize_pdf_links(pdf_path: Path, root_dir: Path,
                        release_path: str = "") -> int:
    """Rewrite absolute file:// links to relative paths.

    Uses a build-path → release-path mapping so links respect the
    release ZIP directory structure, not the build directory.

    Args:
        pdf_path: Path to the PDF to fix (build path).
        root_dir: Project root.
        release_path: This PDF's path in the release ZIP.

    Returns:
        Number of links rewritten.
    """
    import re
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import TextStringObject, NameObject

    # Build release-path → build-path mapping from root_dir
    # (cached on first call via function attribute)
    if not hasattr(relativize_pdf_links, '_path_map'):
        relativize_pdf_links._path_map = _build_release_path_map(root_dir)
    path_map = relativize_pdf_links._path_map

    reader = PdfReader(str(pdf_path))
    pdf_release_dir = Path(release_path).parent if release_path else Path('.')

    rewritten = 0
    for page in reader.pages:
        if '/Annots' not in page:
            continue
        annots = page['/Annots']
        for annot in annots:
            obj = annot.get_object()
            action = obj.get('/A', {})
            uri_obj = action.get('/URI')
            if uri_obj is None:
                continue
            uri = str(uri_obj)
            if not uri.startswith('file:///'):
                continue
            target_name = uri.split('/')[-1]
            # Find release path for this target filename
            candidates = [(rp, bp) for rp, bp in path_map.items()
                          if bp and bp.endswith(target_name)]
            if not candidates:
                continue
            # Prefer exact matches, then same-directory matches
            target_release = candidates[0][0]
            for rp, bp in candidates:
                if rp == release_path:
                    continue  # skip self
                if Path(rp).parent == pdf_release_dir:
                    target_release = rp
                    break
            # Compute relative path from source's release dir to target
            try:
                rel = Path(target_release).relative_to(pdf_release_dir, walk_up=True)
            except ValueError:
                # Target in different tree — use absolute relative
                rel = Path(target_release)
            action[NameObject('/URI')] = TextStringObject(rel.as_posix())
            rewritten += 1

    if rewritten > 0:
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        tmp = pdf_path.with_suffix('.tmp.pdf')
        with open(tmp, 'wb') as f:
            writer.write(f)
        tmp.replace(pdf_path)

    return rewritten


def _build_release_path_map(root_dir: Path) -> dict[str, str | None]:
    """Build mapping from release ZIP path → build path.

    Uses the release.zip if already built, otherwise returns empty.
    """
    import zipfile
    release_zip = root_dir / 'release.zip'
    if not release_zip.exists():
        return {}
    z = zipfile.ZipFile(str(release_zip))
    release_to_build: dict[str, str | None] = {}
    for rel_path in z.namelist():
        if not rel_path.endswith('.pdf'):
            continue
        filename = rel_path.split('/')[-1]
        candidates = list(root_dir.rglob(filename))
        # Filter to build/ and packs/ only
        candidates = [c for c in candidates
                      if str(c).startswith(str(root_dir / 'build'))
                      or str(c).startswith(str(root_dir / 'packs'))]
        if len(candidates) == 1:
            release_to_build[rel_path] = str(candidates[0])
        elif len(candidates) > 1:
            # Try disambiguating by directory name
            rel_dirs = set(rel_path.split('/')[:-1])
            for c in candidates:
                c_parts = str(c).replace('\\', '/').split('/')
                if any(d in c_parts for d in rel_dirs):
                    release_to_build[rel_path] = str(c)
                    break
    z.close()
    return release_to_build