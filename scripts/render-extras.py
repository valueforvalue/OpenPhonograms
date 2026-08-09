# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Render all worksheets and reader MDs to PDFs.

Renders:
  worksheets/phonograms/pg-*.md → build/worksheets/phonograms/pg-*.pdf
  worksheets/rules/rule-*.md      → build/worksheets/rules/rule-*.pdf
  worksheets/cards/*.md          → build/worksheets/cards/*.pdf
  worksheets/blank/*.md          → build/worksheets/blank/*.pdf
  readers/*.md                   → build/readers/*.pdf

Usage:
  python scripts/render-extras.py
  python scripts/render-extras.py --jobs 4
"""

import argparse
import io
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
WORKSHEETS = ROOT / "worksheets"
READERS = ROOT / "readers"
OUT = ROOT / "build"

# Import render helper from framework
sys.path.insert(0, str(ROOT))
from framework.render import render_md_to_pdf, _render_worker
from framework.build_log import (
    get_logger, phase, Progress, WorkerLogQueue,
    set_worker_queue, drain_worker_queue,
)

log = get_logger("render-extras")


def _collect_jobs(skip_existing: bool = False) -> list[tuple[Path, Path, str]]:
    """Enumerate (md_path, pdf_path, doc_type) for all worksheets + readers.

    When skip_existing=True, PDFs whose mtime is newer than their source MD
    are omitted — used for incremental builds.
    """
    jobs: list[tuple[Path, Path, str]] = []
    skipped = 0

    def _prune_orphans(out_dir: Path, expected_stems: set[str]) -> int:
        """Delete PDFs in out_dir whose stem is not in expected_stems."""
        if not out_dir.exists():
            return 0
        removed = 0
        for pdf in list(out_dir.glob("*.pdf")):
            if pdf.stem not in expected_stems:
                pdf.unlink(missing_ok=True)
                removed += 1
        return removed

    def _add(md: Path, pdf: Path, dtype: str) -> None:
        nonlocal skipped
        if skip_existing and pdf.exists() and pdf.stat().st_mtime >= md.stat().st_mtime:
            skipped += 1
            return
        jobs.append((md, pdf, dtype))

    # Worksheets (flat layout)
    for sub in ["phonograms", "rules", "cards", "blank"]:
        src_dir = WORKSHEETS / sub
        if not src_dir.exists():
            continue
        out_dir = OUT / "worksheets" / sub
        out_dir.mkdir(parents=True, exist_ok=True)
        for md in sorted(src_dir.glob("*.md")):
            _add(md, out_dir / (md.stem + ".pdf"), "worksheet")

    # Worksheets (stage-grouped mirrors)
    for sub in ["phonograms", "rules", "cards"]:
        for stage in range(1, 6):
            stage_src = WORKSHEETS / sub / f"stage-{stage}"
            if not stage_src.exists():
                continue
            stage_out = OUT / "worksheets" / sub / f"stage-{stage}"
            stage_out.mkdir(parents=True, exist_ok=True)
            for md in sorted(stage_src.glob("*.md")):
                _add(md, stage_out / (md.stem + ".pdf"), "worksheet")

    # Readers: flat layout (legacy) + per-stage subfolders.
    # Flat readers/ are mirror copies written by the stage-N generators
    # (generate-readers.py, generate-animal-readers.py). The canonical
    # render source is the stage-N/ copy; only render the flat copy when
    # no staged sibling exists (i.e. genuine stage-1 readers that were
    # never promoted to a stage-N/ subfolder).
    if READERS.exists():
        # Build the set of expected PDF stems per stage dir, then prune orphans.
        # Expected set = union of (sources about to be rendered) ∪ (PDFs already
        # up-to-date and not re-queued). This keeps skip-existing correctness:
        # we never delete a PDF whose source is still valid.
        expected_by_stage: dict[Path, set[str]] = {}
        for stage in range(1, 6):
            stage_src = READERS / f"stage-{stage}"
            stage_out = OUT / "readers" / f"stage-{stage}"
            stems: set[str] = set()
            if stage_src.exists():
                stage_out.mkdir(parents=True, exist_ok=True)
                for md in sorted(stage_src.glob("*.md")):
                    _add(md, stage_out / (md.stem + ".pdf"), "reader")
                    stems.add(md.stem)
            # Preserve any existing PDF whose stem still corresponds to a live
            # source (handles --skip-existing where the job was filtered out).
            if stage_out.exists():
                for pdf in stage_out.glob("*.pdf"):
                    if (stage_src / f"{pdf.stem}.md").exists() if stage_src.exists() else False:
                        stems.add(pdf.stem)
            expected_by_stage[stage_out] = stems
        # Flat readers with no stage-N/ sibling: render to build/readers/stage-1/.
        flat_only_stems: set[str] = set()
        flat_only_out = OUT / "readers" / "stage-1"
        if READERS.exists():
            for md in sorted(READERS.glob("*.md")):
                if md.parent != READERS:
                    continue
                if any((READERS / f"stage-{s}" / md.name).exists() for s in range(2, 6)):
                    continue
                pdf = flat_only_out / f"{md.stem}.pdf"
                flat_only_out.mkdir(parents=True, exist_ok=True)
                _add(md, pdf, "reader")
                flat_only_stems.add(md.stem)
        # Preserve any existing stage-1 PDF whose flat source is still valid.
        if flat_only_out.exists():
            for pdf in flat_only_out.glob("*.pdf"):
                if (READERS / f"{pdf.stem}.md").exists():
                    flat_only_stems.add(pdf.stem)
        expected_by_stage[flat_only_out] = flat_only_stems
        # Reconcile: delete PDFs in each stage dir that don't match expected set.
        for out_dir, expected in expected_by_stage.items():
            removed = _prune_orphans(out_dir, expected)
            if removed:
                log.info(f"pruned {removed} orphan PDF(s) from {out_dir.relative_to(ROOT)}")

    if skip_existing and skipped:
        log.info(f"skip-existing: {skipped} PDFs up-to-date, {len(jobs)} to render")
    return jobs


def _run_serial(jobs: list[tuple[Path, Path, str]]) -> int:
    for md, pdf, dtype in jobs:
        render_md_to_pdf(md, pdf, doc_type=dtype)
    return len(jobs)


def _run_parallel(jobs: list[tuple[Path, Path, str]], workers: int) -> int:
    queue = WorkerLogQueue()
    set_worker_queue(queue)
    log.info(f"render-extras: {len(jobs)} files, {workers} workers")
    with Progress("render-extras", total=len(jobs)) as progress:
        executor = ProcessPoolExecutor(max_workers=workers)
        try:
            futures = [
                executor.submit(_render_worker, str(md), str(pdf), dtype)
                for md, pdf, dtype in jobs
            ]
            ok = 0
            for fut in as_completed(futures):
                drain_worker_queue(queue, log)
                try:
                    fut.result()
                    ok += 1
                except Exception as exc:
                    log.error(f"FAIL: {exc}")
                progress.tick()
                drain_worker_queue(queue, log)
        finally:
            executor.shutdown(wait=True)
            set_worker_queue(None)
    return ok


def main():
    parser = argparse.ArgumentParser(description="Render worksheets + readers to PDFs")
    parser.add_argument("--jobs", "-j", type=int, default=4, help="Parallel worker processes (default: 4)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip PDFs whose mtime is newer than source MD (incremental build).")
    args = parser.parse_args()

    phase("Render Worksheets + Readers")
    jobs = _collect_jobs(skip_existing=args.skip_existing)
    if not jobs:
        log.info("no worksheets or readers found" + (" (all up-to-date)" if args.skip_existing else ""))
        return
    if args.jobs > 1:
        ok = _run_parallel(jobs, args.jobs)
    else:
        ok = _run_serial(jobs)
    log.info(f"rendered {ok}/{len(jobs)} worksheet/reader PDFs")


if __name__ == "__main__":
    main()
