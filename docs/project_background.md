# TrayGuard Project Background

## Automated Surgical Tray Inspection Using Computer Vision

TrayGuard is a computer vision prototype for helping sterile processing technicians identify and count instruments in a surgical tray. The long-term goal is a camera-connected system that detects each instrument, compares the visible tray contents against the required list, and clearly shows which required tools are still missing.

This project addresses a documented sterile-processing workflow problem. Surgical instrument errors are commonly tied to missing instruments, wrong instruments, broken or poorly functioning instruments, and bioburden or debris. Visualization-heavy tasks such as identification, inspection, and sorting account for most observed errors in recent studies (Nichol et al., 2024, Nichol and Saari, 2023). TrayGuard is meant to reduce that burden by turning tray checking into a guided visual verification task while preserving technician confirmation as the final decision (Nichol et al., 2024, Natarus et al., 2025).

## Sterile Processing Context and Adoption Risk

Sterile processing is a safety-critical workflow. It is not just an image recognition problem. Central Sterile Processing Department and Sterile Processing Department work includes cleaning, disinfection, inspection, packaging, sterilization, and supply of reusable instruments. Defects in any step can affect operating-room timeliness, cost, and patient safety (Huang et al., 2025, Chen et al., 2023). This work also requires specialized knowledge. Technicians need to understand infection control, regulations, device handling, and practical inspection skills. Studies on CSSD training therefore emphasize structured on-the-job training (Hu et al., 2024, Ofstead et al., 2023).

Recent sterile-processing research makes the case for computer vision. It also shows why customers may hesitate. In one direct-observation study, researchers observed 236 surgical instrument errors across 147 cases. Missing instruments accounted for 160 errors. Broken or poorly functioning instruments accounted for 44 errors. Tray issues accounted for 13 errors. Visualization-related tasks accounted for 88.6% of all observed errors. The same study estimated that instrument delays cost the campus between $6,751,058.06 and $9,421,590.11 in annual lost chargeable OR minutes (Nichol et al., 2024). A separate study analyzed 33,839 surgical instrument packages. Wrong instrument specifications, incomplete packages, and missing instruments were the most common packaging errors (Zhu et al., 2019).

The task is also difficult because trays can be large and varied. A multi-specialty optimization study at Aarhus University Hospital selected 1,340 different instrument trays for optimization. The project reduced total instruments from 43,073 to 36,687 (Rubak et al., 2024). Another study looked at a Major General Surgery tray with 94 reusable instruments. An average of 19 instruments were used per case. Ten were never used (Eussen et al., 2026). These numbers make the visual task easier to understand. A technician is not just checking a few obvious tools. They may be checking a crowded tray where many items look similar and many items may not even be used.

This makes TrayGuard's value proposition plausible. Sterile processing contains repetitive visual tasks. Humans can miss, misidentify, or miscount instruments. Recent research also points to computer vision technologies as possible ways to reduce visualization-related errors (Nichol et al., 2024, Fayad et al., 2025). At the same time, a hospital buyer will not be satisfied by a model accuracy number alone. The system has to fit the workflow. It has to fail safely. It has to preserve technician authority. It also has to show that it reduces risk instead of creating another process to supervise (Natarus et al., 2025, Nichol et al., 2024). SPD improvement programs identify staffing, training, inventory management, physical environment, standard workflows, communication, and governance as separate drivers of defects. Technical accuracy alone is not enough (Natarus et al., 2025).

## Cost-Benefit Rationale for Computer Vision

Computer vision is attractive for this project because it can use commodity cameras and computers. It does not require us to modify every instrument. RFID and barcode systems usually require instrument-level tags, engraving, readers, antennas, or scanner workflows (Olivere et al., 2021, Kusuda et al., 2024, Zhu et al., 2019). RFID can be useful for utilization measurement and tray optimization. Published RFID studies still rely on tagging individual instruments and deploying readers or antennas (Olivere et al., 2021, Hill et al., 2022, Kusuda et al., 2024). That makes RFID better suited for full traceability programs. It is harder to justify for a low-cost visual-assistance prototype. Broader RFID literature also identifies high total spending and unclear return on investment as adoption barriers (Ting et al., 2013).

Hiring more staff is also not a simple substitute. A 2025 national survey of U.S. sterile-processing workers describes a severe shortage of skilled SPD technicians. It links the shortage to wage stagnation, high turnover, and increasing instrument complexity (Macola et al., 2025). The training pipeline is steep. In an AORN Journal survey, most respondents estimated three to six months or six to twelve months to train employees to process general and specialty instruments. The same paper calculated the 2008 cost to train one technician to competence at $41,414 including preceptor salary (Bridges, 2010). More staff can increase capacity. It does not remove the visual-recognition burden, interruption burden, or need for structured training (Hu et al., 2024, Huang et al., 2025, Ofstead et al., 2023).

The cost-benefit hypothesis for TrayGuard is narrow. CV is not a replacement for RFID traceability. It is not a replacement for trained technicians. It is a lightweight first layer for visual verification, missing-item detection, uncertainty flagging, and quality logging. It can be tested before a hospital commits to instrument-level tagging or major staffing expansion (Nichol et al., 2024, Fayad et al., 2025, Natarus et al., 2025).

| Option | Benefits | Costs / Risks | Why TrayGuard Starts With CV |
| --- | --- | --- | --- |
| Hire and train more SPD staff | Adds human capacity and expertise | Skilled-worker shortage, months-long training pipeline, recurring labor cost, persistent visual error risk | CV supports existing staff instead of depending on immediate hiring (Bridges, 2010, Macola et al., 2025, Nichol et al., 2024) |
| RFID or barcode tracking | Strong traceability and utilization data | Requires item-level tags, engraving, readers, antennas, scanning workflow, integration, and ROI justification | CV can pilot visual assistance without modifying every tool (Olivere et al., 2021, Kusuda et al., 2024, Ting et al., 2013) |
| Computer vision assistant | Low physical-infrastructure burden, rapid pilot, visual verification, uncertainty flags, screenshot/log evidence | Needs image-quality controls, confidence calibration, and human confirmation | Matches the visualization failure mode that dominates observed errors (Nichol et al., 2024, Fayad et al., 2025) |

### Failure Modes and Customer Hesitations

The main risks fall into two groups.

**Computer vision failure modes**

- Similar-looking instruments may be confused. This matters because wrong-specification instruments were the largest packaging-error category in Zhu et al. (2019).
- Reflective metal, glare, shadows, water, residue, and tray surfaces may change the visible appearance. Visual inspection is a known weak point in sterile processing (Nichol and Saari, 2023, Nichol et al., 2024).
- Clutter and overlap may cause missed instruments, merged detections, or double counts. Large trays and oversupplied trays increase workload and visual complexity (Hill et al., 2022, Rubak et al., 2024, Eussen et al., 2026).
- Unknown instruments may be forced into the closest known class. This matters because hospital tray inventories include many tray types and specialty-specific variants (Rubak et al., 2024).
- Damaged, wet, contaminated, or partially assembled instruments may look different from training images. Broken instruments and bioburden are documented error categories (Nichol et al., 2024, Chen et al., 2023).
- Confidence scores may be poorly calibrated. A wrong prediction can look certain. A correct prediction can look uncertain. This motivates confidence and review experiments (Nichol et al., 2024, Natarus et al., 2025).
- The system detects visual identity. It cannot prove sterility, sharpness, internal cleanliness, or function. The prototype should stay framed as decision support (Ofstead et al., 2023, Nichol et al., 2024).

**Hospital deployment and workflow risks**

- Technicians may see the tool as slower than the current process. We should measure time and correction burden directly (Huang et al., 2025, Natarus et al., 2025).
- The system may require camera setup, tray staging, rescans, label correction, or exception handling. These extra steps matter because workflow design is a known driver of SPD defects (Natarus et al., 2025).
- The system may not integrate with tray count sheets, preference cards, barcode workflows, instrument tracking systems, or quality reporting. Tracking and tray-optimization studies depend on structured instrument records (Zhu et al., 2019, Olivere et al., 2021, Rubak et al., 2024).
- Hospital leaders may question ROI because staff-reported instrument-error systems can underreport events and lose delay information (Nichol et al., 2024).
- Audit and infection-control concerns require logs and human confirmation. Sterile-processing defects affect patient safety and operating-room readiness (Chen et al., 2023, Natarus et al., 2025).
- Camera drift, lighting changes, dirty lenses, software downtime, and model drift could create new risks. Deployment should include quality checks and not only model accuracy (Natarus et al., 2025).
- A fully automated replacement narrative may threaten technician trust. A decision-support framing better matches the literature on training, human expertise, and quality improvement (Hu et al., 2024, Ofstead et al., 2023, Natarus et al., 2025).

## Current Focus

Because we do not have access to a full set of real surgical instruments, and because collecting a broad surgical dataset is outside the scope of this prototype timeline, we are building evidence along several controlled experiment axes. Instead of claiming full deployment readiness, we are testing whether the core computer vision assumptions hold under conditions that resemble the hard parts of surgical tray inspection.

The current system supports these functions.

- Camera-based image collection
- Manual bounding-box annotation
- Reusing labels across controlled lighting variants
- Exporting collected images to YOLO format
- Training and benchmarking object detection models
- Running a Streamlit tray-check UI for live camera detections

## Proposed Experiments

Detailed experiment plans live in `docs/experiments/`.

- `docs/experiments/shape_similarity.md`
- `docs/experiments/reflectivity_lighting.md`
- `docs/experiments/clutter_occlusion.md`
- `docs/experiments/open_set_confidence.md`
- `docs/experiments/workflow_acceptance.md`
- `docs/experiments/traceability_reporting.md`

### 1. Shape Similarity

**Question** Can the model distinguish between objects that have similar outlines but different identities?

This tests a central recognition challenge in surgical tray assembly. Packaging studies show that wrong-specification instruments are a common error category. Visualization studies identify identification and sorting as weak points in sterile processing (Zhu et al., 2019, Nichol and Saari, 2023, Nichol et al., 2024). The system therefore needs to learn subtle differences in shape, tip geometry, handle structure, and relative proportions (Zhu et al., 2019, Fayad et al., 2025).

**Proposed setup**

- Collect images of visually similar tools.
- Keep lighting and background mostly stable.
- Train the detector on multiple shape classes.
- Evaluate whether the model confuses similarly shaped objects.

**Success indicators**

- High per-class precision and recall for visually similar classes
- Low confusion between paired classes, such as straight vs. curved instruments
- Reasonable detection confidence when objects are rotated or slightly repositioned

### 2. Material and Lighting Robustness

**Question** Can the model remain reliable when reflective or metallic objects appear under different lighting conditions?

Surgical instruments are commonly reusable metal tools. Sterile-processing studies emphasize inspection of instrument condition, cleanliness, and function as visual tasks. This motivates testing whether lighting and reflective surfaces degrade a camera-based detector (Nichol and Saari, 2023, Nichol et al., 2024, Ofstead et al., 2023). Our data collection workflow is designed around this issue. One setup can be annotated once and then captured repeatedly under different lighting conditions.

**Proposed setup**

- Place a fixed set of objects in a tray or tray-like area.
- Capture one annotated reference image.
- Capture lighting variants with changed light angle, brightness, glare, and shadow.
- Train and evaluate on lighting conditions not seen during training.

**Success indicators**

- Stable detections across lighting variants
- Limited confidence drop under glare or shadow
- Better performance when lighting augmentation or multi-lighting training data is used

### 3. Clutter and Occlusion

**Question** Can the model detect and count instruments when objects are close together, overlapping, or partially occluded?

Real trays can be large and visually dense. A Major General Surgery tray in one prospective study contained 94 reusable instruments. Hospital-wide tray optimization at Aarhus University Hospital involved 1,340 tray types and more than 43,000 instruments before redesign (Eussen et al., 2026, Rubak et al., 2024). A useful tray inspection system must measure how touching, overlap, and occlusion affect visible-tool counting (Nichol et al., 2024).

**Proposed setup**

- Create tray scenes with increasing clutter levels.
- Start with separated objects, then move to touching objects, partial overlap, and heavier occlusion.
- Evaluate detection quality at each clutter level.

**Success indicators**

- Accurate counts in low and moderate clutter
- Graceful degradation as occlusion increases
- Clear failure cases where the system can flag low confidence instead of silently miscounting

### 4. Open-Set Recognition and Confidence Calibration

**Question** Does the system know when it does not know?

Hospitals will not trust a tray-check system that confidently mislabels an unfamiliar instrument because wrong instruments, wrong specifications, and missing instruments are documented sterile-processing error categories (Zhu et al., 2019, Nichol et al., 2024). This experiment tests whether TrayGuard can reject unknown tools, flag low-confidence cases, and avoid forcing every object into one of the known classes.

**Proposed setup**

- Train on the known prototype classes.
- Test on visually similar but intentionally unknown tools.
- Compare true known-class detections against unknown-object false positives.
- Evaluate whether confidence thresholds and "needs review" states catch risky predictions.

**Success indicators**

- Unknown tools are rejected or flagged rather than confidently mislabeled.
- Confidence is lower on ambiguous, occluded, or glare-heavy cases.
- A practical threshold can reduce dangerous false confirmations while keeping the UI usable.

### 5. Workflow Acceptance and Throughput

**Question** Would a technician actually want to use the system during tray assembly?

This addresses the UCLA anecdote directly. Published implementation research supports the same concern. SPD improvement work identifies staffing, training, inventory management, physical environment, workflow, communication, and governance as drivers of tray defects (Natarus et al., 2025). A model should therefore be evaluated as a technician-facing support tool. Adoption should also account for the specialized training and visual-inspection skills required of sterile-processing professionals (Hu et al., 2024, Ofstead et al., 2023).

**Proposed setup**

- Simulate a tray assembly checklist with and without TrayGuard.
- Measure task time, number of manual corrections, number of rescans, and perceived workload.
- Record where users hesitate, override the model, or ask for more explanation.
- Compare "assistant mode" against "automation mode" language in the UI.

**Success indicators**

- The UI reduces missed items without adding unacceptable time.
- Users understand uncertain detections and can correct them quickly.
- The system preserves human confirmation rather than pretending to replace the technician.

### 6. Traceability and Quality Reporting

**Question** Can the system produce evidence that matters to a hospital buyer?

Hospitals may underreport tray defects. Nichol et al. found that staff reporting captured far fewer cases than direct observation. Incomplete reporting also limited delay analysis (Nichol et al., 2024). TrayGuard should therefore log detections, uncertain items, corrections, missing instruments, and recurring failure patterns.

**Proposed setup**

- Save per-tray detection results, manual corrections, confidence values, and missing-item lists.
- Group errors by class, lighting condition, clutter level, and tray setup.
- Produce a simple quality report that shows repeatable patterns instead of isolated screenshots.

**Success indicators**

- Each tray check has an auditable record.
- Repeated model or workflow failure modes are visible.
- The output can support a buyer-facing argument about risk reduction, technician support, and process improvement.

## System Concept

TrayGuard is intended to become an interactive tray-checking system.

1. A technician loads the required instrument list for a tray by scanning a barcode.
2. A camera captures the current tray state.
3. The detector identifies and counts visible instruments.
4. The interface shows collected tools, missing tools, and uncertain detections.
5. The technician confirms or corrects the result before the tray is completed.

The current repository focuses on the computer vision foundation. This includes data collection, labeling, dataset export, model training, and model evaluation.

## Evaluation Plan

For each experiment axis, we plan to report these results.

- Dataset size and class list
- Train, validation, and test split strategy
- Mean average precision or other detector metrics
- Per-class precision and recall
- Confusion between similar classes
- Example successes and failures
- Qualitative screenshots of detections
- Unknown-object rejection rate
- Confidence calibration and low-confidence review rate
- Count error per tray
- Time-to-check and number of user corrections in the UI
- Repeated error categories suitable for quality reporting

The strongest final result would not be a claim that TrayGuard is ready for operating-room deployment. Instead, it would show that the main risks are testable, that the prototype works under controlled approximations of those risks, and that the same pipeline could scale to real surgical instruments once real data is available.

## References

- Bridges, ["The Real Costs of Surgical Instrument Training in Sterile Processing Revisited"](https://doi.org/10.1016/j.aorn.2009.10.025), AORN Journal, 2010.
- Chen et al., ["Incidence of Adverse Events in Central Sterile Supply Department: A Single-Center Retrospective Study"](https://doi.org/10.2147/RMHP.S423108), Risk Management and Healthcare Policy, 2023.
- Fayad et al., ["Traceability of Surgical Instruments: A Systematic Review"](https://doi.org/10.3390/app15031592), Applied Sciences, 2025.
- Hu et al., ["Improvement and implementation of central sterile supply department training program based on action research"](https://link.springer.com/article/10.1186/s12912-024-01809-z), BMC Nursing, 2024.
- Huang et al., ["Situations and demands of central sterile supply department training on nursing interruptions"](https://link.springer.com/article/10.1186/s12913-024-12190-7), BMC Health Services Research, 2025.
- Kusuda et al., ["Comparison of Reading Times of RFID-Tagged and Barcode-Engraved Surgical Instruments"](https://doi.org/10.1016/j.jss.2024.09.087), Journal of Surgical Research, 2024.
- Macola et al., ["An analysis of the economic challenges facing central sterile processing employees in the United States: Results of a national survey"](https://doi.org/10.1016/j.pcorm.2025.100520), Perioperative Care and Operating Room Management, 2025.
- Natarus et al., ["Optimization of a Sterile Processing Department Using Lean Six Sigma Methodology, Staffing Enhancement, and Capital Investment"](https://doi.org/10.1016/j.jcjq.2024.10.006), The Joint Commission Journal on Quality and Patient Safety, 2025.
- Nichol et al., ["Observed rates of surgical instrument errors point to visualization tasks as being a critically vulnerable point in sterile processing and a significant cause of lost chargeable OR minutes"](https://link.springer.com/article/10.1186/s12893-024-02407-1), BMC Surgery, 2024.
- Nichol and Saari, ["Patterns in staff reported surgical instrument errors point to failures in visualization as a critically weak point in sterile processing of surgical instruments"](https://doi.org/10.1016/j.pcorm.2023.100356), Perioperative Care and Operating Room Management, 2023.
- Hill et al., ["Measuring intraoperative surgical instrument use with radio-frequency identification"](https://doi.org/10.1093/jamiaopen/ooac003), JAMIA Open, 2022.
- Olivere et al., ["Radiofrequency Identification Track for Tray Optimization: An Instrument Utilization Pilot Study in Surgical Oncology"](https://doi.org/10.1016/j.jss.2021.02.049), Journal of Surgical Research, 2021.
- Ofstead et al., ["Improving mastery and retention of knowledge and complex skills among sterile processing professionals: A pilot study on borescope training and competency testing"](https://doi.org/10.1016/j.ajic.2023.03.002), American Journal of Infection Control, 2023.
- Rubak et al., ["Surgical instrument tray optimization process at a university hospital: A comprehensive overview"](https://doi.org/10.1016/j.sopen.2024.09.007), Surgery Open Science, 2024.
- Ting et al., ["Impact of Radio-Frequency Identification (RFID) Technologies on the Hospital Supply Chain: A Literature Review"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3797551/), Perspectives in Health Information Management, 2013.
- Eussen et al., ["Surgical tray optimization: a prospective and survey-based evaluation of environmental and economic outcomes"](https://doi.org/10.1007/s00464-025-12499-2), Surgical Endoscopy, 2026.
- Zhu et al., ["Errors in packaging surgical instruments based on a surgical instrument tracking system: an observational study"](https://link.springer.com/article/10.1186/s12913-019-4007-3), BMC Health Services Research, 2019.

Regulatory and practice context

- CDC, ["Sterilizing Practices"](https://www.cdc.gov/infection-control/hcp/disinfection-sterilization/sterilizing-practices.html), Guideline for Disinfection and Sterilization in Healthcare Facilities.
- FDA, ["Reprocessing of Reusable Medical Devices"](https://www.fda.gov/medical-devices/products-and-medical-procedures/reprocessing-reusable-medical-devices/).
