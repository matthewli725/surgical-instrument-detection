# Reproducing Lighting YOLO Experiment


## Unzip Data and Weights

Run all commands from the repo root after cloning the project.

From the repo root, unzip so these paths exist:

```text
data/spoon_lighting_yolo/
weights/spoons_reference_only.pt
weights/spoons_reference_plus_45.pt
weights/spoons_reference_plus_45_90.pt
```

The exported dataset already has three staged YOLO datasets:

| Stage | Meaning |
| --- | --- |
| `reference_only` | Train only on the reference lighting condition |
| `reference_plus_45` | Train on reference plus 45 degree flashlight conditions |
| `reference_plus_45_90` | Train on reference plus 45 and 90 degree flashlight conditions |

The local export currently has 399 images and 399 matching label files across
the three stages:

| Stage | Images | Labels |
| --- | ---: | ---: |
| `reference_only` | 109 | 109 |
| `reference_plus_45` | 133 | 133 |
| `reference_plus_45_90` | 157 | 157 |

Each stage has the normal YOLO layout:

```text
data/spoon_lighting_yolo/<stage>/
  data.yaml
  images/train/
  images/val/
  images/test/
  labels/train/
  labels/val/
  labels/test/
  manifests/
```

The `manifests/conditions.csv` file is the easiest way to see which lighting
conditions are train vs test for a stage. The `manifests/samples.csv` file maps
every exported image back to its session and lighting condition.


## Validate The Shared Weights


```bash
uv sync

uv run python scripts/print_yolo_metrics.py \
  --model weights/spoons_reference_only.pt \
  --data data/spoon_lighting_yolo/reference_only/data.yaml \
  --split test 

uv run python scripts/print_yolo_metrics.py \
  --model weights/spoons_reference_plus_45.pt \
  --data data/spoon_lighting_yolo/reference_plus_45/data.yaml \
  --split test 

uv run python scripts/print_yolo_metrics.py \
  --model weights/spoons_reference_plus_45_90.pt \
  --data data/spoon_lighting_yolo/reference_plus_45_90/data.yaml \
  --split test 
```

Use the printed precision, recall, mAP50, and mAP50-95 values as the validation
results for each shared model. The experiment summary table is in
`docs/experiments/reflectivity_lighting.md`.

## Retrain The Three Models

Retraining can produce slightly different values across machines, CUDA versions,
and random seeds. For same-number validation, prefer the shared weights above.
For a rerun that follows the same experiment design, use these commands:

```bash
uv run trayguard train \
  model=yolo11s \
  data.name=spoon_lighting_reference_only \
  data.root=data/spoon_lighting_yolo/reference_only \
  data.yolo_data=data/spoon_lighting_yolo/reference_only/data.yaml \
  trainer.name=spoons_reference_only \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/spoons_reference_only.pt

uv run trayguard train \
  model=yolo11s \
  data.name=spoon_lighting_reference_plus_45 \
  data.root=data/spoon_lighting_yolo/reference_plus_45 \
  data.yolo_data=data/spoon_lighting_yolo/reference_plus_45/data.yaml \
  trainer.name=spoons_reference_plus_45 \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/spoons_reference_plus_45.pt

uv run trayguard train \
  model=yolo11s \
  data.name=spoon_lighting_reference_plus_45_90 \
  data.root=data/spoon_lighting_yolo/reference_plus_45_90 \
  data.yolo_data=data/spoon_lighting_yolo/reference_plus_45_90/data.yaml \
  trainer.name=spoons_reference_plus_45_90 \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/spoons_reference_plus_45_90.pt
```
