# Traceability & Quality Reporting Experiment Plan

## Objective

Evaluate whether TrayGuard can produce useful evidence for recurring tray-check failures. One-off detections are not enough. This experiment targets a hospital buyer's need for auditability, quality improvement, and ROI evidence. Staff-reported instrument-error systems can underreport events and omit delay information. Structured SPD improvement work depends on measurable defect and process metrics (Nichol et al., 2024, Natarus et al., 2025).

## Core Question

> Can TrayGuard turn visual checks into a quality record that helps explain and reduce errors?

## Why This Matters

Sterile processing quality issues can be underreported. Staff reporting may be incomplete and delayed. This makes it hard to estimate the operational cost of instrument errors (Nichol et al., 2024). If a system only displays detections and then forgets them, it does not help managers understand recurring risks. A practical hospital system should create a lightweight record of missing items, uncertain detections, manual corrections, and repeated failure patterns. This matches quality-improvement approaches that track first-pass yield, tray defect rate, and root-cause categories (Natarus et al., 2025).

## Experimental Design Overview

Use outputs from the other experiments and the Streamlit tray-check UI to create a mock quality report.

### Data To Log

- Timestamp or trial ID
- Tray setup or required class list
- Predicted instruments and counts
- Confidence per detection
- Missing required instruments
- Extra or unknown objects
- User corrections
- Image filename or screenshot reference
- Lighting, clutter, and experiment condition tags

## Procedure

1. Run a set of simulated tray checks across known conditions.
2. Save predictions and user corrections for each trial.
3. Categorize each issue as missing, wrong class, extra/unknown, duplicate count, low confidence, or visibility problem.
4. Generate a simple report with summary tables and representative examples.
5. Review whether the report answers a buyer's likely questions.

## Buyer Questions To Answer

- Which instruments are most often missed or confused?
- Which conditions cause the most failures?
- Are errors mostly model mistakes, visibility problems, or user corrections?
- How often does the system ask for review?
- Does the system provide an audit trail for tray completion?
- What additional data would be needed before a hospital pilot?

## Evaluation Metrics

Track these metrics.

- Trials completed
- Missing-item detections
- Extra / unknown objects flagged
- Manual corrections per tray
- Low-confidence detections per tray
- Repeated failure categories
- Time from scan to confirmed tray result, if available

## Required Analysis

### Tray-Level Summary

| Trial | Required Count | Detected Count | Missing Items | Extra / Unknown | Corrections | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Trial 1 | | | | | | |
| Trial 2 | | | | | | |
| Trial 3 | | | | | | |

### Repeated Failure Categories

| Category | Count | Example Condition | Likely Cause | Product Response |
| --- | --- | --- | --- | --- |
| Missing item | | Heavy occlusion | Visibility | Ask for tray spread / rescan |
| Wrong class | | Similar shapes | Model confusion | More data or family-level review |
| Extra / unknown | | Distractor object | Open-set risk | Needs-review state |
| Duplicate count | | Reflections / overlap | NMS or clutter | Tune threshold / collect clutter data |
| Low confidence | | Glare | Lighting | Lighting guidance or augmentation |

### Report Deliverable

Create a short report with these sections.

- One-page executive summary
- Per-condition metrics
- Top failure modes
- Example detection screenshots
- Recommended next experiments or data collection

## What Counts as Success

- The report makes repeated failure patterns visible.
- The logged data can explain why a tray was flagged.
- The system can distinguish "model error" from "visibility too poor" from "user corrected the tray."
- The output supports a credible ROI and safety discussion without claiming clinical readiness.

## What Not To Do

- Do not store only aggregate accuracy.
- Do not omit manual corrections.
- Do not imply that a visual count proves sterility, cleanliness, sharpness, or function.
- Do not treat screenshots as a substitute for structured logs.

## Key Takeaways Expected

At the end, we should be able to answer these questions.

1. What would TrayGuard tell an SPD manager after a week of use?
2. Which model errors are repeatable enough to fix?
3. Which workflow problems need UI or process changes?
4. What evidence would make a customer more comfortable with a pilot?

## Guiding Principle

> A hospital buyer needs a quality story, not just a demo.

## References

- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
