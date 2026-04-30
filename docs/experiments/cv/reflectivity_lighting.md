# Lighting Robustness

TrayGuard needs to work when metal tools reflect light, cast shadows, or create
glare. This page explains what we tested and how to interpret the results.

## What This Test Answers

Lighting can make the same tray look very different to a camera. A tool may be
easy to detect under soft light and harder to detect when a bright reflection
covers part of the object.

## Why This Is A Risk

Shiny metal can change appearance when the light or camera angle changes.
Specular highlights may hide edges, texture, or shape evidence that the detector
needs. The longer source-backed rationale for lighting, controlled capture, and
label reuse lives in the system design's
[research support audit](../../background/system_design.md#research-support-audit).
HOSPITools also treats illumination as a real surgical-tool dataset variable:
its dataset included natural light, LED, halogen, and fluorescent lighting
([Rodrigues et al., 2022b](../../bibliography.md#rodrigues-et-al-2022b)).

This test answers:

- Does performance drop when lighting changes?
- Does adding more lighting variety during training improve the result?
- When should the product ask the user to reduce glare and scan again?

## Dataset

We used spoon images as reflective proxy objects. Spoons are not surgical
instruments, but they are useful for testing glare because they have shiny metal
surfaces.

The data is organized into three training stages:

| Dataset | What The Model Saw During Training |
| --- | --- |
| `reference_only` | Reference lighting only |
| `reference_plus_45` | Reference lighting plus 45 degree flashlight views |
| `reference_plus_45_90` | Reference lighting plus 45 and 90 degree flashlight views |

Each stage is evaluated on lighting conditions that were not included in that
stage's training set. This is more useful than a random split because it tests
whether the model handles new lighting, not whether it memorized similar images.
The evidence link for this decision is the system design's
[held-out-splits row](../../background/system_design.md#research-support-audit).

Reference labels are reused only when object geometry and camera framing stay
fixed and lighting changes. If pose, position, occlusion, or object identity
changes, labels should be checked or redrawn.
The evidence link for this decision is the system design's
[controlled-lighting row](../../background/system_design.md#research-support-audit).

## How To Read The Results

Use precision, recall, mAP50, and mAP50-95 together.

- Precision: when TrayGuard detects a tool, how often is it right?
- Recall: how often does TrayGuard find the tools that are actually present?
- mAP50: general detection quality with a forgiving box-overlap threshold.
- mAP50-95: stricter detection quality across multiple box-overlap thresholds.

For this experiment, recall matters a lot because missed instruments can create
false confidence that a tray is complete.

## Results

| Dataset | Class | Images | Instances | Precision | Recall | mAP50 | mAP50-95 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `reference_only` | spoon1 | 97 | 97 | 0.890 | 0.938 | 0.967 | 0.840 |
| `reference_only` | spoon2 | 97 | 97 | 1.000 | 0.944 | 0.991 | 0.863 |
| `reference_only` | spoon3 | 97 | 97 | 0.950 | 0.982 | 0.993 | 0.804 |
| `reference_plus_45` | spoon1 | 73 | 73 | 0.983 | 0.986 | 0.994 | 0.917 |
| `reference_plus_45` | spoon2 | 73 | 73 | 1.000 | 0.983 | 0.994 | 0.965 |
| `reference_plus_45` | spoon3 | 73 | 73 | 0.996 | 1.000 | 0.995 | 0.953 |
| `reference_plus_45_90` | spoon1 | 49 | 49 | 0.999 | 1.000 | 0.995 | 0.902 |
| `reference_plus_45_90` | spoon2 | 49 | 49 | 0.999 | 1.000 | 0.995 | 0.972 |
| `reference_plus_45_90` | spoon3 | 49 | 49 | 0.999 | 1.000 | 0.995 | 0.980 |

## Interpretation

Adding lighting variety improved the results. The model trained only on the
reference condition still performed well, but the models trained with additional
45 degree and 90 degree lighting were more stable across the held-out lighting
conditions.

The practical takeaway is simple: TrayGuard should not rely on one clean camera
setup. The training data should include realistic lighting variation, especially
glare and hard shadows.

## Product Implications

| Observation | What It Means | Product Response |
| --- | --- | --- |
| Performance improves with lighting diversity | Lighting variation belongs in training data | Keep collecting examples under different lighting |
| Glare can still obscure object shape | Some images are not safe for automatic confirmation | Ask users to reduce glare and rescan |
| Low confidence under harsh light is safer than confident mistakes | Uncertainty should be visible to the user | Use review or rescan language instead of silent failure |

## What We Are Not Claiming

- Spoon data does not prove surgical-instrument readiness.
- This experiment does not measure sterility, cleanliness, sharpness, or tool
  function.
- We are not using a dedicated specularity measurement pipeline right now.

## Note On Specularity Pixels

There are research methods for estimating highlights and separating diffuse from
specular reflection, but this project does not currently implement a validated
specularity-pixel algorithm. Simple saturated-pixel counts or brightness
thresholds would be custom heuristics, not a reliable product metric.

## Bibliography

See the [central bibliography](../../bibliography.md) for full source details.
