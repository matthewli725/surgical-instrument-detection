# Training Module Design

## Goal

TrayGuard's product goal is to reduce the time it takes novice sterile
processing technicians to reach tray and instrument familiarity. The prototype
cannot prove reduced hospital onboarding time by itself, so the measurable
claim should be narrower:

> TrayGuard reduces simulated time-to-competency for a local tray module by
> improving novice accuracy, speed, error recovery, and confidence between a
> pre-test and a post-test.

This keeps the project tied to the real staffing and training burden while
avoiding a claim that would require a longitudinal SPD field study.

## Evidence Base

| Design Decision | Evidence | Product Implication |
| --- | --- | --- |
| Use time-to-competency as the north star | HSPA requires 400 hands-on SPD hours for CRCST, and Chobin reports multi-month instrument-processing training with substantial preceptor cost ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026), [Chobin, 2010](../bibliography.md#chobin-2010)). | The product should reduce supervised explanation burden, not replace supervised competency sign-off. |
| Focus on tray and instrument familiarity | HSPA instrument resources emphasize identification, inspection, maintenance, names, uses, photos, and testing points; the CRCST outline weights preparation and packaging at 21% and includes package assembly, count sheets, item identification, and instrument placement; sterile-processing courses include tray assembly and instrument-identification units ([HSPA Surgical Instrument Resources, accessed 2026](../bibliography.md#hspa-instrument-resources-accessed-2026), [HSPA CRCST Content Outline, 2023](../bibliography.md#hspa-crcst-content-outline-2023), [Towson University, accessed 2026](../bibliography.md#towson-sterile-processing-accessed-2026)). | Local trays, local names, instrument families, variants, and distinguishing features belong in the core data model. |
| Treat assembly as a high-friction subtask, not the whole SPD curriculum | Alfred et al. found that most recorded tray defects occurred during assembly, while Nichol et al. found that most observed surgical instrument errors involved visualization tasks such as inspection, identification, function, and correct tray assembly ([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021), [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). | Sorting should be the capstone practice task for this module, while the product explicitly avoids claiming comprehensive SPD certification readiness. |
| Use simulation and hands-on-style practice | AORN describes simulation and hands-on practice as a way to build competence before formal roles; broad health-professions simulation evidence associates simulation with knowledge, skill, and behavior gains ([AORN Staff, 2025](../bibliography.md#aorn-staffing-shortage-2025), [Cook et al., 2011](../bibliography.md#cook-et-al-2011)). | Tray sorting should be the primary module activity, with cards and quizzes supporting that task. |
| Separate practice from assessment | Ofstead et al. used pre/post testing, lectures, hands-on practice, homework, and a booster session in an SP training pilot, with test scores improving and remaining high after two months ([Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)). | Pre/post assessment should suppress hints and feedback; practice should provide feedback. |
| Use retrieval practice and spacing | Retrieval-practice and learning-technique reviews support practice testing and distributed practice; adaptive spaced education achieved comparable test scores with fewer items in medical education ([Roediger and Karpicke, 2006](../bibliography.md#roediger-and-karpicke-2006), [Dunlosky et al., 2013](../bibliography.md#dunlosky-et-al-2013), [Kerfoot, 2010](../bibliography.md#kerfoot-2010)). | Quiz mode is not decoration. It should generate repeated recall prompts and record weak items for review. |
| Make feedback specific | Feedback research supports telling learners where they are going, how they are doing, and what to do next ([Hattie and Timperley, 2007](../bibliography.md#hattie-and-timperley-2007)). | Feedback should classify missing, extra, wrong, misidentified, and wrong-count errors and suggest the next review target. |
| Keep the module local and authorable | Instrument concepts may be shared, but actual tray requirements are local: count sheets specify contents, quantities, sizes, and catalog/reference numbers; optimization studies model tray contents around procedures, surgeons, usage likelihood, and stock decisions; commercial tools emphasize local count sheets, photos, tray assembly, and proficiency metrics ([Nadeau, 2024](../bibliography.md#nadeau-2024), [dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021), [Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023), [Tray Pacer, accessed 2026](../bibliography.md#tray-pacer-accessed-2026), [LayerJot SID, accessed 2026](../bibliography.md#layerjot-sid-accessed-2026)). | Start with file-based local trays and instructor-verified content; do not promise a universal instrument database. |

## Why The Content Must Be Local

The strongest wording is not that every surgical instrument is completely
unique. Many canonical names and instrument families are broadly recognizable.
The non-universal part is the training object: the exact tray a learner must
assemble or verify.

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
and tray rules through a module file or import. That is what makes the MVP
defensible for reducing simulated time-to-competency: learners practice the
tray they actually need to learn, not a generic instrument encyclopedia.

## MVP Decision

The minimum viable module is a single local tray curriculum with:

- a tray template containing 8-12 required instruments and a few distractors;
- study cards for each required instrument and distractor;
- a short identification quiz that records accuracy, time, and confidence;
- simulated tray sorting in practice mode with immediate feedback;
- pre-test and post-test tray sorting with no hints or corrective feedback;
- exportable metrics that compare pre/post accuracy, time, confidence, and
  error categories.

This means the MVP is not five independent features. It is one learning loop:

```text
local tray module -> pre-test -> study/quiz -> practice sorting -> post-test -> metrics export
```

## Data Contract

| Object | Required Fields | Purpose |
| --- | --- | --- |
| `Instrument` | `id`, `name`, `family`, `image`, `aliases`, `notes`, `distinguishing_features` | Supports study cards, quizzes, distractor generation, and local naming. |
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
| Pre-test | No | No | Yes | Baseline simulated competency. |
| Study | Yes | Yes | Optional | Learn names, families, aliases, and distinguishing features. |
| Quiz | Limited after answer | Yes | Yes | Retrieval practice and weak-item discovery. |
| Practice sort | Yes | Yes | Yes | Deliberate practice on tray organization. |
| Post-test | No | No | Yes | Comparable assessment after practice. |

## Tradeoffs

| Tradeoff | Choose For MVP | Why |
| --- | --- | --- |
| Tray sorting vs pure quiz | Tray sorting first | It maps better to competency and produces accuracy/time/error evidence; quiz supports retrieval but is too narrow alone. |
| Local authoring UI vs file-backed modules | File-backed modules first | It proves extensibility without spending the MVP on forms and validation UI. |
| Manual simulated sorting vs computer vision | Manual simulated sorting first | It lets the training claim stand without depending on detector reliability. CV can later assist authoring or visual review. |
| Immediate feedback vs assessment integrity | Feedback only in learning modes | Feedback improves practice but would contaminate pre/post measurement. |
| Confidence capture vs lower friction | Capture one simple rating per attempt | Confidence helps identify high-confidence errors and low-confidence correct answers, but too many prompts slow practice. |
| Student users vs SPD technicians | Students for early novice evidence; SPD validation later | Students can test learnability and simulated gains, but cannot prove SPD workplace transfer. |
| One tray vs broad content library | One polished tray | A complete loop with clean metrics is stronger evidence than many shallow, unvalidated cards. |

## Acceptance Criteria

The training module is evidence-ready when it can show:

- a learner completing a pre-test and post-test on comparable tray tasks;
- practice mode producing error-specific feedback;
- quiz mode recording correctness, time, and confidence;
- metrics export comparing pre/post accuracy, duration, confidence, and error
  counts;
- a new tray module loaded from data rather than code changes;
- documentation that the result is simulated training evidence, not proof of
  CRCST certification readiness or live SPD productivity.

## What Not To Claim

Do not claim the MVP:

- certifies a technician as competent;
- reduces real hospital onboarding time without a longitudinal field study;
- replaces preceptors, supervisors, certification, or hands-on hours;
- recognizes every manufacturer variant or hospital count sheet;
- proves live SPD tray assembly performance.

The defensible claim is smaller and stronger: TrayGuard gives novices repeated,
measured practice on local tray familiarity and can test whether that practice
improves simulated tray-sorting performance.
