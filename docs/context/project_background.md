# TrayGuard Project Background

This page is a lightweight hub for the pivoted project narrative. TrayGuard is
now centered on reducing simulated time-to-competency for novice SPD learners,
with computer vision treated as an optional support layer rather than the main
deployment claim.

## Core Background Docs

- [Problem explication](problem_explication.md)
- [Surgical instrument taxonomy](../project/reference/instrument_taxonomy.md)
- [Training module design](../project/training_module_design.md)
- [System design](../project/system_design.md)
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
does not drift back toward passive content browsing or a CV-first detector demo.

The system-design doc treats the training module as the primary product and the
existing camera/CV work as legacy or future support. CV feasibility is now
cited from existing literature rather than proved through local experiments.

The experiments overview and evaluation plan live in
[`docs/project/evaluation/README.md`](../project/evaluation/README.md). The primary
experiment is now
[training effectiveness](../project/evaluation/adoption/training_effectiveness.md):
pre/post simulated tray sorting with accuracy, time, confidence, and
error-category metrics.
