# Unknown Objects And Confidence

TrayGuard should be allowed to say "needs review" when it sees something
outside its trained class list. This page explains why uncertainty matters and
how to interpret confidence results.

## What This Test Answers

A tray-checking assistant should not force every object into the closest known
class. Unknown tools, distractors, damaged objects, or unclear images can all
create unsafe false confidence.

## Why This Is A Risk

Most standard classifiers are evaluated as closed-set systems, where every test
class is known during training. Open-set recognition research argues that this
is unrealistic for real vision applications because unknown classes can appear
at inference time
([Scheirer et al., 2013](https://pubmed.ncbi.nlm.nih.gov/23682001/)).
Deep open-set work states the practical requirement plainly: a recognizer must
classify known samples and reject unknown samples, while conventional deep
models assume a closed environment
([Schlachter et al., 2020](https://link.springer.com/article/10.1007/s42979-020-0086-9)).

This matters for TrayGuard because tray errors include missing, extra, and wrong
instruments, and a wrong instrument can look similar to the expected one
([Zhu et al., 2019](https://bmchealthservres.biomedcentral.com/articles/10.1186/s12913-019-4007-3)).
If an unknown object is confidently labeled as a known tool, the product could
make a bad tray look complete.

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

## References

- Chen et al., ["Incidence of Adverse Events in Central Sterile Supply Department: A Single-Center Retrospective Study"](https://doi.org/10.2147/RMHP.S423108), Risk Management and Healthcare Policy, 2023.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
- Rubak et al., ["Surgical instrument tray optimization process at a university hospital: A comprehensive overview"](https://doi.org/10.1016/j.sopen.2024.09.007), Surgery Open Science, 2024.
- Scheirer et al., ["Toward open set recognition"](https://pubmed.ncbi.nlm.nih.gov/23682001/), IEEE Transactions on Pattern Analysis and Machine Intelligence, 2013.
- Schlachter et al., ["Deep Open Set Recognition Using Dynamic Intra-class Splitting"](https://link.springer.com/article/10.1007/s42979-020-0086-9), SN Computer Science, 2020.
- Zhu et al., ["Errors in packaging surgical instruments based on a surgical instrument tracking system: an observational study"](https://link.springer.com/article/10.1186/s12913-019-4007-3), BMC Health Services Research, 2019.
