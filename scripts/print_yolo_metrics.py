from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from ultralytics import YOLO


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run YOLO validation and print scalar metrics.")
    parser.add_argument("--model", type=Path, required=True, help="Path to YOLO weights, usually best.pt.")
    parser.add_argument("--data", type=Path, required=True, help="Path to dataset data.yaml.")
    parser.add_argument("--split", default="test", choices=("train", "val", "test"), help="Dataset split to evaluate.")
    parser.add_argument("--imgsz", type=int, default=640, help="Validation image size.")
    parser.add_argument("--plots", action="store_true", help="Also write Ultralytics plots/curves.")
    parser.add_argument("--json-out", type=Path, default=None, help="Optional path to write metrics as JSON.")
    return parser.parse_args(argv)


def metric_value(metrics, key: str) -> float | None:
    value = metrics.results_dict.get(key)
    if value is None:
        return None
    return float(value)


def collect_metrics(metrics) -> dict[str, object]:
    speed = metrics.speed or {}
    box = metrics.box
    results = {
        "precision": float(box.mp),
        "recall": float(box.mr),
        "map50": float(box.map50),
        "map50_95": float(box.map),
        "fitness": metric_value(metrics, "fitness"),
        "preprocess_ms": float(speed.get("preprocess", 0.0)),
        "inference_ms": float(speed.get("inference", 0.0)),
        "loss_ms": float(speed.get("loss", 0.0)),
        "postprocess_ms": float(speed.get("postprocess", 0.0)),
    }
    results["latency_ms"] = (
        results["preprocess_ms"]
        + results["inference_ms"]
        + results["postprocess_ms"]
    )
    return results


def print_metrics(results: dict[str, object]) -> None:
    print("\n=== YOLO Metrics ===")
    print(f"{'precision':<16} {results['precision']:.4f}")
    print(f"{'recall':<16} {results['recall']:.4f}")
    print(f"{'mAP50':<16} {results['map50']:.4f}")
    print(f"{'mAP50-95':<16} {results['map50_95']:.4f}")
    if results["fitness"] is not None:
        print(f"{'fitness':<16} {results['fitness']:.4f}")
    print(f"{'latency ms/img':<16} {results['latency_ms']:.2f}")
    print()


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    model = YOLO(str(args.model))
    metrics = model.val(
        data=str(args.data),
        split=args.split,
        imgsz=args.imgsz,
        plots=args.plots,
        verbose=False,
    )

    results = collect_metrics(metrics)
    results.update(
        {
            "model": str(args.model),
            "data": str(args.data),
            "split": args.split,
            "imgsz": args.imgsz,
        }
    )

    print_metrics(results)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote JSON metrics to: {args.json_out}")


if __name__ == "__main__":
    main()
