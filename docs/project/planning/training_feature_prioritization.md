# Training Feature Prioritization

This note ranks proposed TrayGuard training features by three criteria:

- **Helpful:** Does it strengthen novice tray and instrument learning?
- **Doable:** Can the current prototype implement it without needing a hospital
  deployment, large verified image library, or validated computer vision model?
- **Verifiable:** Can the project measure the effect with pre/post simulated
  tray tasks, confidence, time, and error-category exports?

The conclusion is that TrayGuard should build one polished local tray learning
loop first, then expand into richer simulations after the core evidence exists.

## Recommended MVP

The strongest defensible MVP combines:

1. Tray reconstruction / simulated tray sorting.
2. Count-sheet-guided error spotting.
3. Lookalike instrument challenges.
4. Retrieval-first study cards.
5. Weak-item replay.
6. Pre/post assessment.
7. Instructor metrics export.
8. File-backed local tray modules.

This combination supports the current project claim:

> TrayGuard gives novices repeated, measurable practice on local tray
> familiarity and tests whether that practice improves simulated tray
> reconstruction and verification performance.

Certification, clinical-transfer, and deployment boundaries are maintained in
[`../scope_boundaries_and_risks.md`](../scope_boundaries_and_risks.md).

## Highest-Priority Features

| Feature | Verdict | Why It Fits TrayGuard | Verification |
| --- | --- | --- | --- |
| Tray reconstruction from memory | Core feature | Trains tray-level organization, count application, spatial logic, and procedural recall rather than isolated recognition. | Compare pre/post tray accuracy, duration, missing items, extras, wrong items, wrong counts, confidence, and weak-item recovery. |
| Error-spotting simulation | Core or near-core feature | Mirrors count-sheet-guided SPD verification and maps directly to missing, wrong, extra, damaged, wrong-count, and mixed-specialty errors. | Measure false negatives, false positives, inspection speed, confidence calibration, and error categories. |
| Instrument similarity challenges | Core support mode | Lookalikes are already part of the TrayGuard data model through declared lookalike pairs and `misidentified` errors. | Track pair-specific confusion rates before and after comparison cards or quizzes. |
| Adaptive weakness replay | Core if schedule allows | Turns retrieval failures into repeated practice and makes the system meaningfully stronger than static cards. | Export missed items, uncertain items, repeated attempts, later correctness, and high-confidence error reduction. |
| Instructor-created local modules | Strategic differentiator | Local trays, names, aliases, count sheets, quantities, and surgeon or facility preferences are the strongest product moat. | For the capstone, prove this with file-backed modules before a full authoring UI. |

## Good Secondary Features

| Feature | Verdict | Why It Fits TrayGuard | Implementation Note |
| --- | --- | --- | --- |
| Progressive tray difficulty system | Helpful after MVP | Creates mastery curves and an adaptive learning path from single instruments to noisy trays. | Wait until one complete tray module works end to end. |
| "Why this instrument exists" context layer | Useful content layer | Adds semantic encoding: procedure role, tissue interaction, surgeon intent, common misuse, and OR consequence. | Put this inside cards and feedback. |
| Tray variant comparison mode | Strong future feature | Directly supports local tray variation, surgeon preferences, and specialty modifications. | Requires multiple verified variants before it can be assessed fairly. |
| Peer benchmarking / cohort analytics | Useful instructor value | Helps educators see common misses, slow trays, repeated lookalikes, and class-level weak areas. | Start with aggregate instructor reports; avoid competitive ranking in early pilots. |
| Instrument damage recognition | Valuable future module | Connects training to patient safety and visual inspection. | Needs real damaged-instrument examples or carefully validated synthetic examples. |
| Procedure-to-tray mapping | Advanced learning mode | Develops conceptual organization from procedure needs to tray composition. | Best after learners already understand basic tray membership and instrument families. |
| Multi-modal instrument learning | Selectively useful | Photos, aliases, distinguishing features, pronunciation, and placement views can enrich encoding. | Do photos and feature prompts first; 3D models or usage clips are not required for the first evidence claim. |

## Lower-Priority Or Riskier Features

| Feature | Verdict | Reason To Defer |
| --- | --- | --- |
| Timed cognitive load modes | Use lightly | Timers are easy and useful, but simulated OR urgency, interruptions, fatigue, or mid-task changes are harder to validate and may make a small student pilot less interpretable. |
| Assembly sequence training | Later | Efficient sequencing is real procedural cognition, but the current software prototype can verify composition better than physical handling efficiency. |
| Blind verification mode | Later | Partial visibility and obscured labels are interesting, but they can interfere with the clean pre/post learning design needed for the first evaluation. |

## Research Support Map

| Research Area | Supports | Key Sources |
| --- | --- | --- |
| Retrieval practice and spacing | Retrieval-first cards, weak-item replay, delayed review, prompt-before-answer design. | Roediger and Karpicke (2006), Karpicke and Blunt (2011), Larsen et al. (2009). |
| Simulation and deliberate practice | Tray sorting, error spotting, repeated attempts, measurable proficiency gains. | Cook et al. (2011), McGaghie et al. (2011), Issenberg et al. (2005). |
| Sterile-processing training precedent | Pre-test, guided teaching, hands-on-style practice, post-test, confidence capture, booster. | Ofstead et al. (2023). |
| Count sheets and local tray authority | Local module authoring, tray-specific quantities, aliases, count-sheet-guided verification. | Nadeau (2024), dos Santos et al. (2021), Ahmadi et al. (2023). |
| Instrument visual confusability | Lookalike challenges, pair-specific comparison cards, `misidentified` error tracking. | Atabuzzaman et al. (2025), Rodrigues et al. (2022b), Alfred et al. (2021). |
| Tray-error categories | Missing, wrong, extra, damaged, wrong-count, misidentified, and visualization-related errors. | Alfred et al. (2021), Nichol et al. (2024). |

## Product Decision

Present the feature list as one learning loop with optional expansions:

```text
local tray module
-> pre-test tray reconstruction or verification
-> retrieval-first cards and lookalike prompts
-> quiz and weak-item replay
-> practice reconstruction / error spotting with feedback
-> post-test
-> learner and instructor metrics export
```

The capstone should prioritize the features that are most measurable in a small
novice pilot: reconstruction accuracy, verification accuracy, duration, error
categories, confidence calibration, and weak-item recovery.
