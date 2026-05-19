# Problem Explication

## SPD Training And Assessment Platform

> TrayGuard helps novice SPD learners improve simulated tray and instrument
> familiarity through local modules, interactive practice, feedback, and
> measurable pre/post assessment.


## Why Novice Training Is A Defensible Target

Sterile processing is safety-critical work. Technicians clean, inspect,
assemble, package, sterilize, store, and distribute reusable medical
instruments. Mistakes can affect OR readiness and patient safety
([Chen et al., 2023](../bibliography.md#chen-et-al-2023),
[Huang et al., 2025](../bibliography.md#huang-et-al-2025),
[Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). The work also
requires visual expertise: technicians must distinguish visually similar
instruments, understand count sheets, recognize aliases and manufacturer
variants, and know where instruments belong in a tray.

That local framing is necessary because instruments differ by manufacturer and hospital. HPN describes count sheets
as tray-specific documents with contents, quantities, sizes, and
catalog/reference numbers. Surgical-tray rationalization research frames tray
management as deciding which instruments and quantities belong in which trays
for which procedures. Tray-configuration modeling uses surgeon preference
cards and procedure-specific instrument requests
([Nadeau, 2024](../bibliography.md#nadeau-2024),
[dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021),
[Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023)). Custom,
specialty, and vendor-loaner trays add another layer of variation by hospital,
surgical team, procedure, surgeon preference, and device manufacturer
([Medline, 2025](../bibliography.md#medline-custom-trays-2025),
[STERIS, 2021](../bibliography.md#steris-loaner-trays-2021)). Therefore,
TrayGuard should teach locally authored tray modules rather than a universal
instrument database.

There is also significant training burden for sterile processing technicians in both certification requirements and
industry practice. HSPA's CRCST pathway requires both a certification exam and
400 hours of hands-on experience in an SPD. Those hours are divided across
decontamination, preparing and packaging instruments, sterilization and
disinfection, storage and distribution, and quality assurance processes
([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026)).
The CRCST exam outline also treats preparation and packaging as one of the major
knowledge domains, weighting it at 21%, the same weight as cleaning,
decontamination, and disinfection
([HSPA CRCST Content Outline, 2023](../bibliography.md#hspa-crcst-content-outline-2023)).
CBSPD's CSPDT route also treats technician certification as minimum
competency and allows candidates to qualify through work experience, allied
health plus SPD experience, a sterile processing course with a passing grade, or
related product sales/service experience
([CBSPD Technician Exam, accessed 2026](../bibliography.md#cbspd-technician-accessed-2026)).

In other words, SPD technician training is a blended competency pipeline:
course material, tests, hands-on repetition, preceptor or supervisor sign-off,
and local workflow learning.

TrayGuard is a way to compress the early familiarity-building portion of that
pipeline by measuring speed and accuracy on simulated local tray tasks. The
certification and clinical-transfer boundaries are maintained in
[Scope Boundaries And Risks](../project/scope_boundaries_and_risks.md).

## Shortage And Training Cost

The first proof point for the pivot is that novice SPD training is a meaningful
stakeholder problem. AORN describes limited training programs, rising market
demand, and high turnover as contributors to a national shortage of qualified
sterile processing technicians
([AORN Staff, 2025](../bibliography.md#aorn-staffing-shortage-2025)). O*NET's
BLS-based national trend page classifies Medical Equipment Preparers, the
occupation that includes many sterile processing roles, as Bright Outlook:
employment is projected to grow from 76,500 workers in 2024 to 84,200 in 2034,
with 10,900 projected annual openings
([O*NET, accessed 2026](../bibliography.md#onet-medical-equipment-preparers-accessed-2026)).

Training one technician is also expensive in staff time. Chobin's AORN Journal
study found that most 2008 survey respondents estimated three to six months
(60%) or six to twelve months (31%) to train employees to process general and
specialty surgical instruments. Most preceptors (52%) spent two to three months
working with new employees. The paper calculated the 2008 cost to train one SPD
technician to competency at $41,414, including preceptor salary
([Chobin, 2010](../bibliography.md#chobin-2010)). A simple CPI-U purchasing
power adjustment puts that legacy estimate in the low $60,000s in 2026 dollars,
using the BLS inflation calculator method
([BLS CPI Inflation Calculator, accessed 2026](../bibliography.md#bls-cpi-calculator-accessed-2026)).
That adjustment is not a new training-cost study, but it helps communicate the
scale of the expense while keeping the primary claim anchored to Chobin's
published estimate.

These facts support a training-platform problem statement better than a direct
efficiency or OR-delay claim. Hospitals need qualified technicians, onboarding
requires months of supervised competency building, and every hour a preceptor
spends explaining basic instrument identity is an hour not spent on other
department work.

## What Training Looks Like In Practice

SPD training varies by program and employer, but the common pattern is blended
learning plus hands-on validation.

| Training Pattern | Evidence | Implication For TrayGuard |
| --- | --- | --- |
| Certification exam plus verified hands-on hours | HSPA CRCST requires 400 SPD hands-on hours and a computer-based exam; CBSPD CSPDT uses eligibility routes that include work experience or a sterile processing course plus an exam ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026), [CBSPD Technician Exam, accessed 2026](../bibliography.md#cbspd-technician-accessed-2026)). | The tool should measure learning and support practice before and during supervised competency development. |
| Self-paced or classroom instruction | Towson's ed2go-backed course is self-paced online, 190 hours, and includes instrument identification and tray assembly topics. Altamont's program is 135 hours over 8-12 weeks with live online classes, in-person labs, and an optional 240-400 hour externship ([Towson University, accessed 2026](../bibliography.md#towson-sterile-processing-accessed-2026), [Altamont Healthcare, accessed 2026](../bibliography.md#altamont-healthcare-accessed-2026)). | The platform can complement formal instruction with reusable local modules and repeated practice. |
| Preceptor-led onboarding | Healthcare Purchasing News describes hospital examples including a 90-day on-the-job training program, a 19-week program with textbook chapters, quizzes, and progress tests, and a structured 1:1 preceptor onboarding program with presentations, online modules, written tests, direct observation, and one-on-one training ([Nadeau, 2017](../bibliography.md#nadeau-2017)). | The system should reduce low-level explanation burden and give preceptors evidence of where a learner still struggles. |
| Simulation and skills assessment | AORN describes Penn Medicine's earn-to-learn SPD training program as combining didactic education, hands-on training, simulation, mentorship, content testing, and skills-based assessment ([AORN Staff, 2025](../bibliography.md#aorn-staffing-shortage-2025)). | Simulated tray sorting and pre/post tasks are aligned with existing training practice. |

This answers the training-process question directly: SPD training can include
online coursework, classroom or hybrid instruction, quizzes and final exams,
one-on-one preceptor tutoring, simulation, direct observation, and externship or
department experience. TrayGuard should occupy the repeatable practice and
assessment layer inside that ecosystem.

## The Training-Access Gap

The training-access gap is repeatable, feedback-rich practice with local
instruments and tray rules. This practice is hard to scale before and during
real SPD experience because it depends on site access, clinical scheduling,
preceptor attention, and available teaching materials.

HSPA makes hands-on experience mandatory for CRCST certification: 400 hours
must be completed in an actual sterile processing department, paid or volunteer,
and the candidate must secure the placement
([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026)).
That requirement creates a clear role for TrayGuard: preclinical and
supplemental practice that strengthens local tray familiarity before scarce
hands-on time is consumed.

Several program examples show why supplemental practice matters. Penn Foster's
online sterile processing program prepares learners for the CRCST exam pathway
but does not require the exam or the 400 hands-on hours as part of the program
([Penn Foster, accessed 2026](../bibliography.md#penn-foster-sterile-processing-accessed-2026)).
MedCerts similarly states that full CRCST certification is obtained after 400
hours of hands-on sterile processing experience following provisional
certification
([MedCerts Catalog, 2025](../bibliography.md#medcerts-catalog-2025)). Central
Sterilization Solutions states that its classroom CRCST course has no hands-on
training in the classroom and that hands-on training is conducted during the
internship
([Central Sterilization Solutions, accessed 2026](../bibliography.md#central-sterilization-solutions-in-person-accessed-2026)).
Other programs include hands-on components but still depend on clinical-site
capacity: AIMS requires a 400-hour clinical internship and says internship
schedules depend on clinical-site availability, while Altamont says externship
placement often takes months and depends on hospital or site availability,
student availability, travel flexibility, and prerequisites
([AIMS Education, accessed 2026](../bibliography.md#aims-education-sterile-processing-accessed-2026),
[Altamont Externship, accessed 2026](../bibliography.md#altamont-externship-accessed-2026)).

Broader allied-health placement research supports the same cautious wording. A
Queensland allied-health placement-capacity study found that placement-offer
growth did not keep pace with student-program growth and that barriers centered
on resourcing and increasing demand
([McBride et al., 2020](../bibliography.md#mcbride-et-al-2020)). A 2025 Greater
Sacramento allied-health report identified shortage of clinical placement
opportunities as a barrier to workforce pipeline growth, described hands-on
clinical training as often required for program completion, licensing, and
employment, and highlighted student preparedness as part of successful placement
partnerships
([North Greater Sacramento COE, 2025](../bibliography.md#north-greater-sacramento-coe-2025)).
These allied-health sources support treating clinical placements as
capacity-constrained practice environments.

These sources support a narrow design claim: learners and instructors benefit
from an accessible practice layer that can be repeated without consuming
capacity-constrained clinical-site time, preceptor attention, or
sterile-processing department capacity.

## Why Tray Assembly Is A High-Friction Subtask

Tray assembly is one major high-friction subtask inside the broader SPD
training pipeline. It is a good target for repeatable practice because it joins
instrument identity, count-sheet interpretation, tray organization, visual
discrimination, and error checking.

There are three evidence streams for that claim:

- Certification structure: HSPA allocates 120 of the 400 CRCST hands-on hours to
  preparing and packaging instruments, equal to the hours for decontamination and
  sterilization/disinfection. The CRCST exam outline assigns preparation and
  packaging a 21% weight and includes item inspection, package assembly, count
  sheets, item identification, instrument placement, organizers, indicators,
  packaging method, and labeling
  ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026),
  [HSPA CRCST Content Outline, 2023](../bibliography.md#hspa-crcst-content-outline-2023)).
- Work-system evidence: Alfred et al. analyzed 3,900 tray defects across 41,799
  cases and found that 55.0% of defects occurred during assembly. Assembly
  defects included missing instruments, wrong instruments, incorrectly assembled
  instruments, and extra instruments. The same study describes assembly as work
  shaped by technician knowledge, instrument nomenclature, inventory, similar
  instruments, tray composition, production pressure, and training variation
  across sites
  ([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021)).
- Error-pattern evidence: Nichol et al. observed 236 surgical instrument errors
  affecting 147 cases; the largest category was missing/wrong/extra instruments,
  and visualization-related tasks such as inspection, identification, function,
  and assembly accounted for 88.6% of observed errors. Zhu et al. separately
  found 398 packaging errors among 33,839 surgical instrument packages, led by
  wrong instrument specification, missing instruments, incomplete packages, and
  higher error rates among the least experienced staff group
  ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
  [Zhu et al., 2019](../bibliography.md#zhu-et-al-2019)).

This evidence shows that local instrument identity, count sheets, tray
assembly, and visual verification are large enough, error-prone enough, and
experience-sensitive enough to justify a dedicated educational module.

## Why Instrument Identification And Tray Organization Belong In Scope

Instrument identification is a core training task. HSPA publishes surgical
instrument resources focused on identification, inspection, maintenance, testing
standards, instrument characteristics, names, lengths, and uses
([HSPA Surgical Instrument Resources, accessed 2026](../bibliography.md#hspa-instrument-resources-accessed-2026)).
The same HSPA description shows why the current learning loop can be
reference-heavy: its instrument manual teaches through "informational text and
photographs," and its inspection textbook lists each instrument's name, length,
use, and testing standards. This shows that manual or directory-style lookup is
a normal support pattern for learning instrument identity. A separate
competency-checklist article makes the same expectation explicit:
instrumentation competency includes knowing instrument names, descriptions, and
inspection points
([Thurmond, 2020](../bibliography.md#thurmond-2020)).
HSPA eLearning lessons also include instrument-specific identification, care,
handling, and quiz-based content
([HSPA Urology Instruments, accessed 2026](../bibliography.md#hspa-urology-instruments-accessed-2026)).
Commercial course outlines likewise include tray assembly and instrumentation
identification as explicit topics
([Towson University, accessed 2026](../bibliography.md#towson-sterile-processing-accessed-2026)).

This is the immediate-feedback opportunity for TrayGuard: instead of making a
novice identify an unfamiliar instrument, consult a manual or photo directory,
and only later find out whether they were right, the system can turn that moment
into an interactive practice cycle at the point of learning.

TrayGuard should therefore focus on learning tasks that map to this real
curriculum:

- identify an instrument from a photo or name;
- distinguish visually similar instruments;
- connect instruments to aliases, sizes, functions, and local notes;
- assemble or sort a simulated tray from a local count sheet;
- receive feedback on missing, wrong, extra, and misidentified items;
- measure pre/post accuracy, completion time, error categories, and learner
  confidence.

The strongest current evaluation is whether a novice improves on a simulated
identification or tray-sorting task after using the trainer.

## Training Pipeline Evidence

TrayGuard's training loop should be built around retrieval practice: learners
orient to the material, retrieve names and features from memory, apply that
retrieval in a simulated tray task, receive specific feedback, and then assess
without hints. That sequence is supported by sterile-processing training
studies, medical simulation research, cognitive psychology, digital education,
and workplace training literature.

Direct sterile-processing evidence supports the same structure. Ofstead et al.
piloted borescope training for sterile processing professionals using pre- and
post-testing, lectures, hands-on practice, homework, and a booster session;
mean test scores improved from 41% to 84% after the workshop and remained high
after two months
([Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)). Hu et al.'s
CSSD training-program study used a structured knowledge system, varied training
methods including simulation experiences, and assessment, reporting gains in
knowledge, operational skills, and satisfaction
([Hu et al., 2024](../bibliography.md#hu-et-al-2024)).
Additional sterile-processing training studies point in the same direction and
support practice-plus-assessment as a design pattern. Fast et al. evaluated a
short sterile-processing course
with theory, skills training, training-of-trainers, and workplace mentoring
across 12 Ethiopian hospitals; participant knowledge improved by more than 20%,
and hospital assessments found improvements in instrument flow, inspection, and
packaging practices
([Fast et al., 2019](../bibliography.md#fast-et-al-2019)). Shreckengost et al.
evaluated sterile-instrument processing workshops in five countries and found
knowledge gains, confidence gains, and improved observed instrument compliance
after training
([Shreckengost et al., 2022](../bibliography.md#shreckengost-et-al-2022)).
These studies strengthen the premise that structured sterile-processing
training with practice, assessment, and local adaptation can improve SP
knowledge and work practices.

Simulation-based healthcare education is one of the closest analogies. A large
review of technology-enhanced simulation in health professions education found
simulation associated with improved knowledge, skills, and behaviors compared
with no intervention
([Cook et al., 2011](../bibliography.md#cook-et-al-2011)). A separate
meta-analytic review found that simulation-based medical education with
deliberate practice produced stronger specific skill acquisition than
traditional clinical education
([McGaghie et al., 2011](../bibliography.md#mcgaghie-et-al-2011)). Earlier
medical-simulation guidance also identifies feedback, repetitive practice,
curriculum integration, measurable outcomes, and controlled task difficulty as
features associated with effective learning
([Issenberg et al., 2005](../bibliography.md#issenberg-et-al-2005)).

More recent software-based simulation literature supports treating TrayGuard as
a virtual practice environment rather than a simple content viewer. Jiang et
al.'s 2024 meta-analysis of randomized trials compared virtual simulations with
mannequins or real persons in medical and nursing education and found virtual
simulation to be a viable training alternative for several education outcomes
([Jiang et al., 2024](../bibliography.md#jiang-et-al-2024-virtual-simulation)).
Wu et al.'s scoping review shows that virtual simulation has become a common
recent pattern in undergraduate medical education, including web- and
software-based learning environments
([Wu et al., 2022](../bibliography.md#wu-et-al-2022-virtual-simulation)).
Phanudulkitti et al.'s review of virtual patient and computer-based simulation
in pharmacy education is also useful because it evaluates experiential outcomes
such as knowledge, skills, confidence, enjoyment, and engagement
([Phanudulkitti et al., 2023](../bibliography.md#phanudulkitti-et-al-2023)).
Together, these sources support a software simulation claim: TrayGuard should
let learners practice an applied task, receive feedback, and generate
performance evidence.

The quiz component is also a learning intervention, not just an assessment.
Retrieval-practice research shows that testing can improve long-term retention
compared with restudying
([Roediger and Karpicke, 2006](../bibliography.md#roediger-and-karpicke-2006)).
Karpicke and Blunt found that retrieval practice produced stronger delayed
learning than elaborative concept mapping in science-text learning, which
supports recall-first activity rather than a purely explanatory study flow
([Karpicke and Blunt, 2011](../bibliography.md#karpicke-and-blunt-2011)).
A broad review of learning techniques rated practice testing and distributed
practice among the most useful strategies for durable learning
([Dunlosky et al., 2013](../bibliography.md#dunlosky-et-al-2013)). In medical
education specifically, repeated testing improved long-term retention compared
with repeated study, and adaptive spaced education uses repeated online
questions to combine testing and spacing
([Larsen et al., 2009](../bibliography.md#larsen-et-al-2009),
[Kerfoot, 2010](../bibliography.md#kerfoot-2010)).

That is the evidence-backed version of the "Quizlet or Duolingo" intuition:
the defendable mechanism is repeated active recall,
spacing, immediate feedback, and repetition of weak items. A 2024 meta-analysis
of spaced digital education for health professionals supports spaced digital
education for knowledge, skills, confidence, and clinical behavior change, and
a 2025 scoping review documents widespread health-professions use of electronic
flashcards, including platforms such as Anki and Quizlet
([Martinengo et al., 2024](../bibliography.md#martinengo-et-al-2024),
[Barrison et al., 2025](../bibliography.md#barrison-et-al-2025)).

Feedback needs to be specific enough to guide the next attempt. Hattie and
Timperley's feedback review frames effective feedback around three questions:
where the learner is going, how the learner is doing, and what the learner
should do next
([Hattie and Timperley, 2007](../bibliography.md#hattie-and-timperley-2007)).
For TrayGuard, that means feedback should identify whether the learner missed
an item, added an extra item, chose the wrong instrument, misidentified a
similar-looking instrument, or used the wrong count.

The same pattern appears in organizational training research. Meta-analytic
evidence shows that workplace training can improve learning, behavior, and
organizational results when it is designed and evaluated well
([Arthur et al., 2003](../bibliography.md#arthur-et-al-2003)). Salas et al.
argue that effective training should be treated as a system: analyze the work,
design instruction around target competencies, provide practice and feedback,
and evaluate transfer
([Salas et al., 2012](../bibliography.md#salas-et-al-2012)).

The engineering implication is that the highest-value build is a measured
practice system:

| TrayGuard Feature | Evidence-Based Role | Engineering Requirement |
| --- | --- | --- |
| Retrieval-first study cards | Initial instruction that still asks learners to answer before reveal. | Store photos, names, aliases, functions, distinguishing features, and local notes; present prompts before explanations. |
| Identification quiz mode | Central retrieval practice for instrument identity and features. | Ask recall/recognition questions, randomize distractors, record correctness, confidence, and time. |
| Simulated tray sorting mode | Safe applied retrieval in a realistic work task. | Let learners assemble or check a tray against a count sheet in a low-risk training environment. |
| Immediate feedback | Deliberate practice and error correction. | Explain wrong answers and classify errors as missing, extra, wrong, misidentified, or wrong count. |
| Confidence ratings | Metacognitive signal for learner and instructor. | Capture confidence before or after tasks so low-confidence correct answers and high-confidence errors are visible. |
| Pre/post tests | Evaluation separated from practice. | Disable hints and feedback during tests; export comparable pre/post accuracy, time, error type, and confidence. |

The resulting project is one complete local tray module. The first module
should prove the loop from local tray data to
pre-test, retrieval-first cards, quiz, applied tray practice, weak-item review,
post-test, and metrics export. The design decision and tradeoffs are detailed in
[Training Module Design](../project/training_module_design.md).

The proposed capstone experiment should therefore test simulation as an added
practice layer:

| Group | Training Condition | Post-Test |
| --- | --- | --- |
| A | Structured flashcards and quizzes only. | No-hints simulated tray-verification task. |
| B | Structured flashcards and quizzes plus simulated tray-verification practice with feedback. | Same no-hints simulated tray-verification task. |

The main outcome is whether Group B performs better on the applied tray task.
Measure tray-verification accuracy, completion time, missing/extra/wrong/
misidentified/wrong-count errors, high-confidence errors, low-confidence correct
answers, weak-item recovery, and whether learners can explain what to review
next. The bounded claim is:

> Compared with structured flashcards alone, adding software-based simulated
> tray-verification practice improves novice performance on a comparable
> simulated tray task.

## Medical Training Software Precedents

Medical training software already uses this same basic design pattern:
simulation, guided practice, feedback, scoring, and progress tracking. These
examples show that the proposed training architecture follows established
healthcare education practice.

| Example | Relevant Design Pattern | Lesson For TrayGuard |
| --- | --- | --- |
| Touch Surgery / Medtronic | Mobile surgical procedure simulations with repeated attempts and scoring. A validation study found that users improved across repeated attempts, and higher-experience cohorts outperformed lower-experience cohorts ([Tulipan et al., 2019](../bibliography.md#tulipan-et-al-2019), [Medtronic Touch Surgery, accessed 2026](../bibliography.md#medtronic-touch-surgery-accessed-2026)). | Repeated app-based simulation with objective scoring can produce measurable improvement and distinguish novice from expert performance. |
| Osso VR-style orthopedic simulation | VR procedural training with hints, repeated sessions, competency thresholds, and a separate physical assessment. In a randomized trial, VR-trained novices completed the procedure more often, made fewer incorrect steps, and finished faster than guide-only learners ([Orland et al., 2020](../bibliography.md#orland-et-al-2020)). | Guided simulation can transfer to a controlled downstream task, so TrayGuard should measure post-training performance on a separate tray scenario. |
| Body Interact virtual patients | Screen-based virtual patient scenarios with immediate feedback, auto-grading, LMS analytics, and instructor review ([Wolters Kluwer Body Interact, accessed 2026](../bibliography.md#wolters-kluwer-body-interact-accessed-2026)). Web-based virtual patient research also reports positive effects on clinical reasoning ([Kleinert et al., 2015](../bibliography.md#kleinert-et-al-2015)). | A safe, repeatable simulation can support both learner practice and educator-facing analytics. |
| Fundamental Surgery | Step-by-step VR/haptic surgical guidance, performance analysis, and a surgical skills score; its total knee arthroplasty simulation received AAOS CME accreditation ([AAOS, 2019](../bibliography.md#aaos-fundamental-surgery-2019)). | Medical education products commonly pair guided practice with formal performance scoring. |
| Surgical Science / Simbionix | Commercial medical simulators across specialties, positioned around evidence-based simulation, clinical proficiency, and performance measurement ([Surgical Science, accessed 2026](../bibliography.md#surgical-science-simulators-accessed-2026)). | The market precedent supports simulation software as a credible healthcare training category. |

## Error Motivation

The broader sterile-processing problem defines the operational stakes for the
training module.
Nichol et al. observed surgical instrument errors across 147 of 562 cases in a
direct-observation study. Missing instruments were the largest error category,
and visualization-related tasks accounted for most observed errors. The same
study estimated substantial annual lost chargeable OR minutes for the observed
campus
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). A separate
packaging-error study found 398 errors among 33,839 surgical instrument
packages, including wrong specifications, incomplete packages, and missing
instruments
([Zhu et al., 2019](../bibliography.md#zhu-et-al-2019)).

These sources justify why instrument familiarity, count sheets, tray
organization, and visual inspection matter. The defensible bridge is upstream:
better novice practice may improve familiarity in simulated tasks, and a future
hospital study could test whether that learning transfers to supervised SPD
work.

## Existing Tools And Differentiation

The product space already contains mature reference, tracking, and tray assembly
tools. TrayGuard's differentiation should therefore be a measured training loop
for local tray familiarity.

CensiTrac supports surgical instrument tracking, assembly instructions,
multimedia aids, training tips, approved substitutions, productivity goals, and
technician progress review
([CensiTrac, accessed 2026](../bibliography.md#censitrac-accessed-2026)).
Tray Pacer's TrayPakk product explicitly frames new SPD technician training as
expensive and slow, describing a 3-6 month training problem and offering tray
assembly training and productivity software
([Tray Pacer, accessed 2026](../bibliography.md#tray-pacer-accessed-2026)).
LayerJot's SID provides a large surgical-instrument directory with search,
count-sheet scanning, camera-based identification, photos, best practices, notes,
and IFU access
([LayerJot SID, accessed 2026](../bibliography.md#layerjot-sid-accessed-2026)).
NuTrace's Nu Scanner translates GS1 DataMatrix codes into instrument
information and includes an education use case for learning instrument names and
part numbers while scanning
([NuTrace Nu Scanner, accessed 2026](../bibliography.md#nutrace-nu-scanner-accessed-2026)).

TrayGuard's differentiation is narrower and more academic:

- structured novice practice;
- simulated identification and tray sorting;
- local curriculum authoring;
- pre/post learning measurement;
- optional visual matching as authoring support.

## Design Implications

The background evidence points to a specific product shape:

- primary user: new or trainee sterile processing technician;
- secondary user: SPD educator, supervisor, or training program;
- core artifact: local instrument and tray modules;
- core workflow: study, retrieve, simulate, receive feedback, repeat, and
  assess;
- core metric: change in novice performance from pre-test to post-test;
- scope boundary: simulated learning value, with clinical-transfer risks
  tracked in
  [Scope Boundaries And Risks](../project/scope_boundaries_and_risks.md).

Computer vision can still support the project by creating instrument cards,
suggesting labels during authoring, generating distractors, or supporting future
visual practice modes. The validated product story should remain: TrayGuard
helps novices learn instruments and tray organization in a measurable,
extensible training environment.

A lightweight physical layer can make the demo more concrete while preserving
the evidence claim. The safest hardware option is a printed tray mat with
printed instrument cards containing QR codes or AprilTags. Learners place cards
on the tray and scan them with a webcam or phone camera. The software still
scores identity, count, lookalikes, and placement. This hardware functions as
an interaction layer for the software simulation.

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
