"""Load the skill's config.json into a dict, merged over sane defaults.

config.json lives at the skill root (sibling of .env) and is git-ignored — it
holds per-user setup: note type, field mapping, deck names, the decks that count
as "known vocabulary", and where the sentence banks live. It is written by
`setup.py` (driven by the `/sentence-mining setup` interview).

Every script imports `load_config()` so there is ONE source of truth and zero
hardcoded "Ray"-specific names left in the scripts.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config.json"

# Keys whose string values are filesystem paths and should be ~-expanded on load.
_PATH_KEYS = {"jpdb_priority_csv", "work_dir"}
_NESTED_PATH_KEYS = {
    "banks": {"source_dir", "index_dir"},
}

DEFAULTS: dict = {
    "anki_connect_url": "http://localhost:8765",
    # The note type new cards are created on, plus how its fields map to the
    # skill's internal field roles. Only mapped (non-empty) roles get written,
    # so any note type with at least `word` + `sentence` works.
    "note_type": "",
    "field_map": {
        "word": "",
        "reading": "",
        "sentence": "",
        "sentence_audio": "",
        "picture": "",
        "explanation": "",
        "explanation_audio": "",
        "source_url": "",
    },
    "decks": {
        "main": "",       # i+1 cards (one unknown) — daily review
        "deferred": "",   # i+2/i+3 cards — optional; falls back to main if empty
    },
    # Self-contained re-implementation of AnkiMorphs' "known morphs" idea: each
    # source is an Anki search + the note field to mine. We tokenize that field
    # with SudachiPy and record each lemma's highest card interval; lemma is "known"
    # once that interval >= interval_threshold (AnkiMorphs' default is 21 days).
    "known_words": {
        "interval_threshold": 21,
        "cache_hours": 6,  # reuse the scanned known-set for N hours (0 = always rescan)
        "sources": [],     # [{"query": "deck:\"My Mining\"", "field": "sentence"}, ...]
    },
    # Optional frequency list for ranking unknowns (lower line = more frequent).
    # Absent/empty → ranking degrades gracefully to source order.
    "jpdb_priority_csv": "",
    "banks": {
        "source_dir": "",  # folder of .apkg sentence banks to fall back on
        "index_dir": "~/Downloads/sentence-mining/banks/index",
    },
    "work_dir": "~/Downloads/sentence-mining",
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _expand_paths(cfg: dict) -> dict:
    for k in _PATH_KEYS:
        if cfg.get(k):
            cfg[k] = str(Path(cfg[k]).expanduser())
    for parent, keys in _NESTED_PATH_KEYS.items():
        for k in keys:
            if cfg.get(parent, {}).get(k):
                cfg[parent][k] = str(Path(cfg[parent][k]).expanduser())
    return cfg


def config_exists() -> bool:
    return CONFIG_PATH.exists()


def load_config(required: bool = True) -> dict | None:
    """Return the merged config dict, or None if absent and not required.

    When required and missing, exits with a message pointing at setup.
    """
    if not CONFIG_PATH.exists():
        if required:
            raise SystemExit(
                "No config.json found for sentence-mining.\n"
                "Run `/sentence-mining setup` (or `python3 scripts/setup.py --probe`) "
                "to create it."
            )
        return None
    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return _expand_paths(_deep_merge(DEFAULTS, raw))


def write_config(cfg: dict) -> Path:
    """Write config.json (merged over defaults so partial input is fine)."""
    merged = _deep_merge(DEFAULTS, cfg)
    CONFIG_PATH.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return CONFIG_PATH


def deck_main(cfg: dict) -> str:
    return cfg["decks"].get("main", "") or ""


def deck_deferred(cfg: dict) -> str:
    """Deferred deck, falling back to the main deck when unset."""
    return cfg["decks"].get("deferred", "") or deck_main(cfg)
