# Scope Pivot Handoff


## Why We Are Pivoting

Professor and TA feedback exposed a major scope problem: the project needs to
create tangible stakeholder value and leave something another team can extend.
The current CV experiments are drifting toward an unrealistic claim: that a
small, self-collected dataset can show model generalization to real sterile
processing or hospital conditions.

That claim is not defensible. Surgical instruments vary by manufacturer,
hospital inventory, local count sheets, local nicknames, tray composition,
lighting, workflow, and instrument condition. Replicating existing datasets or
collecting a small custom dataset does not prove deployment readiness.

## Path Viability Check

Old idea: improve accuracy of assembling instruments.

- Benefit: Targets the final outcome directly: fewer assembly mistakes.
- Benefit: Connects clearly to quality, consistency, and safety motivation.
- Benefit: Could be strong if narrowed to one task, one error type, and one
  simple intervention.
- Risk: Requires a precise technical mechanism, not just a broad accuracy
  claim.
- Risk: Needs validation with real assembly data or realistic workflows.
- Risk: Accuracy becomes hard to prove when instruments, trays, and local
  standards vary.
- Viability: Valuable, but higher risk for the current project timeline and
  resources.
- Viability: Realistic only if scoped to simulated tasks or a tightly bounded
  tray workflow.

New idea: training platform for assembling instruments.

- Benefit: Easier to prototype, test, and present.
- Benefit: Produces a complete learning loop: pre-test, practice, feedback,
  post-test, and metrics.
- Benefit: Supports onboarding, repeated practice, and instructor-created local
  modules.
- Benefit: Still serves the accuracy goal by training people before real
  assembly work.
- Risk: Could feel generic if it becomes only static educational content.
- Risk: Needs measurable outcomes so the value is not just "people used the
  platform."
- Risk: Cannot claim workplace transfer without SPD validation.
- Viability: More realistic and presentation-ready for the current project.
- Viability: Strongest if evaluated with pre/post simulated tray sorting
  accuracy, time, confidence, and error categories.

Decision:

- Use the training platform as the core direction.
- Treat improved assembly accuracy as the purpose and evaluation target, not as
  a hospital-ready deployment claim.
- Preserve CV/few-shot work as optional support or future extension, not the
  central proof.

## Old Scope To De-Emphasize

Do not center the project on these claims:

- Our model can generalize to real hospital scenes.
- Our dataset is sufficient to show real-world SPD deployment readiness.
- Computer vision can reliably identify instruments across hospitals,
  manufacturers, and tray setups.
- The project directly reduces OR delays or lost OR minutes.
- The prototype improves real technician accuracy in live sterile processing.

These claims require hospital-specific validation, real instrument inventories,
clinical workflow testing, and much larger data coverage than we can support.

## New Core Scope

The strongest revised scope is:

> Build an extensible SPD training platform that helps new technicians learn
> surgical instruments and tray organization through interactive practice, with
> measurable improvement in simulated identification and sorting tasks.

The product should be framed as a teaching and assessment tool, not a deployed
automation system.

## Stakeholder Value

Primary stakeholder:

- New or trainee sterile processing technicians.

Secondary stakeholders:

- SPD educators and supervisors.
- Hospitals or training programs that need repeatable onboarding material.
- Future student teams that need an extensible project foundation.

Value proposition:

- Help novices become familiar with instrument names, visual differences,
  functions, and tray placement.
- Let instructors create practice modules from local tray lists and instrument
  photos.
- Measure learning gains with pre/post tasks.
- Create an extendable structure for future trays, instrument variants, and
  practice modes.

## Defensible Metric

Use simulated training metrics, not hospital deployment metrics.

Recommended primary metric:

- Change in novice performance from pre-test to post-test, reported as a
  simulated time-to-competency proxy.

Track:

- Instrument identification accuracy.
- Simulated tray sorting accuracy.
- Time to complete a tray sorting task.
- Error categories: missing, wrong, extra, and misidentified instruments.
- Learner confidence or perceived familiarity.

The wording matters. The prototype can claim improvement in simulated tray
familiarity after practice; it cannot claim shorter hospital onboarding time
without a longitudinal SPD study.

Possible study design:

1. Give participants a baseline identification or sorting task.
2. Let them use the trainer.
3. Give a comparable post-test.
4. Compare accuracy, completion time, error type, and confidence.

## Why Not The SPD Efficiency Direction

The "increase SPD technician efficiency and reduce lost OR minutes" direction
is valuable but too hard to prove directly. Accuracy is safety-critical, and we
cannot responsibly claim improvement in real tray verification accuracy without
field validation.

The better framing is upstream:

> OR delays and tray errors motivate the problem, but this project targets
> novice training and simulated tray familiarity.

This avoids overclaiming while still connecting the work to real SPD pain.

## Existing Tools And Differentiation

LayerJot/SID and similar tools weaken any claim that our value is simply
"identify an instrument from a phone photo." LayerJot already appears to be a
mature recognition/reference pipeline.

Our differentiation should be:

- LayerJot/SID: reference, lookup, recognition, IFU-style support.
- Our project: structured learning, practice, assessment, tray simulation, and
  extensible local curriculum.

The clean distinction:

> We are not competing with mature instrument recognition tools. We are
> building the educational layer that helps novices practice and lets
> instructors measure whether familiarity improves.

## Manufacturer And Hospital Variation

Manufacturer and hospital variation are serious objections if the system
depends on a universal recognition dataset. The defensible distinction is:
instrument concepts may be reusable, but real tray training content is local.
Count sheets specify tray contents, quantities, sizes, and catalog/reference
numbers. Tray-rationalization and tray-configuration studies model decisions
about which instruments belong in which trays, how many instruments and trays
are needed, and how surgeon-procedure preferences affect tray contents. Custom,
specialty, and loaner trays add variation by hospital, surgical team,
procedure, surgeon preference, and device manufacturer
([Nadeau, 2024](../bibliography.md#nadeau-2024),
[dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021),
[Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023),
[Medline, 2025](../bibliography.md#medline-custom-trays-2025),
[STERIS, 2021](../bibliography.md#steris-loaner-trays-2021)).

Design response:

- Do not promise universal recognition.
- Treat variation as local customization.
- Let each hospital or instructor add the instruments trainees actually need.
- Use local count sheets, local tray lists, local photos, local aliases, and
  local variants.

Data model direction:

- Canonical instrument concept: "Mayo scissors", "Adson forceps", etc.
- Local variant: manufacturer, size, SKU, local nickname, photo, notes.
- Tray template: count sheet plus required quantities.
- Training module: generated flashcards, quizzes, distractors, and sorting
  tasks from the tray template.

Low-overhead customization should mean:

- Easy authoring.
- CSV/count-sheet import where possible.
- Simple photo upload.
- Instructor verification.
- Reusable tray modules.

It should not mean:

- The model automatically learns all instruments from one or two images with
  clinical reliability.

## Few-Shot Learning Position

Few-shot learning can support the project, but only as an assistive layer.

Defensible claim:

> Few-shot visual matching may reduce authoring overhead in constrained
> instrument sets, but it does not eliminate local validation.

Why caution is needed:

- Fine-grained few-shot classification is an active research problem.
- Fine-grained classes have small inter-class differences and large intra-class
  variation.
- Surgical instruments are especially challenging because they can differ
  subtly while also changing appearance under lighting, pose, occlusion, glare,
  and manufacturer variation.
- CLIP-style models help with representation learning, but even CLIP is known
  to struggle with very fine-grained distinctions.

Recommended architecture:

1. Core training workflow.
2. Local instrument and tray data layer.
3. Optional embedding/prototype matching to suggest likely labels.
4. Human-in-the-loop instructor verification before learners see content.
5. Evaluation focused on learner improvement, not autonomous recognition.

## Evidence To Use

Use these as support for the pivot.

Training need and industry precedent:

- HSPA offers surgical instrument resources for identification, inspection,
  maintenance, and CIS exam prep:
  https://myhspa.org/education/publications/surgical-instrument-resources/
- HSPA eLearning includes instrument identification/care modules:
  https://elearning.myhspa.org/products/302-urology-instruments-identification-and-proper-care-and-handling
- Sterile Processing University says SPD training includes identifying
  instruments and assembling trays:
  https://www.spdceus.com/

Local variation / non-universal tray support:

- HPN count-sheet guidance says count sheets should include tray name,
  contents, quantities, sizes, and catalog/reference numbers:
  https://www.hpnonline.com/sterile-processing/article/55247421/back-to-basics-in-the-spd
- Surgical-tray rationalization review frames tray management as deciding
  which instruments belong in trays, how many to include, which trays map to
  which procedures, and how many trays to stock:
  https://bmchealthservres.biomedcentral.com/articles/10.1186/s12913-021-06142-8
- Ahmadi et al. model tray configuration from surgeon preference cards,
  procedure-specific instrument requests, usage probability, and reprocessing
  costs:
  https://www.mdpi.com/2227-7390/11/9/2219
- Medline distinguishes standard, custom, and specialty trays and ties custom
  trays to hospital, surgical-team, procedure, and surgeon needs:
  https://www.medline.com/strategies/perioperative/custom-surgical-tray-standardization-tips/
- STERIS describes loaner trays as manufacturer/vendor instruments used for
  specific procedures with their own IFUs and count sheets:
  https://www.steris.com/healthcare/knowledge-center/sterile-processing/how-to-track-loaner-surgical-instrument-trays

Training-pipeline evidence:

- Technology-enhanced simulation improves health-professions knowledge, skills,
  and behavior compared with no intervention:
  https://jamanetwork.com/journals/jama/fullarticle/1104300
- Simulation-based medical education with deliberate practice outperforms
  traditional clinical education for specific skill acquisition:
  https://academic.oup.com/academicmedicine/article-abstract/86/6/706/8352665
- Retrieval practice improves long-term retention compared with restudying:
  https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x
- Practice testing and distributed practice are high-utility learning
  techniques:
  https://pubmed.ncbi.nlm.nih.gov/26173288/
- Effective feedback should show where the learner is going, how they are
  doing, and what to do next:
  https://journals.sagepub.com/doi/10.3102/003465430298487

Medical training software precedents:

- Touch Surgery uses mobile surgical simulations with repeated attempts and
  scoring; a hand-surgery validation study found improvement across attempts:
  https://pubmed.ncbi.nlm.nih.gov/29363359/
- A randomized trial of VR orthopedic training found VR-trained novices
  completed the downstream procedure more often, made fewer incorrect steps,
  and finished faster than guide-only learners:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7431248/
- Body Interact uses virtual patient scenarios with immediate feedback,
  auto-grading, and educator analytics:
  https://www.wolterskluwer.com/en/solutions/lippincott-medicine/medical-education/body-interact-virtual-patient-care-simulator
- Surgical Science/Simbionix and Fundamental Surgery show the broader market
  precedent for medical simulation, objective scoring, and proficiency-focused
  training:
  https://surgicalscience.com/simulators/
  https://www.aaos.org/aaos-home//newsroom/press-releases/fundamental-surgery-cme-accreditation-fromaaos-vr-tka-simulation/

Commercial workflow/training tools:

- CensiTrac supports assembly instructions, multimedia aids, training tips,
  substitutions, productivity goals, and technician progress review:
  https://censis.com/solutions/censitrac/
- Tray Pacer frames new SPD tech training as taking 3-6 months and offers tray
  assembly training/productivity software:
  https://traypacersystem.com/
- LayerJot/SID is an instrument identification and learning app:
  https://www.layerjot.com/sid
- NuTrace's Nu Scanner includes an education use case for learning instrument
  names and part numbers:
  https://nutrace.io/Nu-Scanner

Error and cost motivation:

- BMJ Quality & Safety study: 3,900 tray defects across 41,799 surgical cases;
  assembly failures affected about 5% of cases, with missing instruments as a
  common assembly defect:
  https://qualitysafety.bmj.com/content/30/4/271
- BMC Surgery 2024 direct-observation study: 147 of 562 cases had at least one
  surgical instrument error, delays averaged about 10.16 minutes when delays
  occurred, and annual lost chargeable OR minutes were estimated at about
  $6.75M-$9.42M for the campus:
  https://link.springer.com/article/10.1186/s12893-024-02407-1
- Open Forum Infectious Diseases abstract: 86 errors across 17,348 processed
  trays, including 38 assembly errors:
  https://academic.oup.com/ofid/article/5/suppl_1/S630/5206842

Technician speed:

- "How to Measure Productivity in Sterile Processing" gives a usable benchmark
  that many departments can inspect and assemble about 3-4 trays per hour, with
  highly complex trays taking more than one hour. One hospital example reported
  average assembly time of about 12.5 minutes per instrument set:
  https://www.researchgate.net/publication/292671457_How_to_Measure_Productivity_in_Sterile_Processing

Few-shot and fine-grained learning:

- Few-shot survey: deep models usually need large datasets, and few-shot
  learning tries to adapt to new tasks from limited support examples:
  https://link.springer.com/article/10.1007/s13735-023-00279-4
- Fine-grained few-shot review: fine-grained classes are difficult because
  visually similar subclasses can differ only in subtle details, while pose,
  background, occlusion, lighting, and viewpoint create variation:
  https://www.mdpi.com/2673-2688/5/1/20
- OpenAI CLIP limitation: CLIP struggles with very fine-grained classification:
  https://openai.com/research/clip
- Zero-shot endoscopic instrument classification paper: vendor-specific and
  unseen instruments are a known challenge; sentence-level semantic
  descriptions can improve unseen-class recognition, but broader validation is
  still needed:
  https://link.springer.com/article/10.1007/s11548-025-03439-5

## Minimum Viable Module Decision

Build one evidence-complete training module rather than five shallow feature
islands. The MVP is:

```text
local tray module -> pre-test -> study cards -> quiz -> practice sorting -> post-test -> metrics export
```

Prioritize:

- P0: pre/post simulated tray sorting with accuracy, duration, confidence, and
  error breakdown.
- P0: file-backed local tray and instrument data.
- P1: study cards and identification quiz for retrieval practice.
- P1: practice sorting with immediate feedback.
- P2: polished instructor authoring UI.

Key tradeoffs:

- Tray sorting beats pure quiz for the MVP because it maps to competency and
  yields accuracy/time/error evidence.
- File-backed authoring beats polished authoring UI because it proves
  extensibility sooner.
- Manual simulated sorting beats CV-dependent sorting because the training
  claim should stand without model reliability.
- Feedback belongs in practice, not assessment, so pre/post metrics remain
  interpretable.
- Student pilots can support novice learnability, but SPD validation is needed
  before claiming workplace transfer.

## Suggested New Thesis

> We built an extensible SPD training platform that helps new technicians learn
> surgical instruments and tray organization through interactive practice. The
> system supports local tray and instrument customization, provides simulated
> sorting and identification tasks, and evaluates learner improvement through
> accuracy, completion time, error categories, and confidence.

## Suggested Scope Boundary

In scope:

- Training and assessment.
- Local tray/instrument authoring.
- Simulated sorting tasks.
- Instrument identification practice.
- Progress and error metrics.
- Evidence-backed motivation from SPD tray errors and training burden.
- Optional few-shot visual matching as a non-authoritative helper.

Out of scope:

- Real hospital deployment readiness.
- Autonomous tray approval.
- Universal manufacturer-agnostic recognition.
- Claims of reducing actual OR minutes lost.
- Claims of improving live technician accuracy without field validation.

## Key Message For The Team

The project is stronger if we stop trying to prove a hospital-ready CV model
and instead deliver a usable, extensible training system. The CV work can still
matter, but it should support authoring or future extension, not carry the
central value claim.
