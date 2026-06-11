# TrayGuard: What We Learned About Why Tray Errors Persist

### Slide 1 — Title - Qiyu

**Script** _(15 sec)_:

> We're TrayGuard. We spent two quarters looking at why surgical trays arrive wrong or incomplete, and what a team like ours can actually do about it. The answer turned out to be more interesting — and more frustrating — than a camera-based fix.

---

### Slide 2 — Roadmap - Qiyu

> Outline of the presentation: The Problem → CV Experiments → Solution Evaluation → Training Design → Future Work → Conclusion

---

### Slide 3 — The Problem - Qiyu, Matthew

---

### Slide 4 — The Problem By The Numbers - Qiyu

**Script** _(45 sec)_:

> Three different methods — tray defect analysis, direct OR observation, package inspection — all find the same thing: instruments are missing, wrong, damaged, or swapped at rates that affect every shift, every hospital. When delays happen, they average 10 minutes per affected case. That doesn't sound huge until you multiply by thousands of cases a year. The largest error category in Zhu's study is "wrong specification" — same instrument family, wrong size or variant. The total count was correct; the specific instrument was wrong. That's a visual discrimination problem, not a counting problem.

---
### Slide 5 — Why Tray Errors Persist  - Qiyu

---


### Slide 6 — Lookalike Instruments: Kelly vs Crile - Qiyu

**Script** _(45 sec)_:

> This is the core of the lookalike problem. Kelly and Crile forceps are in the same family — both hemostatic clamps with transverse serrations. But they differ in where those serrations run: Crile serrations cover the entire jaw length; Kelly serrations only cover the distal half. You can't tell them apart at a glance. And within each type, sizes vary — 6 inch, 7 inch, 8 inch. In Zhu's study, the most common error category was "wrong specification": a package calling for four 14cm Kelly clamps and two 16cm Kelly clamps might end up with the counts swapped. Total number correct, specific instrument wrong. That's a visual discrimination failure that a camera can't reliably catch, and that training can directly address.

---

### Slide 7 — What Tray Reconstruction Actually Requires - Qiyu

**Script** _(45 sec)_:

> This is what tray reconstruction looks like. A technician gets a bin of returned instruments — mixed together from the last surgery — and has to identify each one, check for damage, match it to a count sheet that may use local names or outdated photos, and place it in the right tray spot. There are no labels on the instruments. The count sheet might call something "Kelly clamp" when the actual instrument says "Crile" on the original package. And you're doing this under time pressure because the next case is waiting. This is a task that demands detailed visual memory, local knowledge, and sustained attention.

---

### Slide 8 — Common Surgical Instruments - Qiyu

**Script** _(30 sec)_:

> This figure shows the major categories of surgical instruments found in a typical SPD: clamps, forceps, scissors, retractors, needle holders, and other specialty tools. Each category has multiple sub-types with subtle visual differences — jaw shape, serration pattern, length, tip geometry. These are the distinctions that SPD technicians must make by sight during tray reconstruction, and they are exactly the kind of lookalike discriminations that our training intervention targets.

---

### Slide 9 — RCA - Jacob

**Script** _(45 sec)_:

> We built a fishbone RCA across six categories. The quick version: the instrument itself is hard to identify because similar models differ only in subtle dimensions and markings wear off. The technician needs knowledge — but certification tests once, not repeatedly, and local names vary by hospital. The process has no double-check built in; you pick and check in one step. The count sheet might be outdated or use names nobody agrees on. The environment — production pressure, interruptions — makes detail work harder. And when an error does happen, the feedback loop to correct it is slow and manual.


### Slide 10 — Three Structural Drivers - Jacob

**Script** _(45 sec)_:

> Underneath all six, three structural drivers explain why these problems persist year after year. Sterile processing evolved from materials management — think hospital supply closet — not from patient care. So there's no individual licensure, no board with enforcement authority, no recurring competency requirement. Hospital accounting treats SPD as a cost center: spending on staff or training shows up as expense, but the cost of errors is invisible. And there's no information system that connects a tray error discovered in the OR back to the specific tray, shift, and training gap that caused it. So the same errors repeat.

---

### Slide 11 — The Broken Feedback Loop - Jacob

**Script** _(45 sec)_:

> This is the feedback loop that doesn't close. An instrument is missing during surgery. The scrub nurse fills out an incident report — on paper, after the case. That report filters through risk management and reaches SPD management weeks later. By then, nobody can say which tray, which shift, which technician, or which training gap caused it. So nothing changes. The same error repeats next week. Even a perfect detector — one that caught every error at the assembly station — wouldn't fix this broken feedback architecture. It would tell you something was wrong but not why, or who needs help, or whether the count sheet itself is wrong.

---

### Slide 12 — CV Attempt - Andy

---

### Slide 13 — First CV Attempt: One Detector Did Everything - Andy

---

### Slide 14 — The Problem Was Fine-Grained Confusion, Not Just Detection - Andy

---

### Slide 15 — Second CV Attempt: Coarse-to-Fine 2-Stage Pipeline - Andy

---

### Slide 16 — Testing the 2-Stage Demo on Separated Images - Andy

---

### Slide 17 — 2-Stage Helped, But Scissor ID Still Failed - Andy

---

### Slide 18 — Why CV Alone Won't Work - Andy

---

### Slide 19 — We Ran 7 Staged Detection Experiments - Andy

**Script** _(40 sec)_:

> We built a complete YOLO training pipeline. On a clean published dataset — Lavado surgical instruments — we got mAP50 of 0.990. The pipeline works fine. The problem is what happens when you test on conditions that SPD workstations actually present. We ran seven staged experiments isolating brightness, background reflectivity, and layout occlusion. Every variation cost accuracy. The biggest drop — overlay layout, which simulates instruments touching in a tray — produced mAP50-95 of 0.389.

---

### Slide 20 — Brightness Degradation - Andy

**Script** _(40 sec)_:

> This plot shows what happens as the light gap widens. Left panel: trained on darkest, tested on brighter levels. Right panel: trained on brightest, tested on dimmer. The farther the gap, the worse the accuracy. SPD lighting varies by workstation, time of day, fixture condition. Every variation costs you detection reliability. This is not a solvable problem with more training data alone — you'd need to characterize and cover every lighting condition at every workstation.

---

### Slide 21 — Occlusion Is the Dealbreaker (layout comparison) - Andy

**Script** _(20 sec)_:

> Left: separated layout — what you'd train on. Right: overlay — what a real tray looks like. Instruments in a tray touch and overlap.

---

### Slide 22 — Overlay Degradation - Andy

**Script** _(20 sec)_:

> When we trained separated and tested on overlay, mAP50-95 dropped from 0.995 to 0.389. That means every time instruments overlap — which is most of the time in a real tray — the detector can't reliably tell what's there. You'd need to ask the technician to stop and rearrange before scanning, which defeats the purpose of an automated check.

---

### Slide 23 — Real Instruments: The Model Learned Position, Not Shape - Andy

**Script** _(60 sec)_:

> This is the diagnostic result. We tested six real instrument classes — four scissors, a forcep, a scalpel. Per-class AP ranges from 0.000 to 0.862 depending on which split you look at. Different classes survive in different splits. The only class that transfers reliably is the scalpel — the most visually distinct instrument with a single blade versus multi-loop scissors. The pattern is caused by position-cue confounding. Each image has exactly one of each class at fixed positions per session. The model memorizes which class appears at which image location. When the position changes — which happens every time you process a different tray — the model fails. This isn't a problem you can fix with more data alone. You need randomized positions, which means a completely different data collection protocol.

---

### Slide 24 — The Cumulative Lesson: CV Validation Burden - Andy

**Script** _(40 sec)_:

> The cumulative evidence is clear: CV detection works in matched, controlled conditions and degrades under every variation that SPD workflows present. A deployment-grade system would need site-specific data for every hospital, cross-manufacturer validation because Kienle showed big drops between brands, open-set rejection for unknown objects, human-in-the-loop for every uncertain case, workflow integration testing, and regulatory review. We cannot responsibly build that in a one-quarter project. The pivot to a training path was driven by this evidence, not by convenience.

---

### Slide 25 — We Evaluated Seven Solution Categories - Jacob

**Script** _(60 sec)_:

> We mapped every intervention category we could find in the literature and industry. Automated tray checking, physical error-proofing like custom foam cutouts, workflow redesign with dual checks, decision-support kiosks at the workstation, tray rationalization, competency tracking systems — every one requires something we don't have. SPD deployment access, policy authority, instrument inventory, hospital utilization data, multi-stakeholder buy-in. Training is the only category that is buildable with printed cards and a laptop, that we can validate with a pre/post study, and that creates durable infrastructure — the local content module — that any future solution would need anyway.

---

### Slide 26 — Why Training, Not Because Training Is a Cure - Jacob

**Script** _(45 sec)_:

> We need to be clear about what training does and doesn't do. A training tool can help a technician — even one who passed certification — practice the local instrument names, lookalike distinctions, and count-sheet rules that no exam covers. It can produce pre/post evidence of improvement. That's real and measurable. But it won't fix an outdated count sheet. It won't solve staffing shortages, raise wages, or close the feedback loop from the OR. These are structural problems that require organizational and policy change. Training is not a substitute for those. It's the one piece we can build and validate without a hospital partnership. If it works, it gives the next team a reason to tackle the harder pieces. If it doesn't, that's useful evidence too.

---

### Slide 27 — Why Training Is the Best Entry Point - Matthew

---

### Slide 28 — CV and Training Are Complementary - Matthew

**Script** _(45 sec)_:

> Here's the key insight. Building a CV tray checker without this training layer means you don't have ground truth. You don't know the correct instrument names, the correct aliases, the lookalike pairs, the tray-specific counts. The training loop builds and validates all of that at low cost, with printed cards and a laptop. Once you have a validated module — instructor-approved names, tested lookalike pairs, measured error categories — that same data feeds any future CV system. The training loop and CV are not competing approaches. The training loop creates the prerequisite infrastructure.

---

### Slide 29 — The Durable Design Artifact: Tray Module Schema - Matthew

**Script** _(45 sec)_:

> This is the durable output. A file-backed tray module that defines what instruments belong in a tray, what they're called locally, what they're confused with, and how to assess them. The fields mirror real count-sheet structure — Stryker's published count sheets use tray name, reference number, description, location, quantity, check box. Our module adds learning-specific fields: aliases, lookalike pairs, study prompts, confidence tracking. The software prototype we built is throwaway — any future team will choose their own stack. But this schema captures the local tray knowledge that any solution needs. That's what survives.

---

### Slide 30 — Printed Cards: How It Works Physically - Matthew

**Script** _(30 sec)_:

> Each instrument gets a printed card. The front has an AprilTag marker — no text, so during a test the learner can't read the answer off the card. The back has the name, aliases, and features for study mode. The tag ID maps to an instrument ID through the module. The learner places cards on a table, the camera detects which tags are there, and the scoring engine compares their selection against the tray template.

---

### Slide 31 — The Scoring Architecture: 5 Error Categories - Matthew

**Script** _(50 sec)_:

> The scoring engine classifies every selection into six categories. These map directly to the error categories in the literature. Zhu's packaging study found 44\% were wrong specification — that's our misidentified category. Alfred found missing, wrong, extra, and damaged — we have all of those. Nichol found that lookalike substitution is a distinct error pattern — our misidentified category captures that separately from generic "wrong." When a learner improves from pre-test to post-test, we can say which type of error they reduced. That's more informative than a single accuracy number.

---

### Slide 32 — Confidence Capture - Matthew

**Script** _(30 sec)_:

> After each tray sort, the learner rates their confidence. This separates two very different failure modes. A high-confidence error means someone is confidently wrong — that's the hardest type to correct because the learner doesn't know they need help. Low-confidence correct means fragile knowledge that might not survive a week without review. Both are visible in the export.

---

### Slide 33 — The Learning Loop (7 Steps) - Matthew

**Script** _(45 sec)_:

> This is the full learner loop. Each step has a specific evidence-based role. The pre-test and post-test use parallel variants — same instrument families, different specific items — so the learner can't memorize the exact layout — Arthur et al. found that pre/post evaluation is the standard training assessment design . Study cards are prompt-before-reveal: the learner commits to an answer before seeing it, which is retrieval practice, not passive review — Karpicke \& Blunt and Roediger \& Karpicke found retrieval practice doubles long-term retention over re-study . The practice sort gives immediate error-category feedback — "you missed the Kelly clamp," "you selected curved instead of straight Mayo" — Hattie \& Timperley found the most effective feedback is task-specific and immediate . The whole loop takes about 45 to 60 minutes for a first module.

---

### Slide 34 — The Research Question - Matthew

**Script** _(15 sec)_:

> That's the research question this design answers. It's not "does TrayGuard reduce OR delays." It's not "does TrayGuard certify competence." It's: can a technician who holds certification — but has never seen this hospital's specific trays — improve on a simulated local tray task after retrieval-centered practice? That's a question we can answer.

---

### Slide 35 — What a Future Team Should Do - Matthew

---

### Slide 36 — The Study Ladder - Matthew

**Script** _(50 sec)_:

> We designed a five-step study ladder. Each step validates a different piece of the evidence chain, and each step depends on the one before it. Step 1 — marker reliability — makes sure the cards scan correctly so app errors don't look like learner errors. Step 2 — the baseline study — validates the measurement instrument before we invest in a technician pilot. Step 3 checks whether gains persist after 7 days — because same-day improvement is not retention. Step 4 brings in an expert to review whether our names, counts, and lookalike pairs make sense. Only after all four should someone invest in Step 5 — an SPD pilot. The current evidence supports starting at Step 1 and 2.

---

### Slide 37 — Study 1: Novice Pre/Post Design - Matthew

**Script** _(40 sec)_:

> The baseline study uses a within-subject pre/post design with 8--12 participants as a conservative proxy. One 60-minute session per person. Primary measures are pre/post accuracy, error-category counts, duration, and confidence calibration. We also include a convergent photo-ID test — learners identify instruments from photos without the tray context. If tray-sort accuracy correlates with photo-ID accuracy at r $\ge$ 0.50, we have evidence that the tray scores reflect instrument knowledge, not task-specific familiarity.

---

### Slide 38 — Study 2: Delayed Retention (The Falsification Criterion) - Matthew

**Script** _(45 sec)_:

> A same-day post-test can't be called retention. Bell et al. found knowledge decay was detectable within 7 days in a physician online tutorial . So we require a 7-day delayed check with explicit falsification criteria. The retention claim is supported only if three conditions are met: delayed accuracy retains at least half the immediate gain, it stays at least 5 percentage points above baseline, and at least 70\% of participants come back. If these fail, the project claim reverts to "immediate learning only." This is an honest go/no-go — we specify upfront what would falsify our claim.

---

### Slide 39 — Study 3: Expert Review (Closing the Content Gap) - Matthew

**Script** _(30 sec)_:

> The main weakness of a student-built module is content validity. We don't work in an SPD. An instructor or SPD educator needs to review names, counts, distractors, lookalike pairs, and feedback language. If they say the module is plausible, we can proceed to an SPD pilot. If they find problems, we fix those before testing with real trainees.

---

### Slide 40 — Go/No-Go Decision for Future Team - Matthew

**Script** _(30 sec)_:

> This is the decision framework we leave the next team. If the baseline study validates the measurement instrument and the 7-day check shows retention, and an expert confirms the content is plausible, then investing in an SPD technician pilot is justified. If the baseline study fails — if the measurement tool doesn't work, or participants don't improve — then the problem may be harder than training alone can solve, and that's a useful finding too.

---

## Section 4: Future Work and Conclusion (11 slides) — Matthew

---

### Slide 41 — Conclusion - Matthew

---

### Slide 42 — What We Know and What We Don't - Matthew

**Script** _(40 sec)_:

> This sums up what we actually accomplished. We did not build a deployable product. We built an evidence-backed argument for what the right starting point is, designed the measurement and validation infrastructure, and left the next team with a testable protocol.

---

### Slide 43 — The Honest Handoff - Matthew

**Script** _(45 sec)_:

> We started this project thinking we'd build a camera that catches tray errors. We ended up understanding that tray errors are a system problem — rooted in how the SPD workforce is structured, funded, and connected to the OR. A camera can't fix a broken feedback loop. Training alone can't fix wage stagnation or staffing shortages. But a training loop can create the local content infrastructure that every future solution needs, and it can produce the first piece of measurable evidence.
>
> Our honest recommendation: take the module schema, the study protocol, and the falsification criteria we designed. Run the baseline study. If it validates the instrument, the SPD technician pilot is the next question. If it doesn't, the problem is even harder than we thought — and that's useful to know too.
>
> Thank you. Questions.

---

### Slide 44 — References

**Script** _(30 sec)_:

> References cited in this presentation, with slide numbers:
> - Alfred et al. (2021) — Sl. 31
> - Arthur et al. (2003) — Sl. 33
> - Bell et al. (2008) — Sl. 38
> - Hattie & Timperley (2007) — Sl. 33
> - Karpicke & Blunt (2011) — Sl. 33
> - Kienle et al. (2025) — Sl. 25
> - Nichol et al. (2024) — Sl. 4, 31
> - Roediger & Karpicke (2006) — Sl. 33
> - Zhu et al. (2019) — Sl. 4, 6, 31
