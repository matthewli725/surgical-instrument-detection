from __future__ import annotations

import hashlib
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from trayguard.learning.export import export_run
from trayguard.learning.models import AttemptResult, TrayModule


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_learner_id(value: str) -> str:
    normalized = value.strip().lower().encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()[:16]


class RunStore:
    def __init__(self, module: TrayModule, root: Path):
        self.module = module
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.runs: dict[str, dict[str, Any]] = {}
        self.attempts: dict[str, list[AttemptResult]] = {}

    def create_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        run = {
            "run_id": run_id,
            "learner_id_hash": hash_learner_id(payload.get("learner_id", "")),
            "participant_group": payload.get("participant_group", "novice"),
            "prior_experience_level": payload.get("prior_experience_level", "none"),
            "help_requests_count": int(payload.get("help_requests_count", 0)),
            "blocking_help_requests": int(payload.get("blocking_help_requests", 0)),
            "tray_module_id": self.module.module_id,
            "tray_module_version": self.module.version,
            "started_at": utc_now(),
            "completed_at": "",
            "completed_full_flow": False,
            "quiz_events": [],
        }
        self.runs[run_id] = run
        self.attempts[run_id] = []
        self._persist(run_id)
        return run

    def get_run(self, run_id: str) -> dict[str, Any]:
        if run_id not in self.runs:
            raise KeyError(run_id)
        return self.runs[run_id]

    def add_quiz_event(self, run_id: str, event: dict[str, Any]) -> dict[str, Any]:
        run = self.get_run(run_id)
        row = {
            "recorded_at": utc_now(),
            "prompt_id": event.get("prompt_id", ""),
            "instrument_id": event.get("instrument_id", ""),
            "answer": event.get("answer", ""),
            "correct": bool(event.get("correct", False)),
            "confidence": event.get("confidence"),
            "not_sure": bool(event.get("not_sure", False)),
        }
        run["quiz_events"].append(row)
        self._persist(run_id)
        return row

    def add_attempt(self, run_id: str, attempt: AttemptResult) -> dict[str, str]:
        self.get_run(run_id)
        self.attempts[run_id].append(attempt)
        return self._persist(run_id)

    def complete_run(self, run_id: str) -> dict[str, str]:
        run = self.get_run(run_id)
        run["completed_full_flow"] = True
        run["completed_at"] = utc_now()
        return self._persist(run_id)

    def _persist(self, run_id: str) -> dict[str, str]:
        run = self.get_run(run_id)
        payload = dict(run)
        payload["attempts"] = [attempt.attempt_row() for attempt in self.attempts.get(run_id, [])]
        payload["item_results"] = [asdict(item) for attempt in self.attempts.get(run_id, []) for item in attempt.item_results]
        return export_run(payload, self.attempts.get(run_id, []), self.root / run_id)
