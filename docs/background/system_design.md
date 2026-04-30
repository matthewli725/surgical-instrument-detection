# System Design

## Current Focus

Because we do not have access to a full set of real surgical instruments, and
because collecting a broad surgical dataset is outside the scope of this
prototype timeline, we are building evidence along several controlled
experiment axes. Instead of claiming full deployment readiness, we are testing
whether the core computer vision assumptions hold under conditions that
resemble the hard parts of surgical tray inspection.

The current system supports these functions.

- Camera-based image collection
- Manual bounding-box annotation
- Reusing labels across controlled lighting variants
- Exporting collected images to YOLO format
- Training and benchmarking object detection models
- Running a Streamlit tray-check UI for live camera detections

## Prototype Scope

TrayGuard should be described as a technician-centered verification assistant,
not as a fully autonomous tray-approval station. The useful system-design
question for this repository is therefore: what information should the
prototype take in, what should it produce, what pieces does it need, and what
should stay explicitly out of scope?

### In Scope For This Prototype

- Detect known instrument classes in tray-like scenes using a camera and an
  object detector.
- Count visible detections by class and compare them against a required list.
- Show the live tray state in a technician-facing interface.
- Surface missing-item, extra-item, and review-needed situations clearly enough
  to support human confirmation.
- Produce evidence that helps us study lighting, clutter, confusion, open-set,
  and workflow-fit risks.
- Support lightweight logging and reporting as a prototype quality-improvement
  story.

### Out Of Scope For This Prototype

- Autonomous tray approval without human confirmation.
- Proof of sterility, cleanliness, sharpness, alignment, or instrument
  mechanical function.
- Hospital-wide inventory tracking, sterilization records, or full instrument
  traceability across departments.
- Robotic manipulation, sorting, or closed-loop tray assembly.
- Broad claims about deployment readiness in real SPD operations.

## Core System Information

The core tray-checking task is simple in structure even if it is difficult in
practice:

1. Load or enter the required instrument list for a tray.
2. Capture the current tray view with a camera.
3. Detect visible instruments and assign class labels with confidence scores.
4. Aggregate detections into observed class counts.
5. Compare observed counts against required counts.
6. Present a technician-facing result that highlights what appears present,
   missing, extra, or uncertain.
7. Preserve the final decision as human judgment rather than silent automation.

This framing keeps the product centered on visual verification support. It also
matches the strongest current adoption argument: reduce visual search burden,
make uncertainty legible, and create useful review evidence without replacing
technician authority.

## Design Lessons From Close Prior Work

Rodrigues, Mayo, and Patros's HOSPITools study gives direct motivation for
TrayGuard's controlled experiment plan. Their surgical-tool dataset was built
for intelligent surgical-tool management, included 360 tool classes organized
across speciality, pack, set, and tool levels, and was evaluated under concrete
design variables: image size, class frequency, lighting/background variation,
held-out test data, and hierarchy-aware similarity
([Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)).
Most importantly for this project, they state that fine-grained tool
classification is difficult because many surgical tools are visually similar and
differ only in subtle ways. That supports treating shape similarity, data
scarcity, capture conditions, and condition-held-out evaluation as first-class
experiment questions rather than incidental implementation details.

Atabuzzaman et al.'s 2025 CVPR Workshop paper, "Real-Time Ultra-Fine-Grained
Surgical Instrument Classification," is the closest academic
precedent for TrayGuard's computer-vision direction. It targets a hospital CSSD workflow, uses real surgical
tray categories, and focuses on ultra-fine-grained distinctions between
visually similar instruments
([Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025)).

The paper supports several system-design choices:

- **Structured capture matters.** Their initial single-view setup performed
  poorly enough to motivate a dual-camera acquisition station. Their final
  design captures top and side views, including a side-angle view aimed at
  fine-grained tip details such as curvature, surface texture, and tooth
  pattern. TrayGuard should therefore treat camera placement as part of the
  product, not as a removable demo detail.
- **Multi-view evidence is useful for fine-grained tools.** Their architecture
  fuses top-view and side-view features because different views preserve
  different discriminative cues. For TrayGuard, the analogous requirement is to
  keep a future path open for multi-view capture, especially for instrument
  families that remain confusable from overhead imagery alone.
  Multi-view classification research supports this broader design idea: when a
  single image does not contain enough discriminative information, multiple
  literal views of the same object can improve classification
  ([Seeland and Mader, 2021](../bibliography.md#seeland-and-mader-2021)).
- **Real CSSD evaluation is possible but bounded.** Their deployment and user
  study show that CSSD-oriented instrument recognition can improve workflow
  efficiency. However, their task is one-instrument classification, not
  full-tray verification. TrayGuard should cite this as evidence that the
  technical direction is plausible, while still separately validating tray-level
  missing, extra, wrong-item, and review-needed behavior.
- **High accuracy does not remove failure-mode analysis.** A constrained
  platform can achieve excellent classification results, but a tray assistant
  still has to answer what happens under glare, colored light, occlusion,
  unknown instruments, and high-confidence similar-class confusion. Those
  questions remain part of TrayGuard's differentiating design work rather than
  a solved problem.

The practical design implication is that TrayGuard should separate two sensing
modes. A tray-overview mode is useful for counting visible instruments and
finding missing or extra items against a required list. A future
single-instrument review mode, inspired by the two-view station in Atabuzzaman
et al., could be used when the overview model flags a similar-looking or
low-confidence item. This keeps the current prototype aligned with its
tray-level verification goal while acknowledging that ultra-fine-grained
classification may need more controlled imaging than a single overhead tray
view can provide.

## Research Support Audit

This section provides evidence for our design decisions. A
choice can stay in the project only if it is either supported by evidence,
framed as a bounded prototype assumption, or converted into something we will
measure locally.

| Design Choice | Research Support | Defensible Stance |
| --- | --- | --- |
| Technician-centered assistant instead of autonomous approval | SPD error research supports the need for better visual verification, while healthcare AI literature warns about automation bias, deskilling, liability, and workflow fit ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Goddard et al., 2012](../bibliography.md#goddard-et-al-2012), [Natali et al., 2025](../bibliography.md#natali-et-al-2025), [Kelly, 2026](../bibliography.md#kelly-2026), [Zheng et al., 2023](../bibliography.md#zheng-et-al-2023)). | Keep the final decision human. The system may flag, count, explain, and log, but it should not silently approve trays. |
| Workspace observation as the first architecture | Visualization-related errors dominate observed instrument errors, and direct CV studies show surgical-tool detection/counting is feasible. RFID/barcode work supports traceability, but it also requires tags, readers, engraving, antennas, or scanner workflows ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). | Keep CV as the lowest-infrastructure prototype layer. Do not claim it is universally superior to RFID or barcode traceability. |
| Structured capture rather than arbitrary webcam input | Controlled surgical-instrument recognition studies use constrained lighting, background, and acquisition platforms; the closest CSSD paper moved to multi-view capture for fine-grained details ([Lehr et al., 2023](../bibliography.md#lehr-et-al-2023), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Seeland and Mader, 2021](../bibliography.md#seeland-and-mader-2021)). | Keep the overhead tray view for counting visible objects, but preserve a future side-view or single-instrument review path for confusable instruments. |
| Object detection plus count aggregation | Automated surgical-instrument detection/counting has direct proof-of-concept support. General object-detection benchmarks also make bounding boxes and per-instance localization a standard way to evaluate visible objects in scenes ([Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Lin et al., 2014](../bibliography.md#lin-et-al-2014)). | Detect and count visible instruments. Do not infer fully hidden instruments from context. |
| YOLO-format datasets and a real-time detector baseline | YOLO is research-backed as a real-time object-detection family, and RT-DETR is a credible real-time transformer alternative ([Redmon et al., 2016](../bibliography.md#redmon-et-al-2016), [Zhao et al., 2024 RT-DETR](../bibliography.md#zhao-et-al-2024-rtdetr)). | Treat `yolo11s` as the current implementation baseline, not a research conclusion. Keep the model layer benchmarkable across YOLO sizes and RT-DETR. |
| Confidence threshold and "needs review" states | Open-set recognition research shows closed-set assumptions break when unknown classes appear. Calibration research shows modern neural-network confidence can be poorly calibrated, and healthcare uncertainty-display studies support making uncertainty visible ([Scheirer et al., 2013](../bibliography.md#scheirer-et-al-2013), [Schlachter et al., 2020](../bibliography.md#schlachter-et-al-2020), [Guo et al., 2017](../bibliography.md#guo-et-al-2017), [Kim et al., 2025](../bibliography.md#kim-et-al-2025)). | Use confidence as a review trigger, not as a safety probability. Tune thresholds on local validation data and report false confirmations and review burden. |
| Controlled lighting variants and label reuse | Specular highlights are a known CV problem, controlled surgical-instrument papers treat lighting as an acquisition variable, and augmentation research supports label-preserving image variation when the object geometry and class remain unchanged. HOSPITools also captured surgical tools under natural, LED, halogen, and fluorescent lighting, making illumination a documented surgical-tool dataset variable rather than a demo-only concern ([Wang et al., 2016](../bibliography.md#wang-et-al-2016), [Wei et al., 2018](../bibliography.md#wei-et-al-2018), [Lehr et al., 2023](../bibliography.md#lehr-et-al-2023), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Shorten and Khoshgoftaar, 2019](../bibliography.md#shorten-and-khoshgoftaar-2019), [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)). | Reuse boxes only for controlled lighting variants where the object pose is unchanged. Evaluate on held-out lighting conditions rather than random near-duplicate splits. |
| Synthetic data for shape-similarity stress tests | Domain-randomization research supports synthetic-to-real transfer only when variation is broad enough and transfer is measured. Surgical-tool dataset surveys reinforce that dataset assumptions must be explicit, and HOSPITools shows the same need to evaluate dataset design variables such as class frequency, image size, and acquisition conditions rather than assuming one dataset construction is enough ([Tobin et al., 2017](../bibliography.md#tobin-et-al-2017), [Shorten and Khoshgoftaar, 2019](../bibliography.md#shorten-and-khoshgoftaar-2019), [Rodrigues et al., 2022a](../bibliography.md#rodrigues-et-al-2022a), [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)). | Use simulation for controlled stress testing, but claim value only if synthetic pretraining improves a matched real-proxy baseline. |
| Pairwise confusion and high-confidence wrong-class metrics | Fine-grained recognition literature frames subtle inter-class differences as the central risk, and direct surgical-instrument work shows clinically distinct tools can be visually similar. HOSPITools explicitly motivates this point: many surgical tools are visually similar and differ in subtle, hard-to-discern ways ([Wang et al., 2021](../bibliography.md#wang-et-al-2021), [Zhao et al., 2017](../bibliography.md#zhao-et-al-2017), [Lehr et al., 2023](../bibliography.md#lehr-et-al-2023), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025), [Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b)). | Do not rely on average mAP alone. Report per-class metrics, pairwise confusion, and high-confidence wrong similar-class predictions. |
| Held-out splits and dataset-design reporting | HOSPITools reserved images for a test set not seen during training and used experiments to study image size and class frequency. ML reproducibility guidance also supports recording dataset and model details ([Rodrigues et al., 2022b](../bibliography.md#rodrigues-et-al-2022b), [Heil et al., 2021](../bibliography.md#heil-et-al-2021)). | Keep train, validation, and test splits explicit. Report class list, image count, instance count, split rule, and the design variable each experiment isolates. |
| Local/no-PHI prototype data handling | Healthcare AI adoption literature identifies privacy, legal, and data-governance requirements as major deployment barriers ([Khalid et al., 2023](../bibliography.md#khalid-et-al-2023), [Chomutare et al., 2022](../bibliography.md#chomutare-et-al-2022)). | Keep prototype records focused on trays, detections, timestamps, and model versions. This reduces risk, but it is not a substitute for formal hospital privacy review. |
| Lightweight traceability records | Surgical-instrument traceability reviews and error-reporting studies support keeping usable evidence for quality improvement. ML reproducibility standards support recording model/data details ([Fayad et al., 2025](../bibliography.md#fayad-et-al-2025), [Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023), [Heil et al., 2021](../bibliography.md#heil-et-al-2021)). | Save scan ID, required list, observed counts, confidence values, review flags, corrections, screenshot references, dataset version, and model version. |
| Hard P6-style numeric targets | Several old numbers were useful ambition but not research-backed for SPD tray verification: one false alert per eight hours, two user actions, ten-minute setup, and fixed `0.5 m x 0.5 m` coverage. | Do not defend those as requirements. Replace them with local measurement plans until walkthrough and physical capture data exist. |

## Implementation Defaults That Should Not Be Overclaimed

Some repository choices are good engineering defaults, not claims about the
best possible clinical design.

| Default | Current Use | Critique-Ready Interpretation |
| --- | --- | --- |
| `model=yolo11s` | Fast baseline for training and demo inference. | Supported only as a YOLO-family real-time detector baseline. Compare with `yolo11m`, `yolo11l`, and `rtdetr-l` when performance claims matter. |
| `conf=0.25` | Demo slider default. | Not a safety threshold. Choose operating thresholds from validation curves, unknown false-positive rates, and review burden. |
| `imgsz=640`, `epochs=100`, `batch=16` | Reproducible training defaults. | Treat as starting points. Report them, tune when needed, and avoid presenting them as research-backed optima. |
| Streamlit UI | Fast prototype interface for live camera review. | Suitable for demonstrating workflow concepts. Production UI claims need separate usability testing and implementation work. |
| Local ignored `data/`, `runs/`, and `weights/` folders | Keeps raw images, training outputs, and weights out of git. | Sensible prototype hygiene. Formal deployment would require access controls, retention policy, audit policy, and privacy review. |

## Main Components

The current product concept can be understood as seven components:

1. **Imaging And Inspection**
   - Camera, scene framing, and practical lighting conditions.
   - The main risk here is image quality degradation from glare, shadow,
     reflectivity, blur, and camera placement.
   - Close prior work suggests that a single overhead view may be insufficient
     for ultra-fine-grained instrument distinctions, so the sensing design
     should preserve a path to side-view or review-station capture when needed.
2. **Edge Compute And Operator Interface**
   - Local runtime, display, user controls, and status indicators.
   - The prototype should keep session data local by default and avoid patient
     information entirely. This is a risk-reduction choice aligned with
     healthcare AI privacy concerns, not a complete compliance claim.
3. **Workflow Orchestration**
   - Tray-session state, capture, inference, validation, review, rescan, and
     completion flow.
   - Human-in-the-loop actions such as confirm, override, and recapture belong
     here rather than inside the detector.
4. **Computer Vision Inference**
   - Detection model, confidence scores, and class-level predictions.
   - The main risk here is confusion between similar tools, missed detections,
     and unsafe high-confidence errors.
   - The model should distinguish tray-level detection from single-instrument
     classification, since the latter can be tested under more controlled views.
   - The current YOLO-based implementation is an experiment baseline. The
     architecture should stay swappable so model-family comparisons remain
     possible.
5. **Tray Validation And Decision Support**
   - Required-list parsing, observed-count aggregation, and tray-status logic.
   - This is where the system turns raw detections into missing, extra, and
     review-needed information.
   - Future versions should support allowed alternates, confidence thresholds,
     and strict or relaxed review modes only when those rules are explicit.
6. **Knowledge Management**
   - Tray definitions, required instrument lists, label taxonomy, and model
     version alignment.
   - This avoids a quiet mismatch between model class names and the tray
     definition being checked.
7. **Data Lifecycle And Reporting**
   - Saved results, confidence values, screenshots or frame references, and
     repeat-pattern reporting.
   - This is necessary for a buyer-facing quality story, not just demo output.

## Design Candidates And Selection

The design space can be described as three candidate architectures.

| Candidate | Description | Advantages | Main Limits |
| --- | --- | --- | --- |
| Workspace observation | Use a camera and computer vision model to detect visible instruments, count known classes, and compare the counts against a required list. | Does not require modifying instruments or replacing trays; matches the visual-verification failure mode; can be piloted with commodity hardware. | Sensitive to lighting, reflectivity, occlusion, similar-class confusion, and open-set objects. |
| Tagged identification | Add RFID tags, barcodes, or other identifiers to instruments and read the identifiers during tray preparation. | Strong item-level identity and traceability; less dependent on visual conditions. | Requires tags, engraving, readers, scanner workflows, integration, and maintenance. RFID and barcode studies support traceability value but also show infrastructure and workflow costs ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). |
| Instrumented placement | Use custom tray slots or embedded sensors to confirm that expected locations are occupied. | Can make placement checks simple in a highly standardized tray. | Requires specialized trays, restricts tray-layout flexibility, and does not naturally identify wrong-but-similar instruments. |

TrayGuard currently selects workspace observation because it is the best match
for this repository's constraints: low physical-infrastructure burden, direct
study of the visual inspection problem, and compatibility with the existing
camera, annotation, YOLO export, model-training, and Streamlit demo pipeline.
This is a prototype selection rather than a claim that computer vision is always
superior to RFID or tray instrumentation. For a hospital-wide traceability
program, RFID or barcode systems may be the right architecture; for this project,
computer vision is the most testable first layer of tray-readiness support.

## Fallback Strategy

The selected architecture should have graceful fallback paths.

| Level | Trigger | Fallback | What It Preserves |
| --- | --- | --- | --- |
| Sensing | Glare, shadow, or camera placement makes detections unstable. | Add controlled lighting, fixed background, clearer tray staging, or a side/review view. | The workspace-observation concept remains intact while reducing image-quality variation. |
| Perception | Fine-grained class recognition is unreliable for visually similar instruments. | Route low-confidence or similar-pair cases into review, or count broader instrument groups when that still answers the tray question. | The system still supports verification without pretending every class distinction is solved. |
| Interaction | Alerts or rescans slow the user. | Switch from automation-style results to guided review language, clearer rescan prompts, and fewer high-interruption alerts. | Technician authority and workflow acceptance remain central. |
| Architecture | Workspace observation cannot meet local reliability needs. | Revisit tagged identification or hybrid CV-plus-tag workflows. | The readiness-verification goal remains even if the sensing method changes. |
| Full system | Automated detection is not reliable enough within the project timeline. | Deliver a semi-automated checklist assistant that guides manual confirmation and logs evidence. | The project still produces measurable workflow and documentation value. |

## Current Implementation Mapping

The repository already contains the foundations of those components:

- `src/micro_design_project/data_collection/` handles camera capture,
  annotation, and controlled data collection.
- `src/micro_design_project/detection.py` handles detector inference and
  annotated rendering.
- `src/micro_design_project/app/` provides the current live tray-check UI and
  count checklist flow.
- `src/micro_design_project/training/` and `scripts/` support dataset export,
  training, benchmarking, and weight export.

The biggest remaining system-design gap is not "add more model code." It is
bridging the current detector demo into a more complete verification workflow
with review states, clearer tray summaries, and lightweight logging.

## Prototype Requirements

The most useful requirements for this repository are prototype-demonstration
requirements rather than deployment requirements.

TrayGuard should demonstrate that:

- the detector can recognize and count known classes in controlled tray-like
  scenes well enough to support comparison against a required list
- the capture design can justify when an overhead tray view is enough and when
  a controlled review view would be needed
- the system can fail more safely by surfacing uncertainty, not only by raising
  average accuracy
- the interface can communicate present, missing, extra, and review-needed
  states clearly enough for human confirmation
- the evaluation pipeline can expose the main CV risks: lighting,
  shape-similarity confusion, clutter and occlusion, and open-set behavior
- the workflow can be discussed as a realistic technician-assistance concept
  rather than only as a model benchmark
- the system can produce lightweight records that support traceability and
  repeated-error analysis

These requirements are intentionally narrower than field-readiness claims. They
fit the actual state of the codebase and the quarter plan better than strict
deployment-style targets such as full-shift uptime, hospital-grade false-alert
limits, or comprehensive SPD integration.

## Engineering Goals And Evidence Status

The original P6 draft listed several hard numbers. Some can be defended as
controlled-prototype targets; others should be treated as aspirational until we
collect local workflow evidence. The table below separates those cases so the
requirements stay honest.

| Goal Area | Engineering Goal | Evidence Status | How To Evaluate In This Project |
| --- | --- | --- | --- |
| Known-class detection | Report precision, recall, mAP50, and mAP50-95 for each controlled experiment. Use `>=90%` per-class precision and recall as a minimum controlled-prototype target for known classes. | Partly supported. Deol et al. reported 94.0-100% class precision and 97.1-100% class recall across 11 surgical-tool categories, with overlapping-tool precision falling as low as 89.6% for one class and recall staying 97.2-98.2%. Atabuzzaman et al. reported real-time CSSD classification exceeding 99.5%, but in a structured single-instrument multi-view station rather than full-tray checking ([Deol et al., 2024](../bibliography.md#deol-et-al-2024), [Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025)). | Use held-out test splits for lighting, similar-shape, clutter, and open-set experiments. Report per-class failures instead of relying only on averages. |
| Tray-level counting | Target `>=95%` exact class-count agreement for known classes in controlled tray-like scenes. Treat this as a stretch validation target, not an externally proven SPD requirement. | Partly supported, but not proven for our tray workflow. Deol et al. maintained correct tool count in all non-transition frames during a one-hour simulated surgical video and reported high detection recall, but that is not the same as SPD tray verification across many tray layouts ([Deol et al., 2024](../bibliography.md#deol-et-al-2024)). | For each test tray, compare required count vs observed count by class. Report exact-count rate, under-count rate, over-count rate, and the specific classes responsible. |
| Missing-item detection | Target `>=95%` missing-item recall in controlled scenarios where one required item is absent. | Reasonable as a prototype target, but locally unproven. The operational need is strongly supported because missing instruments are a major delay source; the exact 95% number is a design target borrowed from high recall in related CV studies, not a published SPD deployment threshold ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Deol et al., 2024](../bibliography.md#deol-et-al-2024)). | Construct tray scenarios with known missing items. Count how often the system flags the missing class without requiring the user to infer it from raw boxes. |
| False alerts | Do not claim the P6 target of `<=1 false alert per 8 hours` yet. Use `<=5%` false positive rate or false review rate as an interim offline target, and replace it with a scan-volume-based target after walkthrough data exists. | The need for low false alerts is well supported, but the exact one-per-shift number is not. Alert-fatigue and workflow literature supports measuring false alerts because interruptions reduce usability and acceptance, but it does not justify this specific rate for SPD tray verification ([Olakotan and Yusof, 2021](../bibliography.md#olakotan-and-yusof-2021), [Cánovas-Segura et al., 2023](../bibliography.md#canovas-segura-et-al-2023)). | Track false extra-item alerts, false missing-item alerts, and unnecessary review prompts per tray scenario. In user walkthroughs, record rescans, hesitations, complaints, and whether users say alerts are tolerable. |
| Latency | Produce tray status within `<5 seconds` from image capture for the prototype UI. Also report model inference latency separately from full UI latency. | Supported as a conservative prototype target. Deol et al. reported median inference of 24.7 ms, or 40.4 FPS, on a V100 for surgical-tool video; TrayGuard's full UI can be much slower than model inference and still meet a five-second tray-check goal ([Deol et al., 2024](../bibliography.md#deol-et-al-2024)). | Log model inference time, count-aggregation time, and end-to-end UI update time. Treat network calls or manual file movement as outside the runtime target. |
| User interaction | Verification should require only a small number of deliberate actions: select or enter tray list, capture or confirm scan, review flagged issues, and finalize. The P6 `no more than two user actions` target is too rigid for review-heavy cases. | Workflow-fit evidence supports minimizing extra steps, but no source supports exactly two actions for this context. Human-in-the-loop literature and workflow-acceptance planning support fast correction and clear review over arbitrary click counts ([Chomutare et al., 2022](../bibliography.md#chomutare-et-al-2022), [Kim et al., 2025](../bibliography.md#kim-et-al-2025), [Zheng et al., 2023](../bibliography.md#zheng-et-al-2023)). | In walkthroughs, record action count, time to final decision, correction burden, and points of confusion. |
| Setup and deployment burden | Keep setup lightweight: commodity camera or phone camera, fixed background, controlled lighting, local compute, and no instrument modification. Do not claim the P6 `usable within 10 minutes` setup target until it is timed. | Directionally supported. CV is attractive because it avoids instrument-level tagging; RFID and barcode alternatives require additional instrument and reader infrastructure ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)). The exact 10-minute setup number is currently an assumption. | Time a clean setup from packed state to first successful tray scan. Record required hardware, calibration steps, and failure points. |
| Workspace coverage | Use a fixed, documented tray workspace for prototype tests. Do not claim the P6 `0.5 m x 0.5 m` coverage target unless the physical capture setup is measured and photographed. | Not independently supported yet. The number is plausible for a tabletop prototype, but it is not tied to a cited SPD tray standard in the current evidence base. | Measure the actual camera field of view at the chosen mount height. Report usable area, pixel resolution, and whether all test objects remain detectable at the edges. |
| Privacy | Do not collect or transmit patient information. Keep prototype images focused on instruments and tray surfaces. | Strongly justified by scope: the system is intended for tray readiness, not patient data. It also keeps the prototype simpler and lower risk. | Verify that saved records contain scan IDs, timestamps, tray definitions, detections, and screenshots only; no patient identifiers. |
| Traceability | Save scan ID, timestamp, required list, observed counts, confidence values, review flags, user corrections, and screenshot or frame reference. | Supported by the quality-reporting argument: incomplete and delayed reporting makes instrument-error improvement harder, and traceability literature frames tracking as important for safety, cost, logistics, and risk analysis ([Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023), [Fayad et al., 2025](../bibliography.md#fayad-et-al-2025)). | Implement the minimum tray-check record schema and generate an example quality report from prototype data. |

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
