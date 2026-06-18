from __future__ import annotations

import csv
import json

from trayguard.learning.export import export_run
from trayguard.learning.scoring import score_tray


def test_export_run_writes_json_and_csv(tmp_path, tiny_module):
    attempt = score_tray(
        tiny_module,
        "",
        {"forceps": 1, "scissors": 2},
        run_id="run_test",
        learner_id_hash="hash",
    )
    paths = export_run({"run_id": "run_test", "attempts": []}, [attempt], tmp_path)

    assert (
        json.loads((tmp_path / "run.json").read_text(encoding="utf-8"))["run_id"]
        == "run_test"
    )
    with (tmp_path / "attempts.csv").open(newline="", encoding="utf-8") as handle:
        attempt_rows = list(csv.DictReader(handle))
    with (tmp_path / "items.csv").open(newline="", encoding="utf-8") as handle:
        item_rows = list(csv.DictReader(handle))

    assert attempt_rows[0]["run_id"] == "run_test"
    assert item_rows
    assert "feedback_message" in item_rows[0]
    assert paths["items"].endswith("items.csv")


def test_empty_csv_exports_are_empty_files(tmp_path):
    export_run({"run_id": "empty"}, [], tmp_path)

    assert (tmp_path / "attempts.csv").read_text(encoding="utf-8") == ""
    assert (tmp_path / "items.csv").read_text(encoding="utf-8") == ""
