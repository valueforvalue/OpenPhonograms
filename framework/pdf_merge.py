# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
pdf_merge.py — Combine multiple PDFs into a single pack via pypdf.

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

  Render-on-demand fallback:
  If a component PDF is missing, the caller is expected to fall back
  to inline render-to-PDF. This module does NOT render PDFs itself.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class CompileResult:
    ok: bool
    page_count: int = 0
    missing: list[Path] = field(default_factory=list)
    merged_paths: list[Path] = field(default_factory=list)
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

    # Lazy import keeps the module cheap to import + test.

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
