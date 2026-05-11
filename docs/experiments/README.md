# Experiments

This directory now contains the evaluation plan for the training-platform
pivot. Local computer-vision accuracy experiments are no longer part of the
active evidence plan. The repository may keep code for camera capture,
annotation, YOLO export, and live detection as legacy implementation support,
but the report should not ask reviewers to accept TrayGuard because of our own
CV metrics.

## Current Prototype Flow

TrayGuard is being evaluated as a training and assessment platform:

1. Load a local tray module.
2. Run a timed pre-test tray sorting assessment.
3. Let the learner study instrument cards and complete quiz prompts.
4. Let the learner practice simulated tray sorting with feedback.
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

## Evidence Boundary

The project no longer needs to prove that a locally trained CV model reaches
deployment-grade accuracy. Existing research already supports the weaker and
more useful assumption: modern CV can be a plausible support layer in bounded
surgical-instrument settings, but robustness must be validated locally before
clinical use.

| Evidence Area | Existing Literature Supports | Gap We Should Not Pretend To Fill |
| --- | --- | --- |
| Data-efficient detection is plausible | Few-shot object detection exists specifically because large annotated datasets are often impractical; fine-tuning pretrained detectors can work well in low-shot settings ([Xin et al., 2024](../bibliography.md#xin-et-al-2024), [Wang et al., 2020 FSOD](../bibliography.md#wang-et-al-2020-fsod)). | These papers do not prove our instrument set, camera setup, or hospital environment will generalize from a tiny dataset. |
| Surgical-instrument detection is feasible | Deol et al. report strong detection/counting results for multi-tool surgical scenes; Atabuzzaman et al. report high-performing CSSD-oriented multi-view instrument classification ([Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025)). | These are not the same as our full training workflow, our local tray modules, or broad manufacturer-agnostic SPD deployment. |
| Generalization remains the hard part | Kienle et al. show high in-domain mAP50 but a large cross-manufacturer drop when testing on a second dataset ([Kienle et al., 2025](../bibliography.md#kienle-et-al-2025)). | We should not claim robust real-hospital CV performance without a site-specific validation study. |
| SPD assembly is a sociotechnical problem | Alfred et al. connect tray defects to training, nomenclature, production pressure, inventory, tools, and workflow; Nichol et al. connect errors to visualization tasks and OR delays ([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021), [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). | A detector metric alone cannot show that trainees learn, administrators see value, or workflows improve. |
| Training and simulation are defensible | Sterile-processing and healthcare-education studies support structured training, simulation, practice, feedback, and pre/post assessment ([Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023), [Hu et al., 2024](../bibliography.md#hu-et-al-2024), [Cook et al., 2011](../bibliography.md#cook-et-al-2011), [McGaghie et al., 2011](../bibliography.md#mcgaghie-et-al-2011)). | A short class study still cannot prove real SPD competency, certification readiness, or reduced hospital onboarding time. |

## Shared Reporting Checklist

For the current prototype, report:

- pre/post simulated tray-sorting accuracy;
- pre/post duration;
- confidence and high-confidence errors;
- missing, extra, wrong, misidentified, and wrong-count errors;
- whether learners can explain what they missed and what to review next;
- usability friction, help requests, and confusing workflow states;
- what the result means for SPD trainees, hospital administrators, and student
  evaluators.

Do not report our local precision, recall, mAP50, mAP50-95, lighting-stage, or
shape-similarity experiments as central evidence. Those can be mentioned only
as retired exploratory work or future authoring-support infrastructure.

The final claim should remain bounded: TrayGuard is testing whether a local
training module improves simulated tray familiarity, not claiming live SPD
competency, certification readiness, CV robustness, or hospital deployment
readiness.
