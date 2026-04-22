# GitLab Issue Planning Table

This table provides a compact view of the current work plan.

All issues start on a Thursday and are due the following Thursday.

| Issue Title | Status | Start Date | Due Date | Epic | Milestone | Category | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Find candidate 3D models for surgical tools | done | 2026-04-02 | 2026-04-09 | Sensing And Capture | Sensing / Physical Capture Setup Ready | hardware | none |
| Prepare printable files for initial surgical-tool set | done | 2026-04-02 | 2026-04-09 | Sensing And Capture | Sensing / Physical Capture Setup Ready | hardware | Find candidate 3D models for surgical tools |
| Print first small set of 3D surgical-tool proxies | done | 2026-04-02 | 2026-04-09 | Sensing And Capture | Sensing / Physical Capture Setup Ready | hardware | Prepare printable files for initial surgical-tool set |
| Connect iPhone to Mac for frame capture workflow | done | 2026-04-02 | 2026-04-09 | Sensing And Capture | Sensing / Physical Capture Setup Ready | capture | none |
| Upload and inspect individual cv2 frames from phone capture | done | 2026-04-02 | 2026-04-09 | Sensing And Capture | Sensing / Physical Capture Setup Ready | capture | Connect iPhone to Mac for frame capture workflow |
| Define initial question for similar-shape instrument recognition | done | 2026-04-02 | 2026-04-09 | Perception | Perception / Experiment Questions Locked | similar | none |
| Define initial question for metallic-surface lighting robustness | done | 2026-04-02 | 2026-04-09 | Perception | Perception / Experiment Questions Locked | lighting | none |
| Start website interface for displaying detection results | done | 2026-04-02 | 2026-04-09 | Technician UI And Workflow | UI / Baseline Workflow Defined | ui | none |
| Investigate whether spray-painted prints are a usable stainless-steel proxy | done | 2026-04-02 | 2026-04-09 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | none |
| Plan physical image-capture setup | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Physical Capture Setup Ready | hardware | none |
| Design rigid camera-stand approach | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Physical Capture Setup Ready | hardware | Plan physical image-capture setup |
| Select fixed-color background for image capture | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Physical Capture Setup Ready | hardware | Plan physical image-capture setup |
| Refine website interface requirements | done | 2026-04-09 | 2026-04-16 | Technician UI And Workflow | UI / Baseline Workflow Defined | ui | Start website interface for displaying detection results |
| Identify online surgical-instrument datasets to combine | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Collection Pipeline Ready | datasets | none |
| Compare dataset coverage and likely usefulness | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Collection Pipeline Ready | datasets | Identify online surgical-instrument datasets to combine |
| Compare spray-painted proxies against real stainless-steel goal | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Investigate whether spray-painted prints are a usable stainless-steel proxy |
| Investigate visual properties that define object appearance | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | none |
| Research real surgical-instrument material composition | done | 2026-04-09 | 2026-04-16 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | none |
| Run initial retrain and retest cycle for model capability check | done | 2026-04-09 | 2026-04-16 | Perception | Perception / Experiment Questions Locked | ml | none |
| Complete physical image-collection setup | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Collection Pipeline Ready | capture | Design rigid camera-stand approach |
| Complete software image-collection setup | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Collection Pipeline Ready | capture | Plan physical image-capture setup |
| Plan variable lighting-angle and lighting-type setup | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Plan physical image-capture setup |
| Capture silverware images under varied lighting as material proxy | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Plan variable lighting-angle and lighting-type setup |
| Capture first qualitative lighting-variation examples with rough angle and distance notes | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Complete physical image-collection setup |
| Evaluate BRDF as a candidate representation for this project | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Investigate visual properties that define object appearance |
| Research BRDF and related material-property representations | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Evaluate BRDF as a candidate representation for this project |
| Summarize dominant factors in human visual perception for this context | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Investigate visual properties that define object appearance |
| Review BRDF measurement requirements and practical constraints | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Research BRDF and related material-property representations |
| Assess whether BRDF measurement is overkill for this prototype | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Review BRDF measurement requirements and practical constraints |
| Investigate RGB specularity-removal alternatives | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Assess whether BRDF measurement is overkill for this prototype |
| Check whether silverware and surgical tools can share similar steel-alloy assumptions | done | 2026-04-16 | 2026-04-23 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | materials | Research real surgical-instrument material composition |
| Investigate likely SPD lighting conditions | planned | 2026-04-23 | 2026-04-30 | Sensing And Capture | Sensing / Material And Lighting Assumptions Ready | lighting | none |
| Investigate whether technicians work with overlapping instruments | planned | 2026-04-23 | 2026-04-30 | Technician UI And Workflow | UI / Baseline Workflow Defined | workflow | none |
| Investigate whether the system would disrupt current SPD workflow | planned | 2026-04-23 | 2026-04-30 | Technician UI And Workflow | UI / Baseline Workflow Defined | workflow | none |
| Investigate whether the system can be intuitive and plug-and-play | planned | 2026-04-23 | 2026-04-30 | Technician UI And Workflow | UI / Baseline Workflow Defined | ui | none |
| Investigate whether CV can reliably identify similar instruments | planned | 2026-04-23 | 2026-04-30 | Perception | Perception / Experiment Questions Locked | similar | none |
| Estimate training-data needs for similar-instrument recognition | planned | 2026-04-23 | 2026-04-30 | Perception | Perception / Experiment Questions Locked | similar | Investigate whether CV can reliably identify similar instruments |
| Design first similar-object recognition experiment | planned | 2026-04-23 | 2026-04-30 | Perception | Perception / Experiment Questions Locked | similar | Define initial question for similar-shape instrument recognition |
| Design first partial-occlusion experiment | planned | 2026-04-23 | 2026-04-30 | Perception | Perception / Experiment Questions Locked | occlusion | none |
| Plan graph of light intensity vs detection rate or mAP50-95 | planned | 2026-04-23 | 2026-04-30 | Perception | Perception / Experiment Questions Locked | lighting | Collect additional data for lighting experiment |
| Audit lighting dataset sessions and mark usable vs unusable folders | in_progress | 2026-04-23 | 2026-04-30 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Complete software image-collection setup |
| Standardize lighting-condition names across current dataset files | in_progress | 2026-04-23 | 2026-04-30 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Audit lighting dataset sessions and mark usable vs unusable folders |
| Export reproducible YOLO split for lighting experiment | planned | 2026-04-23 | 2026-04-30 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Standardize lighting-condition names across current dataset files |
| Verify train, val, and test manifests for lighting dataset | planned | 2026-04-23 | 2026-04-30 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Export reproducible YOLO split for lighting experiment |
| Define first similar-instrument class pairs to test | in_progress | 2026-04-23 | 2026-04-30 | Perception | Perception / Similar Baseline Ready | similar | Define initial question for similar-shape instrument recognition |
| Write short rationale for chosen similar-instrument pairs | planned | 2026-04-23 | 2026-04-30 | Perception | Perception / Similar Baseline Ready | similar | Define first similar-instrument class pairs to test |
| Collect additional data for lighting experiment | planned | 2026-04-30 | 2026-05-07 | Sensing And Capture | Sensing / Lighting Dataset Ready | lighting | Capture first qualitative lighting-variation examples with rough angle and distance notes |
| Investigate space and form-factor constraints for SPD deployment | planned | 2026-04-30 | 2026-05-07 | Sensing And Capture | Sensing / Collection Pipeline Ready | integration | none |
| Investigate deployment and maintenance expectations for the system | planned | 2026-04-30 | 2026-05-07 | Sensing And Capture | Sensing / Collection Pipeline Ready | ops | none |
| Run baseline lighting model on reference-only dataset | planned | 2026-04-30 | 2026-05-07 | Perception | Perception / Lighting Results Ready | lighting | Verify train, val, and test manifests for lighting dataset |
| Run expanded-lighting model on augmented lighting dataset | planned | 2026-04-30 | 2026-05-07 | Perception | Perception / Lighting Results Ready | lighting | Verify train, val, and test manifests for lighting dataset |
| Collect precision, recall, mAP50, and mAP50-95 into one table | planned | 2026-04-30 | 2026-05-07 | Perception | Perception / Lighting Results Ready | lighting | Run baseline lighting model on reference-only dataset |
| Select 6-10 representative glare-condition images | planned | 2026-04-30 | 2026-05-07 | Perception | Perception / Lighting Results Ready | lighting | Audit lighting dataset sessions and mark usable vs unusable folders |
| Collect initial image set for first similar-instrument pairs | planned | 2026-04-30 | 2026-05-07 | Perception | Perception / Similar Baseline Ready | similar | Define first similar-instrument class pairs to test |
| Organize raw similar-instrument images into a consistent folder structure | planned | 2026-04-30 | 2026-05-07 | Perception | Perception / Similar Baseline Ready | similar | Collect initial image set for first similar-instrument pairs |
| Re-run failed or inconsistent lighting jobs | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Lighting Results Ready | lighting | Run baseline lighting model on reference-only dataset |
| Confirm final lighting metrics to report | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Lighting Results Ready | lighting | Re-run failed or inconsistent lighting jobs |
| Build clean comparison table for lighting-training stages | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Lighting Results Ready | lighting | Confirm final lighting metrics to report |
| Write lighting results section | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Lighting Results Ready | docs | Build clean comparison table for lighting-training stages |
| Write lighting interpretation and limitation section | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Lighting Results Ready | docs | Write lighting results section |
| Review similar-instrument images and remove weak samples | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Similar Baseline Ready | similar | Organize raw similar-instrument images into a consistent folder structure |
| Export YOLO dataset for similar-instrument baseline | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Similar Baseline Ready | similar | Review similar-instrument images and remove weak samples |
| Verify split quality for similar-instrument dataset | planned | 2026-05-07 | 2026-05-14 | Perception | Perception / Similar Baseline Ready | similar | Export YOLO dataset for similar-instrument baseline |
| Train baseline similar-instrument detection model | planned | 2026-05-14 | 2026-05-21 | Perception | Perception / Similar Baseline Ready | similar | Verify split quality for similar-instrument dataset |
| Evaluate baseline model and record per-class metrics | planned | 2026-05-14 | 2026-05-21 | Perception | Perception / Similar Baseline Ready | similar | Train baseline similar-instrument detection model |
| Review false positives for similar classes | planned | 2026-05-14 | 2026-05-21 | Perception | Perception / Similar Baseline Ready | similar | Evaluate baseline model and record per-class metrics |
| Review false negatives for similar classes | planned | 2026-05-14 | 2026-05-21 | Perception | Perception / Similar Baseline Ready | similar | Evaluate baseline model and record per-class metrics |
| Save 5-8 confusing similar-tool examples | planned | 2026-05-14 | 2026-05-21 | Perception | Perception / Similar Baseline Ready | similar | Review false positives for similar classes |
| Write short confusion summary for worst similar pair | planned | 2026-05-14 | 2026-05-21 | Perception | Perception / Similar Baseline Ready | docs | Save 5-8 confusing similar-tool examples |
| Draft in-scope vs out-of-scope capability table | planned | 2026-05-14 | 2026-05-21 | Tray Logic And Decision Support | Tray Logic / Result Semantics Defined | scope | none |
| Draft prototype requirements section | planned | 2026-05-14 | 2026-05-21 | Tray Logic And Decision Support | Tray Logic / Result Semantics Defined | scope | Draft in-scope vs out-of-scope capability table |
| Decide whether manual correction is in scope this quarter | planned | 2026-05-14 | 2026-05-21 | Tray Logic And Decision Support | Tray Logic / Result Semantics Defined | scope | none |
| Document revised scope if manual correction is deferred | planned | 2026-05-14 | 2026-05-21 | Tray Logic And Decision Support | Tray Logic / Result Semantics Defined | docs | Decide whether manual correction is in scope this quarter |
| List top 5 mismatches between current UI and documented product concept | planned | 2026-05-21 | 2026-05-28 | Technician UI And Workflow | UI / Workflow Gap Review Complete | ui | none |
| Write current live-demo workflow description | planned | 2026-05-21 | 2026-05-28 | Technician UI And Workflow | UI / Workflow Gap Review Complete | docs | List top 5 mismatches between current UI and documented product concept |
| Add missing-item summary to Streamlit app | planned | 2026-05-21 | 2026-05-28 | Tray Logic And Decision Support | Tray Logic / Decision Support Implemented | ui | List top 5 mismatches between current UI and documented product concept |
| Add extra-item or over-count summary to Streamlit app | planned | 2026-05-21 | 2026-05-28 | Tray Logic And Decision Support | Tray Logic / Decision Support Implemented | ui | List top 5 mismatches between current UI and documented product concept |
| Add review-state indicator for risky detections | planned | 2026-05-21 | 2026-05-28 | Tray Logic And Decision Support | Tray Logic / Decision Support Implemented | ui | List top 5 mismatches between current UI and documented product concept |
| Capture before-and-after screenshots of updated UI | planned | 2026-05-21 | 2026-05-28 | Technician UI And Workflow | UI / Tray Review Flow Improved | ui | Add review-state indicator for risky detections |
| Define minimum tray-check record schema | planned | 2026-05-21 | 2026-05-28 | Traceability And Reporting | Traceability / Record Schema Ready | logging | none |
| Save scan ID and timestamp for each tray-check record | planned | 2026-05-21 | 2026-05-28 | Traceability And Reporting | Traceability / Logging Implemented | logging | Define minimum tray-check record schema |
| Save required-item list and observed counts to disk | planned | 2026-05-21 | 2026-05-28 | Traceability And Reporting | Traceability / Logging Implemented | logging | Define minimum tray-check record schema |
| Save missing-item results to disk | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Logging Implemented | logging | Save required-item list and observed counts to disk |
| Save per-detection confidence values to disk | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Logging Implemented | logging | Define minimum tray-check record schema |
| Save screenshot or frame reference for each tray check | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Logging Implemented | logging | Define minimum tray-check record schema |
| Draft lightweight quality-report format | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Reporting Ready | reporting | Save missing-item results to disk |
| Generate example tray-check report from prototype data | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Reporting Ready | reporting | Draft lightweight quality-report format |
| Update traceability doc to match implemented logging | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Reporting Ready | docs | Generate example tray-check report from prototype data |
| Build final logging or reporting figure pack | planned | 2026-05-28 | 2026-06-04 | Traceability And Reporting | Traceability / Reporting Ready | demo | Generate example tray-check report from prototype data |
| Build final UI screenshot pack | planned | 2026-05-28 | 2026-06-04 | Technician UI And Workflow | UI / Tray Review Flow Improved | demo | Capture before-and-after screenshots of updated UI |
| Write scripted tray-check walkthrough | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Write current live-demo workflow description |
| Run pilot walkthrough and record confusion points | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Write scripted tray-check walkthrough |
| Revise walkthrough script after pilot | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Run pilot walkthrough and record confusion points |
| Run walkthrough session 1 and record timing | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Revise walkthrough script after pilot |
| Run walkthrough session 2 and record timing | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Revise walkthrough script after pilot |
| Run walkthrough session 3 and record timing | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Revise walkthrough script after pilot |
| Summarize rescans, hesitations, and user complaints | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Run walkthrough session 3 and record timing |
| Summarize what users found helpful or clear | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Run walkthrough session 3 and record timing |
| Run wording comparison between assistant-mode and automation-mode language | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | workflow | Revise walkthrough script after pilot |
| Update workflow-acceptance doc with actual observations | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | docs | Summarize rescans, hesitations, and user complaints |
| Add limitation note about non-SPD participants | planned | 2026-06-04 | 2026-06-11 | Technician UI And Workflow | UI / Walkthrough Evidence Ready | docs | Update workflow-acceptance doc with actual observations |
| Choose best current model weights for final demo | planned | 2026-06-11 | 2026-06-18 | Perception | Perception / Demo Model Ready | demo | Confirm final lighting metrics to report |
| Build final lighting-results figure pack | planned | 2026-06-11 | 2026-06-18 | Perception | Perception / Demo Model Ready | demo | Write lighting interpretation and limitation section |
| Build final similar-instrument figure pack | planned | 2026-06-11 | 2026-06-18 | Perception | Perception / Demo Model Ready | demo | Write short confusion summary for worst similar pair |
| Select final demo scenario | planned | 2026-06-11 | 2026-06-18 | Technician UI And Workflow | UI / Demo Flow Ready | demo | Update workflow-acceptance doc with actual observations |
| Lock final class list for the demo | planned | 2026-06-11 | 2026-06-18 | Technician UI And Workflow | UI / Demo Flow Ready | demo | Select final demo scenario |
| Copy final weights into default demo path | planned | 2026-06-11 | 2026-06-18 | Technician UI And Workflow | UI / Demo Flow Ready | demo | Choose best current model weights for final demo |
| Run end-to-end demo verification test | planned | 2026-06-11 | 2026-06-18 | Technician UI And Workflow | UI / Demo Flow Ready | demo | Copy final weights into default demo path |
| Write live-demo script with fallback steps | planned | 2026-06-11 | 2026-06-18 | Technician UI And Workflow | UI / Demo Flow Ready | demo | Run end-to-end demo verification test |
