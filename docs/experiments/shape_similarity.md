# Shape Similarity Experiment Plan

## Objective

Evaluate whether the object detection model can distinguish between objects with similar shapes, outlines, and proportions. This experiment targets a documented sterile-processing risk. Wrong-specification instruments were the largest packaging-error category in Zhu et al.'s study. Identification and sorting failures are also part of the visualization-related error burden described by Nichol and Saari and Nichol et al. (Zhu et al., 2019, Nichol and Saari, 2023, Nichol et al., 2024).

This is also a customer-trust experiment. A hospital buyer will worry less about obvious objects. They will care more about near-neighbor specifications. Straight vs curved instruments are a good example. A wrong instrument can create both an extra item and a missing item in the same tray (Nichol et al., 2024, Zhu et al., 2019).

## Core Question

> Can the model reliably differentiate between visually similar tools, or does it confuse objects that share the same general shape?

## Experimental Design Overview

We will run a controlled shape-differentiation experiment where lighting, background, and camera position are kept as stable as possible while object identity changes.

### Key Principle

Only one factor should be emphasized.

- Within a setup, keep lighting, background, camera, and tray position fixed
- Across classes, choose objects that are intentionally similar in silhouette

This isolates whether the model is learning fine-grained shape cues rather than relying on easy differences such as color, size, or background.

## Dataset Structure

### Preferred Classes

Use real or proxy objects with similar outlines.

- Straight Mayo Scissor
- Curved Mayo Scissor
- Straight Dissection Clamp
- Scalpel n4

If real surgical instruments are unavailable, use accessible substitutes.

- Similar scissors with different tip shapes
- Similar pliers or clamps
- Similar pens, tweezers, or craft tools
- Utensils with similar long narrow silhouettes

## Shape Variables To Test

Focus on differences that resemble surgical instrument recognition.

1. Straight vs curved tips
2. Different handle shapes
3. Different jaw or blade shapes
4. Slight length or width differences
5. Similar hinge or grip structures

## Data Collection Plan

### Fixed Setup

- Fixed camera position
- Fixed lighting
- Fixed background
- Tray-like layout
- Similar scale across objects
- Similar object orientation distribution across classes

### Capture Targets

- About 30-50 images per class
- About 120-200 images total for a four-class test

If time is tight, prioritize balanced class counts over total volume.

## Procedure

1. Select visually similar object classes.
2. Place one or more objects in a tray-like layout.
3. Capture images with varied rotations and positions.
4. Keep lighting and background stable.
5. Annotate bounding boxes and class labels.
6. Train one detector on the collected shape classes.
7. Evaluate confusion between similar classes.

## Train / Val / Test Split

Split by setup or object instance where possible, not by random near-duplicate frames.

Example split

- Train on most object poses and rotations
- Validate on held-out poses
- Test on unseen rotations or a second physical instance of a similar object

The strongest version uses a held-out object instance, such as a second pair of similar scissors, to test whether the model learns the category rather than memorizing one object.

## Experiment Steps

### First 30 Minutes Setup

- Select object classes.
- Confirm the classes are visually similar enough to be challenging.
- Fix lighting, camera, and background.

### Next 60 Minutes Data Collection

- Capture balanced images for each class.
- Vary pose and rotation.
- Keep lighting fixed.
- Avoid making one class visually easier because of a unique background or location.

### Next 45 Minutes Labeling

- Label all visible objects.
- Check that class names are consistent.
- Review examples of the most similar pairs before training.

### Next 60 Minutes Training

- Train one detector on the full shape dataset.
- If time allows, train a second version with fewer examples to test data sensitivity.

### Final 45 Minutes Evaluation

- Evaluate per-class precision and recall.
- Review confusion matrix or class-level mistakes.
- Save example images where the model confuses similar tools.

## Evaluation Metrics

Track these metrics.

- Per-class precision
- Per-class recall
- mAP, if available
- Confusion between similar class pairs
- False positives between same-shape classes
- Detection confidence for correct vs incorrect predictions
- High-confidence wrong-class predictions
- Cases where a family-level label would be safer than a specific label

## Required Analysis

### Per-Class Performance

| Class | Precision | Recall | mAP | Notes |
| --- | --- | --- | --- | --- |
| Class 1 | | | | |
| Class 2 | | | | |
| Class 3 | | | | |
| Class 4 | | | | |

### Similar-Pair Confusion

| Pair | Common Mistake | Frequency | Notes |
| --- | --- | --- | --- |
| Straight vs curved instrument | | | |
| Clamp vs scissor | | | |
| Long narrow tool vs long narrow tool | | | |

### Customer-Risk Interpretation

| Result Pattern | What It Means For Adoption | Response |
| --- | --- | --- |
| Low aggregate mAP | Model is not ready even for controlled use | Collect more balanced data or simplify classes |
| Good mAP but one bad pair | The system may fail on exactly the cases technicians care about | Add targeted examples and UI review for that pair |
| High-confidence wrong class | Dangerous because the UI may falsely reassure the user | Add confidence calibration or needs-review state |
| Low confidence on similar pair | Safer failure if the UI asks for review | Make review workflow fast and clear |

### Pose Robustness

| Pose Type | Performance | Notes |
| --- | --- | --- |
| Horizontal | | |
| Vertical | | |
| Diagonal | | |
| Partially rotated | | |

## What Counts as Success

- The model separates similar classes better than chance.
- The worst confusions are explainable and visually plausible.
- Per-class recall remains acceptable across different rotations.
- Similar-shape mistakes decrease when more class-balanced data is added.
- High-confidence wrong-specification predictions are rare enough to be caught by a review threshold.

## What Not To Do

- Do not use classes that are too visually different.
- Do not let background or object location reveal the class.
- Do not collect many near-identical frames from one pose.
- Do not report only aggregate mAP if one class pair is failing badly.

## Optional Extension

Use a held-out physical object instance.

- Train on one object instance per class.
- Test on a different instance with similar shape.

This better approximates the real surgical setting, where the system may see instruments of the same type with slight manufacturing or wear differences.

## Key Takeaways Expected

At the end, we should be able to answer these questions.

1. Can the model distinguish similar object shapes?
2. Which shape pairs are most commonly confused?
3. Does pose variation improve shape recognition?
4. Is the model learning object identity or memorizing one visual instance?
5. Which class pairs would need human confirmation before a hospital pilot?

## Guiding Principle

> Similar-looking classes are the point of the experiment.

Make the task challenging enough that success means something.

## References

- Nichol and Saari, ["Patterns in staff reported surgical instrument errors point to failures in visualization as a critically weak point in sterile processing of surgical instruments"](https://doi.org/10.1016/j.pcorm.2023.100356), Perioperative Care and Operating Room Management, 2023.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
- Zhu et al., ["Errors in packaging surgical instruments based on a surgical instrument tracking system: an observational study"](https://link.springer.com/article/10.1186/s12913-019-4007-3), BMC Health Services Research, 2019.
