# TrayGuard — CV Experiments

This branch (`codex`) contains all CV experiment data collection, dataset preparation, model training, and evaluation code. The final paper lives on the `pivot` branch in `final_paper/`. We switched back here because the experiment data and pipeline code were never migrated to `pivot`.

---

## Datasets (under `data/cv/`)

| Directory | Contents | Classes | Description |
|---|---|---|---|
| `surgical_kit_proxy/` | Amazon-bought surgical training kit | 6: scissor1-4, forcep, scalpel | Real surgical instruments on matte/reflective backgrounds with 12 lighting variants. 4 sessions, 6 objects per image. This is the primary dataset. |
| | `lighting/matte_train_reflective_test/` | same | Train on matte bg (2 sessions), test on reflective bg (2 sessions) |
| | `lighting/reflective_train_matte_test/` | same | Train on reflective bg, test on matte bg |
| | `shape_similarity_real_proxy/` | same | Session-level split for layout generalization |
| `spoon_lighting/` | 3 kitchen spoons on a blue surgical drape | 3: spoon1, spoon2, spoon3 | 12 lighting conditions (reference, flashlight 45/90 deg, phone camera, right/both lights). 7 sessions × 12 conditions. |
| `brightness_experiment/` | 4 spoons + 1 fork on matte/reflective backgrounds | 5: spoon_w/l/m/s, fork | 11 brightness levels, 2 backgrounds, 3 layouts (order1, order2, overlay). 7 staged experiments. |
| `collected_andy1/` | Raw webcam capture sessions by Andy | 11 classes | 71 images across 6 sessions. Source data for brightness_experiment. |
| `collected_matthew/` | Raw webcam capture sessions by Matthew | 9 classes | 103 images across 7 sessions. Source data for spoon_lighting. |

Additionally, the **Lavado** dataset (`data/lavado/`) is a Kaggle dataset with 4 surgical instrument classes (scalpel, straight clamp, straight mayo scissor, curved mayo scissor), ~3000 single-instrument images on black background. Used as a clean supervised training baseline only — no classes overlap with surgical_kit_proxy, so cross-dataset evaluation is not meaningful.

---

## Experiment Status

### Completed (on remote server, results in `runs/detect/runs/`)

| Experiment | Dataset | Final mAP50 | Final mAP50-95 | Notes |
|---|---|---|---|---|
| Lavado baseline | `data/lavado` | 0.995 | 0.944 | Clean single-instrument baseline |
| Brightness: bright→dim | `brightness_experiment` | 0.995 | 0.995 | Spoon proxy — near-perfect, not meaningful |
| Brightness: dim→bright | `brightness_experiment` | 0.995 | — | Same spoon proxy limitation |
| Brightness: matte→reflective | `brightness_experiment` | 0.995 | 0.989 | Spoons, not instruments |
| Brightness: reflective→matte | `brightness_experiment` | 0.995 | 0.884 | Same |
| Brightness: separated→overlay | `brightness_experiment` | 0.995 | — | Same |
| Spoon: reference only | `spoon_lighting` | 0.995 | 0.901 | 7 training images only |
| Spoon: reference + 45/90 | `spoon_lighting` | 0.995 | 0.992 | 60 training images |
| **Phase 1 (100 epochs)** | | | | |
| KMS: matte→reflective | `surgical_kit_proxy` | 0.336 | 0.233 | Lighting transfer fails; only scissor2/forcep/scalpel survive |
| KMS: reflective→matte | `surgical_kit_proxy` | 0.160 | 0.119 | All classes 0.0 except scalpel (0.717) |
| KMS: shape similarity | `surgical_kit_proxy` | 0.300 | 0.253 | scissor1/4 work, scissor2/3/forcep at 0.0 |
| **Original: shape similarity** | `surgical_kit_proxy` | **0.373** | **0.241** | **Pre-Phase-1 baseline (50 epochs?)** |
| **Cancelled** | | | | |
| OOD lighting (Phase 3) | — | — | — | No held-out session collected |
| Synthetic data (Phase 4) | — | — | — | No 3D models of instruments |
| Synthetic-to-real (Phase 5) | — | — | — | Depends on Phase 4 |

### Key Finding

The brightness/spoon experiments achieved near-perfect scores (0.995 mAP) by solving an easy problem — separating visually distinct household items under controlled lighting. Real-instrument experiments (`surgical_kit_proxy`) max out at 0.160–0.336 mAP depending on the split.

**Position-cue confound**: Each image has exactly 6 instruments at fixed positions per session. Models learn layout rather than shape. Classes fail systematically — different classes survive in different splits — consistent with position-based memorization. The only class that works across splits is scalpel, which is visually distinct (single blade vs. multi-loop scissors).

---

## Scripts

### Core pipeline
| Script | Purpose |
|---|---|
| `scripts/train_surgical_kit.py` | Train all surgical_kit_proxy stages (lighting transfer + shape similarity) |
| `scripts/validate_surgical_kit.py` | Per-class AP50/AP50-95, confusion matrices, CSV/JSON output |
| `scripts/cross_dataset_eval.py` | Evaluate any model on any dataset's test split (handles mismatched classes) |
| `scripts/train_brightness_yolo.py` | Train 7 brightness experiment stages |
| `scripts/validate_brightness_experiments.py` | Full brightness validation pipeline with plots |
| `scripts/train_shape_similarity_yolo.py` | Train 4 shape-similarity stages (needs synthetic data) |
| `scripts/print_yolo_metrics.py` | Quick YOLO validation metrics printer |

### Data collection
| Script | Purpose |
|---|---|
| `scripts/collect_data.py` | Webcam capture with bounding box annotation |
| `scripts/collect_class_folder.py` | Rapid single-instrument capture |
| `scripts/export_collected_yolo.py` | Flatten sessions into YOLO format |
| `scripts/normalize_collected_labels.py` | Normalize class names to snake_case |
| `scripts/add_ood_lighting_to_tests.py` | Append OOD lighting session to test splits |
| `scripts/visualize_collected_session.py` | OpenCV session viewer with bounding boxes |

### Other
| Script | Purpose |
|---|---|
| `scripts/render_shape_similarity_blender.py` | BlenderProc synthetic renderer (needs Blender) |
| `scripts/plan_shape_similarity_synthetic.py` | Plan synthetic scene manifests |
| `scripts/evaluate_all.py` | Multi-variant benchmark runner |

---

## Phase 1: What to Run Next

The critical experiments use **real surgical instruments** (`surgical_kit_proxy`). All data is prepared.

```bash
# 1. Train all surgical kit stages (lighting + shape)
uv run python scripts/train_surgical_kit.py --epochs 100

# 2. Per-class validation with confusion matrices
uv run python scripts/validate_surgical_kit.py --output-dir reports/surgical_kit_validation
```

## Phase 1 Results (Complete)

All three stages trained for 100 epochs and validated on the held-out test split (not the val set used during training).

| Stage | mAP50 | mAP50-95 | P | R |
|---|---|---|---|---|
| matte→reflective | 0.336 | 0.233 | 0.425 | 0.236 |
| reflective→matte | 0.160 | 0.119 | 0.123 | 0.160 |
| shape_similarity | 0.300 | 0.253 | 0.239 | 0.347 |

### Per-Class Breakdown

| Class | matte→reflective | reflective→matte | shape_similarity |
|---|---|---|---|
| scissor1 | **0.000** | **0.000** | **0.862** |
| scissor2 | 0.435 | 0.000 | 0.000 |
| scissor3 | 0.000 | 0.000 | 0.000 |
| scissor4 | 0.000 | 0.000 | 0.587 |
| forcep | 0.517 | 0.000 | 0.000 |
| scalpel | 0.446 | **0.717** | 0.069 |

### Analysis: Position-Cue Hypothesis

The pattern is systematic and diagnostic. Each image contains exactly 6 objects (one per class) in consistent positions within a session. When train/test splits separate sessions, the model can learn which classes appear at which image locations rather than visual features:

- **matte→reflective**: scissor2, forcep, scalpel survive (3 of 6 classes at ~0.45-0.52 AP); scissor1/3/4 at 0.0. These surviving classes may share a common position that happens to be similar between the training and test sessions.

- **reflective→matte**: Only scalpel survives (0.717). Every other class at 0.0. The scalpel is visually the most distinct instrument (single blade vs. multi-loop scissors), so it's the only class the model actually learned by shape rather than position.

- **shape_similarity**: scissor1 (0.862) and scissor4 (0.587) survive; scissor2/3/forcep at 0.0. Again, classes fail in a session-specific pattern.

**Conclusion**: The lighting transfer experiments are confounded by position-cue leakage. The test metric reflects both the lighting transfer difficulty AND the layout generalization difficulty. To isolate lighting effects, instruments need randomized positions within each image.

---

## Scripts

### Core pipeline
| Script | Purpose |
|---|---|
| `scripts/train_surgical_kit.py` | Train all surgical_kit_proxy stages (lighting transfer + shape similarity) |
| `scripts/validate_surgical_kit.py` | Per-class AP50/AP50-95, confusion matrices, CSV/JSON output |
| `scripts/cross_dataset_eval.py` | Evaluate any model on any dataset's test split (handles mismatched classes) |
| `scripts/train_brightness_yolo.py` | Train 7 brightness experiment stages |
| `scripts/validate_brightness_experiments.py` | Full brightness validation pipeline with plots |
| `scripts/train_shape_similarity_yolo.py` | Train 4 shape-similarity stages (needs synthetic data, no 3D models available) |
| `scripts/print_yolo_metrics.py` | Quick YOLO validation metrics printer |

### Data collection
| Script | Purpose |
|---|---|
| `scripts/collect_data.py` | Webcam capture with bounding box annotation |
| `scripts/collect_class_folder.py` | Rapid single-instrument capture |
| `scripts/export_collected_yolo.py` | Flatten sessions into YOLO format |
| `scripts/normalize_collected_labels.py` | Normalize class names to snake_case |
| `scripts/add_ood_lighting_to_tests.py` | Append OOD lighting session to test splits (no OOD data available) |
| `scripts/visualize_collected_session.py` | OpenCV session viewer with bounding boxes |

### Other
| Script | Purpose |
|---|---|
| `scripts/render_shape_similarity_blender.py` | BlenderProc synthetic renderer (no 3D models available) |
| `scripts/plan_shape_similarity_synthetic.py` | Plan synthetic scene manifests (no 3D models available) |
| `scripts/evaluate_all.py` | Multi-variant benchmark runner |
