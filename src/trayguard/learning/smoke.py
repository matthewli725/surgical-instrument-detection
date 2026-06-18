from __future__ import annotations

import argparse
import tempfile
from pathlib import Path
from typing import Sequence

from trayguard.learning.module import load_tray_module
from trayguard.learning.run_store import RunStore
from trayguard.learning.scoring import score_tray
from trayguard.web.app import DEFAULT_MODULE, create_app


def run_smoke(module_path: Path = DEFAULT_MODULE) -> dict[str, object]:
    module = load_tray_module(module_path)
    selected_counts = {
        instrument_id: item.quantity
        for instrument_id, item in module.required_items.items()
    }
    perfect_attempt = score_tray(module, "", selected_counts)
    if perfect_attempt.accuracy_score != 100:
        raise RuntimeError(
            f"Perfect tray smoke score was {perfect_attempt.accuracy_score}, expected 100."
        )

    first_required_id = next(iter(module.required_items))
    missing_counts = dict(selected_counts)
    missing_counts.pop(first_required_id)
    missing_attempt = score_tray(module, "", missing_counts)
    if missing_attempt.missing_count < 1:
        raise RuntimeError("Missing-item smoke score did not record a missing item.")

    with tempfile.TemporaryDirectory(prefix="trayguard_smoke_") as tmp:
        runs_dir = Path(tmp) / "runs"
        store = RunStore(module, runs_dir)
        run = store.create_run({"learner_id": "smoke"})
        store.add_attempt(run["run_id"], perfect_attempt)
        create_app(module_path=module_path, runs_dir=runs_dir)
        run_path = runs_dir / run["run_id"] / "run.json"
        if not run_path.exists():
            raise RuntimeError(f"Smoke export was not written: {run_path}")

    return {
        "module_id": module.module_id,
        "required_units": module.total_required_units,
        "perfect_accuracy": perfect_attempt.accuracy_score,
        "missing_count": missing_attempt.missing_count,
    }


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="trayguard smoke-learning",
        description="Run a fast smoke test for the TrayGuard learning workflow.",
    )
    parser.add_argument(
        "--module", type=Path, default=DEFAULT_MODULE, help="Tray module JSON file."
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    result = run_smoke(args.module)
    print("TrayGuard learning smoke test passed.")
    print(f"  module_id: {result['module_id']}")
    print(f"  required_units: {result['required_units']}")
    print(f"  perfect_accuracy: {result['perfect_accuracy']}%")
    print(f"  missing_count_check: {result['missing_count']}")
