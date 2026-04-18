# Traceability And Quality Reporting

TrayGuard should produce more than a one-time detection result. It should help a
team understand repeated tray-check problems over time.

## What This Test Answers

A hospital team needs an audit trail and a quality-improvement story, not just a
demo screen.

## Why This Is A Risk

Instrument errors are difficult to improve if they are not recorded in a useful
way. A direct-observation study notes that staff reporting can be burdensome,
incomplete, delayed, and can underreport the real rate and cost of instrument
errors
([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).
Traceability research frames surgical instrument tracking as important for
patient safety, cost, logistics, environmental impact, and risk analysis
([Fayad et al., 2025](https://www.mdpi.com/2076-3417/15/3/1592)).

This matters for TrayGuard because a camera assistant that only shows a live
prediction and then forgets it cannot help managers see repeated missing-item,
wrong-class, glare, clutter, or correction patterns.

This test answers:

- Can TrayGuard explain why a tray was flagged?
- Can it show repeated failure patterns?
- Can it separate model mistakes from visibility problems and user corrections?
- Would the output help an SPD manager decide what to improve next?

## What The Report Should Capture

A useful quality record should include:

- Trial or scan ID.
- Required tray list.
- Detected instruments and counts.
- Missing required items.
- Extra or unknown objects.
- Low-confidence or review-needed detections.
- User corrections.
- Image or screenshot reference.
- Condition tags such as lighting, clutter, or similar-shape risk.

## How To Read The Results

The report should make repeated patterns visible.

Useful questions include:

- Which instruments are most often missed?
- Which instruments are most often confused?
- Which tray conditions create the most review flags?
- How often does a person correct the system?
- Are failures caused by the model, the image quality, or the tray layout?

## Product Interpretation

| Pattern | What It Means | Product Response |
| --- | --- | --- |
| Missing items repeat for one class | The model or data is weak for that class | Collect targeted examples |
| Review flags cluster under glare | Image quality is the issue | Add lighting guidance or rescan prompts |
| Corrections cluster around similar tools | Class distinction is difficult | Add pair-specific review |
| Unknown objects appear often | The workflow needs an extra-object path | Add simple remove-or-confirm actions |

## User-Facing Report Sections

A good report should include:

- Summary of tray checks completed.
- Missing, extra, and uncertain item counts.
- Most common failure categories.
- Representative screenshots.
- Recommended next actions.

## What We Are Not Claiming

- Detection logs do not prove sterility, cleanliness, sharpness, or function.
- Screenshots alone are not a complete audit record.
- A quality report supports human review; it does not replace departmental
  quality processes.

## References

- Fayad et al., ["Traceability of Surgical Instruments: A Systematic Review"](https://www.mdpi.com/2076-3417/15/3/1592), Applied Sciences, 2025.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
