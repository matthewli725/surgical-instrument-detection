# TrayGuard

## Automated Surgical Tray Inspection Using Computer Vision

TrayGuard is a computer vision prototype for helping surgical sterilization technicians identify and count instruments in a surgical tray. The long-term goal is a camera-connected system that detects each instrument, counts what has already been collected, and clearly shows the user which required tools are still missing.

This project addresses a real workflow problem: surgical instruments can look very similar, technicians need significant experience to identify them reliably, and manual tray assembly is vulnerable to fatigue, distraction, and counting errors. TrayGuard is meant to reduce that burden by turning the tray check into a guided visual verification task.

## Current Focus

Because we do not have access to a full set of real surgical instruments, and because collecting a broad surgical dataset is outside the scope of this prototype timeline, we are building evidence along several controlled experiment axes. Instead of claiming full deployment readiness, we are testing whether the core computer vision assumptions hold under conditions that resemble the hard parts of surgical tray inspection.

The current system supports:

- Camera-based image collection
- Manual bounding-box annotation
- Reusing labels across controlled lighting variants
- Exporting collected images to YOLO format
- Training and benchmarking object detection models
- Running a Streamlit tray-check UI for live camera detections

The initial classes are:

- Scalpel n4
- Straight Dissection Clamp
- Straight Mayo Scissor
- Curved Mayo Scissor

These classes were chosen because they give us an early test of fine visual differences between similarly shaped instruments.

## Proposed Experiments

Detailed experiment plans live in `tests/`:

- `tests/shape_similarity.md`
- `tests/reflectivity_lighting.md`
- `tests/clutter_occlusion.md`

### 1. Shape Similarity

**Question:** Can the model distinguish between objects that have similar outlines but different identities?

This tests the most important recognition challenge in surgical tray assembly. Many surgical instruments share common visual structure: handles, hinges, clamps, blades, and long narrow bodies. The system needs to learn subtle differences in shape, tip geometry, handle structure, and relative proportions.

**Proposed setup:**

- Collect images of visually similar tools or substitute objects with related silhouettes.
- Keep lighting and background mostly stable.
- Train the detector on multiple shape classes.
- Evaluate whether the model confuses similarly shaped objects.

**Success indicators:**

- High per-class precision and recall for visually similar classes
- Low confusion between paired classes, such as straight vs. curved instruments
- Reasonable detection confidence when objects are rotated or slightly repositioned

### 2. Material and Lighting Robustness

**Question:** Can the model remain reliable when reflective or metallic objects appear under different lighting conditions?

Surgical instruments are commonly metallic, which makes computer vision harder. Reflections, glare, shadows, and exposure changes can make the same object look different between images. Our data collection workflow is designed around this issue: one setup can be annotated once, then captured repeatedly under different lighting conditions.

**Proposed setup:**

- Place a fixed set of objects in a tray or tray-like area.
- Capture one annotated reference image.
- Capture lighting variants with changed light angle, brightness, glare, and shadow.
- Train and evaluate on lighting conditions not seen during training.

**Success indicators:**

- Stable detections across lighting variants
- Limited confidence drop under glare or shadow
- Better performance when lighting augmentation or multi-lighting training data is used

### 3. Clutter and Occlusion

**Question:** Can the model detect and count instruments when objects are close together, overlapping, or partially occluded?

Real trays are not always perfectly organized. Instruments may touch, overlap, or partially hide one another. A useful tray inspection system must still count visible tools and avoid double-counting.

**Proposed setup:**

- Create tray scenes with increasing clutter levels.
- Start with separated objects, then move to touching objects, partial overlap, and heavier occlusion.
- Evaluate detection quality at each clutter level.

**Success indicators:**

- Accurate counts in low and moderate clutter
- Graceful degradation as occlusion increases
- Clear failure cases where the system can flag low confidence instead of silently miscounting

## System Concept

TrayGuard is intended to become an interactive tray-checking system:

1. A technician selects or loads the required instrument list for a tray.
2. A camera captures the current tray state.
3. The detector identifies and counts visible instruments.
4. The interface shows collected tools, missing tools, and uncertain detections.
5. The technician confirms or corrects the result before the tray is completed.

The current repository focuses on the computer vision foundation: data collection, labeling, dataset export, model training, and model evaluation.

## Evaluation Plan

For each experiment axis, we plan to report:

- Dataset size and class list
- Train, validation, and test split strategy
- Mean average precision or other detector metrics
- Per-class precision and recall
- Confusion between similar classes
- Example successes and failures
- Qualitative screenshots of detections

The strongest final result would not be a claim that TrayGuard is ready for operating-room deployment. Instead, it would show that the main risks are testable, that the prototype works under controlled approximations of those risks, and that the same pipeline could scale to real surgical instruments once real data is available.

## Getting Started

### Step 1: Install `uv`

We use `uv` for dependency management.

- [Install uv](https://docs.astral.sh/uv/)
- [Recommended uv tutorial](https://youtu.be/AMdG7IjgSPM?si=35yro7e7aX2WCrTN)

### Step 2: Clone this repo

```bash
# HTTPS
git clone https://git.capstone.uclalemur.com/2026/building/micro-design-project.git

# SSH
git clone ssh://git@git.capstone.uclalemur.com:5522/2026/building/micro-design-project.git
```

### Step 3: Install dependencies

```bash
uv sync
```

## Usage

### Run the tray-check UI

```bash
uv run trayguard app
```

You can also launch the same Streamlit app directly:

```bash
uv run trayguard-app
```

By default, the app looks for model weights at `weights/trayguard.pt`. During development, train on the SSH server, copy the chosen inference weights into that path, and the local UI will use them automatically. The root-level `yolo11s.pt` file is only a local fallback for quick development if curated TrayGuard weights are not present.

Streamlit is a good fit for this prototype because it keeps the camera feed, detection status, and required-tool checklist together with minimal UI code. If the project needs lower-latency browser video later, the better-suited next UI would be a small NiceGUI or FastAPI/WebRTC frontend that reuses the detection code in `src/micro_design_project`.

### Collect webcam training data

```bash
uv run trayguard collect
```

The collection tool uses setup sessions for lighting variation. Press `SPACE` or `c` to capture a reference image, draw boxes around the fixed objects, then press `s` to lock that setup. After that, vary the lighting and press `SPACE` or `c` to save each additional image with the same labels. Press `e` to edit the setup boxes, `n` to start a new setup, or `q` to quit.

When labeling a box, type the class name or class number directly in the popup and press `ENTER`. Press `TAB` to autocomplete matching classes, `ESC` to discard the pending box, or `u` to undo the last saved box. Unknown class names require a second `ENTER` before they are added.

By default, session data is saved to `data/collected/sessions`, and class names are saved to `data/collected/classes.txt`.

### Export collected sessions to YOLO format

```bash
uv run trayguard export-yolo --overwrite
```

The exporter writes a train, validation, and test YOLO dataset to `data/collected_yolo`, splitting by setup session so lighting variants from the same object placement stay in the same split.

### Export staged spoon lighting experiments

For the metal-spoon lighting robustness test, export one YOLO dataset per training stage:

```bash
uv run trayguard export-lighting-yolo --overwrite
```

This writes staged datasets under `data/spoon_lighting_yolo`:

- `reference_only`: trains on the reference image from each spoon arrangement and tests on all non-reference lighting conditions.
- `reference_plus_45`: trains on reference plus the 45 degree flashlight captures, then tests on right light, both lights, phone-above, and 90 degree captures.
- `reference_plus_45_90`: trains on reference plus all 45 and 90 degree flashlight captures, then tests on right light, both lights, and phone-above captures.

Each stage includes `manifests/conditions.csv` and `manifests/samples.csv` so the exact lighting split is auditable. The validation split is a copy of the training split by default because the first stage only has six reference images; use the test split for the lighting robustness result.

Train a stage by overriding the YOLO data path:

```bash
uv run trayguard train data.yolo_data=data/spoon_lighting_yolo/reference_only/data.yaml trainer.name=spoons_reference_only
uv run trayguard train data.yolo_data=data/spoon_lighting_yolo/reference_plus_45/data.yaml trainer.name=spoons_reference_plus_45
uv run trayguard train data.yolo_data=data/spoon_lighting_yolo/reference_plus_45_90/data.yaml trainer.name=spoons_reference_plus_45_90
```

To train and immediately evaluate the held-out lighting conditions with one model variant:

```bash
uv run trayguard benchmark --tests yolo11s:640:16 --extra-override data.yolo_data=data/spoon_lighting_yolo/reference_only/data.yaml
```

### Train one model

```bash
uv run trayguard train
```

After training, the command copies the run's `best.pt` into `weights/trayguard.pt` so the tray-check UI can use the latest selected model immediately.

Training uses Hydra configs in `config`. Override model or trainer settings at the command line:

```bash
uv run trayguard train model=yolo11m trainer.imgsz=960 trainer.batch=8 trainer.name=yolo11m_custom
```

To train without updating the local demo weights:

```bash
uv run trayguard train --no-export-weights
```

If training happens on an SSH server, copy the trained `best.pt` or run folder locally, then export it into the demo path:

```bash
uv run trayguard export-weights path/to/best.pt
```

### Compare model variants

```bash
uv run trayguard benchmark
```

The benchmark command trains the standard YOLO and RT-DETR variants listed in `src/micro_design_project/training/benchmark.py`, evaluates each run on the YOLO test split, and writes results to `runs/benchmark_results.json`.

### Download the Lavado dataset

```bash
uv run trayguard download-lavado
```

This downloads `dilavado/labeled-surgical-tools` through Kaggle Hub and exports a YOLO dataset under `data/lavado`.

## Project Layout

Reusable project code lives under `src/micro_design_project`. The main CLI entrypoint is `uv run trayguard ...`; legacy script code has been folded into package modules so commands and imports use the same source.

- `src/micro_design_project/cli.py`: top-level `trayguard` command dispatcher
- `src/micro_design_project/app/streamlit_app.py`: Streamlit tray-check UI
- `src/micro_design_project/app/state.py`: camera worker state and live detection loop
- `src/micro_design_project/app/streamlit_runner.py`: package-aware Streamlit launcher
- `src/micro_design_project/detection.py`: YOLO image inference and annotation helpers
- `src/micro_design_project/data_collection/collect.py`: data collection orchestration
- `src/micro_design_project/data_collection/annotation_ui.py`: popup box drawing, class entry, and autocomplete
- `src/micro_design_project/data_collection/camera.py`: webcam capture loops
- `src/micro_design_project/data_collection/session_io.py`: session folders, shared YOLO labels, and metadata
- `src/micro_design_project/data_collection/models.py`: `Box` and `CollectionSession`
- `src/micro_design_project/data_collection/classes.py`: default classes and `classes.txt` handling
- `src/micro_design_project/data_collection/drawing.py`: OpenCV overlay drawing helpers
- `src/micro_design_project/dataset_tools/download_lavado.py`: download and export the Lavado Kaggle dataset
- `src/micro_design_project/dataset_tools/export_collected_yolo.py`: export collected sessions into a YOLO train, validation, and test dataset
- `src/micro_design_project/training/export_weights.py`: copy a trained `best.pt` into `weights/trayguard.pt`
- `src/micro_design_project/training/train.py`: train one configured object detection model
- `src/micro_design_project/training/benchmark.py`: train and evaluate multiple model variants
- `scripts/*.py`: thin, debug-friendly wrappers that call the package CLI commands
- `weights/trayguard.pt`: optional curated inference weights for quick local demos
