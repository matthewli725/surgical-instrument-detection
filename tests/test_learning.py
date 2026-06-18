from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2

from trayguard.learning.aruco import detect_aruco_cards, generate_marker_png
from trayguard.learning.module import load_tray_module
from trayguard.learning.scoring import score_tray

MODULE_PATH = Path("config/tray_modules/fgvc12_major_focused_v1.json")


class LearningPrototypeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_tray_module(MODULE_PATH)

    def test_module_loads_focused_tray(self) -> None:
        self.assertEqual(self.module.module_id, "fgvc12_major_focused_v1")
        self.assertEqual(len(self.module.required_items), 12)
        self.assertEqual(self.module.total_required_units, 12)
        self.assertEqual(len(self.module.marker_cards), 16)
        self.assertEqual(len(self.module.distractor_item_ids), 4)
        self.assertGreaterEqual(len(self.module.lookalike_pairs), 5)
        for instrument in self.module.instruments.values():
            self.assertTrue(len(instrument.image_refs) >= 1)
        self.assertEqual(
            self.module.assessment_variants["fgvc12_major_focused_v1_pre_a"].photo_view,
            "view_a",
        )
        self.assertEqual(
            self.module.assessment_variants[
                "fgvc12_major_focused_v1_post_b"
            ].photo_view,
            "view_b",
        )

    def test_correct_tray_scores_full_credit(self) -> None:
        selected = {
            item.instrument_id: item.quantity
            for item in self.module.required_items.values()
        }
        result = score_tray(self.module, "fgvc12_major_focused_v1_pre_a", selected)
        self.assertEqual(result.accuracy_score, 100)
        self.assertEqual(result.error_points, 0)
        self.assertEqual(result.missing_count, 0)

    def test_lookalike_substitution_scores_misidentified(self) -> None:
        selected = {
            item.instrument_id: item.quantity
            for item in self.module.required_items.values()
        }
        pair = self.module.lookalike_pairs[0]
        del selected[pair.expected_id]
        selected[pair.selected_id] = selected.get(pair.selected_id, 0) + 1
        result = score_tray(self.module, "fgvc12_major_focused_v1_pre_a", selected)
        self.assertEqual(result.misidentified_count, 1)
        self.assertEqual(result.error_points, 1)

    def test_generated_apriltag_marker_detects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            marker_path = generate_marker_png(7, Path(tmp) / "marker.png")
            frame = cv2.imread(str(marker_path))
            detections = detect_aruco_cards(frame, {7: "fgvc12_major_clamp_kelly_8in"})
        self.assertEqual(
            [(d.marker_id, d.instrument_id) for d in detections],
            [(7, "fgvc12_major_clamp_kelly_8in")],
        )


if __name__ == "__main__":
    unittest.main()
