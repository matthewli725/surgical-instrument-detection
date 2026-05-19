# Claim-Evidence Control Sheet

Use this as the project ownership map. The active goal is to defend a
training-centered project with local tray modules, simulated practice, pre/post
metrics, and instructor-facing evidence.

## Claim Index

| ID | Claim To Defend | Canonical Home | Read Depth | Status |
| --- | --- | --- | --- | --- |
| C1 | Surgical tray errors are real, costly, and tied to local visual identification, missing items, wrong items, damaged tools, workflow pressure, and training. | [`../../context/problem_explication.md`](../../context/problem_explication.md) | deep | not started |
| C1a | Tray assembly is a high-friction subtask inside SPD education because it combines instrument identity, count-sheet interpretation, and visual verification. | [`../../context/problem_explication.md`](../../context/problem_explication.md#why-tray-assembly-is-a-high-friction-subtask) | deep | not started |
| C2 | TrayGuard should be framed as training and assessment support that guides practice, classifies errors, and exports instructor-review evidence. | [`../system_design.md`](../system_design.md#prototype-scope) | deep | not started |
| C3 | Existing CV papers make computer vision plausible enough to treat as future authoring or review support. | [`../evaluation/adoption/formal_risk_analysis.md`](../evaluation/adoption/formal_risk_analysis.md#literature-backed-risk-factors) | skim | not started |
| C4 | The major literature gap is training transfer, local content, workflow fit, stakeholder value, and site-specific validation. | [`../evaluation/adoption/formal_risk_analysis.md`](../evaluation/adoption/formal_risk_analysis.md#stakeholder-implications) | deep | not started |
| C5 | TrayGuard's training workflow should center retrieval practice, then connect it to applied tray sorting, feedback, spacing, and pre/post assessment. | [`../../context/problem_explication.md`](../../context/problem_explication.md#training-pipeline-evidence) | deep/skim | not started |
| C6 | Simulated tray-task proficiency is the right capstone metric for the current prototype. | [`../training_module_design.md`](../training_module_design.md) | deep | not started |
| C7 | College-student walkthroughs support novice learnability and checklist-style task clarity. | [`../evaluation/adoption/workflow_acceptance.md`](../evaluation/adoption/workflow_acceptance.md#college-student-participant-role) | deep | not started |
| C8 | Traceability and reporting matter because pre/post metrics, confidence, and repeated error patterns make the system more useful for instructors and administrators. | [`../evaluation/adoption/traceability_reporting.md`](../evaluation/adoption/traceability_reporting.md) | skim | not started |

## Claim Cards

### C1: Tray Errors And Training Burden Are Real

**Plain-English version:** TrayGuard addresses a documented sterile-processing
problem. Existing papers show tray defects, missing/wrong instruments, local
nomenclature problems, and training burdens.

**Primary sources:** [Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021),
[Nichol et al., 2024](../../bibliography.md#nichol-et-al-2024),
[Zhu et al., 2019](../../bibliography.md#zhu-et-al-2019),
[Chobin, 2010](../../bibliography.md#chobin-2010).

**Prototype evidence:** Problem framing and pre/post training plan; no local CV
metric is needed to prove the problem exists.

### C1a: Tray Assembly Is High Friction, But Not The Whole Bottleneck

**Plain-English version:** Instrument identity, count-sheet interpretation, and
tray assembly are major, experience-sensitive tasks within the broader SPD
training pipeline.

**Primary sources:** [HSPA CRCST](../../bibliography.md#hspa-crcst-accessed-2026),
[HSPA CRCST Content Outline](../../bibliography.md#hspa-crcst-content-outline-2023),
[Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021),
[Nichol et al., 2024](../../bibliography.md#nichol-et-al-2024),
[Zhu et al., 2019](../../bibliography.md#zhu-et-al-2019),
[Penn Foster, accessed 2026](../../bibliography.md#penn-foster-sterile-processing-accessed-2026),
[Central Sterilization Solutions, accessed 2026](../../bibliography.md#central-sterilization-solutions-in-person-accessed-2026),
[AIMS Education, accessed 2026](../../bibliography.md#aims-education-sterile-processing-accessed-2026),
[Altamont Externship, accessed 2026](../../bibliography.md#altamont-externship-accessed-2026),
[McBride et al., 2020](../../bibliography.md#mcbride-et-al-2020),
[North Greater Sacramento COE, 2025](../../bibliography.md#north-greater-sacramento-coe-2025).

**Prototype evidence:** Simulated tray assembly/sorting improvement, weak-item
reports, and a link to
[`scope_boundaries_and_risks.md`](../scope_boundaries_and_risks.md).

### C2: Training Support And Instructor Review

**Plain-English version:** The safest claim is a training and assessment tool.
It can guide practice, classify errors, and export evidence for instructor
review.

**Primary sources:** [HSPA CRCST](../../bibliography.md#hspa-crcst-accessed-2026),
[CBSPD Technician Exam](../../bibliography.md#cbspd-technician-accessed-2026),
[MedCerts Catalog, 2025](../../bibliography.md#medcerts-catalog-2025),
[Goddard et al., 2012](../../bibliography.md#goddard-et-al-2012),
[Natali et al., 2025](../../bibliography.md#natali-et-al-2025),
[Kelly, 2026](../../bibliography.md#kelly-2026).

**Prototype evidence:** Pre/post assessment boundaries, practice feedback,
learner metrics, and consolidated scope boundaries.

### C3: CV Is Plausible But Bounded

**Plain-English version:** Other people have shown surgical-instrument CV and
few-shot detection are plausible. We can cite that work and treat CV as future
support-layer infrastructure.

**Primary sources:** [Deol et al., 2024](../../bibliography.md#deol-et-al-2024),
[Atabuzzaman et al., 2025](../../bibliography.md#atabuzzaman-et-al-2025),
[Xin et al., 2024](../../bibliography.md#xin-et-al-2024),
[Wang et al., 2020 FSOD](../../bibliography.md#wang-et-al-2020-fsod),
[Kienle et al., 2025](../../bibliography.md#kienle-et-al-2025).

**Prototype evidence:** Clear boundary language and optional CV support code.

### C4: The Real Gap Is Stakeholder Transfer

**Plain-English version:** Existing papers leave open whether a tool improves
novice learning, fits SPD workflows, persuades hospital administrators, or
transfers from students to real technicians.

**Primary sources:** [Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021),
[Chomutare et al., 2022](../../bibliography.md#chomutare-et-al-2022),
[Jiang et al., 2025](../../bibliography.md#jiang-et-al-2025),
[Kastrup et al., 2024](../../bibliography.md#kastrup-et-al-2024).

**Prototype evidence:** Stakeholder-specific interpretation in the formal risk
analysis and workflow acceptance docs.

### C5: The Retrieval-Centered Learning Loop Is Evidence-Based

**Plain-English version:** Retrieval practice should be the center of the
learning loop. Retrieval-first cards orient learners, while prompt-before-answer
recall, applied tray sorting, feedback, weak-item repetition, and pre/post
assessment are the evidence-backed pieces.

**Primary sources:** [Ofstead et al., 2023](../../bibliography.md#ofstead-et-al-2023),
[Hu et al., 2024](../../bibliography.md#hu-et-al-2024),
[Fast et al., 2019](../../bibliography.md#fast-et-al-2019),
[Shreckengost et al., 2022](../../bibliography.md#shreckengost-et-al-2022),
[Cook et al., 2011](../../bibliography.md#cook-et-al-2011),
[McGaghie et al., 2011](../../bibliography.md#mcgaghie-et-al-2011),
[Roediger and Karpicke, 2006](../../bibliography.md#roediger-and-karpicke-2006),
[Karpicke and Blunt, 2011](../../bibliography.md#karpicke-and-blunt-2011),
[Larsen et al., 2009](../../bibliography.md#larsen-et-al-2009),
[Martinengo et al., 2024](../../bibliography.md#martinengo-et-al-2024),
[Barrison et al., 2025](../../bibliography.md#barrison-et-al-2025),
[Hattie and Timperley, 2007](../../bibliography.md#hattie-and-timperley-2007).

**Prototype evidence:** One complete local tray module, weak-item review data,
and paired pre/post results.

### C6: Simulated Tray-Task Proficiency Is The Metric

**Plain-English version:** The prototype can measure whether learners improve
accuracy, speed, error recovery, and confidence on a simulated local tray task.

**Primary sources:** [Chobin, 2010](../../bibliography.md#chobin-2010),
[AORN Staff, 2025](../../bibliography.md#aorn-staffing-shortage-2025),
[HSPA CRCST](../../bibliography.md#hspa-crcst-accessed-2026),
[Arthur et al., 2003](../../bibliography.md#arthur-et-al-2003),
[Salas et al., 2012](../../bibliography.md#salas-et-al-2012).

**Prototype evidence:** Pre/post accuracy, duration, confidence, and error
breakdown.

### C7: Students Are Novice Learners

**Plain-English version:** Student participants can test clarity and novice
learning. SPD adoption and safety readiness require later workplace validation.

**Primary sources:** [Cook et al., 2011](../../bibliography.md#cook-et-al-2011),
[McGaghie et al., 2011](../../bibliography.md#mcgaghie-et-al-2011),
[Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021).

**Prototype evidence:** Report as novice learnability and link to the study
boundary in
[`scope_boundaries_and_risks.md`](../scope_boundaries_and_risks.md#study-boundary).

### C8: Reporting Helps Instructors And Admins

**Plain-English version:** The output matters because instructors and admins
need to see repeated errors, weak instruments, and whether the module is
actually helping.

**Primary sources:** [Fayad et al., 2025](../../bibliography.md#fayad-et-al-2025),
[Nichol and Saari, 2023](../../bibliography.md#nichol-and-saari-2023),
[Vithlani et al., 2023](../../bibliography.md#vithlani-et-al-2023),
[Kastrup et al., 2024](../../bibliography.md#kastrup-et-al-2024).

**Prototype evidence:** Metrics export and example instructor/admin summary.
