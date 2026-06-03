# TrayGuard FDR Oral Presentation — Outline & Speaker Script

**Duration**: 20–25 min · **Speakers**: Matthew, Andy, Jacob, Owen, Qiyu (~4–5 min each)

## Rationale

The presentation follows a defensive arc: establish the systemic problem → show why CV alone fails → narrow to what is buildable (training) → prove the prototype works as a feasibility argument → hand off a testable protocol.

1. **Open with data** (slides 1–2) — the problem is real, measured, and recurrent. Establishes stakes.
2. **Deepen the problem** (slides 3–7) — SPD's systemic causes and the broken feedback loop. Training isn't the only gap, but it's the only one a student team can address.
3. **Show our attempt at a technical fix failed** (slides 8–11) — CV experiment results. Honest failure builds credibility and justifies the pivot.
4. **Pivot to training** (slides 12–22) — why training is the right entry point, the prototype design, the measurement apparatus, the validation ladder, the empirical protocol. This is the core of the talk.
5. **Close with the handoff** (slides 23–26) — what we built, what survives, what the next team needs to do. Honest delimitation, not overclaim.

Every design choice in the talk serves one of these five moves. No slide exists for its own sake.

---

## Section 1: Introduction (2 slides, ~1.5 min) — Matthew

---

### Slide 1 — Title

**Visual**: Centered title: *TrayGuard: What We Learned About Why Tray Errors Persist*. Subtitle: EC ENGR 180DW — Final Design Review. Team names listed below.

**Script** _(15 sec)_:

> We're TrayGuard. We spent two quarters looking at why surgical trays arrive wrong or incomplete, and what a team like ours can actually do about it. The answer turned out to be more interesting — and more frustrating — than a camera-based fix.

---

### Slide 2 — The Problem By The Numbers

**Visual**: Three-number callout layout, left to right:

> **9 per 100 cases** — Alfred et al. — 3,900 defects in 41,799 cases, 55% at assembly
>
> **10 min avg delay** — Nichol et al. — 236 errors in 147 cases, $6–9M/yr estimated cost
>
> **44% wrong spec** — Zhu et al. — 398 errors in 33,839 packages

Bottom bold line: *These are recurring, measured operational failures, not isolated accidents.*

**Script** _(45 sec)_:

> Three different methods — tray defect analysis, direct OR observation, package inspection — all find the same thing: instruments are missing, wrong, damaged, or swapped at rates that affect every shift, every hospital. When delays happen, they average 10 minutes per affected case. That doesn't sound huge until you multiply by thousands of cases a year. The largest error category in Zhu's study is "wrong specification" — same instrument family, wrong size or variant. The total count was correct; the specific instrument was wrong. That's a visual discrimination problem, not a counting problem.

**Transition**: *So the question is why. Why does this keep happening across every hospital?*

---

## Section 2: The Problem is Deeper Than a Camera Can See (7 slides, ~6 min) — Andy

---

### Slide 3 — What Tray Reconstruction Actually Requires

**Visual**: Split layout. Left — photo of an SPD assembly station (our surgical kit on a table or a search image). Right — bullet list:

- Identify each instrument by sight (no labels)
- Match against a count sheet with local names
- Distinguish lookalikes (straight vs curved Mayo)
- Check for damage, wear, contamination
- Count correct quantities
- All under production pressure

**Script** _(45 sec)_:

> This is what tray reconstruction looks like. A technician gets a bin of returned instruments — mixed together from the last surgery — and has to identify each one, check for damage, match it to a count sheet that may use local names or outdated photos, and place it in the right tray spot. There are no labels on the instruments. The count sheet might call something "Kelly clamp" when the actual instrument says "Crile" on the original package. And you're doing this under time pressure because the next case is waiting. This is a task that demands detailed visual memory, local knowledge, and sustained attention.

---

### Slide 4 — Six Root Causes

**Visual**: Fishbone diagram. Six branches off the spine labeled:

| Branch | Key point |
|--------|-----------|
| Product | Lookalike instruments, no markings, wear hides differences |
| Knowledge | No recurring competency check, general names ≠ local rules |
| Process | Single-pass assembly with no backup check |
| Information | Outdated count sheets, missing photos, local aliases |
| Environment | Production pressure, interruptions |
| Policy/Feedback | No one owns the standard, slow manual error reporting |

Callout box below fishbone:

> **Three structural drivers:**
> 1. SPD evolved from materials management → no licensure, weak professionalization
> 2. Cost-center accounting → wage investment is visible, error cost is invisible
> 3. No information architecture → downstream OR errors don't trigger upstream correction

**Script** _(90 sec)_:

> We built a fishbone RCA across six categories. The quick version: the instrument itself is hard to identify because similar models differ only in subtle dimensions and markings wear off. The technician needs knowledge — but certification tests once, not repeatedly, and local names vary by hospital. The process has no double-check built in; you pick and check in one step. The count sheet might be outdated or use names nobody agrees on. The environment — production pressure, interruptions — makes detail work harder. And when an error does happen, the feedback loop to correct it is slow and manual.
>
> Underneath all six, three structural drivers explain why these problems persist year after year. Sterile processing evolved from materials management — think hospital supply closet — not from patient care. So there's no individual licensure, no board with enforcement authority, no recurring competency requirement. Hospital accounting treats SPD as a cost center: spending on staff or training shows up as expense, but the cost of errors is invisible. And there's no information system that connects a tray error discovered in the OR back to the specific tray, shift, and training gap that caused it. So the same errors repeat.

---

### Slide 5 — The Broken Feedback Loop

**Visual**: Process flow, left to right:

> **OR finds error** (missing instrument)
> → **Paper incident report** (slow)
> → **Received by SPD weeks later** (delayed)
> → **No tie to specific tray/shift/training gap** (broken link)
> → **Same error repeats**

Below: Quote — *Nichol et al.: "Error reporting is cumbersome, human-dependent, delayed, and incomplete."*

**Script** _(45 sec)_:

> This is the feedback loop that doesn't close. An instrument is missing during surgery. The scrub nurse fills out an incident report — on paper, after the case. That report filters through risk management and reaches SPD management weeks later. By then, nobody can say which tray, which shift, which technician, or which training gap caused it. So nothing changes. The same error repeats next week. Even a perfect detector — one that caught every error at the assembly station — wouldn't fix this broken feedback architecture. It would tell you something was wrong but not why, or who needs help, or whether the count sheet itself is wrong.

---

### Slide 6 — We Evaluated Seven Solution Categories

**Visual**: Table — 7 rows, 4 columns:

| Solution | Buildable? | Validatable? | Creates infra for future? |
|----------|-----------|-------------|-------------------------|
| CV tray checker | No (needs SPD) | No | Maybe |
| Physical error-proofing | No (custom fab) | No | No |
| Workflow redesign | No (policy change) | No | No |
| Decision support | Partial | Partial | Yes (local content) |
| Task simplification | No (hospital data) | No | No |
| Accountability system | No (org policy) | No | No |
| **Training (selected)** | **Yes** | **Yes** | **Yes (module schema)** |

**Script** _(60 sec)_:

> We mapped every intervention category we could find in the literature and industry. Automated tray checking, physical error-proofing like custom foam cutouts, workflow redesign with dual checks, decision-support kiosks at the workstation, tray rationalization, competency tracking systems — every one requires something we don't have. SPD deployment access, policy authority, instrument inventory, hospital utilization data, multi-stakeholder buy-in. Training is the only category that is buildable with printed cards and a laptop, that we can validate with a pre/post study, and that creates durable infrastructure — the local content module — that any future solution would need anyway.

---

### Slide 7 — Why Training, Not Because Training Is a Cure

**Visual**: Two boxes.

Left box — *What training addresses*:
- Measurable local tray knowledge
- Lookalike discrimination practice
- Pre/post learning evidence

Right box — *What training does NOT address*:
- Broken count sheets
- Staffing shortages
- Structural wage / investment problem
- No feedback loop

Bottom line: *Training is a buildable entry point. It is not a complete solution.*

**Script** _(45 sec)_:

> We need to be clear about what training does and doesn't do. A training tool can help a novice practice instrument names, lookalike distinctions, and count-sheet rules. It can produce pre/post evidence of improvement. That's real and measurable. But it won't fix an outdated count sheet. It won't solve staffing shortages, raise wages, or close the feedback loop from the OR. These are structural problems that require organizational and policy change. Training is not a substitute for those. It's the one piece we can build and validate without a hospital partnership. If it works, it gives the next team a reason to tackle the harder pieces. If it doesn't, that's useful evidence too.

**Transition**: *So if training is the entry point, why not build a CV detector as the training tool? We tried that first. Here's what we found.*

---

## Section 3: Why CV Alone Won't Work (5 slides, ~5 min) — Jacob or Owen

---

### Slide 8 — We Ran 7 Staged Detection Experiments

**Visual**: Summary table:

| Experiment | What it tested | Key result |
|-----------|---------------|-----------|
| Bright→dim | Light tolerance | mAP50-95 = 0.781 |
| Matte→reflective | Background transfer | mAP50-95 = 0.759 |
| Separated→overlay | Occlusion | **mAP50-95 = 0.389** |
| Real instruments | Shape vs position | Per-class AP: 0.000–0.862 |

Below: *Lavado baseline (clean dataset): mAP50 = 0.990. Pipeline works — the data doesn't generalize.*

**Script** _(40 sec)_:

> We built a complete YOLO training pipeline. On a clean published dataset — Lavado surgical instruments — we got mAP50 of 0.990. The pipeline works fine. The problem is what happens when you test on conditions that SPD workstations actually present. We ran seven staged experiments isolating brightness, background reflectivity, and layout occlusion. Every variation cost accuracy. The biggest drop — overlay layout, which simulates instruments touching in a tray — produced mAP50-95 of 0.389.

---

### Slide 9 — Brightness Degradation

**Visual**: *brightness_map50_95_panels.png* (two-panel plot, dark→bright and bright→dark).

**Script** _(40 sec)_:

> This plot shows what happens as the light gap widens. Left panel: trained on darkest, tested on brighter levels. Right panel: trained on brightest, tested on dimmer. The farther the gap, the worse the accuracy. SPD lighting varies by workstation, time of day, fixture condition. Every variation costs you detection reliability. This is not a solvable problem with more training data alone — you'd need to characterize and cover every lighting condition at every workstation.

---

### Slide 10 — Occlusion Is the Dealbreaker

**Visual**: Side by side — *separated_layout_example.jpg* (left) and *overlay_layout_example.jpg* (right). Below: *overlay_map50_95.png* showing the drop.

**Script** _(40 sec)_:

> This is the most telling experiment. Left: separated layout — what you'd train on. Right: overlay — what a real tray looks like. Instruments in a tray touch and overlap. When we trained separated and tested on overlay, mAP50-95 dropped from 0.995 to 0.389. That means every time instruments overlap — which is most of the time in a real tray — the detector can't reliably tell what's there. You'd need to ask the technician to stop and rearrange before scanning, which defeats the purpose of an automated check.

---

### Slide 11 — Real Instruments: The Model Learned Position, Not Shape

**Visual**: Two figures side by side. Left: *confusion_matrix_normalized.png*. Right: *val_batch0_pred.jpg* (only scalpel detected).

Below: per-class breakdown table:

| Split | Surviving classes | Zero AP classes |
|-------|------------------|----------------|
| Matte→reflective | scissor2, forcep, scalpel | scissor1/3/4 |
| Reflective→matte | **scalpel only** | scissor1/2/3/4, forcep |
| Shape similarity | scissor1, scissor4 | scissor2/3, forcep |

**Script** _(60 sec)_:

> This is the diagnostic result. We tested six real instrument classes — four scissors, a forcep, a scalpel. Per-class AP ranges from 0.000 to 0.862 depending on which split you look at. Different classes survive in different splits. The only class that transfers reliably is the scalpel — the most visually distinct instrument with a single blade versus multi-loop scissors.
>
> The pattern is caused by position-cue confounding. Each image has exactly one of each class at fixed positions per session. The model memorizes which class appears at which image location. When the position changes — which happens every time you process a different tray — the model fails. This isn't a problem you can fix with more data alone. You need randomized positions, which means a completely different data collection protocol.

---

### Slide 12 — The Cumulative Lesson: CV Validation Burden

**Visual**: List, each with red ✗:

- Site-specific training data (instruments, lighting, layouts) ✗
- Cross-manufacturer validation (Kienle: major performance drop) ✗
- Open-set rejection (unknown objects = false positives) ✗
- Human-in-the-loop for every uncertain case ✗
- Workflow integration in live SPD (never tested) ✗
- Regulatory / device policy / privacy review ✗

Bottom: *The training path doesn't need any of this for a first study.*

**Script** _(40 sec)_:

> The cumulative evidence is clear: CV detection works in matched, controlled conditions and degrades under every variation that SPD workflows present. A deployment-grade system would need site-specific data for every hospital, cross-manufacturer validation because Kienle showed big drops between brands, open-set rejection for unknown objects, human-in-the-loop for every uncertain case, workflow integration testing, and regulatory review. We cannot responsibly build that in a one-quarter project. The pivot to a training path was driven by this evidence, not by convenience.

**Transition**: *So if CV can't get us there alone, and training is the entry point — what exactly did we design?*

---

## Section 4: Why Training Is the Best Entry Point (7 slides, ~5.5 min) — Matthew

---

### Slide 13 — CV and Training Are Complementary

**Visual**: Flow diagram. Center box: *Local Tray Module* (names, aliases, counts, lookalikes, photos, variants). Two arrows out:

- Left arrow → *Training loop (now)* → Pre-test → Study → Quiz → Practice → Post-test → Evidence
- Right arrow → *Future CV system* — needs exactly the same data

Bottom: *The module is the durable artifact. Training proves the module works. The module then enables CV.*

**Script** _(45 sec)_:

> Here's the key insight. Building a CV tray checker without this training layer means you don't have ground truth. You don't know the correct instrument names, the correct aliases, the lookalike pairs, the tray-specific counts. The training loop builds and validates all of that at low cost, with printed cards and a laptop. Once you have a validated module — instructor-approved names, tested lookalike pairs, measured error categories — that same data feeds any future CV system. The training loop and CV are not competing approaches. The training loop creates the prerequisite infrastructure.

---

### Slide 14 — The Durable Design Artifact: Tray Module Schema

**Visual**: Snippet of JSON:

```json
{
  "id": "mayo_scissors_straight_55",
  "display_name": "Straight Mayo scissors, 5.5 in",
  "aliases": ["straight Mayo", "suture scissors"],
  "distinguishing_features": ["Heavy straight blades"],
  "common_confusions": ["mayo_scissors_curved_55"],
  "apriltag_id": 12,
  "study_prompts": [
    {"prompt": "Name this instrument.", "answer": "Straight Mayo scissors"},
    {"prompt": "Distinguishing feature?", "answer": "Heavier, broader blades"}
  ]
}
```

Callout: *Mirrors real count-sheet fields: reference number, description, location, quantity, check box.*

**Script** _(45 sec)_:

> This is the durable output. A file-backed tray module that defines what instruments belong in a tray, what they're called locally, what they're confused with, and how to assess them. The fields mirror real count-sheet structure — Stryker's published count sheets use tray name, reference number, description, location, quantity, check box. Our module adds learning-specific fields: aliases, lookalike pairs, study prompts, confidence tracking. The software prototype we built is throwaway — any future team will choose their own stack. But this schema captures the local tray knowledge that any solution needs. That's what survives.

---

### Slide 15 — Printed Cards: How It Works Physically

**Visual**: Side-by-side card images (or physical prop held up):

- Left: card front — AprilTag pattern, no text (neutral assessment front)
- Right: card back — instrument name, aliases, distinguishing features

Below: *Neutral front prevents answer leakage during assessment. Tag ID maps to instrument ID in the module.*

**Script** _(30 sec)_:

> Each instrument gets a printed card. The front has an AprilTag marker — no text, so during a test the learner can't read the answer off the card. The back has the name, aliases, and features for study mode. The tag ID maps to an instrument ID through the module. The learner places cards on a table, the camera detects which tags are there, and the scoring engine compares their selection against the tray template.

---

### Slide 16 — The Scoring Architecture: 5 Error Categories

**Visual**: Table with examples:

| Category | Definition | Example |
|----------|-----------|---------|
| Correct | Right item, right count | Selected 1 scalpel handle ✓ |
| Missing | Required item not selected | Didn't select Kelly clamp |
| Wrong | Item not on the tray list | Selected a retractor not in this tray |
| Extra | Distractor selected | Selected an item from a different tray |
| Misidentified | Right class, wrong variant | Curved Mayo instead of straight |
| Wrong count | Right item, wrong quantity | 2 Kellys when tray needs 4 |

**Script** _(50 sec)_:

> The scoring engine classifies every selection into six categories. These map directly to the error categories in the literature. Zhu's packaging study found 44% were wrong specification — that's our misidentified category. Alfred found missing, wrong, extra, and damaged — we have all of those. Nichol found that lookalike substitution is a distinct error pattern — our misidentified category captures that separately from generic "wrong." When a learner improves from pre-test to post-test, we can say which type of error they reduced. That's more informative than a single accuracy number.

---

### Slide 17 — Confidence Capture

**Visual**: Mockup of a confidence slider (1–5 scale) with *Not sure* checkbox. Two callouts:

- *High-confidence error: learner was sure but wrong — overconfidence, needs targeted feedback*
- *Low-confidence correct: learner was unsure but right — fragile knowledge, needs reinforcement*

**Script** _(30 sec)_:

> After each tray sort, the learner rates their confidence. This separates two very different failure modes. A high-confidence error means someone is confidently wrong — that's the hardest type to correct because the learner doesn't know they need help. Low-confidence correct means fragile knowledge that might not survive a week without review. Both are visible in the export.

---

### Slide 18 — The Learning Loop (7 Steps)

**Visual**: Flow diagram, step by step:

> 1. Pre-test (no hints, no feedback) → baseline accuracy
> 2. Study cards (prompt-before-reveal) → retrieval practice
> 3. Quiz (timed, with confidence) → identify weak items
> 4. Practice tray sort (with feedback) → deliberate practice
> 5. Weak-item review (if needed) → targeted re-study
> 6. Post-test (parallel variant, no hints) → learning evidence
> 7. Export (CSV/JSON) → instructor-facing metrics

**Script** _(45 sec)_:

> This is the full learner loop. Each step has a specific evidence-based role. The pre-test and post-test use parallel variants — same instrument families, different specific items — so the learner can't memorize the exact layout. Study cards are prompt-before-reveal: the learner commits to an answer before seeing it, which is retrieval practice, not passive review. The practice sort gives immediate error-category feedback — "you missed the Kelly clamp," "you selected curved instead of straight Mayo." The whole loop takes about 45 to 60 minutes for a first module.

---

### Slide 19 — The Research Question

**Visual**: Centered, large text:

> *How can a local tray training and assessment system help novice users improve their ability to detect missing, wrong, extra, misidentified, or miscounted instruments before supervised SPD tray-reconstruction work?*

Below: *That question is narrow, testable, and honest about what we can and cannot claim.*

**Script** _(15 sec)_:

> That's the research question this design answers. It's not "does TrayGuard reduce OR delays." It's not "does TrayGuard certify competence." It's: can a novice improve on a simulated local tray task after retrieval-centered practice? That's a question we can answer.

**Transition**: *And here's exactly how to answer it.*

---

## Section 5: What a Future Team Should Do (5 slides, ~4 min) — Qiyu

---

### Slide 20 — The Study Ladder

**Visual**: Five-level staircase, simple labeled boxes:

| Level | Study | Participants | Validates |
|-------|-------|-------------|-----------|
| 5 | SPD pilot | SPD trainees/techs | Behavioral transfer |
| 4 | Expert review | 1 SPD educator | Content validity |
| 3 | Delayed retention | Same novices, 7d later | Temporal persistence |
| 2 | Novice study | 8–12 novices | Learning mechanism |
| 1 | Marker reliability | Project members | Measurement tool |

Callout: *Kirkpatrick Level 2 target. Level 3 and 4 require future validation.*

**Script** _(50 sec)_:

> We designed a five-step study ladder. Each step validates a different piece of the evidence chain, and each step depends on the one before it. Step 1 — marker reliability — makes sure the cards scan correctly so app errors don't look like learner errors. Step 2 — the novice study — tests whether the learning mechanism works at all. Step 3 checks whether gains persist after 7 days — because same-day improvement is not retention. Step 4 brings in an expert to review whether our names, counts, and lookalike pairs make sense. Only after all four should someone invest in Step 5 — an SPD pilot. The current evidence supports starting at Step 1 and 2.

---

### Slide 21 — Study 1: Novice Pre/Post Design

**Visual**: Timeline table:

| Segment | Time | Activity |
|---------|------|----------|
| Consent + intake | 3–5 min | Background, explain study |
| Pre-test tray sort | 5–8 min | No hints, no feedback |
| Retrieval cards | 10–12 min | Prompt-before-reveal study |
| Quiz | 5–8 min | With confidence capture |
| Practice sort | 8–10 min | With error-category feedback |
| Post-test | 5–8 min | Parallel variant, no hints |
| Photo-ID test | 5–7 min | Convergent validity measure |

**Script** _(40 sec)_:

> The novice study uses a within-subject pre/post design, 8–12 participants with no SPD experience. One 60-minute session per person. Primary measures are pre/post accuracy, error-category counts, duration, and confidence calibration. We also include a convergent photo-ID test — learners identify instruments from photos without the tray context. If tray-sort accuracy correlates with photo-ID accuracy at r ≥ 0.50, we have evidence that the tray scores reflect instrument knowledge, not task-specific familiarity.

---

### Slide 22 — Study 2: Delayed Retention (The Falsification Criterion)

**Visual**: Three-outcome diagram:

> Pre-test (30%) → Post-test (85%) → 7 days later → ???
>
> ├─ ≥50% of gain retained → learning persists
> ├─ ≤5 pp above baseline → practice effect only
> └─ <50% of gain retained → partial decay

**Script** _(45 sec)_:

> A same-day post-test can't be called retention. Bell et al. showed medical-knowledge gains can decay measurably within 7 days. So we require a 7-day delayed check with explicit falsification criteria. The retention claim is supported only if three conditions are met: delayed accuracy retains at least half the immediate gain, it stays at least 5 percentage points above baseline, and at least 70% of participants come back. If these fail, the project claim reverts to "immediate learning only." This is an honest go/no-go — we specify upfront what would falsify our claim.

---

### Slide 23 — Study 3: Expert Review (Closing the Content Gap)

**Visual**: Checklist of what the expert reviews:

- Instrument names and aliases — correct for local practice?
- Required counts and distractors — plausible for training?
- Lookalike pairs — educationally meaningful?
- Feedback messages — misleading or safe?
- Weak-item report — would it help target coaching?

**Script** _(30 sec)_:

> The main weakness of a student-built module is content validity. We don't work in an SPD. An instructor or SPD educator needs to review names, counts, distractors, lookalike pairs, and feedback language. If they say the module is plausible, we can proceed to an SPD pilot. If they find problems, we fix those before testing with real trainees.

---

### Slide 24 — Go/No-Go Decision for Future Team

**Visual**: Decision flowchart (simplified):

> Study 1 + 2 pass? (learning + retention)
>
> ├─ Yes → Study 3 (expert review) → positive? → SPD pilot warranted
> └─ No → Report "learning mechanism works but retention fails"
>        → Reconsider whether single-session training is sufficient

**Script** _(30 sec)_:

> This is the decision framework we leave the next team. If the novice study shows learning and the 7-day check shows retention, and an expert confirms the content is plausible, then investing in an SPD pilot is justified. If the novice study fails — if the measurement tool doesn't work, or novices don't improve — then the problem may be harder than training alone can solve, and that's a useful finding too.

**Transition**: *So what should the audience actually take away from all of this?*

---

## Section 6: Conclusion (2 slides, ~1.5 min) — All

---

### Slide 25 — What We Know and What We Don't

**Visual**: Two columns:

| What we know | What we can't claim (yet) |
|-------------|--------------------------|
| Tray errors are systemic, recurring, and well-documented | Training transfers to real SPD work |
| CV alone can't solve this — the validation burden is too high | System works for experienced technicians |
| Training is the buildable entry point | It reduces OR delays |
| The module schema is durable infrastructure | CV is deployment-ready |
| The study ladder has falsification criteria | Same-day gains persist (Study 2 tests this) |

**Script** _(40 sec)_:

> This sums up what we actually accomplished. We did not build a deployable product. We built an evidence-backed argument for what the right starting point is, designed the measurement and validation infrastructure, and left the next team with a testable protocol.

---

### Slide 26 — The Honest Handoff

**Visual**: Centered quote, large:

> *Our project found that this problem is harder and more systemic than any single technical fix can address. Our contribution is documenting why, and giving the next team a validated starting point — not a finished product.*

Below: *The study is designed. The module schema is defined. The scoring is tested. Run the study.*

**Script** _(45 sec)_:

> We started this project thinking we'd build a camera that catches tray errors. We ended up understanding that tray errors are a system problem — rooted in how the SPD workforce is structured, funded, and connected to the OR. A camera can't fix a broken feedback loop. Training alone can't fix wage stagnation or staffing shortages. But a training loop can create the local content infrastructure that every future solution needs, and it can produce the first piece of measurable evidence.
>
> Our honest recommendation: take the module schema, the study protocol, and the falsification criteria we designed. Run the novice study. If it works, the SPD pilot is the next question. If it doesn't, the problem is even harder than we thought — and that's useful to know too.
>
> Thank you. Questions.

---

## Appendix: Figure / Asset Checklist

| Slide | Figure | Source | Status |
|-------|--------|--------|--------|
| 2 | Error rate callout (3-number layout) | New — text slide | To create |
| 3 | SPD workstation photo | Search image or our kit | To source |
| 4 | Simplified fishbone diagram | New — diagram | To draw |
| 4 | Structural drivers callout box | New — text | To create |
| 5 | Broken feedback loop flow | New — diagram | To draw |
| 6 | 7-solution comparison table | New — text | To create |
| 7 | Training scope boxes | New — text | To create |
| 8 | CV experiment summary table | New — text | To create |
| 9 | Brightness degradation plot | `brightness_map50_95_panels.png` | Exists |
| 10 | Separated vs overlay example | `separated_layout_example.jpg`, `overlay_layout_example.jpg` | Exists |
| 10 | Overlay degradation plot | `overlay_map50_95.png` | Exists |
| 11 | Confusion matrix | `confusion_matrix_normalized.png` | Exists |
| 11 | Prediction example | `val_batch0_pred.jpg` | Exists |
| 11 | Per-class AP table | New — text | To create |
| 12 | CV validation burden list | New — text | To create |
| 13 | CV + training complementary flow | New — diagram | To draw |
| 14 | JSON schema snippet | New — render | To create |
| 15 | Card front/back images | Generated cards exist | To photograph |
| 16 | Error category table | New — text | To create |
| 17 | Confidence mockup | New — simple UI mockup | To create |
| 18 | 7-step learning loop flow | New — diagram | To draw |
| 19 | Research question centered text | New — text | To create |
| 20 | Study ladder staircase | New — diagram | To draw |
| 21 | Study 1 timeline table | New — text | To create |
| 22 | Retention outcome diagram | New — diagram | To draw |
| 23 | Expert review checklist | New — text | To create |
| 24 | Go/no-go flowchart | New — diagram | To draw |
| 25 | Know / don't know table | New — text | To create |
| 26 | Honest handoff quote | New — text | To create |

### Diagrams to create (requires tool)

1. **Fishbone diagram** (Slide 4) — 6 branches + structural driver callout
2. **Broken feedback loop** (Slide 5) — 5-step flow with arrows
3. **CV + training complementary** (Slide 13) — center box, two arrows
4. **7-step learning loop** (Slide 18) — sequential flow
5. **Study ladder staircase** (Slide 20) — 5 stacked levels
6. **Retention outcomes** (Slide 22) — three branch decision
7. **Go/no-go flowchart** (Slide 24) — two branch decision

### Timing summary

| Section | Slides | Time | Speaker |
|---------|--------|------|---------|
| 1. Introduction | 2 | 1:00 min | Matthew |
| 2. Systemic problem | 7 | 6:00 min | Andy |
| 3. CV experiments | 5 | 5:00 min | Jacob/Owen |
| 4. Training design | 7 | 5:30 min | Matthew |
| 5. Future work | 5 | 4:00 min | Qiyu |
| 6. Conclusion | 2 | 1:30 min | All |
| **Total** | **26** | **~23:00** | — |
| Buffer / Q&A | — | ~2:00 | — |
