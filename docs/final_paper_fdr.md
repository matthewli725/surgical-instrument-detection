# Final Paper FDR

## Abstract / Executive Summary

TODO: Write this section last after the body of the report is complete. It
should summarize the final problem, the selected TrayGuard direction, the
strongest evidence, the main design decisions, the current limitations, and the
recommended future validation path.

## 1. Introduction And Project Overview

TODO: Write this section after the main body is stable. It should briefly
explain the sterile-processing context, the project pivot toward an
education-centered training and assessment system, and the purpose of this FDR
as a literature-grounded design and risk-reduction handoff for a future team.

## 2. Problem Definition And Scope

### 2.1 Precise Problem Statement

In sterile processing
departments (SPDs), technicians receive used instruments from the OR, clean and
decontaminate them, inspect each item for soil or damage, check function,
assemble procedure-specific trays from count sheets, package trays for
sterilization, run sterilization, store sterile sets, and distribute
them back for surgical use. This work is detailed, high-volume, and highly
local: a technician must know the hospital's instrument names, tray lists,
surgeon preferences, replacement rules, and inspection expectations.

Mistakes can occur at several points in that workflow. A technician may miss
residual soil, overlook a crack or broken tip, confuse two visually similar
instruments, place the wrong size or pattern into a tray, omit an instrument,
add an extra instrument, assemble a device incorrectly, use the wrong count
sheet, package a set incompletely, or fail to catch a sterilization or
documentation problem. In the OR, those mistakes appear as missing, wrong,
extra, damaged, contaminated, nonfunctional, incorrectly assembled, or otherwise
unavailable instruments.

Published rates vary by hospital, measurement method, and error definition, but
the available evidence suggests that these are recurring operational failures,
not isolated accidents. Alfred et al. analyzed 3,900 tray defects across 41,799
cases, or roughly 9 defects per 100 cases, and found that 55.0% of recorded
defects occurred during assembly
([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). Zhu et al. found
398 packaging errors among 33,839 surgical instrument packages, or about 1.2%
of packages, including wrong specifications, incomplete packages, and missing
instruments ([Zhu et al., 2019](bibliography.md#zhu-et-al-2019)). Nichol et al.
observed 236 surgical instrument errors affecting 147 cases, with most errors
tied to visualization work such as inspection, identification, function
checking, and tray assembly
([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)).

The general problem is therefore:

> Sterile processing workflows do not always reliably produce complete,
> correct, functional, sterile, and ready-for-use surgical instrument sets.


### 2.2 Practice Context

The problem appears across the reusable stainless surgical instrument chain. A simplified
SPD-to-OR cycle includes the following stages
([George et al., 2024](bibliography.md#george-et-al-2024)):

1. Point-of-use preparation: at the end of a procedure, instruments are
   prepared for transfer from the OR to sterile processing. This can include
   gross cleaning, use of sterile water, and enzymatic pretreatment to keep
   material from drying on instruments.

2. Transport to sterile processing: used instruments are moved from the OR or
   procedural area to the sterile processing unit.

3. Decontamination: instruments are cleaned and decontaminated. George et al.
   describe manual scrubbing, ultrasonic cleaning, and automated washer systems
   as common parts of this stage.

4. Assembly and inspection: after decontamination, instruments move to the
   assembly area. Technicians inspect instruments, assemble instrument pans or
   sets, replace missing items, and place instruments into containers or wraps
   for sterilization.

5. Sterilization: packaged instruments are sterilized using methods appropriate
   to the device and material. George et al. describe high-temperature methods
   such as autoclave sterilization and low-temperature methods such as chemical
   or radiation-based sterilization.

6. Storage: once sterilized, instruments and trays are cooled as needed and
   placed in storage until they are required again.

7. Return to use: when needed for surgery, stored instruments are obtained and
   brought back to the OR for the next case.

Nichol and Saari's risk model provides a more detailed version of this cycle:
for simple instruments, they mapped 104 human tasks and found that 91% of
modeled error risk occurred during the sterile-processing portion of the cycle,
especially the decontamination and assembly-and-inspection steps
([Nichol and Saari, 2023b](bibliography.md#nichol-and-saari-risk-modeling-2023)).
Those steps are high risk because they contain the most complicated,
non-routine tasks: instruments must be separated, cleaned, inspected for
bioburden and damage, identified, sorted, and rebuilt into the correct tray, and
all eight highest-risk tasks in the model involved human visualization,
inspection, identification, or sorting.

### 2.3 Narrowed Problem

Within the full SPD-to-OR cycle, this project narrows to tray reconstruction
and verification: the point where cleaned instruments are inspected,
identified, matched to count sheets, and rebuilt into procedure-specific trays.
This is the most defensible focus because the highest-risk parts of the cycle
depend on human visualization, sorting, and local tray knowledge.

This focus also addresses a likely stakeholder objection. Even if a tray comes
from a specific surgery and is expected to return with the same contents, it
does not remain a sealed, unchanged kit during reprocessing. Instruments are
transported to decontamination, opened, separated, disassembled when required,
manually cleaned or transferred onto washer racks, and exposed to mechanical
washing before moving to the clean preparation area
([STERIS, accessed 2026](bibliography.md#steris-cleaning-instruments-accessed-2026),
[CDC](bibliography.md#cdc),
[Public Health Ontario, 2013](bibliography.md#public-health-ontario-2013),
[Medline, 2026](bibliography.md#medline-transport-2026)). After cleaning,
technicians manually rebuild sets against tray-specific count sheets, creating
opportunities for items to be mixed between sets, left behind, substituted from
backup inventory, or misidentified because of incomplete count-sheet data,
local jargon, or look-alike instruments
([Purdue University, accessed 2026](bibliography.md#purdue-count-sheets-accessed-2026),
[Alfred et al., 2021](bibliography.md#alfred-et-al-2021),
[Nadeau, 2024](bibliography.md#nadeau-2024)).

Observed error studies support this narrowed focus. Nichol et al. found that
the largest observed error category was Missing+, which included missing,
wrong, and extra instruments, and connected many errors to visualization work
such as inspection, identification, and function checks
([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). Alfred et al. found
missing instruments to be the most commonly reported assembly defect and linked
tray defects to OR delays, training, production pressure, inventory,
nomenclature, technology, and workspace constraints
([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). Zhu et al. found
packaging errors such as wrong instrument specifications, incomplete packages,
and missing instruments in a hospital surgical-instrument tracking system
([Zhu et al., 2019](bibliography.md#zhu-et-al-2019)).

### 2.4 Stakeholders And Importance

Instrument readiness matters because surgery is time-sensitive,
coordination-heavy work. When an instrument set is wrong, incomplete, unclean,
damaged, or unavailable, the OR team may need to pause, search for replacement
instruments, open backup trays, change the procedure flow, or delay the case
([Nichol et al., 2024](bibliography.md#nichol-et-al-2024),
[Pennsylvania Patient Safety Authority, 2006](bibliography.md#pennsylvania-patient-safety-authority-2006)).

Dirty or damaged instruments add a direct safety concern. A 2024 hospital
inspection reported pitting, stains, sticky residue, rust, scratches, and other
concerns in randomly selected ready-for-use trays
([Association of Health Care Journalists, 2024](bibliography.md#association-of-health-care-journalists-2024)).
The Pennsylvania Patient Safety Authority warns that contaminated instruments
can put patients at risk of surgical site infection and can also cause lost OR
time if discovered after a procedure has begun
([Pennsylvania Patient Safety Authority, 2006](bibliography.md#pennsylvania-patient-safety-authority-2006)).

The stakeholders include:

- Patients, who depend on sterile, functional instruments during surgery.
- Surgeons and OR teams, who need complete and usable sets to maintain
  procedure flow.
- SPD technicians, who perform detailed, high-volume work under production
  pressure.
- SPD supervisors and educators, who manage training, quality assurance,
  staffing, documentation, and feedback loops.
- Hospitals, which lose time and capacity when instrument issues delay cases or
  require rework.

### 2.5 General Interest Beyond One Local Practice

This problem is broadly relevant because reusable surgical instruments, SPDs,
procedure-specific trays, count sheets, sterilization records, and OR
dependence on prepared sets are common across hospitals. The exact instruments,
tray lists, vendor systems, and surgeon preferences vary by site, while the
readiness challenge repeats across settings: hospitals must transform complex,
locally defined instrument requirements into complete and ready surgical sets.

The local tray-reconstruction problem connects to broader work on surgical
tray optimization, inventory visibility, and instrument-set readiness. dos
Santos et al. describe tray rationalization as deciding which instruments and
quantities belong in which trays and which trays are needed for procedures
([dos Santos et al., 2021](bibliography.md#dos-santos-et-al-2021)). A 2025
industry benchmark report summarized by Healthcare Purchasing News found that
58% of surveyed SPD and OR leaders reported surgery delays caused by instrument
sets that were missing, incomplete, or not ready on time
([HPN, 2025](bibliography.md#hpn-2025)).
The same benchmark report emphasized human error, inventory gaps, limited data
visibility, and real-time visibility into tray and instrument location as major
readiness concerns
([Aesculap and Ascendco Health, 2025](bibliography.md#aesculap-and-ascendco-health-2025)).

This makes the problem generalizable without making it generic: each hospital
has its own instruments and tray rules, but many hospitals face the same
underlying need to verify that a locally defined set is complete, correct,
clean, functional, and available before surgery.

## 3. Root Cause Analysis

We have already narrowed the problem to a specific point in the sterile
processing workflow. The fishbone head for the RCA is therefore:

> Tray content errors during tray reconstruction.

This effect includes missing instruments, wrong instruments, extra instruments,
wrong quantities, visible damage or function problems, and item selections that
conflict with the count sheet or local tray rule
([Alfred et al., 2021](bibliography.md#alfred-et-al-2021);
[Nichol et al., 2024](bibliography.md#nichol-et-al-2024);
[Zhu et al., 2019](bibliography.md#zhu-et-al-2019)).

### 3.1 Product

| Observed failure mode | Root cause hypothesis |
| --- | --- |
| Wrong instruments appear in trays, and wrong-instrument errors are often similar in type to the intended instrument ([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). | Same-family variants and look-alike instruments create a discrimination burden that generic instrument familiarity does not solve; users need practice distinguishing local variants by visible features, size, function, and tray context ([Nichol et al., 2024](bibliography.md#nichol-et-al-2024); [Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| Assembly defects include missing, wrong, damaged, incorrectly assembled, and extra instruments ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). | Tray composition, instrument design, inventory, and unstandardized nomenclature make the tray itself a complex product to reconstruct reliably ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| Procedure-, surgeon-, and tray-specific decisions determine which instruments and quantities belong in a set ([dos Santos et al., 2021](bibliography.md#dos-santos-et-al-2021); [Ahmadi et al., 2023](bibliography.md#ahmadi-et-al-2023)). | Tray contents are local design decisions rather than fixed universal lists, so a user can know instrument families and still select the wrong item or quantity for a specific tray ([dos Santos et al., 2021](bibliography.md#dos-santos-et-al-2021); [Ahmadi et al., 2023](bibliography.md#ahmadi-et-al-2023)). |
| Damaged, malfunctioning, contaminated, or otherwise unacceptable instruments can create readiness and safety concerns ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021); [Nichol et al., 2024](bibliography.md#nichol-et-al-2024); [Pennsylvania Patient Safety Authority, 2006](bibliography.md#pennsylvania-patient-safety-authority-2006)). | Reconstruction must include rejection of visibly unacceptable items, not only selection of named items; otherwise damaged or suspect instruments can remain in a tray despite correct identity and count ([CDC](bibliography.md#cdc); [Pennsylvania Patient Safety Authority, 2006](bibliography.md#pennsylvania-patient-safety-authority-2006)). |

### 3.2 Knowledge

| Observed failure mode | Root cause hypothesis |
| --- | --- |
| Instrument identification, inspection, names, uses, and testing points are explicit sterile-processing learning needs ([HSPA Surgical Instrument Resources, accessed 2026](bibliography.md#hspa-instrument-resources-accessed-2026)). | Users may not have enough retrievable instrument knowledge to identify items, notice damage, or distinguish similar tools during reconstruction ([HSPA Surgical Instrument Resources, accessed 2026](bibliography.md#hspa-instrument-resources-accessed-2026)). |
| Tray assembly requires local names, aliases, quantities, placement rules, and count-sheet use ([Nadeau, 2024](bibliography.md#nadeau-2024)). | General instrument knowledge is insufficient when the task depends on local tray rules; learners need practice applying the exact tray rule, not just recognizing instruments in isolation ([Nadeau, 2024](bibliography.md#nadeau-2024)). |
| Alfred et al. identify technician knowledge, training variation, missing or incorrect photos, and varied names as assembly work-system factors ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). | Local knowledge may be inconsistent across staff or training materials, so the same tray can be reconstructed differently depending on who learned which names, photos, and informal rules ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| HSPA requires 400 hands-on hours for CRCST certification, including 120 hours in preparation and packaging ([HSPA CRCST, accessed 2026](bibliography.md#hspa-crcst-accessed-2026)). | Tray reconstruction competency depends on repeated hands-on practice; without measured practice, a learner may appear familiar with instruments but still fail under tray-like conditions ([HSPA CRCST, accessed 2026](bibliography.md#hspa-crcst-accessed-2026); [Ofstead et al., 2023](bibliography.md#ofstead-et-al-2023)). |
| AORN describes hands-on and simulation training for decontaminating sets, assembling and wrapping trays, and preparing items for sterilization, while sterile-processing certification commentary frames certification as a baseline that still requires ongoing competency checks, education, and in-services ([AORN Staff, 2025](bibliography.md#aorn-staffing-shortage-2025); [Kovach, 2012](bibliography.md#kovach-2012)). | The supportable root cause is not individual technician incompetence; it is that certification and initial instruction do not prove local tray-reconstruction competence unless they are paired with repeated local practice, observation, feedback, and current tray information ([Kovach, 2012](bibliography.md#kovach-2012); [Ofstead et al., 2023](bibliography.md#ofstead-et-al-2023)). |

### 3.3 Process

| Observed failure mode | Root cause hypothesis |
| --- | --- |
| Alfred et al. found that 55.0% of recorded tray defects occurred during assembly ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). | The assembly step is a high-risk control point because content errors can enter or escape while instruments are being selected, counted, inspected, and arranged ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| Nichol et al. found that 88.6% of observed errors involved visualization tasks such as inspection, identification, function checking, and sorting ([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). | Reconstruction depends heavily on manual visual checking; without task-specific aids or practice, users can miss errors that are visible but visually subtle ([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). |
| Zhu et al. observed packaging errors including wrong specifications, incomplete packages, and missing instruments ([Zhu et al., 2019](bibliography.md#zhu-et-al-2019)). | Downstream package errors can reflect upstream reconstruction and verification gaps, especially when wrong specifications or missing contents are not caught before packaging ([Zhu et al., 2019](bibliography.md#zhu-et-al-2019)). |
| HPN frames following count sheets and inspecting instruments as core preparation, packing, and assembly practices ([Nadeau, 2024](bibliography.md#nadeau-2024)). | If verification is memory-based, inconsistent, or separated from the count sheet, missing, wrong, extra, damaged, or miscounted items can pass through reconstruction ([Nadeau, 2024](bibliography.md#nadeau-2024)). |

### 3.4 Information

| Observed failure mode | Root cause hypothesis |
| --- | --- |
| Count sheets should include tray names, contents, quantities, sizes, reference numbers, preparation and inspection steps, placement instructions, packaging, indicators, and destination/storage details ([Nadeau, 2024](bibliography.md#nadeau-2024)). | If the local build rule is incomplete, outdated, vague, or hard to use, reconstruction shifts from rule-following to interpretation, increasing the chance of wrong items or quantities ([Nadeau, 2024](bibliography.md#nadeau-2024)). |
| Alfred et al. identify missing or incorrect photos and varied instrument names as assembly-relevant factors ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). | If names, aliases, and photos are not aligned with the actual tray, users may match the wrong concept to the physical instrument or fail to recognize a local variant ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| Outpatient Surgery Magazine describes tray customization and standardization as reducing variation and time spent identifying instruments, and notes that proper OR and sterile-processing staff training is important for recognizing instruments that need sharpening or repair ([Loria, 2024](bibliography.md#loria-2024)). | Tray information must be maintained as a shared local standard; otherwise staff training, instrument identification, defect recognition, and tray reconstruction all depend on informal memory instead of a reliable local rule ([Loria, 2024](bibliography.md#loria-2024); [Nadeau, 2024](bibliography.md#nadeau-2024)). |
| Tray-focused commercial tools emphasize count sheets, photos, assembly information, and proficiency metrics ([Tray Pacer, accessed 2026](bibliography.md#tray-pacer-accessed-2026); [LayerJot SID, accessed 2026](bibliography.md#layerjot-sid-accessed-2026)). | The practical market for tray tools suggests that structured local tray information is a real operational need, not just a classroom convenience ([Tray Pacer, accessed 2026](bibliography.md#tray-pacer-accessed-2026); [LayerJot SID, accessed 2026](bibliography.md#layerjot-sid-accessed-2026)). |
| Loaner-tray workflows depend on visibility across scheduling, vendor delivery, OR awareness, SPD awareness, IFUs, count sheets, status, location, and pickup ([STERIS, 2021](bibliography.md#steris-loaner-trays-2021)). | When tray status, IFUs, count sheets, or source information are not visible during reconstruction, staff may not have the correct local rule for a non-routine or loaner tray ([STERIS, 2021](bibliography.md#steris-loaner-trays-2021)). |

### 3.5 Environment

| Observed failure mode | Root cause hypothesis |
| --- | --- |
| Alfred et al. identify production pressure and workspace constraints as performance-shaping factors in assembly work ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). | Time and workspace pressure can reduce the attention available for visual discrimination, count checking, and escalation, making existing product/process risks more likely to become errors ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| AORN describes limited training programs, rising market demand, and high turnover as contributors to a shortage of qualified sterile processing technicians; Medline describes short staffing as increasing overtime, miscommunication, and difficulty maintaining quality; Mácola et al. found wage stagnation, inadequate benefits, and financial stress across a national SPD worker survey ([AORN Staff, 2025](bibliography.md#aorn-staffing-shortage-2025); [Brozak, 2025](bibliography.md#brozak-2025); [Mácola et al., 2025](bibliography.md#macola-et-al-2025)). | Staffing pressure is plausible context, but the evidence does not prove it is the direct root cause of tray content errors; it should be treated as an amplifier that can worsen onboarding burden, training quality, attention, and verification gaps ([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). |
| A Colorado hospital inspection report, summarized by The Colorado Sun, tied a major SPD backlog to increased staffing requirements after new operating rooms opened without evidence that SPD staffing had increased to match the new demand ([Ingold, 2025](bibliography.md#ingold-2025)). | Capacity mismatch can turn SPD work-system stress into delayed cleaning, reprocessing backlogs, and readiness failures; this supports the importance of staffing and training capacity, but it is broader context rather than direct evidence for tray-reconstruction content errors ([Ingold, 2025](bibliography.md#ingold-2025)). |
| Huang et al. examine training demands related to interruptions in central sterile supply departments ([Huang et al., 2025](bibliography.md#huang-et-al-2025)). | Interruptions can break the continuity of counting, sorting, and inspection, so users may lose place in the tray reconstruction task and miss quantity or identity errors ([Huang et al., 2025](bibliography.md#huang-et-al-2025)). |
| OSHA central sterile guidance discusses workstation, reaching, standing, carts, and height-adjustment concerns for central sterile work ([OSHA Central Sterile Supply, accessed 2026](bibliography.md#osha-central-sterile-supply-accessed-2026)). | Physical layout and ergonomic friction can increase handling and search burden, making a visual, detail-heavy reconstruction task harder to perform consistently ([OSHA Central Sterile Supply, accessed 2026](bibliography.md#osha-central-sterile-supply-accessed-2026)). |

### 3.6 Policy And Feedback

| Observed failure mode | Root cause hypothesis |
| --- | --- |
| HPN emphasizes standardized, clearly written count sheets that are available across shifts ([Nadeau, 2024](bibliography.md#nadeau-2024)). | If no one clearly owns count-sheet standardization and updates, different shifts or learners may use different tray rules, names, or quantities during reconstruction ([Nadeau, 2024](bibliography.md#nadeau-2024)). |
| Chobin states that instrument processing requires coordinated policies, procedures, accountability, education, and documentation ([Chobin, 2019](bibliography.md#chobin-2019)). | Without clear policy and accountability, users may not know when to stop, escalate, substitute, reject, or document uncertain tray-content decisions ([Chobin, 2019](bibliography.md#chobin-2019)). |
| Sterile-processing certification commentary argues that certification creates a common knowledge baseline but cannot guarantee error-free work, and that managers must maintain competency programs and continuing education ([Kovach, 2012](bibliography.md#kovach-2012)). | If competency is treated as a one-time credential instead of a measured, recurring, local skill, repeated tray errors may not become targeted retraining, updated modules, or supervisor coaching ([Kovach, 2012](bibliography.md#kovach-2012)). |
| Nichol et al. describe traditional surgical-instrument error reporting as cumbersome, human-dependent, delayed, incomplete, and difficult to integrate with operational systems ([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). | If error reporting is delayed or incomplete, repeated missing, wrong, extra, damaged, or quantity errors may not become targeted retraining or tray-rule updates ([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). |
| Ofstead et al. used competency testing and booster training as part of a structured sterile-processing training intervention ([Ofstead et al., 2023](bibliography.md#ofstead-et-al-2023)). | Without repeated assessment and feedback, local tray reconstruction skill can remain unmeasured, making it hard to identify weak instruments, weak rules, or users who need more practice ([Ofstead et al., 2023](bibliography.md#ofstead-et-al-2023)). |
| Safety reports show that content, contamination, and readiness issues can create patient-safety and lost-time concerns when detected late ([Pennsylvania Patient Safety Authority, 2006](bibliography.md#pennsylvania-patient-safety-authority-2006)). | Escalation and feedback need to happen before the tray is treated as ready; otherwise detected issues may become downstream rework or point-of-use disruption ([Pennsylvania Patient Safety Authority, 2006](bibliography.md#pennsylvania-patient-safety-authority-2006)). |

### 3.7 Consolidated Root Cause Chain

```text
Local tray complexity, similar instruments, and exact count requirements
  -> dependence on local knowledge, count-sheet quality, and visual recognition
  -> manual reconstruction and verification under real work-system conditions
  -> missed, wrong, extra, damaged, or miscounted instruments
  -> tray content errors before the tray is considered ready for use
```


### 3.8 Resulting Solvable Scope

The full readiness problem remains too broad for one final project because it
includes staffing, inventory, cleaning practice, sterilization capacity,
scheduling, tracking systems, and OR-SPD communication. The RCA narrows the
project toward a more actionable training and competency gap: local tray
reconstruction depends on detailed instrument knowledge, count-sheet
interpretation, lookalike discrimination, and repeated feedback, yet those
skills are difficult to practice and measure consistently before supervised
hands-on work.

This scope does not claim to solve the entire SPD staffing shortage or certify
clinical competence. Instead, it focuses on a measurable precursor to
competence: whether a learner can improve at identifying missing, wrong, extra,
damaged, or miscounted instruments in a simulated local tray task. That scope
can be studied without a live hospital deployment by using representative
instrument sets, tray-specific count sheets, distractor items, inspection
criteria, and repeated pre/post tray-building tasks.

The resulting research question is:

> How can a local tray training and assessment system help novice users improve
> their ability to detect missing, wrong, extra, damaged, or miscounted
> instruments before supervised SPD tray-reconstruction work?

## 4. Literature And Related Work

TODO: Synthesize the evidence base that supports the final project direction.
This section should consolidate the literature instead of scattering the full
argument across every design section.

### 4.1 SPD Error And Tray-Readiness Evidence

TODO: Summarize tray defects, missing/wrong/extra instruments, delays,
assembly risk, visualization tasks, packaging errors, dirty or damaged
instruments, and count-sheet dependence.

### 4.2 SPD Training And Competency Context

TODO: Summarize certification and training realities, including CRCST/CBSPD
boundaries, hands-on hour requirements, preceptor burden, preparation and
packaging relevance, and supervised competency sign-off.

### 4.3 Local Tray And Count-Sheet Evidence

TODO: Explain why TrayGuard must use local modules: local names, aliases,
photos, quantities, variants, placement rules, specialty trays, custom trays,
loaner trays, and surgeon/procedure variation.

### 4.4 Learning Science And Simulation Evidence

TODO: Summarize retrieval practice, spacing, feedback, confidence/uncertainty
capture, simulation-based health-professions training, and sterile-processing
training precedents such as Ofstead et al.

### 4.5 Computer Vision Feasibility And Boundary Evidence

TODO: Summarize surgical-instrument CV as plausible future support while
explaining why deployment-grade CV is not the central FDR claim.

### 4.6 Market And Comparable Tools

TODO: Compare relevant commercial tools, research systems, and training
approaches. Suggested columns: tool, target user, relevant features, evidence
strength, and gap relative to TrayGuard.

## 5. Final Product Concept And Design Rationale

TODO: Define the final TrayGuard direction and explain why it was selected.

### 5.1 Final Product Concept

TODO: Define TrayGuard as a software-based local tray training and assessment
platform with retrieval-first study, quizzes, simulated tray sorting, feedback,
weak-item review, pre/post assessment, confidence capture, and exportable
instructor metrics.

### 5.2 Rationale For The Training-Centered Pivot

TODO: Explain why the project is no longer centered on a live clinical CV tray
checker: time constraints, validation risk, existing bounded CV literature,
and the stronger near-term value of reducing training and workflow-transfer
risks.

### 5.3 Alternatives Considered

TODO: Summarize candidate directions such as full CV tray checking, physical
camera-supported review, software-only training, printable QR/AprilTag cards,
and any other concepts from brainstorming or morphological analysis.

### 5.4 Selected Candidate And Backup Paths

TODO: State the selected candidate and Plan B options at the feature, physical,
CV, and evaluation levels.

## 6. Requirements Definition

TODO: Convert the problem and stakeholder needs into measurable requirements.

### 6.1 Element Definition

TODO: Define intended practice / other practice, artifact, problem,
technology, uses, perception, addresses, environment, function, behavior,
structure, intended effects, and side effects.

### 6.2 Objective Tree

TODO: Add the objective tree. Suggested top objective: improve novice readiness
for local tray reconstruction through repeatable, measurable simulated
practice.

### 6.3 Performance Specifications

TODO: List measurable targets from `docs/project/system_requirements.md`,
including completion rate, accuracy gain, post-test floor, severe-error
reduction, time target, confidence calibration, export completeness, and demo
success.

### 6.4 Quality Function Deployment

TODO: Add a House of Quality or compact QFD table linking stakeholder needs to
engineering characteristics and target values.

### 6.5 Requirement Traceability Matrix

TODO: Link each requirement to stakeholder need, design feature, evidence
source, validation method, current status, and future owner/task.

## 7. System Design

TODO: Describe the selected TrayGuard system at a level a future engineering
team can implement.

### 7.1 System Overview

TODO: Present the learning loop:

```text
local tray module -> pre-test -> retrieval-first cards -> quiz -> applied tray practice -> post-test -> metrics export
```

### 7.2 Subsystem Breakdown

TODO: Describe functional subsystems: local content/tray module, learning
workflow, quiz/retrieval practice, simulated tray sorting, scoring and
feedback, confidence/uncertainty, reporting/export, optional physical cards,
optional camera/CV support, and instructor review.

### 7.3 Functional Block Diagram

TODO: Add a procedural/data-flow diagram showing how content, learner actions,
scoring, feedback, and reports move through the system.

### 7.4 Dependency Diagram

TODO: Add a capability/cost dependency diagram and highlight the highest-risk
dependency wires.

### 7.5 Data Model And Module Contract

TODO: Describe `Instrument`, `TrayTemplate`, `LearningRun`, and
`AttemptResult`, including required fields and why they matter.

### 7.6 Mode Behavior

TODO: Summarize pre-test, study, quiz, practice sort, post-test, and
report/export behavior.

### 7.7 User Interaction / Experience

TODO: Describe the learner workflow and instructor workflow separately.

## 8. Training Module Design

TODO: Document the first local tray module and training content decisions.
Include module name, required instruments, distractors, lookalike pairs,
aliases, distinguishing features, photo/source rules, pre/post assessment
variants, scoring rubric, confidence/Not sure behavior, weak-item review, and
instructor verification.

## 9. Evaluation And Validation Plan

TODO: Define how the current design would be validated by a future team.

### 9.1 Current Evidence Available

TODO: State what exists now: literature-backed problem definition,
requirements, architecture, proposed module content, risk analysis, and future
task plan.

### 9.2 Formative Novice Study Plan

TODO: Define the first feasible novice study: participants, sample size,
pre/post sequence, measures, and success thresholds.

### 9.3 SPD Workplace Pilot Plan

TODO: Define the later SPD pilot requirements: local count sheet, local photos,
SPD educator review, technician participants, approval/privacy needs,
comparison condition, and operational outcomes.

### 9.4 Validation Claims By Evidence Level

TODO: For each major claim, list current support, required validation, what
would falsify it, and the next action.

### 9.5 Design Outcome Versus Requirements

TODO: Compare the current design package against each requirement. Mark each
requirement as satisfied by documentation, ready for implementation, ready for
formative test, blocked by missing prototype, blocked by missing SPD access, or
future clinical validation required.

## 10. Risk Assessment And Scope Boundaries

TODO: Consolidate CDR-style concerns and risk-reduction work.

### 10.1 Formal Risk Register

TODO: Include risk statement, cause, consequence, likelihood, severity,
mitigation, residual risk, and future owner/task.

### 10.2 Unknowns And Concerns

TODO: List the unanswered questions that cannot be resolved from the current
project state, such as educator usefulness, simulated-to-physical transfer,
authoring burden, confidence calibration, and future CV value.

### 10.3 Scope Boundaries

TODO: Summarize capability, study, clinical, local content, CV, reporting, and
physical prototype boundaries.

## 11. Broader Impacts And Ethics

TODO: Identify negative externalities and apply at least one ethical framework.
Consider unequal access, punitive use of learner metrics, overreliance on
simulated scores, reduction of supervised practice, printing/e-waste burden,
and bias toward represented instrument libraries.

## 12. Project Plan And Future Work

TODO: Turn the FDR into a handoff plan.

### 12.1 Project Plan Postmortem

TODO: Compare the original engineering plan to actual execution, including the
pivot toward literature synthesis and risk reduction.

### 12.2 Future Work Roadmap

TODO: Organize future work into phases: minimal software prototype, polished
verified module, novice study, report/instructor refinement, SPD educator
review, supervised SPD pilot, and optional CV support.

### 12.3 GitLab Epic / Issue Map

TODO: Summarize planned epics and issues for content authoring, learner
workflow, scoring, reporting, study protocol, instructor validation, optional
physical cards, and optional CV support.

### 12.4 Milestones And Gantt Chart

TODO: Include a proposed continuation schedule and label it as future work.

### 12.5 Budget

TODO: Separate software/prototype costs, physical teaching materials,
camera/stand costs if needed, participant/study costs, future pilot costs, and
labor hours by subsystem.

## 13. Discussion And Final Recommendations

TODO: State what stakeholders can conclude from this FDR, what they cannot
conclude yet, which risks have been reduced, which risks remain decisive, and
why the next team should build and test the software-first training loop before
investing in deployment-grade CV or clinical tray automation.

## References

TODO: Consolidate citations into `docs/bibliography.md` and keep report links
consistent.

## Appendices

TODO: Add supporting materials that would interrupt the body: problem
explication artifacts, design-method artifacts, full requirements artifacts,
system diagrams, training module tables, evaluation instruments, risk register,
budget, schedule, task matrix, and presentation materials.
