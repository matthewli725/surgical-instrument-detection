# GitLab Issue Planning Table

This file reformats the unit task list into a table so it is easier to copy
into GitLab issues, milestones, or a Gantt-style tracker.

Status values:

- `done`: work already completed
- `in_progress`: current active work
- `planned`: future work not yet started

## Weeks 1-3 Retrospective And Weeks 4-10 Forward Plan

| Issue Title | Week | Status | Category | Dependencies |
| --- | --- | --- | --- | --- |
| Schedule sterile processing facility tour outreach | 1 | done | research | none |
| Find candidate 3D models for surgical tools | 1 | done | hardware | none |
| Prepare printable files for initial surgical-tool set | 1 | done | hardware | Find candidate 3D models for surgical tools |
| Print first small set of 3D surgical-tool proxies | 1 | done | hardware | Prepare printable files for initial surgical-tool set |
| Follow up on SPD access and tour scheduling | 1 | done | ops | Schedule sterile processing facility tour outreach |
| Define initial question for similar-shape instrument recognition | 1 | done | similar | none |
| Define initial question for metallic-surface lighting robustness | 1 | done | lighting | none |
| Investigate whether spray-painted prints are a usable stainless-steel proxy | 1 | done | materials | none |
| Start website interface for displaying detection results | 2 | done | ui | none |
| Connect iPhone to Mac for frame capture workflow | 2 | done | capture | none |
| Upload and inspect individual cv2 frames from phone capture | 2 | done | capture | Connect iPhone to Mac for frame capture workflow |
| Contact additional people for hospital tour access | 2 | done | ops | Follow up on SPD access and tour scheduling |
| Visit Ronald Reagan UCLA Medical Center to ask about SPD tour access | 2 | done | ops | none |
| Email Muriel Lauranche requesting surgical room and SPD tour | 2 | done | ops | none |
| Synthesize research to narrow useful tool-identification scope | 2 | done | research | none |
| Compare spray-painted proxies against real stainless-steel goal | 2 | done | materials | Investigate whether spray-painted prints are a usable stainless-steel proxy |
| Plan physical image-capture setup | 2 | done | hardware | none |
| Design rigid camera-stand approach | 2 | done | hardware | Plan physical image-capture setup |
| Select fixed-color background for image capture | 2 | done | hardware | Plan physical image-capture setup |
| Plan variable lighting-angle and lighting-type setup | 2 | done | lighting | Plan physical image-capture setup |
| Refine website interface requirements | 2 | done | ui | Start website interface for displaying detection results |
| Identify online surgical-instrument datasets to combine | 2 | done | datasets | none |
| Compare dataset coverage and likely usefulness | 2 | done | datasets | Identify online surgical-instrument datasets to combine |
| Investigate visual properties that define object appearance | 2 | done | materials | none |
| Evaluate BRDF as a candidate representation for this project | 2 | done | materials | Investigate visual properties that define object appearance |
| Research real surgical-instrument material composition | 2 | done | materials | none |
| Capture silverware images under varied lighting as material proxy | 2 | done | lighting | Plan variable lighting-angle and lighting-type setup |
| Run initial retrain and retest cycle for model capability check | 2 | done | ml | none |
| Complete physical image-collection setup | 3 | done | capture | Design rigid camera-stand approach |
| Complete software image-collection setup | 3 | done | capture | Plan physical image-capture setup |
| Capture first qualitative lighting-variation examples with rough angle and distance notes | 3 | done | lighting | Complete physical image-collection setup |
| Research BRDF and related material-property representations | 3 | done | materials | Evaluate BRDF as a candidate representation for this project |
| Summarize dominant factors in human visual perception for this context | 3 | done | materials | Investigate visual properties that define object appearance |
| Review BRDF measurement requirements and practical constraints | 3 | done | materials | Research BRDF and related material-property representations |
| Assess whether BRDF measurement is overkill for this prototype | 3 | done | materials | Review BRDF measurement requirements and practical constraints |
| Investigate RGB specularity-removal alternatives | 3 | done | materials | Assess whether BRDF measurement is overkill for this prototype |
| Check whether silverware and surgical tools can share similar steel-alloy assumptions | 3 | done | materials | Research real surgical-instrument material composition |
| Synthesize existing research into one compelling project story | 3 | planned | cdr | Synthesize research to narrow useful tool-identification scope |
| Draft cost-benefit comparison of CV vs other technologies vs human labor | 3 | planned | research | Synthesize existing research into one compelling project story |
| Investigate likely SPD lighting conditions | 3 | planned | lighting | none |
| Investigate whether technicians work with overlapping instruments | 3 | planned | workflow | none |
| Investigate whether CV can reliably identify similar instruments | 3 | planned | similar | none |
| Estimate training-data needs for similar-instrument recognition | 3 | planned | similar | Investigate whether CV can reliably identify similar instruments |
| Investigate whether the system would disrupt current SPD workflow | 3 | planned | workflow | none |
| Investigate space and form-factor constraints for SPD deployment | 3 | planned | integration | none |
| Investigate whether the system can be intuitive and plug-and-play | 3 | planned | ui | none |
| Investigate deployment and maintenance expectations for the system | 3 | planned | ops | none |
| Design first similar-object recognition experiment | 3 | planned | similar | Define initial question for similar-shape instrument recognition |
| Design first partial-occlusion experiment | 3 | planned | occlusion | none |
| Collect additional data for lighting experiment | 3 | planned | lighting | Capture first qualitative lighting-variation examples with rough angle and distance notes |
| Plan graph of light intensity vs detection rate or mAP50-95 | 3 | planned | lighting | Collect additional data for lighting experiment |
| Audit lighting dataset sessions and mark usable vs unusable folders | 4 | in_progress | lighting | Complete software image-collection setup |
| Standardize lighting-condition names across current dataset files | 4 | in_progress | lighting | Audit lighting dataset sessions and mark usable vs unusable folders |
| Export reproducible YOLO split for lighting experiment | 4 | planned | lighting | Standardize lighting-condition names across current dataset files |
| Verify train, val, and test manifests for lighting dataset | 4 | planned | lighting | Export reproducible YOLO split for lighting experiment |
| Run baseline lighting model on reference-only dataset | 4 | planned | lighting | Verify train, val, and test manifests for lighting dataset |
| Run expanded-lighting model on augmented lighting dataset | 4 | planned | lighting | Verify train, val, and test manifests for lighting dataset |
| Collect precision, recall, mAP50, and mAP50-95 into one table | 4 | planned | lighting | Run baseline lighting model on reference-only dataset |
| Select 6-10 representative glare-condition images | 4 | planned | lighting | Audit lighting dataset sessions and mark usable vs unusable folders |
| Define first similar-instrument class pairs to test | 4 | in_progress | similar | Define initial question for similar-shape instrument recognition |
| Write short rationale for chosen similar-instrument pairs | 4 | planned | similar | Define first similar-instrument class pairs to test |
| Collect initial image set for first similar-instrument pairs | 4 | planned | similar | Define first similar-instrument class pairs to test |
| Organize raw similar-instrument images into a consistent folder structure | 4 | planned | similar | Collect initial image set for first similar-instrument pairs |
| Re-run failed or inconsistent lighting jobs | 5 | planned | lighting | Run baseline lighting model on reference-only dataset |
| Confirm final lighting metrics to report | 5 | planned | lighting | Re-run failed or inconsistent lighting jobs |
| Build clean comparison table for lighting-training stages | 5 | planned | lighting | Confirm final lighting metrics to report |
| Write lighting results section | 5 | planned | docs | Build clean comparison table for lighting-training stages |
| Write lighting interpretation and limitation section | 5 | planned | docs | Write lighting results section |
| Review similar-instrument images and remove weak samples | 5 | planned | similar | Organize raw similar-instrument images into a consistent folder structure |
| Export YOLO dataset for similar-instrument baseline | 5 | planned | similar | Review similar-instrument images and remove weak samples |
| Verify split quality for similar-instrument dataset | 5 | planned | similar | Export YOLO dataset for similar-instrument baseline |
| Train baseline similar-instrument detection model | 5 | planned | similar | Verify split quality for similar-instrument dataset |
| Evaluate baseline model and record per-class metrics | 5 | planned | similar | Train baseline similar-instrument detection model |
| Review false positives for similar classes | 5 | planned | similar | Evaluate baseline model and record per-class metrics |
| Review false negatives for similar classes | 5 | planned | similar | Evaluate baseline model and record per-class metrics |
| Save 5-8 confusing similar-tool examples | 5 | planned | similar | Review false positives for similar classes |
| Write short confusion summary for worst similar pair | 5 | planned | docs | Save 5-8 confusing similar-tool examples |
| Draft stakeholder table for TrayGuard | 6 | planned | cdr | none |
| Draft in-scope vs out-of-scope capability table | 6 | planned | cdr | none |
| Draft prototype requirements section | 6 | planned | cdr | Draft in-scope vs out-of-scope capability table |
| Draft unknowns and concerns section | 6 | planned | cdr | Confirm final lighting metrics to report |
| Build experiment-summary table for CDR | 6 | planned | cdr | Write short confusion summary for worst similar pair |
| Draft updated remainder-of-quarter milestones | 6 | planned | planning | Build experiment-summary table for CDR |
| Convert lighting experiment progress into engineering-work summary | 6 | planned | cdr | Write lighting interpretation and limitation section |
| Convert similar-instrument baseline into engineering-work summary | 6 | planned | cdr | Write short confusion summary for worst similar pair |
| Add current evidence vs remaining gap notes to experiment docs | 6 | planned | docs | Convert similar-instrument baseline into engineering-work summary |
| List top 5 mismatches between current UI and documented product concept | 7 | planned | ui | none |
| Write current live-demo workflow description | 7 | planned | docs | List top 5 mismatches between current UI and documented product concept |
| Decide whether manual correction is in scope this quarter | 7 | planned | scope | List top 5 mismatches between current UI and documented product concept |
| Document revised scope if manual correction is deferred | 7 | planned | docs | Decide whether manual correction is in scope this quarter |
| Add missing-item summary to Streamlit app | 7 | planned | ui | List top 5 mismatches between current UI and documented product concept |
| Add extra-item or over-count summary to Streamlit app | 7 | planned | ui | List top 5 mismatches between current UI and documented product concept |
| Add review-state indicator for risky detections | 7 | planned | ui | List top 5 mismatches between current UI and documented product concept |
| Capture before-and-after screenshots of updated UI | 7 | planned | ui | Add review-state indicator for risky detections |
| Define minimum tray-check record schema | 8 | planned | logging | none |
| Save scan ID and timestamp for each tray-check record | 8 | planned | logging | Define minimum tray-check record schema |
| Save required-item list and observed counts to disk | 8 | planned | logging | Define minimum tray-check record schema |
| Save missing-item results to disk | 8 | planned | logging | Save required-item list and observed counts to disk |
| Save per-detection confidence values to disk | 8 | planned | logging | Define minimum tray-check record schema |
| Save screenshot or frame reference for each tray check | 8 | planned | logging | Define minimum tray-check record schema |
| Draft lightweight quality-report format | 8 | planned | reporting | Save missing-item results to disk |
| Generate example tray-check report from prototype data | 8 | planned | reporting | Draft lightweight quality-report format |
| Update traceability doc to match implemented logging | 8 | planned | docs | Generate example tray-check report from prototype data |
| Write scripted tray-check walkthrough | 9 | planned | workflow | Write current live-demo workflow description |
| Run pilot walkthrough and record confusion points | 9 | planned | workflow | Write scripted tray-check walkthrough |
| Revise walkthrough script after pilot | 9 | planned | workflow | Run pilot walkthrough and record confusion points |
| Run walkthrough session 1 and record timing | 9 | planned | workflow | Revise walkthrough script after pilot |
| Run walkthrough session 2 and record timing | 9 | planned | workflow | Revise walkthrough script after pilot |
| Run walkthrough session 3 and record timing | 9 | planned | workflow | Revise walkthrough script after pilot |
| Summarize rescans, hesitations, and user complaints | 9 | planned | workflow | Run walkthrough session 3 and record timing |
| Summarize what users found helpful or clear | 9 | planned | workflow | Run walkthrough session 3 and record timing |
| Run wording comparison between assistant-mode and automation-mode language | 9 | planned | workflow | Revise walkthrough script after pilot |
| Update workflow-acceptance doc with actual observations | 9 | planned | docs | Summarize rescans, hesitations, and user complaints |
| Add limitation note about non-SPD participants | 9 | planned | docs | Update workflow-acceptance doc with actual observations |
| Select final demo scenario | 10 | planned | demo | Update workflow-acceptance doc with actual observations |
| Lock final class list for the demo | 10 | planned | demo | Select final demo scenario |
| Choose best current model weights for final demo | 10 | planned | demo | Confirm final lighting metrics to report |
| Copy final weights into default demo path | 10 | planned | demo | Choose best current model weights for final demo |
| Run end-to-end demo verification test | 10 | planned | demo | Copy final weights into default demo path |
| Build final lighting-results figure pack | 10 | planned | slides | Write lighting interpretation and limitation section |
| Build final similar-instrument figure pack | 10 | planned | slides | Write short confusion summary for worst similar pair |
| Build final UI screenshot pack | 10 | planned | slides | Capture before-and-after screenshots of updated UI |
| Build final logging or reporting figure pack | 10 | planned | slides | Generate example tray-check report from prototype data |
| Write final key-claims-and-evidence summary | 10 | planned | slides | Build final lighting-results figure pack |
| Write final risks-and-limitations summary | 10 | planned | slides | Draft unknowns and concerns section |
| Write live-demo script with fallback steps | 10 | planned | demo | Run end-to-end demo verification test |
| Review all docs for claims that exceed current evidence | 10 | planned | review | Write final risks-and-limitations summary |

## Suggested GitLab Labels

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
- `status::done`
- `status::in-progress`
- `status::planned`
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
