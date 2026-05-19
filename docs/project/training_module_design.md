# Training Module Design

## Goal

TrayGuard's product goal is to help novice sterile processing technicians build
local tray and instrument familiarity through measured simulated practice. The
prototype should evaluate a bounded learning outcome:

> TrayGuard improves simulated tray-task proficiency for a local tray module by
> increasing novice accuracy, speed, error recovery, and confidence between a
> pre-test and a post-test.

This keeps the project tied to the staffing and training burden while using
evidence that the current prototype can collect. Certification and clinical
transfer boundaries are consolidated in
[Scope Boundaries And Risks](scope_boundaries_and_risks.md).

## Evidence Base

| Design Decision | Evidence | Product Implication |
| --- | --- | --- |
| Use simulated tray-task proficiency as the north star | HSPA requires 400 hands-on SPD hours for CRCST, and Chobin reports multi-month instrument-processing training with substantial preceptor cost ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026), [Chobin, 2010](../bibliography.md#chobin-2010)). | The product should reduce early familiarity-building burden by measuring local tray practice before supervised competency sign-off. |
| Treat TrayGuard as a supplemental practice layer | HSPA requires real SPD hours and some programs separate classroom or online theory from required hands-on experience, while programs with internships depend on clinical-site availability and learner schedules. Broader allied-health research likewise treats clinical placement capacity as a constrained workforce-pipeline problem ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026), [Penn Foster, accessed 2026](../bibliography.md#penn-foster-sterile-processing-accessed-2026), [Central Sterilization Solutions, accessed 2026](../bibliography.md#central-sterilization-solutions-in-person-accessed-2026), [AIMS Education, accessed 2026](../bibliography.md#aims-education-sterile-processing-accessed-2026), [Altamont Externship, accessed 2026](../bibliography.md#altamont-externship-accessed-2026), [McBride et al., 2020](../bibliography.md#mcbride-et-al-2020), [North Greater Sacramento COE, 2025](../bibliography.md#north-greater-sacramento-coe-2025)). | The product should provide repeatable preclinical and in-between-placement practice with exportable evidence for instructors. |
| Focus on tray and instrument familiarity | HSPA instrument resources emphasize identification, inspection, maintenance, names, uses, photos, and testing points; the CRCST outline weights preparation and packaging at 21% and includes package assembly, count sheets, item identification, and instrument placement; sterile-processing courses include tray assembly and instrument-identification units ([HSPA Surgical Instrument Resources, accessed 2026](../bibliography.md#hspa-instrument-resources-accessed-2026), [HSPA CRCST Content Outline, 2023](../bibliography.md#hspa-crcst-content-outline-2023), [Towson University, accessed 2026](../bibliography.md#towson-sterile-processing-accessed-2026)). | Local trays, local names, instrument families, variants, and distinguishing features belong in the core data model. |
| Treat assembly as a high-friction subtask inside SPD education | Alfred et al. found that most recorded tray defects occurred during assembly, while Nichol et al. found that most observed surgical instrument errors involved visualization tasks such as inspection, identification, function, and correct tray assembly ([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021), [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). | Sorting should be the capstone practice task because it combines identity, quantity, lookalike discrimination, and count-sheet use. |
| Use simulation and hands-on-style practice | AORN describes simulation and hands-on practice as a way to build competence before formal roles; broad health-professions simulation evidence associates simulation with knowledge, skill, and behavior gains ([AORN Staff, 2025](../bibliography.md#aorn-staffing-shortage-2025), [Cook et al., 2011](../bibliography.md#cook-et-al-2011)). | Tray sorting should be the primary module activity, with cards and quizzes supporting that task. |
| Use sterile-processing training precedents, with Ofstead as the closest match | Ofstead et al. evaluated borescope-based endoscope visual-inspection training for certified SP professionals using pre/post testing, lectures, hands-on practice, workplace homework, confidence/satisfaction surveys, and a booster; other SP training studies also report knowledge and practice gains after structured training with skills practice, mentoring, or local adaptation ([Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023), [Fast et al., 2019](../bibliography.md#fast-et-al-2019), [Shreckengost et al., 2022](../bibliography.md#shreckengost-et-al-2022)). | TrayGuard should copy the structure: baseline test, guided study, hands-on-style practice, separated post-test, confidence capture, and optional delayed retention check. |
| Center the module on retrieval practice and spacing | Retrieval-practice studies show that testing improves long-term retention compared with restudying and can outperform elaborative study alone; a medical-education randomized trial found repeated testing improved long-term retention; reviews support practice testing, distributed practice, spaced digital education, and electronic flashcards in health-professions education ([Roediger and Karpicke, 2006](../bibliography.md#roediger-and-karpicke-2006), [Karpicke and Blunt, 2011](../bibliography.md#karpicke-and-blunt-2011), [Larsen et al., 2009](../bibliography.md#larsen-et-al-2009), [Dunlosky et al., 2013](../bibliography.md#dunlosky-et-al-2013), [Martinengo et al., 2024](../bibliography.md#martinengo-et-al-2024), [Barrison et al., 2025](../bibliography.md#barrison-et-al-2025)). | The core interaction should be prompt-before-answer recall. Quiz, study, and sorting modes should generate repeated retrieval attempts, record weak items, and schedule review. |
| Make feedback specific | Feedback research supports telling learners where they are going, how they are doing, and what to do next ([Hattie and Timperley, 2007](../bibliography.md#hattie-and-timperley-2007)). | Feedback should classify missing, extra, wrong, misidentified, and wrong-count errors and suggest the next review target. |
| Keep the module local and authorable | Instrument concepts may be shared, but actual tray requirements are local: count sheets specify contents, quantities, sizes, and catalog/reference numbers; optimization studies model tray contents around procedures, surgeons, usage likelihood, and stock decisions; commercial tools emphasize local count sheets, photos, tray assembly, and proficiency metrics ([Nadeau, 2024](../bibliography.md#nadeau-2024), [dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021), [Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023), [Tray Pacer, accessed 2026](../bibliography.md#tray-pacer-accessed-2026), [LayerJot SID, accessed 2026](../bibliography.md#layerjot-sid-accessed-2026)). | Start with file-based local trays, instructor-verified content, local aliases, and versioned tray rules. |

## Why Retrieval Practice Is The Center

Retrieval practice is the instructional engine, while cards, quizzes, tray
sorting, feedback, and post-tests are different surfaces around that engine.
Learners should usually be asked to bring an answer to mind before the system
reveals it: name this instrument, choose the distinguishing feature, identify
the lookalike, recall the required count, or decide what belongs in the tray.

This matters because local tray familiarity is not just exposure to pictures. A
novice has to retrieve the right name, feature, quantity, and local rule under
uncertainty. Passive study can make a learner feel familiar with an item without
showing whether they can produce or use the knowledge later. Retrieval prompts
turn that hidden uncertainty into observable attempts, which lets the product
find weak items, repeat them, and export evidence about what still needs
instructor attention.

The app-style precedent is useful at the mechanism level. Tools such as
Quizlet, Anki, and language-learning apps are credible analogies when they use
active recall, spacing, immediate feedback, and weak-item repetition. TrayGuard
should borrow the mechanism, then anchor it to the task Ofstead makes
defensible for sterile processing: structured teaching plus hands-on-style
practice, image-based decisions, confidence capture, and delayed reinforcement.

Simulated tray sorting is therefore applied retrieval, not a separate activity
competing with quiz mode. The learner must retrieve which instruments belong in
the tray, apply counts, reject distractors, and distinguish known lookalikes.
Error-specific feedback turns the retrieval failure into the next practice
target by naming whether the problem was `missing`, `extra`, `wrong`,
`misidentified`, or `wrong_count`. The pre-test and post-test stay separate as
the measurement layer: they test whether repeated retrieval and applied practice
improve simulated tray-sorting accuracy, time, error patterns, and confidence.

## Why Ofstead Matters Most

Ofstead et al. is the strongest direct precedent because it evaluates
sterile-processing training for a difficult visual-inspection skill tied to
endoscope reprocessing. The task differs from tray assembly, but the learning
problem is close: learners must recognize visual cues, handle specialized
instruments or devices, distinguish normal from defective states, build
confidence without guessing, and communicate findings.

TrayGuard should borrow these design moves:

| Ofstead Design Move | TrayGuard Translation |
| --- | --- |
| Pre-test used before teaching. | Run a no-hints tray sort before study to reveal baseline knowledge gaps. |
| Lectures and demonstrations interleaved with hands-on practice. | Combine retrieval-first cards, worked examples, quiz prompts, and simulated tray sorting. |
| Test items included images and a `Not sure` option. | Use local instrument photos and capture confidence or uncertainty for each assessed item. |
| Hands-on homework applied the skill to real workplace endoscopes. | Use the physical demo tray or local photos of the exact teaching instruments, not generic web images. |
| Booster session revisited weak concepts and trainee-submitted examples. | Add a delayed retention check or review mode if the schedule allows. |
| Confidence and satisfaction were measured alongside test scores. | Export confidence, high-confidence errors, low-confidence correct answers, and workflow friction. |

## Why The Content Must Be Local

Local authoring matters because the training object is the exact tray a learner
must assemble or verify. Many canonical names and instrument families are
broadly recognizable, but the local count sheet defines the task.

The support is now strong enough to treat local authoring as a requirement:

- Count sheets are the local authority. HPN advises technicians to follow count
  sheets rather than memory and says count sheets should include tray name,
  contents, quantities, sizes, and catalog/reference numbers
  ([Nadeau, 2024](../bibliography.md#nadeau-2024)).
- Tray composition is a configuration problem, not a fixed universal list.
  Surgical-tray rationalization research frames the problem as deciding which
  instruments should be in which trays, how many instruments and trays are
  needed, and which trays map to which procedures
  ([dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021)).
- Surgeon and procedure needs affect tray contents. Ahmadi et al. model tray
  configuration using surgeon preference cards, procedure-instrument requests,
  usage probabilities, and inventory/reprocessing tradeoffs
  ([Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023)).
- Custom and specialty trays vary by hospital, surgical team, procedure,
  surgeon preference, and vendor loaner availability. Medline explicitly
  distinguishes standard, custom, and specialty surgical trays, and STERIS
  notes that loaner trays are not owned by the facility and require their own
  IFUs and count sheets
  ([Medline, 2025](../bibliography.md#medline-custom-trays-2025),
  [STERIS, 2021](../bibliography.md#steris-loaner-trays-2021)).

Design conclusion: TrayGuard should treat the public instrument concept as a
starting label, then attach local aliases, photos, quantities, variant details,
and tray rules through a module file or import. That is what makes the project
defensible as simulated tray-task practice: learners practice the tray they
actually need to learn, not a generic instrument encyclopedia.

## Project Decision

The first focused module is a single local tray curriculum with:

- a tray template containing 8-12 required instruments and a few distractors;
- retrieval-first study cards for each required instrument and distractor;
- short identification and feature quizzes that record accuracy, time, and
  confidence;
- simulated tray sorting in practice mode with immediate feedback;
- a weak-item review queue for repeated retrieval if the schedule allows;
- pre-test and post-test tray sorting with no hints or corrective feedback;
- exportable metrics that compare pre/post accuracy, time, confidence, and
  error categories.

This means the project is not five independent features. It is one learning loop:

```text
local tray module -> pre-test -> retrieval-first cards -> quiz -> applied tray practice -> post-test -> metrics export
```

## Data Contract

| Object | Required Fields | Purpose |
| --- | --- | --- |
| `Instrument` | `id`, `name`, `family`, `image`, `aliases`, `notes`, `distinguishing_features` | Supports retrieval-first cards, quizzes, distractor generation, and local naming. |
| `TrayTemplate` | `id`, `name`, `version`, `required_items`, `distractor_items`, `module_notes` | Defines the local count-sheet task without hard-coding one hospital inventory. |
| `LearningRun` | `id`, `learner_id`, `tray_id`, `mode`, `started_at`, `completed_at`, `task_version` | Separates pre-test, practice, quiz, and post-test attempts for analysis. |
| `AttemptResult` | `run_id`, `selected_items`, `confidence`, `duration_seconds`, `score`, `errors` | Provides the measurable evidence for learning gains. |

Scoring should classify these errors:

- `missing`: required item not selected;
- `extra`: non-required item selected;
- `wrong`: required slot filled with the wrong instrument;
- `misidentified`: selected item is a known lookalike or distractor for the
  intended item;
- `wrong_count`: correct item selected with the wrong quantity.

## Mode Behavior

| Mode | Hints | Corrective Feedback | Metrics | Use |
| --- | --- | --- | --- | --- |
| Pre-test | No | No | Yes | Baseline simulated tray-task proficiency. |
| Study | Yes | Yes | Optional | Prompt-before-reveal retrieval of names, aliases, families, and distinguishing features. |
| Quiz | Limited after answer | Yes | Yes | Retrieval practice, confidence calibration, and weak-item discovery. |
| Practice sort | Yes | Yes | Yes | Applied retrieval and deliberate practice on tray organization. |
| Post-test | No | No | Yes | Comparable assessment after practice. |

## Tradeoffs

| Tradeoff | Project Choice | Why |
| --- | --- | --- |
| Retrieval practice vs passive study | Retrieval practice first | Prompt-before-answer recall creates stronger learning evidence and exposes weak items. Reference content remains available after the attempt. |
| Tray sorting vs pure quiz | Tray sorting as applied retrieval | It maps to the target task and produces accuracy/time/error evidence; quiz supports repeated recall before applied practice. |
| Local authoring UI vs file-backed modules | File-backed modules first | It proves extensibility without spending the project budget on forms and validation UI. |
| Manual simulated sorting vs computer vision | Manual simulated sorting first | It lets the training claim stand on learner performance data. CV can later assist authoring or visual review. |
| Immediate feedback vs assessment integrity | Feedback only in learning modes | Feedback improves practice but would contaminate pre/post measurement. |
| Confidence capture vs lower friction | Capture one simple rating per attempt | Confidence helps identify high-confidence errors and low-confidence correct answers, but too many prompts slow practice. |
| Student users vs SPD technicians | Students for early novice evidence; SPD validation later | Students can test learnability and simulated gains. SPD validation can follow with workplace participants and supervised tasks. |
| One tray vs broad content library | One polished tray | A complete loop with clean metrics is stronger evidence than many shallow, unvalidated cards. |

## Acceptance Criteria

The training module is evidence-ready when it can show:

- a learner completing a pre-test and post-test on comparable tray tasks;
- practice mode producing error-specific feedback;
- quiz mode recording correctness, time, and confidence;
- weak-item review showing that missed or uncertain instruments are repeated;
- metrics export comparing pre/post accuracy, duration, confidence, and error
  counts;
- a new tray module loaded from data rather than code changes;
- documentation that the result is simulated training evidence, with clinical
  and certification boundaries linked to
  [Scope Boundaries And Risks](scope_boundaries_and_risks.md).

## Capability Claim

TrayGuard gives novices repeated, measured practice on local tray familiarity
and can test whether that practice improves simulated tray-sorting performance.
