from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from trayguard.training import train as train_module


DEFAULT_RUNS: tuple[str, ...] = (
    "synthetic_seen_condition",
    "synthetic_heldout_condition",
    "real_small_from_scratch",
    "synthetic_pretrain_plus_real_small",
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train the staged shape-similarity YOLO experiments, including the synthetic-to-real transfer branch."
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
        help="Directory for exported best.pt files.",
    )
    parser.add_argument(
        "--run",
        action="append",
        choices=list(DEFAULT_RUNS),
        help="Training run to execute. Pass more than once to limit the run set. Defaults to all.",
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
        help="Print the underlying trayguard train commands without starting training.",
    )
    return parser.parse_args(argv)


def build_train_args(
    *,
    run_name: str,
    dataset_stage: str,
    datasets_dir: Path,
    weights_dir: Path,
    model: str,
    imgsz: int,
    batch: int,
    device: str | None,
    epochs: int | None,
    init_weights: Path | None = None,
) -> list[str]:
    stage_dir = datasets_dir / dataset_stage
    data_yaml = stage_dir / "data.yaml"
    export_weights = weights_dir / f"{run_name}.pt"

    args = [
        "--export-weights",
        str(export_weights),
        f"model={model}",
        f"data.name={run_name}",
        f"data.root={stage_dir}",
        f"data.yolo_data={data_yaml}",
        f"trainer.name={run_name}",
        f"trainer.imgsz={imgsz}",
        f"trainer.batch={batch}",
        "trainer.deterministic=true",
    ]
    if init_weights is not None:
        args.append(f"model.weights={init_weights}")
    if device:
        args.append(f"trainer.device={device}")
    if epochs is not None:
        args.append(f"trainer.epochs={epochs}")
    return args


def run_train_command(train_args: list[str], *, dry_run: bool) -> None:
    print("uv run trayguard train " + " ".join(train_args))
    if dry_run:
        return
    train_module.main(train_args)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    runs = tuple(args.run or DEFAULT_RUNS)
    args.weights_dir.mkdir(parents=True, exist_ok=True)

    if "synthetic_seen_condition" in runs:
        print("=== synthetic_seen_condition ===")
        run_train_command(
            build_train_args(
                run_name="synthetic_seen_condition",
                dataset_stage="synthetic_seen_condition",
                datasets_dir=args.datasets_dir,
                weights_dir=args.weights_dir,
                model=args.model,
                imgsz=args.imgsz,
                batch=args.batch,
                device=args.device,
                epochs=args.epochs,
            ),
            dry_run=args.dry_run,
        )

    if "synthetic_heldout_condition" in runs:
        print("=== synthetic_heldout_condition ===")
        run_train_command(
            build_train_args(
                run_name="synthetic_heldout_condition",
                dataset_stage="synthetic_heldout_condition",
                datasets_dir=args.datasets_dir,
                weights_dir=args.weights_dir,
                model=args.model,
                imgsz=args.imgsz,
                batch=args.batch,
                device=args.device,
                epochs=args.epochs,
            ),
            dry_run=args.dry_run,
        )

    if "real_small_from_scratch" in runs:
        print("=== real_small_from_scratch ===")
        run_train_command(
            build_train_args(
                run_name="real_small_from_scratch",
                dataset_stage="synthetic_to_real_transfer_real_small",
                datasets_dir=args.datasets_dir,
                weights_dir=args.weights_dir,
                model=args.model,
                imgsz=args.imgsz,
                batch=args.batch,
                device=args.device,
                epochs=args.epochs,
            ),
            dry_run=args.dry_run,
        )

    if "synthetic_pretrain_plus_real_small" in runs:
        pretrain_weights = args.weights_dir / "synthetic_to_real_transfer_pretrain.pt"
        print("=== synthetic_to_real_transfer_pretrain ===")
        run_train_command(
            build_train_args(
                run_name="synthetic_to_real_transfer_pretrain",
                dataset_stage="synthetic_to_real_transfer_pretrain",
                datasets_dir=args.datasets_dir,
                weights_dir=args.weights_dir,
                model=args.model,
                imgsz=args.imgsz,
                batch=args.batch,
                device=args.device,
                epochs=args.epochs,
            ),
            dry_run=args.dry_run,
        )

        print("=== synthetic_pretrain_plus_real_small ===")
        run_train_command(
            build_train_args(
                run_name="synthetic_pretrain_plus_real_small",
                dataset_stage="synthetic_to_real_transfer_real_small",
                datasets_dir=args.datasets_dir,
                weights_dir=args.weights_dir,
                model=args.model,
                imgsz=args.imgsz,
                batch=args.batch,
                device=args.device,
                epochs=args.epochs,
                init_weights=pretrain_weights,
            ),
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
