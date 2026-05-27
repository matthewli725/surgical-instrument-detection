from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import cv2

from trayguard.learning.aruco import detect_aruco_cards, generate_marker_png
from trayguard.learning.export import export_run
from trayguard.learning.module import load_tray_module
from trayguard.learning.scoring import score_tray


MODULE_PATH = Path("config/tray_modules/basic_general_tray_v1.json")


class LearningPrototypeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_tray_module(MODULE_PATH)

    def test_module_loads_seed_tray(self) -> None:
        self.assertEqual(self.module.module_id, "basic_general_tray_v1")
        self.assertEqual(len(self.module.required_items), 10)
        self.assertEqual(self.module.total_required_units, 15)
        self.assertEqual(len(self.module.marker_cards), 20)

    def test_correct_tray_scores_full_credit(self) -> None:
        selected = {key: item.quantity for key, item in self.module.required_items.items()}
        result = score_tray(self.module, "basic_general_tray_v1_pre_a", selected)
        self.assertEqual(result.accuracy_score, 100)
        self.assertEqual(result.error_points, 0)
        self.assertEqual(result.missing_count, 0)

    def test_lookalike_substitution_scores_misidentified(self) -> None:
        selected = {key: item.quantity for key, item in self.module.required_items.items()}
        selected["kelly_forceps_curved_55"] = 1
        selected["crile_hemostat_curved_55"] = 1
        result = score_tray(self.module, "basic_general_tray_v1_pre_a", selected)
        self.assertEqual(result.misidentified_count, 1)
        self.assertEqual(result.error_points, 1)

    def test_export_writes_attempt_and_item_files(self) -> None:
        result = score_tray(self.module, "basic_general_tray_v1_pre_a", {"scalpel_handle_3": 1}, run_id="run_test")
        with tempfile.TemporaryDirectory() as tmp:
            paths = export_run({"run_id": "run_test"}, [result], Path(tmp))
            for path in paths.values():
                self.assertTrue(Path(path).exists())
            self.assertIn("accuracy_score", Path(paths["attempts"]).read_text(encoding="utf-8"))
            self.assertIn("error_category", Path(paths["items"]).read_text(encoding="utf-8"))
            self.assertEqual(json.loads(Path(paths["run"]).read_text(encoding="utf-8"))["run_id"], "run_test")

    def test_generated_aruco_marker_detects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            marker_path = generate_marker_png(7, Path(tmp) / "marker.png")
            frame = cv2.imread(str(marker_path))
            detections = detect_aruco_cards(frame, {7: "mosquito_hemostat_curved_5"})
        self.assertEqual([(d.marker_id, d.instrument_id) for d in detections], [(7, "mosquito_hemostat_curved_5")])


if __name__ == "__main__":
    unittest.main()
