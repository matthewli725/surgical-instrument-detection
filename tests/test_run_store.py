from __future__ import annotations

import json

from trayguard.learning.run_store import RunStore, hash_learner_id
from trayguard.learning.scoring import score_tray


def test_hash_learner_id_is_normalized_and_short():
    assert hash_learner_id(" LearnerA ") == hash_learner_id("learnera")
    assert len(hash_learner_id("learnera")) == 16


def test_run_store_persists_without_raw_learner_id(tmp_path, tiny_module):
    store = RunStore(tiny_module, tmp_path)
    run = store.create_run({"learner_id": "Secret Name", "participant_group": "novice"})

    run_path = tmp_path / run["run_id"] / "run.json"
    payload = json.loads(run_path.read_text(encoding="utf-8"))

    assert payload["learner_id_hash"] == hash_learner_id("Secret Name")
    assert "Secret Name" not in run_path.read_text(encoding="utf-8")


def test_run_store_persists_quiz_attempt_and_completion(tmp_path, tiny_module):
    store = RunStore(tiny_module, tmp_path)
    run = store.create_run({"learner_id": "demo"})

    quiz = store.add_quiz_event(
        run["run_id"],
        {
            "prompt_id": "name",
            "instrument_id": "forceps",
            "answer": "Forceps",
            "correct": True,
        },
    )
    assert quiz["correct"] is True

    attempt = score_tray(
        tiny_module,
        "",
        {"forceps": 1, "scissors": 2},
        run_id=run["run_id"],
        learner_id_hash=run["learner_id_hash"],
    )
    paths = store.add_attempt(run["run_id"], attempt)
    store.complete_run(run["run_id"])

    assert (tmp_path / run["run_id"] / "attempts.csv").exists()
    assert (tmp_path / run["run_id"] / "items.csv").exists()
    assert paths["run"].endswith("run.json")
    payload = json.loads(
        (tmp_path / run["run_id"] / "run.json").read_text(encoding="utf-8")
    )
    assert payload["completed_full_flow"] is True
    assert payload["quiz_events"][0]["answer"] == "Forceps"
