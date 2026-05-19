# Scope Boundaries And Risks

This page consolidates the claims that require explicit boundary management.
The main TrayGuard documents should describe the proposed system in terms of
capabilities, measures, workflows, and evidence. This page should carry the
separate clarification work: certification boundaries, clinical-transfer
risks, computer-vision limits, and physical-prototype constraints.

## Capability Boundary

TrayGuard measures simulated local tray-task proficiency. The current prototype
can load an instructor-verified tray module, guide retrieval-first study, run
quiz and practice-sort modes, classify sorting errors, capture confidence, and
export paired pre/post learning metrics. The measurable claim is improvement in
novice accuracy, duration, error recovery, and confidence on comparable
simulated tray tasks.

TrayGuard does not certify sterile-processing competence, satisfy CRCST or
CSPDT eligibility requirements, replace supervised hands-on hours, or approve a
technician for unsupervised SPD work. HSPA requires 400 hands-on hours for
CRCST, and CBSPD eligibility routes also depend on exam and experience or
course pathways ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026),
[CBSPD Technician Exam, accessed 2026](../bibliography.md#cbspd-technician-accessed-2026)).
Therefore, TrayGuard should be presented as practice evidence and instructor
review support.

## Study Boundary

The current evaluation can test novice learnability and simulated training
gain. Student or class participants can show whether first-time users complete
the workflow, understand feedback, improve on comparable tray tasks, and
produce interpretable learner reports.

Student results do not establish SPD technician adoption, clinical safety,
hospital ROI, reduced OR delays, or reduced real tray-defect rates. Those
claims require SPD participants, local count sheets, supervised workplace
tasks, operational outcome data, and longitudinal follow-up. Existing
simulation and learning-science evidence supports early novice studies, while
SPD certification and work-system evidence still require supervised competence
for practice settings ([Cook et al., 2011](../bibliography.md#cook-et-al-2011),
[McGaghie et al., 2011](../bibliography.md#mcgaghie-et-al-2011),
[Alfred et al., 2021](../bibliography.md#alfred-et-al-2021)).

## Clinical Scope Boundary

TrayGuard's current module focuses on local instrument identity, aliases,
distinguishing features, count-sheet quantities, lookalike discrimination, and
simulated tray sorting. These tasks are operationally relevant because tray
defects include missing, wrong, extra, and incorrectly assembled instruments,
and because certification materials include preparation, packaging, count
sheets, item identification, and instrument placement
([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021),
[Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[HSPA CRCST Content Outline, 2023](../bibliography.md#hspa-crcst-content-outline-2023)).

The current prototype does not validate sterility, cleanliness, bioburden
inspection, packaging integrity, sterilizer operation, mechanical function,
sharpness, alignment, IFU compliance, or full departmental quality assurance.
Those topics can become future training modules or workplace validation tasks,
but they require different evidence, assessment procedures, and supervisory
review.

## Local Content Boundary

TrayGuard depends on instructor-verified local modules. Count sheets specify
tray contents, quantities, sizes, and catalog/reference numbers; tray
optimization research models contents around procedures, surgeons, usage
probabilities, and stock decisions; and specialty or loaner trays can add
facility- and vendor-specific variation ([Nadeau, 2024](../bibliography.md#nadeau-2024),
[dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021),
[Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023),
[STERIS, 2021](../bibliography.md#steris-loaner-trays-2021)).

TrayGuard does not provide a universal hospital count sheet or guarantee
coverage of every manufacturer variant. The proposed capability is a file-backed
local module workflow in which educators verify names, aliases, photos,
quantities, distractors, lookalike pairs, and module versions before learner
use.

## Computer-Vision Boundary

Computer vision remains a plausible support layer for authoring assistance,
camera-supported practice, or future visual review. Existing work reports
bounded surgical-instrument detection, counting, and fine-grained
classification results, including data-efficient and CSSD-oriented approaches
([Deol et al., 2024](../bibliography.md#deol-et-al-2024),
[Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025),
[Xin et al., 2024](../bibliography.md#xin-et-al-2024),
[Wang et al., 2020 FSOD](../bibliography.md#wang-et-al-2020-fsod)).

The current project does not use local detector metrics as its central proof.
Deployment-grade CV robustness would require site-specific validation across
instrument variants, manufacturers, camera geometry, lighting, glare,
occlusion, tray layouts, staff behavior, false-alarm handling, and open-set
objects. Kienle et al. show why this boundary matters: strong in-domain
instrument-stand detection can drop substantially on instruments from different
manufacturers ([Kienle et al., 2025](../bibliography.md#kienle-et-al-2025)).

## Reporting Boundary

TrayGuard reports learner practice evidence. A useful report can show pre/post
accuracy, duration, confidence, high-confidence errors, low-confidence correct
answers, missing items, extra items, wrong substitutions, lookalike
misidentifications, wrong counts, weak-item recovery, and module version.

Training reports do not replace departmental quality systems, sterilization
records, incident reporting, competency sign-off, or hospital audit trails.
They support instructor review and future pilot planning by making repeated
practice errors visible.

## Physical Prototype Boundary

The board-mounted camera stand is a prototype fixture for stable image capture
and demonstration. It can support repeatable camera geometry, a low-cost
tabletop setup, and future camera-assisted authoring experiments.

The physical prototype does not validate clinical materials, sterility,
disinfectant compatibility, reprocessing, cable-management safety, or SPD
deployment readiness. Plywood and adhesive skins are acceptable for low-risk
demo iteration; an SPD-facing pilot would require a smooth nonporous surface,
facility-approved cleaning procedures, cable management, infection-prevention
review, and local equipment approval. CDC and FDA guidance support regular
cleaning of environmental surfaces and design attention to surfaces that retain
debris ([CDC Environmental Surfaces, accessed 2026](../bibliography.md#cdc-environmental-surfaces-accessed-2026),
[FDA Reprocessing Factors, accessed 2026](../bibliography.md#fda-reprocessing-factors-accessed-2026)).
