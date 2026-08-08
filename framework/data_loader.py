# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).
"""Loader for YAML data files in data/.

This module is the single access point for phonogram, rule, and related
curriculum data. Consumers (lesson/worksheet/game generators) call these
loaders instead of importing constants from framework/phonograms.py or
framework/rules.py.

All loaders:
  - Read data/<file>.yaml relative to project root.
  - Validate against schemas/data/<file>.schema.json (jsonschema).
  - Return immutable frozen-dataclass tuples.

Raises DataValidationError on schema or cross-file drift.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, ValidationError

# ── Paths ──────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCHEMA_DIR = PROJECT_ROOT / "schemas" / "data"


class DataValidationError(Exception):
    """Raised when YAML data fails schema validation or cross-file drift check."""


# ── Dataclasses ────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Phonogram:
    id: str
    stage: int
    kind: str
    sounds: str
    words: tuple[str, ...]
    vowel: bool = False
    sound_count: int = 1
    examples: tuple[tuple[str, str], ...] = ()
    writing: tuple[str, ...] = ()
    group: int | None = None
    rule: str | None = None


@dataclass(frozen=True)
class Rule:
    number: str
    stage: int
    name: str
    words: tuple[str, ...]


@dataclass(frozen=True)
class Sentence:
    word: str
    sentence: str


# ── Loader helpers ─────────────────────────────────────────────────────────


def _load_yaml(path: Path) -> Any:
    if not path.exists():
        raise DataValidationError(f"YAML data file missing: {path}")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _validate(data: Any, schema_path: Path, source_label: str) -> None:
    if not schema_path.exists():
        raise DataValidationError(f"Schema file missing: {schema_path}")
    with schema_path.open(encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    if errors:
        msg = "\n".join(f"  - {source_label}: {'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in errors)
        raise DataValidationError(f"Schema validation failed for {source_label}:\n{msg}")


# ── Public loaders ─────────────────────────────────────────────────────────


def load_phonograms() -> tuple[Phonogram, ...]:
    raw = _load_yaml(DATA_DIR / "phonograms.yaml")
    _validate(raw, SCHEMA_DIR / "phonograms.schema.json", "phonograms.yaml")
    out: list[Phonogram] = []
    seen: set[str] = set()
    for entry in raw["phonograms"]:
        pg_id = entry["id"]
        if pg_id in seen:
            raise DataValidationError(f"Duplicate phonogram id: {pg_id!r}")
        seen.add(pg_id)
        out.append(
            Phonogram(
                id=pg_id,
                stage=int(entry["stage"]),
                kind=entry["kind"],
                sounds=entry["sounds"],
                words=tuple(entry["words"]),
                vowel=bool(entry.get("vowel", False)),
                sound_count=int(entry.get("sound_count", 1)),
                examples=tuple((e["sound"], e["words"]) for e in entry.get("examples", [])),
                writing=tuple(entry.get("writing", [])),
                group=entry.get("group"),
                rule=entry.get("rule"),
            )
        )
    return tuple(sorted(out, key=lambda p: (p.stage, p.id)))


def load_rules() -> tuple[Rule, ...]:
    raw = _load_yaml(DATA_DIR / "rules.yaml")
    _validate(raw, SCHEMA_DIR / "rules.schema.json", "rules.yaml")
    out: list[Rule] = []
    seen: set[str] = set()
    for entry in raw["rules"]:
        num = str(entry["number"])
        if num in seen:
            raise DataValidationError(f"Duplicate rule number: {num!r}")
        seen.add(num)
        out.append(
            Rule(
                number=num,
                stage=int(entry["stage"]),
                name=entry["name"],
                words=tuple(entry["words"]),
            )
        )
    return tuple(sorted(out, key=lambda r: int(r.number)))


def load_sentences() -> tuple[Sentence, ...]:
    raw = _load_yaml(DATA_DIR / "sentences.yaml")
    _validate(raw, SCHEMA_DIR / "sentences.schema.json", "sentences.yaml")
    return tuple(Sentence(word=entry["word"], sentence=entry["sentence"]) for entry in raw["sentences"])


# Stub loaders for files whose schemas are placeholders. They validate and
# return empty tuples; populated when content lands.

def load_silent_e() -> tuple:
    raw = _load_yaml(DATA_DIR / "silent_e.yaml")
    _validate(raw, SCHEMA_DIR / "silent_e.schema.json", "silent_e.yaml")
    return tuple(raw.get("silent_e", []))


def load_roots() -> tuple:
    raw = _load_yaml(DATA_DIR / "roots.yaml")
    _validate(raw, SCHEMA_DIR / "roots.schema.json", "roots.yaml")
    return tuple(raw.get("roots", []))


def load_hf_words() -> tuple:
    raw = _load_yaml(DATA_DIR / "high_frequency_words.yaml")
    _validate(raw, SCHEMA_DIR / "high_frequency_words.schema.json", "high_frequency_words.yaml")
    return tuple(raw.get("hf_words", []))


def load_decodable_wordlists() -> tuple:
    raw = _load_yaml(DATA_DIR / "decodable_wordlists.yaml")
    _validate(raw, SCHEMA_DIR / "decodable_wordlists.schema.json", "decodable_wordlists.yaml")
    return tuple(raw.get("wordlists", []))


# ── Aggregation helpers (mirror framework/phonograms.py + rules.py API) ───


def phonograms_by_id(pgs: tuple[Phonogram, ...] | None = None) -> dict[str, Phonogram]:
    """Return dict[pg_id, Phonogram]. Loads if not provided."""
    if pgs is None:
        pgs = load_phonograms()
    return {p.id: p for p in pgs}


def phonograms_by_stage() -> dict[int, list[Phonogram]]:
    """Return dict[stage, list[Phonogram]]."""
    out: dict[int, list[Phonogram]] = {1: [], 2: [], 3: [], 4: [], 5: []}
    for p in load_phonograms():
        out.setdefault(p.stage, []).append(p)
    return out


def rules_by_number(rules: tuple[Rule, ...] | None = None) -> dict[str, Rule]:
    """Return dict[number, Rule]. Loads if not provided."""
    if rules is None:
        rules = load_rules()
    return {r.number: r for r in rules}


def rules_for_words(words: list[str], rules: tuple[Rule, ...] | None = None) -> list[str]:
    """Return rule numbers whose example words overlap with the given words.

    Used by the Spelling Aid sidebar in decodable readers.
    """
    if rules is None:
        rules = load_rules()
    text_words = {w.lower().strip(".,!?;:") for w in words}
    matches = []
    for rule in rules:
        if any(w in text_words for w in rule.words):
            matches.append(rule.number)
    return matches


def words_using_phonogram(pg: str, words: list[str]) -> list[str]:
    """Return the subset of given words that contain the phonogram pg.

    Limits to 3 examples for compact display in sidebars.
    """
    matches = []
    for w in words:
        wl = w.lower().strip(".,!?;:")
        if pg in wl:
            matches.append(wl)
    return matches[:3]


# ── Legacy dict-of-dict helpers (mirror framework/phonograms.py + rules.py API) ─


def pg_dict() -> dict[str, dict]:
    """Return phonogram catalog in legacy dict-of-dict shape.

    Returns {pg_id: {"sounds": str, "words": list[str], "stage": int}}.
    Matches the old framework/phonograms.py API used by consumer scripts.
    """
    return {
        p.id: {"sounds": p.sounds, "words": list(p.words), "stage": p.stage}
        for p in load_phonograms()
    }


def pg_stage_dict() -> dict[str, int]:
    """Return {pg_id: stage} map (legacy PG_STAGE)."""
    return {p.id: p.stage for p in load_phonograms()}


def pg_stage_buckets() -> dict[int, list[str]]:
    """Return {stage: [pg_id, ...]} map (used to split worksheets by stage)."""
    out: dict[int, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}
    for p in load_phonograms():
        out.setdefault(p.stage, []).append(p.id)
    return out


def rules_dict() -> dict[str, dict]:
    """Return rules catalog in legacy dict-of-dict shape.

    Returns {rule_number: {"name": str, "words": list[str], "stage": int}}.
    Matches the old framework/rules.py API used by consumer scripts.
    """
    return {
        r.number: {"name": r.name, "words": list(r.words), "stage": r.stage}
        for r in load_rules()
    }


def pg_kind_buckets() -> dict[str, dict[str, dict]]:
    """Return phonogram catalog split by kind (single, multi, multi3, multi4).

    Returns {"single": {pg: {...}}, "multi": {...}, "multi3": {...}, "multi4": {...}}.
    Mirrors the legacy SINGLE/MULTI/MULTI3/MULTI4 dicts from
    framework/phonograms.py — preserves teaching order so existing
    consumer output stays byte-identical.
    """
    # Teaching order (matches legacy framework/phonograms.py)
    SINGLE_ORDER = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
                    "n","o","p","qu","r","s","t","u","v","w","x","y","z"]
    MULTI_ORDER = ["sh","th","ck","ee","ng","ar","or","er","oi","oy","ai","ay",
                   "ch","wh","ea","ow","ou","oo","ed","igh","aw","au","ir","ur","oa","ear"]
    MULTI3_ORDER = ["dge","tch","kn","gn","wr","eigh","ei","ey","ph","gh","ough","augh",
                    "ew","ui","eu","wor","ie","bu","gu","q"]
    MULTI4_ORDER = ["ti","ci","si"]
    order_maps = {
        "single": SINGLE_ORDER,
        "multi": MULTI_ORDER,
        "multi3": MULTI3_ORDER,
        "multi4": MULTI4_ORDER,
    }
    buckets: dict[str, dict[str, dict]] = {
        "single": {}, "multi": {}, "multi3": {}, "multi4": {},
    }
    for p in load_phonograms():
        buckets[p.kind][p.id] = {
            "sounds": p.sounds,
            "words": list(p.words),
            "stage": p.stage,
        }
    # Re-order each bucket to match teaching order
    ordered: dict[str, dict[str, dict]] = {
        "single": {}, "multi": {}, "multi3": {}, "multi4": {},
    }
    for kind, ids in order_maps.items():
        for pg_id in ids:
            if pg_id in buckets[kind]:
                ordered[kind][pg_id] = buckets[kind][pg_id]
    return ordered


# ── CLI smoke-test ─────────────────────────────────────────────────────────


def _self_test() -> int:
    """Load everything; print summary. Used by just validate-data and tests."""
    pgs = load_phonograms()
    rules = load_rules()
    sents = load_sentences()
    print(f"  phonograms: {len(pgs)} (expect 76)")
    print(f"  rules:      {len(rules)} (expect 31)")
    print(f"  sentences:  {len(sents)}")
    return 0


if __name__ == "__main__":
    sys.exit(_self_test())
