# Reproduce The Brightness YOLO Results

This note explains how to export the new brightness-order datasets from
`data/collected/sessions/` and how to train the five staged YOLO experiments.

## What This Covers

The brightness exporter treats these six session folders as a controlled
illumination dataset:

- `matte-background-order1`
- `matte-background-order2`
- `matte-background-overlay`
- `reflective-background-order1`
- `reflective-background-order2`
- `reflective-background-overlay`

The exporter interprets `variant_0001 ... variant_0011` as a brightness ladder
in capture order, from brightest to dimmest. It ignores `reference.jpg` for
this experiment because the new study is centered on the eleven post-reference
brightness steps.

The current raw data has one known gap:

- `matte-background-order1` is missing `variant_0011`

The exporter reports this during export so the incomplete session is visible in
the logs and manifests.

## Why These Splits Exist

This dataset supports three related questions, and the staged splits are meant
to isolate them instead of mixing all effects together.

### 1. Brightness Generalization

These stages test whether the detector still works when the scene gets darker
than the lighting it saw during training.

- `bright_train_dim_test`: train on brighter separated images and test on
  dimmer separated images
- `dim_train_bright_test`: train on dimmer separated images and test on
  brighter separated images

These are complementary rather than redundant. The first stage shows how much
performance drops when the model is trained on easier lighting and deployed on
harder lighting. The second stage checks whether low-light training transfers
back upward to easier conditions.

### 2. Background Transfer

These stages test whether the model is learning the objects or overfitting to
the scene background and reflectivity context.

- `matte_train_reflective_test`: train on matte-background separated images and
  test on reflective-background separated images
- `reflective_train_matte_test`: train on reflective-background separated
  images and test on matte-background separated images

These stages keep the layout separated and use all brightness ranks so the
background domain is the main thing that changes between train and test.

### 3. Overlap And Occlusion Stress

This stage tests whether overlap and clutter reduce detection and count quality,
especially when the brightness is already challenging.

- `separated_train_overlay_test`: train on non-overlapping layouts and test on
  overlapping layouts

This is intentionally different from the lighting-only stages. The `overlay`
sessions are not pure lighting changes; they add occlusion. Keeping them out of
the brightness-only training stages helps preserve a cleaner causal story.

## How The Session Types Map To The Experiment

The six session folders play different roles:

- `order1` and `order2` are the separated layouts
- `overlay` is the overlapping layout
- `matte` and `reflective` define the background domain
- `variant_0001 ... variant_0011` define the brightness ladder

This means the staged datasets are controlled along one axis at a time:

- brightness stages vary train-vs-test illumination while keeping layout
  separated
- background-transfer stages vary matte-vs-reflective background while keeping
  layout separated
- overlap stages vary separated-vs-overlay layout while keeping the brightness
  ladder available in both conditions

## What The Metrics Are Meant To Show

The experiment outputs are meant to answer two levels of question.

Aggregate stage metrics such as precision, recall, mAP50, and mAP50-95 answer:

- Which experiment split is hardest overall?
- Does training on harder conditions help generalization?

Per-brightness and per-image metrics answer:

- At what brightness rank does performance start to fall?
- Does the drop happen in both backgrounds or mainly one?
- Does overlap cause a bigger failure gap under lower light?
- Are failures mainly missed detections, extra detections, or count errors?

That is why the validation workflow saves both:

- YOLO summary metrics for each stage
- grouped per-brightness metrics
- per-image count and detection outcomes
- plots for brightness, background transfer, and overlap effects

## Export The Staged Datasets

Run all commands from the repo root.

```bash
uv sync

uv run python scripts/export_brightness_yolo.py \
  --output-dir data/brightness_yolo \
  --overwrite
```

The exporter writes five staged YOLO datasets:

| Stage | Meaning |
| --- | --- |
| `bright_train_dim_test` | Train on brighter separated images and test on dimmer separated images |
| `dim_train_bright_test` | Train on dimmer separated images and test on brighter separated images |
| `matte_train_reflective_test` | Train on matte-background separated images and test on reflective-background separated images |
| `reflective_train_matte_test` | Train on reflective-background separated images and test on matte-background separated images |
| `separated_train_overlay_test` | Train on separated layouts and test on overlapping layouts |

Each stage has the normal YOLO layout:

```text
data/brightness_yolo/<stage>/
  data.yaml
  images/train/
  images/val/
  images/test/
  labels/train/
  labels/val/
  labels/test/
  manifests/
```

The manifests are the easiest way to verify the split logic:

- `manifests/stage.csv`: stage definition, including which backgrounds, layouts,
  and brightness ranks belong to train vs test
- `manifests/samples.csv`: one row per exported image with `session_id`,
  `background`, `layout`, and `brightness_rank`
- `manifests/train.txt`, `val.txt`, `test.txt`: raw YOLO image lists

## Current Export Counts

With the current six sessions, the exporter produces these split sizes:

| Stage | Train | Val | Test |
| --- | ---: | ---: | ---: |
| `bright_train_dim_test` | 24 | 24 | 19 |
| `dim_train_bright_test` | 19 | 19 | 24 |
| `matte_train_reflective_test` | 21 | 21 | 22 |
| `reflective_train_matte_test` | 22 | 22 | 21 |
| `separated_train_overlay_test` | 43 | 43 | 22 |

These numbers reflect the missing `variant_0011` in
`matte-background-order1`.

## Train The Five Models

You can train all five stages with one helper script:

```bash
uv run python scripts/train_brightness_yolo.py
```

By default, that script trains all five stages with:

- `model=yolo11s`
- `trainer.imgsz=640`
- `trainer.batch=16`
- `trainer.deterministic=true`

and exports weights to:

```text
weights/bright_train_dim_test.pt
weights/dim_train_bright_test.pt
weights/matte_train_reflective_test.pt
weights/reflective_train_matte_test.pt
weights/separated_train_overlay_test.pt
```

To inspect the commands without starting training:

```bash
uv run python scripts/train_brightness_yolo.py --dry-run
```

To train only a subset:

```bash
uv run python scripts/train_brightness_yolo.py \
  --stage bright_train_dim_test \
  --stage matte_train_reflective_test
```

To override common training settings:

```bash
uv run python scripts/train_brightness_yolo.py \
  --model yolo11s \
  --imgsz 640 \
  --batch 16 \
  --epochs 100
```

## Equivalent Manual Commands

If you prefer running each training job directly:

```bash
uv run trayguard train \
  model=yolo11s \
  data.name=bright_train_dim_test \
  data.root=data/brightness_yolo/bright_train_dim_test \
  data.yolo_data=data/brightness_yolo/bright_train_dim_test/data.yaml \
  trainer.name=bright_train_dim_test \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/bright_train_dim_test.pt

uv run trayguard train \
  model=yolo11s \
  data.name=dim_train_bright_test \
  data.root=data/brightness_yolo/dim_train_bright_test \
  data.yolo_data=data/brightness_yolo/dim_train_bright_test/data.yaml \
  trainer.name=dim_train_bright_test \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/dim_train_bright_test.pt

uv run trayguard train \
  model=yolo11s \
  data.name=matte_train_reflective_test \
  data.root=data/brightness_yolo/matte_train_reflective_test \
  data.yolo_data=data/brightness_yolo/matte_train_reflective_test/data.yaml \
  trainer.name=matte_train_reflective_test \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/matte_train_reflective_test.pt

uv run trayguard train \
  model=yolo11s \
  data.name=reflective_train_matte_test \
  data.root=data/brightness_yolo/reflective_train_matte_test \
  data.yolo_data=data/brightness_yolo/reflective_train_matte_test/data.yaml \
  trainer.name=reflective_train_matte_test \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/reflective_train_matte_test.pt

uv run trayguard train \
  model=yolo11s \
  data.name=separated_train_overlay_test \
  data.root=data/brightness_yolo/separated_train_overlay_test \
  data.yolo_data=data/brightness_yolo/separated_train_overlay_test/data.yaml \
  trainer.name=separated_train_overlay_test \
  trainer.imgsz=640 \
  trainer.batch=16 \
  trainer.deterministic=true \
  --export-weights weights/separated_train_overlay_test.pt
```

## Validate Trained Weights And Generate Plots

To run all matching validations, save stage metrics, save per-image outcomes,
and generate the experiment plots in one pass:

```bash
uv run python scripts/validate_brightness_experiments.py
```

By default, this looks for:

- datasets under `data/brightness_yolo/`
- weights under `weights/<stage>.pt`
- outputs under `reports/brightness_validation/`

If your trained weights live elsewhere, pass `--weights-dir /path/to/weights`.

The script writes:

- `stage_metrics.csv`: aggregate YOLO metrics per stage
- `image_outcomes.csv`: per-image counts and matched detection outcomes
- `grouped_metrics.csv`: aggregated metrics by stage, brightness rank,
  background, and layout
- `plots/`: experiment-ready PNG figures

If you want to evaluate each model manually on its own test split instead:

```bash
uv run python scripts/print_yolo_metrics.py \
  --model weights/bright_train_dim_test.pt \
  --data data/brightness_yolo/bright_train_dim_test/data.yaml \
  --split test

uv run python scripts/print_yolo_metrics.py \
  --model weights/dim_train_bright_test.pt \
  --data data/brightness_yolo/dim_train_bright_test/data.yaml \
  --split test

uv run python scripts/print_yolo_metrics.py \
  --model weights/matte_train_reflective_test.pt \
  --data data/brightness_yolo/matte_train_reflective_test/data.yaml \
  --split test

uv run python scripts/print_yolo_metrics.py \
  --model weights/reflective_train_matte_test.pt \
  --data data/brightness_yolo/reflective_train_matte_test/data.yaml \
  --split test

uv run python scripts/print_yolo_metrics.py \
  --model weights/separated_train_overlay_test.pt \
  --data data/brightness_yolo/separated_train_overlay_test/data.yaml \
  --split test
```

For analysis, pair those aggregate metrics with `manifests/samples.csv` so you
can compute per-brightness trends and compare separated versus overlap behavior
at the same brightness rank.
