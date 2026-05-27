# TrayGuard Training Prototype Runbook

## What We Built

- Renamed the Python project package to `trayguard`.
- Added a fresh FastAPI-based training app separate from the legacy Streamlit/YOLO demo.
- Added a plain browser UI for the first learner loop:
  intake -> pre-test -> study cards -> quiz -> practice sort -> post-test -> summary/export.
- Added `basic_general_tray_v1` as the first file-backed tray module.
- Added OpenCV ArUco marker support for deterministic physical card detection.
- Added manual quantity entry as a fallback when camera access is blocked or unreliable.
- Added printable neutral ArUco card generation.
- Added CSV/JSON exports for learner runs under `data/training_runs/`.
- Added unit tests for module loading, scoring, export, and marker generation/detection.

## How To Run

Install/update dependencies:

```bash
uv sync
```

Start the training app:

```bash
uv run trayguard train-app \
  --module config/tray_modules/basic_general_tray_v1.json \
  --host 127.0.0.1 \
  --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

Generate printable sample cards:

```bash
uv run trayguard print-cards \
  --module config/tray_modules/basic_general_tray_v1.json \
  --output-dir outputs/cards/basic_general_tray_v1
```

Open the generated print sheet:

```text
outputs/cards/basic_general_tray_v1/index.html
```

Run tests:

```bash
uv run python -m unittest discover -s tests
```

## Where To Edit Content

- Tray module JSON:
  `config/tray_modules/basic_general_tray_v1.json`
- Generated card sheet and marker PNGs:
  `outputs/cards/basic_general_tray_v1/`
- Web UI:
  `src/trayguard/web/static/`
- Backend/API:
  `src/trayguard/web/`
- Learning module, scoring, export, and ArUco logic:
  `src/trayguard/learning/`

The JSON should remain the source of truth for curated instruments, required quantities, distractors, lookalike pairs, study prompts, and marker IDs. Regenerate cards after changing marker IDs or card mappings.

## Camera Notes

The app uses the browser camera through `navigator.mediaDevices.getUserMedia`.
If `Start camera` reports `NotAllowedError`, enable camera access for the browser in macOS:

System Settings -> Privacy & Security -> Camera

If the in-app browser does not appear there, open the app in Chrome or Safari at `http://127.0.0.1:8000`.

## Next Steps

- Curate the tray module content against the real physical teaching kit.
- Replace placeholder image references with local photos of the actual cards or instruments.
- Improve printable card layout with optional front/back designs.
- Add an authoring workflow so a CSV or spreadsheet can generate the tray JSON.
- Add richer scoring summaries for weak items and high-confidence errors.
- Add a marker reliability checklist before user testing.
- Run a small novice pilot and export pre/post results.
