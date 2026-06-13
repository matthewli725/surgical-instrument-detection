from __future__ import annotations

from collections.abc import Callable, Sequence
import sys

from trayguard.data_collection import class_folder_collect, collect
from trayguard.app import streamlit_runner
from trayguard.dataset_tools import (
    auto_annotate_class_folders,
    download_lavado,
    export_collected_yolo,
    plan_shape_similarity_synthetic,
)
from trayguard.learning import card_cli
from trayguard import classification as classification_module
from trayguard.training import (
    benchmark,
    export_weights,
    train,
    train_class_folders_classification,
    train_class_folders_detection,
)
from trayguard.web import runner as web_runner


Command = Callable[[Sequence[str]], None]


COMMANDS: dict[str, tuple[Command, str]] = {
    "collect": (collect.main, "Capture setup sessions and lighting variants."),
    "collect-class-folder": (
        class_folder_collect.main,
        "Rapidly capture single-instrument images into one folder per class.",
    ),
    "export-yolo": (export_collected_yolo.main, "Flatten collected sessions into a YOLO dataset."),
    "plan-shape-similarity-synthetic": (
        plan_shape_similarity_synthetic.main,
        "Plan Blender-ready synthetic renders and emit the shape-similarity source manifest.",
    ),
    "download-lavado": (download_lavado.main, "Download the Lavado Kaggle dataset and export YOLO data."),
    "export-weights": (export_weights.main, "Copy trained best.pt weights into the TrayGuard demo path."),
    "train": (train.main, "Train one object detection model."),
    "benchmark": (benchmark.main, "Train and evaluate standard model variants."),
    "app": (streamlit_runner.main, "Launch the Streamlit tray detection UI."),
    "train-app": (web_runner.main, "Launch the TrayGuard educational training web app."),
    "print-cards": (card_cli.main, "Generate printable AprilTag card assets for a tray module."),
    "auto-annotate-class-folders": (
        auto_annotate_class_folders.main,
        "Auto-annotate class-folder images with bounding boxes via background subtraction.",
    ),
    "train-class-folders-detection": (
        train_class_folders_detection.main,
        "Train detection model on auto-annotated class-folder dataset.",
    ),
    "train-class-folders-classification": (
        train_class_folders_classification.main,
        "Train classification model on auto-annotated class-folder dataset.",
    ),
    "classify-image": (
        classification_module.main,
        "Classify a single image using a trained YOLO classification model.",
    ),
}


def print_help() -> None:
    print("usage: trayguard <command> [args]")
    print()
    print("TrayGuard command line tools.")
    print()
    print("commands:")
    for name, (_command, description) in COMMANDS.items():
        print(f"  {name:<22} {description}")
    print()
    print("Run 'uv run trayguard <command> --help' for command-specific options.")


def main(argv: Sequence[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help"}:
        print_help()
        return

    command_name = args[0]
    if command_name not in COMMANDS:
        available = ", ".join(COMMANDS)
        raise SystemExit(f"Unknown command '{command_name}'. Available commands: {available}")

    command, _description = COMMANDS[command_name]
    command(args[1:])
