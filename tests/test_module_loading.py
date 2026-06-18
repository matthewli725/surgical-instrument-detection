from __future__ import annotations

import copy
import json

import pytest

from trayguard.learning.module import load_tray_module


def write_payload(tmp_path, payload):
    path = tmp_path / "module.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_default_module_loads(default_module):
    assert default_module.module_id == "fgvc12_major_focused_v1"
    assert default_module.total_required_units > 0
    assert default_module.marker_map


def test_unknown_required_item_raises(tmp_path, tiny_module_payload):
    payload = copy.deepcopy(tiny_module_payload)
    payload["required_items"].append({"instrument_id": "unknown", "quantity": 1})

    with pytest.raises(ValueError, match="Required item"):
        load_tray_module(write_payload(tmp_path, payload))


def test_duplicate_marker_ids_raise(tmp_path, tiny_module_payload):
    payload = copy.deepcopy(tiny_module_payload)
    payload["marker_cards"][1]["marker_id"] = payload["marker_cards"][0]["marker_id"]

    with pytest.raises(ValueError, match="Marker card IDs"):
        load_tray_module(write_payload(tmp_path, payload))


def test_variant_unknown_instrument_raises(tmp_path, tiny_module_payload):
    payload = copy.deepcopy(tiny_module_payload)
    payload["assessment_variants"][0]["distractor_item_ids"].append("unknown")

    with pytest.raises(ValueError, match="unknown instrument"):
        load_tray_module(write_payload(tmp_path, payload))


def test_variant_required_item_must_be_required_item(tmp_path, tiny_module_payload):
    payload = copy.deepcopy(tiny_module_payload)
    payload["assessment_variants"][0]["required_item_ids"].append("clamp")

    with pytest.raises(ValueError, match="not declared in required_items"):
        load_tray_module(write_payload(tmp_path, payload))
