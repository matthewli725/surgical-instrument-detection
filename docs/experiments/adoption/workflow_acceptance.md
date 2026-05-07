# Workflow Acceptance

TrayGuard only matters if it helps people complete tray checks without making
their work harder. This page explains how to think about usability and adoption.

## What This Test Answers

A hospital does not buy a detector. It buys a workflow change.

## Why This Is A Risk

Healthcare decision-support tools can fail when they interrupt workflow or
create too many low-value alerts. A clinical decision-support review highlights
that inappropriate alerts can interrupt clinical workflow
([Olakotan and Yusof, 2021](../../bibliography.md#olakotan-and-yusof-2021)), and
another review ties alert burden to alert fatigue and reduced usability and
acceptance
([Cánovas-Segura et al., 2023](../../bibliography.md#canovas-segura-et-al-2023)).

SPD improvement work also shows that missing and unusable instrumentation is not
only a detection problem. Successful improvement involved staffing, training,
inventory, equipment, physical environment, workflows, communication, and
governance
([Natarus et al., 2025](../../bibliography.md#natarus-et-al-2025)).
TrayGuard therefore has to fit the human workflow, not just produce boxes on an
image.

This test answers:

- Does TrayGuard help users catch tray issues?
- Does it slow the task down?
- Do users understand uncertainty and review prompts?
- Does the tool feel like an assistant instead of an obstacle?

## Design Assumptions For This Test

This page focuses on how to test workflow acceptance, not on re-arguing the
full adoption case. The background narrative and detailed appendix already cover
the broader evidence base:

- `docs/background/project_background.md`
- `docs/experiments/adoption/formal_risk_analysis.md`

For this experiment, we assume the product is being evaluated as a guided
verification assistant rather than as a fully autonomous tray-approval system.
That means the workflow test should focus on whether TrayGuard helps users catch
issues, recover from uncertainty, and finish the task with acceptable time and
correction burden.

The main workflow hypotheses are:

- Assistant-mode review is more acceptable than automation-style language.
- Users will tolerate imperfect detections if corrections are fast and obvious.
- Trust will depend more on uncertainty handling and correction burden than on raw detector accuracy alone.
- False alarms and rescans will hurt adoption quickly.

## UI Design Principles To Validate

The UI should be evaluated as part of the safety workflow. A good TrayGuard
screen minimizes unnecessary effort while preserving deliberate review for
exceptions, uncertainty, and final human confirmation.

Use these principles as acceptance criteria for the next UI pass:

| Principle | Stakeholder Meaning | What To Look For In Testing |
| --- | --- | --- |
| Reduce interaction cost | The repeated path should not require unnecessary button presses, reading, scrolling, waiting, or mode switching. | Time to final decision, action count, backtracking, and whether each action visibly moves the user closer to completion. |
| Use deliberate action targets | Some steps, such as final human confirmation or reviewing a risky detection, are valuable even if they add an action. | Whether extra actions prevent mistakes or only slow the user down. |
| Make tray state visible | The user should not infer the result from bounding boxes alone. The screen should state whether the tray is complete, missing items, has extras, or needs review. | Whether participants can state the tray status in plain language without help. |
| Make uncertainty actionable | Low-confidence, similar-looking, unknown, glare, overlap, and count-mismatch cases should say what needs review or what scan condition should change. | Whether participants know when to inspect manually, correct the result, dismiss a prompt, or rescan. |
| Keep correction fast | Imperfect detections are acceptable only if the user can fix or route them without restarting the task. | Correction time, correction success, frustration comments, and repeated failed attempts. |
| Use visual-first feedback | Persistent visible status should be the source of truth. Audio may reinforce major state changes but should never be required to understand the screen. | Whether users notice status changes visually, and whether the task still works with sound muted. |
| Restrain alerts | Alerts should be limited to conditions that change the tray decision or require action. Low-value or repeated alerts risk being ignored. | False alert rate, dismissals, ignored correct warnings, and comments about interruption. |
| Preserve human authority | The final tray decision should remain an explicit human confirmation. | Whether users still feel responsible and do not treat the system as silent approval. |

For this prototype, the preferred normal path is: select or confirm the required
list, capture or start the scan, review the tray summary, resolve any flagged
exception, and confirm the final decision. Model settings and camera
configuration are implementation controls; they should not dominate the
technician-facing workflow.

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
| Feedback clarity | Whether visual status, optional audio cues, and review messages made the next action obvious |

## Literature-Guided Study Logic

The strongest user study should not ask only whether the tool is "easy." It
should test whether the assistant improves a real verification task without
creating new work, hidden over-reliance, or adoption barriers.

Use four evidence buckets:

| Evidence bucket | Why it matters | Supporting literature | What to ask or observe |
| --- | --- | --- | --- |
| Task performance | A detector is only useful if people catch missing, wrong, extra, or uncertain items. | Automation-bias and CDSS studies warn that automated support can introduce new errors if users over-trust or ignore it ([Goddard et al., 2012](../../bibliography.md#goddard-et-al-2012), [Olakotan and Yusof, 2021](../../bibliography.md#olakotan-and-yusof-2021)). | Error catch rate, false accepts, false rejects, corrections, overrides, and final tray decisions. |
| Workload and usability | Healthcare tools fail when they add time, clicks, alerts, or mental load. | SUS, NASA-TLX, and HSUS frame usability around task completion, workload, workflow integration, user control, and patient-safety-relevant ease of use ([Brooke, 1996](../../bibliography.md#brooke-1996), [NASA TLX, accessed 2026](../../bibliography.md#nasa-tlx-accessed-2026), [Ghorayeb et al., 2023](../../bibliography.md#ghorayeb-et-al-2023)). | Time, steps, rescans, frustration, clarity, correction burden, and mental demand. |
| Trust calibration | The system must make uncertainty and failure recoverable, not just look confident. | Trust-in-automation and human-AI interaction work supports measuring whether users know system limits and can correct or dismiss wrong AI output ([Jian et al., 2000](../../bibliography.md#jian-et-al-2000), [Amershi et al., 2019](../../bibliography.md#amershi-et-al-2019)). | Whether users understand review-needed states, challenge confident errors, and keep human sign-off meaningful. |
| Adoption fit | Hospitals adopt workflows, not screens. Fit depends on roles, training, leadership, infrastructure, and local value. | TAM/UTAUT, hospital AI acceptance, CSSD training, pharmacy robotics, and hospital implementation studies emphasize usefulness, ease of use, role fit, training, leadership communication, infrastructure, costs, privacy, interoperability, and workflow fit ([Davis, 1989](../../bibliography.md#davis-1989), [Lambert et al., 2023](../../bibliography.md#lambert-et-al-2023), [Hu et al., 2024](../../bibliography.md#hu-et-al-2024), [Hogan et al., 2020](../../bibliography.md#hogan-et-al-2020), [Abell et al., 2023](../../bibliography.md#abell-et-al-2023), [McGinn et al., 2011](../../bibliography.md#mcginn-et-al-2011), [Grossi et al., 2021](../../bibliography.md#grossi-et-al-2021)). | Whether the tool fits existing tray work, who must approve it, what training is needed, and what evidence would justify a pilot. |

## Recommended Study Structure

Run the study as a task-based walkthrough rather than a pure survey.

1. Baseline interview: ask about the participant's role, experience with
   checklists or verification tasks, and prior use of automation.
2. Manual tray check: have the participant inspect a tray or tray-like scene
   using a printed required list.
3. TrayGuard-assisted check: have the participant inspect comparable scenarios
   with the assistant. Counterbalance the order if there are enough
   participants.
4. Post-task survey: use the Likert items below, plus SUS or NASA-TLX if a
   standard benchmark is useful.
5. Semi-structured interview: ask about trust, workflow fit, training, failure
   recovery, and adoption concerns.

If the participants are classmates or general users, report the result as UI
and task-walkthrough evidence only. Do not claim SPD adoption unless at least
some participants have sterile-processing, OR, pharmacy, lab, radiology, or
hospital operations experience.

## College Student Participant Caveat

College students are not a proxy for sterile-processing technicians. They do
not have SPD knowledge of instrument names, tray norms, substitutions,
contamination risk, packaging rules, damaged-tool handling, local policy, OR
urgency, or accountability. A positive student study therefore cannot prove SPD
technician adoption, hospital workflow fit, or safety readiness.

College students can still be useful participants for a narrower question:

> Can a novice user complete a checklist-based visual verification task with
> limited training, understand the system's review prompts, and avoid blindly
> accepting incorrect automation?

That question has a plausible parallel to early onboarding and guided
verification. Many student tasks have the same cognitive structure as tray
checking even if the domain is different:

- Lab setup: compare unfamiliar tools, reagents, or materials against a
  protocol before starting.
- Engineering kits: compare physical parts against a bill of materials.
- First-aid or emergency-kit restocking: check required items, counts, and
  missing supplies.
- Warehouse or classroom picking tasks: verify that the selected objects match
  a list before handoff.
- Practical exams or lab checkouts: confirm that a physical setup is complete,
  safe enough to proceed, and documented.

The defensible claim is therefore:

> Student participants support a novice-learnability and checklist-verification
> claim. If TrayGuard helps untrained users catch missing, extra,
> wrong-but-similar, or uncertain items without excessive over-reliance, that
> suggests the system may lower training friction. SPD technician validation is
> still required before claiming real workflow adoption.

This framing turns the limitation into a bounded study purpose. It does not
argue that students are equivalent to technicians; it argues that novices can
test whether the interface teaches the verification workflow clearly enough to
reduce onboarding burden.

### Risk Of Overclaiming

The tempting argument is: "If TrayGuard works for complete novices, it proves
the system lowers the barrier to entry." Use "suggests" instead of "proves."
The main flaws are:

- Students may rely on the system because they lack domain knowledge, not
  because the system is genuinely trustworthy.
- Students may not know when a confident result is wrong, which can make
  automation bias look like usability.
- Students are not working under SPD time pressure, interruptions, shift
  fatigue, sterility constraints, or real accountability.
- A workflow that helps novices may still feel slow or unnecessary to an
  experienced technician.
- A short class study cannot measure local SOP fit, manager approval,
  competency requirements, IT support, or downtime procedures.

### How To Report Student Results

Use this boundary in the writeup:

| Student Study Can Support | Student Study Cannot Support |
| --- | --- |
| Novice learnability | SPD technician adoption |
| Clarity of tray-like checklist workflow | Safety readiness in real sterile processing |
| Whether prompts and review states are understandable | Whether experts would trust or tolerate the system |
| Whether students catch planted issues with less workload | Whether the system reduces real OR delays or tray defects |
| Whether the tool may reduce onboarding burden | Whether hospital administrators would approve deployment |

## Observation Checklist

Record these without asking the participant to self-report them:

- Time from first view of the tray to final decision.
- Number of user actions: select tray, capture, rescan, review, correct, finalize.
- Number of missing, wrong, extra, hidden, and unknown objects caught.
- Number of planted issues missed.
- Number of system errors the participant noticed and corrected.
- Number of times the participant accepted a wrong system output.
- Number of times the participant ignored or dismissed a correct warning.
- Number of rescans and why they happened.
- Whether users noticed scan-complete, review-needed, and error feedback.
- Whether users could complete the task with sound muted.
- Whether users could explain the tray issue without only repeating the system
  label.
- Help requests, pauses, backtracking, or comments showing confusion.
- Whether the participant could state the final tray status in plain language.

## Post-Task Survey

Use a 1-5 agreement scale:

`1 = strongly disagree`, `3 = neutral`, `5 = strongly agree`.

### Usability And Workload

1. I could complete the tray-check task without help.
2. The order of steps felt clear from start to finish.
3. TrayGuard added too many extra steps.
4. The review screen was easy to scan.
5. The amount of information shown felt manageable.
6. I could imagine using this repeatedly without frustration.
7. The main action on the screen was clear at each step.

### Workflow Fit

1. TrayGuard fit naturally into the way I would check a tray.
2. The system highlighted problems at the right time.
3. Review prompts were specific enough for me to know what to do next.
4. Rescanning or correcting the system felt fast enough.
5. The tool would be more helpful than a manual checklist alone.
6. The tool would slow the work down too much.
7. Alerts appeared only when they were worth my attention.

### Trust, Safety, And Human Authority

1. I understood which detections were confident and which needed review.
2. I knew when to inspect manually instead of relying on the system.
3. The system made me more confident in the final tray check.
4. The system would help catch missing, wrong, or extra items.
5. I would worry that users might accept the system's output too quickly.
6. I still felt responsible for the final decision.
7. The final confirmation step felt appropriate for the task.
8. I relied on TrayGuard because I understood the tray state, not because I had
   no other way to decide.

### Error Recovery

1. When TrayGuard was wrong, I could correct it.
2. I knew what to do when an item was hidden, unknown, or ambiguous.
3. The system gave enough information to recover from a bad scan.
4. I would know how to continue if TrayGuard were unavailable.
5. The saved result would help explain why the tray was approved or flagged.
6. I could still understand the system state without relying on sound.

### Adoption Intent

1. I would want this tool if I were responsible for tray assembly or verification.
2. The training required to use this system seems reasonable.
3. I would recommend piloting this workflow with real sterile-processing staff.
4. I would need stronger evidence before using this in a safety-critical workflow.
5. Workflow disruption would be a major adoption barrier.
6. This system seems useful for helping a beginner learn what to check.

For small samples, report medians and the number of participants who chose
`4` or `5`; do not over-interpret decimal averages. Reverse-code negative
items when summarizing by category.

## Open-Ended Interview Questions

Ask these after the task so participants can answer from experience.

1. Walk me through how you decided the tray was ready or not ready.
2. Where did TrayGuard help you most?
3. Where did it slow you down or interrupt your normal checking strategy?
4. Was there any moment when you trusted the system more than you should have?
5. Was there any moment when you distrusted the system even though it was useful?
6. What did you think the review-needed state meant?
7. What would you change about the correction or rescan process?
8. What would make you hesitate to use this system in real work?
9. What training would someone need before using it alone?
10. What kind of failure would make you stop using it?
11. Did you rely on TrayGuard because you understood the tray, or because you
    did not know how else to decide?
12. Would you have noticed the planted issue without TrayGuard?
13. Did TrayGuard teach you what to inspect, or did it simply give you an
    answer?
14. What information would you need before trusting this in a real
    safety-critical job?

## Technician-Focused Questions

Use these for sterile-processing technicians, OR staff, pharmacy technicians,
lab technicians, radiology technologists, or similar operational users.

1. Where in your current workflow would this tool fit best?
2. Which part of tray or equipment verification is most error-prone today?
3. Would this reduce visual search, counting, interruption, or documentation burden?
4. Would it change who is responsible for the final check?
5. Would it make you feel monitored, replaced, supported, or something else?
6. What exception cases happen often: substitutions, damaged items, loaner trays,
   partial sets, hidden tools, rushed work, or interruptions?
7. How much false alerting would be tolerable before people ignored the tool?
8. What should happen when the system is unsure?
9. What should happen when the system is down?
10. Who would staff trust for training: peers, leads, vendor trainers, engineers,
    infection prevention, or managers?

This category matters because hospital worker adoption is role-specific.
Radiology AI research shows that different professional groups can have
different knowledge, autonomy concerns, and attitudes toward the same AI
technology, while CSSD training research supports practical, iterative,
participant-informed training instead of one-way instruction
([Chen, Stavropoulou, et al., 2021](../../bibliography.md#chen-stavropoulou-et-al-2021),
[Hu et al., 2024](../../bibliography.md#hu-et-al-2024)).

## Administrator And Manager Questions

Use these for SPD managers, OR directors, quality leaders, hospital innovation
teams, purchasing, IT, risk, or compliance stakeholders.

1. What problem would this need to solve before you would sponsor a pilot?
2. Which baseline metric matters most: missing instruments, tray defects,
   rework time, OR delay minutes, documentation burden, training burden, or
   staff satisfaction?
3. What level of local validation would you need before using it outside a demo?
4. Who would approve the workflow change?
5. Which departments would need to be involved: SPD, OR, infection prevention,
   quality, IT, biomed, risk, purchasing, or finance?
6. What would make the pilot too disruptive?
7. What data can the system store without creating privacy, security, or policy
   issues?
8. What evidence would justify the hardware, training, maintenance, and support
   costs?
9. What SOP or competency documentation would need to change?
10. What should the audit record prove: who checked the tray, what was flagged,
    what was corrected, or why a tray was approved?
11. What downtime or manual fallback process would be required?
12. What would make you reject the system even if users liked it?

This category matters because adoption decisions at the hospital level are
contextual. Reviews of EHR and health-technology implementation identify
interoperability, privacy, security, cost, productivity, infrastructure, human
resources, finance, leadership, and stakeholder differences as adoption factors
([McGinn et al., 2011](../../bibliography.md#mcginn-et-al-2011),
[Grossi et al., 2021](../../bibliography.md#grossi-et-al-2021)). A hospital
team may also require clinical or operational evidence, availability through
normal ordering channels, and clear ownership before adopting a new technology
([Vonken et al., 2024](../../bibliography.md#vonken-et-al-2024)).

## What Counts As Convincing

For a class or capstone user study, a convincing result would look like:

- Participants catch more planted tray issues with TrayGuard than with the
  manual-only baseline, or catch the same issues with lower workload.
- Median ratings are at least `4` for step clarity, review clarity, correction
  ease, confidence, human responsibility, and willingness to pilot.
- Median ratings are at most `2` for "too many extra steps," "slows work down
  too much," "users might accept output too quickly," and "workflow disruption
  would be a major adoption barrier."
- Observed correction and rescan steps are fast enough that participants do not
  treat them as a separate chore.
- Open-ended answers identify specific fixable issues instead of broad rejection.
- Student participants can explain why a tray was flagged, not only repeat that
  the system said it was flagged.
- The study reports the finding as novice learnability and tray-like
  verification support, not as SPD adoption evidence.

For a hospital-facing claim, the bar is higher:

- At least one relevant operational user says the workflow fits a plausible
  tray-check step.
- A manager or administrator can name a pilot metric, approval path, evidence
  requirement, and failure condition.
- The study reports negative feedback and limitations, not only positive quotes.

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
- Low hardware cost alone does not prove adoption.
- A good offline accuracy number alone does not prove workflow value.

## Bibliography

See the [central bibliography](../../bibliography.md) for full source details.
