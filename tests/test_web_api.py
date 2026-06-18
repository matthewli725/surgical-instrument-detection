from __future__ import annotations

import json

from fastapi.testclient import TestClient

from trayguard.web.app import create_app


def write_module(tmp_path, payload):
    path = tmp_path / "module.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_web_api_learning_flow(tmp_path, tiny_module_payload):
    module_path = write_module(tmp_path, tiny_module_payload)
    app = create_app(module_path=module_path, runs_dir=tmp_path / "runs")
    client = TestClient(app)

    module_response = client.get("/api/module")
    assert module_response.status_code == 200
    assert module_response.json()["module_id"] == "tiny_module"

    run_response = client.post(
        "/api/runs", json={"learner_id": "demo", "participant_group": "novice"}
    )
    assert run_response.status_code == 200
    run = run_response.json()

    quiz_response = client.post(
        f"/api/runs/{run['run_id']}/quiz",
        json={
            "prompt_id": "name",
            "instrument_id": "forceps",
            "answer": "Forceps",
            "correct": True,
        },
    )
    assert quiz_response.status_code == 200

    score_response = client.post(
        f"/api/runs/{run['run_id']}/score",
        json={
            "mode": "practice",
            "variant_id": "forceps_only",
            "selected_counts": {"forceps": 1},
            "overall_confidence": 3,
        },
    )
    assert score_response.status_code == 200
    assert score_response.json()["attempt"]["accuracy_score"] == 100

    complete_response = client.post(f"/api/runs/{run['run_id']}/complete")
    assert complete_response.status_code == 200

    export_response = client.get(f"/api/runs/{run['run_id']}/export")
    assert export_response.status_code == 200
    assert export_response.json()["run"].endswith("run.json")


def test_web_api_unknown_run_returns_404(tmp_path, tiny_module_payload):
    module_path = write_module(tmp_path, tiny_module_payload)
    client = TestClient(create_app(module_path=module_path, runs_dir=tmp_path / "runs"))

    response = client.post("/api/runs/missing/score", json={"selected_counts": {}})

    assert response.status_code == 404
