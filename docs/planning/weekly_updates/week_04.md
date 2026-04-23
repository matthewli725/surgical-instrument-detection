# Week 04 Update

## Completed

- Narrowed the next CV risk work to two concrete tracks:
  lighting robustness and similar-looking instrument recognition.
- Turned the lighting question into a defined experiment plan with staged
  training conditions instead of ad hoc trial runs.
- Reviewed the current lighting data and identified the immediate cleanup work
  needed before reproducible training and evaluation.
- Started framing the similar-instrument study around pairwise confusion risk
  rather than generic fine-grained accuracy.
- Identified candidate proxy pairs for the first similar-instrument runs and
  outlined the initial collection needs.
- Continued converting experiment ideas into clearer CDR-ready writeups so the
  technical work supports the project story.

## Goals For Next Week

- Finish auditing and normalizing the lighting dataset so the splits and
  condition names are consistent.
- Run the first reproducible lighting baseline and collect precision, recall,
  `mAP50`, and `mAP50-95` in one summary table.
- Select the first similar-instrument proxy pairs and write a short rationale
  for why they are hard but representative.
- Collect and organize the initial image set for those pairs in a consistent
  folder structure.
- Draft the first experiment writeup sections while the results are still fresh
  so they can drop into the CDR narrative later.
