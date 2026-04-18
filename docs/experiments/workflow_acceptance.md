# Workflow Acceptance

TrayGuard only matters if it helps people complete tray checks without making
their work harder. This page explains how to think about usability and adoption.

## What This Test Answers

A hospital does not buy a detector. It buys a workflow change.

## Why This Is A Risk

Healthcare decision-support tools can fail when they interrupt workflow or
create too many low-value alerts. A clinical decision-support review highlights
that inappropriate alerts can interrupt clinical workflow
([Olakotan and Yusof, 2021](https://pubmed.ncbi.nlm.nih.gov/33853395/)), and
another review ties alert burden to alert fatigue and reduced usability and
acceptance
([Cánovas-Segura et al., 2023](https://pubmed.ncbi.nlm.nih.gov/37245656/)).

SPD improvement work also shows that missing and unusable instrumentation is not
only a detection problem. Successful improvement involved staffing, training,
inventory, equipment, physical environment, workflows, communication, and
governance
([Natarus et al., 2025](https://www.sciencedirect.com/science/article/abs/pii/S1553725024003003)).
TrayGuard therefore has to fit the human workflow, not just produce boxes on an
image.

This test answers:

- Does TrayGuard help users catch tray issues?
- Does it slow the task down?
- Do users understand uncertainty and review prompts?
- Does the tool feel like an assistant instead of an obstacle?

## Tray Issues To Include

Use tray-like tasks that include realistic problems:

- One missing required item.
- One extra item.
- One similar-looking wrong item.
- One hard-to-see or partially hidden item.
- One unknown distractor object.

The goal is to test the workflow, not just the model.

## What To Measure

Track both task outcomes and user reactions.

| Category | Examples |
| --- | --- |
| Accuracy | Missing items caught, wrong items caught, extra items caught |
| Speed | Time to final tray decision, number of rescans |
| Correction burden | Number of model corrections, ease of correction |
| Trust | Whether users understood review prompts and final status |
| Hesitation | Moments where the user paused, questioned, or distrusted the system |

## Suggested User Questions

Use a 1-5 scale:

1. TrayGuard made the task easier.
2. TrayGuard made me more confident in the final tray check.
3. I understood which detections needed review.
4. Correcting the system was easy.
5. I would want this tool if I were responsible for tray assembly.

Ask one open-ended question:

- What is the biggest reason you would hesitate to use this system?

## Product Interpretation

| Pattern | What It Means | Product Response |
| --- | --- | --- |
| Users catch more issues with small added time | The workflow has promise | Keep the assistant framing |
| Users are faster but miss issues | The product is not helping safely | Make review states clearer |
| Users correct the model easily | Human-in-the-loop design is viable | Keep correction controls simple |
| Users distrust confident results | The product needs better evidence and explanations | Show uncertainty, examples, and logs |
| Users dislike rescanning | The scan guidance is too costly | Make rescan instructions specific and fast |

## What We Are Not Claiming

- Classmate or team-member feedback does not prove SPD technician adoption.
- Speed alone is not success.
- TrayGuard should support technician judgment, not replace it.

## References

- Bridges, ["The Real Costs of Surgical Instrument Training in Sterile Processing Revisited"](https://doi.org/10.1016/j.aorn.2009.10.025), AORN Journal, 2010.
- Cánovas-Segura et al., ["Meaningful time-related aspects of alerts in Clinical Decision Support Systems. A unified framework"](https://pubmed.ncbi.nlm.nih.gov/37245656/), Journal of Biomedical Informatics, 2023.
- Hu et al., ["Improvement and implementation of central sterile supply department training program based on action research"](https://link.springer.com/article/10.1186/s12912-024-01809-z), BMC Nursing, 2024.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Ofstead et al., ["Improving mastery and retention of knowledge and complex skills among sterile processing professionals: A pilot study on borescope training and competency testing"](https://doi.org/10.1016/j.ajic.2023.03.002), American Journal of Infection Control, 2023.
- Olakotan and Yusof, ["The appropriateness of clinical decision support systems alerts in supporting clinical workflows: A systematic review"](https://pubmed.ncbi.nlm.nih.gov/33853395/), Health Informatics Journal, 2021.
