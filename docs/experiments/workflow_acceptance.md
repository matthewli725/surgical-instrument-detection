# Workflow Acceptance & Throughput Experiment Plan

## Objective

Evaluate whether TrayGuard helps a person complete a tray-checking task faster, more accurately, or with less cognitive burden. This experiment targets an adoption risk. A technically accurate system can still be rejected if it feels disruptive, opaque, or slower than the current process. SPD quality-improvement studies identify staffing, training, workflows, communication, environment, inventory, and governance as defect drivers. Technology alone is not the solution (Natarus et al., 2025).

## Core Question

> Would a technician second-guess buying or using this system after trying it in a realistic workflow?

## Why This Matters

A hospital does not buy a detector. It buys a workflow change. Our professor's UCLA Ronald Reagan anecdote about a rejected 100%-accurate sorting robot should be treated as a warning consistent with the literature. Missing and unusable instrumentation can cause delays. Sustained improvement also requires changes to staffing, training, inventory management, equipment, environment, standard workflows, communication, and governance (Natarus et al., 2025).

TrayGuard should therefore be framed as decision support for tray verification. It should not be framed as a full replacement for sterile processing judgment. CSSD and SPD work requires specialized on-the-job training and complex visual-inspection skills (Bridges, 2010, Hu et al., 2024, Ofstead et al., 2023).

## Experimental Design Overview

Run a lightweight user study with simulated tray assembly.

### Conditions

1. Manual checklist only
2. TrayGuard assistant mode with detections, missing-item list, and uncertainty flags
3. Optional TrayGuard automation-mode wording that sounds more authoritative

The third condition is useful if there is time because wording and control affect trust.

## Task Setup

Use a tray-like area with a required instrument list.

Each trial should include one or more realistic issues.

- One missing required item
- One extra item
- One visually similar wrong item
- One occluded or hard-to-see item
- One unknown distractor item

## Participants

Use classmates or team members if SPD technicians are unavailable. Record that these are proxy users and avoid overclaiming clinical realism.

Minimum useful sample

- 3-5 users for qualitative usability issues
- 8-10 users if comparing task-time trends

## Procedure

1. Give the participant a required tray list.
2. Ask them to verify whether the tray is complete.
3. Run the task manually first or counterbalance task order if possible.
4. Run the task with TrayGuard.
5. Record time, corrections, missed issues, and user comments.
6. Ask a short post-task survey.

## Measures

### Quantitative

- Task completion time
- Missing instruments caught
- Wrong instruments caught
- Extra instruments caught
- Number of model corrections
- Number of rescans
- Number of times the user hesitates or asks for clarification

### Qualitative

- Did the user trust the result?
- Did uncertainty flags make sense?
- Did the UI reduce or increase cognitive load?
- Did the system feel like an assistant or an obstacle?
- What would make the user second-guess deployment?

## Suggested Survey

Use a 1-5 scale.

1. TrayGuard made the task easier.
2. TrayGuard made me more confident in the final tray check.
3. I understood which detections needed review.
4. Correcting the system was easy.
5. I would want this tool if I were responsible for tray assembly.

Ask one open-ended question.

- What is the biggest reason you would hesitate to use this system?

## Required Analysis

### Task Outcomes

| Condition | Avg Time | Missed Issues | Corrections | Rescans | Notes |
| --- | --- | --- | --- | --- | --- |
| Manual checklist | | | | | |
| TrayGuard assistant | | | | | |
| TrayGuard automation wording | | | | | |

### User Hesitations

| Hesitation | Frequency | Severity | Possible Design Response |
| --- | --- | --- | --- |
| Too slow | | | Faster scan flow |
| Unclear uncertainty | | | Better review labels |
| Hard to correct | | | One-click correction |
| Trust concern | | | Audit log and human confirmation |
| Workflow mismatch | | | Integrate with tray list / barcode step |

## What Counts as Success

- TrayGuard catches issues that users miss manually, or catches them with less effort.
- The added time is small enough to justify the safety and documentation value.
- Users can correct the system without confusion.
- Users describe the tool as supportive rather than replacing their judgment.

## What Not To Do

- Do not claim SPD technician acceptance from classmates alone.
- Do not measure only speed. A fast wrong check is not valuable.
- Do not hide model mistakes from participants.
- Do not use confident language when the system is uncertain.

## Key Takeaways Expected

At the end, we should be able to answer these questions.

1. Does TrayGuard reduce verification errors in a simulated tray task?
2. Does it slow users down, and by how much?
3. Which UI moments cause hesitation or mistrust?
4. Should the product pitch emphasize automation, decision support, audit logs, or training?

## Guiding Principle

> The buyer's question is not "Can it detect?" but "Will this make my department safer without making the day harder?"

## References

- Bridges, ["The Real Costs of Surgical Instrument Training in Sterile Processing Revisited"](https://doi.org/10.1016/j.aorn.2009.10.025), AORN Journal, 2010.
- Hu et al., ["Improvement and implementation of central sterile supply department training program based on action research"](https://link.springer.com/article/10.1186/s12912-024-01809-z), BMC Nursing, 2024.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Ofstead et al., ["Improving mastery and retention of knowledge and complex skills among sterile processing professionals: A pilot study on borescope training and competency testing"](https://doi.org/10.1016/j.ajic.2023.03.002), American Journal of Infection Control, 2023.
