# Scope Pivot Handoff

Use this as the morning restart note. The project needs to shift away from
"prove computer vision generalizes to real hospital trays" and toward a
stakeholder-centered, extensible training tool with measurable learning value.

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

- Change in novice performance from pre-test to post-test.

Track:

- Instrument identification accuracy.
- Simulated tray sorting accuracy.
- Time to complete a tray sorting task.
- Error categories: missing, wrong, extra, and misidentified instruments.
- Learner confidence or perceived familiarity.

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

Manufacturer variation is a serious objection if the system depends on a
universal recognition dataset. Instruments differ by manufacturer, length,
shape, finish, local naming, condition, and hospital inventory. Hospitals may
also use instruments from multiple manufacturers.

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

## Tomorrow Morning Priorities

Start with these in order:

1. Rewrite the one-sentence project thesis around SPD training and assessment.
2. Choose the primary metric: likely pre/post simulated tray sorting accuracy
   plus completion time.
3. Decide the minimum viable module:
   - instrument cards,
   - quiz mode,
   - tray sorting simulation,
   - feedback/error breakdown,
   - local tray authoring.
4. Identify what existing CV work becomes:
   - background motivation,
   - optional few-shot assist,
   - future work,
   - or deprecated scope.
5. Update the presentation/report narrative so every claim has one of these
   roles:
   - stakeholder value,
   - measurable training outcome,
   - extensibility,
   - real-world motivation,
   - limitation/future work.

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
