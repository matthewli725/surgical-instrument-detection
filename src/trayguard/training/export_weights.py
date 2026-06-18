from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DESTINATION = PROJECT_ROOT / "weights" / "trayguard.pt"


def resolve_weights_path(source: Path) -> Path:
    source = source.expanduser()

    candidates = [
        source,
        source / "weights" / "best.pt",
        source / "best.pt",
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    searched = "\n".join(f"  - {candidate}" for candidate in candidates)
    raise FileNotFoundError(f"Could not find weights file. Searched:\n{searched}")


def export_weights(source: Path, destination: Path = DEFAULT_DESTINATION) -> Path:
    weights_path = resolve_weights_path(source)
    destination = destination.expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(weights_path, destination)
    return destination


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard export-weights",
        description="Copy a trained YOLO best.pt file into the local TrayGuard inference weights path.",
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to best.pt, a weights directory, or an Ultralytics run directory.",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=DEFAULT_DESTINATION,
        help=f"Destination weights path. Default: {DEFAULT_DESTINATION}",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    destination = export_weights(args.source, args.destination)
    print(f"Exported TrayGuard weights to: {destination}")
