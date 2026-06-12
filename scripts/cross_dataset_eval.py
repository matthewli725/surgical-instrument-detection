from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

import yaml
from ultralytics import YOLO


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-dataset evaluation: evaluate a model trained on dataset A"
        " against the test split of dataset B. Useful when class schemas differ."
    )
    parser.add_argument("--model", type=Path, required=True, help="Path to trained model weights (best.pt).")
    parser.add_argument("--data", type=Path, required=True, help="Path to target dataset's data.yaml.")
    parser.add_argument("--split", default="test", choices=("train", "val", "test"))
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--max-images", type=int, default=None, help="Limit to N images for quick checks.")
    parser.add_argument("--json-out", type=Path, default=None, help="Save full detection report as JSON.")
    parser.add_argument("--class-map", type=Path, default=None, help="JSON file mapping source->target class IDs.")
    return parser.parse_args(argv)


def load_class_map(path: Path | None) -> dict[str, str] | None:
    if path is None:
        return None
    return json.loads(path.read_text())


def load_names(data_yaml: Path) -> dict[int, str]:
    raw = yaml.safe_load(data_yaml.read_text())
    names = raw.get("names", {})
    return {int(k): v for k, v in names.items()}


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    class_map = load_class_map(args.class_map)

    target_names = load_names(args.data)
    print(f"Target dataset classes ({args.data}):")
    for cid, cname in sorted(target_names.items()):
        print(f"  {cid}: {cname}")

    print(f"\nLoading model: {args.model}")
    model = YOLO(str(args.model))

    source_names = model.names
    print(f"Source model classes:")
    for cid, cname in sorted(source_names.items()):
        mapped = f" -> {class_map.get(str(cid), '?')}" if class_map else ""
        print(f"  {cid}: {cname}{mapped}")

    print(f"\nRunning predictions on {args.data} ({args.split} split)...")
    metrics = model.val(
        data=str(args.data),
        split=args.split,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        plots=True,
        verbose=False,
    )

    speed = metrics.speed or {}
    latency = (
        float(speed.get("preprocess", 0))
        + float(speed.get("inference", 0))
        + float(speed.get("postprocess", 0))
    )

    standard_metrics = {
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "latency_ms": latency,
    }

    print(f"\n=== Cross-Dataset Metrics ===")
    print(f"  mAP50:    {standard_metrics['map50']:.4f}")
    print(f"  mAP50-95: {standard_metrics['map50_95']:.4f}")
    print(f"  P:        {standard_metrics['precision']:.4f}")
    print(f"  R:        {standard_metrics['recall']:.4f}")
    print(f"  latency:  {standard_metrics['latency_ms']:.1f}ms")

    ap = metrics.box.ap
    ap_class_index = metrics.box.ap_class_index
    if ap is not None and ap_class_index is not None:
        print(f"\n  Per-class AP on target dataset:")
        for idx, class_id in enumerate(ap_class_index):
            class_name = source_names.get(int(class_id), f"class_{int(class_id)}")
            if class_map:
                mapped_name = class_map.get(str(class_id), "?")
                label = f"{class_name} -> {mapped_name}"
            else:
                label = class_name
            ap50 = float(ap[idx][0]) if len(ap[idx]) > 0 else None
            ap50_95 = float(ap[idx][1]) if len(ap[idx]) > 1 else None
            ap50_str = f"{ap50:.4f}" if ap50 is not None else "N/A"
            ap50_95_str = f"{ap50_95:.4f}" if ap50_95 is not None else "N/A"
            print(f"    {label:<30} AP50={ap50_str}  AP50-95={ap50_95_str}")

    report = {
        "model": str(args.model),
        "target_data": str(args.data),
        "target_split": args.split,
        "target_classes": target_names,
        "source_classes": source_names,
        "class_map": class_map,
        **standard_metrics,
    }

    if ap is not None and ap_class_index is not None:
        per_class = []
        for idx, class_id in enumerate(ap_class_index):
            entry = {
                "class_id": int(class_id),
                "class_name": source_names.get(int(class_id), f"class_{int(class_id)}"),
                "ap50": float(ap[idx][0]) if len(ap[idx]) > 0 else None,
                "ap50_95": float(ap[idx][1]) if len(ap[idx]) > 1 else None,
            }
            if class_map:
                entry["mapped_target"] = class_map.get(str(class_id))
            per_class.append(entry)
        report["per_class"] = per_class

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n")
        print(f"\nWrote report: {args.json_out}")


if __name__ == "__main__":
    main()
