# Workflow Acceptance

TrayGuard only matters if the learning workflow helps novices practice tray
work without making the training process harder. This page explains how to test
usability and adoption for the training platform.

## What This Test Answers

A hospital or training program does not buy a detector. It buys a workflow
change: a way to reduce early training burden while preserving instructor
authority, local competency expectations, and supervised hands-on sign-off.

For the training module, this test asks:

- Can learners move through pre-test, study, quiz, practice, and post-test
  without help?
- Does feedback make the next learning action obvious?
- Does the module feel faster than asking an instructor for every unfamiliar
  instrument?
- Do learners understand that post-test results are simulated evidence, not
  certification or workplace sign-off?

## Why This Is A Risk

SPD improvement work shows that missing and unusable instrumentation is not
only a recognition problem. Successful improvement involves staffing, training,
inventory, equipment, physical environment, workflows, communication, and
governance ([Alfred et al., 2021](../../../bibliography.md#alfred-et-al-2021),
[Natarus et al., 2025](../../../bibliography.md#natarus-et-al-2025)).

Healthcare implementation research also warns that adoption depends on
workflow fit, leadership, infrastructure, privacy, cost, training, and user
trust, not technical performance alone
([Chomutare et al., 2022](../../../bibliography.md#chomutare-et-al-2022),
[Lambert et al., 2023](../../../bibliography.md#lambert-et-al-2023),
[Grossi et al., 2021](../../../bibliography.md#grossi-et-al-2021)).

TrayGuard therefore has to fit the training workflow, not just present correct
answers.

## UI Principles To Validate

| Principle | Stakeholder Meaning | What To Look For |
| --- | --- | --- |
| Clear mode boundaries | Learners and instructors must know when the system is teaching versus assessing. | Participants can explain the difference between study, quiz, practice, pre-test, and post-test. |
| Low-friction practice | A trainee should not need an instructor to explain every screen. | Time to start, help requests, pauses, backtracking, and comments about confusion. |
| Actionable feedback | Feedback should tell the learner what was wrong and what to review next. | Learners can name whether they missed an item, added an extra, chose a wrong item, misidentified a lookalike, or used the wrong count. |
| Assessment integrity | Pre/post results are only useful if hints and feedback are suppressed during assessment. | Participants do not receive answer leakage during pre-test or post-test. |
| Confidence awareness | Instructors need to see overconfidence and fragile knowledge, not only raw score. | High-confidence errors and low-confidence correct answers are captured. |
| Human authority | The tool should support training, not imply certification or autonomous approval. | Participants can state that a supervisor/preceptor still owns real competency sign-off. |

## What To Measure

| Category | Examples |
| --- | --- |
| Task completion | Whether the participant completes every mode without help. |
| Learning outcome | Pre/post accuracy, duration, confidence, and error-category changes. |
| Feedback comprehension | Whether the participant can explain one mistake and next review step. |
| Workflow friction | Help requests, backtracking, unclear labels, excessive reading, or repeated failed attempts. |
| Trust boundary | Whether the participant understands the result is simulated training evidence. |
| Admin relevance | Whether the exported summary would help an instructor or manager see weak areas. |

## Recommended Study Structure

Run the study as a task-based walkthrough:

1. Baseline interview: ask about prior SPD, medical, lab, or tool-identification
   experience.
2. Pre-test: have the participant sort or check the local tray module with no
   hints or feedback.
3. Study and quiz: have the participant review cards and answer identification
   prompts.
4. Practice sort: let the participant receive error-specific feedback.
5. Post-test: use a comparable tray-sorting assessment with no hints or
   feedback.
6. Post-task survey and interview: ask what became easier, what remained
   confusing, and whether the metrics would help a learner or instructor.

Use descriptive results and participant-level plots for a small class demo.
Do not overstate statistical significance.

## College Student Participant Caveat

College students are not a proxy for sterile-processing technicians. They do
not have SPD knowledge of instrument names, tray norms, substitutions,
contamination risk, packaging rules, damaged-tool handling, local policy, OR
urgency, or accountability. A positive student study therefore cannot prove SPD
technician adoption, hospital workflow fit, or safety readiness.

College students can still be useful participants for a narrower question:

> Can a novice user learn an unfamiliar checklist-like tray task, understand
> feedback, and improve on a comparable post-test?

That question is relevant to early onboarding, but only as a simulated
learnability proxy.

| Student Study Can Support | Student Study Cannot Support |
| --- | --- |
| Novice learnability | SPD technician adoption |
| Clarity of the learning workflow | Safety readiness in real sterile processing |
| Whether feedback is understandable | Whether experts would trust or tolerate the system |
| Whether students improve on simulated sorting | Whether the system reduces real OR delays or tray defects |
| Whether the tool may reduce training friction | Whether hospital administrators would approve deployment |

## Post-Task Survey

Use a 1-5 agreement scale:

`1 = strongly disagree`, `3 = neutral`, `5 = strongly agree`.

### Usability And Learning Flow

1. I could complete the training workflow without help.
2. The order of steps felt clear from start to finish.
3. The study cards helped me understand the instruments.
4. The quiz helped me notice what I did not know.
5. Practice feedback made it clear what to review next.
6. The amount of information shown felt manageable.
7. I could imagine using this repeatedly without frustration.

### Assessment And Trust Boundary

1. I understood when I was practicing and when I was being assessed.
2. I understood that the post-test was simulated evidence, not certification.
3. I would still expect an instructor or supervisor to verify real competence.
4. The confidence rating helped me reflect on what I knew.
5. The final summary made my weak areas visible.

### Stakeholder Fit

1. This tool could help a new learner practice before asking an instructor for
   help.
2. This tool could help an instructor see what a learner is struggling with.
3. I would recommend piloting this workflow with real sterile-processing staff.

## Interview Prompts

Ask 5-8, depending on time:

1. What became easier after using the study and practice modes?
2. Which instrument or tray rule was still confusing?
3. Which feedback message helped most?
4. Did any screen feel like it was testing you before teaching you?
5. What would you want an instructor to see in your results?
6. What would make this feel more trustworthy as a training tool?
7. What should the system never claim based on this short exercise?

## Evidence Interpretation

| Finding | Meaning | Next Step |
| --- | --- | --- |
| Learners improve accuracy and reduce severe errors | The training loop has promise. | Expand content and run a larger novice study. |
| Learners improve accuracy but take longer | The tool may increase carefulness before fluency. | Add timed practice and better retrieval repetition. |
| Learners cannot explain errors | Feedback is not actionable enough. | Rewrite feedback around distinguishing features and next steps. |
| Learners confuse assessment and practice | Mode boundaries are too weak. | Strengthen labels, screen state, and hint suppression. |
| Students improve, but results are small or uneven | Useful early signal, not SPD proof. | Treat as iteration input and seek SPD participant validation later. |
