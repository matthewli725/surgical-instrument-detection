# TODO: Generate CV Experiment Data for FDR Section 6.2.1

Current Section 6.2.1 uses placeholder numbers that need to be replaced with actual results.

## Experiment 1: Brightness Robustness (7 stages)

**Location:** `data/cv/brightness_yolo/` — all 7 staged YOLO datasets exist.
**Weights:** need to be trained.
**Current paper claim to replace:** "mAP50-95 decayed from approximately 0.85–0.90 to below 0.50 (separated), below 0.30 (overlay)"

### Pipeline

```bash
# 1. Train all 7 brightness models (takes ~1-2 hours)
uv run python scripts/train_brightness_yolo.py

# This trains: brightest_train_darker_test, darkest_train_brighter_test,
#   bright_train_dim_test, dim_train_bright_test, matte_train_reflective_test,
#   reflective_train_matte_test, separated_train_overlay_test

# 2. Validate and generate metrics + plots
uv run python scripts/validate_brightness_experiments.py

# Outputs to reports/brightness_validation/:
#   stage_metrics.csv       — mAP50, mAP50-95, precision, recall per stage
#   grouped_metrics.csv     — aggregated by brightness rank, background, layout
#   brightness_map_metrics.csv — per-brightness metrics with estimated lumens
#   plots/                  — key PNG figures
```

### Key numbers to extract
- For `brightest_train_darker_test`: mAP50-95 at each brightness rank (800→80 lumens) → shows decay curve
- For `separated_train_overlay_test`: compare mAP50-95 vs separated → shows overlay penalty
- Also extract: recall decay, precision decay

---

## Experiment 2: Shape Similarity Confusion

**Location:** `data/cv/kms_yolo/shape_similarity_real_proxy/` — single YOLO dataset.
**Scripts expect:** `data/shape_similarity_yolo/` with 4 stage subdirectories (`synthetic_seen_condition`, `synthetic_heldout_condition`, `real_small_from_scratch`, `synthetic_pretrain_plus_real_small`).
**Status:** Only the real proxy data exists. The synthetic Blender pipeline was never executed, so `synthetic_seen_condition` and `synthetic_heldout_condition` do not exist.

### Option A: Run with real proxy only (pragmatic)
```bash
# The real proxy data at data/cv/kms_yolo/shape_similarity_real_proxy/
# needs to be split into the expected stage structure, or the scripts modified.
# Simplest path: symlink or copy to data/shape_similarity_yolo/real_small_from_scratch/
# then train + validate just that stage.
```

### Option B: Generate synthetic data first, then run full pipeline
```bash
# 1. Fill in blender_assets.template.json with mesh paths
# 2. Plan and render synthetic scenes (requires Blender)
uv run python scripts/plan_shape_similarity_synthetic.py \
  --assets-config config/shape_similarity/blender_assets.template.json \
  --output-dir data/shape_similarity_source
blenderproc run scripts/render_shape_similarity_blender.py \
  --scene-plan data/shape_similarity_source/manifests/scene_plan.jsonl

# 3. The real proxy data is separate:
#    data/cv/kms_yolo/shape_similarity_real_proxy/

# 4. Train + validate
uv run python scripts/train_shape_similarity_yolo.py
uv run python scripts/validate_shape_similarity_experiments.py
```

### Key numbers to extract
- Per-class precision/recall for similar-shape pairs
- Pairwise confusion rates (e.g., straight vs curved scissors)
- Wrong-similar-class prediction counts
- High-confidence wrong predictions

---

## Experiment 3: Synthetic-to-Real Transfer Gain

**Current paper claim to replace:** "pretraining on synthetic data improved mAP50 by roughly 5–10 percentage points"

**Status:** Depends on Experiment 2 (needs both synthetic + real data). The validation script (`validate_shape_similarity_experiments.py`) produces `transfer_comparison.csv` with `map50_delta` and `map50_95_delta` between `synthetic_pretrain_plus_real_small` vs `real_small_from_scratch`.

---

## Experiment 4: Open-Set False Positive Rate

**Current paper claim to replace:** "open-set false-positive rates of 40–60%"

**Status:** Plan only (`docs/experiments/cv/open_set_confidence.md`). No data was ever collected. The `validate_shape_similarity_experiments.py` script does compute `unknown_false_positive_rate` from distractor/unknown images in the test set, so if the shape similarity data includes unknown-class distractor images, this could be extracted there.

---

## Baseline Benchmark (already exists)

Clean-dataset results from `benchmark_results.json` (committed in git):
```json
yolo11s_imgsz640: mAP50=0.986, mAP50-95=0.928
yolo11m_imgsz640: mAP50=0.991, mAP50-95=0.940
yolo11l_imgsz640: mAP50=0.988, mAP50-95=0.932
```
These are from the FGVC/HOSPITools multi-class benchmark — useful as an upper-bound comparison for the degradation experiments.

---

## Estimated Time

| Experiment | Data Ready? | Train Time | Val Time | Total |
|---|---|---|---|---|
| Brightness (7 stages) | Yes | ~1-2 h | ~30 min | ~2 h |
| Shape similarity real proxy | Partial | ~30 min | ~15 min | ~45 min |
| Shape similarity synthetic | No (needs Blender setup) | ~1 h | ~15 min | ~2-3 h |
| Open-set | No | — | — | New experiment needed |

## What to update in the FDR after generating data

- **Section 6.2.1**: Replace all placeholder numbers with actual metrics from CSVs
- **Section 13.4**: Update Completed Work items with actual quantitative outcomes
- **Section 8.2**: The "why revised" subsection references CV experiment findings
