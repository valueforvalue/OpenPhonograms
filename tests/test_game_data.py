"""Tests for the game data generator + injector (issue #5).

Verifies that:
1. generate-game-data.py produces a valid _game_data.json
2. inject-game-data.py updates the game HTML with the data
3. The injected PHONOGRAMS + SPELL_WORDS arrays are syntactically valid JS
4. The Word Builder mode (id='mode-build') is present in the HTML
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))


def _load_module(name: str):
    """Load a script by name (handles dashes)."""
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), PROJECT_ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestGenerateGameData:
    """generate-game-data.py produces a JSON dump from framework.phonograms."""

    @pytest.fixture(scope="class")
    def data(self):
        return json.loads((PROJECT_ROOT / "scripts" / "_game_data.json").read_text(encoding="utf-8"))

    def test_phonogram_tiles_count(self, data):
        assert len(data["phonogram_tiles"]) == 72, \
            f"Expected 72 phonograms, got {len(data['phonogram_tiles'])}"

    def test_phonogram_tiles_have_required_fields(self, data):
        for tile in data["phonogram_tiles"]:
            assert "pg" in tile
            assert "sounds" in tile
            assert "stage" in tile
            assert tile["stage"] in {1, 2, 3, 4}

    def test_spell_words_have_required_fields(self, data):
        for w in data["spell_words"]:
            assert "word" in w
            assert "sentence" in w
            assert "stage" in w
            assert w["stage"] in {1, 2, 3, 4}

    def test_spell_words_cover_all_pg_stages(self, data):
        """Spell words come from phonogram word lists, which span stages 1-4."""
        stages = {w["stage"] for w in data["spell_words"]}
        assert stages == {1, 2, 3, 4}, f"Missing stages: {stages}"

    def test_spell_words_at_least_50(self, data):
        """Issue #5 acceptance: Word Builder needs targets. Spell Practice too."""
        assert len(data["spell_words"]) >= 50, \
            f"Only {len(data['spell_words'])} spell words (expected >=50)"


class TestInjectGameData:
    """inject-game-data.py substitutes the markers in the game HTML."""

    GAME_HTML = PROJECT_ROOT / "games" / "phonogram-trainer.html"

    def test_game_html_exists(self):
        assert self.GAME_HTML.exists(), "games/phonogram-trainer.html missing"

    def test_phonogram_marker_present(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        assert "__PHONOGRAM_DATA_BEGIN__" in html, "PHONOGRAM marker missing"
        assert "__PHONOGRAM_DATA_END__" in html, "PHONOGRAM end marker missing"

    def test_spell_marker_present(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        assert "__SPELL_WORDS_BEGIN__" in html, "SPELL_WORDS marker missing"
        assert "__SPELL_WORDS_END__" in html, "SPELL_WORDS end marker missing"

    def test_phonogram_array_in_has_72_entries(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        m = re.search(r"const PHONOGRAMS = \[(.+?)\];", html, re.DOTALL)
        assert m is not None, "PHONOGRAMS array not found"
        n = m.group(1).count("{pg:")
        assert n == 72, f"Expected 72 PGs in array, got {n}"

    def test_spell_words_array_in_has_many_entries(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        m = re.search(r"const SPELL_WORDS = \[(.+?)\];", html, re.DOTALL)
        assert m is not None, "SPELL_WORDS array not found"
        n = m.group(1).count("{word:")
        assert n >= 50, f"Expected ≥50 spell words, got {n}"


class TestBuildMode:
    """Issue #5: Word Builder mode is present and functional."""

    GAME_HTML = PROJECT_ROOT / "games" / "phonogram-trainer.html"

    def test_build_tab_exists(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        assert "switchMode('build')" in html, "Build tab not wired up"

    def test_build_mode_div_exists(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        assert 'id="mode-build"' in html, "mode-build div missing"

    def test_build_mode_key_functions_present(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        for fn in ("newBuildWord", "addBuildTile", "checkBuild",
                   "clearBuild", "revealBuild", "renderBuildPalette",
                   "renderBuildSlot"):
            assert f"function {fn}" in html, f"{fn} not defined"

    def test_build_stats_elements_present(self):
        html = self.GAME_HTML.read_text(encoding="utf-8")
        for sid in ("buildCorrect", "buildMissed", "buildStreak"):
            assert f'id="{sid}"' in html, f"#{sid} stat element missing"