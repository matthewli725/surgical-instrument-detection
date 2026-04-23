# Reproduce The Shape-Similarity YOLO Pipeline

This note explains the staged shape-similarity experiment path. The v1 pipeline
is manifest-driven so synthetic BlenderProc renders and small real proxy images
can be exported through the same staged split logic.

## What This Covers

The pipeline exports four stage directories:

| Stage Directory | Purpose |
| --- | --- |
| `synthetic_seen_condition` | Synthetic floor stage inside one seen rendering domain |
| `synthetic_heldout_condition` | Synthetic robustness stage with held-out rendering conditions |
| `synthetic_to_real_transfer_pretrain` | Synthetic pretraining source for the transfer comparison |
| `synthetic_to_real_transfer_real_small` | Small real proxy dataset used for both transfer branches |

The transfer report is then evaluated through two training branches:

- `real_small_from_scratch`
- `synthetic_pretrain_plus_real_small`

## Source Dataset Contract

The exporter expects a source root such as `data/shape_similarity_source/` with
this structure:

```text
data/shape_similarity_source/
  samples.csv
  renders_or_photos/...
  labels/...
```

The default experiment definition lives at:

```text
config/shape_similarity/default_experiment.json
```

That config fixes:

- the known classes used in `data.yaml`
- the default similar-pair families
- the stage names and split columns
- the rationale for what each stage is meant to prove

## Required `samples.csv` Columns

Each row in `samples.csv` describes one image:

| Column | Meaning |
| --- | --- |
| `sample_id` | Stable sample identifier used in exported filenames |
| `image` | Image path, relative to the source root or absolute |
| `label` | YOLO label path, relative or absolute; may be blank for unknown-only distractor images |
| `source_type` | `synthetic` or `real` |
| `open_set_role` | `known` or `unknown_similar_distractor` |
| `class_name` | Known class name for known samples; blank is acceptable for distractor-only images |
| `pair_family` | Similarity family such as `scissors_curve` |
| `scene_id` | Synthetic scene or real capture scene identifier |
| `condition_id` | Lighting/material/session condition bucket |
| `mesh_id` | Mesh identifier for synthetic assets, or proxy asset id for real captures |
| `mesh_split` | Human-readable note such as `shared`, `heldout`, or `not_applicable` |
| `physical_instance_id` | Physical instance id for real captures when available |
| `session_id` | Capture or render session identifier |
| `stage_seen_split` | `train`, `val`, `test`, or blank |
| `stage_heldout_split` | `train`, `val`, `test`, or blank |
| `transfer_pretrain_split` | `train`, `val`, `test`, or blank |
| `transfer_real_split` | `train`, `val`, `test`, or blank |

The split columns are the most important part. The exporter does not invent the
claim logic after the fact. It copies the split assignments you decided in the
source manifest.

## Why The Split Columns Matter

The stage meanings should stay explicit:

- `stage_seen_split` proves interpolation inside one synthetic domain
- `stage_heldout_split` proves held-out synthetic condition robustness
- `transfer_pretrain_split` defines the synthetic source used for pretraining
- `transfer_real_split` defines the real proxy dataset used by both transfer
  branches

If the real stage cannot hold out physical instances, keep the split but record
that limitation in the source manifest notes and in the final writeup.

## Synthetic Scene Generation Workflow

The repo does not yet bundle BlenderProc scene builders. The current workflow is
therefore:

1. Render overhead tray-like scenes in BlenderProc with mild pose and spacing
   variation.
2. Export YOLO image and label files for each rendered scene.
3. Assign each render to the stage split columns in `samples.csv`.
4. Record asset identifiers, mesh holdout status, and condition buckets in the
   same manifest.
5. Keep licenses for downloaded 3D assets alongside the asset inventory used to
   build `mesh_id`.

The intended v1 randomization axes are:

- lighting direction and intensity
- material roughness
- camera distance
- object rotation
- tray or background texture

## Export The Staged Datasets

Run all commands from the repo root.

```bash
uv sync

uv run python scripts/export_shape_similarity_yolo.py \
  --input-dir data/shape_similarity_source \
  --output-dir data/shape_similarity_yolo \
  --overwrite
```

Each exported stage has the standard YOLO layout:

```text
data/shape_similarity_yolo/<stage>/
  data.yaml
  images/train/
  images/val/
  images/test/
  labels/train/
  labels/val/
  labels/test/
  manifests/
```

The stage manifests are the audit trail:

- `manifests/stage.csv`: stage purpose, rationale, and split interpretation
- `manifests/pairs.csv`: similar-pair family definitions
- `manifests/samples.csv`: one row per exported image with source metadata
- `manifests/train.txt`, `val.txt`, `test.txt`: raw YOLO image lists

## Train The Staged Models

Train the whole staged study with one helper:

```bash
uv run python scripts/train_shape_similarity_yolo.py
```

That helper trains these four reportable runs with `model=yolo11s` by default:

- `synthetic_seen_condition`
- `synthetic_heldout_condition`
- `real_small_from_scratch`
- `synthetic_pretrain_plus_real_small`

The helper also trains `synthetic_to_real_transfer_pretrain.pt` as the internal
initialization step before the fine-tune branch.

To inspect the exact commands without starting training:

```bash
uv run python scripts/train_shape_similarity_yolo.py --dry-run
```

To run only part of the study:

```bash
uv run python scripts/train_shape_similarity_yolo.py \
  --run synthetic_seen_condition \
  --run synthetic_pretrain_plus_real_small
```

To override the standard model and trainer family:

```bash
uv run python scripts/train_shape_similarity_yolo.py \
  --model yolo11s \
  --imgsz 640 \
  --batch 16 \
  --epochs 100
```

## Validate The Study

The validation workflow keeps pairwise confusion as the headline.

```bash
uv run python scripts/validate_shape_similarity_experiments.py
```

Outputs are written to:

```text
reports/shape_similarity_validation/
```

Key outputs include:

- `stage_summary.csv`
- `per_class_metrics.csv`
- `pairwise_confusion.csv`
- `detection_audit.csv`
- `hardest_failures.csv`
- `transfer_comparison.csv`
- `plots/*_confusion_heatmap.png`
- `plots/confidence_histogram.png`

## What The Validation Outputs Mean

- `stage_summary.csv` reports the standard detector metrics plus high-risk
  pair-confusion counts and unknown-distractor false-positive rates.
- `per_class_metrics.csv` is the per-class precision and recall table for known
  classes.
- `pairwise_confusion.csv` shows which specific similar classes are being mixed
  up.
- `hardest_failures.csv` surfaces the highest-confidence wrong-pair and
  unknown-distractor false positives for qualitative review.
- `transfer_comparison.csv` is the main transfer result. It compares
  `synthetic_pretrain_plus_real_small` against `real_small_from_scratch` on the
  same small real test set.

## v1 Limitations To Keep Explicit

- BlenderProc scene generation is assumed but not yet bundled in this repo.
- Real transfer claims are only as strong as the real proxy split design.
- Public 3D assets may be acceptable for research prototyping, but commercial
  readiness is out of scope.
- This pipeline answers a narrow discrimination question under tray-like
  conditions. It does not claim readiness for real surgical-instrument
  deployment.
