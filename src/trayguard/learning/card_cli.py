from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from trayguard.learning.cards import print_cards
from trayguard.learning.module import load_tray_module


DEFAULT_MODULE = Path("config/tray_modules/basic_general_tray_v1.json")
DEFAULT_OUTPUT_DIR = Path("outputs/cards/basic_general_tray_v1")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="trayguard print-cards", description="Generate neutral printable ArUco card assets.")
    parser.add_argument("--module", type=Path, default=DEFAULT_MODULE, help="Tray module JSON file.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory for marker PNGs and index.html.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    module = load_tray_module(args.module)
    paths = print_cards(module, args.output_dir)
    print(f"Wrote {len(paths)} card asset(s) to {args.output_dir}")
