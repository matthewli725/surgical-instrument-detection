# TrayGuard Project Background

This page is a lightweight hub for the project narrative. TrayGuard is centered
on reducing simulated time-to-competency for novice SPD learners through local
tray modules, retrieval-first practice, simulated sorting, feedback, and
pre/post metrics. Computer vision remains an optional support layer for future
authoring or visual-review workflows.

## Core Background Docs

- [Problem explication](problem_explication.md)
- [Surgical instrument taxonomy](../project/reference/instrument_taxonomy.md)
- [Training module design](../project/training_module_design.md)
- [System design](../project/system_design.md)
- [Scope boundaries and risks](../project/scope_boundaries_and_risks.md)
- [Experiments overview](../project/evaluation/README.md)

The problem-explication doc now establishes the training-centered motivation:
SPD technician shortages, the cost and duration of onboarding, certification
and hands-on training pathways, and the need for repeatable novice practice in
instrument identification and tray organization. It also connects the proposed
learner workflow to evidence from simulation-based medical education,
retrieval practice, feedback research, organizational training, and existing
medical training software.

The training-module design doc makes the focused module decision explicit: one
local tray curriculum with pre-test, retrieval-first study cards, quiz prompts,
applied tray sorting with feedback, weak-item review, post-test, and exportable
metrics. It also records the tradeoffs behind that decision so implementation
continues to prioritize active practice and pre/post evidence.

The system-design doc treats the training module as the primary product and
keeps camera/CV work available as future support. CV feasibility is cited from
existing literature, while the active prototype evidence comes from local
learning metrics.

The scope-boundaries doc consolidates certification, clinical-transfer,
computer-vision, reporting, and physical-prototype risks so the main docs can
stay focused on proposed capabilities.

The experiments overview and evaluation plan live in
[`docs/project/evaluation/README.md`](../project/evaluation/README.md). The primary
experiment is now
[training effectiveness](../project/evaluation/adoption/training_effectiveness.md):
pre/post simulated tray sorting with accuracy, time, confidence, and
error-category metrics.
