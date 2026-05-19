# Experiments

This directory contains the evaluation plan for the training-platform
prototype. The active evidence plan measures whether a local tray module
improves novice simulated tray familiarity. Camera capture, annotation, YOLO
export, and live detection code remain available as support infrastructure for
future authoring or visual-review work.

## Current Prototype Flow

TrayGuard is being evaluated as a training and assessment platform:

1. Load a local tray module.
2. Run a timed pre-test tray sorting assessment.
3. Let the learner use retrieval-first cards and quiz prompts.
4. Let the learner practice simulated tray sorting as applied retrieval with
   feedback.
5. Run a timed post-test tray sorting assessment.
6. Export accuracy, duration, confidence, and error-category metrics.

The evidence question is:

> Does a novice improve on simulated local tray familiarity after using the
> TrayGuard module?

## Active Experiment Map

| Axis | Doc | Local Question |
| --- | --- | --- |
| Training effectiveness | [`adoption/training_effectiveness.md`](adoption/training_effectiveness.md) | Does the trainer improve simulated tray-sorting accuracy, speed, confidence, and error breakdown from pre-test to post-test? |
| Workflow acceptance | [`adoption/workflow_acceptance.md`](adoption/workflow_acceptance.md) | Can novice users complete the learning workflow without excessive friction or over-reliance? |
| Traceability and reporting | [`adoption/traceability_reporting.md`](adoption/traceability_reporting.md) | Can the prototype produce useful learner and instructor evidence about repeated errors? |
| Literature-backed risk analysis | [`adoption/formal_risk_analysis.md`](adoption/formal_risk_analysis.md) | What do existing papers already show, what gaps do they leave, and what does that mean for our system and stakeholders? |

## Evidence Boundary Routing

The evaluation plan separates the active training claim from future clinical,
CV, and deployment validation work. Existing research supports CV as a
plausible support layer in bounded surgical-instrument settings; the current
prototype uses manual simulated sorting so learning evidence can be collected
without making detector performance a proof obligation.

| Evidence Area | Existing Literature Supports | TrayGuard Response |
| --- | --- | --- |
| Data-efficient detection is plausible | Few-shot object detection exists specifically because large annotated datasets are often impractical; fine-tuning pretrained detectors can work well in low-shot settings ([Xin et al., 2024](../../bibliography.md#xin-et-al-2024), [Wang et al., 2020 FSOD](../../bibliography.md#wang-et-al-2020-fsod)). | Treat local CV as future support-layer validation. |
| Surgical-instrument detection is feasible | Deol et al. report strong detection/counting results for multi-tool surgical scenes; Atabuzzaman et al. report high-performing CSSD-oriented multi-view instrument classification ([Deol et al., 2024](../../bibliography.md#deol-et-al-2024), [Atabuzzaman et al., 2025](../../bibliography.md#atabuzzaman-et-al-2025)). | Use CV literature for feasibility and focus this evaluation on the learning workflow. |
| Generalization remains the hard part | Kienle et al. show high in-domain mAP50 but a large cross-manufacturer drop when testing on a second dataset ([Kienle et al., 2025](../../bibliography.md#kienle-et-al-2025)). | Keep local photos and instructor verification as the source of truth. |
| SPD assembly is a sociotechnical problem | Alfred et al. connect tray defects to training, nomenclature, production pressure, inventory, tools, and workflow; Nichol et al. connect errors to visualization tasks and OR delays ([Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021), [Nichol et al., 2024](../../bibliography.md#nichol-et-al-2024)). | Measure trainee learning, workflow friction, and instructor-facing evidence. |
| Training and simulation are defensible | Sterile-processing and healthcare-education studies support structured training, simulation, practice, feedback, and pre/post assessment ([Ofstead et al., 2023](../../bibliography.md#ofstead-et-al-2023), [Hu et al., 2024](../../bibliography.md#hu-et-al-2024), [Cook et al., 2011](../../bibliography.md#cook-et-al-2011), [McGaghie et al., 2011](../../bibliography.md#mcgaghie-et-al-2011)). | Run a paired novice learning study and report the clinical-transfer boundary separately. |
| Retrieval-centered digital practice is defensible | Retrieval-practice and health-professions digital-education studies support prompt-before-answer practice, spacing, and weak-item repetition, while electronic-flashcard research shows that app-style recall tools are already common in health-professions learning ([Roediger and Karpicke, 2006](../../bibliography.md#roediger-and-karpicke-2006), [Larsen et al., 2009](../../bibliography.md#larsen-et-al-2009), [Martinengo et al., 2024](../../bibliography.md#martinengo-et-al-2024), [Barrison et al., 2025](../../bibliography.md#barrison-et-al-2025)). | Use retrieval practice as the center and test applied transfer with simulated tray sorting. |

Detailed boundaries live in
[Scope Boundaries And Risks](../scope_boundaries_and_risks.md).

## Shared Reporting Checklist

For the current prototype, report:

- pre/post simulated tray-sorting accuracy;
- pre/post duration;
- confidence and high-confidence errors;
- weak-item recovery after repeated retrieval;
- missing, extra, wrong, misidentified, and wrong-count errors;
- whether learners can explain what they missed and what to review next;
- usability friction, help requests, and confusing workflow states;
- what the result means for SPD trainees, hospital administrators, and student
  evaluators.

Report local precision, recall, mAP50, mAP50-95, lighting-stage, or
shape-similarity experiments as exploratory support-layer work when relevant.
The final claim should remain: TrayGuard tests whether a local training module
improves simulated tray familiarity.
