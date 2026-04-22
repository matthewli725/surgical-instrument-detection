# Workflow Acceptance

TrayGuard only matters if it helps people complete tray checks without making
their work harder. This page explains how to think about usability and adoption.

## What This Test Answers

A hospital does not buy a detector. It buys a workflow change.

## Why This Is A Risk

Healthcare decision-support tools can fail when they interrupt workflow or
create too many low-value alerts. A clinical decision-support review highlights
that inappropriate alerts can interrupt clinical workflow
([Olakotan and Yusof, 2021](../../bibliography.md#olakotan-and-yusof-2021)), and
another review ties alert burden to alert fatigue and reduced usability and
acceptance
([Cánovas-Segura et al., 2023](../../bibliography.md#canovas-segura-et-al-2023)).

SPD improvement work also shows that missing and unusable instrumentation is not
only a detection problem. Successful improvement involved staffing, training,
inventory, equipment, physical environment, workflows, communication, and
governance
([Natarus et al., 2025](../../bibliography.md#natarus-et-al-2025)).
TrayGuard therefore has to fit the human workflow, not just produce boxes on an
image.

This test answers:

- Does TrayGuard help users catch tray issues?
- Does it slow the task down?
- Do users understand uncertainty and review prompts?
- Does the tool feel like an assistant instead of an obstacle?

## Design Assumptions For This Test

This page focuses on how to test workflow acceptance, not on re-arguing the
full adoption case. The background narrative and detailed appendix already cover
the broader evidence base:

- `docs/background/project_background.md`
- `docs/experiments/adoption/formal_risk_analysis.md`

For this experiment, we assume the product is being evaluated as a guided
verification assistant rather than as a fully autonomous tray-approval system.
That means the workflow test should focus on whether TrayGuard helps users catch
issues, recover from uncertainty, and finish the task with acceptable time and
correction burden.

The main workflow hypotheses are:

- Assistant-mode review is more acceptable than automation-style language.
- Users will tolerate imperfect detections if corrections are fast and obvious.
- Trust will depend more on uncertainty handling and correction burden than on raw detector accuracy alone.
- False alarms and rescans will hurt adoption quickly.

## Tray Issues To Include

Use tray-like tasks that include realistic problems:

- One missing required item.
- One extra item.
- One similar-looking wrong item.
- One hard-to-see or partially hidden item.
- One unknown distractor object.

The goal is to test the workflow, not just the model.

## What To Measure

Track both task outcomes and user reactions.

| Category | Examples |
| --- | --- |
| Accuracy | Missing items caught, wrong items caught, extra items caught |
| Speed | Time to final tray decision, number of rescans |
| Correction burden | Number of model corrections, ease of correction |
| Trust | Whether users understood review prompts and final status |
| Hesitation | Moments where the user paused, questioned, or distrusted the system |

## Suggested User Questions

Use a 1-5 scale:

1. TrayGuard made the task easier.
2. TrayGuard made me more confident in the final tray check.
3. I understood which detections needed review.
4. Correcting the system was easy.
5. I would want this tool if I were responsible for tray assembly.

Ask one open-ended question:

- What is the biggest reason you would hesitate to use this system?

## Product Interpretation

| Pattern | What It Means | Product Response |
| --- | --- | --- |
| Users catch more issues with small added time | The workflow has promise | Keep the assistant framing |
| Users are faster but miss issues | The product is not helping safely | Make review states clearer |
| Users correct the model easily | Human-in-the-loop design is viable | Keep correction controls simple |
| Users distrust confident results | The product needs better evidence and explanations | Show uncertainty, examples, and logs |
| Users dislike rescanning | The scan guidance is too costly | Make rescan instructions specific and fast |

## What We Are Not Claiming

- Classmate or team-member feedback does not prove SPD technician adoption.
- Speed alone is not success.
- TrayGuard should support technician judgment, not replace it.
- Low hardware cost alone does not prove adoption.
- A good offline accuracy number alone does not prove workflow value.

## Bibliography

See the [central bibliography](../../bibliography.md) for full source details.
