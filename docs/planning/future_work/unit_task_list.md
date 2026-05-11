# Unit Task List For GitLab Issues

This task list reflects the training-platform pivot. CV experiment tasks have
been retired from the active plan; camera and YOLO code may remain as future
support infrastructure.

## Issue-Sized Task List

### Local Tray Data Ready

- Define the first tray module with 8-12 required instruments.
- Define 3-5 distractors, including at least one lookalike.
- Add instrument names, aliases, families, photos, notes, and distinguishing
  features.
- Add required quantities and tray-template metadata.
- Add module version and source fields.

### Study And Quiz Flow Ready

- Build instrument study-card view.
- Build identification quiz prompts.
- Randomize quiz item and distractor order.
- Record quiz correctness, duration, and confidence.
- Add feedback that explains distinguishing features.

### Practice Sorting Feedback Ready

- Build simulated tray sorting from the local item pool.
- Implement `missing`, `extra`, `wrong`, `misidentified`, and `wrong_count`
  scoring.
- Add immediate feedback in practice mode.
- Show what to review next after each attempt.

### Pre/Post Assessment Ready

- Build pre-test tray sorting with hints and feedback disabled.
- Build post-test tray sorting with comparable difficulty.
- Randomize item order so users cannot memorize screen position.
- Capture accuracy, duration, confidence, and error categories.
- Add a short learner reflection prompt after post-test.

### Metrics Export Ready

- Export learner/session ID, module version, mode, score, duration,
  confidence, and error breakdown.
- Summarize pre/post differences per learner.
- Summarize repeated weak instruments and high-confidence errors.
- Create an instructor/admin-readable example report.

### Literature And Stakeholder Narrative Ready

- Update final presentation language around simulated time-to-competency.
- Cite existing CV papers for feasibility instead of local detector metrics.
- Cite Kienle et al. for cross-manufacturer generalization caution.
- Add stakeholder implications for SPD trainees, hospital administrators, and
  student evaluators.
- Add the non-SPD participant limitation wherever pilot results are reported.

### Pilot Walkthrough Ready

- Write a scripted novice walkthrough.
- Run one pilot and record confusion points.
- Revise the script and UI wording.
- Run additional walkthroughs if time allows.
- Report results as novice learnability, not SPD adoption.
