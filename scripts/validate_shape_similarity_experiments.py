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


DEFAULT_EVALS: tuple[str, ...] = (
    "synthetic_seen_condition",
    "synthetic_heldout_condition",
    "real_small_from_scratch",
    "synthetic_pretrain_plus_real_small",
)


@dataclass(frozen=True)
class EvalSpec:
    run_name: str
    dataset_stage: str
    split: str
    stage_group: str


@dataclass(frozen=True)
class SampleRow:
    stage: str
    stage_group: str
    split: str
    sample_id: str
    source_type: str
    open_set_role: str
    class_name: str
    pair_family: str
    scene_id: str
    condition_id: str
    mesh_id: str
    mesh_split: str
    physical_instance_id: str
    session_id: str
    image_path: Path
    label_path: Path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate shape-similarity YOLO models and report pairwise confusion plus synthetic-to-real transfer outcomes."
    )
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=Path("data/shape_similarity_yolo"),
        help="Directory containing exported shape-similarity YOLO stages.",
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
        default=Path("reports/shape_similarity_validation"),
        help="Directory for CSV, JSON, and plot outputs.",
    )
    parser.add_argument(
        "--eval",
        action="append",
        choices=list(DEFAULT_EVALS),
        help="Evaluation branch to run. Pass more than once to restrict the run. Defaults to all.",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Validation image size.")
    parser.add_argument("--conf", type=float, default=0.25, help="Prediction confidence threshold.")
    parser.add_argument("--iou", type=float, default=0.50, help="IoU threshold for box matching.")
    parser.add_argument(
        "--high-conf-threshold",
        type=float,
        default=0.60,
        help="Confidence threshold used for risky wrong-pair and open-set summaries.",
    )
    parser.add_argument("--plots", action="store_true", help="Also write Ultralytics validation plots per stage.")
    parser.add_argument(
        "--skip-missing",
        action="store_true",
        help="Skip missing datasets or weights instead of stopping.",
    )
    return parser.parse_args(argv)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def build_eval_specs(eval_names: Sequence[str]) -> list[EvalSpec]:
    mapping = {
        "synthetic_seen_condition": EvalSpec(
            run_name="synthetic_seen_condition",
            dataset_stage="synthetic_seen_condition",
            split="test",
            stage_group="synthetic_seen_condition",
        ),
        "synthetic_heldout_condition": EvalSpec(
            run_name="synthetic_heldout_condition",
            dataset_stage="synthetic_heldout_condition",
            split="test",
            stage_group="synthetic_heldout_condition",
        ),
        "real_small_from_scratch": EvalSpec(
            run_name="real_small_from_scratch",
            dataset_stage="synthetic_to_real_transfer_real_small",
            split="test",
            stage_group="synthetic_to_real_transfer",
        ),
        "synthetic_pretrain_plus_real_small": EvalSpec(
            run_name="synthetic_pretrain_plus_real_small",
            dataset_stage="synthetic_to_real_transfer_real_small",
            split="test",
            stage_group="synthetic_to_real_transfer",
        ),
    }
    return [mapping[name] for name in eval_names]


def load_names(stage_dir: Path) -> list[str]:
    data_yaml = stage_dir / "data.yaml"
    names: list[str] = []
    in_names_block = False
    for raw_line in data_yaml.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.strip() == "names:":
            in_names_block = True
            continue
        if in_names_block:
            if not line.startswith("  "):
                break
            _index, name = line.split(":", maxsplit=1)
            names.append(name.strip())
    if not names:
        raise ValueError(f"Could not parse class names from {data_yaml}")
    return names


def discover_samples(stage_dir: Path) -> dict[str, list[SampleRow]]:
    manifest_path = stage_dir / "manifests" / "samples.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing samples manifest: {manifest_path}")

    rows_by_split: dict[str, list[SampleRow]] = defaultdict(list)
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            sample = SampleRow(
                stage=row["stage"],
                stage_group=row["stage_group"],
                split=row["split"],
                sample_id=row["sample_id"],
                source_type=row["source_type"],
                open_set_role=row["open_set_role"],
                class_name=row["class_name"],
                pair_family=row["pair_family"],
                scene_id=row["scene_id"],
                condition_id=row["condition_id"],
                mesh_id=row["mesh_id"],
                mesh_split=row["mesh_split"],
                physical_instance_id=row["physical_instance_id"],
                session_id=row["session_id"],
                image_path=stage_dir / row["image"],
                label_path=stage_dir / row["label"],
            )
            rows_by_split[sample.split].append(sample)
    return rows_by_split


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


def yolo_to_xyxy(
    cx: float,
    cy: float,
    w: float,
    h: float,
    image_w: int,
    image_h: int,
) -> tuple[float, float, float, float]:
    x1 = (cx - w / 2.0) * image_w
    y1 = (cy - h / 2.0) * image_h
    x2 = (cx + w / 2.0) * image_w
    y2 = (cy + h / 2.0) * image_h
    return x1, y1, x2, y2


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


def load_ground_truth(label_path: Path, image_w: int, image_h: int) -> list[tuple[int, tuple[float, float, float, float]]]:
    if not label_path.exists():
        return []
    boxes: list[tuple[int, tuple[float, float, float, float]]] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        cls = int(parts[0])
        cx, cy, w, h = map(float, parts[1:])
        boxes.append((cls, yolo_to_xyxy(cx, cy, w, h, image_w, image_h)))
    return boxes


def greedy_match_any_class(
    gt_boxes: list[tuple[int, tuple[float, float, float, float]]],
    pred_boxes: list[tuple[int, float, tuple[float, float, float, float]]],
    iou_threshold: float,
) -> tuple[list[tuple[int, int, float]], list[int], list[int]]:
    candidates: list[tuple[float, int, int]] = []
    for gt_index, (_gt_cls, gt_box) in enumerate(gt_boxes):
        for pred_index, (_pred_cls, _pred_conf, pred_box) in enumerate(pred_boxes):
            iou = box_iou(gt_box, pred_box)
            if iou >= iou_threshold:
                candidates.append((iou, gt_index, pred_index))

    candidates.sort(reverse=True)
    matched_gt: set[int] = set()
    matched_pred: set[int] = set()
    matches: list[tuple[int, int, float]] = []
    for iou, gt_index, pred_index in candidates:
        if gt_index in matched_gt or pred_index in matched_pred:
            continue
        matched_gt.add(gt_index)
        matched_pred.add(pred_index)
        matches.append((gt_index, pred_index, iou))

    unmatched_gt = [index for index in range(len(gt_boxes)) if index not in matched_gt]
    unmatched_pred = [index for index in range(len(pred_boxes)) if index not in matched_pred]
    return matches, unmatched_gt, unmatched_pred


def save_histogram(
    correct_confidences: list[float],
    wrong_confidences: list[float],
    output_path: Path,
    title: str,
) -> None:
    if not correct_confidences and not wrong_confidences:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    bins = [value / 20.0 for value in range(21)]
    if correct_confidences:
        ax.hist(correct_confidences, bins=bins, alpha=0.65, label="correct", color="#2a9d8f")
    if wrong_confidences:
        ax.hist(wrong_confidences, bins=bins, alpha=0.65, label="wrong", color="#e76f51")
    ax.set_title(title)
    ax.set_xlabel("Confidence")
    ax.set_ylabel("Predictions")
    ax.set_xlim(0.0, 1.0)
    ax.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def save_confusion_heatmap(
    class_names: list[str],
    confusion_matrix: dict[tuple[str, str], int],
    output_path: Path,
    title: str,
) -> None:
    if not class_names:
        return
    grid = [[confusion_matrix.get((true_name, pred_name), 0) for pred_name in class_names] for true_name in class_names]
    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(grid, cmap="Blues")
    ax.set_xticks(range(len(class_names)))
    ax.set_yticks(range(len(class_names)))
    ax.set_xticklabels(class_names, rotation=30, ha="right")
    ax.set_yticklabels(class_names)
    ax.set_xlabel("Predicted Class")
    ax.set_ylabel("True Class")
    ax.set_title(title)
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            ax.text(col_index, row_index, str(value), ha="center", va="center", color="black")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def evaluate_stage(
    spec: EvalSpec,
    stage_dir: Path,
    weights_path: Path,
    samples: list[SampleRow],
    *,
    imgsz: int,
    conf: float,
    iou_threshold: float,
    high_conf_threshold: float,
    plots: bool,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    model = YOLO(str(weights_path))
    metrics = model.val(
        data=str(stage_dir / "data.yaml"),
        split=spec.split,
        imgsz=imgsz,
        plots=plots,
        verbose=False,
    )
    scalar_metrics = collect_scalar_metrics(metrics)
    class_names = load_names(stage_dir)

    gt_counts: dict[str, int] = defaultdict(int)
    pred_counts: dict[str, int] = defaultdict(int)
    true_positive_counts: dict[str, int] = defaultdict(int)
    confusion_matrix: dict[tuple[str, str], int] = defaultdict(int)
    status_counts: dict[str, int] = defaultdict(int)
    unknown_samples = 0
    unknown_samples_with_fp = 0
    unknown_fp_detections = 0
    high_conf_wrong_pair = 0

    image_paths = [str(sample.image_path) for sample in samples]
    results = list(model.predict(source=image_paths, stream=True, imgsz=imgsz, conf=conf, verbose=False))
    if len(results) != len(samples):
        raise RuntimeError(
            "Prediction output count did not match the manifest sample count: "
            f"{len(results)} predictions vs {len(samples)} samples."
        )

    detection_rows: list[dict[str, object]] = []
    image_rows: list[dict[str, object]] = []

    for sample, result in zip(samples, results, strict=True):
        image_h, image_w = result.orig_shape
        gt_boxes = load_ground_truth(sample.label_path, image_w=image_w, image_h=image_h)
        pred_boxes = [
            (
                int(box.cls.item()),
                float(box.conf.item()),
                tuple(float(value) for value in box.xyxy[0].tolist()),
            )
            for box in result.boxes
        ]

        for gt_cls, _gt_box in gt_boxes:
            gt_counts[class_names[gt_cls]] += 1
        for pred_cls, _pred_conf, _pred_box in pred_boxes:
            pred_counts[class_names[pred_cls]] += 1

        matches, unmatched_gt, unmatched_pred = greedy_match_any_class(gt_boxes, pred_boxes, iou_threshold)

        image_tp = 0
        image_wrong_pair = 0
        image_unknown_fp = 0
        image_missed = len(unmatched_gt)
        image_extra_fp = 0

        for gt_index, pred_index, iou in matches:
            gt_cls, _gt_box = gt_boxes[gt_index]
            pred_cls, pred_conf, _pred_box = pred_boxes[pred_index]
            true_class = class_names[gt_cls]
            predicted_class = class_names[pred_cls]
            confusion_matrix[(true_class, predicted_class)] += 1
            if gt_cls == pred_cls:
                true_positive_counts[true_class] += 1
                status = "correct"
                image_tp += 1
            else:
                status = "wrong_similar_class"
                image_wrong_pair += 1
                if pred_conf >= high_conf_threshold:
                    high_conf_wrong_pair += 1
            status_counts[status] += 1
            detection_rows.append(
                {
                    "eval_name": spec.run_name,
                    "stage_group": spec.stage_group,
                    "dataset_stage": spec.dataset_stage,
                    "sample_id": sample.sample_id,
                    "image_path": str(sample.image_path),
                    "source_type": sample.source_type,
                    "open_set_role": sample.open_set_role,
                    "pair_family": sample.pair_family,
                    "true_class": true_class,
                    "predicted_class": predicted_class,
                    "confidence": pred_conf,
                    "iou": iou,
                    "status": status,
                    "scene_id": sample.scene_id,
                    "condition_id": sample.condition_id,
                    "mesh_id": sample.mesh_id,
                    "mesh_split": sample.mesh_split,
                    "physical_instance_id": sample.physical_instance_id,
                    "session_id": sample.session_id,
                }
            )

        for gt_index in unmatched_gt:
            gt_cls, _gt_box = gt_boxes[gt_index]
            status_counts["missed_ground_truth"] += 1
            detection_rows.append(
                {
                    "eval_name": spec.run_name,
                    "stage_group": spec.stage_group,
                    "dataset_stage": spec.dataset_stage,
                    "sample_id": sample.sample_id,
                    "image_path": str(sample.image_path),
                    "source_type": sample.source_type,
                    "open_set_role": sample.open_set_role,
                    "pair_family": sample.pair_family,
                    "true_class": class_names[gt_cls],
                    "predicted_class": "",
                    "confidence": 0.0,
                    "iou": 0.0,
                    "status": "missed_ground_truth",
                    "scene_id": sample.scene_id,
                    "condition_id": sample.condition_id,
                    "mesh_id": sample.mesh_id,
                    "mesh_split": sample.mesh_split,
                    "physical_instance_id": sample.physical_instance_id,
                    "session_id": sample.session_id,
                }
            )

        for pred_index in unmatched_pred:
            pred_cls, pred_conf, _pred_box = pred_boxes[pred_index]
            predicted_class = class_names[pred_cls]
            if sample.open_set_role == "unknown_similar_distractor":
                status = "unknown_false_positive"
                image_unknown_fp += 1
                unknown_fp_detections += 1
            else:
                status = "background_false_positive"
                image_extra_fp += 1
            status_counts[status] += 1
            detection_rows.append(
                {
                    "eval_name": spec.run_name,
                    "stage_group": spec.stage_group,
                    "dataset_stage": spec.dataset_stage,
                    "sample_id": sample.sample_id,
                    "image_path": str(sample.image_path),
                    "source_type": sample.source_type,
                    "open_set_role": sample.open_set_role,
                    "pair_family": sample.pair_family,
                    "true_class": "",
                    "predicted_class": predicted_class,
                    "confidence": pred_conf,
                    "iou": 0.0,
                    "status": status,
                    "scene_id": sample.scene_id,
                    "condition_id": sample.condition_id,
                    "mesh_id": sample.mesh_id,
                    "mesh_split": sample.mesh_split,
                    "physical_instance_id": sample.physical_instance_id,
                    "session_id": sample.session_id,
                }
            )

        if sample.open_set_role == "unknown_similar_distractor":
            unknown_samples += 1
            if image_unknown_fp > 0:
                unknown_samples_with_fp += 1

        image_rows.append(
            {
                "eval_name": spec.run_name,
                "stage_group": spec.stage_group,
                "dataset_stage": spec.dataset_stage,
                "sample_id": sample.sample_id,
                "image_path": str(sample.image_path),
                "source_type": sample.source_type,
                "open_set_role": sample.open_set_role,
                "pair_family": sample.pair_family,
                "scene_id": sample.scene_id,
                "condition_id": sample.condition_id,
                "mesh_id": sample.mesh_id,
                "mesh_split": sample.mesh_split,
                "physical_instance_id": sample.physical_instance_id,
                "session_id": sample.session_id,
                "gt_objects": len(gt_boxes),
                "pred_objects": len(pred_boxes),
                "tp_objects": image_tp,
                "wrong_pair_predictions": image_wrong_pair,
                "missed_ground_truth": image_missed,
                "background_false_positives": image_extra_fp,
                "unknown_false_positives": image_unknown_fp,
            }
        )

    per_class_rows: list[dict[str, object]] = []
    for class_name in class_names:
        tp = true_positive_counts[class_name]
        pred_total = pred_counts[class_name]
        gt_total = gt_counts[class_name]
        per_class_rows.append(
            {
                "eval_name": spec.run_name,
                "stage_group": spec.stage_group,
                "dataset_stage": spec.dataset_stage,
                "class_name": class_name,
                "true_positives": tp,
                "predictions": pred_total,
                "ground_truth": gt_total,
                "precision": safe_div(tp, pred_total),
                "recall": safe_div(tp, gt_total),
            }
        )

    total_gt = sum(gt_counts.values())
    total_pred = sum(pred_counts.values())
    total_tp = sum(true_positive_counts.values())
    summary = {
        "eval_name": spec.run_name,
        "stage_group": spec.stage_group,
        "dataset_stage": spec.dataset_stage,
        "split": spec.split,
        "weights": str(weights_path),
        "data_yaml": str(stage_dir / "data.yaml"),
        "images": len(samples),
        "known_gt_objects": total_gt,
        "predicted_objects": total_pred,
        "true_positive_objects": total_tp,
        "wrong_similar_class_predictions": status_counts["wrong_similar_class"],
        "high_conf_wrong_similar_class_predictions": high_conf_wrong_pair,
        "missed_ground_truth": status_counts["missed_ground_truth"],
        "background_false_positives": status_counts["background_false_positive"],
        "unknown_false_positive_detections": unknown_fp_detections,
        "unknown_images": unknown_samples,
        "unknown_images_with_false_positive": unknown_samples_with_fp,
        "unknown_false_positive_rate": safe_div(unknown_samples_with_fp, unknown_samples),
        **scalar_metrics,
    }

    return summary, per_class_rows, image_rows, detection_rows


def select_rows(rows: Iterable[dict[str, object]], *, status: str) -> list[dict[str, object]]:
    return [row for row in rows if row["status"] == status]


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    eval_names = tuple(args.eval or DEFAULT_EVALS)
    eval_specs = build_eval_specs(eval_names)

    stage_summary_rows: list[dict[str, object]] = []
    per_class_rows: list[dict[str, object]] = []
    per_image_rows: list[dict[str, object]] = []
    detection_rows: list[dict[str, object]] = []

    for spec in eval_specs:
        stage_dir = args.datasets_dir / spec.dataset_stage
        weights_path = args.weights_dir / f"{spec.run_name}.pt"
        if not stage_dir.exists():
            message = f"Missing dataset stage directory: {stage_dir}"
            if args.skip_missing:
                print(f"Skipping {spec.run_name}: {message}")
                continue
            raise FileNotFoundError(message)
        if not weights_path.exists():
            message = f"Missing weights file: {weights_path}"
            if args.skip_missing:
                print(f"Skipping {spec.run_name}: {message}")
                continue
            raise FileNotFoundError(message)

        samples_by_split = discover_samples(stage_dir)
        samples = samples_by_split.get(spec.split, [])
        if not samples:
            message = f"No manifest rows for {spec.dataset_stage} split={spec.split}"
            if args.skip_missing:
                print(f"Skipping {spec.run_name}: {message}")
                continue
            raise ValueError(message)

        print(f"Evaluating {spec.run_name} on {len(samples)} image(s)")
        summary, class_rows, image_rows, det_rows = evaluate_stage(
            spec,
            stage_dir,
            weights_path,
            samples,
            imgsz=args.imgsz,
            conf=args.conf,
            iou_threshold=args.iou,
            high_conf_threshold=args.high_conf_threshold,
            plots=args.plots,
        )
        stage_summary_rows.append(summary)
        per_class_rows.extend(class_rows)
        per_image_rows.extend(image_rows)
        detection_rows.extend(det_rows)

    if not stage_summary_rows:
        print("No evaluations were run.")
        return

    write_csv(
        args.output_dir / "stage_summary.csv",
        stage_summary_rows,
        fieldnames=tuple(stage_summary_rows[0].keys()),
    )
    write_csv(
        args.output_dir / "per_class_metrics.csv",
        per_class_rows,
        fieldnames=tuple(per_class_rows[0].keys()),
    )
    write_csv(
        args.output_dir / "per_image_summary.csv",
        per_image_rows,
        fieldnames=tuple(per_image_rows[0].keys()),
    )
    write_csv(
        args.output_dir / "detection_audit.csv",
        detection_rows,
        fieldnames=tuple(detection_rows[0].keys()),
    )

    confusion_rows: list[dict[str, object]] = []
    for row in detection_rows:
        if row["status"] not in {"correct", "wrong_similar_class"}:
            continue
        confusion_rows.append(
            {
                "eval_name": row["eval_name"],
                "true_class": row["true_class"],
                "predicted_class": row["predicted_class"],
                "count": 1,
            }
        )
    aggregated_confusion: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in confusion_rows:
        aggregated_confusion[(str(row["eval_name"]), str(row["true_class"]), str(row["predicted_class"]))] += 1
    pairwise_confusion_rows = [
        {
            "eval_name": eval_name,
            "true_class": true_class,
            "predicted_class": predicted_class,
            "count": count,
        }
        for (eval_name, true_class, predicted_class), count in sorted(aggregated_confusion.items())
    ]
    if pairwise_confusion_rows:
        write_csv(
            args.output_dir / "pairwise_confusion.csv",
            pairwise_confusion_rows,
            fieldnames=("eval_name", "true_class", "predicted_class", "count"),
        )

    correct_confidences = [float(row["confidence"]) for row in detection_rows if row["status"] == "correct"]
    wrong_confidences = [
        float(row["confidence"])
        for row in detection_rows
        if row["status"] in {"wrong_similar_class", "background_false_positive", "unknown_false_positive"}
    ]
    save_histogram(
        correct_confidences,
        wrong_confidences,
        args.output_dir / "plots" / "confidence_histogram.png",
        "Correct vs Wrong Prediction Confidence",
    )

    eval_to_classes: dict[str, set[str]] = defaultdict(set)
    eval_confusions: dict[str, dict[tuple[str, str], int]] = defaultdict(lambda: defaultdict(int))
    for row in detection_rows:
        if row["status"] not in {"correct", "wrong_similar_class"}:
            continue
        eval_name = str(row["eval_name"])
        true_class = str(row["true_class"])
        predicted_class = str(row["predicted_class"])
        eval_to_classes[eval_name].add(true_class)
        eval_to_classes[eval_name].add(predicted_class)
        eval_confusions[eval_name][(true_class, predicted_class)] += 1

    for eval_name, class_name_set in sorted(eval_to_classes.items()):
        save_confusion_heatmap(
            sorted(class_name_set),
            eval_confusions[eval_name],
            args.output_dir / "plots" / f"{eval_name}_confusion_heatmap.png",
            f"{eval_name} Pairwise Confusion",
        )

    high_conf_rows = [
        row
        for row in detection_rows
        if row["status"] in {"wrong_similar_class", "unknown_false_positive"}
        and float(row["confidence"]) >= args.high_conf_threshold
    ]
    high_conf_rows.sort(key=lambda row: float(row["confidence"]), reverse=True)
    hardest_failures = high_conf_rows[:25]
    if hardest_failures:
        write_csv(
            args.output_dir / "hardest_failures.csv",
            hardest_failures,
            fieldnames=tuple(hardest_failures[0].keys()),
        )

    transfer_comparison_rows: list[dict[str, object]] = []
    summaries_by_eval = {str(row["eval_name"]): row for row in stage_summary_rows}
    if {
        "real_small_from_scratch",
        "synthetic_pretrain_plus_real_small",
    }.issubset(summaries_by_eval):
        scratch = summaries_by_eval["real_small_from_scratch"]
        transfer = summaries_by_eval["synthetic_pretrain_plus_real_small"]
        transfer_comparison_rows.append(
            {
                "comparison": "synthetic_pretrain_plus_real_small_minus_real_small_from_scratch",
                "map50_delta": float(transfer["map50"]) - float(scratch["map50"]),
                "map50_95_delta": float(transfer["map50_95"]) - float(scratch["map50_95"]),
                "precision_delta": float(transfer["precision"]) - float(scratch["precision"]),
                "recall_delta": float(transfer["recall"]) - float(scratch["recall"]),
                "wrong_similar_delta": int(transfer["wrong_similar_class_predictions"])
                - int(scratch["wrong_similar_class_predictions"]),
                "high_conf_wrong_similar_delta": int(transfer["high_conf_wrong_similar_class_predictions"])
                - int(scratch["high_conf_wrong_similar_class_predictions"]),
                "unknown_false_positive_rate_delta": float(transfer["unknown_false_positive_rate"])
                - float(scratch["unknown_false_positive_rate"]),
            }
        )
        write_csv(
            args.output_dir / "transfer_comparison.csv",
            transfer_comparison_rows,
            fieldnames=tuple(transfer_comparison_rows[0].keys()),
        )

    summary_payload = {
        "evaluations": stage_summary_rows,
        "transfer_comparison": transfer_comparison_rows,
        "high_confidence_threshold": args.high_conf_threshold,
        "iou_threshold": args.iou,
        "prediction_confidence_threshold": args.conf,
    }
    write_json(args.output_dir / "summary.json", summary_payload)
    print(f"Wrote shape-similarity validation outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
