from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import cv2

from trayguard.learning.aruco import detect_aruco_cards, generate_marker_png
from trayguard.learning.catalog import load_instrument_catalog
from trayguard.learning.export import export_run
from trayguard.learning.module import load_tray_module
from trayguard.learning.scoring import score_tray


MODULE_PATH = Path("config/tray_modules/basic_general_tray_v1.json")
CATALOG_PATH = Path("config/instrument_catalogs/hospitools_dslr_v1.json")
COMMONS_CATALOG_PATH = Path("config/instrument_catalogs/wikimedia_commons_surgical_instruments_v1.json")
FGVC12_MAJOR_CATALOG_PATH = Path("config/instrument_catalogs/fgvc12_major_tray_v1.json")
DERIVED_MODULE_PATHS = [
    Path("config/tray_modules/minor_skin_closure_tray_v1.json"),
    Path("config/tray_modules/cut_down_tray_v1.json"),
    Path("config/tray_modules/basic_tissue_handling_tray_v1.json"),

]


class LearningPrototypeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_tray_module(MODULE_PATH)

    def test_module_loads_seed_tray(self) -> None:
        self.assertEqual(self.module.module_id, "basic_general_tray_v1")
        self.assertEqual(len(self.module.required_items), 10)
        self.assertEqual(self.module.total_required_units, 15)
        self.assertEqual(len(self.module.marker_cards), 20)
        self.assertEqual(len(self.module.distractor_item_ids), 5)
        self.assertGreaterEqual(len(self.module.lookalike_pairs), 5)
        for instrument in self.module.instruments.values():
            self.assertEqual({"view_a", "view_b"}, {ref["id"] for ref in instrument.image_refs[:2]})
        self.assertEqual(self.module.assessment_variants["basic_general_tray_v1_pre_a"].photo_view, "view_a")
        self.assertEqual(self.module.assessment_variants["basic_general_tray_v1_post_b"].photo_view, "view_b")

    def test_hospitools_catalog_loads(self) -> None:
        catalog = load_instrument_catalog(CATALOG_PATH)
        self.assertEqual(catalog.catalog_id, "hospitools_dslr_v1")
        self.assertGreaterEqual(len(catalog.instruments), 400)
        first = next(iter(catalog.instruments.values()))
        self.assertTrue(first.image_refs)

    def test_wikimedia_commons_catalog_loads(self) -> None:
        catalog = load_instrument_catalog(COMMONS_CATALOG_PATH)
        self.assertEqual(catalog.catalog_id, "wikimedia_commons_surgical_instruments_v1")
        self.assertGreaterEqual(len(catalog.instruments), 5)
        first = next(iter(catalog.instruments.values()))
        self.assertTrue(first.image_refs)

    def test_fgvc12_major_catalog_loads(self) -> None:
        catalog = load_instrument_catalog(FGVC12_MAJOR_CATALOG_PATH)
        self.assertEqual(catalog.catalog_id, "fgvc12_major_tray_v1")
        self.assertGreaterEqual(len(catalog.instruments), 30)
        first = next(iter(catalog.instruments.values()))
        self.assertGreaterEqual(len(first.image_refs), 2)

    def test_derived_modules_load_with_evidence(self) -> None:
        for path in DERIVED_MODULE_PATHS:
            with self.subTest(path=path):
                module = load_tray_module(path)
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(module.required_items), 5)
                self.assertGreaterEqual(module.total_required_units, 6)
                self.assertGreaterEqual(len(module.distractor_item_ids), 3)
                self.assertGreaterEqual(len(module.assessment_variants), 2)
                self.assertGreaterEqual(len(payload.get("evidence_sources", [])), 2)
                for variant in module.assessment_variants.values():
                    self.assertEqual(set(variant.required_item_ids), set(module.required_items))

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
