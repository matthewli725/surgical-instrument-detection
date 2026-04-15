# Shape Similarity Experiment Plan

## Objective

Evaluate whether the object detection model can distinguish between objects with similar shapes, outlines, and proportions. This experiment targets one of TrayGuard's central challenges: many surgical instruments look nearly identical to inexperienced users, especially when viewed from a top-down camera.

## Core Question

> Can the model reliably differentiate between visually similar tools, or does it confuse objects that share the same general shape?

## Experimental Design Overview

We will run a controlled shape-differentiation experiment where lighting, background, and camera position are kept as stable as possible while object identity changes.

### Key Principle

Only one factor should be emphasized:

- Within a setup: keep lighting, background, camera, and tray position fixed
- Across classes: choose objects that are intentionally similar in silhouette

This isolates whether the model is learning fine-grained shape cues rather than relying on easy differences such as color, size, or background.

## Dataset Structure

### Preferred Classes

Use real or proxy objects with similar outlines:

- Straight Mayo Scissor
- Curved Mayo Scissor
- Straight Dissection Clamp
- Scalpel n4

If real surgical instruments are unavailable, use accessible substitutes:

- Similar scissors with different tip shapes
- Similar pliers or clamps
- Similar pens, tweezers, or craft tools
- Utensils with similar long narrow silhouettes

## Shape Variables To Test

Focus on differences that resemble surgical instrument recognition:

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

Example:

- Train: most object poses and rotations
- Validation: held-out poses
- Test: unseen rotations or a second physical instance of a similar object

The strongest version uses a held-out object instance, such as a second pair of similar scissors, to test whether the model learns the category rather than memorizing one object.

## Experiment Steps

### 0:00-0:30 Setup

- Select object classes.
- Confirm the classes are visually similar enough to be challenging.
- Fix lighting, camera, and background.

### 0:30-1:30 Data Collection

- Capture balanced images for each class.
- Vary pose and rotation.
- Keep lighting fixed.
- Avoid making one class visually easier because of a unique background or location.

### 1:30-2:15 Labeling

- Label all visible objects.
- Check that class names are consistent.
- Review examples of the most similar pairs before training.

### 2:15-3:15 Training

- Train one detector on the full shape dataset.
- If time allows, train a second version with fewer examples to test data sensitivity.

### 3:15-4:00 Evaluation

- Evaluate per-class precision and recall.
- Review confusion matrix or class-level mistakes.
- Save example images where the model confuses similar tools.

## Evaluation Metrics

Track:

- Per-class precision
- Per-class recall
- mAP, if available
- Confusion between similar class pairs
- False positives between same-shape classes
- Detection confidence for correct vs incorrect predictions

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

## What Not To Do

- Do not use classes that are too visually different.
- Do not let background or object location reveal the class.
- Do not collect many near-identical frames from one pose.
- Do not report only aggregate mAP if one class pair is failing badly.

## Optional Extension

Use a held-out physical object instance:

- Train on one object instance per class.
- Test on a different instance with similar shape.

This better approximates the real surgical setting, where the system may see instruments of the same type with slight manufacturing or wear differences.

## Key Takeaways Expected

At the end, we should be able to answer:

1. Can the model distinguish similar object shapes?
2. Which shape pairs are most commonly confused?
3. Does pose variation improve shape recognition?
4. Is the model learning object identity or memorizing one visual instance?

## Guiding Principle

> Similar-looking classes are the point of the experiment.

Make the task challenging enough that success means something.
