# TrayGuard CV Utilities

Camera capture, annotation, YOLO training, model evaluation, and the legacy
Streamlit tray-check demo app.

The active education workflow is documented in [README.md](README.md).

## Quick Start

```bash
# Data collection
uv run trayguard collect
uv run trayguard collect-class-folder

# Export collected data to YOLO format
uv run trayguard export-yolo

# Train an object detection model
uv run trayguard train
uv run trayguard train model=yolo11m trainer.imgsz=960 trainer.batch=8

# Train all benchmark variants
uv run trayguard benchmark

# Download the Lavado surgical tools dataset
uv run trayguard download-lavado

# Launch the legacy Streamlit tray-check demo app
uv run trayguard app

# Export trained weights to the demo path
uv run trayguard export-weights runs/detect/spoons/weights/best.pt
```

## Data Collection

### Main Capture (collect)

Captures webcam setup sessions and reuses annotations across lighting variants.

```bash
uv run trayguard collect
uv run trayguard collect --camera-index 1
uv run trayguard collect --camera-index 1 --output-dir data/cv/collected_my_session
```

Options:
- `--camera-index` — OpenCV camera index (default: 0)
- `--output-dir` — session output root (default: `data/cv/collected/`)
- `--prefix` — filename prefix for session IDs (default: `setup`)
- `--classes-file` — optional path to existing `classes.txt`
- `--image-ext` — image format (jpg or png, default: jpg)

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
- Draw tight boxes around the object, not shadow or glare.
- Press `n` only when ready for a new object arrangement.

Output structure:

```text
data/cv/collected/classes.txt
data/cv/collected/sessions/<session_id>/images/
data/cv/collected/sessions/<session_id>/labels/
data/cv/collected/sessions/<session_id>/metadata.json
```

### Class Folder Capture (collect-class-folder)

Rapidly capture single-instrument images into one folder per class. No
annotation — each image is saved into a folder named after the class.

```bash
uv run trayguard collect-class-folder
```

Controls:
- Type the instrument class name in the OpenCV window first.
- `ENTER`: start capturing that class
- `SPACE` or `c`: save image
- `n`: start a new class
- `q`: quit

Output:

```text
data/cv/class_folder_raw/<class_slug>/
```

### Review Collected Data

```bash
uv run python scripts/visualize_collected_session.py
uv run python scripts/visualize_collected_session.py --collected-dir data/cv/collected_andy1
uv run python scripts/visualize_collected_session.py 090045
```

Viewer controls:
- Left/right arrows, `a`/`d`, `h`/`l`, `p`/`n`: previous/next image
- Up/down arrows, `w`/`s`, `k`/`j`: jump backward/forward 5 images
- `SPACE`: next image
- `0`: first image
- `q` or `ESC`: quit

### Export to YOLO

Flatten collected sessions into a YOLO-format dataset with train/val/test
splits at the session level.

```bash
uv run trayguard export-yolo
uv run trayguard export-yolo --input-dir data/cv/collected_my_session --output-dir data/cv/collected_yolo --overwrite
```

Options:
- `--input-dir` — collected session root (default: `data/cv/collected/`)
- `--output-dir` — YOLO dataset output (default: `data/cv/collected_yolo/`)
- `--train-ratio` — train split fraction (default: 0.7)
- `--val-ratio` — validation split fraction (default: 0.2)
- `--test-ratio` — test split fraction (default: 0.1)
- `--seed` — random seed for session-level splitting (default: 42)
- `--overwrite` — replace existing output directory

Output includes `data.yaml` that can be passed directly to the training command.

### Auto-Annotate Class Folders

Generate bounding box annotations for class-folder images using background
subtraction:

```bash
uv run trayguard auto-annotate-class-folders
```

## Training

### Config System (Hydra)

Training uses Hydra for configuration. The config directory is `config/`:

```text
config/
  default.yaml             master config (data, model, trainer defaults)
  data/                    dataset configs
    object_detection.yaml  points to data/lavado by default
    surgical_kit_proxy.yaml
  model/                   model architecture configs
    yolo11n.yaml           YOLO11 nano
    yolo11s.yaml           YOLO11 small
    yolo11m.yaml           YOLO11 medium
    yolo11l.yaml           YOLO11 large
    rtdetr-l.yaml          RT-DETR large
  trainer/                 training hyperparameters
    default.yaml           100 epochs, batch 16, imgsz 640, lr 0.01
  hydra/                   Hydra system config
```

Train with defaults (loads `config/default.yaml` which points at `yolo11s`
model and `data/lavado` dataset):

```bash
uv run trayguard train
```

Override any config value on the command line:

```bash
uv run trayguard train model=yolo11m trainer.imgsz=960 trainer.batch=8 \
  data.name=my_dataset \
  data.root=data/cv/collected_yolo \
  data.yolo_data=data/cv/collected_yolo/data.yaml \
  trainer.name=my_experiment
```

The `--export-weights` flag copies the trained `best.pt` to a specific path:

```bash
uv run trayguard train --export-weights weights/my_model.pt
```

Use `--no-export-weights` to skip copying.

### Experiment Scripts

Shell scripts that chain multiple training runs:

```bash
bash scripts/train_surgical_kit.sh      # 3 surgical kit proxy experiments
bash scripts/train_lighting_diversity.sh # 3 lighting diversity experiments
```

These scripts run from the repo root and pass Hydra overrides for each
training variant.

### Full Training Example

```bash
uv run trayguard train --export-weights weights/surgical_kit_matte.pt \
  model=yolo11s \
  data.name=surgical_kit_matte \
  data.root=data/cv/surgical_kit_proxy/lighting/matte_train_reflective_test \
  data.yolo_data=data/cv/surgical_kit_proxy/lighting/matte_train_reflective_test/data.yaml \
  trainer.name=surgical_kit_matte \
  trainer.imgsz=640 trainer.batch=16 trainer.device=0 trainer.deterministic=true
```

### Train on Auto-Annotated Class-Folder Data

```bash
uv run trayguard train-class-folders-detection
uv run trayguard train-class-folders-classification
```

### Download External Dataset

```bash
uv run trayguard download-lavado
```

Downloads the Lavado surgical tools dataset from Kaggle and exports to
YOLO format under `data/lavado/`.

### Benchmark

Train and evaluate standard model variants defined in `config/`:

```bash
uv run trayguard benchmark
```

### Export Weights

Copy a trained run's weights into the default demo path:

```bash
uv run trayguard export-weights runs/detect/spoons/weights/best.pt
```

## Evaluation

Experiment evaluation scripts in `scripts/`:

| Script | Purpose |
|---|---|
| `scripts/evaluate_all.py` | Evaluate all trained models |
| `scripts/eval_surgical_kit.py` | Surgical kit proxy evaluation |
| `scripts/eval_lighting_diversity.py` | Lighting diversity evaluation |
| `scripts/validate_surgical_kit.py` | Validate surgical kit predictions |
| `scripts/validate_brightness_experiments.py` | Validate brightness experiment results |
| `scripts/validate_shape_similarity_experiments.py` | Validate shape similarity experiment results |
| `scripts/cross_dataset_eval.py` | Cross-dataset evaluation |
| `scripts/print_yolo_metrics.py` | Print YOLO metrics from saved runs |
| `scripts/replot_brightness_reports.py` | Regenerate brightness experiment plots |

## Legacy App

Run the Streamlit tray-check UI:

```bash
uv run trayguard app
```

By default the app looks for `weights/trayguard.pt`. Use `export-weights` to
copy a trained model into the expected path:

```bash
uv run trayguard export-weights runs/detect/spoons/weights/best.pt
```
