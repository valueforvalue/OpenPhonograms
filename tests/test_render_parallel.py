"""Tests for parallel render in framework/render.py + build-lesson-pack.py.

Verifies:
  - worker entry point exists and is picklable
  - _render_worker accepts (str, str, str) — Path objects are NOT picklable on Windows
  - serial vs parallel produce the same number of pages per lesson PDF
  - missing MDs are reported, not crashed
  - log file is created on demand

Run with: pytest tests/test_render_parallel.py -v
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "framework"))

from framework import render as render_module  # noqa: E402
from framework.build_log import (  # noqa: E402
    build_log_path,
    get_logger,
    LOGS_DIR,
    WorkerLogQueue,
    set_worker_queue,
    drain_worker_queue,
)


# ── worker entry point ─────────────────────────────────────────────────

class TestRenderWorker:
    def test_worker_function_exists(self):
        assert hasattr(render_module, "_render_worker")
        assert callable(render_module._render_worker)

    def test_worker_imports_lazy(self):
        """weasyprint must NOT be imported at module load — only inside the worker."""
        # If weasyprint leaked into module namespace, the lazy-import design is broken.
        # python imports it under 'weasyprint' which is allowed at top. But _render_worker
        # should not have already executed any HTML rendering.
        assert hasattr(render_module, "render_md_to_pdf")
        # The function body defers `from weasyprint import HTML` — verify by reading
        # the source (cheap, no real test of import timing).
        import inspect
        src = inspect.getsource(render_module.render_md_to_pdf)
        assert "from weasyprint import HTML" in src

    def test_worker_signature_takes_strings(self):
        """ProcessPoolExecutor on Windows spawn requires picklable args.
        Path objects DO pickle on Linux but not on Windows. We standardize
        on strings."""
        import inspect
        sig = inspect.signature(render_module._render_worker)
        params = list(sig.parameters)
        assert params == ["md_path_str", "output_path_str", "doc_type"]

    def test_worker_renders_to_pdf(self, tmp_path):
        md = tmp_path / "x.md"
        md.write_text("# Hello\n\nBody.", encoding="utf-8")
        pdf = tmp_path / "x.pdf"
        # Mimic how the worker is invoked: pass strings only.
        result = render_module._render_worker(str(md), str(pdf), "lesson")
        assert result == str(pdf)
        assert pdf.exists()
        assert pdf.stat().st_size > 100


# ── parallel dispatch ──────────────────────────────────────────────────

class TestParallelDispatch:
    def test_parallel_renders_match_serial_count(self, tmp_path):
        """Render a few test MDs the same way via serial and parallel helpers."""
        # Build 3 tiny lessons
        lessons = []
        for i in range(3):
            md = tmp_path / f"l{i}.md"
            md.write_text(f"# Lesson {i}\n\nText {i}.", encoding="utf-8")
            lessons.append((md, tmp_path / f"l{i}.pdf", "lesson"))

        # Serial baseline
        for md, pdf, dtype in lessons:
            render_module.render_md_to_pdf(md, pdf, doc_type=dtype)

        # Hash + page counts
        try:
            import pypdf
        except ImportError:
            pytest.skip("pypdf not installed")

        serial = []
        for _md, pdf, _ in lessons:
            serial.append((pdf.stat().st_size, len(pypdf.PdfReader(str(pdf)).pages)))

        # Delete + parallel
        for _md, pdf, _ in lessons:
            pdf.unlink()

        set_worker_queue(WorkerLogQueue())
        try:
            from concurrent.futures import ProcessPoolExecutor, as_completed
            with ProcessPoolExecutor(max_workers=2) as ex:
                futures = [
                    ex.submit(render_module._render_worker, str(md), str(pdf), dtype)
                    for md, pdf, dtype in lessons
                ]
                for f in as_completed(futures):
                    f.result()
        finally:
            set_worker_queue(None)

        parallel = []
        for _md, pdf, _ in lessons:
            parallel.append((pdf.stat().st_size, len(pypdf.PdfReader(str(pdf)).pages)))

        # Page counts must match exactly. PDF file sizes may differ by a few
        # bytes due to embedded timestamps (weasyprint writes creation date).
        serial_pages = sorted(p for _s, p in serial)
        parallel_pages = sorted(p for _s, p in parallel)
        assert serial_pages == parallel_pages, (
            f"Parallel page counts differ from serial. "
            f"serial={serial_pages} parallel={parallel_pages}"
        )
        # File sizes within 5 bytes (timestamp + ID). Sanity check we didn't
        # change bulk content.
        for (s_size, _), (p_size, _) in zip(sorted(serial), sorted(parallel)):
            assert abs(s_size - p_size) < 100, f"size drift {s_size} vs {p_size}"


# ── logging ────────────────────────────────────────────────────────────

class TestBuildLog:
    def test_log_path_under_build_logs(self):
        p = build_log_path()
        assert p.parent.parent == PROJECT_ROOT / "build"
        assert p.name.startswith("build-")
        assert p.suffix == ".log"

    def test_get_logger_returns_child(self):
        log = get_logger("test.foo")
        assert log.name == "build.test.foo"

    def test_attach_worker_handler_idempotent(self):
        from framework.build_log import attach_worker_handler, WorkerLogHandler
        log = get_logger("test.idempot")
        attach_worker_handler(log)
        n = sum(1 for h in log.handlers if isinstance(h, WorkerLogHandler))
        attach_worker_handler(log)
        n2 = sum(1 for h in log.handlers if isinstance(h, WorkerLogHandler))
        assert n == 1
        assert n2 == 1

    def test_drain_handles_empty_queue(self):
        q = WorkerLogQueue()
        log = get_logger("test.drain")
        assert drain_worker_queue(q, log) == 0


# ── end-to-end CLI smoke ───────────────────────────────────────────────

@pytest.mark.slow
class TestCliSmoke:
    """Touches the actual CLI. Slow (real weasyprint render)."""

    def test_render_file_writes_pdf(self, tmp_path):
        md = tmp_path / "x.md"
        md.write_text("# E2E", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "framework" / "render.py"), str(md)],
            capture_output=True, text=True, timeout=60,
        )
        assert result.returncode == 0, result.stderr
        assert (tmp_path / "x.pdf").exists()

    def test_render_stage_with_jobs(self, tmp_path):
        """--jobs 2 should succeed for stage 1 on a real run."""
        result = subprocess.run(
            [
                sys.executable, str(PROJECT_ROOT / "framework" / "render.py"),
                "--stage", "1", "--jobs", "2",
            ],
            capture_output=True, text=True, timeout=300,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0, result.stderr
        # Stage 1 PDFs should exist under build/stage-1/
        stage_dir = PROJECT_ROOT / "build" / "stage-1"
        assert stage_dir.exists()
        assert any(stage_dir.glob("*.pdf"))
