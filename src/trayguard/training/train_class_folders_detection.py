from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from trayguard.training import train as train_module


DEFAULT_MODEL = "yolo11n"
DEFAULT_IMGSZ = 640
DEFAULT_BATCH = 16
DEFAULT_EPOCHS = 100


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard train-class-folders-detection",
        description="Train a YOLO detection model on the auto-annotated class-folder dataset.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("data/cv/50_pictures_auto/yolo"),
        help="YOLO dataset directory containing data.yaml.",
    )
    parser.add_argument(
        "--weights-dir",
        type=Path,
        default=Path("weights"),
        help="Directory for exported best.pt.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="YOLO model config to use (e.g., yolo11n, yolo11s).",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=DEFAULT_IMGSZ,
        help="Training image size.",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=DEFAULT_BATCH,
        help="Training batch size.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=DEFAULT_EPOCHS,
        help="Training epochs.",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Training device override (e.g., 0, cpu, mps).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the training command without running it.",
    )
    return parser.parse_args(argv)


def build_train_args(args: argparse.Namespace) -> list[str]:
    data_yaml = args.dataset_dir / "data.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError(f"data.yaml not found: {data_yaml}")

    export_weights = args.weights_dir / "50_pictures_detection.pt"

    train_args = [
        "--export-weights",
        str(export_weights),
        f"model={args.model}",
        f"data.name=50_pictures",
        f"data.root={args.dataset_dir}",
        f"data.yolo_data={data_yaml}",
        f"trainer.name=50_pictures_detection",
        f"trainer.imgsz={args.imgsz}",
        f"trainer.batch={args.batch}",
        f"trainer.epochs={args.epochs}",
        "trainer.deterministic=true",
    ]
    if args.device:
        train_args.append(f"trainer.device={args.device}")
    return train_args


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    args.weights_dir.mkdir(parents=True, exist_ok=True)

    train_args = build_train_args(args)
    print("uv run trayguard train " + " ".join(train_args))

    if args.dry_run:
        return

    train_module.main(train_args)
