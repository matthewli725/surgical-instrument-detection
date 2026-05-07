# Claim-Evidence Control Sheet

Use this as the project ownership map. The goal is not to read every citation
with equal depth. The goal is to know which claims you are defending, where the
evidence lives, what you still need to verify, and what you can confidently say
in your own words.

## How To Use This

For each claim:

- Read the canonical doc section first.
- Read the primary sources marked `deep`.
- Skim sources marked `skim` for the specific detail listed here.
- Write a two- or three-sentence ownership note in your own words.
- Mark the status as `not started`, `skimmed`, `owned`, or `needs revision`.

## Claim Index

| ID | Claim To Defend | Canonical Home | Read Depth | Status |
| --- | --- | --- | --- | --- |
| C1 | Surgical tray errors are real, costly, and often tied to visual identification, missing items, wrong items, or unusable instruments. | [`../background/problem_explication.md`](../background/problem_explication.md) | deep | not started |
| C2 | Computer vision is a reasonable low-infrastructure prototype layer, but it is not a replacement for RFID, barcode systems, staffing, or full traceability. | [`../background/problem_explication.md`](../background/problem_explication.md#cost-benefit-rationale-for-computer-vision) | deep/skim | not started |
| C3 | TrayGuard should be framed as technician-centered verification, not autonomous tray approval. | [`../background/system_design.md`](../background/system_design.md#prototype-scope) | deep | not started |
| C4 | The product space is real but early: patents, commercial systems, pilots, and academic studies exist, but they do not prove deployment readiness for TrayGuard. | [`../experiments/adoption/formal_risk_analysis.md`](../experiments/adoption/formal_risk_analysis.md#direct-evidence-boundary) | skim | not started |
| C5 | The main CV risks are lighting/glare, occlusion, similar-class confusion, unknown objects, and confidence calibration. | [`../background/system_design.md`](../background/system_design.md#research-support-audit) | deep/skim | not started |
| C6 | The experiments provide controlled prototype evidence, not hospital deployment proof. | [`../experiments/README.md`](../experiments/README.md) | deep | not started |
| C7 | Traceability and reporting matter because logs, screenshots, corrections, and repeat patterns make the system more defensible and useful for quality improvement. | [`../experiments/adoption/traceability_reporting.md`](../experiments/adoption/traceability_reporting.md) | skim | not started |
| C8 | The engineering pipeline is reproducible enough for a capstone prototype when commands, datasets, splits, metrics, and limitations are recorded. | [`../experiments/reproducibility/`](../experiments/reproducibility/) | verify | not started |
| C9 | The existing overhead camera stand is a defensible physical fixture when mounted to a portable board instead of screwed into a table. | [`../background/system_design.md`](../background/system_design.md#physical-capture-setup) | skim/verify | not started |
| C10 | Plywood and the existing camera stand are prototype materials, not SPD-ready cleanability claims. | [`../background/system_design.md`](../background/system_design.md#material-and-cleaning-assumptions) | skim/verify | not started |
| C11 | A tabletop default with a rolling standing option is the best prototype fit for varied SPD workflows. | [`../background/system_design.md`](../background/system_design.md#tabletop-default-with-rolling-standing-option) | skim/verify | not started |
| C12 | College-student walkthroughs support novice learnability and checklist-style visual verification claims, not SPD technician adoption claims. | [`../experiments/adoption/workflow_acceptance.md`](../experiments/adoption/workflow_acceptance.md#college-student-participant-caveat) | deep | not started |
| C13 | The technician UI should minimize workflow friction while preserving visual-first feedback, restrained audio, fast correction, and explicit human sign-off. | [`../background/system_design.md`](../background/system_design.md#technician-ui-design-principles) | deep/skim | not started |

## Claim Cards

### C1: Tray Errors Are Real And Visual

**Plain-English version:** TrayGuard addresses a documented sterile-processing
problem, not an invented demo problem. Missing, wrong, broken, and poorly
functioning instruments create delays and safety risk, and much of the work is
visual identification and inspection.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024) | deep | Error counts, missing-item frequency, visualization-related error share, delay-cost estimate. |
| [Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023) | skim | How sterile processing errors are categorized and reported. |
| [Zhu et al., 2019](../bibliography.md#zhu-et-al-2019) | skim | Packaging-error categories such as wrong specifications, incomplete packages, and missing instruments. |
| [Rubak et al., 2024](../bibliography.md#rubak-et-al-2024) and [Eussen et al., 2026](../bibliography.md#eussen-et-al-2026) | skim | Tray scale and complexity examples. |

**Prototype evidence:** Problem framing and experiment axes; no prototype result
is needed to prove the problem exists.

**Ownership note:** _Write this after reading._

**Open questions:** Which one or two numbers will you actually cite in the
final presentation?

### C2: CV Is Reasonable But Bounded

**Plain-English version:** CV is attractive because it can start with cameras
and software instead of instrument-level modification. That does not make it
universally better than RFID, barcode tracking, or staffing investment.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Olivere et al., 2021](../bibliography.md#olivere-et-al-2021) | skim | What RFID-style tracking requires and what value it provides. |
| [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024) | skim | Barcode/RFID read-time comparison and workflow implications. |
| [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013) | skim | RFID adoption barriers, cost, and ROI uncertainty. |
| [Mácola et al., 2025](../bibliography.md#macola-et-al-2025) and [Chobin, 2010](../bibliography.md#chobin-2010) | skim | Staffing shortage and training-cost context. |

**Prototype evidence:** Camera capture, YOLO export, training pipeline, and live
UI show why CV is testable in this repo.

**Ownership note:** _Write this after reading._

**Open questions:** How will you phrase the RFID/barcode comparison without
sounding like CV is always superior?

### C3: Assistant, Not Autonomous Approval

**Plain-English version:** The safest and most defensible product framing is a
human-confirmed assistant that flags issues, uncertainty, and evidence. It
should not silently approve trays.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Goddard et al., 2012](../bibliography.md#goddard-et-al-2012) | deep | Automation bias and over-reliance risk. |
| [Natali et al., 2025](../bibliography.md#natali-et-al-2025) | skim | Deskilling and human expertise concerns. |
| [Zheng et al., 2023](../bibliography.md#zheng-et-al-2023) and [Kim et al., 2025](../bibliography.md#kim-et-al-2025) | skim | Human-centered AI and uncertainty-aware review in pharmacy. |
| [Jiang et al., 2025](../bibliography.md#jiang-et-al-2025) and [Kelly, 2026](../bibliography.md#kelly-2026) | skim | Transparency, governance, and accountability. |

**Prototype evidence:** Review-needed states, correction flow goals, and logging
requirements in the system design.

**Ownership note:** _Write this after reading._

**Open questions:** What exact UI language will you use to avoid implying
autonomous approval?

### C13: Technician UI Supports The Workflow

**Plain-English version:** TrayGuard should feel like a focused verification
assistant, not a detector control panel. The interface should reduce repeated
workflow friction, make tray state and uncertainty visible, keep correction and
rescan paths fast, use audio only as optional reinforcement, and preserve
explicit human sign-off.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Nielsen Norman Group, accessed 2026](../bibliography.md#nielsen-norman-group-accessed-2026) and [Porter, 2003](../bibliography.md#porter-2003) | skim | Interaction cost, visible status, and why raw click count is not enough. |
| [Amershi et al., 2019](../bibliography.md#amershi-et-al-2019) | skim | Human-AI guidance for efficient invocation, dismissal, correction, and uncertainty handling. |
| [Olakotan and Yusof, 2021](../bibliography.md#olakotan-and-yusof-2021) and [Cánovas-Segura et al., 2023](../bibliography.md#canovas-segura-et-al-2023) | skim | Alert burden, alert fatigue, and workflow interruption risks. |
| [FDA Human Factors, accessed 2026](../bibliography.md#fda-human-factors-accessed-2026) | skim | Interface elements, user abilities, environment, and feedback as human-factors concerns. |
| [W3C/WAI Audio Control, accessed 2026](../bibliography.md#w3c-wai-audio-control-accessed-2026), [W3C/WAI Use of Color, accessed 2026](../bibliography.md#w3c-wai-use-of-color-accessed-2026), and [W3C/WAI Status Messages, accessed 2026](../bibliography.md#w3c-wai-status-messages-accessed-2026) | skim | Audio controls, not relying on color alone, and accessible dynamic status feedback. |

**Prototype evidence:** The system-design UI requirements and the workflow
acceptance checklist define what the next Streamlit UI pass should demonstrate:
one primary action per state, clear tray-status hierarchy, actionable review
reasons, fast correction/rescan, optional audio, restrained alerts, and final
human confirmation.

**Ownership note:** _Write this after reading._

**Open questions:** Which UI states must be shown in the final demo screenshot
pack: complete, missing, extra, review-needed, rescan recommended, camera error,
or all of them?

### C4: Product Space Is Real But Early

**Plain-English version:** TrayGuard is entering a real product/research space,
but existing products and studies mostly support feasibility and direction, not
full validation of this prototype.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Sayani et al., 2018](../bibliography.md#sayani-et-al-2018) | skim | Patent concept: detect present instruments and compare to expected list. |
| [SteelcoBelimed, accessed 2026](../bibliography.md#steelcobelimed-accessed-2026) | skim | Commercial guided-packing framing. |
| [American Hospital Association, 2023](../bibliography.md#american-hospital-association-2023) | skim | Wellstar/RIF Robotics pilot signal and staff-feedback angle. |
| [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025) | deep | CSSD-oriented structured capture and fine-grained classification scope. |
| [Deol et al., 2024](../bibliography.md#deol-et-al-2024) | deep | Automated detection/counting feasibility and validation limits. |

**Prototype evidence:** The project differentiates itself by focusing on
controlled tray-level risk tests and bounded claims.

**Ownership note:** _Write this after reading._

**Open questions:** Which existing system will you compare TrayGuard to in the
presentation, and what is the cleanest distinction?

### C5: Main CV Risks

**Plain-English version:** Average detection accuracy is not enough. The system
has to be tested against the visual conditions most likely to create unsafe
tray results.

**Primary sources to read:**

| Risk | Sources | Depth | What To Extract |
| --- | --- | --- | --- |
| Lighting/glare | [Wang et al., 2016](../bibliography.md#wang-et-al-2016), [Wei et al., 2018](../bibliography.md#wei-et-al-2018) | skim | Why specular highlights are hard for vision. |
| Occlusion/clutter | [Ahmed et al., 2021](../bibliography.md#ahmed-et-al-2021), [Ning et al., 2021](../bibliography.md#ning-et-al-2021) | skim | Why hidden object parts degrade detection. |
| Similar tools | [Wang et al., 2021](../bibliography.md#wang-et-al-2021), [Zhao et al., 2017](../bibliography.md#zhao-et-al-2017) | skim | Why fine-grained recognition needs pairwise analysis. |
| Unknown objects | [Scheirer et al., 2013](../bibliography.md#scheirer-et-al-2013), [Schlachter et al., 2020](../bibliography.md#schlachter-et-al-2020) | deep | Why closed-set accuracy does not prove unknown rejection. |
| Confidence and thresholds | [Guo et al., 2017](../bibliography.md#guo-et-al-2017), [Küppers et al., 2022](../bibliography.md#kuppers-et-al-2022), [Wenkel et al., 2021](../bibliography.md#wenkel-et-al-2021), and [Geifman and El-Yaniv, 2017](../bibliography.md#geifman-and-el-yaniv-2017) | skim | Why confidence is not automatically a calibrated probability; why object-detection thresholds trade false positives against false negatives; why review/reject bands are defensible. |

**Prototype evidence:** The four CV experiment pages map directly to these
risks, and the system design now defines `T_review`, `T_present`, and
scan-quality gating as the required bridge from detector confidence to
user-facing tray labels:
[`shape_similarity.md`](../experiments/cv/shape_similarity.md),
[`reflectivity_lighting.md`](../experiments/cv/reflectivity_lighting.md),
[`clutter_occlusion.md`](../experiments/cv/clutter_occlusion.md), and
[`open_set_confidence.md`](../experiments/cv/open_set_confidence.md).

**Ownership note:** _Write this after reading._

**Open questions:** Which CV risk is most important to demonstrate live or with
figures?

### C6: Prototype Evidence, Not Deployment Readiness

**Plain-English version:** The project can show controlled feasibility and
failure-mode awareness. It cannot claim real SPD deployment readiness without
real instruments, local validation, and workflow testing.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025) | deep | High accuracy in structured CSSD capture, plus task-scope limits. |
| [Deol et al., 2024](../bibliography.md#deol-et-al-2024) | deep | Counting feasibility, metrics, and clinical-validation caveat. |
| [Lehr et al., 2023](../bibliography.md#lehr-et-al-2023) | skim | Controlled single-instrument recognition assumptions. |
| [Rodrigues et al., 2022a](../bibliography.md#rodrigues-et-al-2022a) | skim | Dataset limitations in surgical-tool research. |
| [Tikhomirov et al., 2026](../bibliography.md#tikhomirov-et-al-2026) and [Yang et al., 2024](../bibliography.md#yang-et-al-2024) | skim | Local validation and distribution-shift caution. |

**Prototype evidence:** Local metrics, controlled splits, screenshots, and
reproducibility docs.

**Ownership note:** _Write this after reading._

**Open questions:** What is the strongest claim you can make without
overstating?

### C7: Traceability And Reporting

**Plain-English version:** TrayGuard's value is not only live detection. It can
also create records that help teams see repeated missing-item, correction,
lighting, clutter, and model-failure patterns.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024) | deep | Underreporting and delay-analysis limitations. |
| [Fayad et al., 2025](../bibliography.md#fayad-et-al-2025) | skim | Traceability value for safety, cost, logistics, and risk analysis. |
| [Heil et al., 2021](../bibliography.md#heil-et-al-2021) | skim | Why ML work should report data/model details. |

**Prototype evidence:** Minimum tray-check record schema, saved detections,
confidence values, review flags, corrections, screenshots, dataset version, and
model version.

**Ownership note:** _Write this after reading._

**Open questions:** What would one example quality report show?

### C8: Reproducible Engineering Pipeline

**Plain-English version:** A capstone prototype is stronger when someone can
rerun the important experiments and see how datasets, splits, metrics, and
figures were produced.

**Primary artifacts to verify:**

| Artifact | Depth | What To Check |
| --- | --- | --- |
| [`../experiments/reproducibility/brightness_yolo_reproducibility.md`](../experiments/reproducibility/brightness_yolo_reproducibility.md) | verify | Commands, outputs, and limitations are clear. |
| [`../experiments/reproducibility/lighting_yolo_reproducibility.md`](../experiments/reproducibility/lighting_yolo_reproducibility.md) | verify | Lighting stages and result locations are clear. |
| [`../experiments/reproducibility/shape_similarity_yolo_reproducibility.md`](../experiments/reproducibility/shape_similarity_yolo_reproducibility.md) | verify | Manifests, split logic, and validation commands are clear. |

**Prototype evidence:** Dataset manifests, training commands, validation
outputs, plots, and summary JSON files.

**Ownership note:** _Write this after verifying._

**Open questions:** Which commands do you actually need to rerun before
submission, and which can be checked by reading saved outputs?

### C9: Portable Board-Mounted Camera Stand

**Plain-English version:** We are not choosing the existing stand just because
we already own it. We are choosing it because a rigid overhead fixture gives
repeatable camera geometry, and mounting it to a portable board preserves that
stability without permanently modifying a table or blocking the user.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025) | skim | Structured capture and multi-view station as evidence that camera placement is part of the system. |
| [Lehr et al., 2023](../bibliography.md#lehr-et-al-2023) and [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b) | skim | Controlled acquisition variables for surgical-tool recognition. |
| [Cambo, accessed 2026](../bibliography.md#cambo-accessed-2026) | skim | Copy-stand pattern: baseboard, column, adjustable camera arm, leveling, and vibration control. |
| [Meiji Techno, accessed 2026](../bibliography.md#meiji-techno-accessed-2026) | skim | Boom-stand pattern: support from the side/rear while clearing the workstation. |
| [CDC/NIOSH, 2024](../bibliography.md#cdc-niosh-2024) and [OSHA, accessed 2026](../bibliography.md#osha-computer-workstations-accessed-2026) | skim | Ergonomic basis for fitting tools/equipment to workers, easy reach, and neutral posture. |

**Prototype evidence:** The existing stand already provides the vertical column
and overhead arm. The board-mounted build needs local verification for board
size, tipping risk, anti-slip behavior, camera field of view, and setup time.

**Ownership note:** _Write this after reading and measuring the build._

**Open questions:** What board size and ballast weight give a stable setup
when the camera arm is fully extended?

### C10: Material And Cleanability Boundary

**Plain-English version:** The prototype can use plywood, inexpensive white or
stainless-look surface skins, and the existing camera stand to stabilize image
capture. Those choices should be described as budget-conscious visual
approximations for CV testing, not as lab/demo proof of SPD cleanability. A real
SPD pilot would need smooth, nonporous, facility-approved materials and a
cleaning protocol reviewed against local infection-prevention requirements.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [CDC](../bibliography.md#cdc) and [CDC Healthcare Equipment, accessed 2026](../bibliography.md#cdc-healthcare-equipment-accessed-2026) | skim | Difference between critical/semicritical/noncritical items and environmental-surface disinfection expectations. |
| [CDC Environmental Surfaces, accessed 2026](../bibliography.md#cdc-environmental-surfaces-accessed-2026) | skim | Environmental surfaces are lower risk but still need cleaning/disinfection schedules. |
| [FDA Reprocessing, accessed 2026](../bibliography.md#fda-reprocessing-accessed-2026) | skim | Reprocessing is specific to intended use, materials, and device design. |
| [FDA Reprocessing Factors, accessed 2026](../bibliography.md#fda-reprocessing-factors-accessed-2026) | skim | Design features that retain debris and the need to validate cleaning instructions. |
| [Con-Tact Shelf Liner, accessed 2026](../bibliography.md#contact-shelf-liner-accessed-2026), [Con-Tact Stainless-Look Liner, accessed 2026](../bibliography.md#contact-stainless-liner-accessed-2026), and [U.S. Plastic, accessed 2026](../bibliography.md#us-plastic-hdpe-accessed-2026) | skim | Cost and visual/material basis for cheap versus more realistic surface options. |

**Prototype evidence:** The current stand and board can be inspected for
crevices, wipeable surfaces, cable contact, whether the board remains outside
the direct tray-contact zone, and whether the cheap visual skin produces
acceptable camera contrast/glare behavior.

**Ownership note:** _Write this after deciding whether the final demo will use
raw plywood, sealed plywood, plastic, or metal._

**Open questions:** What material will the final physical prototype use, what
surface-glare check will justify it for CV, and what one-paragraph cleaning
protocol will be shown in the final design package?

### C11: Tabletop Default With Rolling Standing Option

**Plain-English version:** TrayGuard should not assume every SPD task happens
at the same posture, table height, or workstation type. The tabletop module
fits seated or existing-table workflows, while the rolling standing base lets
the same camera module dock into standing metal-table or cart-like workflows
without rebuilding the capture fixture.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [OSHA Central Sterile Supply, accessed 2026](../bibliography.md#osha-central-sterile-supply-accessed-2026) | skim | Reaching, standing, carts, height-adjustable surfaces, and sit/stand controls for sterile supply ergonomics. |
| [Skytron, accessed 2026](../bibliography.md#skytron-prep-pack-accessed-2026), [Getinge, accessed 2026](../bibliography.md#getinge-prep-pack-accessed-2026), and [Southwest Solutions CSSD Tables, accessed 2026](../bibliography.md#southwest-cssd-tables-accessed-2026) | skim | Commercial SPD workstations are flexible, ergonomic, height-adjustable, accessory-rich, and designed around different users/tasks. |
| [User-provided SPD video 1](../bibliography.md#user-spd-video-1-accessed-2026) and [User-provided SPD video 2](../bibliography.md#user-spd-video-2-accessed-2026) | verify visually | Real SPD-adjacent visual references show both seated tabletop and standing metal-table workflows. |

**Prototype evidence:** The same board-mounted camera module can be placed on a
table or secured to a rolling base. Verification should measure setup time,
field-of-view consistency after docking, caster locking stability, and whether
the camera/stand blocks hands or tray movement.

**Ownership note:** _Write this after building or mocking up both modes._

**Open questions:** What is the minimum rolling-base footprint and lock/clamp
method that keeps the docked module stable without making it awkward to move?

### C12: Student Participants Are Novice Evidence

**Plain-English version:** College students are not equivalent to SPD
technicians. Their value is in testing whether a complete novice can understand
a tray-like checklist verification task, use review prompts, catch planted
missing/extra/wrong items, and avoid blindly accepting automation. This supports
a learnability and onboarding-friction claim, not a deployment or adoption
claim.

**Primary sources to read:**

| Source | Depth | What To Extract |
| --- | --- | --- |
| [Workflow acceptance student caveat](../experiments/adoption/workflow_acceptance.md#college-student-participant-caveat) | deep | The exact boundary between novice evidence and SPD adoption evidence. |
| [Goddard et al., 2012](../bibliography.md#goddard-et-al-2012) | skim | Why novice over-reliance can make an automation feel easy while introducing risk. |
| [Hu et al., 2024](../bibliography.md#hu-et-al-2024) and [Chobin, 2010](../bibliography.md#chobin-2010) | skim | Why training burden and structured onboarding are relevant to the product story. |
| [Chen, Stavropoulou, et al., 2021](../bibliography.md#chen-stavropoulou-et-al-2021) | skim | Why healthcare technology adoption is role-specific and affected by knowledge, autonomy, and professional identity. |

**Prototype evidence:** A student walkthrough can compare manual checklist
performance against TrayGuard-assisted performance on tray-like scenarios with
planted missing, extra, wrong-but-similar, hidden, and unknown items. The study
should record whether students understand the reason for a flag, not only
whether they agree with the system.

**Ownership note:** _Write this after running the walkthrough._

**Open questions:** Which exact sentence will you use in the final report to
avoid implying that student results prove SPD adoption?

## Reading Order

1. C1, C3, and C6 first. These are the spine of the project.
2. C5 next. This connects the engineering experiments to the argument.
3. C2 and C4 after that. These help with positioning and comparison.
4. C9, C10, and C11 before hardware review or demo setup.
5. C12 before presenting user-study results.
6. C7 and C8 last. These strengthen the quality and reproducibility story.

## Final Presentation Compression

If you only have time to defend the core claims, use these:

1. Tray errors are real and often visual.
2. CV is a reasonable low-infrastructure prototype, but not a universal
   replacement for RFID/barcode tracking or staff expertise.
3. TrayGuard is an assistant with human confirmation, not autonomous approval.
4. The core CV risks are lighting, occlusion, similar tools, unknowns, and
   confidence behavior.
5. The experiments provide controlled prototype evidence, not deployment
   readiness.
6. Logs and reports matter because they turn one-off detections into quality
   improvement evidence.
7. The camera fixture is portable and structured: it preserves repeatable
   overhead capture without requiring table modification.
8. Plywood is a prototype simplification; an SPD-facing version needs
   cleanable, nonporous materials and a reviewed cleaning protocol.
9. Tabletop plus rolling dock is a workflow-fit compromise: it supports seated
   and standing SPD-style work without forcing one fixed workstation design.
10. Student walkthroughs are novice learnability evidence, not proof of SPD
    technician adoption.
