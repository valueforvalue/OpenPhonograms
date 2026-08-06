# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""
build_log.py — shared logging + progress reporting for the curriculum build.

Provides:
  - get_logger(name)            — stdlib logger with file + console handlers
  - build_log_path()            — path to the current build's log file
  - Progress                    — minimal context manager (no rich dep)
  - WorkerLogQueue / WorkerLogHandler — main-process aggregation of worker logs

Design constraints:
  - Zero new dependencies. Uses stdlib logging + ANSI escape codes.
  - Header lines indented 80 chars with ─ for visual separation when run
    through `just` recipes.
  - File handler is process-safe (append mode, no shared in-memory state).
  - Console handler is single-process only. Workers must use WorkerLogQueue.

Log file location:
  build/logs/build-YYYYMMDD-HHMMSS.log

Future: if we add `rich` to deps, swap the ConsoleHandler for RichHandler
and replace Progress with rich.progress.Progress.
"""

import logging
import os
import queue
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = PROJECT_ROOT / "build"
LOGS_DIR = BUILD_DIR / "logs"


# 80-char ruler line for visual separation between build phases.
RULER = "─" * 80


# ---------------------------------------------------------------------------
# Log file path (one per process invocation of `just build`)
# ---------------------------------------------------------------------------

_log_file_path: Optional[Path] = None


def build_log_path() -> Path:
    """Return the path to the current build's log file. Created lazily."""
    global _log_file_path
    if _log_file_path is None:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        _log_file_path = LOGS_DIR / f"build-{stamp}.log"
    return _log_file_path


# ---------------------------------------------------------------------------
# Console handler that loses ANSI on non-TTY (Windows stdio, CI logs)
# ---------------------------------------------------------------------------

class _ConsoleHandler(logging.StreamHandler):
    """StreamHandler that strips ANSI codes when stdout is not a TTY."""

    ANSI_RE = None  # lazy: avoid re import at module load

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            stream = self.stream
            # Strip ANSI if not a TTY (so pipes, redirected files stay clean)
            if not hasattr(stream, "isatty") or not stream.isatty():
                if self.ANSI_RE is None:
                    import re
                    _ConsoleHandler.ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
                msg = self.ANSI_RE.sub("", msg)
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:  # never let logging crash the build
            self.handleError(record)


# ---------------------------------------------------------------------------
# Root logger setup (idempotent)
# ---------------------------------------------------------------------------

_configured = False
_config_lock = threading.Lock()


def _configure_root() -> None:
    global _configured
    with _config_lock:
        if _configured:
            return

        root = logging.getLogger("build")
        root.setLevel(logging.DEBUG)
        root.propagate = False  # don't double-log via root

        fmt = logging.Formatter(
            "%(asctime)s %(levelname)-7s %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )

        log_path = build_log_path()
        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)

        console = _ConsoleHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(fmt)

        # Replace any existing handlers (HMR-safe, re-import-safe)
        root.handlers.clear()
        root.addHandler(file_handler)
        root.addHandler(console)

        _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the 'build' namespace."""
    _configure_root()
    return logging.getLogger(f"build.{name}")


# ---------------------------------------------------------------------------
# Progress reporter (no rich dependency)
# ---------------------------------------------------------------------------

class Progress:
    """Minimal progress bar.

    Prints one line per task on completion. For longer-running parallel work,
    workers write to a WorkerLogQueue and the main process prints them.

    Usage:
        with Progress("Rendering", total=248) as p:
            for item in items:
                do_work(item)
                p.tick()
    """

    def __init__(self, label: str, total: int, log: Optional[logging.Logger] = None):
        self.label = label
        self.total = total
        self.log = log or get_logger("progress")
        self.count = 0
        self._start = None

    def __enter__(self) -> "Progress":
        import time
        self._start = time.monotonic()
        self.log.info(f"{self.label}: 0/{self.total} (0%)")
        return self

    def tick(self, n: int = 1) -> None:
        self.count += n
        if self.total:
            pct = self.count * 100 // self.total
            # Only log every 5% or at completion to avoid log spam
            if pct % 5 == 0 or self.count == self.total:
                self.log.info(f"{self.label}: {self.count}/{self.total} ({pct}%)")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        import time
        elapsed = time.monotonic() - (self._start or time.monotonic())
        self.log.info(f"{self.label}: done in {elapsed:.1f}s")


# ---------------------------------------------------------------------------
# Worker → main log aggregation (for ProcessPoolExecutor)
# ---------------------------------------------------------------------------

class WorkerLogQueue:
    """Thread-safe queue that worker processes feed log records into.

    The main process drains the queue and re-emits records through the
    'build' logger so they appear in the console + log file alongside
    everything else.
    """

    def __init__(self) -> None:
        self._q: "queue.Queue[logging.LogRecord]" = queue.Queue()

    def put(self, record: logging.LogRecord) -> None:
        self._q.put(record)

    def drain(self, timeout: float = 0.1) -> list[logging.LogRecord]:
        """Pull all available records. Non-blocking after first timeout."""
        records = []
        while True:
            try:
                records.append(self._q.get(timeout=timeout))
            except queue.Empty:
                break
        return records


_worker_queue: Optional[WorkerLogQueue] = None


def set_worker_queue(q: Optional[WorkerLogQueue]) -> None:
    """Inject the queue workers should write to. Called by main process."""
    global _worker_queue
    _worker_queue = q


def get_worker_queue() -> Optional[WorkerLogQueue]:
    return _worker_queue


class WorkerLogHandler(logging.Handler):
    """Logging handler that forwards records to a shared WorkerLogQueue.

    Workers emit records via this handler. The main process drains the
    queue and re-emits them through its own logger.
    """

    def __init__(self) -> None:
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        q = get_worker_queue()
        if q is None:
            # No queue — fall back to stderr so we don't lose messages
            sys.stderr.write(self.format(record) + "\n")
            sys.stderr.flush()
            return
        try:
            q.put(record)
        except Exception:
            pass


def attach_worker_handler(logger: logging.Logger) -> None:
    """Add a WorkerLogHandler to a worker-side logger. Idempotent."""
    for h in logger.handlers:
        if isinstance(h, WorkerLogHandler):
            return
    logger.addHandler(WorkerLogHandler())
    logger.setLevel(logging.DEBUG)
    logger.propagate = False


def drain_worker_queue(q: WorkerLogQueue, target: logging.Logger) -> int:
    """Drain queued worker records and re-emit through `target`. Returns count."""
    records = q.drain()
    for rec in records:
        target.handle(rec)
    return len(records)


# ---------------------------------------------------------------------------
# Convenience: phase banner
# ---------------------------------------------------------------------------

def phase(label: str) -> None:
    """Print a visual separator + label for a new build phase."""
    log = get_logger("phase")
    log.info(RULER)
    log.info(f"  {label}")
    log.info(RULER)
