# TrayGuard

TrayGuard is an SPD training and assessment prototype. The active project
tests whether a local tray module can improve novice simulated tray familiarity
through retrieval-first study, quiz prompts, simulated tray sorting, immediate
feedback, confidence capture, and pre/post error analysis.

The consolidated final report is at
[final_paper/trayguard_paper.pdf](final_paper/trayguard_paper.pdf).

## 1. Install

### Install `uv`

We use `uv` for dependency management.

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


## 2. Active Evaluation Path

The active project work is consolidated in the
[final\_paper/](final_paper/). Use the FDR PDF to defend the
current claim: TrayGuard tests whether a local training module improves novice
simulated tray familiarity. Camera and YOLO utilities support future authoring
or visual-review extensions; the active
evidence path is the pre/post training workflow.

## 3. Legacy/Future CV Utilities

The commands below support camera capture, annotation, model demos, and future
visual-support work. The active experiment plan is the training workflow in
Section 2.

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
data/cv/collected/classes.txt
data/cv/collected/sessions/<session_id>/images/
data/cv/collected/sessions/<session_id>/labels/
data/cv/collected/sessions/<session_id>/metadata.json
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
data/cv/class_folder_raw/<class_slug>/
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
src/trayguard/       main Python package
scripts/                        helper scripts
config/                         training config
data/                           local datasets, ignored by git
runs/                           training outputs, ignored by git
weights/                        local model weights
final_paper/                    FDR paper and bibliography
```
