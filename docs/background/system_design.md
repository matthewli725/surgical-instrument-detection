# System Design

## Current Focus

Because we do not have access to a full set of real surgical instruments, and
because collecting a broad surgical dataset is outside the scope of this
prototype timeline, we are building evidence along several controlled
experiment axes. Instead of claiming full deployment readiness, we are testing
whether the core computer vision assumptions hold under conditions that
resemble the hard parts of surgical tray inspection.

The current system supports these functions.

- Camera-based image collection
- Manual bounding-box annotation
- Reusing labels across controlled lighting variants
- Exporting collected images to YOLO format
- Training and benchmarking object detection models
- Running a Streamlit tray-check UI for live camera detections

## Prototype Scope

TrayGuard should be described as a technician-centered verification assistant,
not as a fully autonomous tray-approval station. The useful system-design
question for this repository is therefore: what information should the
prototype take in, what should it produce, what pieces does it need, and what
should stay explicitly out of scope?

### In Scope For This Prototype

- Detect known instrument classes in tray-like scenes using a camera and an
  object detector.
- Count visible detections by class and compare them against a required list.
- Show the live tray state in a technician-facing interface.
- Surface missing-item, extra-item, and review-needed situations clearly enough
  to support human confirmation.
- Produce evidence that helps us study lighting, clutter, confusion, open-set,
  and workflow-fit risks.
- Support lightweight logging and reporting as a prototype quality-improvement
  story.

### Out Of Scope For This Prototype

- Autonomous tray approval without human confirmation.
- Proof of sterility, cleanliness, sharpness, alignment, or instrument
  mechanical function.
- Hospital-wide inventory tracking, sterilization records, or full instrument
  traceability across departments.
- Robotic manipulation, sorting, or closed-loop tray assembly.
- Broad claims about deployment readiness in real SPD operations.

## Core System Information

The core tray-checking task is simple in structure even if it is difficult in
practice:

1. Load or enter the required instrument list for a tray.
2. Capture the current tray view with a camera.
3. Detect visible instruments and assign class labels with confidence scores.
4. Aggregate detections into observed class counts.
5. Compare observed counts against required counts.
6. Present a technician-facing result that highlights what appears present,
   missing, extra, or uncertain.
7. Preserve the final decision as human judgment rather than silent automation.

This framing keeps the product centered on visual verification support. It also
matches the strongest current adoption argument: reduce visual search burden,
make uncertainty legible, and create useful review evidence without replacing
technician authority.

## Technician UI Design Principles

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
TrayGuard's controlled experiment plan. Their surgical-tool dataset was built
for intelligent surgical-tool management, included 360 tool classes organized
across speciality, pack, set, and tool levels, and was evaluated under concrete
design variables: image size, class frequency, lighting/background variation,
held-out test data, and hierarchy-aware similarity
([Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)).
Most importantly for this project, they state that fine-grained tool
classification is difficult because many surgical tools are visually similar and
differ only in subtle ways. That supports treating shape similarity, data
scarcity, capture conditions, and condition-held-out evaluation as first-class
experiment questions rather than incidental implementation details.

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
  still has to answer what happens under glare, colored light, occlusion,
  unknown instruments, and high-confidence similar-class confusion. Those
  questions remain part of TrayGuard's differentiating design work rather than
  a solved problem.

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
white or stainless-look surface skin. This is defensible for the computer
vision prototype because the current experiment needs the camera to see a
tray-like work surface with similar broad visual properties: light plastic-like
background for the seated workflow or gray metallic-looking background for the
standing workflow. The detector and capture tests are not measuring material
bioburden, chemical compatibility, or validated reprocessing. For those CV
purposes, a smooth white liner or stainless-look adhesive liner is similar
enough to study framing, glare, contrast, object placement, and workflow
ergonomics at low cost. The more expensive HDPE, stainless sheet, or commercial
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
| Why use the existing camera stand at all? | It already provides the most important capture functions: rigid vertical support, overhead reach, adjustable height/arm position, and repeatable framing. Reusing it reduces build risk and lets the project focus on tray-vision evidence rather than custom hardware fabrication. |
| Why not keep screwing it into a table? | A table-screwed fixture is stable but not portable and requires modifying the work surface. A board-mounted fixture preserves the fixed stand geometry while allowing the setup to move between tables and be removed after use. |
| Why plywood? | Plywood is cheap, rigid, heavy enough to help stability, and easy to drill while board size, ballast, and camera position are still experimental. It is a prototype material, not a clinical material claim. |
| Is plywood sterile? | No. The board is not sterile, should not contact sterile instruments, and should not be presented as SPD-ready. It is an environmental support surface for prototype imaging. |
| Should we use plastic instead? | For an SPD-facing pilot, probably yes. Smooth nonporous plastic or metal would be easier to clean and defend. Plywood is acceptable only for low-risk lab/demo iteration. |
| Can we make the prototype visually match real SPD work areas? | Yes. The cheapest version uses white or stainless-look adhesive liner over plywood. The more realistic version uses HDPE, stainless sheet, or a stainless work table. The cheap version is acceptable for CV testing because the visual background is similar enough for framing, contrast, glare, and workflow experiments, while the expensive version is a future upgrade outside the current budget/scope. |
| Can the camera stand be cleaned easily? | Only partly. Smooth tubes are easier to wipe; knobs, clamps, seams, textured grips, and cables are weaker points. The prototype mitigation is to keep the stand outside the direct tray-contact zone and wipe exterior surfaces under a demo cleaning protocol. |
| What would change for a real SPD pilot? | Replace plywood with a sealed nonporous base, simplify the mount geometry, cover or reroute cables, minimize crevices, choose disinfectant-compatible components, and document a facility-approved cleaning SOP. |
| Does the rolling base change the cleanability problem? | Yes. Wheels, brakes, underside surfaces, rails, straps, and clamps add more surfaces to clean. A wheeled version should be treated as a cart-like environmental surface and reviewed separately. |
| What are we simplifying? | We are testing stable, repeatable image capture and workflow fit. We are not validating sterility, validated reprocessing, disinfectant compatibility, or hospital deployment readiness. |

## Research Support Audit

This section provides evidence for our design decisions. A
choice can stay in the project only if it is either supported by evidence,
framed as a bounded prototype assumption, or converted into something we will
measure locally.

| Design Choice | Research Support | Defensible Stance |
| --- | --- | --- |
| Technician-centered assistant instead of autonomous approval | SPD error research supports the need for better visual verification, while healthcare AI literature warns about automation bias, deskilling, liability, and workflow fit ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Goddard et al., 2012](../bibliography.md#goddard-et-al-2012), [Natali et al., 2025](../bibliography.md#natali-et-al-2025), [Kelly, 2026](../bibliography.md#kelly-2026), [Zheng et al., 2023](../bibliography.md#zheng-et-al-2023)). | Keep the final decision human. The system may flag, count, explain, and log, but it should not silently approve trays. |
| Workflow-first technician UI | General usability guidance supports visible status, efficient action paths, error prevention, and recoverable mistakes. Human-AI guidance supports efficient invocation, dismissal, and correction when AI guesses wrong. Clinical alert literature warns that low-value alerts and added tasks can undermine acceptance ([Nielsen Norman Group, accessed 2026](../bibliography.md#nielsen-norman-group-accessed-2026), [Amershi et al., 2019](../bibliography.md#amershi-et-al-2019), [Olakotan and Yusof, 2021](../bibliography.md#olakotan-and-yusof-2021), [Cánovas-Segura et al., 2023](../bibliography.md#canovas-segura-et-al-2023)). | Design around the tray decision, not around model controls. Use one primary action per state, clear review reasons, fast correction, and explicit final confirmation. |
| Workspace observation as the first architecture | Visualization-related errors dominate observed instrument errors, and direct CV studies show surgical-tool detection/counting is feasible. RFID/barcode work supports traceability, but it also requires tags, readers, engraving, antennas, or scanner workflows ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). | Keep CV as the lowest-infrastructure prototype layer. Do not claim it is universally superior to RFID or barcode traceability. |
| Structured capture rather than arbitrary webcam input | Controlled surgical-instrument recognition studies use constrained lighting, background, and acquisition platforms; the closest CSSD paper moved to multi-view capture for fine-grained details ([Lehr et al., 2023](../bibliography.md#lehr-et-al-2023), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Seeland and Mader, 2021](../bibliography.md#seeland-and-mader-2021)). | Keep the overhead tray view for counting visible objects, but preserve a future side-view or single-instrument review path for confusable instruments. |
| Portable board-mounted overhead stand | Structured camera placement is already a design requirement for repeatable tray images. Copy-stand and boom-stand designs support a rigid base/column/arm pattern that keeps the capture plane stable while leaving the work area accessible. Ergonomics guidance supports arranging tools and equipment to preserve neutral posture and easy reach ([Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Cambo, accessed 2026](../bibliography.md#cambo-accessed-2026), [Meiji Techno, accessed 2026](../bibliography.md#meiji-techno-accessed-2026), [CDC/NIOSH, 2024](../bibliography.md#cdc-niosh-2024), [OSHA, accessed 2026](../bibliography.md#osha-computer-workstations-accessed-2026)). | Use the existing stand, but bolt it to a weighted portable board instead of screwing it into a table. Treat the board as the reusable capture module for both tabletop use and a future wheeled standing base. |
| Tabletop default with rolling standing option | SPD workstations are not one-size-fits-all. OSHA central sterile guidance calls out reach, prolonged standing, rolling carts, height-adjustable surfaces, and sit/stand stools, while commercial prep/pack tables emphasize ergonomic flexibility, height adjustment, accessories, and different user/task needs. User-provided SPD video references also show both seated plastic-looking work surfaces and standing metal-table workflows ([OSHA Central Sterile Supply, accessed 2026](../bibliography.md#osha-central-sterile-supply-accessed-2026), [Skytron, accessed 2026](../bibliography.md#skytron-prep-pack-accessed-2026), [Getinge, accessed 2026](../bibliography.md#getinge-prep-pack-accessed-2026), [Southwest Solutions CSSD Tables, accessed 2026](../bibliography.md#southwest-cssd-tables-accessed-2026), [User-provided SPD video 1](../bibliography.md#user-spd-video-1-accessed-2026), [User-provided SPD video 2](../bibliography.md#user-spd-video-2-accessed-2026)). | Make tabletop the default because it plugs into existing work surfaces. Provide a rolling dock as an optional standing-height adapter. This approximates workflow flexibility without claiming commercial powered height adjustment. |
| Object detection plus count aggregation | Automated surgical-instrument detection/counting has direct proof-of-concept support. General object-detection benchmarks also make bounding boxes and per-instance localization a standard way to evaluate visible objects in scenes ([Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Lin et al., 2014](../bibliography.md#lin-et-al-2014)). | Detect and count visible instruments. Do not infer fully hidden instruments from context. |
| YOLO-format datasets and a real-time detector baseline | YOLO is research-backed as a real-time object-detection family, and RT-DETR is a credible real-time transformer alternative ([Redmon et al., 2016](../bibliography.md#redmon-et-al-2016), [Zhao et al., 2024 RT-DETR](../bibliography.md#zhao-et-al-2024-rtdetr)). | Treat `yolo11s` as the current implementation baseline, not a research conclusion. Keep the model layer benchmarkable across YOLO sizes and RT-DETR. |
| Confidence threshold and "needs review" states | Open-set recognition research shows closed-set assumptions break when unknown classes appear. Calibration research shows modern neural-network confidence and object-detection confidence can be poorly calibrated. Selective-classification work supports rejecting or abstaining when a model cannot meet the desired risk level, and healthcare uncertainty-display studies support making uncertainty visible ([Scheirer et al., 2013](../bibliography.md#scheirer-et-al-2013), [Schlachter et al., 2020](../bibliography.md#schlachter-et-al-2020), [Guo et al., 2017](../bibliography.md#guo-et-al-2017), [Küppers et al., 2022](../bibliography.md#kuppers-et-al-2022), [Wenkel et al., 2021](../bibliography.md#wenkel-et-al-2021), [Geifman and El-Yaniv, 2017](../bibliography.md#geifman-and-el-yaniv-2017), [Kim et al., 2025](../bibliography.md#kim-et-al-2025)). | Use confidence as a review trigger, not as a safety probability. Separate the low review threshold from the high present threshold. Treat "missing" as valid only when scan quality is good enough for absence to be meaningful. |
| Controlled lighting variants and label reuse | Specular highlights are a known CV problem, controlled surgical-instrument papers treat lighting as an acquisition variable, and augmentation research supports label-preserving image variation when the object geometry and class remain unchanged. HOSPITools also captured surgical tools under natural, LED, halogen, and fluorescent lighting, making illumination a documented surgical-tool dataset variable rather than a demo-only concern ([Wang et al., 2016](../bibliography.md#wang-et-al-2016), [Wei et al., 2018](../bibliography.md#wei-et-al-2018), [Lehr et al., 2023](../bibliography.md#lehr-et-al-2023), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Shorten and Khoshgoftaar, 2019](../bibliography.md#shorten-and-khoshgoftaar-2019), [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)). | Reuse boxes only for controlled lighting variants where the object pose is unchanged. Evaluate on held-out lighting conditions rather than random near-duplicate splits. |
| Synthetic data for shape-similarity stress tests | Domain-randomization research supports synthetic-to-real transfer only when variation is broad enough and transfer is measured. Surgical-tool dataset surveys reinforce that dataset assumptions must be explicit, and HOSPITools shows the same need to evaluate dataset design variables such as class frequency, image size, and acquisition conditions rather than assuming one dataset construction is enough ([Tobin et al., 2017](../bibliography.md#tobin-et-al-2017), [Shorten and Khoshgoftaar, 2019](../bibliography.md#shorten-and-khoshgoftaar-2019), [Rodrigues et al., 2022a](../bibliography.md#rodrigues-et-al-2022a), [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)). | Use simulation for controlled stress testing, but claim value only if synthetic pretraining improves a matched real-proxy baseline. |
| Pairwise confusion and high-confidence wrong-class metrics | Fine-grained recognition literature frames subtle inter-class differences as the central risk, and direct surgical-instrument work shows clinically distinct tools can be visually similar. HOSPITools explicitly motivates this point: many surgical tools are visually similar and differ in subtle, hard-to-discern ways ([Wang et al., 2021](../bibliography.md#wang-et-al-2021), [Zhao et al., 2017](../bibliography.md#zhao-et-al-2017), [Lehr et al., 2023](../bibliography.md#lehr-et-al-2023), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)). | Do not rely on average mAP alone. Report per-class metrics, pairwise confusion, and high-confidence wrong similar-class predictions. |
| Held-out splits and dataset-design reporting | HOSPITools reserved images for a test set not seen during training and used experiments to study image size and class frequency. ML reproducibility guidance also supports recording dataset and model details ([Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b), [Heil et al., 2021](../bibliography.md#heil-et-al-2021)). | Keep train, validation, and test splits explicit. Report class list, image count, instance count, split rule, and the design variable each experiment isolates. |
| Local/no-PHI prototype data handling | Healthcare AI adoption literature identifies privacy, legal, and data-governance requirements as major deployment barriers ([Khalid et al., 2023](../bibliography.md#khalid-et-al-2023), [Chomutare et al., 2022](../bibliography.md#chomutare-et-al-2022)). | Keep prototype records focused on trays, detections, timestamps, and model versions. This reduces risk, but it is not a substitute for formal hospital privacy review. |
| Lightweight traceability records | Surgical-instrument traceability reviews and error-reporting studies support keeping usable evidence for quality improvement. ML reproducibility standards support recording model/data details ([Fayad et al., 2025](../bibliography.md#fayad-et-al-2025), [Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023), [Heil et al., 2021](../bibliography.md#heil-et-al-2021)). | Save scan ID, required list, observed counts, confidence values, review flags, corrections, screenshot references, dataset version, and model version. |
| Hard P6-style numeric targets | Several old numbers were useful ambition but not research-backed for SPD tray verification: one false alert per eight hours, two user actions, ten-minute setup, and fixed `0.5 m x 0.5 m` coverage. | Do not defend those as requirements. Replace them with local measurement plans until walkthrough and physical capture data exist. |

## Implementation Defaults That Should Not Be Overclaimed

Some repository choices are good engineering defaults, not claims about the
best possible clinical design.

| Default | Current Use | Critique-Ready Interpretation |
| --- | --- | --- |
| `model=yolo11s` | Fast baseline for training and demo inference. | Supported only as a YOLO-family real-time detector baseline. Compare with `yolo11m`, `yolo11l`, and `rtdetr-l` when performance claims matter. |
| `conf=0.25` | Demo slider default. | Not a safety threshold and not a missing-item rule. Production-style tray logic should use a low `T_review`, a higher `T_present`, and a scan-quality gate chosen from local validation curves, unknown false-positive rates, and review burden. |
| `imgsz=640`, `epochs=100`, `batch=16` | Reproducible training defaults. | Treat as starting points. Report them, tune when needed, and avoid presenting them as research-backed optima. |
| Streamlit UI | Fast prototype interface for live camera review. | Suitable for demonstrating workflow concepts. Production UI claims need separate usability testing and implementation work. |
| Local ignored `data/`, `runs/`, and `weights/` folders | Keeps raw images, training outputs, and weights out of git. | Sensible prototype hygiene. Formal deployment would require access controls, retention policy, audit policy, and privacy review. |

## Main Components

The current product concept can be understood as seven components:

1. **Imaging And Inspection**
   - Camera, scene framing, and practical lighting conditions.
   - The main risk here is image quality degradation from glare, shadow,
     reflectivity, blur, and camera placement.
   - Close prior work suggests that a single overhead view may be insufficient
     for ultra-fine-grained instrument distinctions, so the sensing design
     should preserve a path to side-view or review-station capture when needed.
2. **Edge Compute And Operator Interface**
   - Local runtime, display, user controls, and status indicators.
   - The prototype should keep session data local by default and avoid patient
     information entirely. This is a risk-reduction choice aligned with
     healthcare AI privacy concerns, not a complete compliance claim.
3. **Workflow Orchestration**
   - Tray-session state, capture, inference, validation, review, rescan, and
     completion flow.
   - Human-in-the-loop actions such as confirm, override, and recapture belong
     here rather than inside the detector.
4. **Computer Vision Inference**
   - Detection model, confidence scores, and class-level predictions.
   - The main risk here is confusion between similar tools, missed detections,
     and unsafe high-confidence errors.
   - The model should distinguish tray-level detection from single-instrument
     classification, since the latter can be tested under more controlled views.
   - The current YOLO-based implementation is an experiment baseline. The
     architecture should stay swappable so model-family comparisons remain
     possible.
5. **Tray Validation And Decision Support**
   - Required-list parsing, observed-count aggregation, and tray-status logic.
   - This is where the system turns raw detections into missing, extra, and
     review-needed information.
   - Future versions should support allowed alternates, confidence thresholds,
     and strict or relaxed review modes only when those rules are explicit.
6. **Knowledge Management**
   - Tray definitions, required instrument lists, label taxonomy, and model
     version alignment.
   - This avoids a quiet mismatch between model class names and the tray
     definition being checked.
7. **Data Lifecycle And Reporting**
   - Saved results, confidence values, screenshots or frame references, and
     repeat-pattern reporting.
   - This is necessary for a buyer-facing quality story, not just demo output.

## Design Candidates And Selection

The design space can be described as three candidate architectures.

| Candidate | Description | Advantages | Main Limits |
| --- | --- | --- | --- |
| Workspace observation | Use a camera and computer vision model to detect visible instruments, count known classes, and compare the counts against a required list. | Does not require modifying instruments or replacing trays; matches the visual-verification failure mode; can be piloted with commodity hardware. | Sensitive to lighting, reflectivity, occlusion, similar-class confusion, and open-set objects. |
| Tagged identification | Add RFID tags, barcodes, or other identifiers to instruments and read the identifiers during tray preparation. | Strong item-level identity and traceability; less dependent on visual conditions. | Requires tags, engraving, readers, scanner workflows, integration, and maintenance. RFID and barcode studies support traceability value but also show infrastructure and workflow costs ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). |
| Instrumented placement | Use custom tray slots or embedded sensors to confirm that expected locations are occupied. | Can make placement checks simple in a highly standardized tray. | Requires specialized trays, restricts tray-layout flexibility, and does not naturally identify wrong-but-similar instruments. |

TrayGuard currently selects workspace observation because it is the best match
for this repository's constraints: low physical-infrastructure burden, direct
study of the visual inspection problem, and compatibility with the existing
camera, annotation, YOLO export, model-training, and Streamlit demo pipeline.
This is a prototype selection rather than a claim that computer vision is always
superior to RFID or tray instrumentation. For a hospital-wide traceability
program, RFID or barcode systems may be the right architecture; for this project,
computer vision is the most testable first layer of tray-readiness support.

## Fallback Strategy

The selected architecture should have graceful fallback paths.

| Level | Trigger | Fallback | What It Preserves |
| --- | --- | --- | --- |
| Sensing | Glare, shadow, or camera placement makes detections unstable. | Add controlled lighting, fixed background, clearer tray staging, or a side/review view. | The workspace-observation concept remains intact while reducing image-quality variation. |
| Perception | Fine-grained class recognition is unreliable for visually similar instruments. | Route low-confidence or similar-pair cases into review, or count broader instrument groups when that still answers the tray question. | The system still supports verification without pretending every class distinction is solved. |
| Interaction | Alerts or rescans slow the user. | Switch from automation-style results to guided review language, clearer rescan prompts, and fewer high-interruption alerts. | Technician authority and workflow acceptance remain central. |
| Architecture | Workspace observation cannot meet local reliability needs. | Revisit tagged identification or hybrid CV-plus-tag workflows. | The readiness-verification goal remains even if the sensing method changes. |
| Full system | Automated detection is not reliable enough within the project timeline. | Deliver a semi-automated checklist assistant that guides manual confirmation and logs evidence. | The project still produces measurable workflow and documentation value. |

## Current Implementation Mapping

The repository already contains the foundations of those components:

- `src/micro_design_project/data_collection/` handles camera capture,
  annotation, and controlled data collection.
- `src/micro_design_project/detection.py` handles detector inference and
  annotated rendering.
- `src/micro_design_project/app/` provides the current live tray-check UI and
  count checklist flow.
- `src/micro_design_project/training/` and `scripts/` support dataset export,
  training, benchmarking, and weight export.

The biggest remaining system-design gap is not "add more model code." It is
bridging the current detector demo into a more complete verification workflow
with review states, clearer tray summaries, and lightweight logging.

## Prototype Requirements

The most useful requirements for this repository are prototype-demonstration
requirements rather than deployment requirements.

TrayGuard should demonstrate that:

- the detector can recognize and count known classes in controlled tray-like
  scenes well enough to support comparison against a required list
- the capture design can justify when an overhead tray view is enough and when
  a controlled review view would be needed
- the system can fail more safely by surfacing uncertainty, not only by raising
  average accuracy
- the interface can communicate present, missing, extra, and review-needed
  states clearly enough for human confirmation
- the interface can give visual-first, optional audio feedback without creating
  unnecessary alert burden
- the evaluation pipeline can expose the main CV risks: lighting,
  shape-similarity confusion, clutter and occlusion, and open-set behavior
- the workflow can be discussed as a realistic technician-assistance concept
  rather than only as a model benchmark
- the system can produce lightweight records that support traceability and
  repeated-error analysis

These requirements are intentionally narrower than field-readiness claims. They
fit the actual state of the codebase and the quarter plan better than strict
deployment-style targets such as full-shift uptime, hospital-grade false-alert
limits, or comprehensive SPD integration.

## Engineering Goals And Evidence Status

The original P6 draft listed several hard numbers. Some can be defended as
controlled-prototype targets; others should be treated as aspirational until we
collect local workflow evidence. The table below separates those cases so the
requirements stay honest.

| Goal Area | Engineering Goal | Evidence Status | How To Evaluate In This Project |
| --- | --- | --- | --- |
| Known-class detection | Report precision, recall, mAP50, and mAP50-95 for each controlled experiment. Use `>=90%` per-class precision and recall as a minimum controlled-prototype target for known classes. | Partly supported. Deol et al. reported 94.0-100% class precision and 97.1-100% class recall across 11 surgical-tool categories, with overlapping-tool precision falling as low as 89.6% for one class and recall staying 97.2-98.2%. Atabuzzaman et al. reported real-time CSSD classification exceeding 99.5%, but in a structured single-instrument multi-view station rather than full-tray checking ([Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025)). | Use held-out test splits for lighting, similar-shape, clutter, and open-set experiments. Report per-class failures instead of relying only on averages. |
| Tray-level counting | Target `>=95%` exact class-count agreement for known classes in controlled tray-like scenes. Treat this as a stretch validation target, not an externally proven SPD requirement. | Partly supported, but not proven for our tray workflow. Deol et al. maintained correct tool count in all non-transition frames during a one-hour simulated surgical video and reported high detection recall, but that is not the same as SPD tray verification across many tray layouts ([Deol et al., 2024](../bibliography.md#deol-et-al-2024)). | For each test tray, compare required count vs observed count by class. Report exact-count rate, under-count rate, over-count rate, and the specific classes responsible. |
| Missing-item detection | Target `>=95%` missing-item recall in controlled scenarios where one required item is absent. | Reasonable as a prototype target, but locally unproven. The operational need is strongly supported because missing instruments are a major delay source; the exact 95% number is a design target borrowed from high recall in related CV studies, not a published SPD deployment threshold ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Deol et al., 2024](../bibliography.md#deol-et-al-2024)). | Construct tray scenarios with known missing items. Count how often the system flags the missing class without requiring the user to infer it from raw boxes. |
| False alerts | Do not claim the P6 target of `<=1 false alert per 8 hours` yet. Use `<=5%` false positive rate or false review rate as an interim offline target, and replace it with a scan-volume-based target after walkthrough data exists. | The need for low false alerts is well supported, but the exact one-per-shift number is not. Alert-fatigue and workflow literature supports measuring false alerts because interruptions reduce usability and acceptance, but it does not justify this specific rate for SPD tray verification ([Olakotan and Yusof, 2021](../bibliography.md#olakotan-and-yusof-2021), [Cánovas-Segura et al., 2023](../bibliography.md#canovas-segura-et-al-2023)). | Track false extra-item alerts, false missing-item alerts, and unnecessary review prompts per tray scenario. In user walkthroughs, record rescans, hesitations, complaints, and whether users say alerts are tolerable. |
| Latency | Produce tray status within `<5 seconds` from image capture for the prototype UI. Also report model inference latency separately from full UI latency. | Supported as a conservative prototype target. Deol et al. reported median inference of 24.7 ms, or 40.4 FPS, on a V100 for surgical-tool video; TrayGuard's full UI can be much slower than model inference and still meet a five-second tray-check goal ([Deol et al., 2024](../bibliography.md#deol-et-al-2024)). | Log model inference time, count-aggregation time, and end-to-end UI update time. Treat network calls or manual file movement as outside the runtime target. |
| User interaction | Verification should require only a small number of deliberate actions: select or enter tray list, capture or confirm scan, review flagged issues, and finalize. The P6 `no more than two user actions` target is too rigid for review-heavy cases. | Workflow-fit evidence supports minimizing extra steps, but no source supports exactly two actions for this context. Human-in-the-loop literature and workflow-acceptance planning support fast correction and clear review over arbitrary click counts ([Chomutare et al., 2022](../bibliography.md#chomutare-et-al-2022), [Kim et al., 2025](../bibliography.md#kim-et-al-2025), [Zheng et al., 2023](../bibliography.md#zheng-et-al-2023)). | In walkthroughs, record action count, time to final decision, correction burden, and points of confusion. |
| Setup and deployment burden | Keep setup lightweight: commodity camera or phone camera, fixed background, controlled lighting, local compute, and no instrument modification. Do not claim the P6 `usable within 10 minutes` setup target until it is timed. | Directionally supported. CV is attractive because it avoids instrument-level tagging; RFID and barcode alternatives require additional instrument and reader infrastructure ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). The exact 10-minute setup number is currently an assumption. | Time a clean setup from packed state to first successful tray scan. Record required hardware, calibration steps, and failure points. |
| Workspace coverage | Use a fixed, documented tray workspace for prototype tests. Do not claim the P6 `0.5 m x 0.5 m` coverage target unless the physical capture setup is measured and photographed. | Not independently supported yet. The number is plausible for a tabletop prototype, but it is not tied to a cited SPD tray standard in the current evidence base. | Measure the actual camera field of view at the chosen mount height. Report usable area, pixel resolution, and whether all test objects remain detectable at the edges. |
| Privacy | Do not collect or transmit patient information. Keep prototype images focused on instruments and tray surfaces. | Strongly justified by scope: the system is intended for tray readiness, not patient data. It also keeps the prototype simpler and lower risk. | Verify that saved records contain scan IDs, timestamps, tray definitions, detections, and screenshots only; no patient identifiers. |
| Traceability | Save scan ID, timestamp, required list, observed counts, confidence values, review flags, user corrections, and screenshot or frame reference. | Supported by the quality-reporting argument: incomplete and delayed reporting makes instrument-error improvement harder, and traceability literature frames tracking as important for safety, cost, logistics, and risk analysis ([Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023), [Fayad et al., 2025](../bibliography.md#fayad-et-al-2025)). | Implement the minimum tray-check record schema and generate an example quality report from prototype data. |

## Deployment-Style Threshold Ranges

There is no published universal confidence cutoff that makes a tray-checking
assistant safe for a high-stakes environment. A deployment threshold would need
to be justified by the intended use, tray classes, user workflow, camera setup,
local validation data, and risk controls. FDA and international MLMD guidance
points in that direction: use representative data, test under clinically or
operationally relevant conditions, focus on the human-AI team, communicate
limits, and monitor performance across the product lifecycle
([FDA GMLP, accessed 2026](../bibliography.md#fda-gmlp-accessed-2026),
[FDA Transparency, accessed 2026](../bibliography.md#fda-transparency-accessed-2026)).

The ranges below are not current TrayGuard claims. They are rough deployment
screening targets for a future high-stakes guided-verification system before it
would be reasonable to run outside a shadow-mode or supervised pilot.

Raw confidence cutoffs should not be copied between models. If the prototype
needs placeholder UI values before a validation sweep, a conservative starting
band would be something like `T_review = 0.15-0.30` and
`T_present = 0.75-0.90`, but those numbers would be demo assumptions only. A
deployable cutoff is the value that achieves the validation targets below for a
specific model, class list, camera setup, and use environment.

| Area | Rough Pre-Deployment Target | Rationale |
| --- | --- | --- |
| False complete tray decisions | `<=0.1%` per tray scenario, and ideally zero false complete decisions in the final validation set with confidence intervals reported. | A false complete result hides missing, wrong, extra, or uncertain items and is the highest-risk UI failure. |
| Required-item recall at `T_review` | `>=99.5%` for critical required classes under intended scan conditions. | A present item should almost always appear at least as reviewable evidence instead of disappearing into `Missing`. |
| Required-item precision at `T_present` | `>=99%` per class, with no unresolved high-confidence wrong similar-class pattern. | Quiet `Present` labels should be reserved for detections that are very likely to be correct. |
| Missing-item recall | `>=99%` for planted missing-item scenarios. | The system should reliably flag truly absent required items. |
| False missing rate | `<=0.5%` for visible required items under acceptable scan quality. | A visible tool should not be incorrectly treated as absent when the image is usable. |
| Unknown or wrong-similar high-confidence false positives | `<=0.1-0.5%`, with `>=95-99%` of plausible unknowns routed to review or extra-item handling. | Unknown or wrong-but-similar objects should not quietly satisfy required classes. |
| Review rate in normal use | Usually `<=5-10%` of routine trays, with higher rates acceptable for known hard trays if users find the review worthwhile. | Review is safer than false approval, but too much review becomes workflow burden and alert fatigue. |
| Unnecessary rescan rate | Usually `<=5%` under intended lighting and staging conditions. | Frequent rescans signal that image-quality controls or camera setup are not deployment-ready. |
| Calibration | Reliability plots by class and operating region; target calibration error around `<=0.05` for accepted detections, or justify why a different metric is used. | Confidence should be monitored as an operating signal, especially near `T_review` and `T_present`. |
| Human-AI workflow | Users catch at least as many planted issues as manual baseline with acceptable time, correction, and trust-calibration results. | Deployment readiness is about the whole verification workflow, not the model alone. |
| Monitoring and fallback | Defined manual fallback, downtime process, drift monitoring, and threshold-change control. | A high-stakes system needs performance monitoring and a safe path when the model or capture setup is outside validated conditions. |

For this capstone prototype, the defensible target remains narrower: report the
curves and failure cases that would let a future team choose those thresholds.
The prototype should not claim clinical or SPD deployment readiness until those
deployment-style targets are tested with real instruments, representative users,
site-specific trays, and local operating conditions.

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
