# TrayGuard

TrayGuard is an SPD training and assessment prototype. It tests whether a local
tray module can improve novice simulated tray familiarity through retrieval-first
study, quiz prompts, simulated tray sorting, immediate feedback, confidence
capture, and pre/post error analysis.

The consolidated final report is at [fdr/trayguard_paper.pdf](fdr/trayguard_paper.pdf).

CV utilities (data collection, YOLO training, Streamlit demo app) are documented
in [CV_ATTEMPT.md](CV_ATTEMPT.md).

## Install

### Install `uv`

We use `uv` for dependency management. Dependencies are defined in `pyproject.toml` and locked in `uv.lock`; `requirements.txt` mirrors the runtime dependencies for pip-based environments.

- [Install uv](https://docs.astral.sh/uv/)
- [Recommended uv tutorial](https://youtu.be/AMdG7IjgSPM?si=35yro7e7aX2WCrTN)

Clone the repo and install dependencies:

```bash
git clone https://git.capstone.uclalemur.com/2026/building/trayguard.git
cd trayguard
uv sync
```

If you already cloned the repo, run this from the repo folder:

```bash
cd trayguard
uv sync
```

## Quick Start

```bash
# Generate printable AprilTag marker cards and flashcards
uv run trayguard print-cards

# Launch the training web app
uv run trayguard train-app
```

Open `http://127.0.0.1:8000` in a browser.

Print the files in `outputs/cards/fgvc12_major_focused_v1/`:
- `index.html` — one card per instrument, each with a unique AprilTag marker
- `flashcards.html` — instrument study cards with images, distinguishing features, and lookalike info

The web app guides the learner through: Intake → Pre-test → Study → Quiz → Practice sort → Post-test → Summary.

## Learner Workflow

The training web app has seven steps:

1. **Intake** — learner registration. A learner ID (hashed for privacy), group
   assignment (novice/experienced), and prior experience level are recorded.

2. **Pre-test** — baseline tray sort. The learner places printed AprilTag cards
   in the camera frame. The app detects which instruments are present via the
   markers. No feedback is given. Pre-test errors are the baseline for pre/post
   comparison.

3. **Study cards** — the learner reviews instrument flashcards displayed in the
   browser. Each card shows the instrument image, distinguishing features,
   family, aliases, and common lookalikes.

4. **Quiz** — prompted identification. The app shows an instrument image. The
   learner types the instrument name. Accepted answers include the display name
   and any aliases (fuzzy-matched via Levenshtein distance). Confidence is
   recorded per question.

5. **Practice sort** — same mechanics as pre-test, but with feedback. After
   submitting, the app highlights errors and identifies lookalike substitutions
   with feedback messages.

6. **Post-test** — final sort. Identical structure to pre-test. No feedback.
   Scores are compared to pre-test to measure improvement.

7. **Summary** — results page showing pre/post accuracy comparison, detailed
   error breakdown by category, and export paths.

## Print Cards

Generate AprilTag marker cards and instrument flashcards for a tray module:

```bash
# Default module (FGVC12 Major Laparotomy Focused Tray)
uv run trayguard print-cards

# Custom module
uv run trayguard print-cards --module config/tray_modules/50_pictures_demo_v1.json --output-dir outputs/cards/demo

# Instrument catalog flashcards (no markers)
uv run trayguard print-cards --catalog config/instrument_catalogs/hospitools_dslr_v1.json
```

Options:
- `--module` — tray module JSON path (default: `config/tray_modules/fgvc12_major_focused_v1.json`)
- `--catalog` — instrument catalog JSON path (when set, prints catalog flashcards instead of tray cards)
- `--output-dir` — output directory (default: `outputs/cards/fgvc12_major_focused_v1/`)
- `--marker-start` — first AprilTag marker ID for catalog flashcards (default: 100)

Output files:
- `markers/` — individual AprilTag marker PNGs, one per instrument
- `index.html` — printable grid of AprilTag cards (print and cut)
- `flashcards.html` — instrument study cards in 4-per-page grid, printable
- `images/` — standardized instrument images used in flashcards

## Launch the Training App

```bash
# Default module and runs directory
uv run trayguard train-app

# Custom module and runs directory
uv run trayguard train-app --module config/tray_modules/50_pictures_demo_v1.json --runs-dir data/learning/my_study

# Development mode with hot reload
uv run trayguard train-app --reload

# Bind to all interfaces
uv run trayguard train-app --host 0.0.0.0 --port 8000
```

Options:
- `--module` — tray module JSON path
- `--runs-dir` — directory for learner run exports (default: `data/learning/runs/`)
- `--host` — bind host (default: `127.0.0.1`)
- `--port` — bind port (default: `8000`)
- `--reload` — enable Uvicorn reload for UI development

### Camera and AprilTag Detection

The practice sort and pre/post-test screens use the camera to detect printed
AprilTag cards. When a card is placed in the camera frame, the app identifies
the instrument by reading the AprilTag marker and records it as selected.

Detection runs continuously while the camera is active. Cards can be added or
removed from the frame before submitting. A snapshot is taken on submit.

### Manual Fallback

Each sort step includes manual quantity controls. Camera detection can populate
the controls automatically; learners can also submit the manual counts directly.

### Results Export

Results for each learner are exported to `<runs-dir>/<run_id>/`:

- `run.json` — full run metadata, quiz events, attempt summaries
- `attempts.csv` — per-attempt scores (pre, practice, post)
- `items.csv` — per-item error breakdown with error categories

## Authoring a Tray Module

A tray module is a JSON file that defines a surgical instrument tray for
training and assessment. Modules are loaded by `print-cards` and `train-app`.

Two example modules are in `config/tray_modules/`:
- [`fgvc12_major_focused_v1.json`](config/tray_modules/fgvc12_major_focused_v1.json)
  — 16-instrument major laparotomy tray with lookalike pairs and assessment variants
- [`50_pictures_demo_v1.json`](config/tray_modules/50_pictures_demo_v1.json)
  — 11-instrument demo tray (minimal config)

### Required Fields

| Field | Type | Description |
|---|---|---|
| `module_id` | string | Unique module identifier |
| `version` | string | Module version (date or semantic) |
| `name` | string | Human-readable module name |
| `instruments` | array | List of instrument definitions |
| `required_items` | array | Required instrument quantities per tray |

### Instrument Object

Each instrument in `instruments`:

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique identifier used as key in other sections |
| `display_name` | string | Human-readable name |
| `family` | string | Instrument family (e.g., "Cutting/dissecting") |
| `aliases` | array of string | Alternative names for quiz answer matching |
| `distinguishing_features` | array of string | Key visual features displayed on study cards |
| `image_refs` | array of object | Image sources for study and assessment |
| `study_prompts` | array of object | Quiz prompt questions and answers |
| `local_verification_status` | string | Default: `"pending_review"` |

Each image_ref:

| Field | Type | Description |
|---|---|---|
| `id` | string | View identifier (e.g., `"view_a"`) |
| `path` | string | Path to image file |
| `source` | string | Source label |
| `approved_for_study` | boolean | Show on study cards |
| `approved_for_assessment` | boolean | Show during quiz |
| `attribution` | string | Attribution text |
| `url` | string | Source URL |

### Required Item Object

Each item in `required_items`:

| Field | Type | Description |
|---|---|---|
| `instrument_id` | string | References an instrument `id` |
| `quantity` | integer | Number of units required |
| `reference_number` | string | Optional tray reference number |
| `location_or_layer` | string | Optional location/layer label |
| `notes` | string | Optional notes |

### Optional Fields

**`distractor_item_ids`** — array of instrument IDs that serve as distractors
(not required but placed on the tray alongside required items).

**`lookalike_pairs`** — array of instrument pairs that are commonly confused.

Each pair:

| Field | Type | Description |
|---|---|---|
| `id` | string | Pair identifier |
| `expected_id` | string | Correct instrument ID |
| `selected_id` | string | Commonly mistaken instrument ID |
| `feedback_message` | string | Educational feedback shown on lookalike error |

**`assessment_variants`** — array of assessment configurations.

Each variant:

| Field | Type | Description |
|---|---|---|
| `id` | string | Variant identifier |
| `mode` | string | `"pre_test"`, `"post_test"`, or `"practice"` |
| `required_item_ids` | array of string | Subset of instruments to assess |
| `distractor_item_ids` | array of string | Distractors for this variant |
| `random_seed` | string | Seed for reproducible ordering |
| `feedback_enabled` | boolean | Show feedback on submission |
| `photo_view` | string | Image view to use (e.g., `"view_a"`) |

**`marker_cards`** — array of AprilTag card assignments.

Each card:

| Field | Type | Description |
|---|---|---|
| `marker_id` | integer | Unique AprilTag marker ID |
| `instrument_id` | string | Instrument this marker represents |
| `card_id` | string | Human-readable card identifier |
| `role` | string | Optional role (default: `"assessment"`) |

### Validation Rules

When a module is loaded, the following are validated:
- Every `required_items` entry references a valid instrument `id`
- Every `distractor_item_ids` entry references a valid instrument `id`
- Every `assessment_variant` required/distractor item references a valid instrument
- Assessment variant required items are a subset of `required_items`
- `marker_cards` instrument IDs reference valid instruments
- Marker IDs are unique

## Running a Training Session

### Physical Setup

1. **Print cards** — print `outputs/cards/fgvc12_major_focused_v1/index.html`
   (AprilTag markers). Cut individual cards. Each card represents one instrument.
2. **Print flashcards** — print `outputs/cards/fgvc12_major_focused_v1/flashcards.html`
   double-sided for the study phase.
3. **Camera** — position a webcam facing the sorting area. Cards placed in view
   are detected automatically. Good lighting improves detection.
4. **Learner station** — the learner sees the web app on a monitor and places
   cards in the camera frame to indicate tray contents.

### Learner Flow

The app enforces the step order. Each learner completes:
1. Registration (ID, group, experience)
2. Pre-test sort (baseline, no feedback)
3. Self-directed study (browser-based flashcards)
4. Quiz (image to type name)
5. Practice sort (with immediate feedback)
6. Post-test sort (final, no feedback)
7. Summary (pre/post comparison)

Pre-test and post-test use different photo views (`view_a` vs `view_b`) to
prevent image memorization.

### After the Session

Results are in `<runs-dir>/<run_id>/`. Compare pre-test and post-test
`accuracy_score` and `required_recall` to measure improvement.

## Scoring Reference

### Error Categories

| Category | Meaning |
|---|---|
| `correct` | Correct instrument at correct quantity |
| `missing` | Required instrument not placed |
| `extra` | Unrequired instrument placed |
| `misidentified` | Documented lookalike pair substitution |
| `wrong` | Wrong instrument substituted (not a documented lookalike) |
| `wrong_count` | Correct instrument but wrong quantity |

### Confidence Tracking

Each sort submission includes a confidence rating (1-5 scale).
- **High-confidence errors** — confidence >= 4 on an error (overconfidence)
- **Low-confidence correct** — confidence <= 2 on a correct item (underconfidence)

Learners can also flag "not sure" for a given attempt.

### Accuracy Formula

```
error_points = missing_count + extra_count + wrong_substitution_count + misidentified_count
accuracy_score = 100 x (1 - error_points / total_required_units)
required_recall = 100 x correct_units / total_required_units
```

### Output Format

`attempts.csv` columns: `run_id`, `learner_id_hash`, `mode`, `accuracy_score`,
`required_recall`, `error_points`, `missing_count`, `extra_count`,
`wrong_substitution_count`, `misidentified_count`, `wrong_count_error_count`,
`high_confidence_error_count`, `low_confidence_correct_count`,
`duration_seconds`, `overall_confidence`, `completed_full_flow`.

`items.csv` columns: `run_id`, `mode`, `expected_instrument_id`,
`required_quantity`, `selected_instrument_id`, `selected_quantity`,
`error_category`, `is_high_confidence_error`, `is_low_confidence_correct`,
`feedback_message_id`.

## Testing

```bash
uv run pytest
uv run trayguard smoke-learning
```

Tests cover tray module loading, variant-aware scoring, run persistence,
CSV/JSON export, FastAPI endpoints, and AprilTag marker utilities when OpenCV
ArUco support is available.

## Project Layout

```text
src/trayguard/             main Python package
  cli.py                   CLI entry point
  learning/                educational training module
    aruco.py               AprilTag marker detection
    card_cli.py            print-cards CLI
    cards.py               card generation
    module.py              tray module loader
    models.py              tray module schema (dataclasses)
    scoring.py             tray scoring engine
    run_store.py           run persistence
  web/                     FastAPI training web app
    app.py                 API routes
    runner.py              uvicorn launcher
    static/                frontend assets (app.js, index.html, styles.css)
config/                    training config (Hydra) and tray module JSONs
  tray_modules/            tray module definitions
data/                      local datasets, ignored by git
outputs/cards/             generated card assets
tests/                     unit tests
scripts/                   experiment scripts
fdr/                       FDR paper, presentation, and bibliography
weights/                   trained model weights, ignored by git
runs/                      training outputs, ignored by git
```
