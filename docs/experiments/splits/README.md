# Experiment Splits

This README records the split logic for each experiment axis. The project no
longer keeps one-off YOLO export scripts for each setup because those scripts
encoded temporary folder names and capture assumptions in code.

Use the generic exporter only when a source folder already has the collected
session shape expected by the tool:

```bash
uv run trayguard export-yolo \
  --input-dir data/<source_root> \
  --output-dir data/<yolo_root> \
  --overwrite
```

Experiment-specific split decisions should live in source manifests, staged
folders, or notes like this file. Each exported YOLO stage should still keep a
`manifests/` folder with the sample rows used for train, validation, and test.

## Generic YOLO Contract

The generic collected-data exporter expects:

```text
data/<source_root>/
  sessions/
    <session_id>/
      metadata.json
      images/
      labels/
```

It performs a session-level train/val/test split. That is appropriate for a
plain collected dataset where sessions are the unit of independence. It is not
enough by itself for staged experiments where the held-out variable is lighting,
background, layout, physical instance, synthetic condition, or open-set role.

For staged experiments, prepare stage-specific source folders or manifests
first, then export each stage with the generic tool if YOLO layout is needed.

## Controlled Brightness And Background Transfer

Source family:

```text
data/collected_andy1/sessions/
```

Session naming contract:

| Session Name Part | Meaning |
| --- | --- |
| `matte` / `reflective` | Background domain |
| `order1` / `order2` | Separated layout |
| `overlay` | Overlapping layout |
| `variant_0001 ... variant_0011` | Brightness ladder from brightest to dimmest |

Known data limitation:

- `matte-background-order1` is missing `variant_0011`.

Recommended experiments:

| Experiment Name | Stage ID | Train | Test | What It Isolates |
| --- | --- | --- | --- | --- |
| Bright-to-dim lighting degradation | `brightest_train_darker_test` | separated layouts, brightness rank 1 | separated layouts, ranks 2-11 | How quickly recall falls as light drops from a bright anchor |
| Dark-to-bright lighting recovery | `darkest_train_brighter_test` | separated layouts, darkest available rank | separated layouts, brighter ranks | Whether a model trained on the hardest dark view recovers under better light |
| Bright-half to dim-half transfer | `bright_train_dim_test` | separated layouts, ranks 1-6 | separated layouts, ranks 7-11 | Coarse transfer from brighter captures to dimmer captures |
| Dim-half to bright-half transfer | `dim_train_bright_test` | separated layouts, ranks 7-11 | separated layouts, ranks 1-6 | Coarse transfer from dimmer captures to brighter captures |
| Matte-to-reflective background transfer | `matte_train_reflective_test` | matte, separated layouts, all ranks | reflective, separated layouts, all ranks | Whether the detector overfits to a matte background |
| Reflective-to-matte background transfer | `reflective_train_matte_test` | reflective, separated layouts, all ranks | matte, separated layouts, all ranks | Whether training on glare-prone backgrounds transfers back to matte |
| Separated-to-overlapping layout stress | `separated_train_overlay_test` | order1/order2, all backgrounds, all ranks | overlay, all backgrounds, all ranks | Detection and count quality under overlap |

Validation policy:

- With tiny controlled stages, validation may be a copy of train for training
  mechanics only.
- Use test metrics for the claim because the test split holds out the
  experiment variable.

## Reflective Spoon Lighting Robustness

Source family:

```text
data/spoon_lighting_yolo/
```

This dataset already exists as staged YOLO folders. The split variable is
lighting condition while object identity and pose stay fixed enough for label
reuse.

Recommended experiments:

| Experiment Name | Stage ID | Train | Test | What It Isolates |
| --- | --- | --- | --- | --- |
| Single-lighting baseline | `reference_only` | reference condition only | all non-reference lighting conditions | Generalization from one clean lighting condition |
| Moderate directional-lighting training | `reference_plus_45` | reference plus 45 degree flashlight conditions | remaining lighting conditions | Benefit from adding moderate angled lighting |
| Broad directional-lighting training | `reference_plus_45_90` | reference plus 45 and 90 degree flashlight conditions | remaining non-training conditions | Benefit from broader harsh-light coverage |

Label reuse rule:

- Reuse labels only when object identity, pose, and camera framing are fixed.
- Redraw or check labels when pose, position, occlusion, or object identity
  changes.

## Amazon Surgical-Kit Similar-Instrument Proxy

Source family:

```text
data/kms/
```

Focused class list:

| ID | Class |
| ---: | --- |
| 0 | `scissor1` |
| 1 | `scissor2` |
| 2 | `scissor3` |
| 3 | `scissor4` |
| 4 | `forcep` |
| 5 | `scalpel` |

Background mapping for the current capture set:

| Session | Background |
| --- | --- |
| `setup_20260427_212432` | matte |
| `setup_20260427_212940` | matte |
| `setup_20260427_213455` | reflective |
| `setup_20260427_213819` | reflective |

Recommended similar-instrument split:

| Split Unit | Policy | Why |
| --- | --- | --- |
| Session | Hold out entire setup sessions | Avoid testing on near-identical lighting variants from the same setup |
| Class labels | Remap to the focused six-class list | Remove stale spoon/knife class IDs from the capture metadata |
| Lighting variants | Either all variants or a representative subset | Use all for more training examples; use representative variants to reduce near-duplicates |

Recommended Amazon-kit background-transfer experiments:

| Experiment Name | Stage ID | Train | Test | What It Isolates |
| --- | --- | --- | --- | --- |
| Amazon-kit matte-to-reflective transfer | `amazon_kit_matte_train_reflective_test` | matte Amazon-kit sessions, all fixed-pose variants | reflective Amazon-kit sessions, all fixed-pose variants | Transfer from matte to reflective background with similar metal instruments |
| Amazon-kit reflective-to-matte transfer | `amazon_kit_reflective_train_matte_test` | reflective Amazon-kit sessions, all fixed-pose variants | matte Amazon-kit sessions, all fixed-pose variants | Reverse background transfer with similar metal instruments |

This dataset is useful evidence for similar-instrument and background-transfer
stress, but it is too small to support broad surgical-instrument readiness
claims by itself.

## Similar-Instrument Synthetic-To-Real Transfer

Source families:

```text
data/shape_similarity_source/
data/shape_similarity_real_source/
```

The split contract belongs in `samples.csv`, not in an exporter. Each row should
carry explicit stage split columns so the held-out condition is visible.

Required split columns:

| Column | Meaning |
| --- | --- |
| `stage_seen_split` | Train/val/test assignment for synthetic seen-condition interpolation |
| `stage_heldout_split` | Assignment for held-out synthetic lighting/material/background/camera conditions |
| `transfer_pretrain_split` | Synthetic pretraining source assignment |
| `transfer_real_split` | Small real-proxy assignment used by both transfer branches |

Recommended experiments:

| Experiment Name | Stage ID | Train | Test | What It Proves |
| --- | --- | --- | --- | --- |
| Synthetic same-condition interpolation | `synthetic_seen_condition` | synthetic seen condition | held-out synthetic scenes from the same condition family | Interpolation inside the simulator |
| Synthetic held-condition robustness | `synthetic_heldout_condition` | one synthetic condition subset | held-out lighting/material/background/camera buckets | Robustness beyond one render setup |
| Small real-proxy baseline | `real_small_from_scratch` | small real-proxy train split | same real-proxy test split | Baseline real-data performance |
| Synthetic-pretrained real-proxy transfer | `synthetic_pretrain_plus_real_small` | synthetic pretraining, then small real-proxy train split | same real-proxy test split | Whether synthetic pretraining reduces real-data needs |

Real-proxy split preference:

1. Hold out physical instances when possible.
2. If only one instance exists per class, hold out sessions or capture
   conditions and mark the evidence as weaker.
3. Do not mix near-duplicate variants from one fixed setup across train and
   test unless the claim is explicitly about interpolation.

## Unknown Similar-Object Review Routing

The unknown-object experiment should keep unknown or similar-but-wrong objects
out of known-class training labels.

Recommended split fields:

| Field | Values | Purpose |
| --- | --- | --- |
| `open_set_role` | `known`, `unknown_similar_distractor` | Separates trainable known classes from review-only distractors |
| `pair_family` | e.g. `scissors_curve`, `clamp_like` | Groups confusable objects for pairwise error reporting |
| `split` | `train`, `val`, `test` | Keeps unknown distractors in validation/test unless explicitly training rejection behavior |

Main test readout:

- unknown false-positive rate
- high-confidence known-label predictions on unknown distractors
- review-threshold behavior

## Crowded-Tray Clutter And Occlusion

The clutter split should hold out layout, not random images.

Recommended experiments:

| Experiment Name | Stage ID | Train | Test | What It Isolates |
| --- | --- | --- | --- | --- |
| Separated-to-overlapping tray layout | `separated_train_overlay_test` | separated layout sessions | overlay/crowded sessions | Effect of overlap on detection and count quality |
| Light-to-heavy tray clutter | `light_clutter_train_heavy_clutter_test` | sparse or lightly cluttered scenes | crowded or occluded scenes | Generalization as tray density increases |

Count metrics matter here as much as detector metrics. Report per-image count
error, missed visible tools, extra detections, and representative failure
screenshots.
