from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ultralytics import YOLO


DEFAULT_STAGES: tuple[str, ...] = (
    "bright_train_dim_test",
    "dim_train_bright_test",
    "matte_train_reflective_test",
    "reflective_train_matte_test",
    "separated_train_overlay_test",
)


@dataclass(frozen=True)
class SampleRow:
    stage: str
    split: str
    session_id: str
    background: str
    layout: str
    brightness_rank: int
    brightness_stem: str
    image_path: Path
    label_path: Path


@dataclass(frozen=True)
class EvalSpec:
    stage: str
    split: str
    eval_label: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the brightness-order YOLO models and generate experiment tables and plots."
    )
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=Path("data/brightness_yolo"),
        help="Directory containing staged brightness YOLO datasets.",
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
        default=Path("reports/brightness_validation"),
        help="Directory for CSV, JSON, and plot outputs.",
    )
    parser.add_argument(
        "--stage",
        action="append",
        choices=list(DEFAULT_STAGES),
        help="Stage to validate. Pass more than once to restrict the run. Defaults to all stages.",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Validation image size.")
    parser.add_argument("--conf", type=float, default=0.25, help="Prediction confidence threshold.")
    parser.add_argument("--iou", type=float, default=0.50, help="IoU threshold for class-aware matching.")
    parser.add_argument("--plots", action="store_true", help="Also write Ultralytics validation plots per stage.")
    parser.add_argument(
        "--skip-missing",
        action="store_true",
        help="Skip stages with missing weights or datasets instead of stopping.",
    )
    return parser.parse_args(argv)


def metric_value(metrics, key: str) -> float | None:
    value = metrics.results_dict.get(key)
    if value is None:
        return None
    return float(value)


def collect_scalar_metrics(metrics) -> dict[str, float | None]:
    speed = metrics.speed or {}
    box = metrics.box
    results: dict[str, float | None] = {
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
        float(results["preprocess_ms"] or 0.0)
        + float(results["inference_ms"] or 0.0)
        + float(results["postprocess_ms"] or 0.0)
    )
    return results


def discover_samples(stage_dir: Path) -> dict[tuple[str, str], list[SampleRow]]:
    manifest_path = stage_dir / "manifests" / "samples.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing samples manifest: {manifest_path}")

    rows_by_split: dict[tuple[str, str], list[SampleRow]] = defaultdict(list)
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            sample = SampleRow(
                stage=row["stage"],
                split=row["split"],
                session_id=row["session_id"],
                background=row["background"],
                layout=row["layout"],
                brightness_rank=int(row["brightness_rank"]),
                brightness_stem=row["brightness_stem"],
                image_path=stage_dir / row["image"],
                label_path=stage_dir / row["label"],
            )
            rows_by_split[(sample.stage, sample.split)].append(sample)
    return rows_by_split


def yolo_to_xyxy(cx: float, cy: float, w: float, h: float, image_w: int, image_h: int) -> tuple[float, float, float, float]:
    x1 = (cx - w / 2.0) * image_w
    y1 = (cy - h / 2.0) * image_h
    x2 = (cx + w / 2.0) * image_w
    y2 = (cy + h / 2.0) * image_h
    return x1, y1, x2, y2


def load_ground_truth(label_path: Path, image_w: int, image_h: int) -> list[tuple[int, tuple[float, float, float, float]]]:
    boxes: list[tuple[int, tuple[float, float, float, float]]] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        cls = int(parts[0])
        cx, cy, w, h = map(float, parts[1:])
        boxes.append((cls, yolo_to_xyxy(cx, cy, w, h, image_w, image_h)))
    return boxes


def box_iou(box_a: tuple[float, float, float, float], box_b: tuple[float, float, float, float]) -> float:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    if inter_area <= 0.0:
        return 0.0

    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter_area
    if union <= 0.0:
        return 0.0
    return inter_area / union


def greedy_match(
    gt_boxes: list[tuple[int, tuple[float, float, float, float]]],
    pred_boxes: list[tuple[int, tuple[float, float, float, float]]],
    iou_threshold: float,
) -> tuple[int, int, int]:
    candidates: list[tuple[float, int, int]] = []
    for gt_index, (gt_cls, gt_box) in enumerate(gt_boxes):
        for pred_index, (pred_cls, pred_box) in enumerate(pred_boxes):
            if gt_cls != pred_cls:
                continue
            iou = box_iou(gt_box, pred_box)
            if iou >= iou_threshold:
                candidates.append((iou, gt_index, pred_index))

    candidates.sort(reverse=True)
    matched_gt: set[int] = set()
    matched_pred: set[int] = set()
    tp = 0
    for _iou, gt_index, pred_index in candidates:
        if gt_index in matched_gt or pred_index in matched_pred:
            continue
        matched_gt.add(gt_index)
        matched_pred.add(pred_index)
        tp += 1

    fp = len(pred_boxes) - tp
    fn = len(gt_boxes) - tp
    return tp, fp, fn


def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def evaluate_stage(
    spec: EvalSpec,
    stage_dir: Path,
    weights_path: Path,
    samples: list[SampleRow],
    *,
    imgsz: int,
    conf: float,
    iou_threshold: float,
    plots: bool,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    model = YOLO(str(weights_path))
    metrics = model.val(
        data=str(stage_dir / "data.yaml"),
        split=spec.split,
        imgsz=imgsz,
        plots=plots,
        verbose=False,
    )

    scalar_metrics = collect_scalar_metrics(metrics)
    stage_metrics: dict[str, object] = {
        "stage": spec.stage,
        "eval_label": spec.eval_label,
        "split": spec.split,
        "weights": str(weights_path),
        "data_yaml": str(stage_dir / "data.yaml"),
        "images": len(samples),
    }
    stage_metrics.update(scalar_metrics)

    image_paths = [str(sample.image_path) for sample in samples]
    results = model.predict(source=image_paths, stream=True, imgsz=imgsz, conf=conf, verbose=False)
    sample_by_image = {str(sample.image_path): sample for sample in samples}

    per_image_rows: list[dict[str, object]] = []
    for result in results:
        sample = sample_by_image.get(str(Path(result.path)))
        if sample is None:
            raise KeyError(f"Prediction result path did not match a manifest row: {result.path}")

        image_h, image_w = result.orig_shape
        gt_boxes = load_ground_truth(sample.label_path, image_w=image_w, image_h=image_h)
        pred_boxes = [
            (int(box.cls.item()), tuple(float(value) for value in box.xyxy[0].tolist()))
            for box in result.boxes
        ]
        tp, fp, fn = greedy_match(gt_boxes, pred_boxes, iou_threshold=iou_threshold)

        gt_count = len(gt_boxes)
        pred_count = len(pred_boxes)
        count_error = pred_count - gt_count
        row = {
            "stage": spec.stage,
            "eval_label": spec.eval_label,
            "split": spec.split,
            "session_id": sample.session_id,
            "background": sample.background,
            "layout": sample.layout,
            "brightness_rank": sample.brightness_rank,
            "brightness_stem": sample.brightness_stem,
            "image_path": str(sample.image_path),
            "label_path": str(sample.label_path),
            "gt_count": gt_count,
            "pred_count": pred_count,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "image_precision": safe_div(tp, tp + fp),
            "image_recall": safe_div(tp, tp + fn),
            "exact_count_match": int(pred_count == gt_count),
            "count_error": count_error,
            "abs_count_error": abs(count_error),
        }
        per_image_rows.append(row)

    return stage_metrics, per_image_rows


def aggregate_rows(rows: Iterable[dict[str, object]], group_fields: Sequence[str]) -> list[dict[str, object]]:
    groups: dict[tuple[object, ...], dict[str, object]] = {}
    for row in rows:
        key = tuple(row[field] for field in group_fields)
        bucket = groups.setdefault(
            key,
            {field: row[field] for field in group_fields}
            | {
                "images": 0,
                "gt_count": 0,
                "pred_count": 0,
                "tp": 0,
                "fp": 0,
                "fn": 0,
                "exact_count_matches": 0,
                "abs_count_error_sum": 0,
            },
        )
        bucket["images"] = int(bucket["images"]) + 1
        bucket["gt_count"] = int(bucket["gt_count"]) + int(row["gt_count"])
        bucket["pred_count"] = int(bucket["pred_count"]) + int(row["pred_count"])
        bucket["tp"] = int(bucket["tp"]) + int(row["tp"])
        bucket["fp"] = int(bucket["fp"]) + int(row["fp"])
        bucket["fn"] = int(bucket["fn"]) + int(row["fn"])
        bucket["exact_count_matches"] = int(bucket["exact_count_matches"]) + int(row["exact_count_match"])
        bucket["abs_count_error_sum"] = int(bucket["abs_count_error_sum"]) + int(row["abs_count_error"])

    aggregated: list[dict[str, object]] = []
    for key in sorted(groups):
        bucket = groups[key]
        images = int(bucket["images"])
        tp = int(bucket["tp"])
        fp = int(bucket["fp"])
        fn = int(bucket["fn"])
        aggregated.append(
            bucket
            | {
                "precision": safe_div(tp, tp + fp),
                "recall": safe_div(tp, tp + fn),
                "exact_count_rate": safe_div(int(bucket["exact_count_matches"]), images),
                "mean_abs_count_error": safe_div(int(bucket["abs_count_error_sum"]), images),
            }
        )
    return aggregated


def save_stage_overview_plot(stage_metrics: list[dict[str, object]], output_path: Path) -> None:
    test_rows = [row for row in stage_metrics if row["split"] == "test"]
    if not test_rows:
        return

    stage_names = [str(row["stage"]) for row in test_rows]
    recalls = [float(row["recall"]) for row in test_rows]
    map50s = [float(row["map50"]) for row in test_rows]
    map95s = [float(row["map50_95"]) for row in test_rows]

    x = list(range(len(stage_names)))
    width = 0.22
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar([value - width for value in x], recalls, width=width, label="Recall")
    ax.bar(x, map50s, width=width, label="mAP50")
    ax.bar([value + width for value in x], map95s, width=width, label="mAP50-95")
    ax.set_title("Brightness Experiment Stage Overview")
    ax.set_ylabel("Score")
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(x)
    ax.set_xticklabels(stage_names, rotation=20, ha="right")
    ax.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def save_line_plot(
    rows: list[dict[str, object]],
    *,
    output_path: Path,
    title: str,
    metric_field: str,
    series_field: str,
) -> None:
    if not rows:
        return

    by_series: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_series[str(row[series_field])].append(row)

    fig, ax = plt.subplots(figsize=(9, 5))
    for series_name, series_rows in sorted(by_series.items()):
        ordered = sorted(series_rows, key=lambda row: int(row["brightness_rank"]))
        xs = [int(row["brightness_rank"]) for row in ordered]
        ys = [float(row[metric_field]) for row in ordered]
        ax.plot(xs, ys, marker="o", label=series_name)

    ax.set_title(title)
    ax.set_xlabel("Brightness Rank")
    ax.set_ylabel(metric_field.replace("_", " ").title())
    ax.set_xticks(sorted({int(row["brightness_rank"]) for row in rows}))
    if metric_field in {"precision", "recall", "exact_count_rate"}:
        ax.set_ylim(0.0, 1.05)
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def build_eval_specs(stages: Sequence[str]) -> list[EvalSpec]:
    specs = [EvalSpec(stage=stage, split="test", eval_label="test") for stage in stages]
    if "separated_train_overlay_test" in stages:
        specs.append(
            EvalSpec(
                stage="separated_train_overlay_test",
                split="train",
                eval_label="separated_baseline",
            )
        )
    return specs


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    stages = tuple(args.stage or DEFAULT_STAGES)
    eval_specs = build_eval_specs(stages)

    stage_metric_rows: list[dict[str, object]] = []
    per_image_rows: list[dict[str, object]] = []
    processed_specs: list[dict[str, str]] = []

    for spec in eval_specs:
        stage_dir = args.datasets_dir / spec.stage
        weights_path = args.weights_dir / f"{spec.stage}.pt"
        if not stage_dir.exists():
            message = f"Missing dataset stage directory: {stage_dir}"
            if args.skip_missing:
                print(f"Skipping {spec.stage} ({spec.eval_label}): {message}")
                continue
            raise FileNotFoundError(message)
        if not weights_path.exists():
            message = f"Missing weights file: {weights_path}"
            if args.skip_missing:
                print(f"Skipping {spec.stage} ({spec.eval_label}): {message}")
                continue
            raise FileNotFoundError(message)

        samples_by_split = discover_samples(stage_dir)
        samples = samples_by_split.get((spec.stage, spec.split), [])
        if not samples:
            message = f"No manifest rows for {spec.stage} split={spec.split}"
            if args.skip_missing:
                print(f"Skipping {spec.stage} ({spec.eval_label}): {message}")
                continue
            raise ValueError(message)

        print(f"Evaluating {spec.stage} ({spec.eval_label}) on {len(samples)} image(s)")
        stage_metrics, image_rows = evaluate_stage(
            spec,
            stage_dir,
            weights_path,
            samples,
            imgsz=args.imgsz,
            conf=args.conf,
            iou_threshold=args.iou,
            plots=args.plots,
        )
        stage_metric_rows.append(stage_metrics)
        per_image_rows.extend(image_rows)
        processed_specs.append({"stage": spec.stage, "eval_label": spec.eval_label, "split": spec.split})

    if not stage_metric_rows:
        print("No stages were evaluated.")
        return

    grouped_rows = aggregate_rows(
        per_image_rows,
        group_fields=("stage", "eval_label", "split", "background", "layout", "brightness_rank"),
    )

    write_csv(
        args.output_dir / "stage_metrics.csv",
        stage_metric_rows,
        fieldnames=(
            "stage",
            "eval_label",
            "split",
            "weights",
            "data_yaml",
            "images",
            "precision",
            "recall",
            "map50",
            "map50_95",
            "fitness",
            "preprocess_ms",
            "inference_ms",
            "loss_ms",
            "postprocess_ms",
            "latency_ms",
        ),
    )
    write_csv(
        args.output_dir / "image_outcomes.csv",
        per_image_rows,
        fieldnames=(
            "stage",
            "eval_label",
            "split",
            "session_id",
            "background",
            "layout",
            "brightness_rank",
            "brightness_stem",
            "image_path",
            "label_path",
            "gt_count",
            "pred_count",
            "tp",
            "fp",
            "fn",
            "image_precision",
            "image_recall",
            "exact_count_match",
            "count_error",
            "abs_count_error",
        ),
    )
    write_csv(
        args.output_dir / "grouped_metrics.csv",
        grouped_rows,
        fieldnames=(
            "stage",
            "eval_label",
            "split",
            "background",
            "layout",
            "brightness_rank",
            "images",
            "gt_count",
            "pred_count",
            "tp",
            "fp",
            "fn",
            "exact_count_matches",
            "abs_count_error_sum",
            "precision",
            "recall",
            "exact_count_rate",
            "mean_abs_count_error",
        ),
    )
    write_json(
        args.output_dir / "summary.json",
        {
            "datasets_dir": str(args.datasets_dir),
            "weights_dir": str(args.weights_dir),
            "output_dir": str(args.output_dir),
            "imgsz": args.imgsz,
            "conf": args.conf,
            "iou": args.iou,
            "processed": processed_specs,
        },
    )

    plots_dir = args.output_dir / "plots"
    save_stage_overview_plot(stage_metric_rows, plots_dir / "stage_test_overview.png")

    brightness_rows = [
        row for row in grouped_rows
        if row["stage"] in {"bright_train_dim_test", "dim_train_bright_test"}
        and row["eval_label"] == "test"
        and row["layout"] in {"order1", "order2"}
    ]
    save_line_plot(
        brightness_rows,
        output_path=plots_dir / "brightness_test_recall.png",
        title="Brightness Generalization Recall By Brightness Rank",
        metric_field="recall",
        series_field="stage",
    )

    background_rows = [
        row for row in grouped_rows
        if row["stage"] in {"matte_train_reflective_test", "reflective_train_matte_test"}
        and row["eval_label"] == "test"
    ]
    save_line_plot(
        background_rows,
        output_path=plots_dir / "background_transfer_recall.png",
        title="Background Transfer Recall By Brightness Rank",
        metric_field="recall",
        series_field="stage",
    )

    overlay_rows = [
        row for row in grouped_rows
        if row["stage"] == "separated_train_overlay_test"
        and row["eval_label"] in {"test", "separated_baseline"}
    ]
    save_line_plot(
        overlay_rows,
        output_path=plots_dir / "overlay_gap_exact_count.png",
        title="Separated Vs Overlay Exact Count Rate",
        metric_field="exact_count_rate",
        series_field="eval_label",
    )

    print(f"Wrote validation artifacts to: {args.output_dir}")


if __name__ == "__main__":
    main()
