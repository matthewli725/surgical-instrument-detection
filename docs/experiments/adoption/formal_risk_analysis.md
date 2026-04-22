# Formal Risk Analysis

TrayGuard should not be evaluated as "just a detector." In high-risk workflows,
buyers can reject even a technically excellent system if it creates the wrong
kind of dependency, disrupts operations, or creates unclear responsibility. The
evidence from healthcare AI, radiology, pharmacy verification, and
computer-vision inspection in manufacturing points to a consistent conclusion:
adoption depends on sociotechnical fit, not accuracy alone.

This page combines the major adoption risks into one formal framework with two
lenses:

- system-level risks, which would matter even if the model were perfect
- computer-vision-specific risks, which arise because the system depends on CV
  in a variable real-world environment

## Core Claim

A hospital may reject a fully autonomous tray-sorting or tray-approval system
even if it performs extremely well in tests, because the real procurement
question is not "Can the model recognize instruments?" It is "Does this system
improve the workflow without creating new operational, legal, or human-factor
risks?" That framing is consistent with implementation research in healthcare AI
and with adjacent high-stakes verification workflows such as radiology and
pharmacy verification. In radiology specifically, the commercial market has
grown faster than the evidence base, which reinforces the point that commercial
availability is not the same thing as workflow-ready adoption
([van Leeuwen et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8128724/),
[Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898),
[Zheng et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10775023/)).

## Direct Product and Market Evidence

There is now enough direct evidence to say this is a real product and design
space, not just an adjacent-domain analogy. The direct evidence is still thin
enough that adjacent industries remain useful for explaining adoption risk, but
it is no longer accurate to describe tray verification with CV as purely
speculative.

The most direct conceptual precedent is the 2018 patent "Detection of surgical
instruments on surgical tray," which describes a camera-based system that
detects what instruments are present, retrieves what should be present from a
database, compares the two, and identifies missing items
([Sayani et al., 2018](https://patents.google.com/patent/US20180204323A1/en)).

The closest visible commercial analog is SteelcoBelimed's SUIS product. Their
product page describes a system that guides staff step-by-step through set
packing procedures, identifies instruments by shape, outlines extraneous items,
and targets complex loan sets. That overlap is substantial enough that TrayGuard
should treat SUIS as a real comparison point rather than as a distant adjacent
example
([SteelcoBelimed, accessed 2026](https://www.steelcobelimed.com/insights/surgical-instrument-scanner/)).

There is also direct health-system pilot evidence. The American Hospital
Association reported in 2023 that Wellstar invested in RIF Robotics and used a
pilot to refine the technology with feedback from sterile processing staff. The
reported goal was automated assembly of a basic surgical tray using AI, computer
vision, and robotics
([American Hospital Association, 2023](https://www.aha.org/aha-center-health-innovation-market-scan/2023-10-31-4-ways-wellstar-health-funding-collaborative-innovation)).

Academic robotics work has now moved directly into SPD tray assembly as well. A
2026 arXiv paper on autonomous instrument tray assembly reports a custom dataset
of 31 instruments and 6,975 annotated images, a calibrated vision module, a
robot arm, and statistically significant reduction in tool-to-tool collisions
relative to human-assembled trays. The same paper describes itself as a first
step toward automating SPD workflows, which reinforces both the reality and the
early-stage nature of the space
([da Silva et al., 2026](https://arxiv.org/abs/2602.01679)).

The direct academic literature is stronger on intraoperative detection and
counting than on sterile-processing workflow adoption. A 2024 proof-of-concept
study showed that automated surgical instrument detection and counting is
feasible and could reduce manual burden, but it still called for further
clinical validation
([Deol et al., 2024](https://doi.org/10.1186/s13037-024-00406-y)).

The main implication for TrayGuard is strategic. The existence of SUIS, the tray
patent, the Wellstar pilot, and the 2026 tray-assembly paper means the core
product motivation is already validated. The open questions are workflow fit,
trust, integration, and positioning. It is therefore reasonable to say that
TrayGuard is entering an early but real product category, with SUIS as the
closest visible commercial analog and guided verification as the clearest proven
product framing.

## 1. System-Level Risks

These risks remain important even if the vision model is very accurate.

### 1.1 Human Agency, Deskilling, and Over-Reliance

If the system fully replaces tray verification, technicians may become passive
monitors instead of active verifiers. Recent reviews on AI-induced deskilling in
medicine warn that repeated delegation to AI can erode technical skills,
clinical judgment, confidence, and opportunities for trainees to build
expertise. Separate automation-bias research shows that users can over-accept
automation output or fail to act when the system does not prompt them
([Natali et al., 2025](https://link.springer.com/article/10.1007/s10462-025-11352-1),
[Goddard et al., 2012](https://academic.oup.com/jamia/article/19/1/121/732254)).

**Adoption implication:** hospitals may prefer systems that preserve technician
judgment and practice, rather than systems that turn staff into backup
observers.

### 1.2 Operational Fragility and Single-Point-of-Failure Risk

Automation can improve peak consistency while reducing graceful degradation. A
manual tray workflow distributes risk across people and local decisions; a fully
automated workflow concentrates risk in one technical stack. Healthcare AI
implementation reviews repeatedly identify workflow dependence, interoperability,
and sustainment as deployment risks, and they emphasize that systems requiring
extra steps or brittle integrations are less likely to be implemented or
sustained
([Steenhuis et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9738234/),
[van Leeuwen et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8128724/),
[Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898)).

**Adoption implication:** buyers worry about what happens when the camera,
network, UI, or model pipeline fails during peak workload, not just when the
system is operating normally.

### 1.3 Exception Handling and Wrong-Level-of-Autonomy Risk

High-consequence verification work is dominated by exceptions: substitutions,
partial trays, damaged instruments, unusual surgeon preferences, and policy
questions. Adjacent industries have generally adopted AI as triage, exception
handling, or second-read support rather than as full replacement. Pharmacists in
human-centered AI studies preferred hybrid workflows where human intervention is
triggered by medication risk and AI confidence, and HITL reviews similarly argue
that human oversight remains essential in high-stakes domains
([Zheng et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10775023/),
[Kim et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11862782/),
[Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898)).

**Adoption implication:** a system that automates normal cases but still leaves
humans with the hardest edge cases may only be valuable if it makes those edge
cases easier to resolve, not merely more visible.

### 1.4 Throughput, Latency, and Workflow-Fit Risk

A system can improve per-image accuracy and still lose on operational
throughput. Healthcare implementation studies consistently identify workflow fit
as a major barrier: extra screens, extra clicks, manual data handling, and poor
integration all reduce adoption. Reviews of commercial radiology AI and
implementation research suggest that the evidence base remains much more mature
on stand-alone performance than on workflow or cost impact
([van Leeuwen et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8128724/),
[Steenhuis et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9738234/),
[Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898)).

**Adoption implication:** hospitals optimize for throughput under pressure, not
average-case elegance. A rigid system that slows busy periods can still be
rejected.

### 1.5 Change-Management, Training, and Cultural Resistance

Implementation is costly even when the model works. Healthcare AI reviews point
to training, local buy-in, implementation management, and organizational support
as critical determinants of success. Manufacturing studies aimed at small and
medium enterprises make a similar point: barriers are not just technical, but
also cost, perceived risk, and complexity of adoption
([Steenhuis et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9738234/),
[Agostini and Nosella, 2020](https://www.sciencedirect.com/science/article/pii/S0025174719000399),
[Stentoft et al., 2020](https://www.sciencedirect.com/science/article/pii/S0166361520304954)).

**Adoption implication:** a hospital may reject a good system because staff
training, SOP changes, pilot management, and stakeholder alignment cost more
organizational effort than the expected benefit.

### 1.6 Liability, Accountability, and Auditability

High-risk organizations care about who is responsible when the system is wrong.
Recent legal and HITL reviews emphasize that accountability does not transfer to
the algorithm; human oversight must be meaningful, documented, and supported by
governance structures. Radiology deployment guidance similarly emphasizes
transparency, monitoring, and operational governance
([Kelly, 2026](https://pubmed.ncbi.nlm.nih.gov/41932077/),
[Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898)).

**Adoption implication:** if a hospital cannot explain why a tray was approved,
or who overrode what, the system is harder to defend in audits, quality reviews,
or legal disputes.

### 1.7 Physical Integration and Sterility Constraints

A fully autonomous sorter is not just a perception problem. It is also a
mechanical-handling, cleaning, and sterility problem. Studies on robotic
instrument reprocessing show that complex instrument design creates challenges in
cleaning, disinfection, and sterilization, and even existing robotic instrument
reprocessing is operationally demanding
([Pistillo et al., 2024](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0300355)).

**Adoption implication:** even perfect vision may not overcome the practical
difficulty of reliable instrument manipulation, contamination control, and
maintenance inside SPD operations.

### 1.8 Economic and Incentive Misalignment

Adoption depends on total value capture, not technical merit alone. In
manufacturing, firms hesitate when ROI, capability, and integration benefits
are unclear. In healthcare, systematic reviews of AI economic evaluation show
that the evidence base is still limited and often methodologically weak, while
radiology reimbursement work argues that adoption is difficult when AI adds
value but is treated as unrecoverable overhead rather than reimbursed or tied to
measurable savings
([Agostini and Nosella, 2020](https://www.sciencedirect.com/science/article/pii/S0025174719000399),
[Vithlani et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10486896/),
[Kastrup et al., 2024](https://bmcdigitalhealth.biomedcentral.com/articles/10.1186/s44247-024-00088-7),
[Lobig et al., 2023](https://www.nature.com/articles/s41746-023-00861-4)).

**Adoption implication:** if TrayGuard does not clearly reduce labor burden,
rework, delays, or quality losses, buyers may reject it even if it is
technically impressive.

## 2. Computer-Vision-Specific Risks

These risks arise because TrayGuard depends on a visual model in a messy
real-world environment.

### 2.1 Distribution Shift and Real-World Variability

Strong internal performance does not guarantee strong external performance.
Recent medical-imaging literature shows that AI systems often underperform on
external datasets or after deployment because of shifts in population, scanner,
protocol, and environment. Silent-trial research also shows that models commonly
drop in performance when moved from retrospective testing to live evaluation
([Yang et al., 2024](https://www.nature.com/articles/s41591-024-03113-4),
[van Leeuwen et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8128724/),
[Tikhomirov et al., 2026](https://www.nature.com/articles/s44360-025-00048-z)).

For TrayGuard, the analogous risks are lighting changes, reflective metal,
occlusion, tray clutter, worn instruments, novel tools, residue, and setup
variation.

### 2.2 False Positives, Alert Burden, and Correction Cost

Users often tolerate imperfect CV when the system reduces work, but not when it
creates nuisance interventions. Clinical decision-support and healthcare AI
implementation literature repeatedly links false alarms and poor usability to
alert fatigue, workflow disruption, and reduced acceptance
([Olakotan and Yusof, 2021](https://pubmed.ncbi.nlm.nih.gov/33853395/),
[Cánovas-Segura et al., 2023](https://pubmed.ncbi.nlm.nih.gov/37245656/),
[Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898)).

For TrayGuard, the relevant question is not only whether the model is wrong, but
how expensive it is for a technician to recover from a wrong or low-value
prompt.

### 2.3 Uncertainty Calibration and Open-Set Behavior

Trust depends on whether the system knows when it does not know. Pharmacy
verification studies show that communicating uncertainty affects pharmacists'
trust and cognitive behavior, while human-centered design work in pharmacy found
that users preferred interfaces with probability displays, match status, and
"unsure" paths rather than binary claims
([Kim et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11862782/),
[Kim et al., 2025 RCT](https://pubmed.ncbi.nlm.nih.gov/39888668/),
[Zheng et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10775023/)).

For TrayGuard, this means the product should avoid forced certainty when
instruments are unfamiliar, partially hidden, or visually ambiguous.

### 2.4 Transparency and Defensibility of CV Output

In high-stakes workflows, adoption depends on defensible output rather than raw
prediction alone. Radiology deployment papers emphasize transparency,
monitoring, and real-world testing, and legal analyses of AI-supported practice
argue that human reasoning and documentation must remain primary
([Jiang et al., 2025](https://ajronline.org/doi/10.2214/AJR.24.31898),
[Kelly, 2026](https://pubmed.ncbi.nlm.nih.gov/41932077/)).

For TrayGuard, a detection should be reviewable through screenshots, confidence,
missing-item lists, correction logs, and final human confirmation.

### 2.5 Need for Local Validation Before Workflow Dependence

Because CV systems are sensitive to environment and workflow details, buyers
often want local evidence before changing operations. Silent-trial literature in
medical AI shows that institutions increasingly evaluate models prospectively in
their intended environment before letting them affect real decisions
([Tikhomirov et al., 2026](https://www.nature.com/articles/s44360-025-00048-z)).

For TrayGuard, that supports a pilot strategy based on shadow-mode or guided-use
evaluation before any stronger automation claims.

## 3. Combined Interpretation

Taken together, the literature suggests that the biggest adoption risk is not
"the model is imperfect." The bigger risk is building the wrong system
architecture.

The evidence supports these design conclusions:

- Full replacement is harder to adopt than assistive verification.
- Human sign-off should remain explicit.
- Uncertain and exceptional cases should be surfaced, not hidden.
- The system should degrade gracefully when unavailable.
- Logs, screenshots, and correction history matter for trust.
- Pilot evidence should focus on workflow value, not only detector metrics.

## 4. What This Means For TrayGuard

TrayGuard is better positioned as a technician-centered verification assistant
than as an autonomous tray-sorting robot. That position is more consistent with
what adjacent industries actually adopt:

- manufacturing uses CV for first-pass screening and exception review
- radiology uses AI for prioritization, triage, and second-read support
- pharmacy verification work favors uncertainty-aware hybrid review

The most defensible product claim is therefore:

> TrayGuard should reduce cognitive burden and missed items while preserving
> human authority, auditability, and recovery paths.

That claim is narrower than "automation replaces tray checking," but it is much
better aligned with the adoption patterns documented in adjacent industries.

## References

- American Hospital Association, ["4 Ways Wellstar Health Is Funding Collaborative Innovation"](https://www.aha.org/aha-center-health-innovation-market-scan/2023-10-31-4-ways-wellstar-health-funding-collaborative-innovation), 2023.
- Cánovas-Segura et al., ["Meaningful time-related aspects of alerts in Clinical Decision Support Systems. A unified framework"](https://pubmed.ncbi.nlm.nih.gov/37245656/), Journal of Biomedical Informatics, 2023.
- Agostini and Nosella, ["The adoption of Industry 4.0 technologies in SMEs: results of an international study"](https://www.sciencedirect.com/science/article/pii/S0025174719000399), Management Decision, 2020.
- Deol et al., ["Artificial intelligence model for automated surgical instrument detection and counting: an experimental proof-of-concept study"](https://doi.org/10.1186/s13037-024-00406-y), Patient Safety in Surgery, 2024.
- Goddard et al., ["Automation bias: a systematic review of frequency, effect mediators, and mitigators"](https://academic.oup.com/jamia/article/19/1/121/732254), Journal of the American Medical Informatics Association, 2012.
- Jiang et al., ["Deployment of Artificial Intelligence in Radiology: Strategies for Success"](https://ajronline.org/doi/10.2214/AJR.24.31898), American Journal of Roentgenology, 2025.
- Kastrup et al., ["Landscape and challenges in economic evaluations of artificial intelligence in healthcare: a systematic review of methodology"](https://bmcdigitalhealth.biomedcentral.com/articles/10.1186/s44247-024-00088-7), BMC Digital Health, 2024.
- Kelly, ["Human in the loop: Balancing artificial intelligence, clinical judgment, and legal responsibility"](https://pubmed.ncbi.nlm.nih.gov/41932077/), International Journal of Law and Psychiatry, 2026.
- Kim et al., ["The Effects of Presenting AI Uncertainty Information on Pharmacists’ Trust in Automated Pill Recognition Technology: Exploratory Mixed Subjects Study"](https://pmc.ncbi.nlm.nih.gov/articles/PMC11862782/), JMIR Human Factors, 2025.
- Kim et al., ["Effect of Artificial Intelligence Helpfulness and Uncertainty on Cognitive Interactions with Pharmacists: Randomized Controlled Trial"](https://pubmed.ncbi.nlm.nih.gov/39888668/), Journal of Medical Internet Research, 2025.
- Lobig et al., ["To pay or not to pay for artificial intelligence applications in radiology"](https://www.nature.com/articles/s41746-023-00861-4), npj Digital Medicine, 2023.
- Natali et al., ["AI-induced Deskilling in Medicine: A Mixed-Method Review and Research Agenda for Healthcare and Beyond"](https://link.springer.com/article/10.1007/s10462-025-11352-1), Artificial Intelligence Review, 2025.
- Olakotan and Yusof, ["The appropriateness of clinical decision support systems alerts in supporting clinical workflows: A systematic review"](https://pubmed.ncbi.nlm.nih.gov/33853395/), Health Informatics Journal, 2021.
- Pistillo et al., ["Evaluation of microbial occurrence in reusable robotic instruments for minimally invasive surgery: A pilot study"](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0300355), PLOS One, 2024.
- Sayani et al., ["Detection of surgical instruments on surgical tray"](https://patents.google.com/patent/US20180204323A1/en), US Patent Application US20180204323A1, 2018.
- Steenhuis et al., ["Artificial Intelligence Implementation in Healthcare: A Theory-Based Scoping Review of Barriers and Facilitators"](https://pmc.ncbi.nlm.nih.gov/articles/PMC9738234/), International Journal of Environmental Research and Public Health, 2022.
- Stentoft et al., ["Industry 4.0: Adoption challenges and benefits for SMEs"](https://www.sciencedirect.com/science/article/pii/S0166361520304954), Computers in Industry, 2020.
- SteelcoBelimed, ["SUIS - Surgical Instrument Vision System"](https://www.steelcobelimed.com/insights/surgical-instrument-scanner/), accessed 2026.
- Tikhomirov et al., ["A scoping review of silent trials for medical artificial intelligence"](https://www.nature.com/articles/s44360-025-00048-z), Nature Health, 2026.
- van Leeuwen et al., ["Artificial intelligence in radiology: 100 commercially available products and their scientific evidence"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8128724/), European Radiology, 2021.
- Vithlani et al., ["Economic evaluations of artificial intelligence-based healthcare interventions: a systematic literature review of best practices in their conduct and reporting"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10486896/), Frontiers in Pharmacology, 2023.
- Yang et al., ["The limits of fair medical imaging AI in real-world generalization"](https://www.nature.com/articles/s41591-024-03113-4), Nature Medicine, 2024.
- da Silva et al., ["Towards Autonomous Instrument Tray Assembly for Sterile Processing Applications"](https://arxiv.org/abs/2602.01679), arXiv, 2026.
- Zheng et al., ["Designing Human-Centered AI to Prevent Medication Dispensing Errors: Focus Group Study With Pharmacists"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10775023/), JMIR Formative Research, 2023.
