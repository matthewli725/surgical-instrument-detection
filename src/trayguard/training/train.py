from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from hydra import compose, initialize_config_dir
from omegaconf import DictConfig, OmegaConf
from ultralytics import YOLO

from trayguard.training.export_weights import DEFAULT_DESTINATION, export_weights


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = PROJECT_ROOT / "config"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard train",
        description="Train one object detection model using Hydra-style overrides.",
    )
    parser.add_argument(
        "--export-weights",
        type=Path,
        default=DEFAULT_DESTINATION,
        help="Copy the trained best.pt to this path after training. Defaults to weights/trayguard.pt.",
    )
    parser.add_argument(
        "--no-export-weights",
        action="store_true",
        help="Skip copying trained weights after training.",
    )
    parser.add_argument(
        "overrides",
        nargs="*",
        help="Hydra overrides, e.g. model=yolo11m trainer.imgsz=960 trainer.batch=8",
    )
    return parser.parse_args(argv)


def load_config(overrides: Sequence[str]) -> DictConfig:
    with initialize_config_dir(config_dir=str(CONFIG_DIR), version_base=None):
        return compose(config_name="default", overrides=list(overrides))


def train_model(cfg: DictConfig) -> Path:
    print(OmegaConf.to_yaml(cfg))

    model = YOLO(cfg.model.weights)
    model.train(
        data=cfg.data.yolo_data,
        epochs=cfg.trainer.epochs,
        batch=cfg.trainer.batch,
        imgsz=cfg.trainer.imgsz,
        device=cfg.trainer.device,
        workers=cfg.trainer.workers,
        patience=cfg.trainer.patience,
        optimizer=cfg.trainer.optimizer,
        lr0=cfg.trainer.lr0,
        lrf=cfg.trainer.lrf,
        weight_decay=cfg.trainer.weight_decay,
        project=cfg.trainer.project,
        name=cfg.trainer.name,
        pretrained=cfg.trainer.pretrained,
        save=cfg.trainer.save,
        plots=cfg.trainer.plots,
        exist_ok=cfg.trainer.exist_ok,
        verbose=cfg.trainer.verbose,
        resume=cfg.trainer.resume,
        multi_scale=cfg.trainer.multi_scale,
        deterministic=cfg.trainer.deterministic,
    )

    trainer = getattr(model, "trainer", None)
    save_dir = getattr(trainer, "save_dir", None)
    if save_dir is None:
        raise RuntimeError("Training finished, but Ultralytics did not expose a run save directory.")

    return Path(save_dir)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    cfg = load_config(args.overrides)
    save_dir = train_model(cfg)

    if args.no_export_weights:
        print(f"Training complete. Weights remain in run directory: {save_dir}")
        return

    destination = export_weights(save_dir, args.export_weights)
    print(f"Training complete. Exported best weights to: {destination}")
