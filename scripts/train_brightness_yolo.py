from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from trayguard.training import train as train_module


DEFAULT_STAGES: tuple[str, ...] = (
    "brightest_train_darker_test",
    "darkest_train_brighter_test",
    "bright_train_dim_test",
    "dim_train_bright_test",
    "matte_train_reflective_test",
    "reflective_train_matte_test",
    "separated_train_overlay_test",
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train one or more brightness-order YOLO experiment stages."
    )
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=Path("data/brightness_yolo"),
        help="Directory containing exported brightness YOLO stages.",
    )
    parser.add_argument(
        "--weights-dir",
        type=Path,
        default=Path("weights"),
        help="Directory for exported best.pt files.",
    )
    parser.add_argument(
        "--stage",
        action="append",
        choices=list(DEFAULT_STAGES),
        help="Stage to train. Pass more than once to train a subset. Defaults to all stages.",
    )
    parser.add_argument("--model", default="yolo11s", help="Model config override, e.g. yolo11s.")
    parser.add_argument("--imgsz", type=int, default=640, help="Training image size.")
    parser.add_argument("--batch", type=int, default=16, help="Training batch size.")
    parser.add_argument(
        "--device",
        default=None,
        help="Optional trainer.device override. Leave unset to use the project default.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Optional trainer.epochs override. Leave unset to use the project default.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying trayguard train arguments without starting training.",
    )
    return parser.parse_args(argv)


def stage_train_args(
    stage: str,
    datasets_dir: Path,
    weights_dir: Path,
    *,
    model: str,
    imgsz: int,
    batch: int,
    device: str | None,
    epochs: int | None,
) -> list[str]:
    stage_dir = datasets_dir / stage
    data_yaml = stage_dir / "data.yaml"
    export_weights = weights_dir / f"{stage}.pt"

    args = [
        "--export-weights",
        str(export_weights),
        f"model={model}",
        f"data.name={stage}",
        f"data.root={stage_dir}",
        f"data.yolo_data={data_yaml}",
        f"trainer.name={stage}",
        f"trainer.imgsz={imgsz}",
        f"trainer.batch={batch}",
        "trainer.deterministic=true",
    ]
    if device:
        args.append(f"trainer.device={device}")
    if epochs is not None:
        args.append(f"trainer.epochs={epochs}")
    return args


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    stages = tuple(args.stage or DEFAULT_STAGES)
    args.weights_dir.mkdir(parents=True, exist_ok=True)

    for stage in stages:
        train_args = stage_train_args(
            stage,
            args.datasets_dir,
            args.weights_dir,
            model=args.model,
            imgsz=args.imgsz,
            batch=args.batch,
            device=args.device,
            epochs=args.epochs,
        )
        print(f"=== {stage} ===")
        print("uv run trayguard train " + " ".join(train_args))
        if args.dry_run:
            continue
        train_module.main(train_args)


if __name__ == "__main__":
    main()
