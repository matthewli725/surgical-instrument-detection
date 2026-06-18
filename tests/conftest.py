from __future__ import annotations

from pathlib import Path

import pytest

from trayguard.learning.module import load_tray_module

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODULE_PATH = (
    PROJECT_ROOT / "config" / "tray_modules" / "fgvc12_major_focused_v1.json"
)


@pytest.fixture
def default_module():
    return load_tray_module(DEFAULT_MODULE_PATH)


@pytest.fixture
def tiny_module_payload():
    return {
        "module_id": "tiny_module",
        "version": "test",
        "name": "Tiny Module",
        "instruments": [
            {
                "id": "forceps",
                "display_name": "Forceps",
                "family": "grasping",
                "aliases": ["tissue forceps"],
                "distinguishing_features": ["two arms"],
                "study_prompts": [
                    {"id": "name", "prompt": "Name it", "answer": "Forceps"}
                ],
            },
            {
                "id": "scissors",
                "display_name": "Scissors",
                "family": "cutting",
                "aliases": [],
                "distinguishing_features": ["blades"],
                "study_prompts": [
                    {"id": "name", "prompt": "Name it", "answer": "Scissors"}
                ],
            },
            {
                "id": "clamp",
                "display_name": "Clamp",
                "family": "clamping",
                "aliases": [],
                "distinguishing_features": ["ratchet"],
                "study_prompts": [
                    {"id": "name", "prompt": "Name it", "answer": "Clamp"}
                ],
            },
        ],
        "required_items": [
            {"instrument_id": "forceps", "quantity": 1},
            {"instrument_id": "scissors", "quantity": 2},
        ],
        "distractor_item_ids": ["clamp"],
        "lookalike_pairs": [
            {
                "id": "lookalike_forceps_clamp",
                "expected_id": "forceps",
                "selected_id": "clamp",
                "feedback_message": "Forceps have two spring arms; clamps have a ratchet.",
            }
        ],
        "assessment_variants": [
            {
                "id": "forceps_only",
                "mode": "practice",
                "required_item_ids": ["forceps"],
                "distractor_item_ids": ["clamp"],
                "random_seed": "test",
                "feedback_enabled": True,
            }
        ],
        "marker_cards": [
            {"marker_id": 1, "instrument_id": "forceps", "card_id": "forceps_card"},
            {"marker_id": 2, "instrument_id": "scissors", "card_id": "scissors_card"},
            {"marker_id": 3, "instrument_id": "clamp", "card_id": "clamp_card"},
        ],
    }


@pytest.fixture
def tiny_module(tmp_path, tiny_module_payload):
    path = tmp_path / "tiny_module.json"
    import json

    path.write_text(json.dumps(tiny_module_payload), encoding="utf-8")
    return load_tray_module(path)
