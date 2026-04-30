# Unknown Objects And Confidence

TrayGuard should be allowed to say "needs review" when it sees something
outside its trained class list. This page explains why uncertainty matters and
how to interpret confidence results.

## What This Test Answers

A tray-checking assistant should not force every object into the closest known
class. Unknown tools, distractors, damaged objects, or unclear images can all
create unsafe false confidence.

## Why This Is A Risk

TrayGuard may see wrong, damaged, substituted, or partially hidden tools. If an
unknown object is confidently labeled as a known tool, the product could make a
bad tray look complete. The shared evidence for open-set behavior, calibration,
and review states lives in the system design's
[research support audit](../../background/system_design.md#research-support-audit).

This test answers:

- Does TrayGuard recognize when an object is unfamiliar?
- Are wrong predictions low confidence or dangerously high confidence?
- What confidence threshold creates a reasonable review workflow?

## Known And Unknown Objects

Known objects are the classes the model was trained to detect.

Unknown objects are intentionally held out. They should include objects that are
plausible confusions, such as similar scissors, clamps, pliers, tweezers, pens,
craft tools, kitchen utensils, or partially covered versions of known tools.

The useful test is not whether TrayGuard rejects random unrelated objects. The
useful test is whether it avoids confidently mislabeling similar-looking tools.

## How To Read The Results

Track these outcomes:

- Known recall: how often known tools are still found.
- Unknown false positives: how often unknown objects are labeled as known tools.
- High-confidence unknown false positives: the riskiest failure mode.
- Review rate: how often the system asks a person to inspect the result.

There is a tradeoff. A higher threshold may reduce false confirmations, but it
can also send more real tools to review.

The threshold itself should not be defended as a universal constant. Confidence
is an operating signal that must be tuned against known-class recall, unknown
false positives, high-confidence errors, and review burden on local validation
data.

## Product Interpretation

| Result Pattern | What It Means | Product Response |
| --- | --- | --- |
| Unknown objects are often sent to review | The system is behaving cautiously | Use clear "needs review" language |
| Unknown objects are confidently labeled as known tools | The system may falsely confirm a wrong tray | Add more training data, thresholds, or an unknown-object workflow |
| Known tools are reviewed too often | The workflow may feel slow | Improve data coverage and tune the threshold |
| Low-confidence errors are visible to users | The system can fail safely | Make correction and confirmation easy |

## User-Facing Guidance

When TrayGuard marks an item for review, the user should check whether it is:

- A wrong or unexpected tool.
- A known tool seen from an unusual angle.
- A partially hidden tool.
- A reflection, shadow, or glare artifact.
- An object that should be removed from the tray area.

## What We Are Not Claiming

- Confidence is not the same thing as clinical safety.
- A model trained on a few classes cannot identify every surgical instrument.
- A review flag is a support tool, not a substitute for technician judgment.

## Bibliography

See the [central bibliography](../../bibliography.md) for full source details.
