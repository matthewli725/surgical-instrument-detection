# TODO

## In Progress

- Create file-backed tray and instrument seed data from
  `docs/project/system_requirements.md`.
- Implement pre-test and post-test tray sorting with hints and feedback
  disabled.
- Implement retrieval-first cards and a short identification quiz for the same
  module.
- Implement practice sorting with immediate error-specific feedback.
- Export learner metrics as CSV or JSON.

## Next Up

- Run a small pilot walkthrough and record pre/post accuracy, time, confidence,
  and error categories.
- Update presentation/report language so the main claim is simulated
  time-to-competency, with deployment boundaries linked to
  `docs/project/scope_boundaries_and_risks.md`.
- Add the literature-gap and stakeholder-implication framing to the final
  presentation.
- Review accessible surgical instrument catalogs as candidate sources for
  common canonical names, aliases, families, variants, and lookalike pairs:
  [Teleflex Surgical Catalog](https://www.teleflexsurgicalcatalog.com/),
  [Sklar Catalogues via ActionMed](https://www.actionmed.ae/index.php/downloads/sklar-catalogues),
  [Medicta General Surgery Instruments Catalog](https://pdf.medicalexpo.com/pdf/medicta-instruments/general-surgery-instruments/129353-265855.html),
  and
  [SurgicalInstruments.com Major Instrument Set](https://www.surgicalinstruments.com/major-instrument-set/).
  Use them as authoring references only, then verify final module names against
  local tray count sheets and teaching photos.
- Treat camera/CV work as future authoring or visual-review support unless a
  future team validates it as an active evaluation layer.

## Completed Decisions

- Training feature priorities are ranked in
  `docs/project/planning/training_feature_prioritization.md`: tray
  reconstruction, error spotting, lookalike challenges, weak-item replay,
  metrics export, and file-backed local modules are the recommended MVP focus.
- First local tray training module is defined in
  `docs/project/system_requirements.md`: 10 required instrument types,
  15 required units, 5 distractors, photo manifest, lookalike pairs, and
  comparable pre/post variants.
- Scoring rubric is locked in `docs/project/system_requirements.md` for
  `missing`, `extra`, `wrong`, `misidentified`, and `wrong_count`.
- Minimum metrics export is locked in
  `docs/project/system_requirements.md`: accuracy, duration, confidence,
  help requests, and full error breakdown at attempt and item levels.

## Upcoming Milestones

### Training Module

- Local Tray Data Contract Ready
- Seed Tray Module Ready
- Study And Quiz Flow Ready
- Practice Sorting Feedback Ready
- Pre/Post Assessment Ready
- Metrics Export Ready
- Pilot Training Walkthrough Ready

### Evidence And Reporting

- Training Effectiveness Protocol Ready
- Claim-Evidence Control Sheet Updated
- Literature Gaps And Stakeholders Ready
- Final Report Scope Language Ready
- Demo Narrative Ready
