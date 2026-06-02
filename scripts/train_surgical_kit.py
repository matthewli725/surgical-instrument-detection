from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from micro_design_project.training import train as train_module


LIGHTING_STAGES: tuple[str, ...] = (
    "matte_train_reflective_test",
    "reflective_train_matte_test",
)

SHAPE_STAGES: tuple[str, ...] = (
    "shape_similarity_real_proxy",
)

DEFAULT_STAGES: tuple[str, ...] = LIGHTING_STAGES + SHAPE_STAGES


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train surgical-kit proxy YOLO experiments: lighting transfer and shape similarity."
    )
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=Path("data/cv/surgical_kit_proxy"),
        help="Directory containing exported surgical-kit proxy YOLO stages.",
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
        default=100,
        help="Training epochs. Surgical kit experiments need more epochs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the underlying trayguard train arguments without starting training.",
    )
    return parser.parse_args(argv)


def stage_data_yaml(stage: str, datasets_dir: Path) -> Path:
    if stage in SHAPE_STAGES:
        return datasets_dir / stage / "data.yaml"
    return datasets_dir / "lighting" / stage / "data.yaml"


def export_weight_path(stage: str, weights_dir: Path) -> Path:
    return weights_dir / f"surgical_kit_{stage}.pt"


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
    data_yaml = stage_data_yaml(stage, datasets_dir)
    export_weights = export_weight_path(stage, weights_dir)

    args = [
        "--export-weights",
        str(export_weights),
        f"model={model}",
        f"data.name=surgical_kit_{stage}",
        f"data.root={data_yaml.parent}",
        f"data.yolo_data={data_yaml}",
        f"trainer.name=surgical_kit_{stage}",
        f"trainer.imgsz={imgsz}",
        f"trainer.batch={batch}",
        "trainer.deterministic=true",
        "trainer.patience=40",
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
        print(f"=== surgical_kit_{stage} ===")
        print("uv run trayguard train " + " ".join(train_args))
        if args.dry_run:
            continue
        train_module.main(train_args)


if __name__ == "__main__":
    main()
