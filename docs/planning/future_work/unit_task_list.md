# Unit Task List For GitLab Issues

This file breaks the remainder-of-quarter plan into issue-sized units. Each item
should be small enough for one person to complete in roughly 2-3 hours.

Recommended fields for GitLab issues:

- title
- target week
- category
- acceptance criteria

## Week 1

These are retrospective tasks based on work that was actually done or actively
planned during week 1.

### Initial Problem Framing And Physical Assets

- `[W1][research][scope] Schedule sterile processing facility tour outreach`
- `[W1][hardware][assets] Find candidate 3D models for surgical tools`
- `[W1][hardware][assets] Prepare printable files for initial surgical-tool set`
- `[W1][hardware][assets] Print first small set of 3D surgical-tool proxies`
- `[W1][ops][outreach] Follow up on SPD access and tour scheduling`

### Early Technical Direction

- `[W1][similar][scope] Define initial question for similar-shape instrument recognition`
- `[W1][lighting][scope] Define initial question for metallic-surface lighting robustness`
- `[W1][materials][research] Investigate whether spray-painted prints are a usable stainless-steel proxy`

## Week 2

These are retrospective tasks based on work that was actually done during week
2.

### Interface And Capture Workflow

- `[W2][ui][prototype] Start website interface for displaying detection results`
- `[W2][capture][prototype] Connect iPhone to Mac for frame capture workflow`
- `[W2][capture][prototype] Upload and inspect individual cv2 frames from phone capture`

### Outreach And Access

- `[W2][ops][outreach] Contact additional people for hospital tour access`
- `[W2][ops][outreach] Visit Ronald Reagan UCLA Medical Center to ask about SPD tour access`
- `[W2][ops][outreach] Email Muriel Lauranche requesting surgical room and SPD tour`

### Scope Narrowing And Materials Research

- `[W2][research][scope] Synthesize research to narrow useful tool-identification scope`
- `[W2][materials][research] Compare spray-painted proxies against real stainless-steel goal`

### Week 2 Forward-Looking Setup Tasks

- `[W2][hardware][setup] Plan physical image-capture setup`
- `[W2][hardware][setup] Design rigid camera-stand approach`
- `[W2][hardware][setup] Select fixed-color background for image capture`
- `[W2][lighting][setup] Plan variable lighting-angle and lighting-type setup`
- `[W2][ui][prototype] Refine website interface requirements`
- `[W2][datasets][research] Identify online surgical-instrument datasets to combine`
- `[W2][datasets][research] Compare dataset coverage and likely usefulness`
- `[W2][materials][research] Investigate visual properties that define object appearance`
- `[W2][materials][research] Evaluate BRDF as a candidate representation for this project`
- `[W2][materials][research] Research real surgical-instrument material composition`
- `[W2][lighting][data] Capture silverware images under varied lighting as material proxy`
- `[W2][ml][experiments] Run initial retrain and retest cycle for model capability check`

## Week 3

These are retrospective tasks based on work that was actually done during week
3, plus the immediate next-step tasks that followed from that work.

### Data Collection System Setup

- `[W3][capture][setup] Complete physical image-collection setup`
- `[W3][capture][setup] Complete software image-collection setup`
- `[W3][lighting][data] Capture first qualitative lighting-variation examples with rough angle and distance notes`

### Materials And Perception Research

- `[W3][materials][research] Research BRDF and related material-property representations`
- `[W3][materials][research] Summarize dominant factors in human visual perception for this context`
- `[W3][materials][research] Review BRDF measurement requirements and practical constraints`
- `[W3][materials][research] Assess whether BRDF measurement is overkill for this prototype`
- `[W3][materials][research] Investigate RGB specularity-removal alternatives`
- `[W3][materials][research] Check whether silverware and surgical tools can share similar steel-alloy assumptions`

### Week 3 Forward-Looking Planning Tasks

- `[W3][cdr][docs] Synthesize existing research into one compelling project story`
- `[W3][research][tradeoffs] Draft cost-benefit comparison of CV vs other technologies vs human labor`
- `[W3][lighting][research] Investigate likely SPD lighting conditions`
- `[W3][workflow][research] Investigate whether technicians work with overlapping instruments`
- `[W3][similar][research] Investigate whether CV can reliably identify similar instruments`
- `[W3][similar][research] Estimate training-data needs for similar-instrument recognition`
- `[W3][workflow][research] Investigate whether the system would disrupt current SPD workflow`
- `[W3][integration][research] Investigate space and form-factor constraints for SPD deployment`
- `[W3][ui][research] Investigate whether the system can be intuitive and plug-and-play`
- `[W3][ops][research] Investigate deployment and maintenance expectations for the system`
- `[W3][similar][experiments] Design first similar-object recognition experiment`
- `[W3][occlusion][experiments] Design first partial-occlusion experiment`
- `[W3][lighting][data] Collect additional data for lighting experiment`
- `[W3][lighting][results] Plan graph of light intensity vs detection rate or mAP50-95`

## Week 4

### Data And Experiment Setup

- `[W4][lighting][data] Audit lighting dataset sessions and mark usable vs unusable folders`
- `[W4][lighting][data] Standardize lighting-condition names across current dataset files`
- `[W4][lighting][data] Export reproducible YOLO split for lighting experiment`
- `[W4][lighting][data] Verify train, val, and test manifests for lighting dataset`

### Lighting Experiment Runs

- `[W4][lighting][train] Run baseline lighting model on reference-only dataset`
- `[W4][lighting][train] Run expanded-lighting model on augmented lighting dataset`
- `[W4][lighting][results] Collect precision, recall, mAP50, and mAP50-95 into one table`
- `[W4][lighting][figures] Select 6-10 representative glare-condition images`

### Similar-Instrument Startup

- `[W4][similar][scope] Define first similar-instrument class pairs to test`
- `[W4][similar][data] Write short rationale for chosen similar-instrument pairs`
- `[W4][similar][data] Collect initial image set for first similar-instrument pairs`
- `[W4][similar][data] Organize raw similar-instrument images into a consistent folder structure`

## Week 5

### Lighting Writeup

- `[W5][lighting][train] Re-run failed or inconsistent lighting jobs`
- `[W5][lighting][results] Confirm final lighting metrics to report`
- `[W5][lighting][figures] Build clean comparison table for lighting-training stages`
- `[W5][lighting][docs] Write lighting results section`
- `[W5][lighting][docs] Write lighting interpretation and limitation section`

### Similar-Instrument Baseline

- `[W5][similar][data] Review similar-instrument images and remove weak samples`
- `[W5][similar][data] Export YOLO dataset for similar-instrument baseline`
- `[W5][similar][data] Verify split quality for similar-instrument dataset`
- `[W5][similar][train] Train baseline similar-instrument detection model`
- `[W5][similar][results] Evaluate baseline model and record per-class metrics`
- `[W5][similar][results] Review false positives for similar classes`
- `[W5][similar][results] Review false negatives for similar classes`
- `[W5][similar][figures] Save 5-8 confusing similar-tool examples`
- `[W5][similar][docs] Write short confusion summary for worst similar pair`

## Week 6

### CDR Definition And Scope

- `[W6][cdr][docs] Draft stakeholder table for TrayGuard`
- `[W6][cdr][docs] Draft in-scope vs out-of-scope capability table`
- `[W6][cdr][docs] Draft prototype requirements section`
- `[W6][cdr][docs] Draft unknowns and concerns section`
- `[W6][cdr][docs] Build experiment-summary table for CDR`
- `[W6][cdr][planning] Draft updated remainder-of-quarter milestones`

### Engineering Work Summaries

- `[W6][cdr][docs] Convert lighting experiment progress into engineering-work summary`
- `[W6][cdr][docs] Convert similar-instrument baseline into engineering-work summary`
- `[W6][cdr][docs] Add current evidence vs remaining gap notes to experiment docs`

## Week 7

### Workflow Gap Review

- `[W7][ui][review] List top 5 mismatches between current UI and documented product concept`
- `[W7][ui][docs] Write current live-demo workflow description`
- `[W7][scope][decision] Decide whether manual correction is in scope this quarter`
- `[W7][scope][docs] Document revised scope if manual correction is deferred`

### UI Improvements

- `[W7][ui][feature] Add missing-item summary to Streamlit app`
- `[W7][ui][feature] Add extra-item or over-count summary to Streamlit app`
- `[W7][ui][feature] Add review-state indicator for risky detections`
- `[W7][ui][figures] Capture before-and-after screenshots of updated UI`

## Week 8

### Logging Schema

- `[W8][logging][design] Define minimum tray-check record schema`
- `[W8][logging][feature] Save scan ID and timestamp for each tray-check record`
- `[W8][logging][feature] Save required-item list and observed counts to disk`
- `[W8][logging][feature] Save missing-item results to disk`
- `[W8][logging][feature] Save per-detection confidence values to disk`
- `[W8][logging][feature] Save screenshot or frame reference for each tray check`

### Reporting

- `[W8][reporting][design] Draft lightweight quality-report format`
- `[W8][reporting][data] Generate example tray-check report from prototype data`
- `[W8][reporting][docs] Update traceability doc to match implemented logging`

## Week 9

### Workflow Walkthrough Preparation

- `[W9][workflow][study] Write scripted tray-check walkthrough`
- `[W9][workflow][study] Run pilot walkthrough and record confusion points`
- `[W9][workflow][study] Revise walkthrough script after pilot`

### Workflow Walkthrough Execution

- `[W9][workflow][study] Run walkthrough session 1 and record timing`
- `[W9][workflow][study] Run walkthrough session 2 and record timing`
- `[W9][workflow][study] Run walkthrough session 3 and record timing`
- `[W9][workflow][results] Summarize rescans, hesitations, and user complaints`
- `[W9][workflow][results] Summarize what users found helpful or clear`
- `[W9][workflow][study] Run wording comparison between assistant-mode and automation-mode language`
- `[W9][workflow][docs] Update workflow-acceptance doc with actual observations`
- `[W9][workflow][docs] Add limitation note about non-SPD participants`

## Week 10

### Demo Freeze

- `[W10][demo][decision] Select final demo scenario`
- `[W10][demo][decision] Lock final class list for the demo`
- `[W10][demo][train] Choose best current model weights for final demo`
- `[W10][demo][feature] Copy final weights into default demo path`
- `[W10][demo][verify] Run end-to-end demo verification test`

### Final Presentation Assets

- `[W10][slides][figures] Build final lighting-results figure pack`
- `[W10][slides][figures] Build final similar-instrument figure pack`
- `[W10][slides][figures] Build final UI screenshot pack`
- `[W10][slides][figures] Build final logging or reporting figure pack`
- `[W10][slides][docs] Write final key-claims-and-evidence summary`
- `[W10][slides][docs] Write final risks-and-limitations summary`
- `[W10][demo][docs] Write live-demo script with fallback steps`
- `[W10][review][docs] Review all docs for claims that exceed current evidence`

## Cross-Cutting Backlog

These are useful filler issues when someone has one short block available.

- `[Any][docs][cleanup] Convert one experiment section from proposed language to completed-work language`
- `[Any][docs][cleanup] Add one reusable table for both CDR and FDR slides`
- `[Any][docs][cleanup] Add one reproducibility command block to experiment docs`
- `[Any][docs][cleanup] Record team ownership for one deliverable`
- `[Any][repo][cleanup] Rename one doc or section for clearer navigation`

## Suggested Labels

- `week::1`
- `week::2`
- `week::3`
- `week::4`
- `week::5`
- `week::6`
- `week::7`
- `week::8`
- `week::9`
- `week::10`
- `category::lighting`
- `category::similar`
- `category::materials`
- `category::hardware`
- `category::ops`
- `category::capture`
- `category::datasets`
- `category::research`
- `category::cdr`
- `category::ui`
- `category::logging`
- `category::reporting`
- `category::workflow`
- `category::integration`
- `category::demo`
- `category::slides`
- `category::docs`

## Suggested Acceptance-Criteria Template

Use this for issue descriptions:

```text
Acceptance criteria
- Task output exists in the repo or run artifacts
- Any commands used are recorded if the task is experimental
- Any metrics or figures are saved in a reusable format
- Related doc is updated if the task changes reported claims
```
