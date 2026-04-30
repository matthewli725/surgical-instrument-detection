# Experiments

This directory is the experiment map.

## Sections

- `cv/`: computer-vision technical risks and experiments
- `adoption/`: workflow fit, reporting, and sociotechnical risk
- `splits/`: split policies for each experiment axis
- `reproducibility/`: rerun instructions for benchmarked results

## Current Prototype Flow

TrayGuard is being tested as a technician-centered tray-checking assistant:

1. Load or enter the required tray list.
2. Capture the current tray view.
3. Detect and count visible instruments.
4. Show present, missing, extra, and review-needed items.
5. Preserve technician confirmation as the final decision.

This repository focuses on the evidence needed for that prototype claim:
camera capture, labeling, dataset export, model training, evaluation, review
states, and lightweight reporting.

## CV Experiment Map

| Axis | Doc | Local Question |
| --- | --- | --- |
| Similar-instrument recognition | [`cv/shape_similarity.md`](cv/shape_similarity.md) | Can the model separate visually similar classes without hiding pairwise confusion behind average metrics? |
| Reflective-object lighting robustness | [`cv/reflectivity_lighting.md`](cv/reflectivity_lighting.md) | Does lighting diversity improve detection on reflective proxy objects, and when should glare trigger review or rescan? |
| Crowded-tray clutter and occlusion | [`cv/clutter_occlusion.md`](cv/clutter_occlusion.md) | When do crowded tray scenes make visible-tool counts unreliable? |
| Unknown similar-object review routing | [`cv/open_set_confidence.md`](cv/open_set_confidence.md) | Can unknown or similar-but-wrong objects be routed to review instead of forced into known classes? |

The shared rationale for these axes lives in the system design's
[research support audit](../background/system_design.md#research-support-audit).
The individual pages should document only their local setup, metrics, results,
and product interpretation.

## Experiment Decision Evidence Index

The project already includes justification for the experiment directions in the
system design, especially the
[research support audit](../background/system_design.md#research-support-audit).
Use this table as the visible bridge between those sources and the concrete
experiment decisions.

| Decision | Evidence Link | What It Supports |
| --- | --- | --- |
| Run controlled experiments instead of claiming deployment readiness | [System scope](../background/system_design.md#current-focus), [Research support audit](../background/system_design.md#research-support-audit) | The prototype should test measurable assumptions under bounded conditions. |
| Use shape similarity as a primary CV axis | [Pairwise-confusion row](../background/system_design.md#research-support-audit), [HOSPITools source](../bibliography.md#rodrigues-et-al-2022b) | Surgical tools can be visually similar with subtle differences, so average metrics are not enough. |
| Report pairwise confusion and high-confidence wrong-class predictions | [Pairwise-confusion row](../background/system_design.md#research-support-audit), [`cv/shape_similarity.md`](cv/shape_similarity.md#headline-metrics) | Similar-class mistakes are the product-critical failure mode for fine-grained tray checks. |
| Use lighting and reflectivity stages | [Controlled-lighting row](../background/system_design.md#research-support-audit), [`cv/reflectivity_lighting.md`](cv/reflectivity_lighting.md#dataset) | Lighting is a documented acquisition variable for surgical-tool imagery and reflective objects can hide visual cues. |
| Reuse labels only for fixed-pose lighting variants | [Controlled-lighting row](../background/system_design.md#research-support-audit), [`cv/reflectivity_lighting.md`](cv/reflectivity_lighting.md#dataset) | Label reuse is defensible only when object geometry, identity, pose, and camera framing stay fixed. |
| Evaluate on held-out conditions instead of random near-duplicates | [Held-out-splits row](../background/system_design.md#research-support-audit), [`cv/reflectivity_lighting.md`](cv/reflectivity_lighting.md#dataset), [`cv/shape_similarity.md`](cv/shape_similarity.md#staged-experiment-logic) | The result should measure generalization to the isolated condition, not memorization of similar images. |
| Use synthetic data only as a transfer hypothesis | [Synthetic-data row](../background/system_design.md#research-support-audit), [`cv/shape_similarity.md`](cv/shape_similarity.md#dataset-design) | Simulation is useful only if it improves a matched real-proxy baseline. |
| Include clutter and occlusion as an axis | [Object-detection/counting row](../background/system_design.md#research-support-audit), [`cv/clutter_occlusion.md`](cv/clutter_occlusion.md#why-this-is-a-risk) | TrayGuard should count visible tools and know when overlap makes the view unreliable. |
| Include open-set confidence and review states | [Confidence/review row](../background/system_design.md#research-support-audit), [`cv/open_set_confidence.md`](cv/open_set_confidence.md#how-to-read-the-results) | Unknown or similar-but-wrong objects should route to review instead of being forced into known labels. |
| Keep technician confirmation as the final decision | [Technician-centered row](../background/system_design.md#research-support-audit), [Current prototype flow](#current-prototype-flow) | The detector supports human verification; it does not silently approve trays. |

## Adoption Experiment Map

| Axis | Doc | Local Question |
| --- | --- | --- |
| Workflow acceptance | [`adoption/workflow_acceptance.md`](adoption/workflow_acceptance.md) | Does the assistant help users catch tray issues without adding unacceptable correction burden? |
| Formal risk analysis | [`adoption/formal_risk_analysis.md`](adoption/formal_risk_analysis.md) | What system-level and CV-specific risks must stay visible during positioning and evaluation? |
| Traceability and reporting | [`adoption/traceability_reporting.md`](adoption/traceability_reporting.md) | Can the prototype produce useful evidence about repeated tray-check problems? |

## Reproducibility

- [`splits/README.md`](splits/README.md)
- [`reproducibility/brightness_yolo_reproducibility.md`](reproducibility/brightness_yolo_reproducibility.md)
- [`reproducibility/lighting_yolo_reproducibility.md`](reproducibility/lighting_yolo_reproducibility.md)
- [`reproducibility/shape_similarity_yolo_reproducibility.md`](reproducibility/shape_similarity_yolo_reproducibility.md)

The split README is the source of truth for experiment split intent. The
reproducibility notes keep command-level detail for benchmarked results.

## Shared Reporting Checklist

For each experiment axis, report the smallest set of results that supports the
claim:

- dataset size, class list, and split strategy
- precision, recall, mAP50, and mAP50-95 where applicable
- per-class failures and pairwise confusion for similar classes
- unknown-object false positives and high-confidence errors
- count error per tray or condition
- review, rescan, correction, and time-to-check behavior where relevant
- representative success and failure screenshots

The final claim should remain bounded: TrayGuard is testing whether the main
risks are measurable and manageable in a controlled prototype, not claiming
deployment readiness for real SPD operations.
