from __future__ import annotations

from trayguard.learning.scoring import score_tray


def categories(result):
    return {item.error_category for item in result.item_results}


def test_perfect_tray_scores_100(tiny_module):
    result = score_tray(tiny_module, "", {"forceps": 1, "scissors": 2})

    assert result.accuracy_score == 100
    assert result.required_recall == 100
    assert result.error_points == 0
    assert categories(result) == {"correct"}


def test_missing_required_item(tiny_module):
    result = score_tray(tiny_module, "", {"scissors": 2}, overall_confidence=4)

    assert result.accuracy_score == 66.67
    assert result.missing_count == 1
    assert result.high_confidence_error_count >= 1
    missing = next(
        item for item in result.item_results if item.error_category == "missing"
    )
    assert missing.feedback_message == "Required instrument was not selected."


def test_extra_item(tiny_module):
    result = score_tray(tiny_module, "", {"forceps": 1, "scissors": 2, "clamp": 1})

    assert result.extra_count == 1
    assert "extra" in categories(result)


def test_lookalike_substitution_includes_feedback(tiny_module):
    result = score_tray(tiny_module, "", {"clamp": 1, "scissors": 2})

    assert result.misidentified_count == 1
    item = next(
        item for item in result.item_results if item.error_category == "misidentified"
    )
    assert item.lookalike_pair_id == "lookalike_forceps_clamp"
    assert (
        item.feedback_message == "Forceps have two spring arms; clamps have a ratchet."
    )


def test_wrong_count(tiny_module):
    result = score_tray(tiny_module, "", {"forceps": 1, "scissors": 1})

    assert result.wrong_count_error_count == 1
    assert "wrong_count" in categories(result)


def test_low_confidence_correct_count(tiny_module):
    result = score_tray(
        tiny_module, "", {"forceps": 1, "scissors": 2}, overall_confidence=1
    )

    assert result.low_confidence_correct_count == 2


def test_variant_scoring_uses_required_subset(tiny_module):
    result = score_tray(tiny_module, "forceps_only", {"forceps": 1})

    assert result.total_required_units == 1
    assert result.accuracy_score == 100
    assert result.required_recall == 100
    assert result.selected_units == 1
