from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from ultralytics import YOLO

from trayguard.training.train import PROJECT_ROOT, load_config, train_model


RESULTS_JSON = PROJECT_ROOT / "runs" / "benchmark_results.json"

DEFAULT_TESTS = [
    ("yolo11n", 640, 16),
    ("yolo11s", 640, 16),
    ("yolo11s", 960, 16),
    ("yolo11m", 640, 16),
    ("yolo11m", 960, 8),
    ("yolo11l", 640, 16),
    ("yolo11l", 960, 6),
    ("rtdetr-l", 640, 8),
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard benchmark",
        description="Train and evaluate the standard object detection model variants.",
    )
    parser.add_argument(
        "--tests",
        nargs="*",
        default=None,
        help="Optional variants as model:imgsz:batch, e.g. yolo11s:960:16",
    )
    parser.add_argument(
        "--extra-override",
        action="append",
        default=[],
        help="Extra Hydra override applied to every training run. Can be repeated.",
    )
    return parser.parse_args(argv)


def parse_tests(raw_tests: list[str] | None) -> list[tuple[str, int, int]]:
    if not raw_tests:
        return DEFAULT_TESTS

    tests: list[tuple[str, int, int]] = []
    for raw_test in raw_tests:
        model, imgsz, batch = raw_test.split(":", maxsplit=2)
        tests.append((model, int(imgsz), int(batch)))
    return tests


def build_run_name(model: str, imgsz: int, batch: int) -> str:
    return f"{model}_imgsz{imgsz}_batch{batch}"


def run_train(model: str, imgsz: int, batch: int, extra_overrides: Sequence[str]) -> Path:
    run_name = build_run_name(model, imgsz, batch)
    overrides = [
        f"model={model}",
        f"trainer.imgsz={imgsz}",
        f"trainer.batch={batch}",
        f"trainer.name={run_name}",
        *extra_overrides,
    ]

    if model == "rtdetr-l":
        overrides.append("trainer.lr0=0.003")

    print("\nRunning training overrides:")
    print(" ".join(overrides))
    return train_model(load_config(overrides))


def evaluate_model(save_dir: Path, imgsz: int, data_yaml: str) -> dict[str, float | str]:
    weights = save_dir / "weights" / "best.pt"

    print("\nEvaluating test set:", save_dir.name)
    model = YOLO(str(weights))
    metrics = model.val(data=data_yaml, split="test", imgsz=imgsz, plots=False, verbose=False)

    speed = metrics.speed or {}
    latency = (
        float(speed.get("preprocess", 0))
        + float(speed.get("inference", 0))
        + float(speed.get("postprocess", 0))
    )
    precision = float(metrics.box.mp)

    return {
        "precision": precision,
        "recall": float(metrics.box.mr),
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "latency_ms": latency,
        "fp_rate_approx": 1 - precision,
        "weights": str(weights),
    }


def save_results(results: list[dict[str, object]]) -> None:
    RESULTS_JSON.parent.mkdir(exist_ok=True)
    RESULTS_JSON.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print("\nSaved results to:", RESULTS_JSON)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    tests = parse_tests(args.tests)
    data_yaml = str(load_config(args.extra_override).data.yolo_data)

    results: list[dict[str, object]] = []
    for model, imgsz, batch in tests:
        entry: dict[str, object] = {
            "model": model,
            "imgsz": imgsz,
            "batch": batch,
        }

        try:
            save_dir = run_train(model, imgsz, batch, args.extra_override)
            entry.update(evaluate_model(save_dir, imgsz, data_yaml))
            entry["run_name"] = save_dir.name
            entry["save_dir"] = str(save_dir)
            entry["status"] = "completed"
        except Exception as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)

        results.append(entry)
        save_results(results)

    print("\nFINAL RESULTS")
    for result in results:
        print(result)
