from __future__ import annotations

import argparse
import csv
import json
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from ultralytics import YOLO


CLASS_NAMES = {
    0: "scissor1",
    1: "scissor2",
    2: "scissor3",
    3: "scissor4",
    4: "forcep",
    5: "scalpel",
}

LIGHTING_STAGES: tuple[str, ...] = (
    "matte_train_reflective_test",
    "reflective_train_matte_test",
)

SHAPE_STAGES: tuple[str, ...] = (
    "shape_similarity_real_proxy",
)

ALL_STAGES: tuple[str, ...] = LIGHTING_STAGES + SHAPE_STAGES


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate surgical-kit proxy models: per-class metrics, confusion matrices, and stage-level reporting."
    )
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=Path("data/cv/surgical_kit_proxy"),
    )
    parser.add_argument(
        "--weights-dir",
        type=Path,
        default=Path("weights"),
        help="Directory containing stage-matched .pt files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports/surgical_kit_validation"),
    )
    parser.add_argument(
        "--stage",
        action="append",
        choices=list(ALL_STAGES),
        help="Stage to validate. Defaults to all.",
    )
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument(
        "--skip-missing",
        action="store_true",
        help="Skip stages with missing weights or datasets instead of stopping.",
    )
    return parser.parse_args(argv)


def stage_data_yaml(stage: str, datasets_dir: Path) -> Path:
    if stage in SHAPE_STAGES:
        return datasets_dir / stage / "data.yaml"
    return datasets_dir / "lighting" / stage / "data.yaml"


def stage_weight(stage: str, weights_dir: Path) -> Path:
    return weights_dir / f"surgical_kit_{stage}.pt"


def collect_per_class_metrics(metrics) -> list[dict]:
    ap = metrics.box.ap
    ap_class_index = metrics.box.ap_class_index
    mp = metrics.box.mp
    mr = metrics.box.mr
    map50 = metrics.box.map50
    map50_95 = metrics.box.map

    per_class = []
    for idx, class_id in enumerate(ap_class_index):
        class_name = CLASS_NAMES.get(int(class_id), f"class_{int(class_id)}")
        ap_val = ap[idx] if ap is not None and idx < len(ap) else None
        if ap_val is not None and hasattr(ap_val, "__len__"):
            ap50 = float(ap_val[0]) if len(ap_val) > 0 else None
            ap50_95 = float(ap_val[-1]) if len(ap_val) > 1 else None
        else:
            ap50 = float(ap_val) if ap_val is not None else None
            ap50_95 = float(ap_val) if ap_val is not None else None
        per_class.append({
            "class_id": int(class_id),
            "class_name": class_name,
            "ap50": ap50,
            "ap50_95": ap50_95,
        })

    return {
        "mean_precision": float(mp),
        "mean_recall": float(mr),
        "map50": float(map50),
        "map50_95": float(map50_95),
        "per_class": per_class,
    }


def validate_stage(
    stage: str,
    datasets_dir: Path,
    weights_dir: Path,
    output_dir: Path,
    *,
    imgsz: int,
    conf: float,
    iou: float,
    skip_missing: bool,
) -> dict | None:
    weight_path = stage_weight(stage, weights_dir)
    data_yaml = stage_data_yaml(stage, datasets_dir)

    if not weight_path.exists():
        msg = f"Missing weights: {weight_path}"
        if skip_missing:
            print(f"  SKIP: {msg}")
            return None
        raise FileNotFoundError(msg)

    if not data_yaml.exists():
        msg = f"Missing data.yaml: {data_yaml}"
        if skip_missing:
            print(f"  SKIP: {msg}")
            return None
        raise FileNotFoundError(msg)

    print(f"\n  Validating: {stage}")
    print(f"    model: {weight_path}")
    print(f"    data:  {data_yaml}")

    model = YOLO(str(weight_path))

    with tempfile.TemporaryDirectory() as tmp_dir:
        metrics = model.val(
            data=str(data_yaml),
            split="test",
            imgsz=imgsz,
            conf=conf,
            iou=iou,
            plots=True,
            save_dir=tmp_dir,
            verbose=False,
        )

        result = collect_per_class_metrics(metrics)
        result["stage"] = stage
        result["weights"] = str(weight_path)
        result["data"] = str(data_yaml)

        speed = metrics.speed or {}
        result["latency_ms"] = (
            float(speed.get("preprocess", 0))
            + float(speed.get("inference", 0))
            + float(speed.get("postprocess", 0))
        )

        print(f"    mAP50:    {result['map50']:.4f}")
        print(f"    mAP50-95: {result['map50_95']:.4f}")
        print(f"    P:        {result['mean_precision']:.4f}")
        print(f"    R:        {result['mean_recall']:.4f}")
        print(f"    latency:  {result['latency_ms']:.1f}ms")
        print("    Per class:")
        for pc in result["per_class"]:
            ap50 = f"{pc['ap50']:.4f}" if pc['ap50'] is not None else "N/A"
            ap50_95 = f"{pc['ap50_95']:.4f}" if pc['ap50_95'] is not None else "N/A"
            print(f"      {pc['class_name']:<12} AP50={ap50}  AP50-95={ap50_95}")

        stage_out = output_dir / stage
        stage_out.mkdir(parents=True, exist_ok=True)

        metrics_path = stage_out / "metrics.json"
        metrics_path.write_text(json.dumps(result, indent=2) + "\n")
        print(f"    Wrote: {metrics_path}")

        per_class_csv = stage_out / "per_class_metrics.csv"
        with open(per_class_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["class_id", "class_name", "ap50", "ap50_95"])
            writer.writeheader()
            writer.writerows(result["per_class"])
        print(f"    Wrote: {per_class_csv}")

        return result


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    stages = tuple(args.stage or ALL_STAGES)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    for stage in stages:
        result = validate_stage(
            stage,
            args.datasets_dir,
            args.weights_dir,
            args.output_dir,
            imgsz=args.imgsz,
            conf=args.conf,
            iou=args.iou,
            skip_missing=args.skip_missing,
        )
        if result is not None:
            results.append(result)

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nWrote summary: {summary_path}")

    summary_csv = args.output_dir / "stage_metrics.csv"
    with open(summary_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["stage", "map50", "map50_95", "mean_precision", "mean_recall"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "stage": r["stage"],
                "map50": r["map50"],
                "map50_95": r["map50_95"],
                "mean_precision": r["mean_precision"],
                "mean_recall": r["mean_recall"],
            })
    print(f"Wrote summary CSV: {summary_csv}")


if __name__ == "__main__":
    main()
