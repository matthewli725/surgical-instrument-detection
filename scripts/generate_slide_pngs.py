"""Generate per-slide PNGs from the Beamer PDF using pdftoppm.

Usage:
    python scripts/generate_slide_pngs.py

Requires: pdftoppm (part of poppler, available via `brew install poppler`)
"""

import subprocess
import sys
from pathlib import Path

PDF_DIR = Path("final_paper/source")
OUT_DIR = Path("outputs/slides")
PDF = PDF_DIR / "fdr_presentation.pdf"


def main():
    if not PDF.exists():
        print(f"Error: {PDF} not found. Run the LaTeX build first.")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old slide PNGs
    for old in OUT_DIR.glob("slide-*.png"):
        old.unlink()
        print(f"  Removed: {old}")

    # Convert PDF to per-slide PNGs using pdftoppm
    # pdftoppm -png -r 150 input.pdf output_prefix
    # Produces: output_prefix-1.png, output_prefix-2.png, etc.
    prefix = str(OUT_DIR / "slide")
    cmd = [
        "pdftoppm",
        "-png",
        "-r", "150",
        str(PDF),
        prefix,
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: pdftoppm failed:\n{result.stderr}")
        sys.exit(1)

    # Rename from slide-1.png to slide-01.png for consistent sorting
    for png in OUT_DIR.glob("slide-*.png"):
        parts = png.stem.split("-")
        if len(parts) == 2:
            num = int(parts[1])
            new_name = f"slide-{num:02d}.png"
            new_path = png.with_name(new_name)
            png.rename(new_path)

    n_slides = len(list(OUT_DIR.glob("slide-*.png")))
    print(f"Generated {n_slides} slide PNGs in {OUT_DIR}/")


if __name__ == "__main__":
    main()
