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

## Main Components

The current product concept can be understood as five components:

1. **Sensing**
   - Camera, scene framing, and practical lighting conditions.
   - The main risk here is image quality degradation from glare, shadow,
     reflectivity, blur, and camera placement.
2. **Perception**
   - Detection model, confidence scores, and class-level predictions.
   - The main risk here is confusion between similar tools, missed detections,
     and unsafe high-confidence errors.
3. **Comparison And Decision Support**
   - Required-list parsing, observed-count aggregation, and tray-status logic.
   - This is where the system turns raw detections into missing, extra, and
     review-needed information.
4. **Technician Interface**
   - Live image view, checklist, review prompts, and future correction flow.
   - The UI should help the user finish the check quickly, not just display
     boxes on an image.
5. **Traceability And Reporting**
   - Saved results, confidence values, screenshots or frame references, and
     repeat-pattern reporting.
   - This is necessary for a buyer-facing quality story, not just demo output.

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
- the system can fail more safely by surfacing uncertainty, not only by raising
  average accuracy
- the interface can communicate present, missing, extra, and review-needed
  states clearly enough for human confirmation
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

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
