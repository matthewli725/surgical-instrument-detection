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

Additionally, the **Lavado** dataset (`data/lavado/`) is available from Kaggle — 4 surgical instrument classes (scalpel, straight clamp, straight mayo scissor, curved mayo scissor), ~3000 single-instrument images on black background. Clean supervised training set for cross-dataset evaluation.

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
| **KMS: shape similarity** | `surgical_kit_proxy` | **0.373** | **0.241** | **Only real-instrument test — failed** |

### Key Finding

The brightness/spoon experiments achieved near-perfect scores (0.995 mAP) by solving an easy problem — separating visually distinct household items under controlled lighting. The single real-instrument experiment (`surgical_kit_proxy`) reached only **0.373 mAP**, revealing the actual difficulty: distinguishing similar metallic instruments with subtle shape differences, especially under lighting variation.

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

# 3. Cross-dataset: Lavado model → surgical kit test
uv run python scripts/cross_dataset_eval.py \
    --model runs/detect/runs/yolo11s_lavado/weights/best.pt \
    --data data/cv/surgical_kit_proxy/shape_similarity_real_proxy/data.yaml

# 4. Cross-dataset: surgical kit model → Lavado test
uv run python scripts/cross_dataset_eval.py \
    --model weights/surgical_kit_shape_similarity_real_proxy.pt \
    --data data/lavado/data.yaml

# 5. Spoon lighting stages (existing data)
uv run python scripts/train_brightness_yolo.py \
    --datasets-dir data/cv/spoon_lighting \
    --stage reference_only reference_plus_45 reference_plus_45_90
```

After Phase 1, the key numbers will be:
- Can KMS models beat 0.373 mAP with full 100-epoch training?
- Which instrument classes are hardest (per-class AP)?
- Does Lavado pretraining transfer to multi-instrument scenes?
