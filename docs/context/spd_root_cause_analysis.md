# SPD Root Cause Analysis

## Purpose

This document starts from scratch to frame the sterile processing department
(SPD) problem before selecting a solution direction. The initial concern is:

> There are not enough SPD technicians, and surgical instrument errors are
> causing delays or disruption in the operating room.

That concern contains two different things:

- a workforce condition: not enough qualified SPD capacity;
- a quality and reliability outcome: instruments are missing, wrong, damaged,
  contaminated, incorrectly assembled, or unavailable when needed.

A strong root cause analysis should treat the workforce condition as one system
input rather than the full answer. Staffing shortages may be an important
contributor, but the best problem framing should explain why the system fails
to produce complete, correct, functional, sterile, and available instrument sets
at the point of use.

## Evidence Anchors

The following evidence helps anchor the RCA without making the problem too
narrow:

- HSPA requires 400 hours of hands-on SPD experience for CRCST certification,
  including 120 hours in preparing and packaging instruments, which shows that
  instrument preparation is a major hands-on competency area
  ([HSPA CRCST](https://myhspa.org/certification/certification-overview/certified-registered-central-service-technician-crcst/)).
- A work-system study of sterile processing found tray defects across the
  reprocessing workflow, with assembly responsible for the largest share of
  recorded defects; examples included missing, wrong, extra, damaged, and
  incorrectly assembled instruments
  ([Alfred et al., 2021](https://qualitysafety.bmj.com/content/30/4/271)).
- A surgical-instrument error study found missing, wrong, extra, broken, tray,
  and contamination-related errors, and connected many observed errors to
  visual tasks such as inspection, identification, function checks, and tray
  assembly
  ([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).
- AORN describes SPD staffing shortages as a current operational issue shaped
  by limited training pipelines, market demand, and turnover
  ([AORN, 2025](https://www.aorn.org/about-aorn/aorn-newsroom/periop-life/article/5-proven-ways-to-address-your-sterile-processing-staffing-shortage)).

## Problem Narrowing

### Candidate Frames

| Option | Candidate Problem Frame | Strength | Limitation |
| --- | --- | --- | --- |
| 1 | Lack of qualified SPD technicians. | Highlights workforce pressure, hiring difficulty, retention, and training capacity. | Too solution-shaped. It assumes more people is the primary answer before analyzing process, product, knowledge, place, and policy factors. |
| 2 | SPD technicians make surgical instrument errors. | Points directly at missing, wrong, extra, damaged, contaminated, or misassembled instruments. | Too individual-blaming. It can hide system contributors such as tray complexity, interruptions, policies, transport, inventory, count sheets, and training design. |
| 3 | OR delays are caused by instrumentation errors. | Starts with the visible hospital impact and makes the problem operationally urgent. | Too downstream. OR delays can involve scheduling, room turnover, surgeon preference changes, supply chain, equipment availability, and case complexity. |
| 4 | Surgical instrument trays are not reliably complete, correct, functional, sterile, and available at the point of use. | Best balance. It focuses on the failure experienced by the OR while leaving room to analyze staffing, training, tray complexity, process design, location, and policy. | Still broad enough that the literature review must separate error types and workflow stages. |
| 5 | Novice SPD staff lack local instrument and tray familiarity. | Strong if the chosen solution will be training-centered. | Too narrow as the starting problem because experienced staff, policy, inventory, and logistics can also create errors. |

### Recommended Problem Frame

> Surgical instrument sets are not reliably complete, correct, functional,
> sterile, and available at the point of use, creating rework, delays,
> workarounds, and safety risk across the SPD-OR workflow.

This is the strongest framing because it:

- defines the failure in terms of readiness, not blame;
- includes both instrument errors and availability problems;
- allows staffing shortage to be analyzed as one cause instead of the only
  cause;
- connects SPD work to OR impact without claiming every delay is caused by SPD;
- supports multiple solution directions, including staffing, training,
  standardization, tray redesign, tracking, escalation, or workflow changes.

### Direct Effect For The Fishbone

Use this as the fishbone head:

> Unreliable surgical instrument readiness at point of use.

This effect includes:

- missing instruments;
- wrong instruments;
- extra instruments;
- wrong quantities;
- damaged or poorly functioning instruments;
- instruments with possible bioburden or cleaning concerns;
- incorrectly assembled instruments;
- packaging or sterilization readiness issues;
- trays unavailable because of transport, turnover, or location problems.

## RCA Boundary

This RCA focuses on:

- the SPD-to-OR workflow for preparing, assembling, transporting, and using
  surgical instrument sets;
- staffing capacity, skill mix, interruptions, and workload pressure;
- tray complexity, look-alike instruments, count sheets, inventory, and
  instrument condition;
- training, local knowledge, handoffs, policy, and escalation;
- errors that reach the OR or create rework before the case.

Separate analyses would be needed for:

- every possible cause of OR delay;
- national labor-market reform as a standalone problem;
- individual blame for one technician's mistake;
- sterile processing failures unrelated to surgical instrument readiness;
- claims about patient harm unless local incident data support them.

## Six-Category Root Cause Analysis

### People

Contributors:

- staffing shortages and vacancies;
- turnover and reliance on novice or temporary staff;
- uneven experience across shifts;
- production pressure during peak case volume;
- interruptions during count, inspection, assembly, and handoff;
- fatigue, overtime, or rushed work;
- limited educator or preceptor capacity.

Root cause mechanism:

SPD work requires sustained attention and specialized local knowledge. When the
department is understaffed or the skill mix is thin, technicians have less time
to inspect, identify, assemble, verify, and ask questions. Experienced staff may
be pulled into production instead of coaching. Novices may be exposed to complex
trays before they have enough supervised repetition.

Root cause hypothesis:

> The SPD workforce does not consistently have enough protected capacity,
> experience, and coaching time to complete high-detail tray preparation work
> without rushing or interruption.

Evidence from prior literature:

- AORN describes sterile processing technician shortages as a current workforce
  problem shaped by limited training programs, rising demand, and turnover
  ([AORN, 2025](https://www.aorn.org/about-aorn/aorn-newsroom/periop-life/article/5-proven-ways-to-address-your-sterile-processing-staffing-shortage)).
- HSPA requires 400 hours of hands-on SPD experience for CRCST certification,
  including 120 hours in preparing and packaging instruments, which reinforces
  that competency depends on supervised practice, not just classroom knowledge
  ([HSPA CRCST](https://myhspa.org/certification/certification-overview/certified-registered-central-service-technician-crcst/)).
- Chobin's AORN Journal survey found that most respondents estimated three to
  six months or six to twelve months to train employees to process general and
  specialty instruments, with substantial preceptor time and cost
  ([Chobin, 2010](https://www.sciencedirect.com/science/article/pii/S000120921000551X)).
- Alfred et al. identified production pressure, high turnover, training
  variation, and technician knowledge as performance-shaping factors in sterile
  processing assembly work
  ([Alfred et al., 2021](https://qualitysafety.bmj.com/content/30/4/271)).

### Product

Contributors:

- excessive tray complexity;
- large trays with many low-use instruments;
- look-alike instruments;
- inconsistent names, aliases, sizes, or manufacturer variants;
- damaged or aging instruments;
- insufficient backup inventory;
- specialty, loaner, or surgeon-specific trays;
- count sheets that do not match actual tray contents.

Root cause mechanism:

Some trays are hard to assemble correctly even when staff are competent. Large
instrument sets increase search, identification, and count burden. Look-alike
instruments increase substitution risk. Damaged instruments and limited backup
inventory can turn a small defect into an availability problem. If the count
sheet, physical inventory, and surgeon preference do not match, technicians are
forced to resolve ambiguity under time pressure.

Root cause hypothesis:

> The instrument set itself is often too complex, variable, or poorly matched to
> current count-sheet and inventory controls for reliable assembly under normal
> production conditions.

Evidence from prior literature:

- Alfred et al. found that assembly defects included missing, wrong, damaged,
  extra, and incorrectly assembled instruments, and linked failures to tray
  composition, instrument design, inventory, and unstandardized nomenclature
  ([Alfred et al., 2021](https://qualitysafety.bmj.com/content/30/4/271)).
- Nichol et al. defined wrong-instrument errors as incorrect instruments in a
  tray, often of a similar type, showing why look-alike instruments and local
  variants belong in the product branch of the RCA
  ([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).
- A scoping review of surgical tray rationalization describes tray
  rationalization as systematically reducing instruments needed for a procedure
  without compromising safety, which supports the idea that excessive tray
  contents create processing and assembly burden
  ([dos Santos et al., 2021](https://bmchealthservres.biomedcentral.com/articles/10.1186/s12913-021-06142-8)).
- Nichol et al. note that inpatient procedures are generally more complex,
  longer, and require more instruments, and that a larger number of trays or
  instruments increases the opportunity for errors
  ([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).

### Knowledge

Contributors:

- incomplete instrument identification knowledge;
- weak familiarity with local trays, aliases, and surgeon preferences;
- inadequate onboarding structure;
- limited competency validation after training;
- inconsistent feedback when errors are found;
- training materials that lag behind tray or policy changes;
- informal knowledge held by experienced staff but not documented.

Root cause mechanism:

SPD knowledge is both technical and local. A technician must know instrument
families, names, functions, inspection points, sizes, tray placement, count
requirements, local aliases, and escalation expectations. Classroom knowledge or
certification preparation may not be enough for a specific facility's trays.
When feedback is delayed or informal, repeated errors may not become learning.

Root cause hypothesis:

> Local tray knowledge is not consistently converted into current, measurable,
> role-specific competency before technicians are expected to assemble complex
> trays independently.

Evidence from prior literature:

- Alfred et al. found that completing trays involved major individual variation
  and that failures could be shaped by technician knowledge, missing or
  incorrect instrument photos, varied names, and training differences across
  sites
  ([Alfred et al., 2021](https://qualitysafety.bmj.com/content/30/4/271)).
- HPN's sterile processing guidance emphasizes that assembly technicians should
  follow count sheets rather than memory, and that count sheets should include
  complete tray names, contents, quantities, sizes, catalog/reference numbers,
  preparation and inspection steps, placement instructions, packaging, indicators,
  and destination/storage details
  ([HPN, 2024](https://www.hpnonline.com/sterile-processing/article/55247421/back-to-basics-in-the-spd)).
- Chobin's training-cost survey supports the knowledge burden by reporting
  multi-month training timelines and extended preceptor involvement for new
  sterile processing staff
  ([Chobin, 2010](https://www.sciencedirect.com/science/article/pii/S000120921000551X)).
- HSPA's CRCST experience requirements divide required hands-on hours across
  decontamination, preparation and packaging, sterilization/disinfection,
  storage/distribution, and quality assurance, showing that instrument readiness
  requires multiple linked knowledge domains
  ([HSPA CRCST](https://myhspa.org/certification/certification-overview/certified-registered-central-service-technician-crcst/)).

### Process

Contributors:

- manual inspection, sorting, counting, and assembly;
- non-standard tray build instructions;
- inconsistent count-sheet use;
- weak independent verification for high-risk trays;
- unclear handoff between decontamination, assembly, sterilization, storage, and
  transport;
- defects detected late, often at or near the OR;
- lack of closed-loop correction after errors.

Root cause mechanism:

The process has multiple points where an error can enter or escape: cleaning,
inspection, assembly, packaging, sterilization, storage, transport, picking, and
OR setup. If checks are manual, variable, or late, the system relies heavily on
individual attention. Late detection creates rework and delay because the tray
has already moved downstream.

Root cause hypothesis:

> The SPD-OR workflow does not reliably catch missing, wrong, damaged,
> contaminated, or misassembled instruments early enough to prevent rework or
> point-of-use disruption.

Evidence from prior literature:

- Alfred et al. analyzed 3,900 tray defects across 41,799 cases and found that
  55.0% of defects occurred during assembly; common assembly defects included
  missing instruments, broken/damaged/malfunctioning instruments, wrong
  instruments, incorrectly assembled instruments, and extra instruments
  ([Alfred et al., 2021](https://qualitysafety.bmj.com/content/30/4/271)).
- Nichol et al. directly observed 236 surgical instrument errors affecting 147
  cases; the three most common categories were missing/wrong/extra instruments,
  broken or poorly functioning instruments, and tray-related failures
  ([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).
- Nichol et al. found that errors tied to visualization tasks such as
  inspection, identification, function checking, and sorting accounted for 88.6%
  of observed errors, reinforcing that manual visual process steps are a
  vulnerable part of the workflow
  ([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).
- HPN's assembly guidance frames prioritizing trays, following count sheets, and
  inspecting instruments as core preparation, packing, and assembly practices
  ([HPN, 2024](https://www.hpnonline.com/sterile-processing/article/55247421/back-to-basics-in-the-spd)).

### Place

Contributors:

- long transport paths between SPD, storage, and OR;
- off-site or outsourced sterile processing;
- fragmented storage locations;
- inconsistent point-of-use return practices;
- poor visibility into tray location or readiness status;
- layout constraints that increase walking, searching, or batching;
- separation between OR demand signals and SPD production planning.

Root cause mechanism:

Even a correctly assembled tray can fail the readiness test if it is in the
wrong place, delayed in transport, stored inconsistently, or invisible to the
people who need it. Physical distance also weakens communication. When SPD and
OR teams do not share real-time visibility into demand, location, and readiness,
staff may discover problems too late.

Root cause hypothesis:

> The physical and information flow between SPD, storage, transport, and OR does
> not consistently make the right tray visible, reachable, and ready before it
> is needed.

Evidence from prior literature:

- STERIS describes loaner trays as instruments not owned or stored by the
  facility and notes that loaner workflows depend on visibility across case
  scheduling, vendor delivery, OR awareness, SPD awareness, IFUs, count sheets,
  status, location, and pickup
  ([STERIS, 2021](https://www.steris.com/healthcare/knowledge-center/sterile-processing/how-to-track-loaner-surgical-instrument-trays)).
- STERIS also identifies common loaner-tray challenges such as unexpected trays
  arriving in SPD, expected trays not arriving, unclear vendor contacts, unclear
  or unavailable IFUs, missing loaned instruments, and uncertainty about whether
  trays will arrive on time and be fit for use
  ([STERIS, 2021](https://www.steris.com/healthcare/knowledge-center/sterile-processing/how-to-track-loaner-surgical-instrument-trays)).
- HPN describes storage and transport between CS/SPD and procedural areas as
  essential parts of the process by which clean, sterilized instruments reach
  clinicians, and emphasizes that OR and CS/SPD teams share responsibility for
  safe and efficient handling and movement
  ([HPN, 2020](https://www.hpnonline.com/sterile-processing/article/21154165/kit-tray-and-kaboodle)).
- AORN's staffing-shortage article highlights a large off-site sterile
  processing model at Penn Medicine, illustrating that modern SPD work can span
  on-site and off-site facilities and therefore depends on coordination across
  place and workflow
  ([AORN, 2025](https://www.aorn.org/about-aorn/aorn-newsroom/periop-life/article/5-proven-ways-to-address-your-sterile-processing-staffing-shortage)).

### Policy

Contributors:

- inconsistent count policy or poor compliance;
- unclear escalation for incorrect counts or missing instruments;
- unclear ownership for count-sheet updates;
- weak rules for tray version control;
- productivity targets that compete with quality checks;
- incomplete maintenance or replacement thresholds;
- lack of standard definitions for error categories.

Root cause mechanism:

Policies decide what "correct" means and what staff should do when correctness
is uncertain. If policies are outdated, inconsistently followed, or not
translated into daily practice, technicians may improvise. If productivity is
rewarded more visibly than quality, staff may feel pressure to move trays
forward instead of stopping to escalate uncertainty.

Root cause hypothesis:

> Governance for count accuracy, escalation, tray changes, and quality feedback
> is not strong enough to keep daily practice aligned with instrument-readiness
> requirements.

Evidence from prior literature:

- HPN emphasizes that count sheets should be clearly written, standardized, and
  available to all sterile processing employees across all shifts, supporting
  the need for governance over count-sheet content and use
  ([HPN, 2024](https://www.hpnonline.com/sterile-processing/article/55247421/back-to-basics-in-the-spd)).
- Chobin's AORN Journal article on decontamination states that instrument
  processing requires coordination among facility leaders, OR staff, and SPD
  personnel, and that leaders should develop policies, procedures,
  accountability, education, and documentation for process steps
  ([Chobin, 2019](https://pubmed.ncbi.nlm.nih.gov/31465566/)).
- STERIS's loaner-tray guidance highlights the need to track compliance with
  loaned instrumentation policies and to provide SPD access to accurate IFUs and
  count sheets, reinforcing the policy role in managing non-routine trays
  ([STERIS, 2021](https://www.steris.com/healthcare/knowledge-center/sterile-processing/how-to-track-loaner-surgical-instrument-trays)).
- Nichol et al. note that traditional reporting of surgical instrument errors
  can be cumbersome, human-dependent, delayed, incomplete, and difficult to
  integrate with operational systems, which supports standard definitions and
  stronger quality-feedback governance
  ([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1)).

## Consolidated Root Cause Chain

```text
High case volume, staffing pressure, and tray complexity
  -> less time for training, inspection, verification, and escalation
  -> incomplete or inconsistent local tray knowledge and count-sheet use
  -> manual assembly errors or unresolved instrument defects
  -> missing, wrong, extra, damaged, contaminated, or misassembled instruments
  -> tray rework, last-minute substitutions, search time, case disruption, or OR delay
```

## Final Problem And Root Cause Framing

Use this as the main problem framing:

> Surgical teams cannot consistently rely on instrument sets being complete,
> correct, functional, sterile, and available at the point of use because the
> SPD-OR system lacks reliable controls for matching instrument-set complexity,
> staffing capacity, local knowledge, count-sheet accuracy, physical flow, and
> timely verification to the level required for consistent surgical instrument
> readiness.

Short version:

> Unreliable surgical instrument readiness is a system problem caused by the
> interaction of staffing capacity, tray complexity, local knowledge, manual
> process controls, physical flow, and policy compliance.

This framing explains how staffing interacts with complexity, knowledge,
process, place, and policy. It also frames errors as the output of a work
system.

## Literature-Supported Solution Directions

Because no local operational dataset is available, solution selection should be
motivated by the strongest patterns in prior literature. The RCA suggests
several possible directions:

- staffing and retention: improve hiring pipeline, retention, scheduling, and
  protected educator capacity;
- training and competency: standardize onboarding, local tray practice,
  competency checks, and feedback loops;
- tray rationalization: reduce unnecessary instruments, simplify complex trays,
  and standardize names and variants;
- process control: improve count-sheet use, independent verification,
  defect-tracking, and closed-loop corrective action;
- technology support: use instrument tracking, tray status visibility, image
  references, digital count sheets, or decision support where appropriate;
- location and flow: reduce transport friction, improve tray visibility, and
  align SPD production with OR demand;
- policy governance: clarify escalation, count-sheet ownership, version
  control, maintenance thresholds, and quality metrics.

The current literature makes three areas especially defensible as starting
points. Their feasibility differs for this project:

| Direction | Why It Is Supported | Why It Is Challenging Here |
| --- | --- | --- |
| Training and competency | SPD preparation requires substantial hands-on experience, local instrument knowledge, and repeated practice. Prior literature also shows training variation, technician knowledge, instrument identification, and count-sheet use are tied to assembly reliability. | This is the most feasible direction because it can be studied with simulated trays, public or instructor-created instrument examples, learning tasks, and pre/post assessment without entering a hospital SPD. |
| Process control and visual verification | Observed errors cluster around inspection, identification, function checking, sorting, and assembly, so better checks could plausibly reduce defects. | This would require access to real SPD workflows, live or representative tray assembly steps, current count sheets, staff observations, defect reports, and approval to study clinical operations. Without that access, the project could only speculate about workflow redesign. |
| Tray standardization and rationalization | Tray complexity, unnecessary instruments, naming variation, and count-sheet quality all shape assembly reliability. Literature on tray rationalization supports simplifying trays while preserving procedure needs. | This would require actual tray lists, instrument utilization data, surgeon preference cards, procedure requirements, inventory constraints, and clinical stakeholder approval. Without hospital and instrument access, there is no defensible way to decide which instruments are unnecessary or how a tray should be redesigned. |

Training and competency is therefore the best starting point for this project.
It addresses a real contributor identified in the RCA while staying within the
available evidence and access constraints. Unlike process redesign or tray
rationalization, a training intervention can be prototyped and evaluated without
modifying hospital workflows, touching sterile instruments, observing staff at
work, or using protected operational data.

The selected project direction should therefore focus on simulated local tray
familiarity: helping learners identify instruments, distinguish look-alikes,
understand count-sheet expectations, practice tray organization, receive
specific feedback, and show measurable pre/post improvement. It targets the
training portion of the SPD-OR readiness problem because that portion is
important, literature-supported, and feasible without direct hospital access.
Project-level clinical-transfer boundaries are consolidated in
[`../project/scope_boundaries_and_risks.md`](../project/scope_boundaries_and_risks.md).
