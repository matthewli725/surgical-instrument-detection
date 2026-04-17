# TrayGuard

Practical setup and command reference for collecting data, exporting YOLO datasets, training models, and running the demo.

Project background and experiment motivation live in [docs/project_background.md](docs/project_background.md).

Reproduce lighting experiments in
[docs/experiments/lighting_yolo_reproducibility.md](docs/experiments/lighting_yolo_reproducibility.md).

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


## 2. Collect Data

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

## 3. Review Collected Data

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


## 4. Run The Demo App

Run the Streamlit tray-check UI:

```bash
uv run trayguard app
```


By default, the app looks for:

```text
weights/trayguard.pt
```


## 5. Other Useful Commands

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

## 6. Project Layout

```text
src/micro_design_project/       main Python package
scripts/                        helper scripts
config/                         training config
data/                           local datasets, ignored by git
runs/                           training outputs, ignored by git
weights/                        local model weights
docs/project_background.md      motivation and experiment background
docs/experiments/               experiment writeups
```
