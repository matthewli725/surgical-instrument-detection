# Reflectivity & Lighting Experiment Plan

## Objective

Evaluate how reflective materials, such as metal utensils, affect object detection performance under varying lighting conditions, and determine whether:

1. Increasing training data diversity improves robustness
2. Preprocessing, such as reflection or glare reduction, provides measurable benefit

This experiment supports the broader TrayGuard goal of ensuring reliable detection of metallic surgical instruments under realistic lighting conditions.

## Core Question

> How much do lighting and reflections degrade detection performance, and what is the most effective way to mitigate this: data diversity or preprocessing?

## Experimental Design Overview

We will run a controlled lighting experiment with minimal confounding variables.

### Key Principle

Only one factor changes at a time within a setup:

- Within a setup: vary lighting only
- Across setups: allow small variations such as background, tray pose, or object placement

This keeps the experiment focused on image-space effects of specular reflection, including saturated highlights, glare shape, contrast distortion, and shadow changes. We are not attempting to physically model reflectance or estimate material properties.

## Dataset Structure

### Classes

Keep the class list small so errors are easy to interpret:

- Spoon
- Fork
- Knife
- Tongs, optional

These kitchen objects are accessible proxy objects for metallic surgical instruments. They are not perfect substitutes, but they reproduce the reflective surface problem that can degrade detector performance.

## Lighting Conditions

Define simple, repeatable categories:

1. Diffuse overhead light
2. Left-side angled light, roughly 30-45 degrees
3. Right-side angled light, roughly 30-45 degrees
4. Low-angle harsh light with strong glare

Exact angle measurement is not required. Consistency and documentation matter more than precision.

## Data Collection Plan

### Fixed Setup

- Fixed object placement
- Fixed camera position, taped down if possible
- Fixed background
- Same framing
- Same object identities across all lighting conditions

### Capture Targets

- About 30 images per lighting condition
- About 120 images total

### Procedure

1. Arrange objects in a tray-like layout.
2. Capture one reference image.
3. Annotate bounding boxes.
4. Lock the setup.
5. Change lighting condition.
6. Capture multiple images per condition using the same labels.

Avoid near-duplicate spam. Small natural variations are useful, but repeated identical frames make the dataset look larger without adding much information.

## Train / Val / Test Split

Split by lighting condition, not randomly.

Example:

- Train: diffuse overhead light and left-side angled light
- Validation: right-side angled light
- Test: low-angle harsh glare

This tests generalization to unseen lighting. Random splitting would leak nearly identical object setups across train and test, making the results look better than they really are.

## Experiment Steps

### 0:00-0:30 Setup

- Define lighting conditions.
- Fix camera and tray position.
- Prepare objects.
- Confirm that glare is visible in at least one harsh-light condition.

### 0:30-1:45 Data Collection

- Capture all lighting conditions.
- Keep framing consistent.
- Record the lighting condition for each image.
- Avoid changing object placement within the setup.

### 1:45-2:30 Labeling

If time is tight, label a balanced subset first:

- About 80 train images
- About 20 validation images
- About 20 test images

### 2:30-3:30 Training

Train one detector under three training data sizes:

- 25% of training set
- 50% of training set
- 100% of training set

Keep validation and test fixed.

### 3:30-4:00 Optional Ablation

Try preprocessing only if it is quick to set up:

- Run glare or reflection reduction.
- Apply it to validation and test first.
- Compare raw images against preprocessed images.

If preprocessing setup takes too long, skip it. A clean data-diversity result is more valuable than an unfinished preprocessing experiment.

## Evaluation Metrics

Track:

- Precision
- Recall
- mAP, if available
- Detection confidence
- Number of detections per image
- False negatives, especially on reflective surfaces
- False positives caused by glare or reflected edges

## Specularity Measurements

To connect performance degradation to reflectivity, compute simple image-based metrics inside each object bounding box:

- Percentage of saturated pixels
- Bright highlight area fraction above a chosen threshold
- Top percentile brightness, such as 95th or 99th percentile
- Mean and standard deviation of pixel intensity

Then compare model performance against these specularity measurements. The goal is to answer whether failures correlate with visible glare, saturation, or contrast distortion.

## Required Analysis

### By Lighting Condition

| Condition | Precision | Recall | mAP | Notes |
| --- | --- | --- | --- | --- |
| Seen lighting | | | | |
| Unseen lighting | | | | |
| Harsh glare | | | | |

### By Training Size

| Train Size | Precision | Recall | mAP | Notes |
| --- | --- | --- | --- | --- |
| 25% | | | | |
| 50% | | | | |
| 100% | | | | |

### With vs Without Preprocessing

| Setup | Precision | Recall | mAP | Notes |
| --- | --- | --- | --- | --- |
| Raw images | | | | |
| Preprocessed images | | | | |

### Performance vs Specularity

| Specularity Level | Example Definition | Performance Notes |
| --- | --- | --- |
| Low | Few saturated pixels | |
| Medium | Visible highlights but object shape remains clear | |
| High | Strong glare or saturated regions obscure object shape | |

## What Counts as Success

- Stable performance on unseen lighting
- Improvement with increased lighting diversity
- Clear evidence whether preprocessing helps enough to justify the added complexity
- Documented failure cases when glare causes uncertainty or missed detections

## What Not To Do

- Do not randomly split images.
- Do not change multiple variables at once within a setup.
- Do not spend excessive time on preprocessing tools.
- Do not aim for perfect surgical realism yet.
- Do not claim silverware fully replaces surgical instrument testing.

## Optional Extension

Collect a second setup:

- Slightly different background, or
- Slight rotation of tray, or
- Different arrangement of the same objects

Use this as a robustness test set.

## Key Takeaways Expected

At the end, we should be able to answer:

1. Does lighting significantly affect detection?
2. Does more diverse training data fix it?
3. Is preprocessing worth the added complexity?
4. Do failures correlate with measurable glare or saturation?

## Guiding Principle

> Clean experimental design is more valuable than more data.

Focus on controlled variation, not volume.



| Dataset              | Class  | Images | Instances | Precision (P) | Recall (R) | mAP50 | mAP50-95 |
|----------------------|--------|--------|-----------|---------------|------------|-------|----------|
| reference            | spoon1 | 97     | 97        | 0.890         | 0.938      | 0.967 | 0.840    |
| reference            | spoon2 | 97     | 97        | 1.000         | 0.944      | 0.991 | 0.863    |
| reference            | spoon3 | 97     | 97        | 0.950         | 0.982      | 0.993 | 0.804    |
| reference_plus_45    | spoon1 | 73     | 73        | 0.983         | 0.986      | 0.994 | 0.917    |
| reference_plus_45    | spoon2 | 73     | 73        | 1.000         | 0.983      | 0.994 | 0.965    |
| reference_plus_45    | spoon3 | 73     | 73        | 0.996         | 1.000      | 0.995 | 0.953    |
| reference_plus_45_90 | spoon1 | 49     | 49        | 0.999         | 1.000      | 0.995 | 0.902    |
| reference_plus_45_90 | spoon2 | 49     | 49        | 0.999         | 1.000      | 0.995 | 0.972    |
| reference_plus_45_90 | spoon3 | 49     | 49        | 0.999         | 1.000      | 0.995 | 0.980    |