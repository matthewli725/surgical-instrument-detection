# Open-Set Recognition & Confidence Experiment Plan

## Objective

Evaluate whether TrayGuard can identify when an object is outside the trained class list. This includes ambiguous objects and objects that are too visually degraded for safe automatic confirmation. This experiment targets a major hospital adoption risk. Wrong instruments, missing instruments, wrong specifications, broken instruments, and bioburden are documented error categories. A system that confidently makes the wrong call is worse than a system that asks for human review (Zhu et al., 2019, Nichol et al., 2024, Chen et al., 2023).

## Core Question

> Does the model know when it does not know?

## Why This Matters

Sterile processing errors often involve missing, wrong, broken, or contaminated instruments. Direct-observation research frames identification, function, and bioburden inspection as visualization-heavy weak points (Nichol et al., 2024). A tray-checking assistant should not force every visible object into the closest known class. Tray inventories can include many manufacturers and worn or missing identification markings (Rubak et al., 2024). If TrayGuard cannot represent uncertainty, technicians and hospital leaders will have a clear reason to distrust it (Natarus et al., 2025).

## Experimental Design Overview

Train on known classes and test on both known and intentionally unknown objects.

### Known Classes

Use the current prototype classes where possible.

- Scalpel n4
- Straight Dissection Clamp
- Straight Mayo Scissor
- Curved Mayo Scissor

### Unknown / Distractor Classes

Choose objects that are plausible confusions.

- Similar scissors not included in training
- Similar clamps or pliers
- Tweezers or forceps-like tools
- Pens, craft knives, kitchen tongs, or metal utensils
- Damaged or partially covered versions of known tools

The unknowns should be visually close enough that rejection is meaningful.

## Data Collection Plan

### Fixed Setup

- Same camera position
- Same tray-like area
- Same lighting as the baseline shape experiment
- Balanced known and unknown object scenes

### Capture Targets

- 20-30 known-class images per class
- 40-80 unknown-object images
- 20-40 mixed scenes containing both known and unknown objects

If time is tight, prioritize mixed scenes because they best match the workflow risk.

## Procedure

1. Train a detector on known classes only.
2. Collect test images with unknown objects that were never included in training.
3. Run inference at multiple confidence thresholds.
4. Record when unknowns are mislabeled as known instruments.
5. Add a "needs review" rule based on low confidence, overlapping detections, or disagreement across augmentations.
6. Compare raw model predictions against the review rule.

## Evaluation Metrics

Track these metrics.

- Known-class precision and recall
- Unknown false positive rate
- High-confidence unknown false positive rate
- Low-confidence review rate
- False confirmation rate after thresholding
- Percentage of real known instruments sent to review

## Required Analysis

### Unknown Rejection

| Unknown Object Type | Images | Mislabeled as Known | High-Confidence Mislabeled | Notes |
| --- | --- | --- | --- | --- |
| Similar scissor | | | | |
| Similar clamp / plier | | | | |
| Long narrow distractor | | | | |
| Mixed tray scene | | | | |

### Threshold Tradeoff

| Confidence Threshold | Known Recall | Unknown False Positives | Review Rate | Notes |
| --- | --- | --- | --- | --- |
| 0.25 | | | | |
| 0.50 | | | | |
| 0.75 | | | | |

### Failure Modes

| Failure Mode | Example | Risk | Possible Mitigation |
| --- | --- | --- | --- |
| Unknown confidently labeled as known | | Wrong tray confirmation | Add review threshold or unknown class |
| Known object sent to review too often | | Workflow slowdown | Improve training diversity |
| Occluded known object labeled as wrong class | | False completion or false missing item | Combine with occlusion warning |

## What Counts as Success

- Unknown objects are usually rejected or sent to review.
- High-confidence wrong labels are rare and documented.
- The chosen threshold reduces dangerous false confirmations without making every tray require manual review.
- The UI can explain uncertainty in plain language, such as "needs review" instead of "model confidence = 0.43."

## What Not To Do

- Do not test only random unrelated objects that are visually easy to reject.
- Do not report only mAP on known classes.
- Do not choose a threshold based only on accuracy. Include workflow review burden.
- Do not claim the system is safe because it can detect four known classes.

## Key Takeaways Expected

At the end, we should be able to answer these questions.

1. How often does TrayGuard mislabel unknown objects?
2. Are the wrong labels high confidence or low confidence?
3. What threshold creates a reasonable review workflow?
4. Can the UI turn model uncertainty into technician action?

## Guiding Principle

> A safe assistant must be allowed to say "I am not sure."

## References

- Chen et al., ["Incidence of Adverse Events in Central Sterile Supply Department: A Single-Center Retrospective Study"](https://doi.org/10.2147/RMHP.S423108), Risk Management and Healthcare Policy, 2023.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
- Rubak et al., ["Surgical instrument tray optimization process at a university hospital: A comprehensive overview"](https://doi.org/10.1016/j.sopen.2024.09.007), Surgery Open Science, 2024.
- Zhu et al., ["Errors in packaging surgical instruments based on a surgical instrument tracking system: an observational study"](https://link.springer.com/article/10.1186/s12913-019-4007-3), BMC Health Services Research, 2019.
