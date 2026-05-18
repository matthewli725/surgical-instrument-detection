# System Design

## Current Focus

TrayGuard's current product focus is an SPD training module that reduces
simulated time-to-competency for novice learners. The prototype should help a
learner practice local tray and instrument familiarity, then measure whether
the learner improves between a pre-test and a post-test.

The central stakeholder value is accessibility and modernization of SPD
education. TrayGuard should make local tray practice more repeatable,
self-paced, updateable, feedback-rich, and measurable before a learner reaches
supervised hands-on work. Design choices should therefore be justified by how
they reduce dependence on scarce preceptor time, make local tray knowledge
easier to practice outside scheduled labs, or give educators clearer evidence
about learner gaps.

Computer vision remains useful, but it is no longer the primary value claim or
an active experiment obligation. Existing camera, annotation, YOLO export,
model training, and live detection code should be treated as legacy
implementation support for possible future authoring assistance or visual
review. The current report should cite existing CV literature for feasibility
instead of relying on local mAP or lighting/glare experiments.

The current training system should support these functions.

- Load a local tray module from instructor-verified data.
- Show retrieval-first instrument cards with names, aliases, families, photos,
  notes, and distinguishing features hidden behind prompts.
- Run identification and feature quizzes for retrieval practice.
- Run simulated tray sorting in practice mode as applied retrieval with
  immediate feedback.
- Run pre-test and post-test tray sorting with no hints or feedback.
- Export learner metrics: accuracy, time, confidence, weak-item recovery, and
  error categories.

## Prototype Scope

TrayGuard should be described as a training and assessment platform, not as a
hospital-ready tray automation system. The useful system-design question for
this repository is therefore: what learning content should the prototype take
in, what evidence should it produce, what pieces does it need, and what should
stay explicitly out of scope?

### In Scope For This Prototype

- One seeded local tray curriculum with 8-12 required instruments and a small
  distractor pool.
- File-backed local tray and instrument authoring.
- Retrieval-first cards, identification quiz, weak-item review, and simulated
  tray sorting.
- Pre/post assessment with accuracy, time, confidence, and error breakdown.
- Immediate feedback in learning modes, suppressed feedback in assessment
  modes.
- Lightweight export for learner and instructor review.

### Out Of Scope For This Prototype

- Proof that TrayGuard shortens real hospital onboarding time.
- CRCST or CSPDT certification readiness claims.
- Replacement of supervised hands-on hours, preceptors, or competency sign-off.
- Universal manufacturer-agnostic instrument recognition.
- Autonomous tray approval without human confirmation.
- Proof of sterility, cleanliness, sharpness, alignment, or instrument
  mechanical function.
- Hospital-wide inventory tracking, sterilization records, or full instrument
  traceability across departments.
- Robotic manipulation, sorting, or closed-loop tray assembly.
- Broad claims about deployment readiness in real SPD operations.

## Core System Information

The core learning task is simple in structure even if local tray knowledge is
hard to acquire:

1. Load a local tray module.
2. Run a timed pre-test tray sort with no hints or feedback.
3. Let the learner answer retrieval-first card prompts.
4. Let the learner complete identification and feature quizzes.
5. Let the learner practice simulated tray sorting as applied retrieval with
   immediate feedback.
6. Repeat weak items if the schedule allows.
7. Run a timed post-test tray sort with no hints or feedback.
8. Export accuracy, time, confidence, weak-item recovery, and error-category
   metrics.

This framing keeps the product centered on measurable novice learning. It also
matches the strongest current adoption argument: reduce early training burden
by giving learners repeatable local practice before, during, or between
supervised hands-on experiences.

The simulation component is included because accessible SPD education should
not stop at recognition drills. Flashcards and quizzes help learners retrieve
names, aliases, functions, and distinguishing features, but tray work requires
using that knowledge against a count sheet. Simulated tray sorting/checking
therefore trains and measures a different competency: applying local
instrument knowledge to a tray-verification task.

## Accessibility And Modernization Design Decisions

Every major design choice should contribute to the same value proposition:
modernize SPD education by making local, applied practice easier to access and
easier to measure.

| Design Decision | Contribution To Accessible And Updated SPD Education |
| --- | --- |
| Local tray modules | SPD tray knowledge varies by site. File-backed modules let educators update count sheets, aliases, photos, quantities, distractors, and lookalikes without rebuilding the application. |
| Retrieval-first cards | Supports self-paced active recall before supervised practice. Learners can repeat names and distinguishing features without requiring continuous preceptor attention. |
| Identification and feature quizzes | Turns passive review into measurable retrieval attempts. The system can record accuracy, time, confidence, and weak items. |
| Simulated tray sorting/checking | Gives learners repeatable access to applied tray practice without requiring a full physical instrument set, a lab session, or a preceptor for every repetition. |
| Error-specific feedback | Updates the learning loop from delayed correction to immediate coaching. Feedback should identify `missing`, `extra`, `wrong`, `misidentified`, and `wrong_count` errors so learners know what to review next. |
| Weak-item review | Makes practice adaptive by focusing repetition on the instruments and tray rules a learner actually missed. |
| Confidence capture | Helps educators see overconfidence and uncertainty, not just right/wrong scores. High-confidence errors are especially useful coaching targets. |
| Pre/post assessment | Separates learning from evaluation and provides evidence that the module improves simulated performance rather than merely exposing learners to content. |
| Metrics export | Gives educators an updated way to track repeated errors, learner progress, and module-level weak points. |
| Optional QR/AprilTag cards | Adds low-cost physical interaction without requiring expensive instrument sets or fragile full-object computer vision. The physical layer supports access and engagement, but the software learning claim remains primary. |

The simulation does not need to reproduce an entire SPD room. Its purpose is to
simulate the educational bottleneck: can a learner apply local instrument
knowledge to a count sheet and detect tray errors? The minimum useful
simulation is therefore a count sheet, tray scenario, instrument options,
seeded errors, learner correction, feedback, and metrics.

This design should be described as a lower-cost preparation layer, not a
replacement for hands-on competency validation. The intended value is that
learners arrive at supervised practice with stronger local familiarity and
educators arrive with clearer weak-point data.

## Printable Card Adoption Rationale

A printable tray-practice kit with phone or tablet scanning is a plausible
education workflow because it combines familiar low-cost materials with mobile
learning. The adoption claim should still be cautious: this workflow is most
plausible for training programs, classrooms, and skills labs. Live SPD
departments would need additional review of device policy, cleaning, privacy,
storage, instructor setup burden, and whether learners are allowed to use
personal devices in the training space.

The closest precedents support parts of the workflow rather than proving this
exact SPD use case:

| Precedent | Relevance To TrayGuard | Design Implication |
| --- | --- | --- |
| QR codes in healthcare education | A scoping review found QR codes used in healthcare education for engagement, just-in-time learning, simulation, and training support, with advantages such as low cost, ease of creation, and rapid access to resources ([Karia et al., 2019](../bibliography.md#karia-et-al-2019)). | Printable codes are a reasonable access layer for instrument cards, local notes, answer reveal, and self-paced review. |
| Electronic flashcards in health professions | A recent scoping review documents widespread health-professions use of electronic flashcards ([Barrison et al., 2025](../bibliography.md#barrison-et-al-2025)). | The app-based retrieval portion is familiar to health-professions learners, but it should remain connected to tray simulation rather than standing alone. |
| Tangible mobile AR cue-card learning | NeuroVase is a recent preprint, so it should be treated as emerging design precedent rather than settled evidence. It is still highly relevant because it combines physical cue cards, tablet-based interaction, standalone card review, structured medical curriculum, pre/post knowledge assessment, usability measures, and a controlled user study comparing AR-supported learning against traditional paper-based learning ([Jahani et al., 2026](../bibliography.md#jahani-et-al-2026-neurovase)). | TrayGuard can use printable instrument cards as both offline study aids and digital triggers for app-based practice. The evaluation should similarly compare physical/digital practice against a more traditional learning condition. |
| Marker-based mobile learning and AR cards | Mobile augmented-reality anatomy work shows that marker/card-triggered learning materials can be evaluated for usability, perceived usefulness, and learning support in medical education ([Bolek et al., 2021](../bibliography.md#bolek-et-al-2021)). | AprilTags should be used only when spatial tracking or tray placement matters. QR codes are enough when the goal is simply opening the correct instrument record. |

The strongest adoption value is not novelty. It is that an instructor can print
or update a local tray kit, learners can practice outside scarce hands-on lab
time, and the software can return weak-item and error-category reports. For
that reason, QR codes should be the default low-friction marker. AprilTags are
appropriate only for the more advanced physical simulation case where the app
needs card identity, position, or orientation on a tray mat.

## Training Module Architecture

The training data model should stay small enough for file-backed authoring:

| Object | Role |
| --- | --- |
| `Instrument` | Stores the local name, aliases, family, image, notes, and distinguishing features used by retrieval cards and quiz questions. |
| `TrayTemplate` | Stores the tray name, version, required items, quantities, and distractors. |
| `LearningRun` | Stores learner/session identity, mode, task version, start, and completion time. |
| `AttemptResult` | Stores selected items, confidence, duration, score, and error categories. |

The scoring model should classify errors as `missing`, `extra`, `wrong`,
`misidentified`, and `wrong_count`. This is the minimum breakdown needed to
tell an instructor whether a learner lacks tray familiarity, confuses
lookalikes, or understands identity but not count-sheet quantities.

Mode behavior should be explicit:

| Mode | Hints | Feedback | Purpose |
| --- | --- | --- | --- |
| Pre-test | No | No | Baseline simulated competency. |
| Study | Yes | Yes | Prompt-before-reveal instruction and reference support. |
| Quiz | Limited after answer | Yes | Retrieval practice, confidence calibration, and weak-item discovery. |
| Practice sort | Yes | Yes | Applied retrieval and deliberate practice on the tray task. |
| Post-test | No | No | Comparable learning assessment. |

The detailed design rationale is in
[Training Module Design](training_module_design.md).

## Optional Camera-Supported Tray Check

The older tray-check workflow remains useful as technical background and a
future extension, but it is outside the current evaluation claim:

1. Load or enter the required instrument list for a tray.
2. Capture the current tray view with a camera.
3. Detect visible instruments and assign class labels with confidence scores.
4. Aggregate detections into observed class counts.
5. Compare observed counts against required counts.
6. Present a result that highlights what appears present, missing, extra, or
   uncertain.
7. Preserve the final decision as human judgment rather than silent automation.

This camera-supported path should not carry the project's learning claim. Existing
papers already make CV plausible in constrained surgical-instrument settings
([Deol et al., 2024](../bibliography.md#deol-et-al-2024),
[Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025),
[Xin et al., 2024](../bibliography.md#xin-et-al-2024)). Other work also shows
why deployment robustness cannot be assumed, especially across manufacturers
and sites ([Kienle et al., 2025](../bibliography.md#kienle-et-al-2025)). If
camera support returns later, it should be validated as site-specific review
support, not as universal autonomous tray approval.

## Technician UI Design Principles

These principles were written for the camera-supported tray-check UI, but the
same human-factors pattern applies to the training module: keep the primary task
visible, make feedback actionable, avoid noisy alerts, and preserve deliberate
assessment boundaries.

For the current project, apply these principles to the learning workflow. The
camera-specific examples below are retained as future support notes, not active
experiment requirements.

TrayGuard's interface should be designed as a high-stakes workflow aid, not as
a generic detector dashboard. The user should be able to understand the tray
state, decide what needs attention, and preserve human confirmation without
being forced through unnecessary controls. This is a safety and adoption
requirement, not only a visual-design preference.

The strongest UI principle is to minimize interaction cost for the normal tray
check while preserving deliberate review for risky states. Interaction cost
includes physical actions, reading, waiting, mode switching, and uncertainty
about what to do next. It should not be reduced to a fixed click target. General
usability guidance supports timely status feedback, visible actions, error
prevention, and efficient expert paths, while three-click-rule research warns
that raw click count alone is a poor success metric
([Nielsen Norman Group, accessed 2026](../bibliography.md#nielsen-norman-group-accessed-2026),
[Porter, 2003](../bibliography.md#porter-2003)). For TrayGuard, a small number
of meaningful actions is defensible; the action count should be validated
against task time, errors, and correction burden.

The expected technician-facing workflow is:

1. Select or confirm the tray requirement list.
2. Capture or start the tray scan.
3. Review one clear tray-status summary: complete, missing item, extra item, or
   needs review.
4. Correct, dismiss, or rescan only when the system gives a specific reason.
5. Confirm the final tray decision as human judgment.

The primary screen should therefore be organized around the tray decision, not
around model controls. The main view should show the camera evidence, the tray
status, and one primary action that matches the current state. Configuration
inputs such as model path, camera index, confidence threshold, and image size
belong in a setup or advanced-settings area for the prototype, not in the
technician's repeated decision path.

Status and feedback should be visual-first. The UI should provide a large,
plain-language tray state such as `Ready`, `Scanning`, `Complete`,
`Missing Item`, `Extra Item`, `Needs Review`, `Rescan Recommended`, or
`Camera Error`. It should pair color with text, shape, or icon cues rather than
depending on color alone, and dynamic status changes should be available to
assistive technologies when implemented in a web UI
([W3C/WAI Use of Color, accessed 2026](../bibliography.md#w3c-wai-use-of-color-accessed-2026),
[W3C/WAI Status Messages, accessed 2026](../bibliography.md#w3c-wai-status-messages-accessed-2026)).

Audio feedback can be useful, but it should be secondary, optional, and sparse.
A short sound can reinforce three events: scan complete, review needed, and
camera or model failure. It should not repeat, replace visual information, or
create a new alarm burden. Web-accessibility guidance discourages uncontrolled
automatic audio because it can distract users and interfere with screen readers,
and clinical decision-support literature warns that excessive low-value alerts
interrupt work and are eventually ignored
([W3C/WAI Audio Control, accessed 2026](../bibliography.md#w3c-wai-audio-control-accessed-2026),
[Olakotan and Yusof, 2021](../bibliography.md#olakotan-and-yusof-2021),
[Cánovas-Segura et al., 2023](../bibliography.md#canovas-segura-et-al-2023)).
Any production-facing design should include a mute or volume control and should
make every audio cue redundant with visible text.

Human-factors guidance for medical devices treats displays, auditory and visual
alarms, buttons, control logic, and feedback timing as part of the device-user
interface, shaped by user abilities and the use environment
([FDA Human Factors, accessed 2026](../bibliography.md#fda-human-factors-accessed-2026)).
That matters here because sterile-processing work can involve glare, noise,
interruptions, gloves, standing work, shared surfaces, and time pressure. The
TrayGuard UI should therefore favor large readable states, restrained alerts,
plain action labels, recoverable corrections, and a visible manual fallback.

The current prototype should evolve toward these interface requirements:

| Requirement | Design Direction |
| --- | --- |
| One primary action per state | Show the next meaningful action: start scan, rescan, review issue, confirm tray, or stop. Avoid presenting all controls as equally important. |
| Clear tray-status hierarchy | Summarize `Complete`, `Missing`, `Extra`, and `Needs Review` above detailed detections so the user does not have to infer tray status from boxes alone. |
| Fast correction and rescan | When the model is wrong or uncertain, provide direct correction, dismiss, and rescan paths instead of forcing the user to restart the workflow. |
| Specific review reasons | Label review prompts with the cause: low confidence, similar-class risk, glare, overlap, unknown object, or count mismatch. |
| Visual-first feedback with optional sound | Use persistent visible status as the source of truth. Use short optional audio only for major state changes. |
| Alert restraint | Escalate only conditions that change the tray decision or require user action. Keep informational updates quiet. |
| Human sign-off | Require explicit final confirmation for approval or flagged completion. The system should support the decision, not silently make it. |
| Manual fallback | Make it clear how to continue if the camera, model, or scan quality is unavailable. |

## Tray Status Logic From Confidence

This section is retained only for a future camera-supported tray-check path; it
is not part of the current training project or evaluation plan.

The Streamlit prototype currently exposes a single confidence threshold. That
threshold is useful as a model-control setting, but it is not enough to decide
whether a required instrument is truly present, missing, or uncertain. A
detector threshold only says which predicted boxes are allowed through the model
filter. It does not distinguish a genuinely absent item from a visible item
missed because of glare, occlusion, blur, camera placement, similar-class
confusion, or open-set behavior.

TrayGuard should therefore use confidence as one input to tray-status logic,
not as the tray-status logic itself. The safer pattern is a two-threshold review
band plus a scan-quality gate:

| User-Facing State | Decision Logic |
| --- | --- |
| `Present` | The required class has at least the required count of detections above a high `T_present`, there is no active similar-class or image-quality risk flag, and duplicate boxes have been reconciled. |
| `Needs Review` | The system has some evidence, but not enough for a quiet present result: detections fall between `T_review` and `T_present`, a similar class appears, the count is unstable, an unknown or extra object is plausible, or scan quality is degraded. |
| `Missing` | No candidate for the required class appears above low `T_review`, and scan quality is acceptable enough that absence is meaningful. |
| `Rescan Recommended` | The system lacks evidence for a required class, but glare, occlusion, blur, poor framing, or lighting makes a missing label unsafe. |

In pseudocode:

```text
if scan_quality_bad:
    rescan_or_review
elif observed_count(conf >= T_present) >= required_count and no risk flags:
    present
elif observed_count(conf >= T_review) > 0 or risk flags:
    needs_review
else:
    missing
```

This approach follows the evidence better than a single cutoff. Calibration
research shows that neural-network confidence is often not a reliable
probability of correctness, object-detection research shows that confidence
thresholds trade false positives against false negatives, and selective
classification research supports abstaining or routing cases to review when
the model cannot meet the desired risk level
([Guo et al., 2017](../bibliography.md#guo-et-al-2017),
[Küppers et al., 2022](../bibliography.md#kuppers-et-al-2022),
[Wenkel et al., 2021](../bibliography.md#wenkel-et-al-2021),
[Geifman and El-Yaniv, 2017](../bibliography.md#geifman-and-el-yaniv-2017)).
Open-set recognition work also supports treating "unknown" as a valid outcome
rather than forcing unfamiliar objects into the nearest known class
([Scheirer et al., 2013](../bibliography.md#scheirer-et-al-2013)).

Thresholds should be selected from local validation data by sweeping candidate
values for `T_review` and `T_present`. The sweep should report, by class and by
tray scenario:

- present precision and recall at `T_present`
- known-item recall at `T_review`
- false `Present` decisions for missing, wrong, extra, and unknown objects
- false `Missing` decisions when the item is present but hard to see
- review rate and rescan rate
- high-confidence wrong similar-class predictions
- calibration plots or calibration error for accepted detections

The selected thresholds should be saved with the model version, camera setup,
lighting setup, class list, and validation dataset. They should be retuned when
any of those conditions change. Transparency guidance for machine-learning
medical devices supports communicating known failure modes, confidence-related
information, local validation expectations, and use cases where the input may
not match the validation data
([FDA Transparency, accessed 2026](../bibliography.md#fda-transparency-accessed-2026)).

## Design Lessons From Close Prior Work

Rodrigues, Mayo, and Patros's HOSPITools study gives direct motivation for
TrayGuard's literature-backed CV boundary. Their surgical-tool dataset was built
for intelligent surgical-tool management, included 360 tool classes organized
across speciality, pack, set, and tool levels, and was evaluated under concrete
design variables: image size, class frequency, lighting/background variation,
held-out test data, and hierarchy-aware similarity
([Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)).
Most importantly for this project, they state that fine-grained tool
classification is difficult because many surgical tools are visually similar and
differ only in subtle ways. That supports designing training content around
lookalike instruments and distinguishing features. It no longer means this
capstone must run its own shape-similarity detector experiment.

Atabuzzaman et al.'s 2025 CVPR Workshop paper, "Real-Time Ultra-Fine-Grained
Surgical Instrument Classification," is the closest academic
precedent for TrayGuard's computer-vision direction. It targets a hospital CSSD workflow, uses real surgical
tray categories, and focuses on ultra-fine-grained distinctions between
visually similar instruments
([Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025)).

The paper supports several system-design choices:

- **Structured capture matters.** Their initial single-view setup performed
  poorly enough to motivate a dual-camera acquisition station. Their final
  design captures top and side views, including a side-angle view aimed at
  fine-grained tip details such as curvature, surface texture, and tooth
  pattern. TrayGuard should therefore treat camera placement as part of the
  product, not as a removable demo detail.
- **Multi-view evidence is useful for fine-grained tools.** Their architecture
  fuses top-view and side-view features because different views preserve
  different discriminative cues. For TrayGuard, the analogous requirement is to
  keep a future path open for multi-view capture, especially for instrument
  families that remain confusable from overhead imagery alone.
  Multi-view classification research supports this broader design idea: when a
  single image does not contain enough discriminative information, multiple
  literal views of the same object can improve classification
  ([Seeland and Mader, 2021](../bibliography.md#seeland-and-mader-2021)).
- **Real CSSD evaluation is possible but bounded.** Their deployment and user
  study show that CSSD-oriented instrument recognition can improve workflow
  efficiency. However, their task is one-instrument classification, not
  full-tray verification. TrayGuard should cite this as evidence that the
  technical direction is plausible, while still separately validating tray-level
  missing, extra, wrong-item, and review-needed behavior.
- **High accuracy does not remove failure-mode analysis.** A constrained
  platform can achieve excellent classification results, but a tray assistant
  still has to handle glare, colored light, occlusion, unknown instruments, and
  high-confidence similar-class confusion. For the current project, those are
  literature-backed limitations and future validation requirements, not local
  accuracy experiments.

The practical design implication is that TrayGuard should separate two sensing
modes. A tray-overview mode is useful for counting visible instruments and
finding missing or extra items against a required list. A future
single-instrument review mode, inspired by the two-view station in Atabuzzaman
et al., could be used when the overview model flags a similar-looking or
low-confidence item. This keeps the current prototype aligned with its
tray-level verification goal while acknowledging that ultra-fine-grained
classification may need more controlled imaging than a single overhead tray
view can provide.

## Physical Capture Setup

The current prototype should use the existing overhead camera stand as the
primary capture fixture, but the stand should be attached to a portable base
board rather than screwed into the user's table. This keeps the physical setup
aligned with the rest of the prototype: low infrastructure, repeatable camera
geometry, and easy movement between work surfaces.

The recommended tabletop setup is:

1. Bolt the camera stand's base plate through a portable board.
2. Use a 3/4 inch plywood or comparable rigid panel, ideally at least
   24 in. x 30 in. and preferably 24 in. x 36 in. when the arm is extended.
3. Place the stand near the rear-left or rear-right area of the board so the
   front working edge remains open.
4. Add large washers or a metal backing plate under the stand base to spread
   the load through the board.
5. Add rubber feet or a non-slip underside so the board does not slide on the
   table.
6. Add ballast on the rear/stand side if the camera arm creates tipping risk.

The supporting logic is practical rather than ornamental. Prior surgical
instrument CV work supports structured acquisition, including controlled camera
placement and view design, because fine-grained instrument recognition is
sensitive to capture geometry
([Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025),
[Lehr et al., 2023](../bibliography.md#lehr-et-al-2023),
[Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)).
Commercial copy-stand designs use the same general pattern: a rigid baseboard,
upright column, adjustable camera arm, leveling, and vibration control to keep
the camera aligned with the object plane
([Cambo, accessed 2026](../bibliography.md#cambo-accessed-2026)).
Document-camera and boom-stand designs also show why the camera support should
come from the rear or side of the work area: the fixture should hold the camera
over the scene while leaving the front of the workspace available for hands,
tools, and tray movement
([Meiji Techno, accessed 2026](../bibliography.md#meiji-techno-accessed-2026)).

This setup also supports the workflow claim. NIOSH defines ergonomics as
designing work tasks to fit worker capabilities, including the tools, lighting,
and equipment around the task
([CDC/NIOSH, 2024](../bibliography.md#cdc-niosh-2024)). OSHA workstation
guidance similarly emphasizes neutral posture, easy reach, and avoiding
awkward component placement
([OSHA, accessed 2026](../bibliography.md#osha-computer-workstations-accessed-2026)).
A board-mounted stand is therefore preferable to a table-screwed stand for the
prototype because it does not require modifying the work surface, can be
positioned without forcing the user around a fixed table constraint, and can be
removed when the capture task is finished.

The rolling standing version should treat the board-mounted stand as a
removable camera module. The wheeled structure should provide a stable
standing-height platform with raised stops, straps, pins, or toggle clamps that
secure the board without changing the camera geometry. This preserves the same
capture module across tabletop and standing workflows while avoiding a second
camera calibration problem.

### Tabletop Default With Rolling Standing Option

TrayGuard's physical setup should default to a tabletop camera module with an
available rolling standing base. This is a workflow-fit decision, not only a
fabrication convenience. Real SPD work can occur at seated benches, standing
stainless tables, height-adjustable prep/pack stations, and cart-like work
areas. The user-provided SPD workflow videos show this variation directly: one
reference shows a technician seated at a light plastic-looking work surface,
while another shows standing work at metal tables
([User-provided SPD video 1, accessed 2026](../bibliography.md#user-spd-video-1-accessed-2026),
[User-provided SPD video 2, accessed 2026](../bibliography.md#user-spd-video-2-accessed-2026)).

External guidance supports designing for this variability. OSHA's hospital
central sterile guidance identifies reaching, lifting, pushing/pulling carts,
continuous standing, and hard counter edges as musculoskeletal risks. Its
controls include redesigning workstations so supplies can be reached with
elbows close to the body, using rolling carts with large low-resistance wheels,
using height-adjustable work surfaces, and providing sit/stand stools
([OSHA Central Sterile Supply, accessed 2026](../bibliography.md#osha-central-sterile-supply-accessed-2026)).
SPD workstation suppliers make the same design point in product terms:
prep/pack workstations are sold as height-adjustable, ergonomic, flexible
systems that support different users, tasks, and accessories
([Skytron, accessed 2026](../bibliography.md#skytron-prep-pack-accessed-2026),
[Getinge, accessed 2026](../bibliography.md#getinge-prep-pack-accessed-2026),
[Southwest Solutions CSSD Tables, accessed 2026](../bibliography.md#southwest-cssd-tables-accessed-2026)).

The design response is a two-mode physical architecture:

| Mode | Use Case | Design Reason |
| --- | --- | --- |
| Tabletop camera module | Seated work, existing bench/table workflows, demos in small rooms, and low-cost data collection. | Lets the system sit on a user's existing work surface without drilling into the table. It keeps the tray area familiar and preserves portability. |
| Rolling standing base | Standing prep/pack tables, metal-table layouts, shared lab rooms, or demonstrations where no suitable table is available. | Provides a plug-and-play standing option while keeping the same camera geometry and board surface. Locking wheels allow positioning near existing workflows without rebuilding the camera fixture. |

This choice also reduces integration risk. A single fixed standing cart would
force every demo and future site into one posture and one table height. A
table-screwed fixture would be stable but would fail the portability test. A
tabletop module with a rolling adapter lets the prototype follow the local
workflow: put it on an existing seated table when that is how the technician is
working, or dock it onto a wheeled standing base when the environment is closer
to a standing prep/pack station. The simplification is that the prototype does
not yet provide true powered height adjustment like commercial SPD
workstations; instead, it provides two practical height modes within the
project's budget and fabrication scope.

### Material And Cleaning Assumptions

The prototype base-board recommendation is a capstone build choice, not a claim
that plywood is the correct material for an SPD-ready product. Plywood is
defensible for this stage because it is low-cost, rigid, easy to cut, easy to
drill, heavy enough to help resist tipping, and fast to modify while we are
still learning the required field of view, board size, stand position, ballast,
and setup time. Those are prototype variables, so a material that supports
iteration is useful.

Plywood is not defensible as an unqualified deployment material for a sterile
processing environment. The board should not be treated as sterile, should not
touch sterile instruments, and should not be part of the sterile barrier. In
the prototype workflow, the board is an environmental support surface for a
camera fixture, while the tray or instrument proxies remain in their own
staging area. If the project were moving toward a real SPD pilot, the base
should move to a smooth, sealed, nonporous, facility-approved material such as
high-density polyethylene, polypropylene, phenolic resin board, sealed aluminum
composite, stainless steel, or a commercial medical/workstation surface. The
specific choice would need review against the facility's disinfectants,
cleaning frequency, weight limits, and infection-prevention policy.

The camera stand should be treated the same way: acceptable for a prototype
capture fixture, not automatically acceptable as clinical equipment. It has
knobs, seams, clamps, cable-routing points, and textured surfaces that may be
harder to clean than a purpose-built medical cart or sealed camera mount. For
prototype use, the cleaning assumption should be limited to noncritical
environmental-surface handling: wipe the exterior surfaces before and after
demo sessions with an approved product that is compatible with the stand,
remove visible soil, keep the stand out of the direct tray-contact zone, and
use disposable or cleanable cable ties/guards to reduce dangling cable contact.
CDC guidance treats environmental surfaces as lower-risk than critical or
semicritical items, but still calls for regular cleaning/disinfection when
surfaces are visibly soiled and according to facility schedules
([CDC, accessed 2026](../bibliography.md#cdc),
[CDC Healthcare Equipment, accessed 2026](../bibliography.md#cdc-healthcare-equipment-accessed-2026),
[CDC Environmental Surfaces, accessed 2026](../bibliography.md#cdc-environmental-surfaces-accessed-2026)).

FDA reprocessing guidance reinforces the design direction for any future
clinical version: avoid surfaces and assemblies that retain debris, prefer
smooth cleanable surfaces, design for disassembly where needed, and validate
cleaning instructions rather than assuming that a wipe-down is enough
([FDA Reprocessing, accessed 2026](../bibliography.md#fda-reprocessing-accessed-2026),
[FDA Reprocessing Factors, accessed 2026](../bibliography.md#fda-reprocessing-factors-accessed-2026)).
Therefore the current physical build should be documented as a bench prototype
used to stabilize image capture. An SPD-ready version would require a separate
materials, cleanability, cable-management, and infection-prevention review.

If the final demo needs to look closer to real SPD work environments, the best
near-term compromise is to keep a plywood or comparable structural core but add
a replaceable smooth surface layer. A white HDPE sheet over the board visually
approximates a plastic work surface while improving wipeability compared with
raw plywood. A thin stainless-steel sheet over the board, or an inexpensive
commercial stainless work table, visually approximates the standing metal-table
environment seen in many SPD and food-service-style work areas. Supplier data
for common HDPE sheet stock emphasizes impact resistance, corrosion resistance,
and FDA-compliant resin, while inexpensive stainless tables are available as
NSF-listed commercial work surfaces
([U.S. Plastic, accessed 2026](../bibliography.md#us-plastic-hdpe-accessed-2026),
[California Cooking, accessed 2026](../bibliography.md#california-cooking-table-accessed-2026),
[Atosa, accessed 2026](../bibliography.md#atosa-stainless-table-accessed-2026)).
These sources support feasibility and visual/material direction; they do not
replace local SPD approval or cleaning validation.

The budget choice is to use a plywood structural board with an inexpensive
white or stainless-look surface skin if a physical demo is needed. This is a
prototype visual and fabrication choice, not a clinical material claim. The
current training project does not depend on camera measurements or detector
performance, but a visually plausible work surface can still help future teams
or reviewers understand how camera-assisted authoring or review might fit a
tray workspace. The more expensive HDPE, stainless sheet, or commercial
stainless-table options remain straightforward upgrades if the project moves
from capstone prototype to an SPD-facing pilot, but buying and validating those
materials is outside the current scope.

| Surface Option | Approx. Cost | Prototype Use | Strengths | Limits |
| --- | --- | --- | --- |
| Raw plywood | $25-40 for a 2 ft. x 4 ft. panel | Early fabrication and stability tests. | Cheapest rigid base; drillable, easy to modify, and adds useful weight. | Not visually SPD-like, porous unless sealed, and not appropriate to defend as a cleanable clinical surface. |
| White poster board or foam board skin | $0.50-10 per sheet | Cheapest plastic-looking visual mockup. | Gives a white surface for photos, layout trials, and quick camera-framing checks. | Paper-faced, not durable, not meaningfully cleanable, and should not be used for final material claims. |
| White adhesive shelf liner over plywood | $10-16 per roll | Preferred cheapest plastic-looking prototype surface. | Smooth white visual surface, replaceable, easy to apply, and close enough for CV framing/contrast tests. | Can wrinkle, peel, stain, or trap debris at seams; not a clinical material claim. |
| Stainless-look adhesive shelf liner over plywood | About $10-20 for small rolls; about $51 for a six-roll pack | Preferred cheapest metal-looking prototype surface. | Provides a faux metal shine and stainless visual cue without sheet-metal cost or sharp edges. | More reflective than white liner and may add glare; still only a visual mimic. |
| Sealed plywood with HDPE top sheet | $48-71 for 1/4 in. x 24 in. x 48 in. HDPE, plus the structural board | Better plastic-looking tabletop prototype and plausible pilot-direction material. | Smooth white plastic, more durable than liner, impact/corrosion resistant, and closer to a cleanable nonporous surface. | Edges, fastener holes, seams, and underside still need attention; HDPE sheet alone may flex unless thick or supported. |
| Plywood with thin stainless top sheet | About $62 for a 24 in. x 48 in. thin 304 stainless sheet, plus substrate | Better metal-looking portable prototype. | Looks closer to standing metal work tables and keeps the board portable. | Thin sheet needs a substrate, edges can be sharp, glare may affect vision tests, and it is not the same as a welded stainless table. |
| Commercial stainless work table | About $225-400 for lower-cost 24 in. x 48 in. tables; higher-grade models can exceed $900 | Strongest standing-environment visual match. | Existing food-service tables are sold as smooth stainless work surfaces; some are NSF-listed and provide standing height. | More expensive and less portable than a board; still not automatically an SPD-approved medical-device setup. |

The cost ranges above use current retail examples for project panels, poster
board, foam board, white shelf liner, stainless-look liner, HDPE sheet,
stainless sheet, and stainless work tables
([Home Depot Project Panels, accessed 2026](../bibliography.md#home-depot-project-panels-accessed-2026),
[Poster Board, accessed 2026](../bibliography.md#poster-board-walmart-accessed-2026),
[Office Depot Foam Board, accessed 2026](../bibliography.md#office-depot-foam-board-accessed-2026),
[Con-Tact Shelf Liner, accessed 2026](../bibliography.md#contact-shelf-liner-accessed-2026),
[Con-Tact Stainless-Look Liner, accessed 2026](../bibliography.md#contact-stainless-liner-accessed-2026),
[U.S. Plastic, accessed 2026](../bibliography.md#us-plastic-hdpe-accessed-2026),
[Best Metal Products, accessed 2026](../bibliography.md#best-metal-products-stainless-sheet-accessed-2026),
[California Cooking, accessed 2026](../bibliography.md#california-cooking-table-accessed-2026),
[Atosa, accessed 2026](../bibliography.md#atosa-stainless-table-accessed-2026)).

### Physical Setup Review Questions

These are the questions a reviewer should be able to ask without surprising
the team:

| Question | Current Answer |
| --- | --- |
| Why use the existing camera stand at all? | It already provides the most important capture functions for future visual support: rigid vertical support, overhead reach, adjustable height/arm position, and repeatable framing. Reusing it reduces build risk if later teams revisit camera-assisted authoring or review. |
| Why not keep screwing it into a table? | A table-screwed fixture is stable but not portable and requires modifying the work surface. A board-mounted fixture preserves the fixed stand geometry while allowing the setup to move between tables and be removed after use. |
| Why plywood? | Plywood is cheap, rigid, heavy enough to help stability, and easy to drill while board size, ballast, and camera position are still experimental. It is a prototype material, not a clinical material claim. |
| Is plywood sterile? | No. The board is not sterile, should not contact sterile instruments, and should not be presented as SPD-ready. It is an environmental support surface for prototype imaging. |
| Should we use plastic instead? | For an SPD-facing pilot, probably yes. Smooth nonporous plastic or metal would be easier to clean and defend. Plywood is acceptable only for low-risk lab/demo iteration. |
| Can we make the prototype visually match real SPD work areas? | Yes. The cheapest version uses white or stainless-look adhesive liner over plywood. The more realistic version uses HDPE, stainless sheet, or a stainless work table. This matters only for demos or future camera-supported work; the current training project does not depend on material realism. |
| Can the camera stand be cleaned easily? | Only partly. Smooth tubes are easier to wipe; knobs, clamps, seams, textured grips, and cables are weaker points. The prototype mitigation is to keep the stand outside the direct tray-contact zone and wipe exterior surfaces under a demo cleaning protocol. |
| What would change for a real SPD pilot? | Replace plywood with a sealed nonporous base, simplify the mount geometry, cover or reroute cables, minimize crevices, choose disinfectant-compatible components, and document a facility-approved cleaning SOP. |
| Does the rolling base change the cleanability problem? | Yes. Wheels, brakes, underside surfaces, rails, straps, and clamps add more surfaces to clean. A wheeled version should be treated as a cart-like environmental surface and reviewed separately. |
| What are we simplifying? | We are preserving a low-cost future capture fixture while the current project tests simulated learning. We are not validating sterility, reprocessing, disinfectant compatibility, CV robustness, or hospital deployment readiness. |

## Research Support Audit

This section provides evidence for our design decisions. A
choice can stay in the project only if it is either supported by evidence,
framed as a bounded prototype assumption, or converted into something we will
measure locally.

| Design Choice | Research Support | Defensible Stance |
| --- | --- | --- |
| Time-to-competency as the north star | SPD certification and training evidence shows that entry into practice requires hands-on hours, structured training, and preceptor support ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026), [Chobin, 2010](../bibliography.md#chobin-2010), [AORN Staff, 2025](../bibliography.md#aorn-staffing-shortage-2025)). | Measure simulated improvement in local tray familiarity. Do not claim reduced hospital onboarding time without a longitudinal SPD study. |
| Retrieval-centered learning loop instead of isolated cards | Simulation, retrieval practice, spacing, feedback, and pre/post testing are supported by health-professions and learning-science evidence, with direct SP training precedent in Ofstead et al. and digital-practice support from spaced education and electronic-flashcard research ([Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023), [Cook et al., 2011](../bibliography.md#cook-et-al-2011), [Roediger and Karpicke, 2006](../bibliography.md#roediger-and-karpicke-2006), [Larsen et al., 2009](../bibliography.md#larsen-et-al-2009), [Martinengo et al., 2024](../bibliography.md#martinengo-et-al-2024), [Barrison et al., 2025](../bibliography.md#barrison-et-al-2025), [Hattie and Timperley, 2007](../bibliography.md#hattie-and-timperley-2007)). | Build pre-test, retrieval-first cards, quizzes, applied tray practice with feedback, weak-item review, post-test, and metrics export as one module. |
| Local tray authoring instead of a universal database | Instrument families are reusable, but actual tray requirements are local: count sheets specify tray contents, quantities, sizes, and catalog/reference numbers; tray optimization depends on procedure, surgeon preference, usage likelihood, and stock decisions; specialty and loaner trays can be vendor-specific ([Nadeau, 2024](../bibliography.md#nadeau-2024), [dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021), [Ahmadi et al., 2023](../bibliography.md#ahmadi-et-al-2023), [Medline, 2025](../bibliography.md#medline-custom-trays-2025), [STERIS, 2021](../bibliography.md#steris-loaner-trays-2021)). | Start with file-backed instructor-verified modules. Treat universal recognition as out of scope. |
| Human authority instead of certification or autonomous approval | Healthcare AI literature warns about automation bias, deskilling, liability, and workflow fit ([Goddard et al., 2012](../bibliography.md#goddard-et-al-2012), [Natali et al., 2025](../bibliography.md#natali-et-al-2025), [Kelly, 2026](../bibliography.md#kelly-2026), [Zheng et al., 2023](../bibliography.md#zheng-et-al-2023)). | The system may teach, score, explain, and log, but instructors and supervisors remain responsible for real competency judgments. |
| Workflow-first learner UI | General usability guidance supports visible status, efficient action paths, error prevention, and recoverable mistakes. Human-AI guidance supports efficient invocation, dismissal, and correction when AI guesses wrong. Clinical alert literature warns that low-value alerts and added tasks can undermine acceptance ([Nielsen Norman Group, accessed 2026](../bibliography.md#nielsen-norman-group-accessed-2026), [Amershi et al., 2019](../bibliography.md#amershi-et-al-2019), [Olakotan and Yusof, 2021](../bibliography.md#olakotan-and-yusof-2021), [Cánovas-Segura et al., 2023](../bibliography.md#canovas-segura-et-al-2023)). | Design around the learning mode, not model controls. Use clear mode boundaries, fast practice feedback, and no hints during assessment. |
| CV feasibility as an external assumption | Few-shot object detection and surgical-instrument CV papers show that data-efficient detection and constrained instrument recognition are plausible ([Xin et al., 2024](../bibliography.md#xin-et-al-2024), [Wang et al., 2020 FSOD](../bibliography.md#wang-et-al-2020-fsod), [Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025)). | Cite existing papers for feasibility. Do not make local CV accuracy a capstone proof obligation. |
| CV generalization as a future validation problem | Kienle et al. show a large cross-manufacturer performance drop despite strong in-domain instrument-stand results ([Kienle et al., 2025](../bibliography.md#kienle-et-al-2025)). | Any future camera-supported feature needs site-specific validation. The current project should work without it. |
| Portable board-mounted overhead stand | Structured camera placement is already a design requirement for repeatable tray images. Copy-stand and boom-stand designs support a rigid base/column/arm pattern that keeps the capture plane stable while leaving the work area accessible. Ergonomics guidance supports arranging tools and equipment to preserve neutral posture and easy reach ([Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Cambo, accessed 2026](../bibliography.md#cambo-accessed-2026), [Meiji Techno, accessed 2026](../bibliography.md#meiji-techno-accessed-2026), [CDC/NIOSH, 2024](../bibliography.md#cdc-niosh-2024), [OSHA, accessed 2026](../bibliography.md#osha-computer-workstations-accessed-2026)). | Use the existing stand, but bolt it to a weighted portable board instead of screwing it into a table. Treat the board as the reusable capture module for both tabletop use and a future wheeled standing base. |
| Tabletop default with rolling standing option | SPD workstations are not one-size-fits-all. OSHA central sterile guidance calls out reach, prolonged standing, rolling carts, height-adjustable surfaces, and sit/stand stools, while commercial prep/pack tables emphasize ergonomic flexibility, height adjustment, accessories, and different user/task needs. User-provided SPD video references also show both seated plastic-looking work surfaces and standing metal-table workflows ([OSHA Central Sterile Supply, accessed 2026](../bibliography.md#osha-central-sterile-supply-accessed-2026), [Skytron, accessed 2026](../bibliography.md#skytron-prep-pack-accessed-2026), [Getinge, accessed 2026](../bibliography.md#getinge-prep-pack-accessed-2026), [Southwest Solutions CSSD Tables, accessed 2026](../bibliography.md#southwest-cssd-tables-accessed-2026), [User-provided SPD video 1](../bibliography.md#user-spd-video-1-accessed-2026), [User-provided SPD video 2](../bibliography.md#user-spd-video-2-accessed-2026)). | Make tabletop the default because it plugs into existing work surfaces. Provide a rolling dock as an optional standing-height adapter. This approximates workflow flexibility without claiming commercial powered height adjustment. |
| Lookalike tools as learning content | HOSPITools and Atabuzzaman et al. highlight subtle instrument differences; Alfred et al. identifies nomenclature and training as assembly factors ([Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Alfred et al., 2021](../bibliography.md#alfred-et-al-2021)). | Teach distinguishing features in retrieval-first cards and track `misidentified` errors separately from generic wrong answers. |
| Student participants as novice evidence only | Simulation and learning-science evidence supports novice practice studies, but SPD certification and work-system evidence show real work requires supervised hands-on competence ([Cook et al., 2011](../bibliography.md#cook-et-al-2011), [McGaghie et al., 2011](../bibliography.md#mcgaghie-et-al-2011), [HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026), [Alfred et al., 2021](../bibliography.md#alfred-et-al-2021)). | Student results can support first-use clarity and novice simulated learning, not SPD adoption or safety readiness. |
| Admin-facing metrics and traceability | Work-system studies and traceability reviews support recordkeeping for quality improvement, while economic AI reviews warn that technical performance alone is not a business case ([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021), [Fayad et al., 2025](../bibliography.md#fayad-et-al-2025), [Vithlani et al., 2023](../bibliography.md#vithlani-et-al-2023), [Kastrup et al., 2024](../bibliography.md#kastrup-et-al-2024)). | Export learner progress, repeated weak items, time, confidence, and error patterns. Treat ROI as future pilot work. |

## Implementation Defaults That Should Not Be Overclaimed

Some repository choices are good engineering defaults, not claims about the
best possible clinical design.

| Default | Current Use | Critique-Ready Interpretation |
| --- | --- | --- |
| File-backed tray and instrument data | Fast local authoring for one seeded module. | Good for a capstone project. A real training program would need role permissions, content review, versioning, and integration decisions. |
| Pre/post simulated tray sorting | Primary training-effectiveness evidence. | Measures simulated local familiarity, not live SPD competency. |
| Confidence ratings | Learner metacognition and instructor review. | Useful for spotting overconfidence and fragile knowledge; not a clinical safety score. |
| Existing YOLO/Streamlit tray-check code | Legacy demo and possible future visual support. | Not central evidence. Avoid presenting its detector metrics as proof of robustness. |
| Local ignored `data/`, `runs/`, and `weights/` folders | Keeps raw images, training outputs, and weights out of git. | Sensible prototype hygiene. Formal deployment would require access controls, retention policy, audit policy, and privacy review. |

## Main Components

The current training product concept can be understood as seven components:

1. **Local Curriculum Data**
   - Instrument cards, tray templates, quantities, aliases, families,
     distinguishing features, distractors, and module versioning.
   - The main risk is vague or nonlocal content that does not match what a
     learner is expected to assemble.
2. **Learning Mode Orchestration**
   - Pre-test, retrieval-first cards, quiz, practice sort, post-test, and
     export flow.
   - Assessment modes suppress hints and feedback; practice modes make feedback
     immediate and specific.
3. **Simulated Tray Sorting**
   - Learner selection of required instruments and quantities from a local item
     pool.
   - This is the primary competency proxy because it combines identity,
     count-sheet reading, and distractor resistance.
4. **Scoring And Feedback**
   - Error classification into missing, extra, wrong, misidentified, and
     wrong-count categories.
   - The system should explain what happened and what to review next, not only
     mark answers right or wrong.
5. **Learner Metrics And Instructor Reporting**
   - Accuracy, duration, confidence, error categories, high-confidence errors,
     low-confidence correct answers, and pre/post comparisons.
   - This is the evidence layer for simulated time-to-competency.
6. **Optional Camera And CV Support**
   - Camera capture, detection, and review states for future visual practice or
     authoring assistance.
   - This remains a support layer until the training loop is working.
7. **Local Data Lifecycle**
   - Module files, learner run records, export files, screenshots when
     applicable, and version references.
   - Prototype records should avoid patient information and should not be
     presented as a complete hospital audit system.

## Design Candidates And Selection

The design space can be described as three candidate architectures.

| Candidate | Description | Advantages | Main Limits |
| --- | --- | --- | --- |
| Workspace observation | Use a camera and computer vision model to detect visible instruments, count known classes, and compare the counts against a required list. | Does not require modifying instruments or replacing trays; matches the visual-verification failure mode; can be piloted with commodity hardware. | Sensitive to lighting, reflectivity, occlusion, similar-class confusion, and open-set objects. |
| Tagged identification | Add RFID tags, barcodes, or other identifiers to instruments and read the identifiers during tray preparation. | Strong item-level identity and traceability; less dependent on visual conditions. | Requires tags, engraving, readers, scanner workflows, integration, and maintenance. RFID and barcode studies support traceability value but also show infrastructure and workflow costs ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). |
| Instrumented placement | Use custom tray slots or embedded sensors to confirm that expected locations are occupied. | Can make placement checks simple in a highly standardized tray. | Requires specialized trays, restricts tray-layout flexibility, and does not naturally identify wrong-but-similar instruments. |

For this project, TrayGuard selects local file-backed simulation because it is the
best match for this repository's new constraints: it supports the
time-to-competency claim, avoids universal recognition overclaims, and can be
evaluated with pre/post learning metrics. Workspace observation remains the
best optional sensing architecture for future visual practice because it fits
the existing camera, annotation, YOLO export, model-training, and Streamlit demo
pipeline. This is a prototype selection rather than a claim that computer
vision is always superior to RFID or tray instrumentation.

## Fallback Strategy

The selected architecture should have graceful fallback paths.

| Level | Trigger | Fallback | What It Preserves |
| --- | --- | --- | --- |
| Content | The first tray module is too thin or confusing. | Reduce to one polished tray and improve cards, aliases, distractors, and feedback. | The learning claim remains measurable. |
| Assessment | Pre/post tasks are too similar or too easy. | Create parallel variants with matched difficulty and randomized item order. | Improvement is less likely to be a memorized replay. |
| Interaction | Feedback or confidence prompts slow learners. | Keep feedback concise and capture one simple confidence rating per attempt. | Practice remains useful without creating friction. |
| Participants | Only students are available. | Report novice learnability and simulated gains only; require SPD validation later. | The project avoids adoption overclaims. |
| Optional sensing | CV is unreliable within the timeline. | Keep sorting manual and use CV work only as future visual-practice support. | The training evidence still stands. |

## Current Implementation Mapping

The repository already contains foundations for the optional CV support layer:

- `src/micro_design_project/data_collection/` handles camera capture,
  annotation, and controlled data collection.
- `src/micro_design_project/detection.py` handles detector inference and
  annotated rendering.
- `src/micro_design_project/app/` provides the current live tray-check UI and
  count checklist flow.
- `src/micro_design_project/training/` and `scripts/` support dataset export,
  training, benchmarking, and weight export.

The biggest remaining system-design gap is the new training layer: local tray
module files, learner modes, scoring, feedback, and metrics export. The detector
demo can be reused later, but it should not block the training project.

## Prototype Requirements

The most useful requirements for this repository are prototype-demonstration
requirements rather than deployment requirements.

TrayGuard should demonstrate that:

- one local tray module can be loaded from data rather than code changes
- learners can complete pre-test, retrieval-first cards, quiz, practice sort,
  and post-test flows
- practice mode gives immediate feedback for missing, extra, wrong,
  misidentified, and wrong-count errors
- assessment modes suppress hints and feedback
- metrics export compares pre/post accuracy, duration, confidence, and error
  categories
- the result can be discussed as simulated time-to-competency evidence, not
  certification readiness or live SPD productivity
- optional CV code remains available for future authoring or visual-review
  support, but local CV experiments are not part of the active evidence plan

These requirements are intentionally narrower than field-readiness claims. They
fit the actual state of the codebase and the quarter plan better than strict
deployment-style targets such as full-shift uptime, hospital-grade false-alert
limits, or comprehensive SPD integration.

## Literature Gaps And Stakeholder Response

| Gap In The Literature | System Response | Stakeholder Meaning |
| --- | --- | --- |
| CV papers show feasibility but often under-test manufacturer, site, tray, and workflow variation. | Keep CV optional and locally verifiable. Use instructor-approved content as the source of truth. | Admins should not buy the prototype as autonomous inspection; trainees should not rely on it as final authority. |
| SPD error papers show real defects but do not isolate which training intervention reduces them. | Run a pre/post simulated learning study. | Students can help test novice learnability; SPD trainees still need future validation. |
| Training literature supports retrieval practice, simulation, spacing, and feedback but does not provide a ready-made SPD tray module design. | Build the module around local retrieval cards, quizzes, applied sorting, weak-item repetition, and error-specific feedback. | Trainees get repeatable practice; instructors get evidence about weak items. |
| Adoption literature is broad healthcare AI, not specifically SPD training assistants. | Report workflow friction, role boundaries, privacy assumptions, and pilot requirements. | Admins get a clearer approval path and know what remains unproven. |

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
