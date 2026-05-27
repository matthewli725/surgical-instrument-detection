from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from trayguard.learning.aruco import decode_data_url, detect_aruco_cards
from trayguard.learning.module import load_tray_module
from trayguard.learning.run_store import RunStore, utc_now
from trayguard.learning.scoring import score_tray


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODULE = PROJECT_ROOT / "config" / "tray_modules" / "basic_general_tray_v1.json"
DEFAULT_RUNS_DIR = PROJECT_ROOT / "data" / "training_runs"
STATIC_DIR = Path(__file__).with_name("static")


def create_app(module_path: str | Path = DEFAULT_MODULE, runs_dir: str | Path = DEFAULT_RUNS_DIR) -> FastAPI:
    module = load_tray_module(module_path)
    store = RunStore(module, Path(runs_dir))
    app = FastAPI(title="TrayGuard Training Prototype")
    app.state.module = module
    app.state.store = store

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/api/module")
    def get_module():
        return module.to_public_dict()

    @app.post("/api/runs")
    def create_run(payload: dict[str, Any]):
        return store.create_run(payload)

    @app.post("/api/runs/{run_id}/quiz")
    def record_quiz(run_id: str, payload: dict[str, Any]):
        try:
            return store.add_quiz_event(run_id, payload)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Unknown run_id") from exc

    @app.post("/api/runs/{run_id}/score")
    def score_run(run_id: str, payload: dict[str, Any]):
        try:
            run = store.get_run(run_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Unknown run_id") from exc

        started_at = payload.get("started_at") or utc_now()
        completed_at = utc_now()
        selected_counts = {key: int(value) for key, value in payload.get("selected_counts", {}).items()}
        attempt = score_tray(
            module,
            payload.get("variant_id", ""),
            selected_counts,
            run_id=run_id,
            learner_id_hash=run["learner_id_hash"],
            participant_group=run["participant_group"],
            prior_experience_level=run["prior_experience_level"],
            mode=payload.get("mode", "practice"),
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=float(payload.get("duration_seconds", 0)),
            overall_confidence=payload.get("overall_confidence"),
            not_sure=bool(payload.get("not_sure", False)),
            help_requests_count=int(run.get("help_requests_count", 0)),
            blocking_help_requests=int(run.get("blocking_help_requests", 0)),
            completed_full_flow=bool(run.get("completed_full_flow", False)),
        )
        paths = store.add_attempt(run_id, attempt)
        return {"attempt": attempt.attempt_row(), "items": [asdict(item) for item in attempt.item_results], "export_paths": paths}

    @app.post("/api/detect-cards")
    def detect_cards(payload: dict[str, Any]):
        try:
            frame = decode_data_url(payload["image"])
        except (KeyError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        detections = detect_aruco_cards(frame, module.marker_map)
        counts = Counter(detection.instrument_id for detection in detections if detection.instrument_id)
        return {"detections": [asdict(detection) for detection in detections], "selected_counts": dict(counts)}

    @app.post("/api/runs/{run_id}/complete")
    def complete_run(run_id: str):
        try:
            return store.complete_run(run_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Unknown run_id") from exc

    @app.get("/api/runs/{run_id}/export")
    def get_export(run_id: str):
        try:
            store.get_run(run_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Unknown run_id") from exc
        run_dir = Path(store.root) / run_id
        return {"run": str(run_dir / "run.json"), "attempts": str(run_dir / "attempts.csv"), "items": str(run_dir / "items.csv")}

    return app
