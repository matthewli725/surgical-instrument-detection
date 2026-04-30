# Formal Risk Analysis

TrayGuard should not be evaluated as "just a detector." In high-risk workflows,
buyers can reject a technically strong system if it creates dependency,
disrupts operations, or makes responsibility unclear. The central design stance
is already defined in the [system design](../../background/system_design.md):
TrayGuard is a technician-centered verification assistant, not an autonomous
tray-approval system.

This page keeps the risk register in one place. It links back to longer
argument sections instead of restating the same evidence in every experiment
doc.

## Core Claim

A hospital may reject fully autonomous tray sorting or approval even if test
accuracy is high. The adoption question is whether the system improves tray
work without adding operational, legal, or human-factor risk. Healthcare AI
implementation, radiology deployment, and pharmacy verification research all
support that narrower assistant framing
([van Leeuwen et al., 2021](../../bibliography.md#van-leeuwen-et-al-2021),
[Jiang et al., 2025](../../bibliography.md#jiang-et-al-2025),
[Zheng et al., 2023](../../bibliography.md#zheng-et-al-2023)).

## Direct Evidence Boundary

The product space is real but still early. The closest direct signals are:

- Sayani et al.'s tray-detection patent, which describes camera-based
  comparison of present and expected instruments
  ([Sayani et al., 2018](../../bibliography.md#sayani-et-al-2018)).
- SteelcoBelimed's SUIS product, which frames CV as guided set-packing support
  rather than invisible autonomous approval
  ([SteelcoBelimed, accessed 2026](../../bibliography.md#steelcobelimed-accessed-2026)).
- Wellstar's reported pilot with RIF Robotics, which reinforces the need for
  sterile-processing staff feedback
  ([American Hospital Association, 2023](../../bibliography.md#american-hospital-association-2023)).
- Atabuzzaman et al.'s CSSD-oriented two-camera classification system, which
  supports structured capture for fine-grained instruments but does not solve
  full-tray verification
  ([Atabuzzaman et al., 2025](../../bibliography.md#atabuzzaman-et-al-2025)).
- Deol et al.'s automated surgical-instrument detection and counting study,
  which supports object detection for multi-tool scenes while still calling
  for clinical validation
  ([Deol et al., 2024](../../bibliography.md#deol-et-al-2024)).

For how these signals shape the architecture, see
[`../../background/system_design.md`](../../background/system_design.md#design-lessons-from-close-prior-work).

## System-Level Risk Register

These risks matter even if the vision model is accurate.

| Risk | Why It Matters | TrayGuard Response |
| --- | --- | --- |
| Human agency and over-reliance | Deskilling and automation bias can make users passive monitors rather than active verifiers ([Natali et al., 2025](../../bibliography.md#natali-et-al-2025), [Goddard et al., 2012](../../bibliography.md#goddard-et-al-2012)). | Keep human sign-off explicit and make review actions meaningful. |
| Operational fragility | A brittle camera, UI, model, or integration can become a single point of failure during peak work ([Chomutare et al., 2022](../../bibliography.md#chomutare-et-al-2022), [Jiang et al., 2025](../../bibliography.md#jiang-et-al-2025)). | Preserve manual fallback and treat guided review as a valid mode. |
| Exception handling | Substitutions, damaged tools, partial trays, and local policies cannot be solved by a detector alone. | Route exceptions into review instead of forcing automatic approval. |
| Workflow fit and alert burden | Extra clicks, false alerts, and rescans can erase the value of high offline accuracy ([Olakotan and Yusof, 2021](../../bibliography.md#olakotan-and-yusof-2021), [Cánovas-Segura et al., 2023](../../bibliography.md#canovas-segura-et-al-2023)). | Measure correction burden, rescan rate, and time-to-final-decision in workflow tests. |
| Change management | Training, SOP changes, stakeholder buy-in, and pilot management can dominate technical performance. | Evaluate adoption as a workflow change, not a model demo. |
| Accountability and auditability | Hospitals need to explain who approved a tray and what evidence was available ([Kelly, 2026](../../bibliography.md#kelly-2026)). | Save screenshots, confidence/review states, corrections, and final human confirmation. |
| Physical integration and sterility | A future sorter would add cleaning, handling, maintenance, and validated reprocessing constraints ([Pelzer et al., 2024](../../bibliography.md#pelzer-et-al-2024), [CDC](../../bibliography.md#cdc), [FDA](../../bibliography.md#fda)). | Keep this prototype focused on visual verification, not robotic manipulation. |
| Economic fit | Buyers need evidence of reduced rework, delays, or quality losses, not only model performance ([Vithlani et al., 2023](../../bibliography.md#vithlani-et-al-2023), [Kastrup et al., 2024](../../bibliography.md#kastrup-et-al-2024)). | Pair model metrics with reporting and workflow-value evidence. |

## CV-Specific Risk Register

The longer source-backed treatment of these choices lives in the system
design's [research support audit](../../background/system_design.md#research-support-audit).
The experiment pages below should document local evidence, not re-argue the
whole case.

| Risk | Practical Concern | Primary Local Test |
| --- | --- | --- |
| Distribution shift | Local camera placement, tray layout, lighting, wear, and handling habits can change model behavior. | Held-out condition evaluation in the CV experiments. |
| Reflectivity and lighting | Specular glare can hide edges and details on metal tools. | [`../cv/reflectivity_lighting.md`](../cv/reflectivity_lighting.md) |
| Occlusion and clutter | Hidden geometry can produce undercounts, merged detections, or false confidence. | [`../cv/clutter_occlusion.md`](../cv/clutter_occlusion.md) |
| Similar-class confusion | Wrong-but-similar tools may be more dangerous than obvious misses. | [`../cv/shape_similarity.md`](../cv/shape_similarity.md) |
| Open-set behavior | Unknown or damaged tools should not be forced into known labels. | [`../cv/open_set_confidence.md`](../cv/open_set_confidence.md) |
| Confidence calibration | A confidence score is an operating signal, not a safety probability ([Guo et al., 2017](../../bibliography.md#guo-et-al-2017)). | Threshold and review-rate analysis in validation data. |
| Local validation | Internal prototype results do not prove site readiness ([Tikhomirov et al., 2026](../../bibliography.md#tikhomirov-et-al-2026), [Yang et al., 2024](../../bibliography.md#yang-et-al-2024)). | Shadow-mode or guided-use evaluation before stronger workflow claims. |

## Combined Interpretation

The evidence supports these design conclusions:

- Full replacement is harder to adopt than assistive verification.
- Human sign-off should remain explicit.
- Uncertain and exceptional cases should be surfaced, not hidden.
- The system should degrade gracefully when unavailable.
- Logs, screenshots, and correction history matter for trust.
- Pilot evidence should focus on workflow value, not only detector metrics.
- Environmental assumptions and scope limits should be stated explicitly.

The most defensible product claim is therefore:

> TrayGuard should reduce cognitive burden and missed items while preserving
> human authority, auditability, and recovery paths.

## Bibliography

See the [central bibliography](../../bibliography.md) for full source details.
