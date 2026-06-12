from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from trayguard.learning.cards import print_cards, print_instrument_catalog_cards
from trayguard.learning.catalog import load_instrument_catalog
from trayguard.learning.module import load_tray_module


DEFAULT_MODULE = Path("config/tray_modules/fgvc12_major_focused_v1.json")
DEFAULT_CATALOG = Path("config/instrument_catalogs/hospitools_dslr_v1.json")
DEFAULT_OUTPUT_DIR = Path("outputs/cards/fgvc12_major_focused_v1")
DEFAULT_CATALOG_OUTPUT_DIR = Path("outputs/cards/hospitools_dslr_v1")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="trayguard print-cards", description="Generate neutral printable ArUco card assets.")
    parser.add_argument("--module", type=Path, default=DEFAULT_MODULE, help="Tray module JSON file.")
    parser.add_argument("--catalog", type=Path, help="Instrument catalog JSON file. When set, prints catalog flashcards instead of tray cards.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory for marker PNGs and index.html.")
    parser.add_argument("--marker-start", type=int, default=100, help="First ArUco marker ID for catalog flashcards.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.catalog:
        output_dir = args.output_dir if args.output_dir != DEFAULT_OUTPUT_DIR else DEFAULT_CATALOG_OUTPUT_DIR
        catalog = load_instrument_catalog(args.catalog)
        paths = print_instrument_catalog_cards(catalog.name, catalog.instruments, output_dir, marker_start=args.marker_start)
        print(f"Wrote {len(paths)} catalog card asset(s) to {output_dir}")
        return

    module = load_tray_module(args.module)
    paths = print_cards(module, args.output_dir)
    print(f"Wrote {len(paths)} card asset(s) to {args.output_dir}")
