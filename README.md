# TrayGuard

TrayGuard is now framed as an SPD training and assessment prototype. The active
project evidence focuses on local tray modules, simulated pre/post sorting,
feedback, confidence, and error breakdowns. Camera capture and YOLO utilities
remain in the repo as legacy/future support, but local CV experiments are no
longer the central claim.

Project background and experiment motivation live in
[docs/background/project_background.md](docs/background/project_background.md).

Workflow adoption risks and literature-backed CV feasibility boundaries live in
[docs/experiments/adoption/workflow_acceptance.md](docs/experiments/adoption/workflow_acceptance.md).

Detailed appendix for literature gaps, stakeholder implications, and retired CV
scope lives in
[docs/experiments/adoption/formal_risk_analysis.md](docs/experiments/adoption/formal_risk_analysis.md).

Planning materials and weekly updates live in
[docs/planning/README.md](docs/planning/README.md).

## 1. Install

### Install `uv`

We use `uv` for dependency management.

- [Install uv](https://docs.astral.sh/uv/)
- [Recommended uv tutorial](https://youtu.be/AMdG7IjgSPM?si=35yro7e7aX2WCrTN)

Clone the repo and install dependencies:

```bash
git clone https://git.capstone.uclalemur.com/2026/building/micro-design-project.git
cd micro-design-project
uv sync
```

If you already cloned the repo, run this from the repo folder:

```bash
cd micro-design-project
uv sync
```


## 2. Active Evaluation Path

The active project work is documentation and prototype evidence for the
training-platform pivot:

- [training effectiveness plan](docs/experiments/adoption/training_effectiveness.md)
- [workflow acceptance plan](docs/experiments/adoption/workflow_acceptance.md)
- [traceability and reporting plan](docs/experiments/adoption/traceability_reporting.md)
- [literature-backed risk analysis](docs/experiments/adoption/formal_risk_analysis.md)
- [claim-evidence control sheet](docs/planning/claim_evidence_control_sheet.md)

Use these files to defend the current claim: TrayGuard tests whether a local
training module improves novice simulated tray familiarity. Do not use local CV
accuracy metrics as the central evidence.

## 3. Legacy/Future CV Utilities

The commands below are retained for camera capture, annotation, model demos, and
future visual-support work. They are not part of the active experiment plan.

### Collect Data

Start data collection:

```bash
uv run trayguard collect
```

If the wrong webcam opens, override the camera index:

```bash
uv run trayguard collect --camera-index 1
```

Try a few camera indexes if needed:

```bash
uv run trayguard collect --camera-index 0
uv run trayguard collect --camera-index 1
uv run trayguard collect --camera-index 2
uv run trayguard collect --camera-index 3
```

Collection controls:

- `SPACE` or `c`: capture image
- Draw boxes with the mouse
- `s`: save/lock the annotated reference setup
- `e`: edit boxes for the current setup
- `n`: start a new setup/session
- `q`: quit
- `TAB`: autocomplete a class name while labeling
- `ENTER`: accept a class label
- `ESC`: cancel a pending box
- `u`: undo the last saved box while annotating

Data collection rules:

- Keep objects still during one setup session.
- Capture and label the reference image first.
- After the reference is saved, change only lighting while capturing variants.
- Use the same class names every time.
- Draw tight boxes around the object, not the shadow or glare.
- Press `n` only when you are ready for a new object arrangement.

Collected data is saved here:

```text
data/collected/classes.txt
data/collected/sessions/<session_id>/images/
data/collected/sessions/<session_id>/labels/
data/collected/sessions/<session_id>/metadata.json
```

For rapid single-instrument capture into one folder per class, run:

```bash
uv run trayguard collect-class-folder
```

Class-folder capture controls:

- Type the instrument class name in the OpenCV window first.
- `ENTER`: start capturing that class
- `SPACE` or `c`: save image
- `n`: start a new class
- `q`: quit

Class-folder images are saved here:

```text
data/class_folder_raw/<class_slug>/
```

### Review Collected Data

Open the latest non-empty session with boxes drawn:

```bash
uv run python scripts/visualize_collected_session.py
```

Open a specific session:

```bash
uv run python scripts/visualize_collected_session.py 090045
```

Viewer controls:

- Left/right arrows: previous/next image
- `a`/`d`, `h`/`l`, or `p`/`n`: previous/next image
- Up/down arrows: jump backward/forward 5 images
- `w`/`s` or `k`/`j`: jump backward/forward 5 images
- `SPACE`: next image
- `0`: first image
- `q` or `ESC`: quit


### Run The Legacy Tray-Check Demo App

Run the Streamlit tray-check UI:

```bash
uv run trayguard app
```


By default, the app looks for:

```text
weights/trayguard.pt
```


### Other Useful Commands

Download the Lavado surgical tools dataset:

```bash
uv run trayguard download-lavado
```

Run the built-in benchmark command:

```bash
uv run trayguard benchmark
```

Export one run's weights into the default demo path:

```bash
uv run trayguard export-weights runs/detect/spoons_reference_plus_45_90/weights/best.pt
```

## 4. Project Layout

```text
src/micro_design_project/       main Python package
scripts/                        helper scripts
config/                         training config
data/                           local datasets, ignored by git
runs/                           training outputs, ignored by git
weights/                        local model weights
docs/README.md                  docs index
docs/background/                problem framing and design background
docs/experiments/               experiment writeups by theme
docs/planning/                  weekly updates and forward plans
```
