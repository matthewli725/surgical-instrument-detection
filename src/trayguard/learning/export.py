from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from trayguard.learning.models import AttemptResult


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def export_run(run_payload: dict[str, Any], attempts: list[AttemptResult], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    attempt_rows = [attempt.attempt_row() for attempt in attempts]
    item_rows = []
    for attempt in attempts:
        for item in attempt.item_results:
            row = asdict(item)
            row.update(
                {
                    "run_id": attempt.run_id,
                    "learner_id_hash": attempt.learner_id_hash,
                    "tray_module_id": attempt.tray_module_id,
                    "assessment_variant_id": attempt.assessment_variant_id,
                    "mode": attempt.mode,
                }
            )
            item_rows.append(row)

    run_path = output_dir / "run.json"
    attempts_path = output_dir / "attempts.csv"
    items_path = output_dir / "items.csv"
    run_path.write_text(json.dumps(run_payload, indent=2), encoding="utf-8")
    write_csv(attempts_path, attempt_rows)
    write_csv(items_path, item_rows)
    return {"run": str(run_path), "attempts": str(attempts_path), "items": str(items_path)}
