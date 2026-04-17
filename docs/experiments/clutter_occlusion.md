# Clutter & Occlusion Experiment Plan

## Objective

Evaluate whether the object detection model can detect and count tools when objects are close together, touching, overlapping, or partially hidden. This experiment supports reliable tray inspection in realistic layouts. Instrument oversupply, large trays, and tray-design complexity all increase the visual burden in OR and SPD workflows (Hill et al., 2022, Rubak et al., 2024, Eussen et al., 2026).

This is one of the clearest workflow risks. A technician may not want to stage every instrument carefully for the camera. A pile or hopper-style workflow may create occlusion that makes vision unreliable. Sterile-processing improvement research shows that workflow design and physical environment are defect drivers (Natarus et al., 2025). The experiment should measure the cost of asking users to spread, separate, or rescan instruments.

## Core Question

> How much clutter or occlusion can the model tolerate before detection and counting performance breaks down?

## Experimental Design Overview

We will run a controlled clutter experiment with increasing scene difficulty. The object set, camera, background, and lighting should remain stable while the amount of clutter and overlap changes.

### Key Principle

Change clutter level systematically.

- Level 0 means separated objects
- Level 1 means close but not touching
- Level 2 means touching or slightly overlapping
- Level 3 means moderate overlap
- Level 4 means heavy occlusion

This allows us to measure graceful degradation instead of simply asking whether the model works in one messy scene.

## Dataset Structure

### Classes

Use the same classes as the main prototype where possible.

- Scalpel n4
- Straight Dissection Clamp
- Straight Mayo Scissor
- Curved Mayo Scissor

If surgical instruments are unavailable, use proxy objects.

- Spoon
- Fork
- Knife
- Tongs
- Scissors
- Pens or craft tools with elongated shapes

## Clutter Levels

### Level 0 Separated

- Objects are clearly separated.
- No touching or overlap.
- This gives a baseline for ideal detection and counting.

### Level 1 Close

- Objects are close together but still visually distinct.
- Bounding boxes may be near each other but should not overlap much.

### Level 2 Touching / Slight Overlap

- Objects touch or overlap at small regions.
- Most of each object remains visible.

### Level 3 Moderate Occlusion

- One object partly covers another.
- Important features such as handles, tips, or blades may be partially hidden.

### Level 4 Heavy Occlusion

- Objects are significantly hidden.
- Detection may become ambiguous.
- The system should ideally lower confidence or miss uncertain objects rather than hallucinate confident counts.

## Data Collection Plan

### Fixed Setup

- Fixed camera position
- Fixed lighting
- Fixed background
- Same set of objects across clutter levels
- Same tray-like area

### Capture Targets

- About 20-30 images per clutter level
- About 100-150 images total

If time is tight, collect fewer clutter levels but keep them clearly separated, such as separated, touching, moderate overlap, and heavy occlusion.

## Procedure

1. Arrange all objects in a separated layout.
2. Capture images for Level 0.
3. Move objects closer for Level 1.
4. Introduce touching or slight overlap for Level 2.
5. Introduce moderate overlap for Level 3.
6. Introduce heavy occlusion for Level 4.
7. Annotate visible objects consistently.
8. Train or evaluate the detector across clutter levels.

## Annotation Rules

Use consistent annotation rules.

- Label every object that is visible enough for a human to identify.
- Draw boxes around the visible extent if full extent is ambiguous.
- Mark heavily occluded cases in notes if the object identity is unclear.
- Do not label objects that are almost entirely hidden unless the project explicitly decides to count hidden known objects.

The goal is camera-visible detection and counting, not guessing from memory that an object must be present.

## Train / Val / Test Split

Use a split that tests clutter generalization.

Example split

- Train on Level 0, Level 1, and Level 2
- Validate on Level 3
- Test on Level 4

Alternative split

- Train on all clutter levels from one setup.
- Test on a second setup with different object arrangement.

The first split tests whether the model handles worse clutter than it saw during training. The second tests whether the learned behavior transfers to a new tray arrangement.

## Experiment Steps

### First 30 Minutes Setup

- Choose object classes.
- Fix camera, lighting, and tray position.
- Define clutter levels before collecting images.

### Next 60 Minutes Data Collection

- Capture images for each clutter level.
- Save notes about clutter level for each group.
- Avoid changing lighting while changing clutter.

### Next 45 Minutes Labeling

- Label all visible objects.
- Apply occlusion rules consistently.
- Review heavy-occlusion examples as a team if possible.

### Next 60 Minutes Training

- Train one detector using the selected split.
- Keep validation and test clutter levels fixed.

### Final 45 Minutes Evaluation

- Evaluate performance by clutter level.
- Compare predicted counts against true visible counts.
- Save examples where the detector misses, merges, or double-counts tools.

## Evaluation Metrics

Track these metrics.

- Precision
- Recall
- mAP, if available
- Count error per image
- False negatives caused by occlusion
- False positives caused by overlapping edges
- Duplicate detections on a single object
- Number of scenes where the system should ask the user to spread objects out
- Count accuracy before and after a simple rescan or re-spread instruction

## Required Analysis

### By Clutter Level

| Clutter Level | Precision | Recall | Count Error | Notes |
| --- | --- | --- | --- | --- |
| Level 0 separated | | | | |
| Level 1 close | | | | |
| Level 2 touching / slight overlap | | | | |
| Level 3 moderate occlusion | | | | |
| Level 4 heavy occlusion | | | | |

### Counting Accuracy

| Setup | True Visible Count | Predicted Count | Error | Notes |
| --- | --- | --- | --- | --- |
| Example 1 | | | | |
| Example 2 | | | | |
| Example 3 | | | | |

### Failure Modes

| Failure Mode | Example | Likely Cause | Possible Fix |
| --- | --- | --- | --- |
| Missed hidden object | | Occlusion | More clutter data |
| Merged objects | | Touching edges | Better annotations or segmentation |
| Double-counted object | | Reflections or overlapping boxes | Confidence/NMS tuning |

### Workflow Burden

| Clutter Level | Extra User Action Needed? | Time Cost | Error Reduction After Action | Notes |
| --- | --- | --- | --- | --- |
| Level 0 separated | | | | |
| Level 1 close | | | | |
| Level 2 touching / slight overlap | | | | |
| Level 3 moderate occlusion | | | | |
| Level 4 heavy occlusion | | | | |

### Customer-Risk Interpretation

| Result Pattern | What It Means For Adoption | Response |
| --- | --- | --- |
| Works only with fully separated objects | May add too much tray-staging labor | Position as final verification, not bulk sorting |
| Heavy clutter creates confident wrong counts | Unsafe for hopper-style use | Add hard stop for cluttered scenes |
| Heavy clutter lowers confidence | Safer if the UI requests a spread/rescan | Make the rescan workflow fast |
| Moderate clutter works reliably | Supports practical tray-check usage | Use as pilot operating range |

## What Counts as Success

- Strong baseline performance on separated and close objects
- Acceptable count accuracy in low and moderate clutter
- Predictable degradation as occlusion increases
- Clear identification of the clutter level where the system becomes unreliable
- Low-confidence or missed detections are understandable from the image
- Clear instructions for when users must spread out instruments or rescan

## What Not To Do

- Do not mix lighting changes into clutter changes.
- Do not randomly split near-identical clutter scenes.
- Do not count invisible objects as model failures.
- Do not hide failure cases behind aggregate metrics.
- Do not expect perfect performance under heavy occlusion.

## Optional Extension

Add a second tray arrangement.

- Same object classes
- Different object order
- Different overlap pattern
- Same lighting and background

Use this as a robustness test for generalization to new clutter layouts.

## Key Takeaways Expected

At the end, we should be able to answer these questions.

1. How does clutter affect detection performance?
2. How does clutter affect tool counting accuracy?
3. What level of occlusion causes the system to fail?
4. Does the model fail safely by lowering confidence or fail dangerously by producing confident wrong counts?
5. Would the necessary tray-staging steps feel acceptable in a real SPD workflow?

## Guiding Principle

> Counting is only useful if the system knows when visibility is too poor.

The goal is not perfect detection under impossible occlusion. The goal is to understand and communicate the reliable operating range.

## References

- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Hill et al., ["Measuring intraoperative surgical instrument use with radio-frequency identification"](https://doi.org/10.1093/jamiaopen/ooac003), JAMIA Open, 2022.
- Rubak et al., ["Surgical instrument tray optimization process at a university hospital: A comprehensive overview"](https://doi.org/10.1016/j.sopen.2024.09.007), Surgery Open Science, 2024.
- Eussen et al., ["Surgical tray optimization: a prospective and survey-based evaluation of environmental and economic outcomes"](https://doi.org/10.1007/s00464-025-12499-2), Surgical Endoscopy, 2026.
