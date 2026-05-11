# Training Effectiveness

This is the primary evaluation plan for the training-platform pivot. It tests
whether TrayGuard can reduce simulated time-to-competency for one local tray
module.

## What This Test Answers

The study asks:

> After using TrayGuard's study, quiz, and practice modes, does a novice
> complete a comparable tray-sorting assessment more accurately, faster, with
> fewer error types, and with better-calibrated confidence?

This is not a hospital deployment study. It is a controlled learning study that
supports or weakens the product's training claim.

## Closest Precedent

The strongest direct precedent is Ofstead et al.'s sterile-processing training
pilot on borescope-based endoscope visual inspection. The topic was endoscope
reprocessing rather than tray assembly, but the study tested the same kind of
training process TrayGuard needs: pre-test, structured teaching, demonstration,
hands-on practice, post-test, confidence/satisfaction measurement, workplace
homework, and a booster session. Their certified SP trainee group improved from
41% to 84% mean test score after the workshop and retained high scores after
the 2-month booster ([Ofstead et al., 2023](../../../bibliography.md#ofstead-et-al-2023)).

TrayGuard should therefore use Ofstead as the local sterile-processing model,
with broader simulation and retrieval-practice literature as support.

## Why The Intervention Should Help

The intervention is not evaluated as flashcards alone. The study cards orient
learners to local instrument names, aliases, photos, families, and distinguishing
features, but the active learning work comes from retrieval practice, simulated
tray sorting, and feedback.

The quiz requires learners to recall or recognize instrument concepts, which
matches retrieval-practice evidence better than passive rereading. The practice
tray sort asks learners to apply that recall in a count-sheet-like task: choose
the required instruments, use the right quantities, avoid distractors, and
distinguish lookalikes. Immediate error-specific feedback then tells learners
whether the issue was `missing`, `extra`, `wrong`, `misidentified`, or
`wrong_count`, so the next attempt has a concrete target.

That is why the outcome should be measured with a no-hints pre-test and
post-test rather than quiz scores alone. If the full loop is helpful, learners
should show better simulated tray-sorting accuracy, duration, error breakdowns,
and confidence calibration after practice.

## Hypotheses

| Hypothesis | Metric |
| --- | --- |
| Learners improve tray sorting accuracy after practice. | Post-test accuracy exceeds pre-test accuracy on a comparable tray task. |
| Learners complete the task faster without losing accuracy. | Post-test duration decreases while accuracy does not decline. |
| Learners make fewer severe errors. | Missing, wrong, misidentified, extra, and wrong-count errors decline by category. |
| Learners become better calibrated. | High-confidence errors decline, and low-confidence correct answers become visible for follow-up. |
| The module lowers instructor explanation burden. | Learners can explain what they missed and what they should review next. |

## Study Design

Use one seeded tray module with 8-12 required instruments and a small distractor
pool. Use parallel pre/post tasks so the post-test is not an exact replay of the
pre-test.

1. Consent and demographic context: ask about prior SPD, medical, lab, or tool
   identification experience.
2. Pre-test tray sort: no hints, no feedback, timed, confidence and `Not sure`
   captured.
3. Study cards: learners review the same tray's instruments, aliases, families,
   notes, and distinguishing features.
4. Identification quiz: learners answer recall or recognition prompts with
   distractors.
5. Practice tray sort: learners receive immediate error-specific feedback.
6. Post-test tray sort: no hints, no feedback, timed, confidence and `Not sure`
   captured.
7. Short interview: ask what became easier, what remained confusing, and which
   feedback helped most.

Stretch extension, if the schedule allows: add a delayed retention check or
short booster session using the same weak-item summary, modeled on Ofstead's
2-month booster.

## Metrics

| Metric | Definition | Why It Matters |
| --- | --- | --- |
| Accuracy | Required items correctly selected with correct counts. | Primary learning outcome. |
| Duration | Seconds from task start to final submission. | Proxy for time-to-competency and fluency. |
| Error breakdown | Counts of missing, extra, wrong, misidentified, and wrong-count errors. | Shows what kind of competency improved. |
| Confidence | 1-5 learner rating per assessment or item. | Separates knowledge from uncertainty and overconfidence. |
| Not-sure responses | Learner marks an item as uncertain during assessment. | Mirrors Ofstead's uncertainty capture and reduces hidden guessing. |
| High-confidence errors | Incorrect selections with high confidence. | Useful for instructor review because these errors are risky. |
| Low-confidence correct answers | Correct selections with low confidence. | Shows fragile knowledge that may need repetition. |
| Feedback comprehension | Learner can explain at least one error and next step. | Tests whether feedback is actionable, not just visible. |

## Analysis

Report each participant as a paired pre/post comparison:

- pre-test vs post-test accuracy;
- pre-test vs post-test duration;
- pre-test vs post-test total errors;
- error categories by type;
- confidence calibration before and after practice.
- not-sure responses before and after practice, if used.

For a small class demo, use descriptive statistics and participant-level plots
instead of overclaiming statistical significance. If there are enough
participants, report paired differences with confidence intervals.

## Acceptance Bar

The training claim is supported if most learners show:

- higher post-test accuracy;
- equal or lower post-test duration;
- fewer severe errors, especially missing and misidentified items;
- fewer high-confidence errors;
- fewer `Not sure` responses or low-confidence correct answers;
- interview evidence that they can name what they learned or what remains hard.

Mixed results are still useful. For example, accuracy may improve while time
increases, which would mean learners are becoming more careful but not yet more
fluent. That should guide the next module design.

## Tradeoffs And Risks

| Risk | Mitigation |
| --- | --- |
| Practice effect from seeing the same tray twice | Use parallel pre/post trays with the same difficulty and instrument families. |
| Student participants are not SPD technicians | Report novice learning only; run SPD technician validation later. |
| Short-term gain may not persist | Add an Ofstead-style delayed retention check or booster if schedule allows. |
| Learners may memorize screen layout instead of instruments | Randomize item order and use parallel task variants. |
| Feedback could leak assessment answers | Suppress hints and feedback in pre/post modes. |
| Time reduction could hide unsafe guessing | Require accuracy and severe-error reduction alongside speed. |

## Evidence Links

This protocol follows the evidence summarized in
[Training Module Design](../../training_module_design.md):

- SPD training has a real time and supervision burden
  ([HSPA CRCST, accessed 2026](../../../bibliography.md#hspa-crcst-accessed-2026),
  [Chobin, 2010](../../../bibliography.md#chobin-2010)).
- Pre/post testing, hands-on practice, confidence capture, workplace application,
  and delayed booster testing have direct sterile-processing precedent in
  Ofstead et al.'s borescope/endoscope visual-inspection training pilot
  ([Ofstead et al., 2023](../../../bibliography.md#ofstead-et-al-2023)).
- Broader simulation and hands-on practice evidence supports the same training
  direction
  ([AORN Staff, 2025](../../../bibliography.md#aorn-staffing-shortage-2025),
  [Cook et al., 2011](../../../bibliography.md#cook-et-al-2011)).
- Retrieval practice, spacing, and feedback explain why the module uses quiz
  and feedback modes
  ([Roediger and Karpicke, 2006](../../../bibliography.md#roediger-and-karpicke-2006),
  [Dunlosky et al., 2013](../../../bibliography.md#dunlosky-et-al-2013),
  [Hattie and Timperley, 2007](../../../bibliography.md#hattie-and-timperley-2007)).

## What We Are Not Claiming

This experiment does not prove live SPD competence, certification readiness,
reduced hospital onboarding months, reduced OR delays, or lower tray-defect
rates. Those require SPD participants, real workplace tasks, supervisor signoff,
and longitudinal follow-up.
