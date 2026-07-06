"""
Shared progress/state persistence helpers.

Provides JSON persistence and default-state normalization for resumable
workflows.

Unit 5 - Progress Tracking Consolidation
"""

import json
from copy import deepcopy
from pathlib import Path


def copy_default_state(default_state=None):
    """Return a deep-copied default progress state."""
    return deepcopy(default_state or {})


def normalize_state(state, default_state=None):
    """
    Return state with any missing default keys populated.

    Values already present in state are preserved. Defaults are deep-copied so
    callers can safely use list/dict defaults without sharing mutable objects.
    """
    normalized = copy_default_state(default_state)

    if state:
        normalized.update(state)

    return normalized


def has_resume_data(state, keys=None):
    """
    Return True when a progress state contains resumable data.

    When keys are provided, only those state entries are considered.
    """
    if not state:
        return False

    if keys is None:
        return any(bool(value) for value in state.values())

    return any(bool(state.get(key)) for key in keys)


def ensure_state_defaults(state, default_state=None):
    """Compatibility alias for default-state recovery."""
    return normalize_state(state, default_state)


def load_json_state(path, default_state=None):
    """
    Load a JSON state file and normalize it with default_state.

    Missing files return the normalized default state. JSON parse and filesystem
    errors are intentionally allowed to propagate to the caller.
    """
    state_path = Path(path)

    if not state_path.exists():
        return normalize_state(None, default_state)

    with state_path.open("r", encoding="utf-8") as state_file:
        return normalize_state(json.load(state_file), default_state)


def save_json_state(path, state):
    """Save state to a JSON file using the project's progress-file format."""
    state_path = Path(path)

    if state_path.parent != Path("."):
        state_path.parent.mkdir(parents=True, exist_ok=True)

    with state_path.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, ensure_ascii=False, indent=2)
