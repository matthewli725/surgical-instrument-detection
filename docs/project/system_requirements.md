# TrayGuard System Requirements

## Purpose

This document replaces the qualitative prototype requirements with measurable
requirements for the training project. The requirements start from the root-cause
analysis problem frame:

> Surgical instrument sets are not reliably complete, correct, functional,
> sterile, and available at the point of use.

TrayGuard cannot prove live SPD readiness in the current project. It can prove a narrower
learning claim: novices can practice one local tray module and show measurable
improvement on a comparable simulated tray-sorting post-test.

## Evidence-To-Metric Basis

| Evidence | Requirement Implication |
| --- | --- |
| HSPA requires 400 hands-on CRCST hours, including 120 hours in preparing and packaging instruments ([HSPA CRCST, accessed 2026](../bibliography.md#hspa-crcst-accessed-2026)). | The training project must be framed as practice evidence, not certification or workplace sign-off. |
| Alfred et al. found 3900 tray defects across 41,799 cases; 55.0% occurred during assembly, with missing, wrong, damaged, extra, and incorrectly assembled instruments represented ([Alfred et al., 2021](../bibliography.md#alfred-et-al-2021)). | The project must score tray assembly categories, not only quiz correctness. |
| Nichol et al. observed 236 surgical instrument errors; Missing+ accounted for 160 errors, including 144 missing, 9 wrong, and 7 extra instruments, and the average delay when a delay occurred was 10.16 minutes ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). | Missing, wrong, and extra items must be visible as separate exported metrics. |
| Surgical tray management asks which instruments belong in trays, in what quantities, which trays map to procedures, and how many trays to hold ([dos Santos et al., 2021](../bibliography.md#dos-santos-et-al-2021)). | The module must include quantities and versioned local tray rules, not only instrument names. |
| Ofstead et al. pilot-tested sterile-processing training for endoscope visual inspection using pre/post tests, lectures, demonstrations, hands-on practice, workplace homework, confidence/satisfaction surveys, and a 2-month booster; nine certified SP employees improved from 41% to 84% after the workshop and retained high scores after the booster ([Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)). | The project should treat Ofstead as the primary training-process analog: baseline assessment, guided practice, separated post-test, confidence/uncertainty capture, and an optional retention check. |
| Qualitative health research should justify sample size by information power and saturation, not by fixed statistical rules; empirical saturation studies commonly converged around 9-17 interviews for homogeneous, narrowly scoped studies ([Malterud et al., 2016](../bibliography.md#malterud-et-al-2016), [Hennink and Kaiser, 2022](../bibliography.md#hennink-and-kaiser-2022)). | A class pilot can use 8 novices as a formative floor, while stronger qualitative theme claims should target 12-17 complete participants. |

## Project Success Targets

The project is evidence-ready only if all targets in this table are met.

| Area | Locked Target | Measurement |
| --- | --- | --- |
| Participant count | Minimum 8 novice participants for the formative class pilot; target 12-17 complete participants before claiming qualitative theme stability. | Count unique `learner_id_hash` values with complete pre/post attempts. |
| Completion rate | At least 7 of 8 participants, or 85% when n > 8, complete the full loop without a blocking moderator intervention. | `completed_full_flow = true` and `blocking_help_requests = 0`. |
| Accuracy gain | Mean paired `accuracy_score` improves by at least 20 percentage points from pre-test to post-test. | `post_accuracy_score - pre_accuracy_score`. |
| Post-test floor | Mean post-test `accuracy_score` is at least 80%, and no more than one participant scores below 70%. | Post-test `accuracy_score`. |
| Severe-error reduction | Mean `missing + wrong + misidentified` error count decreases by at least 30% from pre-test to post-test. | Paired error category counts. |
| Speed without unsafe guessing | Median post-test duration is at least 10% lower than pre-test, or is no more than 20% higher if accuracy improves by at least 20 points. | `duration_seconds`, paired by learner. |
| Confidence calibration | High-confidence errors decline by at least 30%; low-confidence correct answers are exported for review. | Confidence >= 4 on incorrect items; confidence <= 2 on correct items. |
| Uncertainty capture | Assessment screens include a 1-5 confidence rating and an explicit `Not sure` option for each assessed item. | Exports include `item_confidence`, `item_uncertainty`, `not_sure_count`, high-confidence errors, and low-confidence correct answers. |
| Workflow help | Median help requests per participant is <= 1; no participant needs more than 2 non-blocking help requests. | `help_requests_count` and moderator notes. |
| Export completeness | Every completed run exports attempt-level and item-level records with all required fields. | CSV/JSON schema validation. |
| Demo success | A facilitator can load the module, run pre-test, retrieval-first cards, quiz, practice sort, post-test, and export metrics in one uninterrupted demo. | End-to-end demo checklist. |

## First Local Tray Module

The first module is `basic_general_tray_v1`. It is a local, instructor-verified
training tray inspired by a basic general/minor procedure instrument set. It is
not a universal hospital count sheet. Before pilot use, an instructor must
verify the exact instruments, quantities, names, aliases, and photos against the
physical teaching set.

Module acceptance requirements:

- 10 required instrument types;
- 15 total required instrument units;
- 5 distractor instrument types;
- at least 2 local photos per instrument type after the demo set is acquired or
  printed: `view_a` and `view_b`;
- at least 5 declared lookalike pairs;
- two assessment variants using the same required tray rules but different
  photo views, item order, and distractor mix.

Physical demo set note: the team purchased a basic dissection/specimen-
preparation kit as an early photo-capture and authoring source. Its provisional
instrument mapping is documented in
[`instrument_taxonomy.md`](reference/instrument_taxonomy.md#purchased-demo-kit-basic-dissection--specimen-preparation-set).
Treat that kit as teaching/demo material only; the physical items still need
photo capture and instructor verification before they replace or modify the
scored `basic_general_tray_v1` content below.

### Required Instruments

| ID | Required Name | Qty | Family | Accepted Aliases | Real Photo Reference | Distinguishing Features |
| --- | --- | ---: | --- | --- | --- | --- |
| `scalpel_handle_3` | Scalpel handle #3 | 1 | Cutting | #3 handle, Bard-Parker #3, knife handle | <a href="https://surgicalmart.com/shop/surgical-instruments/scalpel-handle/scalpal-handle-3-sm1911/"><img src="https://surgicalmart.com/wp-content/uploads/2017/05/scalpel-handle-3-surgicalmart.jpg" alt="Scalpel handle #3" width="90"><br>Source: Surgical Mart</a> | Short handle for smaller blades; flat metal handle with blade slot. |
| `mayo_scissors_straight_55` | Straight Mayo scissors, 5.5 in | 1 | Cutting | straight Mayo, suture scissors | <a href="https://prodentusa.com/shop/instruments/surgical/scissors-surgical/standard-scissors-surgical/mayo-scissors/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/mayo-scissors-straight-5.5-12-14201-full-300x300.jpg" alt="Straight Mayo scissors" width="90"><br>Source: ProDentUSA</a> | Heavy straight blades; broader than Metzenbaum scissors. |
| `metzenbaum_scissors_curved_55` | Curved Metzenbaum scissors, 5.5 in | 1 | Cutting/dissecting | curved Metzenbaum, Metz scissors | <a href="https://eyerounds.org/tutorials/instruments/Oculoplastics/OculoplasticTray/metzenbaum-dissecting-scissors-curved.htm"><img src="https://eyerounds.org/tutorials/instruments/Oculoplastics/OculoplasticTray/Full%20size/Metzenbaum-Dissecting-Scissors-Curved-2204.jpg" alt="Curved Metzenbaum scissors" width="90"><br>Source: EyeRounds</a> | Slim curved blades; lighter profile for delicate tissue. |
| `adson_forceps_1x2_475` | Adson tissue forceps, 1x2 teeth, 4.75 in | 2 | Grasping/holding | toothed Adson, Adson 1x2 | <a href="https://prodentusa.com/shop/instruments/surgical/tissue-dressing-forceps/adson-tissue-forceps-4-75/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/adson-tissue-forceps-1-by-2-teeth-15-23200-full-300x300.jpg" alt="Adson tissue forceps 1x2" width="90"><br>Source: ProDentUSA</a> | Short thumb forceps; one tooth opposing two teeth at tip. |
| `debakey_forceps_6` | DeBakey tissue forceps, 6 in | 1 | Grasping/holding | DeBakey, atraumatic forceps | <a href="https://surgicalmart.com/shop/surgical-instruments/dissecting-forceps/debakey-atraumatic-tissue-forceps-6-1-5mm-tip-sm3711/"><img src="https://surgicalmart.com/wp-content/uploads/2022/12/debakey-atraumatic-tissue-forceps-6inch-1.5mm-tip-surgicalmart.jpg" alt="DeBakey tissue forceps" width="90"><br>Source: Surgical Mart</a> | Long narrow jaws; atraumatic longitudinal serrations. |
| `mosquito_hemostat_curved_5` | Curved mosquito hemostat, 5 in | 2 | Clamping/occluding | mosquito clamp, small hemostat, snap | <a href="https://surgicalmart.com/shop/surgical-instruments/hemostatic-forceps/halsted-mosquito-forceps-12-sm1753/"><img src="https://surgicalmart.com/wp-content/uploads/2017/05/halsted-mosquito-hemostatic-forceps-5-curved-surgicalmart.jpg" alt="Curved mosquito hemostat" width="90"><br>Source: Surgical Mart</a> | Small ring-handled clamp; shorter and finer than Kelly. |
| `kelly_forceps_curved_55` | Curved Kelly forceps, 5.5 in | 2 | Clamping/occluding | Kelly clamp, curved Kelly, hemostat | <a href="https://prodentusa.com/shop/instruments/surgical/hemostats-forceps/kelly-hemostat-5-5/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/kelly-hemostat-curved-5.5-inch-13-17400-full-300x300.jpg" alt="Curved Kelly forceps" width="90"><br>Source: ProDentUSA</a> | Curved jaws; transverse serrations on distal half of jaws. |
| `allis_tissue_forceps_6` | Allis tissue forceps, 6 in | 2 | Grasping/holding | Allis clamp, Allis forceps | <a href="https://surgicalmart.com/shop/surgical-instruments/hemostatic-forceps/allis-tissue-forceps-6-5x6-teeth-sm4685/"><img src="https://surgicalmart.com/wp-content/uploads/2024/03/allis-tissue-forceps-5x6-teeth-6inch-surgicalmart.jpg" alt="Allis tissue forceps" width="90"><br>Source: Surgical Mart</a> | Ring-handled clamp with multiple interlocking teeth. |
| `mayo_hegar_needle_holder_6` | Mayo-Hegar needle holder, 6 in | 1 | Suturing | needle driver, Mayo-Hegar | <a href="https://prodentusa.com/shop/instruments/surgical/needle-holders/mayo-hegar-needle-holder/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/mayo-hegar-needle-holder-5-GS14-20000.jpg" alt="Mayo-Hegar needle holder" width="90"><br>Source: ProDentUSA</a> | Short broad jaws with cross-hatching; no cutting blades. |
| `senn_retractor_double_ended` | Senn retractor, double-ended | 2 | Retracting/exposing | Senn, rake retractor | <a href="https://surgicalmart.com/shop/surgical-instruments/retractor/senn-mueller-retractor-16cm-sm1873/"><img src="https://surgicalmart.com/wp-content/uploads/2017/05/senn-miller-retractor-3-blunt-prongs-surgicalmart.jpg" alt="Senn-Mueller retractor" width="90"><br>Source: Surgical Mart</a> | Double-ended handheld retractor; one L-shaped blade and one three-prong rake. |

### Distractors

| ID | Distractor Name | Family | Accepted Aliases | Real Photo Reference | Primary Confusion Risk |
| --- | --- | --- | --- | --- | --- |
| `mayo_scissors_curved_55` | Curved Mayo scissors, 5.5 in | Cutting | curved Mayo | <a href="https://prodentusa.com/shop/instruments/surgical/scissors-surgical/standard-scissors-surgical/mayo-scissors/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/mayo-scissors-curved-6.75-12-14502-full.jpg" alt="Curved Mayo scissors" width="90"><br>Source: ProDentUSA</a> | May be confused with curved Metzenbaum scissors. |
| `crile_hemostat_curved_55` | Curved Crile hemostat, 5.5 in | Clamping/occluding | Crile clamp, curved Crile | <a href="https://prodentusa.com/shop/instruments/surgical/hemostats-forceps/crile-forceps/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/crile-hemostat-forceps-curved-13-17600-full.jpg" alt="Curved Crile hemostat" width="90"><br>Source: ProDentUSA</a> | May be confused with curved Kelly forceps. |
| `brown_adson_forceps_475` | Brown-Adson tissue forceps, 4.75 in | Grasping/holding | Brown-Adson, multiple-tooth Adson | <a href="https://prodentusa.com/shop/instruments/surgical/tissue-dressing-forceps/adson-brown-tissue-forceps-4-75/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/adson-brown-tissue-forceps-15-23204-full.jpg" alt="Brown-Adson tissue forceps" width="90"><br>Source: ProDentUSA</a> | May be confused with Adson 1x2 forceps. |
| `olsen_hegar_needle_holder_55` | Olsen-Hegar needle holder, 5.5 in | Suturing/cutting | Olsen-Hegar, needle holder with scissors | <a href="https://prodentusa.com/shop/instruments/surgical/needle-holders/olsen-hegar-needle-holder/"><img src="https://prodentusa.com/wp-content/uploads/2024/11/olsen-hegar-needle-holder-5.5-GS14-21100-300x300.jpg" alt="Olsen-Hegar needle holder" width="90"><br>Source: ProDentUSA</a> | May be confused with Mayo-Hegar needle holder. |
| `babcock_tissue_forceps_6` | Babcock tissue forceps, 6 in | Grasping/holding | Babcock clamp, Babcock forceps | <a href="https://surgicalmart.com/shop/surgical-instruments/hemostatic-forceps/babcock-intestinal-forceps-6-25-with-9mm-jaws-sm4657/"><img src="https://surgicalmart.com/wp-content/uploads/2024/01/babcock-intestinal-forceps-6-25inch-surgicalmart.jpg" alt="Babcock tissue forceps" width="90"><br>Source: Surgical Mart</a> | May be confused with Allis tissue forceps. |

Photo rule: the linked real photos are visual and procurement references only.
Accepted training assets must still be local photos of the actual demo
instruments or 3D-printed proxies used in the pilot. Web or vendor photos may
be shown in planning docs, but should not be treated as the assessed image set
unless licensing and attribution are explicitly cleared.

### Lookalike Pairs

| Expected Required ID | Lookalike/Distractor ID | Error Category | Feedback Focus |
| --- | --- | --- | --- |
| `metzenbaum_scissors_curved_55` | `mayo_scissors_curved_55` | `misidentified` | Compare blade thickness and tissue role. |
| `kelly_forceps_curved_55` | `crile_hemostat_curved_55` | `misidentified` | Check serration pattern: Kelly distal half vs Crile full jaw. |
| `adson_forceps_1x2_475` | `brown_adson_forceps_475` | `misidentified` | Compare tip teeth: 1x2 vs multiple fine teeth. |
| `mayo_hegar_needle_holder_6` | `olsen_hegar_needle_holder_55` | `misidentified` | Look for integrated scissor blades on Olsen-Hegar. |
| `allis_tissue_forceps_6` | `babcock_tissue_forceps_6` | `misidentified` | Compare toothed Allis jaws vs smooth fenestrated Babcock jaws. |
| `mosquito_hemostat_curved_5` | `kelly_forceps_curved_55` | `misidentified` | Compare size and jaw length; mosquito is smaller/finer. |

## Pre/Post Assessment Variants

Both variants use the same required tray rules and quantities. They differ in
presentation so the post-test is not a layout replay.

| Variant | Use | Required Items | Distractors | Photo View | Randomization |
| --- | --- | --- | --- | --- | --- |
| `basic_general_tray_v1_pre_a` | Pre-test | All 10 required IDs, 15 total units | `mayo_scissors_curved_55`, `crile_hemostat_curved_55`, `brown_adson_forceps_475`, `babcock_tissue_forceps_6` | `view_a` | Seed `pre_a_2026_05` |
| `basic_general_tray_v1_post_b` | Post-test | All 10 required IDs, 15 total units | `mayo_scissors_curved_55`, `crile_hemostat_curved_55`, `brown_adson_forceps_475`, `olsen_hegar_needle_holder_55` | `view_b` | Seed `post_b_2026_05` |

Assessment rules:

- no hints;
- no corrective feedback until submission;
- confidence captured once per item or once per submitted tray;
- item order randomized but deterministic by variant seed;
- the learner may inspect the count sheet during assessment because the real
  training target is count-sheet-guided sorting, not memorization alone.

## Scoring Rubric

The answer is scored as a multiset of selected instrument IDs and quantities.

Definitions:

- `required_i`: required quantity for instrument `i`;
- `selected_i`: learner-selected quantity for instrument `i`;
- `total_required_units = sum(required_i)` for the tray, which is 15 for
  `basic_general_tray_v1`;
- `correct_units = sum(min(selected_i, required_i))` for required instruments
  only.

Scoring steps:

1. Calculate exact matches for required instruments.
2. Create one missing unit for every required unit not selected.
3. Create one surplus unit for every selected non-required item and every
   selected quantity above the required count.
4. Pair surplus units to missing units when possible.
5. If the surplus item is a declared lookalike for the missing required item,
   classify that paired substitution as `misidentified`.
6. If the surplus item is known but not a declared lookalike for the missing
   required item, classify that paired substitution as `wrong`.
7. Any unpaired missing units remain `missing`.
8. Any unpaired surplus units remain `extra`.
9. Mark `wrong_count` for each required instrument type where the learner
   selected the correct instrument ID but the quantity differs from the required
   quantity.

Score math:

```text
error_points =
  missing_units
  + extra_units
  + wrong_substitution_units
  + misidentified_substitution_units

accuracy_score =
  max(0, 100 * (1 - error_points / total_required_units))

required_recall =
  100 * (correct_units / total_required_units)
```

Weighting decisions:

- `missing` and `extra` are weighted equally at 1 error point per unit.
- `wrong` and `misidentified` are also weighted at 1 error point per paired
  substitution unit.
- A `wrong` or `misidentified` substitution consumes one missing unit and one
  surplus unit; it is not double-penalized as both `missing` and `extra`.
- `misidentified` differs from `wrong` only by evidence: it must match a
  declared lookalike pair. This lets the feedback teach visual discrimination.
- `wrong_count` affects score through the underlying missing or surplus units.
  It is exported as a diagnostic category but is not an additional double
  penalty.

Example:

```text
Required: 2 curved Kelly forceps
Selected: 1 curved Kelly forceps + 1 curved Crile hemostat

correct_units = 1
misidentified_substitution_units = 1
missing_units after pairing = 0
extra_units after pairing = 0
wrong_count = 1 for curved Kelly forceps
accuracy_score contribution = one error point against the 15-unit tray
```

## Required Export Fields

The project must export both attempt-level and item-level data. CSV is acceptable;
JSON is acceptable if it preserves the same field names.

### Attempt-Level Export

Required fields:

- `run_id`
- `learner_id_hash`
- `participant_group`
- `prior_experience_level`
- `tray_module_id`
- `tray_module_version`
- `assessment_variant_id`
- `mode`
- `started_at`
- `completed_at`
- `duration_seconds`
- `completed_full_flow`
- `help_requests_count`
- `blocking_help_requests`
- `confidence_scale`
- `overall_confidence`
- `total_required_units`
- `selected_units`
- `correct_units`
- `error_points`
- `accuracy_score`
- `required_recall`
- `missing_count`
- `extra_count`
- `wrong_substitution_count`
- `misidentified_count`
- `wrong_count_error_count`
- `not_sure_count`
- `high_confidence_error_count`
- `low_confidence_correct_count`

### Item-Level Export

Required fields:

- `run_id`
- `learner_id_hash`
- `tray_module_id`
- `assessment_variant_id`
- `mode`
- `expected_instrument_id`
- `expected_instrument_name`
- `required_quantity`
- `selected_instrument_id`
- `selected_instrument_name`
- `selected_quantity`
- `correct_quantity`
- `error_category`
- `lookalike_pair_id`
- `item_confidence`
- `item_uncertainty`
- `is_high_confidence_error`
- `is_low_confidence_correct`
- `feedback_message_id`

## Functional Requirements

| ID | Requirement | Acceptance Test |
| --- | --- | --- |
| FR-1 | Load `basic_general_tray_v1` from a data file without code changes. | Change module content in data, restart app, and see updated cards and assessment items. |
| FR-2 | Render retrieval-first cards for all required and distractor instruments. | Each card prompts before reveal, then shows name, aliases, family, quantity if required, local photos, and distinguishing features. |
| FR-3 | Run pre-test and post-test without hints or corrective feedback. | User submits both variants and sees feedback only after submission. |
| FR-4 | Run quiz mode with immediate correctness feedback. | Quiz records correctness, time, confidence, and weak-item recovery. |
| FR-5 | Run practice sort with error-specific feedback. | Feedback names `missing`, `extra`, `wrong`, `misidentified`, and `wrong_count` when present. |
| FR-6 | Export valid metrics after a full learner run. | Attempt-level and item-level files contain every required field. |
| FR-7 | Separate teaching and assessment modes. | UI state and export mode values make mode boundaries unambiguous. |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-1 | Demo data load time | Module loads in <= 2 seconds on the project laptop. |
| NFR-2 | Flow duration | A novice can complete the full learning loop in <= 20 minutes. |
| NFR-3 | Export reliability | 100% of completed runs produce a valid export file. |
| NFR-4 | Data privacy | Exports use `learner_id_hash`; no names, emails, MRNs, or patient data. |
| NFR-5 | Content traceability | Every instrument has a module version, photo path, source note, and instructor verification status. |
| NFR-6 | Claim boundary | The UI and report language never label a learner as certified, workplace-ready, or clinically approved. |

## Successful Demo Definition

A successful project demo means:

1. The first local module is loaded from data.
2. The facilitator shows at least one required instrument card, one distractor,
   and one lookalike feedback example.
3. A learner run completes pre-test, retrieval-first cards, quiz, practice sort,
   and post-test.
4. The post-test uses the `post_b` variant, not the exact pre-test layout.
5. Metrics export includes accuracy, duration, confidence, help requests, and
   all five error categories.
6. The summary compares pre/post outcomes and names the weakest instruments.
7. The presenter explicitly states that results are simulated training evidence,
   not certification or live SPD productivity proof.

## Out Of Scope

The project does not need to:

- certify SPD competency;
- prove reduced real hospital onboarding time;
- prove fewer OR delays or tray defects;
- use computer vision for assessment;
- recognize every manufacturer variant;
- integrate with hospital instrument tracking systems;
- handle sterile technique, damaged instruments, bioburden inspection, or
  packaging/sterilization readiness beyond explanatory training notes.
