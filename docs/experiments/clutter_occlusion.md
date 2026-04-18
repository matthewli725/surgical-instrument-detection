# Clutter And Occlusion

TrayGuard needs to handle trays where tools are close together, touching, or
partly hidden. This page explains what this test is meant to show and how to
use the results.

## What This Test Answers

The system should not assume every tray is neatly arranged. In real workflows,
objects may overlap or sit close together.

## Why This Is A Risk

Occlusion removes visual information. In object detection research, cluttered
and occluded scenes are repeatedly identified as challenging because important
features are hidden, which can create missed detections or merged objects. A
survey of challenging detection environments treats occlusion, illumination, and
scale as major stressors for deep object detectors
([Ahmed et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8348086/)).
Another occlusion-focused survey notes that detection accuracy decreases when
objects are deformed or occluded
([Ning et al., 2021](https://link.springer.com/article/10.1007/s40747-020-00206-8)).

This is a tray-checking risk because missing, extra, and wrong instruments are
documented surgical-instrument error categories
([Nichol et al., 2024](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-024-02407-1/tables/2)).
If instruments overlap, TrayGuard may undercount visible tools or produce a
confident count from a bad view.

This test answers:

- How much clutter can TrayGuard handle?
- When do counts become unreliable?
- When should the product ask the user to spread tools out and scan again?

## Clutter Levels

| Level | Meaning | Expected Product Behavior |
| --- | --- | --- |
| Level 0 | Objects are separated | Detect and count normally |
| Level 1 | Objects are close but distinct | Detect and count normally |
| Level 2 | Objects touch or slightly overlap | Detect with some caution |
| Level 3 | Objects partly cover each other | Flag uncertainty when needed |
| Level 4 | Objects are heavily hidden | Ask the user to spread tools out |

The goal is not to make TrayGuard guess hidden objects. The goal is to know when
the camera view is good enough for a reliable tray check.

## How To Read The Results

Use detection metrics and count-level outcomes together.

- Precision: how often detections are correct.
- Recall: how often visible tools are found.
- Count error: how far the predicted count is from the visible true count.
- Review or rescan rate: how often the system asks for a better view.

Count error is especially important because a tray-checking tool must help users
decide whether the tray is complete.

## Product Interpretation

| Result Pattern | What It Means | Product Response |
| --- | --- | --- |
| Works only when objects are fully separated | The workflow may require too much tray staging | Position TrayGuard as final verification, not bulk sorting |
| Moderate clutter works reliably | The product can support realistic tray checks | Keep the scan flow simple |
| Heavy clutter causes confident wrong counts | The product should not auto-confirm crowded scenes | Add a hard stop or rescan request |
| Heavy clutter lowers confidence | This is a safer failure mode | Explain what the user should fix |

## User-Facing Guidance

If TrayGuard cannot confidently count the tray:

- Spread overlapping tools apart.
- Move reflective tools so their edges are visible.
- Keep the camera view clear.
- Scan again before confirming the tray.

## What We Are Not Claiming

- TrayGuard should not count tools that are completely hidden.
- A good score on separated objects does not prove cluttered-tray readiness.
- A fast result is not useful if the count is wrong.

## References

- Ahmed et al., ["Survey and Performance Analysis of Deep Learning Based Object Detection in Challenging Environments"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8348086/), Sensors, 2021.
- Eussen et al., ["Surgical tray optimization: a prospective and survey-based evaluation of environmental and economic outcomes"](https://doi.org/10.1007/s00464-025-12499-2), Surgical Endoscopy, 2026.
- Hill et al., ["Measuring intraoperative surgical instrument use with radio-frequency identification"](https://doi.org/10.1093/jamiaopen/ooac003), JAMIA Open, 2022.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Ning et al., ["Survey of pedestrian detection with occlusion"](https://link.springer.com/article/10.1007/s40747-020-00206-8), Complex & Intelligent Systems, 2021.
- Rubak et al., ["Surgical instrument tray optimization process at a university hospital: A comprehensive overview"](https://doi.org/10.1016/j.sopen.2024.09.007), Surgery Open Science, 2024.
