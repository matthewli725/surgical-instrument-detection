from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from ultralytics import YOLO


DEFAULT_MODEL = "yolo11n-cls"
DEFAULT_IMGSZ = 640
DEFAULT_BATCH = 16
DEFAULT_EPOCHS = 100


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard train-class-folders-classification",
        description="Train a YOLO classification model on the auto-annotated class-folder dataset.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("data/cv/50_pictures_auto/cls"),
        help="Classification dataset directory with train/ and val/ subfolders.",
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
        help="YOLO classification model to use (e.g., yolo11n-cls, yolo11s-cls).",
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
        "--project",
        type=Path,
        default=Path("runs"),
        help="Ultralytics project directory for run logs.",
    )
    parser.add_argument(
        "--name",
        default="50_pictures_classification",
        help="Run name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the training command without running it.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    if not args.dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {args.dataset_dir}")

    args.weights_dir.mkdir(parents=True, exist_ok=True)
    args.project.mkdir(parents=True, exist_ok=True)

    print("=== Classification Training ===")
    print(f"Model: {args.model}")
    print(f"Dataset: {args.dataset_dir}")
    print(f"Epochs: {args.epochs} | imgsz: {args.imgsz} | batch: {args.batch}")
    if args.device:
        print(f"Device: {args.device}")
    print()

    if args.dry_run:
        print("Dry run — skipping training.")
        return

    model = YOLO(args.model)
    model.train(
        data=str(args.dataset_dir),
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        project=str(args.project),
        name=args.name,
        exist_ok=True,
        verbose=True,
    )

    trainer = getattr(model, "trainer", None)
    save_dir = getattr(trainer, "save_dir", None)
    if save_dir is None:
        raise RuntimeError("Training finished, but Ultralytics did not expose a run save directory.")

    best_pt = Path(save_dir) / "weights" / "best.pt"
    if not best_pt.exists():
        raise FileNotFoundError(f"best.pt not found in {save_dir}")

    export_path = args.weights_dir / "50_pictures_classification.pt"
    export_path.write_bytes(best_pt.read_bytes())
    print(f"\nTraining complete. Exported best weights to: {export_path}")
