# TrayGuard Project Background

## Automated Surgical Tray Inspection Using Computer Vision

TrayGuard is a computer vision prototype for helping surgical sterilization technicians identify and count instruments in a surgical tray. The long-term goal is a camera-connected system that detects each instrument, counts what has already been collected, and clearly shows the user which required tools are still missing.

This project addresses a real workflow problem: surgical instruments can look very similar, technicians need significant experience to identify them reliably, and manual tray assembly is vulnerable to fatigue, distraction, and counting errors. TrayGuard is meant to reduce that burden by turning the tray check into a guided visual verification task.

## Current Focus

Because we do not have access to a full set of real surgical instruments, and because collecting a broad surgical dataset is outside the scope of this prototype timeline, we are building evidence along several controlled experiment axes. Instead of claiming full deployment readiness, we are testing whether the core computer vision assumptions hold under conditions that resemble the hard parts of surgical tray inspection.

The current system supports:

- Camera-based image collection
- Manual bounding-box annotation
- Reusing labels across controlled lighting variants
- Exporting collected images to YOLO format
- Training and benchmarking object detection models
- Running a Streamlit tray-check UI for live camera detections

## Proposed Experiments

Detailed experiment plans live in `docs/experiments/`:

- `docs/experiments/shape_similarity.md`
- `docs/experiments/reflectivity_lighting.md`
- `docs/experiments/clutter_occlusion.md`

### 1. Shape Similarity

**Question:** Can the model distinguish between objects that have similar outlines but different identities?

This tests the most important recognition challenge in surgical tray assembly. Many surgical instruments share common visual structure: handles, hinges, clamps, blades, and long narrow bodies. The system needs to learn subtle differences in shape, tip geometry, handle structure, and relative proportions.

**Proposed setup:**

- Collect images of visually similar tools.
- Keep lighting and background mostly stable.
- Train the detector on multiple shape classes.
- Evaluate whether the model confuses similarly shaped objects.

**Success indicators:**

- High per-class precision and recall for visually similar classes
- Low confusion between paired classes, such as straight vs. curved instruments
- Reasonable detection confidence when objects are rotated or slightly repositioned

### 2. Material and Lighting Robustness

**Question:** Can the model remain reliable when reflective or metallic objects appear under different lighting conditions?

Surgical instruments are commonly metallic, which makes computer vision harder. Reflections, glare, shadows, and exposure changes can make the same object look different between images. Our data collection workflow is designed around this issue: one setup can be annotated once, then captured repeatedly under different lighting conditions.

**Proposed setup:**

- Place a fixed set of objects in a tray or tray-like area.
- Capture one annotated reference image.
- Capture lighting variants with changed light angle, brightness, glare, and shadow.
- Train and evaluate on lighting conditions not seen during training.

**Success indicators:**

- Stable detections across lighting variants
- Limited confidence drop under glare or shadow
- Better performance when lighting augmentation or multi-lighting training data is used

### 3. Clutter and Occlusion

**Question:** Can the model detect and count instruments when objects are close together, overlapping, or partially occluded?

Real trays are not always perfectly organized. Instruments may touch, overlap, or partially hide one another. A useful tray inspection system must still count visible tools and avoid double-counting.

**Proposed setup:**

- Create tray scenes with increasing clutter levels.
- Start with separated objects, then move to touching objects, partial overlap, and heavier occlusion.
- Evaluate detection quality at each clutter level.

**Success indicators:**

- Accurate counts in low and moderate clutter
- Graceful degradation as occlusion increases
- Clear failure cases where the system can flag low confidence instead of silently miscounting

## System Concept

TrayGuard is intended to become an interactive tray-checking system:

1. A technician loads the required instrument list for a tray by scanning a barcode.
2. A camera captures the current tray state.
3. The detector identifies and counts visible instruments.
4. The interface shows collected tools, missing tools, and uncertain detections.
5. The technician confirms or corrects the result before the tray is completed.

The current repository focuses on the computer vision foundation: data collection, labeling, dataset export, model training, and model evaluation.

## Evaluation Plan

For each experiment axis, we plan to report:

- Dataset size and class list
- Train, validation, and test split strategy
- Mean average precision or other detector metrics
- Per-class precision and recall
- Confusion between similar classes
- Example successes and failures
- Qualitative screenshots of detections

The strongest final result would not be a claim that TrayGuard is ready for operating-room deployment. Instead, it would show that the main risks are testable, that the prototype works under controlled approximations of those risks, and that the same pipeline could scale to real surgical instruments once real data is available.
