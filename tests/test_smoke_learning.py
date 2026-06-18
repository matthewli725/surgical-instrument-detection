from __future__ import annotations

from fastapi.testclient import TestClient

from trayguard.learning.run_store import RunStore
from trayguard.learning.scoring import score_tray
from trayguard.learning.smoke import run_smoke
from trayguard.web.app import create_app


def test_learning_smoke(default_module, tmp_path):
    selected_counts = {
        instrument_id: item.quantity
        for instrument_id, item in default_module.required_items.items()
    }
    attempt = score_tray(default_module, "", selected_counts)
    assert attempt.accuracy_score == 100

    store = RunStore(default_module, tmp_path / "runs")
    run = store.create_run({"learner_id": "smoke"})
    store.add_attempt(run["run_id"], attempt)
    assert (tmp_path / "runs" / run["run_id"] / "run.json").exists()

    app = create_app(runs_dir=tmp_path / "api_runs")
    response = TestClient(app).get("/api/module")
    assert response.status_code == 200


def test_run_smoke(default_module):
    result = run_smoke()

    assert result["module_id"] == default_module.module_id
    assert result["perfect_accuracy"] == 100
    missing_count = result["missing_count"]
    assert isinstance(missing_count, int)
    assert missing_count >= 1
