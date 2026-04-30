# Unit Task List For GitLab Issues

This task list is organized by milestone.

## Issue-Sized Task List

### Sensing / Physical Capture Setup Ready

- Find candidate 3D models for surgical tools
- Prepare printable files for initial surgical-tool set
- Print first small set of 3D surgical-tool proxies
- Plan physical image-capture setup
- Design rigid camera-stand approach
- Select fixed-color background for image capture
- Connect iPhone to Mac for frame capture workflow
- Upload and inspect individual cv2 frames from phone capture

### Sensing / Collection Pipeline Ready

- Complete physical image-collection setup
- Complete software image-collection setup
- Identify online surgical-instrument datasets to combine
- Compare dataset coverage and likely usefulness
- Investigate space and form-factor constraints for SPD deployment
- Investigate deployment and maintenance expectations for the system
- Measure actual prototype field of view and usable tray workspace
- Time clean setup from packed state to first successful scan

### Sensing / Material And Lighting Assumptions Ready

- Investigate whether spray-painted prints are a usable stainless-steel proxy
- Compare spray-painted proxies against real stainless-steel goal
- Investigate visual properties that define object appearance
- Evaluate BRDF as a candidate representation for this project
- Research real surgical-instrument material composition
- Research BRDF and related material-property representations
- Summarize dominant factors in human visual perception for this context
- Review BRDF measurement requirements and practical constraints
- Assess whether BRDF measurement is overkill for this prototype
- Investigate RGB specularity-removal alternatives
- Check whether silverware and surgical tools can share similar steel-alloy assumptions
- Investigate likely SPD lighting conditions

### Sensing / Lighting Dataset Ready

- Plan variable lighting-angle and lighting-type setup
- Capture silverware images under varied lighting as material proxy
- Capture first qualitative lighting-variation examples with rough angle and distance notes
- Collect additional data for lighting experiment
- Audit lighting dataset sessions and mark usable vs unusable folders
- Standardize lighting-condition names across current dataset files
- Export reproducible YOLO split for lighting experiment
- Verify train, val, and test manifests for lighting dataset

### Perception / Experiment Questions Locked

- Define initial question for similar-shape instrument recognition
- Define initial question for metallic-surface lighting robustness
- Run initial retrain and retest cycle for model capability check
- Investigate whether CV can reliably identify similar instruments
- Estimate training-data needs for similar-instrument recognition
- Design first similar-object recognition experiment
- Design first partial-occlusion experiment
- Plan graph of light intensity vs detection rate or mAP50-95

### Perception / Lighting Results Ready

- Run baseline lighting model on reference-only dataset
- Run expanded-lighting model on augmented lighting dataset
- Collect precision, recall, mAP50, and mAP50-95 into one table
- Select 6-10 representative glare-condition images
- Re-run failed or inconsistent lighting jobs
- Confirm final lighting metrics to report
- Build clean comparison table for lighting-training stages
- Write lighting results section
- Write lighting interpretation and limitation section

### Perception / Similar Baseline Ready

- Define first similar-instrument class pairs to test
- Write short rationale for chosen similar-instrument pairs
- Collect initial image set for first similar-instrument pairs
- Organize raw similar-instrument images into a consistent folder structure
- Review similar-instrument images and remove weak samples
- Export YOLO dataset for similar-instrument baseline
- Verify split quality for similar-instrument dataset
- Train baseline similar-instrument detection model
- Evaluate baseline model and record per-class metrics
- Review false positives for similar classes
- Review false negatives for similar classes
- Save 5-8 confusing similar-tool examples
- Write short confusion summary for worst similar pair

### Perception / Demo Model Ready

- Choose best current model weights for final demo
- Build final lighting-results figure pack
- Build final similar-instrument figure pack

### Tray Logic / Result Semantics Defined

- Draft in-scope vs out-of-scope capability table
- Draft prototype requirements section
- Add evidence status for each hard engineering target
- Decide whether manual correction is in scope this quarter
- Document revised scope if manual correction is deferred

### Tray Logic / Decision Support Implemented

- Add missing-item summary to Streamlit app
- Add extra-item or over-count summary to Streamlit app
- Add review-state indicator for risky detections
- Track exact-count, under-count, and over-count outcomes by class

### UI / Baseline Workflow Defined

- Start website interface for displaying detection results
- Refine website interface requirements
- Investigate whether technicians work with overlapping instruments
- Investigate whether the system would disrupt current SPD workflow
- Investigate whether the system can be intuitive and plug-and-play

### UI / Workflow Gap Review Complete

- List top 5 mismatches between current UI and documented product concept
- Write current live-demo workflow description

### UI / Tray Review Flow Improved

- Capture before-and-after screenshots of updated UI
- Build final UI screenshot pack

### UI / Walkthrough Evidence Ready

- Write scripted tray-check walkthrough
- Run pilot walkthrough and record confusion points
- Revise walkthrough script after pilot
- Run walkthrough session 1 and record timing
- Run walkthrough session 2 and record timing
- Run walkthrough session 3 and record timing
- Record user action count from tray selection to final decision
- Summarize rescans, hesitations, and user complaints
- Summarize what users found helpful or clear
- Run wording comparison between assistant-mode and automation-mode language
- Update workflow-acceptance doc with actual observations
- Add limitation note about non-SPD participants

### UI / Demo Flow Ready

- Select final demo scenario
- Lock final class list for the demo
- Copy final weights into default demo path
- Run end-to-end demo verification test
- Write live-demo script with fallback steps

### Traceability / Record Schema Ready

- Define minimum tray-check record schema

### Traceability / Logging Implemented

- Save scan ID and timestamp for each tray-check record
- Save required-item list and observed counts to disk
- Save missing-item results to disk
- Save per-detection confidence values to disk
- Save screenshot or frame reference for each tray check

### Traceability / Reporting Ready

- Draft lightweight quality-report format
- Generate example tray-check report from prototype data
- Update traceability doc to match implemented logging
- Build final logging or reporting figure pack
