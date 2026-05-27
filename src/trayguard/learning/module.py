from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from trayguard.learning.models import (
    AssessmentVariant,
    Instrument,
    LookalikePair,
    MarkerCard,
    RequiredItem,
    TrayModule,
)


def _require_keys(payload: dict[str, Any], keys: set[str], context: str) -> None:
    missing = sorted(keys - set(payload))
    if missing:
        raise ValueError(f"{context} is missing required field(s): {', '.join(missing)}")


def load_tray_module(path: str | Path) -> TrayModule:
    module_path = Path(path)
    payload = json.loads(module_path.read_text(encoding="utf-8"))
    _require_keys(payload, {"module_id", "version", "name", "instruments", "required_items"}, str(module_path))

    instruments = {
        row["id"]: Instrument(
            id=row["id"],
            display_name=row["display_name"],
            family=row.get("family", ""),
            aliases=list(row.get("aliases", [])),
            distinguishing_features=list(row.get("distinguishing_features", [])),
            image_refs=list(row.get("image_refs", [])),
            study_prompts=list(row.get("study_prompts", [])),
            local_verification_status=row.get("local_verification_status", "pending_review"),
        )
        for row in payload["instruments"]
    }

    required_items = {
        row["instrument_id"]: RequiredItem(
            instrument_id=row["instrument_id"],
            quantity=max(0, int(row["quantity"])),
            reference_number=row.get("reference_number", ""),
            location_or_layer=row.get("location_or_layer", ""),
            notes=row.get("notes", ""),
        )
        for row in payload["required_items"]
    }

    unknown_required = sorted(set(required_items) - set(instruments))
    if unknown_required:
        raise ValueError(f"Required item(s) are not declared instruments: {', '.join(unknown_required)}")

    distractor_item_ids = list(payload.get("distractor_item_ids", []))
    unknown_distractors = sorted(set(distractor_item_ids) - set(instruments))
    if unknown_distractors:
        raise ValueError(f"Distractor item(s) are not declared instruments: {', '.join(unknown_distractors)}")

    lookalike_pairs = [
        LookalikePair(
            id=row["id"],
            expected_id=row["expected_id"],
            selected_id=row["selected_id"],
            feedback_message=row.get("feedback_message", ""),
        )
        for row in payload.get("lookalike_pairs", [])
    ]

    assessment_variants = {
        row["id"]: AssessmentVariant(
            id=row["id"],
            mode=row["mode"],
            required_item_ids=list(row.get("required_item_ids", [])),
            distractor_item_ids=list(row.get("distractor_item_ids", [])),
            random_seed=row.get("random_seed", ""),
            feedback_enabled=bool(row.get("feedback_enabled", False)),
        )
        for row in payload.get("assessment_variants", [])
    }

    marker_cards = [
        MarkerCard(
            marker_id=int(row["marker_id"]),
            instrument_id=row["instrument_id"],
            card_id=row.get("card_id", f"card_{row['marker_id']}"),
            role=row.get("role", "assessment"),
        )
        for row in payload.get("marker_cards", [])
    ]
    unknown_markers = sorted({card.instrument_id for card in marker_cards} - set(instruments))
    if unknown_markers:
        raise ValueError(f"Marker card(s) refer to unknown instruments: {', '.join(unknown_markers)}")
    marker_ids = [card.marker_id for card in marker_cards]
    if len(marker_ids) != len(set(marker_ids)):
        raise ValueError("Marker card IDs must be unique.")

    return TrayModule(
        module_id=payload["module_id"],
        version=payload["version"],
        name=payload["name"],
        procedure_family=payload.get("procedure_family", ""),
        source_note=payload.get("source_note", ""),
        instruments=instruments,
        required_items=required_items,
        distractor_item_ids=distractor_item_ids,
        lookalike_pairs=lookalike_pairs,
        assessment_variants=assessment_variants,
        marker_cards=marker_cards,
    )
