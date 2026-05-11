# Claim-Evidence Control Sheet

Use this as the project ownership map. The active goal is to defend a
training-centered project, not to defend local CV accuracy experiments.

## Claim Index

| ID | Claim To Defend | Canonical Home | Read Depth | Status |
| --- | --- | --- | --- | --- |
| C1 | Surgical tray errors are real, costly, and tied to local visual identification, missing items, wrong items, damaged tools, workflow pressure, and training. | [`../../context/problem_explication.md`](../../context/problem_explication.md) | deep | not started |
| C1a | Tray assembly is a high-friction subtask inside SPD education, but it should not be claimed as the only or main bottleneck without site-specific evidence. | [`../../context/problem_explication.md`](../../context/problem_explication.md#why-tray-assembly-is-a-high-friction-subtask) | deep | not started |
| C2 | TrayGuard should be framed as training and assessment support, not certification, autonomous tray approval, or deployment-ready SPD automation. | [`../system_design.md`](../system_design.md#prototype-scope) | deep | not started |
| C3 | Existing CV papers make computer vision plausible enough to treat as future support; our project does not need to prove mAP or hospital robustness. | [`../evaluation/adoption/formal_risk_analysis.md`](../evaluation/adoption/formal_risk_analysis.md#literature-backed-risk-factors) | skim | not started |
| C4 | The major literature gap is not "can any detector work"; it is training transfer, local content, workflow fit, stakeholder value, and site-specific validation. | [`../evaluation/adoption/formal_risk_analysis.md`](../evaluation/adoption/formal_risk_analysis.md#stakeholder-implications) | deep | not started |
| C5 | TrayGuard's training workflow should use study, retrieval practice, simulation, feedback, and pre/post assessment because these patterns are supported by medical simulation and learning-science evidence. | [`../../context/problem_explication.md`](../../context/problem_explication.md#training-pipeline-evidence) | deep/skim | not started |
| C6 | Reducing time to competency is the right north-star goal, but this prototype can only measure simulated time-to-competency proxies unless it runs a longitudinal SPD study. | [`../training_module_design.md`](../training_module_design.md) | deep | not started |
| C7 | College-student walkthroughs support novice learnability and checklist-style task clarity, not SPD technician adoption or hospital safety readiness. | [`../evaluation/adoption/workflow_acceptance.md`](../evaluation/adoption/workflow_acceptance.md#college-student-participant-caveat) | deep | not started |
| C8 | Traceability and reporting matter because pre/post metrics, confidence, and repeated error patterns make the system more useful for instructors and administrators. | [`../evaluation/adoption/traceability_reporting.md`](../evaluation/adoption/traceability_reporting.md) | skim | not started |

## Claim Cards

### C1: Tray Errors And Training Burden Are Real

**Plain-English version:** TrayGuard addresses a documented sterile-processing
problem, not an invented demo problem. Existing papers show tray defects,
missing/wrong instruments, local nomenclature problems, and training burdens.

**Primary sources:** [Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021),
[Nichol et al., 2024](../../bibliography.md#nichol-et-al-2024),
[Zhu et al., 2019](../../bibliography.md#zhu-et-al-2019),
[Chobin, 2010](../../bibliography.md#chobin-2010).

**Prototype evidence:** Problem framing and pre/post training plan; no local CV
metric is needed to prove the problem exists.

### C1a: Tray Assembly Is High Friction, But Not The Whole Bottleneck

**Plain-English version:** TrayGuard does not need to prove that sorting is the
single biggest barrier in SPD education. The safer claim is that instrument
identity, count-sheet interpretation, and tray assembly are major,
experience-sensitive tasks within the broader training pipeline.

**Primary sources:** [HSPA CRCST](../../bibliography.md#hspa-crcst-accessed-2026),
[HSPA CRCST Content Outline](../../bibliography.md#hspa-crcst-content-outline-2023),
[Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021),
[Nichol et al., 2024](../../bibliography.md#nichol-et-al-2024),
[Zhu et al., 2019](../../bibliography.md#zhu-et-al-2019).

**Prototype evidence:** Simulated tray assembly/sorting improvement, weak-item
reports, and explicit scope language that this is not full SPD certification
training.

### C2: Training Support, Not Certification

**Plain-English version:** The safest claim is a training and assessment tool.
It can guide practice, classify errors, and export evidence. It cannot certify
a technician or replace supervised hands-on hours.

**Primary sources:** [HSPA CRCST](../../bibliography.md#hspa-crcst-accessed-2026),
[CBSPD Technician Exam](../../bibliography.md#cbspd-technician-accessed-2026),
[Goddard et al., 2012](../../bibliography.md#goddard-et-al-2012),
[Natali et al., 2025](../../bibliography.md#natali-et-al-2025),
[Kelly, 2026](../../bibliography.md#kelly-2026).

**Prototype evidence:** Pre/post assessment boundaries, practice feedback,
learner metrics, and explicit scope limits.

### C3: CV Is Plausible But Bounded

**Plain-English version:** Other people have shown surgical-instrument CV and
few-shot detection are plausible. We can cite that work and stop trying to
prove detector accuracy ourselves.

**Primary sources:** [Deol et al., 2024](../../bibliography.md#deol-et-al-2024),
[Atabuzzaman et al., 2025](../../bibliography.md#atabuzzaman-et-al-2025),
[Xin et al., 2024](../../bibliography.md#xin-et-al-2024),
[Wang et al., 2020 FSOD](../../bibliography.md#wang-et-al-2020-fsod),
[Kienle et al., 2025](../../bibliography.md#kienle-et-al-2025).

**Prototype evidence:** None required beyond clear boundary language. The CV
code remains optional future support.

### C4: The Real Gap Is Stakeholder Transfer

**Plain-English version:** Existing papers gloss over whether a tool improves
novice learning, fits SPD workflows, persuades hospital administrators, or
transfers from students to real technicians.

**Primary sources:** [Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021),
[Chomutare et al., 2022](../../bibliography.md#chomutare-et-al-2022),
[Jiang et al., 2025](../../bibliography.md#jiang-et-al-2025),
[Kastrup et al., 2024](../../bibliography.md#kastrup-et-al-2024).

**Prototype evidence:** Stakeholder-specific interpretation in the formal risk
analysis and workflow acceptance docs.

### C5: The Learning Loop Is Evidence-Based

**Plain-English version:** Study, retrieval, simulation, feedback, and pre/post
assessment are supported by sterile-processing training, medical simulation,
and learning-science research.

**Primary sources:** [Ofstead et al., 2023](../../bibliography.md#ofstead-et-al-2023),
[Hu et al., 2024](../../bibliography.md#hu-et-al-2024),
[Cook et al., 2011](../../bibliography.md#cook-et-al-2011),
[McGaghie et al., 2011](../../bibliography.md#mcgaghie-et-al-2011),
[Roediger and Karpicke, 2006](../../bibliography.md#roediger-and-karpicke-2006),
[Hattie and Timperley, 2007](../../bibliography.md#hattie-and-timperley-2007).

**Prototype evidence:** One complete local tray module and paired pre/post
results.

### C6: Simulated Time-To-Competency Is The Metric

**Plain-English version:** The right north star is reducing time to competency,
but the capstone can only measure a proxy: whether learners improve on a
simulated local tray task.

**Primary sources:** [Chobin, 2010](../../bibliography.md#chobin-2010),
[AORN Staff, 2025](../../bibliography.md#aorn-staffing-shortage-2025),
[Arthur et al., 2003](../../bibliography.md#arthur-et-al-2003),
[Salas et al., 2012](../../bibliography.md#salas-et-al-2012).

**Prototype evidence:** Pre/post accuracy, duration, confidence, and error
breakdown.

### C7: Students Are Novices, Not SPD Proxies

**Plain-English version:** Student participants can test clarity and novice
learning, but they cannot prove SPD adoption or safety readiness.

**Primary sources:** [Cook et al., 2011](../../bibliography.md#cook-et-al-2011),
[McGaghie et al., 2011](../../bibliography.md#mcgaghie-et-al-2011),
[Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021).

**Prototype evidence:** Report as novice learnability only.

### C8: Reporting Helps Instructors And Admins

**Plain-English version:** The output matters because instructors and admins
need to see repeated errors, weak instruments, and whether the module is
actually helping.

**Primary sources:** [Fayad et al., 2025](../../bibliography.md#fayad-et-al-2025),
[Nichol and Saari, 2023](../../bibliography.md#nichol-and-saari-2023),
[Vithlani et al., 2023](../../bibliography.md#vithlani-et-al-2023),
[Kastrup et al., 2024](../../bibliography.md#kastrup-et-al-2024).

**Prototype evidence:** Metrics export and example instructor/admin summary.
