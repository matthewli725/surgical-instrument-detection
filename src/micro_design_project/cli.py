from __future__ import annotations

from collections.abc import Callable, Sequence
import sys

from micro_design_project.data_collection import collect
from micro_design_project.dataset_tools import export_collected_yolo
from micro_design_project.training import benchmark, train


Command = Callable[[Sequence[str]], None]


COMMANDS: dict[str, tuple[Command, str]] = {
    "collect": (collect.main, "Capture setup sessions and lighting variants."),
    "export-yolo": (export_collected_yolo.main, "Flatten collected sessions into a YOLO dataset."),
    "train": (train.main, "Train one object detection model."),
    "benchmark": (benchmark.main, "Train and evaluate standard model variants."),
}


def print_help() -> None:
    print("usage: trayguard <command> [args]")
    print()
    print("TrayGuard command line tools.")
    print()
    print("commands:")
    for name, (_command, description) in COMMANDS.items():
        print(f"  {name:<12} {description}")
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
