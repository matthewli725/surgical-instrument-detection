# Formal Risk Analysis

TrayGuard should no longer be evaluated as a local computer-vision experiment.
The active project claim is educational: a novice uses a local tray module,
practices instrument identification and simulated sorting, and shows measurable
pre/post improvement. Computer vision remains a plausible future support layer
because other groups have already shown surgical-instrument CV can work in
bounded settings.

The risk analysis therefore uses existing papers as the evidence base. Our
local work should fill the training and workflow gap, not try to prove
deployment-grade CV accuracy.

## Core Claim

Existing literature supports three things at once:

- SPD assembly errors, training burden, and workflow variability are real
  problems ([Alfred et al., 2021](../../../bibliography.md#alfred-et-al-2021),
  [Nichol et al., 2024](../../../bibliography.md#nichol-et-al-2024),
  [Chobin, 2010](../../../bibliography.md#chobin-2010)).
- Computer vision for surgical instruments is technically plausible in
  constrained settings ([Deol et al., 2024](../../../bibliography.md#deol-et-al-2024),
  [Atabuzzaman et al., 2025](../../../bibliography.md#atabuzzaman-et-al-2025),
  [Xin et al., 2024](../../../bibliography.md#xin-et-al-2024),
  [Wang et al., 2020 FSOD](../../../bibliography.md#wang-et-al-2020-fsod)).
- Robust hospital deployment, cross-manufacturer generalization, training
  transfer, and adoption economics are not solved by those papers
  ([Kienle et al., 2025](../../../bibliography.md#kienle-et-al-2025),
  [Chomutare et al., 2022](../../../bibliography.md#chomutare-et-al-2022),
  [Kastrup et al., 2024](../../../bibliography.md#kastrup-et-al-2024)).

TrayGuard's defensible contribution is the gap between those points: a
training and assessment workflow that helps novices practice local tray
knowledge and gives instructors/admins usable evidence without claiming
clinical automation.

## Literature-Backed Risk Factors

| Risk Factor | What Existing Papers Show | What The Literature Glosses Over | Meaning For TrayGuard |
| --- | --- | --- | --- |
| SPD assembly is not just recognition | Alfred et al. found assembly defects tied to missing, incorrect, damaged, and extra instruments, shaped by training, production pressure, inventory, nomenclature, technology, and workspace constraints ([Alfred et al., 2021](../../../bibliography.md#alfred-et-al-2021)). | Many technical papers treat the scene as an image-recognition task and understate the local work system around the image. | The system must be a learning/workflow aid with local tray names, aliases, counts, and error categories, not a generic detector demo. |
| Novice training is expensive and local | Chobin reports months of SPD training and a high training cost estimate; HSPA and CBSPD certification pathways require exams and hands-on experience ([Chobin, 2010](../../../bibliography.md#chobin-2010), [HSPA CRCST, accessed 2026](../../../bibliography.md#hspa-crcst-accessed-2026), [CBSPD Technician Exam, accessed 2026](../../../bibliography.md#cbspd-technician-accessed-2026)). | The literature rarely evaluates lightweight software that teaches local tray familiarity before or between supervised shifts. | Measure simulated time-to-competency proxies: accuracy, duration, confidence, and error type before and after practice. |
| Instrument errors have visual and operational consequences | Nichol et al. connect observed instrument errors to visualization tasks and lost OR minutes; Zhu et al. document packaging errors including wrong specifications, incomplete packages, and missing instruments ([Nichol et al., 2024](../../../bibliography.md#nichol-et-al-2024), [Zhu et al., 2019](../../../bibliography.md#zhu-et-al-2019)). | Error studies motivate the problem but do not prove which training intervention reduces errors. | Use these papers for motivation only; our evidence should show novice learning on simulated tray tasks. |
| CV feasibility is already supported elsewhere | Deol et al. report high precision/recall and real-time counting in surgical-tool scenes; Atabuzzaman et al. report CSSD-oriented multi-view fine-grained classification; few-shot detection papers show limited-data adaptation is an established research direction ([Deol et al., 2024](../../../bibliography.md#deol-et-al-2024), [Atabuzzaman et al., 2025](../../../bibliography.md#atabuzzaman-et-al-2025), [Xin et al., 2024](../../../bibliography.md#xin-et-al-2024), [Wang et al., 2020 FSOD](../../../bibliography.md#wang-et-al-2020-fsod)). | Feasibility studies often use bounded datasets, structured capture, selected instrument sets, or proof-of-concept settings. | We can cite CV plausibility instead of spending the project proving mAP. CV should be optional authoring/review support, with human verification. |
| Generalization remains unresolved | Kienle et al. report strong in-domain instrument-stand detection but a large performance drop on instruments from different manufacturers ([Kienle et al., 2025](../../../bibliography.md#kienle-et-al-2025)). | Papers may report strong headline metrics while external site, manufacturer, tray, and staff variation remain thinly tested. | Do not claim real-hospital CV robustness. Let local photos and instructor verification define training modules. |
| Fine-grained lookalikes are a training problem, not only a model problem | HOSPITools and Atabuzzaman et al. highlight subtle visual differences among surgical instruments; Alfred et al. also identify nomenclature and training as assembly factors ([Rodrigues et al., 2022b](../../../bibliography.md#rodrigues-et-al-2022b), [Atabuzzaman et al., 2025](../../../bibliography.md#atabuzzaman-et-al-2025), [Alfred et al., 2021](../../../bibliography.md#alfred-et-al-2021)). | CV papers focus on classifying lookalikes; they say less about how trainees learn the discriminating features. | Study cards and feedback should teach distinguishing features and mark `misidentified` errors separately from generic wrong answers. |
| Automation can create over-reliance and accountability problems | Automation-bias, deskilling, human-centered AI, and clinical-AI deployment literature warn against silent automation in high-stakes work ([Goddard et al., 2012](../../../bibliography.md#goddard-et-al-2012), [Natali et al., 2025](../../../bibliography.md#natali-et-al-2025), [Zheng et al., 2023](../../../bibliography.md#zheng-et-al-2023), [Kelly, 2026](../../../bibliography.md#kelly-2026)). | SPD-specific evidence about AI assistant language, trust, and responsibility is still sparse. | Keep instructor/technician authority explicit. Present results as practice evidence or review support, never autonomous approval. |
| Workflow adoption is broader than technical performance | Healthcare AI implementation work emphasizes workflow fit, infrastructure, leadership, governance, training, privacy, and cost ([Chomutare et al., 2022](../../../bibliography.md#chomutare-et-al-2022), [Jiang et al., 2025](../../../bibliography.md#jiang-et-al-2025), [Lambert et al., 2023](../../../bibliography.md#lambert-et-al-2023), [Grossi et al., 2021](../../../bibliography.md#grossi-et-al-2021)). | There is little direct evidence on how hospitals evaluate an SPD training assistant specifically. | Provide admin-facing metrics: learner progress, preceptor burden hypothesis, repeated errors, pilot scope, privacy boundary, and manual fallback. |
| Student studies have limited external validity | Simulation and learning-science evidence supports novice practice and pre/post assessment, but SPD certification and work-system evidence show real work requires hands-on supervised competence ([Cook et al., 2011](../../../bibliography.md#cook-et-al-2011), [McGaghie et al., 2011](../../../bibliography.md#mcgaghie-et-al-2011), [HSPA CRCST, accessed 2026](../../../bibliography.md#hspa-crcst-accessed-2026), [Alfred et al., 2021](../../../bibliography.md#alfred-et-al-2021)). | A classmate or student participant is not exposed to SPD time pressure, sterility norms, local policies, or accountability. | Report student results as novice learnability and UI clarity only. SPD technician validation remains future work. |

## Stakeholder Implications

### SPD Trainees

The literature implies trainees need repeated local practice, not a magical
recognition model. TrayGuard should help them learn names, aliases, counts,
lookalikes, and distinguishing features before they are expected to perform
under real workflow pressure.

Design consequences:

- keep study cards local and instructor-verified;
- teach visual differences explicitly;
- separate `wrong`, `misidentified`, `missing`, `extra`, and `wrong_count`;
- show confidence so learners and instructors can see fragile knowledge;
- avoid language that implies the module certifies competence.

### Hospital Administrators

Administrators should see TrayGuard as a possible onboarding and quality
improvement tool, not as evidence that the hospital can automate tray approval.
The economic case should eventually be about reduced preceptor burden, faster
local familiarity, fewer repeated training errors, and cleaner documentation.

Design consequences:

- export pre/post learning metrics;
- summarize repeated weak instruments or trays;
- keep records free of patient information;
- define a small supervised pilot before any operational claim;
- state what departments would need to approve future use: SPD education,
  quality, infection prevention, IT, risk, and finance.

### Students And Class Evaluators

Students are useful for testing whether the learning workflow is understandable
to novices. They are not a proxy for SPD technicians.

Design consequences:

- use students to evaluate first-use clarity, task flow, feedback
  comprehension, and pre/post learning;
- write results as "novice simulated tray familiarity";
- do not claim student results prove SPD adoption, safety readiness, or
  hospital ROI;
- make the system extensible so future teams can add real SPD participant
  validation.

## Retired Local CV Experiment Role

The previous CV experiments on lighting, shape similarity, clutter, and
open-set confidence are no longer active proof obligations. Their useful
residue is architectural:

- CV can remain an optional future authoring or visual-review layer.
- Any CV output must be instructor- or technician-verifiable.
- Existing papers provide enough feasibility support for the capstone narrative.
- Robust deployment would require local validation with representative trays,
  instruments, users, camera setup, lighting, policies, and failure handling.

## Bibliography

See the [central bibliography](../../../bibliography.md) for full source details.
