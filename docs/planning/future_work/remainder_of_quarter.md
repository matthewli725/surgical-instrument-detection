## Main Goal

Finish the quarter with a prototype and documentation set that support the
following claim:

- TrayGuard is a technician-centered visual verification assistant whose core
  computer-vision assumptions have been tested under controlled approximations
  of real tray-checking risks.


## Week 4

### Primary Focus

- Run the lighting experiments.
- Start the similar-instrument experiment.

### Tasks

- Audit the current lighting dataset folders and confirm which sessions are
  clean enough to use.
- Write down the lighting-condition labels already present in the data and note
  missing labels or inconsistent naming.
- Export or regenerate the lighting YOLO dataset so the train, val, and test
  splits are reproducible.
- Run one baseline lighting training job and save the command, weights path, and
  result metrics.
- Run one expanded-lighting training job and save the command, weights path, and
  result metrics.
- Pull the key precision, recall, `mAP50`, and `mAP50-95` numbers into one
  comparison table.
- Capture 6-10 representative lighting images that show easy, medium, and hard
  glare conditions.
- Define the first similar-instrument class pairs to test.
- Collect or stage the first small similar-instrument image set.
- Write a short note explaining why those similar pairs matter to tray
  verification.

### Week 4 Outputs

- Lighting metrics table
- Lighting example image set
- Initial similar-instrument class list
- First similar-instrument dataset stub

## Week 5

### Primary Focus

- Strengthen the lighting writeup.
- Build the first usable similar-instrument experiment.

### Tasks

- Re-run any failed or inconsistent lighting jobs and confirm the final numbers
  you want to report.
- Make one clean figure or markdown table comparing lighting-training stages.
- Write the result and interpretation sections for the lighting doc using the
  final numbers.
- Inspect similar-instrument images and remove obviously bad labels or weak
  captures.
- Export the first similar-instrument YOLO dataset with a documented split.
- Train one baseline model for similar-instrument detection.
- Evaluate the model on the held-out split and record per-class metrics.
- Review false positives and false negatives for the similar classes.
- Save 5-8 screenshots of confusing similar-tool examples.
- Write a short confusion summary focused on the worst pair, not just the
  average metrics.

### Week 5 Outputs

- Updated `reflectivity_lighting.md`
- Similar-instrument baseline results
- Similar-pair failure screenshot set

## Week 6

### Primary Focus

- Turn experiment progress into CDR material.
- Lock the problem, stakeholders, and scope language.

### Tasks

- Write a stakeholder table covering technician, manager, buyer, and downstream
  OR impacts.
- Write a scope table listing in-scope and out-of-scope capabilities for this
  quarter.
- Add a short requirements section to the project docs stating what the
  prototype must demonstrate.
- Convert the completed lighting work into a concise engineering-work summary.
- Convert the similar-instrument baseline into a concise engineering-work
  summary.
- Write a short unknowns section covering clutter, open-set behavior, workflow
  usefulness, and reporting gaps.
- Build one CDR-ready summary table mapping each experiment to:
  - question
  - evidence collected
  - current conclusion
  - remaining gap
- Draft the week 6 version of remaining-quarter milestones.

### Week 6 Outputs

- CDR-ready stakeholder section
- CDR-ready scope and requirements section
- Updated unknowns and remaining-work summary

## Week 7

### Primary Focus

- Improve the prototype workflow so it better matches the written product
  concept.

### Tasks

- Review the current Streamlit app and list the top 5 workflow mismatches
  between code and docs.
- Add a clearer missing-item summary to the UI.
- Add a clearer extra-item or over-count summary to the UI.
- Add a visible review state for low-confidence detections or risky conditions.
- Save before-and-after screenshots of the tray-check UI.
- Write a short doc describing the current live-demo workflow step by step.
- Decide whether manual correction will be implemented now or represented as a
  documented future extension.
- If manual correction is deferred, write a short justification and revised
  scope note.

### Week 7 Outputs

- Improved tray-check UI
- UI screenshots
- Workflow gap note

## Week 8

### Primary Focus

- Add traceability and logging support strong enough to support the reporting
  story.

### Tasks

- Define the minimum tray-check record format in markdown or JSON schema form.
- Add a scan ID and timestamp to each saved tray-check record.
- Save required items, observed counts, and missing-item results to disk.
- Save per-detection confidence values to disk.
- Save a screenshot or frame reference for each tray-check run.
- Draft a simple report format that aggregates repeated misses, repeated review
  flags, and repeated corrections.
- Generate one example report using mock or real prototype data.
- Update the traceability doc so it matches what is actually implemented.

### Week 8 Outputs

- Tray-check logging schema
- Example tray-check records
- Example lightweight quality report

## Week 9

### Primary Focus

- Gather lightweight workflow-acceptance evidence and close the biggest product
  narrative gaps.

### Tasks

- Write a short scripted walkthrough for testing the tray-check workflow.
- Run one pilot walkthrough with an available classmate or teammate and note
  confusion points.
- Revise the walkthrough script based on the pilot.
- Run 2-3 additional walkthroughs and record task time, rescans, and major
  hesitations.
- Summarize the main workflow complaints and the main points users liked.
- Compare assistant-style language and stronger automation-style language in one
  lightweight wording test if time allows.
- Update the workflow-acceptance doc with actual observations instead of only
  proposed measurements.
- Add a short limitation note making clear that these are not SPD technicians.

### Week 9 Outputs

- Walkthrough script
- Small user-feedback summary
- Updated workflow-acceptance doc

## Week 10

### Primary Focus

- Freeze the demo path and prepare final report and presentation artifacts.

### Tasks

- Pick the final demo scenario and final class list.
- Select the best current model weights for the demo and copy them into the
  default path.
- Run one end-to-end verification from collection or saved image through live
  UI output.
- Make one final figure pack for slides:
  - lighting results
  - similar-instrument results
  - UI screenshots
  - logging or reporting example
- Write one final summary page of key claims and evidence.
- Write one final summary page of remaining risks and limitations.
- Prepare a short live-demo script with setup steps and fallback steps.
- Review the docs for any claims that are stronger than the actual code and tone
  them down if needed.

### Week 10 Outputs

- Frozen demo configuration
- Final figure pack
- Final claim-and-evidence summary
- Final risks-and-limitations summary

## Cross-Cutting Tasks

These can be slotted into any week when there is a short work block available.

- Clean up one experiment doc so the language distinguishes proposed work from
  completed work.
- Move one important command or workflow into reproducibility docs.
- Add one table or figure that can be reused in both CDR and FDR.
- Rename files or sections to keep the docs modular and easy to navigate.
- Record team ownership for one deliverable or experiment result.

## Key Open Risks To Watch

- Similar-looking tools may still produce unsafe high-confidence confusions.
- The lighting experiment may show plausible trends without enough rigor to
  support stronger claims.
- The demo UI may remain weaker than the written product concept.
- Workflow usefulness may be hard to support without real SPD-user feedback.
- Logging and reporting may remain lightweight rather than fully product-like.
- Scope may still need to narrow if too many experiment axes remain unfinished by
  week 8.
