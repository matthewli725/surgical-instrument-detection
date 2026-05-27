from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from trayguard.learning.models import AttemptResult, ItemResult, LookalikePair, TrayModule


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _instrument_name(module: TrayModule, instrument_id: str) -> str:
    if not instrument_id:
        return ""
    instrument = module.instruments.get(instrument_id)
    return instrument.display_name if instrument else instrument_id


def _lookalike_lookup(module: TrayModule) -> dict[tuple[str, str], LookalikePair]:
    return {(pair.expected_id, pair.selected_id): pair for pair in module.lookalike_pairs}


def _pop_pair(missing: list[str], surplus: list[str], lookup: dict[tuple[str, str], LookalikePair]) -> tuple[str, str, LookalikePair] | None:
    for expected_id in list(missing):
        for selected_id in list(surplus):
            pair = lookup.get((expected_id, selected_id))
            if pair is not None:
                missing.remove(expected_id)
                surplus.remove(selected_id)
                return expected_id, selected_id, pair
    return None


def _pop_wrong_pair(missing: list[str], surplus: list[str]) -> tuple[str, str] | None:
    if not missing or not surplus:
        return None
    return missing.pop(0), surplus.pop(0)


def score_tray(
    module: TrayModule,
    variant_id: str,
    selected_counts: dict[str, int],
    *,
    run_id: str = "",
    learner_id_hash: str = "",
    participant_group: str = "",
    prior_experience_level: str = "",
    mode: str = "practice",
    started_at: str | None = None,
    completed_at: str | None = None,
    duration_seconds: float = 0,
    overall_confidence: int | None = None,
    not_sure: bool = False,
    help_requests_count: int = 0,
    blocking_help_requests: int = 0,
    completed_full_flow: bool = False,
) -> AttemptResult:
    selected = Counter({key: max(0, int(value)) for key, value in selected_counts.items() if int(value) > 0})
    required = Counter({key: item.quantity for key, item in module.required_items.items()})

    missing_units: list[str] = []
    surplus_units: list[str] = []
    correct_units = 0
    item_results: list[ItemResult] = []

    for instrument_id, required_qty in required.items():
        selected_qty = selected[instrument_id]
        correct_qty = min(selected_qty, required_qty)
        correct_units += correct_qty
        if selected_qty < required_qty:
            missing_units.extend([instrument_id] * (required_qty - selected_qty))
        elif selected_qty > required_qty:
            surplus_units.extend([instrument_id] * (selected_qty - required_qty))

    for instrument_id, selected_qty in selected.items():
        if instrument_id not in required:
            surplus_units.extend([instrument_id] * selected_qty)

    missing_count = 0
    extra_count = 0
    wrong_count = 0
    misidentified_count = 0
    wrong_count_error_count = 0

    lookup = _lookalike_lookup(module)
    paired_expected: set[str] = set()

    while True:
        pair = _pop_pair(missing_units, surplus_units, lookup)
        if pair is None:
            break
        expected_id, selected_id, lookalike = pair
        misidentified_count += 1
        paired_expected.add(expected_id)
        item_results.append(
            _item_result(
                module,
                expected_id,
                selected_id,
                selected[selected_id],
                "misidentified",
                lookalike.id,
                overall_confidence,
                not_sure,
                lookalike.id,
            )
        )

    while True:
        pair = _pop_wrong_pair(missing_units, surplus_units)
        if pair is None:
            break
        expected_id, selected_id = pair
        wrong_count += 1
        paired_expected.add(expected_id)
        item_results.append(
            _item_result(module, expected_id, selected_id, selected[selected_id], "wrong", "", overall_confidence, not_sure, "wrong")
        )

    for expected_id in missing_units:
        missing_count += 1
        item_results.append(_item_result(module, expected_id, "", 0, "missing", "", overall_confidence, not_sure, "missing"))

    for selected_id in surplus_units:
        extra_count += 1
        item_results.append(_item_result(module, "", selected_id, selected[selected_id], "extra", "", overall_confidence, not_sure, "extra"))

    for instrument_id, required_qty in required.items():
        selected_qty = selected[instrument_id]
        if selected_qty != required_qty:
            wrong_count_error_count += 1
            if instrument_id not in paired_expected and selected_qty > 0:
                item_results.append(
                    _item_result(
                        module,
                        instrument_id,
                        instrument_id,
                        selected_qty,
                        "wrong_count",
                        "",
                        overall_confidence,
                        not_sure,
                        "wrong_count",
                    )
                )
        elif instrument_id not in paired_expected:
            item_results.append(
                _item_result(module, instrument_id, instrument_id, selected_qty, "correct", "", overall_confidence, not_sure, "")
            )

    error_points = missing_count + extra_count + wrong_count + misidentified_count
    total_required_units = module.total_required_units
    accuracy_score = max(0.0, 100 * (1 - error_points / total_required_units)) if total_required_units else 0.0
    required_recall = 100 * (correct_units / total_required_units) if total_required_units else 0.0
    high_confidence_error_count = sum(1 for item in item_results if item.is_high_confidence_error)
    low_confidence_correct_count = sum(1 for item in item_results if item.is_low_confidence_correct)

    return AttemptResult(
        run_id=run_id,
        learner_id_hash=learner_id_hash,
        participant_group=participant_group,
        prior_experience_level=prior_experience_level,
        tray_module_id=module.module_id,
        tray_module_version=module.version,
        assessment_variant_id=variant_id,
        mode=mode,
        started_at=started_at or _now(),
        completed_at=completed_at or _now(),
        duration_seconds=round(float(duration_seconds), 3),
        completed_full_flow=completed_full_flow,
        help_requests_count=help_requests_count,
        blocking_help_requests=blocking_help_requests,
        confidence_scale="1-5",
        overall_confidence=overall_confidence,
        total_required_units=total_required_units,
        selected_units=sum(selected.values()),
        correct_units=correct_units,
        error_points=error_points,
        accuracy_score=round(accuracy_score, 2),
        required_recall=round(required_recall, 2),
        missing_count=missing_count,
        extra_count=extra_count,
        wrong_substitution_count=wrong_count,
        misidentified_count=misidentified_count,
        wrong_count_error_count=wrong_count_error_count,
        not_sure_count=1 if not_sure else 0,
        high_confidence_error_count=high_confidence_error_count,
        low_confidence_correct_count=low_confidence_correct_count,
        item_results=item_results,
    )


def _item_result(
    module: TrayModule,
    expected_id: str,
    selected_id: str,
    selected_quantity: int,
    category: str,
    lookalike_pair_id: str,
    confidence: int | None,
    not_sure: bool,
    feedback_message_id: str,
) -> ItemResult:
    required_qty = module.required_items[expected_id].quantity if expected_id in module.required_items else 0
    correct_qty = min(selected_quantity, required_qty) if expected_id == selected_id else 0
    is_error = category != "correct"
    return ItemResult(
        expected_instrument_id=expected_id,
        expected_instrument_name=_instrument_name(module, expected_id),
        required_quantity=required_qty,
        selected_instrument_id=selected_id,
        selected_instrument_name=_instrument_name(module, selected_id),
        selected_quantity=selected_quantity,
        correct_quantity=correct_qty,
        error_category=category,
        lookalike_pair_id=lookalike_pair_id,
        item_confidence=confidence,
        item_uncertainty=not_sure,
        is_high_confidence_error=bool(is_error and confidence is not None and confidence >= 4),
        is_low_confidence_correct=bool(category == "correct" and confidence is not None and confidence <= 2),
        feedback_message_id=feedback_message_id,
    )
