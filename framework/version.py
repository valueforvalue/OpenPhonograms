"""Read VERSION file at repo root. Single source of truth for build version."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_version() -> str:
    """Return the current version string from the VERSION file."""
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def get_version_long() -> str:
    """Version + git short hash, e.g. '1.0.0 (9d53016)'.

    Falls back to bare version when git is unavailable (e.g. release tarball).
    """
    import subprocess
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"{get_version()} ({sha})"
    except Exception:
        return get_version()