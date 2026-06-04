#!/usr/bin/env bash
# Pipeline: .tex → .pdf → .png → .pptx
# Usage: ./scripts/build_presentation.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$REPO_DIR/final_paper/source"
OUT_DIR="$REPO_DIR/final_paper/output"

echo "=== Step 1: .tex → .pdf ==="
cd "$SRC_DIR"
pdflatex -interaction=nonstopmode fdr_presentation.tex
bibtex fdr_presentation
pdflatex -interaction=nonstopmode fdr_presentation.tex
pdflatex -interaction=nonstopmode fdr_presentation.tex
cp fdr_presentation.pdf "$OUT_DIR/fdr_presentation.pdf"
echo "PDF: $OUT_DIR/fdr_presentation.pdf"

echo ""
echo "=== Step 2: Clean LaTeX build artifacts ==="
cd "$SRC_DIR"
rm -f \
  fdr_presentation.aux \
  fdr_presentation.bbl \
  fdr_presentation.blg \
  fdr_presentation.log \
  fdr_presentation.out \
  fdr_presentation.toc \
  texput.log

echo ""
echo "=== Step 3: .pdf → per-slide .png ==="
cd "$REPO_DIR"
python3 "$SCRIPT_DIR/generate_slide_pngs.py"

echo ""
echo "=== Step 4: .png → .pptx ==="
uv run python "$SCRIPT_DIR/generate_pptx.py"

echo ""
echo "=== Done ==="
echo "  PDF:  $OUT_DIR/fdr_presentation.pdf"
echo "  PPTX: final_paper/output/fdr_presentation.pptx"
