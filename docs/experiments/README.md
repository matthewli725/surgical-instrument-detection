# Experiments

Experiment docs are grouped by purpose so results and open questions can be
revised without rewriting the whole project background.

## Sections

- `cv/`: computer-vision technical risks and experiments
- `adoption/`: workflow fit, reporting, and sociotechnical risk
- `reproducibility/`: rerun instructions for benchmarked results

## CV

- `cv/shape_similarity.md`
- `cv/reflectivity_lighting.md`
- `cv/clutter_occlusion.md`
- `cv/open_set_confidence.md`

## Adoption

- `adoption/workflow_acceptance.md`
- `adoption/formal_risk_analysis.md`
- `adoption/traceability_reporting.md`

## Reproducibility

- `reproducibility/brightness_yolo_reproducibility.md`
- `reproducibility/lighting_yolo_reproducibility.md`

## Experiment Overview

TrayGuard is intended to become an interactive tray-checking system.

1. A technician loads the required instrument list for a tray by scanning a
   barcode.
2. A camera captures the current tray state.
3. The detector identifies and counts visible instruments.
4. The interface shows collected tools, missing tools, and uncertain
   detections.
5. The technician confirms or corrects the result before the tray is
   completed.

The current repository focuses on the computer vision foundation. This includes
data collection, labeling, dataset export, model training, and model
evaluation.

### 1. Shape Similarity

**Question** Can the model distinguish between objects that have similar
outlines but different identities?

This tests a central recognition challenge in surgical tray assembly. Packaging
studies show that wrong-specification instruments are a common error category.
Visualization studies identify identification and sorting as weak points in
sterile processing
([Zhu et al., 2019](../bibliography.md#zhu-et-al-2019),
[Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023),
[Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). The system
therefore needs to learn subtle differences in shape, tip geometry, handle
structure, and relative proportions
([Zhu et al., 2019](../bibliography.md#zhu-et-al-2019),
[Fayad et al., 2025](../bibliography.md#fayad-et-al-2025)).

**Proposed setup**

- Collect images of visually similar tools.
- Keep lighting and background mostly stable.
- Train the detector on multiple shape classes.
- Evaluate whether the model confuses similarly shaped objects.

**Success indicators**

- High per-class precision and recall for visually similar classes
- Low confusion between paired classes, such as straight vs. curved instruments
- Reasonable detection confidence when objects are rotated or slightly
  repositioned

### 2. Material And Lighting Robustness

**Question** Can the model remain reliable when reflective or metallic objects
appear under different lighting conditions?

Surgical instruments are commonly reusable metal tools. Sterile-processing
studies emphasize inspection of instrument condition, cleanliness, and function
as visual tasks. This motivates testing whether lighting and reflective
surfaces degrade a camera-based detector
([Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023),
[Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)). Our data
collection workflow is designed around this issue. One setup can be annotated
once and then captured repeatedly under different lighting conditions.

**Proposed setup**

- Place a fixed set of objects in a tray or tray-like area.
- Capture one annotated reference image.
- Capture lighting variants with changed light angle, brightness, glare, and
  shadow.
- Train and evaluate on lighting conditions not seen during training.

**Success indicators**

- Stable detections across lighting variants
- Limited confidence drop under glare or shadow
- Better performance when lighting augmentation or multi-lighting training data
  is used

### 3. Clutter And Occlusion

**Question** Can the model detect and count instruments when objects are close
together, overlapping, or partially occluded?

Real trays can be large and visually dense. A Major General Surgery tray in one
prospective study contained 94 reusable instruments. Hospital-wide tray
optimization at Aarhus University Hospital involved 1,340 tray types and more
than 43,000 instruments before redesign
([Eussen et al., 2026](../bibliography.md#eussen-et-al-2026),
[Rubak et al., 2024](../bibliography.md#rubak-et-al-2024)). A useful tray
inspection system must measure how touching, overlap, and occlusion affect
visible-tool counting
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)).

**Proposed setup**

- Create tray scenes with increasing clutter levels.
- Start with separated objects, then move to touching objects, partial overlap,
  and heavier occlusion.
- Evaluate detection quality at each clutter level.

**Success indicators**

- Accurate counts in low and moderate clutter
- Graceful degradation as occlusion increases
- Clear failure cases where the system can flag low confidence instead of
  silently miscounting

### 4. Open-Set Recognition And Confidence Calibration

**Question** Does the system know when it does not know?

Hospitals will not trust a tray-check system that confidently mislabels an
unfamiliar instrument because wrong instruments, wrong specifications, and
missing instruments are documented sterile-processing error categories
([Zhu et al., 2019](../bibliography.md#zhu-et-al-2019),
[Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). This experiment
tests whether TrayGuard can reject unknown tools, flag low-confidence cases,
and avoid forcing every object into one of the known classes.

**Proposed setup**

- Train on the known prototype classes.
- Test on visually similar but intentionally unknown tools.
- Compare true known-class detections against unknown-object false positives.
- Evaluate whether confidence thresholds and "needs review" states catch risky
  predictions.

**Success indicators**

- Unknown tools are rejected or flagged rather than confidently mislabeled.
- Confidence is lower on ambiguous, occluded, or glare-heavy cases.
- A practical threshold can reduce dangerous false confirmations while keeping
  the UI usable.

### 5. Workflow Acceptance And Throughput

**Question** Would a technician actually want to use the system during tray
assembly?

This addresses the UCLA anecdote directly. Published implementation research
supports the same concern. SPD improvement work identifies staffing, training,
inventory management, physical environment, workflow, communication, and
governance as drivers of tray defects
([Natarus et al., 2025](../bibliography.md#natarus-et-al-2025)). A model
should therefore be evaluated as a technician-facing support tool. Adoption
should also account for the specialized training and visual-inspection skills
required of sterile-processing professionals
([Hu et al., 2024](../bibliography.md#hu-et-al-2024),
[Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)).

**Proposed setup**

- Simulate a tray assembly checklist with and without TrayGuard.
- Measure task time, number of manual corrections, number of rescans, and
  perceived workload.
- Record where users hesitate, override the model, or ask for more
  explanation.
- Compare "assistant mode" against "automation mode" language in the UI.

**Success indicators**

- The UI reduces missed items without adding unacceptable time.
- Users understand uncertain detections and can correct them quickly.
- The system preserves human confirmation rather than pretending to replace the
  technician.

### 6. Traceability And Quality Reporting

**Question** Can the system produce evidence that matters to a hospital buyer?

Hospitals may underreport tray defects. Nichol et al. found that staff
reporting captured far fewer cases than direct observation. Incomplete
reporting also limited delay analysis
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). TrayGuard
should therefore log detections, uncertain items, corrections, missing
instruments, and recurring failure patterns.

**Proposed setup**

- Save per-tray detection results, manual corrections, confidence values, and
  missing-item lists.
- Group errors by class, lighting condition, clutter level, and tray setup.
- Produce a simple quality report that shows repeatable patterns instead of
  isolated screenshots.

**Success indicators**

- Each tray check has an auditable record.
- Repeated model or workflow failure modes are visible.
- The output can support a buyer-facing argument about risk reduction,
  technician support, and process improvement.

## Evaluation Plan

For each experiment axis, we plan to report these results.

- Dataset size and class list
- Train, validation, and test split strategy
- Mean average precision or other detector metrics
- Per-class precision and recall
- Confusion between similar classes
- Example successes and failures
- Qualitative screenshots of detections
- Unknown-object rejection rate
- Confidence calibration and low-confidence review rate
- Count error per tray
- Time-to-check and number of user corrections in the UI
- Repeated error categories suitable for quality reporting

The strongest final result would not be a claim that TrayGuard is ready for
operating-room deployment. Instead, it would show that the main risks are
testable, that the prototype works under controlled approximations of those
risks, and that the same pipeline could scale to real surgical instruments once
real data is available.
