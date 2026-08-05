"""Shared pytest fixtures for the curriculum test suite.

Tests run from the project root. The framework and scripts directories
are added to sys.path so tests can import modules by their script names.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "framework"))
sys.path.insert(0, str(ROOT / "scripts"))


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Path to the project root."""
    return ROOT


@pytest.fixture(scope="session")
def catalog_path() -> Path:
    """Path to the lesson catalog CSV."""
    return ROOT / "framework" / "lesson-catalog.csv"


@pytest.fixture(scope="session")
def fonts_dir() -> Path:
    """Path to the embedded Atkinson Hyperlegible font files."""
    return ROOT / "framework" / "fonts"


@pytest.fixture(scope="session")
def render_module():
    """The framework.render module (loaded once per session)."""
    import render
    return render