# Similar-Looking Tools

TrayGuard needs to distinguish tools that look almost the same. This page
explains why that matters and how to interpret results for visually similar
classes.

## What This Test Answers

Some tray errors are not obvious. A wrong tool may have the same general shape
as the correct one, such as a straight instrument instead of a curved one.

## Why This Is A Risk

Computer vision research treats fine-grained recognition as a hard problem
because the model must distinguish categories with small inter-class differences
and sometimes large variation within the same class
([Zhao et al., 2017](https://link.springer.com/article/10.1007/s11633-017-1053-3)).
Recent fine-grained recognition work makes the same point: subtle differences
between otherwise similar categories are difficult for generic classifiers
([Wang et al., 2021](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0254054)).

This is directly relevant to sterile processing. In a packaging-error study,
wrong instrument specification was the largest category, and the authors note
that instruments in the same category can have very small structural
differences
([Zhu et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6425664/)).
That is exactly the kind of visual problem this experiment is meant to test.

This test answers:

- Can TrayGuard tell similar tools apart?
- Which pairs are most often confused?
- Are wrong labels low confidence or high confidence?
- Which pairs should require human review before confirmation?

## Similarity Examples

Useful pairs include:

- Straight vs curved scissors.
- Straight vs curved clamps.
- Similar tools with different jaw, tip, or handle shapes.
- Long narrow instruments that share the same silhouette.
- Proxy objects such as similar scissors, pliers, tweezers, pens, or utensils.

The test should be challenging enough that success means something. If the
objects are visually obvious, the result does not tell us much about real tray
verification risk.

## How To Read The Results

Aggregate accuracy is not enough. Look at class-level and pair-level outcomes.

- Per-class precision: when the model predicts this class, how often is it
  right?
- Per-class recall: how often does the model find this class when it is present?
- Pair confusion: which specific class pairs get mixed up?
- High-confidence wrong class: the riskiest failure mode.

The most important result is the worst similar pair, not the average score.

## Product Interpretation

| Result Pattern | What It Means | Product Response |
| --- | --- | --- |
| Similar pairs are separated reliably | TrayGuard can support more specific tray checks | Keep class labels specific |
| One similar pair fails often | That pair needs special handling | Add targeted data or review prompts |
| Wrong similar-class labels are high confidence | The product may falsely reassure the user | Add confidence review for that pair |
| Similar tools are low confidence | The system is failing more safely | Ask the user to confirm the class |

## User-Facing Guidance

When TrayGuard flags a similar-looking item for review, the user should compare:

- Tip shape.
- Curve direction.
- Handle shape.
- Jaw or blade profile.
- Size and length.
- Any printed or etched markings visible in the image.

The product should make review fast instead of pretending that every similar
tool can be automatically confirmed.

## What We Are Not Claiming

- A few proxy classes do not prove coverage of all surgical instruments.
- High aggregate mAP does not mean every important pair is safe.
- Tool identification is not the same thing as functional inspection.

## References

- Nichol and Saari, ["Patterns in staff reported surgical instrument errors point to failures in visualization as a critically weak point in sterile processing of surgical instruments"](https://doi.org/10.1016/j.pcorm.2023.100356), Perioperative Care and Operating Room Management, 2023.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
- Wang et al., ["Fine-grained classification based on multi-scale pyramid convolution networks"](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0254054), PLOS One, 2021.
- Zhao et al., ["A survey on deep learning-based fine-grained object classification and semantic segmentation"](https://link.springer.com/article/10.1007/s11633-017-1053-3), Machine Intelligence Research, 2017.
- Zhu et al., ["Errors in packaging surgical instruments based on a surgical instrument tracking system: an observational study"](https://link.springer.com/article/10.1186/s12913-019-4007-3), BMC Health Services Research, 2019.
