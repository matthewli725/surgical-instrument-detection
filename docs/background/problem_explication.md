# Problem Explication

## Automated Surgical Tray Inspection Using Computer Vision

TrayGuard is a computer vision prototype for helping sterile processing
technicians identify and count instruments in a surgical tray. The long-term
goal is a camera-connected system that detects each instrument, compares the
visible tray contents against the required list, and clearly shows which
required tools are still missing.

This project addresses a documented sterile-processing workflow problem rather
than a purely speculative one. Surgical instrument errors are commonly tied to
missing instruments, wrong instruments, broken or poorly functioning
instruments, and bioburden or debris. Recent studies also suggest that
visualization-heavy tasks such as identification, inspection, and sorting
account for most observed errors
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023)). TrayGuard
is therefore meant to reduce that burden by turning tray checking into a
guided visual verification task while still preserving technician confirmation
as the final decision
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[Natarus et al., 2025](../bibliography.md#natarus-et-al-2025)).

## Sterile Processing Context And Adoption Risk

Sterile processing is a safety-critical workflow, so this problem is not just
an image-recognition exercise. Central Sterile Processing Department and
Sterile Processing Department work includes cleaning, disinfection,
inspection, packaging, sterilization, and supply of reusable instruments.
Defects in any step can affect operating-room timeliness, cost, and patient
safety
([Huang et al., 2025](../bibliography.md#huang-et-al-2025),
[Chen et al., 2023](../bibliography.md#chen-et-al-2023)). In practice, the
work also requires specialized knowledge. Technicians need to understand
infection control, regulations, device handling, and practical inspection
skills, which is why studies on CSSD training emphasize structured on-the-job
training
([Hu et al., 2024](../bibliography.md#hu-et-al-2024),
[Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)).

Recent sterile-processing research makes the case for computer vision, but it
also shows why customers may hesitate. In one direct-observation study,
researchers observed 236 surgical instrument errors across 147 cases. Missing
instruments accounted for 160 errors, broken or poorly functioning instruments
accounted for 44 errors, and tray issues accounted for 13 errors.
Visualization-related tasks accounted for 88.6% of all observed errors. The
same study estimated that instrument delays cost the campus between
$6,751,058.06 and $9,421,590.11 in annual lost chargeable OR minutes
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). A separate
study analyzed 33,839 surgical instrument packages. Wrong instrument
specifications, incomplete packages, and missing instruments were the most
common packaging errors
([Zhu et al., 2019](../bibliography.md#zhu-et-al-2019)).

The task is also difficult because trays can be large and varied. A
multi-specialty optimization study at Aarhus University Hospital selected 1,340
different instrument trays for optimization. The project reduced total
instruments from 43,073 to 36,687
([Rubak et al., 2024](../bibliography.md#rubak-et-al-2024)). Another study
looked at a Major General Surgery tray with 94 reusable instruments. An average
of 19 instruments were used per case. Ten were never used
([Eussen et al., 2026](../bibliography.md#eussen-et-al-2026)). These numbers
help make the visual task concrete. A technician is not just checking a few
obvious tools; they may be checking a crowded tray where many items look
similar and many items may not even be used in the procedure.

This makes TrayGuard's value proposition plausible. Sterile processing
contains repetitive visual tasks, and humans can miss, misidentify, or
miscount instruments. Recent research also points to computer vision
technologies as possible ways to reduce visualization-related errors
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[Fayad et al., 2025](../bibliography.md#fayad-et-al-2025)). At the same time,
a hospital buyer will not be satisfied by a model accuracy number alone. The
system has to fit the workflow, fail safely, preserve technician authority,
and show that it reduces risk instead of creating another process to supervise
([Natarus et al., 2025](../bibliography.md#natarus-et-al-2025),
[Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). SPD improvement
programs identify staffing, training, inventory management, physical
environment, standard workflows, communication, and governance as separate
drivers of defects. Technical accuracy alone is not enough
([Natarus et al., 2025](../bibliography.md#natarus-et-al-2025)).

## Cost-Benefit Rationale For Computer Vision

Computer vision is attractive for this project because it can use commodity
cameras and computers without requiring us to modify every instrument. RFID and
barcode systems usually require instrument-level tags, engraving, readers,
antennas, or scanner workflows
([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021),
[Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024),
[Zhu et al., 2019](../bibliography.md#zhu-et-al-2019)). RFID can be useful for
utilization measurement and tray optimization. Published RFID studies still
rely on tagging individual instruments and deploying readers or antennas
([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021),
[Hill et al., 2022](../bibliography.md#hill-et-al-2022),
[Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024)). That makes RFID
better suited for full traceability programs, while it is harder to justify
for a low-cost visual-assistance prototype. Broader RFID literature also
identifies high total spending and unclear return on investment as adoption
barriers
([Ting et al., 2013](../bibliography.md#ting-et-al-2013)).

Hiring more staff is also not a simple substitute. A 2025 national survey of
U.S. sterile-processing workers describes a severe shortage of skilled SPD
technicians. It links the shortage to wage stagnation, high turnover, and
increasing instrument complexity
([Macola et al., 2025](../bibliography.md#macola-et-al-2025)). The training
pipeline is steep. In an AORN Journal survey, most respondents estimated three
to six months or six to twelve months to train employees to process general and
specialty instruments. The same paper calculated the 2008 cost to train one
technician to competence at $41,414 including preceptor salary
([Bridges, 2010](../bibliography.md#bridges-2010)). More staff can increase
capacity, but it does not remove the visual-recognition burden, interruption
burden, or need for structured training
([Hu et al., 2024](../bibliography.md#hu-et-al-2024),
[Huang et al., 2025](../bibliography.md#huang-et-al-2025),
[Ofstead et al., 2023](../bibliography.md#ofstead-et-al-2023)).

The cost-benefit hypothesis for TrayGuard is intentionally narrow. CV is not a
replacement for RFID traceability, and it is not a replacement for trained
technicians. Instead, it is a lightweight first layer for visual verification,
missing-item detection, uncertainty flagging, and quality logging. That makes
it something a hospital could test before committing to instrument-level
tagging or major staffing expansion
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[Fayad et al., 2025](../bibliography.md#fayad-et-al-2025),
[Natarus et al., 2025](../bibliography.md#natarus-et-al-2025)).

| Option | Benefits | Costs / Risks | Why TrayGuard Starts With CV |
| --- | --- | --- | --- |
| Hire and train more SPD staff | Adds human capacity and expertise | Skilled-worker shortage, months-long training pipeline, recurring labor cost, persistent visual error risk | CV supports existing staff instead of depending on immediate hiring ([Bridges, 2010](../bibliography.md#bridges-2010), [Macola et al., 2025](../bibliography.md#macola-et-al-2025), [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)) |
| RFID or barcode tracking | Strong traceability and utilization data | Requires item-level tags, engraving, readers, antennas, scanning workflow, integration, and ROI justification | CV can pilot visual assistance without modifying every tool ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Ting et al., 2013](../bibliography.md#ting-et-al-2013)) |
| Computer vision assistant | Low physical-infrastructure burden, rapid pilot, visual verification, uncertainty flags, screenshot/log evidence | Needs image-quality controls, confidence calibration, and human confirmation | Matches the visualization failure mode that dominates observed errors ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Fayad et al., 2025](../bibliography.md#fayad-et-al-2025)) |

## Existing Product And Research Landscape

This is no longer just an adjacent-field thought experiment. There is now
enough direct evidence to say that surgical tray verification and packaging
assistance with computer vision is an active product and research space, even
if broad adoption still appears to be early.

The closest conceptual precedent is a 2018 patent from Aga Khan University for
"Detection of surgical instruments on surgical tray." It describes a
camera-plus-database workflow that detects what instruments are present,
retrieves what instruments should be present, compares the two, and identifies
missing items. That is very close to TrayGuard's core concept of visual
verification against an expected set rather than generic object detection
([Sayani et al., 2018](../bibliography.md#sayani-et-al-2018)).

The closest visible commercial analog is SteelcoBelimed's SUIS system. Their
product page says SUIS guides staff step-by-step through set packing
procedures, identifies instruments by shape, outlines extraneous items, reduces
procedure time, and is especially useful for complex loan sets. That means the
core motivation behind TrayGuard already exists in the market as guided
packaging assistance. The most important design implication is that operator
guidance, not autonomous replacement, is the product framing that appears to
have made it to commercialization
([SteelcoBelimed, accessed 2026](../bibliography.md#steelcobelimed-accessed-2026)).

There is also direct hospital-side pilot activity. In 2023, the American
Hospital Association reported that Wellstar invested in RIF Robotics and ran a
pilot to refine the technology with feedback from sterile processing staff. The
reported goal was automated assembly of a basic surgical tray using AI,
computer vision, and robotics. That is strong evidence that health systems see
this as a real operational problem. It also reinforces that frontline workflow
feedback is part of the product, not an afterthought
(American Hospital Association, 2023).

The academic literature is moving in the same direction. A 2026 arXiv paper,
"Towards Autonomous Instrument Tray Assembly for Sterile Processing
Applications," presents a robotic tray assembly system using a custom dataset of
31 instruments and 6,975 annotated images, along with structured tray fixtures
that reduce collisions during transport. The paper explicitly describes this as
a first step toward automating SPD workflows. That matters because it suggests
the field is real, but still early and often dependent on semi-structured
layouts rather than fully unconstrained pile-of-instruments scenes
([da Silva et al., 2026](../bibliography.md#da-silva-et-al-2026)).

Direct academic evidence is somewhat broader in intraoperative counting than in
SPD tray assembly. A 2024 proof-of-concept study on automated surgical
instrument detection and counting found that deep-learning-based counting is
feasible and could reduce manual burden, but it still called for further
clinical validation
([Deol et al., 2024](../bibliography.md#deol-et-al-2024)).

Taken together, the market signal is clear enough to matter. TrayGuard is not
inventing the general idea of visual tray verification from scratch. It is
entering an early product space where patents, commercial assistance systems,
startup pilots, and early robotic assembly papers already exist. The closest
commercial overlap appears to be SteelcoBelimed's SUIS. That does not make the
project irrelevant; instead, it sharpens the question. The important issue is
not whether computer vision could be used for tray verification, but what
motivations, constraints, and limitations shape how such a system should be
positioned, evaluated, and differentiated.

### Failure Modes And Customer Hesitations

The main risks fall into two connected groups: system-level adoption risks and
computer-vision-specific risks.

At the system level, a hospital may reject an apparently strong automation
product if it removes too much human agency, creates a single point of failure,
handles exceptions poorly, slows peak workflow, or creates unclear liability.
Evidence from healthcare AI implementation, radiology deployment, and pharmacy
verification suggests that high-risk organizations adopt AI more readily when
it preserves human sign-off, makes the workflow easier to recover from, and
keeps accountability legible rather than hidden inside a black box. Radiology
market reviews also show that commercial availability often outpaces evidence
of real clinical or economic impact
([Steenhuis et al., 2022](../bibliography.md#steenhuis-et-al-2022),
[van Leeuwen et al., 2021](../bibliography.md#van-leeuwen-et-al-2021),
[Jiang et al., 2025](../bibliography.md#jiang-et-al-2025),
[Zheng et al., 2023](../bibliography.md#zheng-et-al-2023)). That matters for
TrayGuard because sterile processing depends on technician expertise, exception
handling, and auditability, not just correct object recognition.

At the computer-vision level, strong lab performance does not guarantee strong
live performance. Tray verification involves reflective metal, occlusion,
similar-looking instruments, residue, tray variation, and unfamiliar tools. The
medical-imaging literature shows that AI performance often degrades under
real-world distribution shift, and the pharmacy literature shows that trust
depends strongly on uncertainty communication and human-centered review paths
([Yang et al., 2024](../bibliography.md#yang-et-al-2024),
[Tikhomirov et al., 2026](../bibliography.md#tikhomirov-et-al-2026),
[Kim et al., 2025](../bibliography.md#kim-et-al-2025)). For TrayGuard, that
means the product should be framed as guided visual verification rather than
autonomous tray approval. It should surface missing items, low-confidence
items, and corrections clearly enough that a technician can make the final
decision quickly and defensibly.

The resulting design stance is intentionally narrow. TrayGuard should not try
to replace SPD judgment, prove sterility, or make policy decisions about
unusual substitutions. It should reduce visual search burden, highlight likely
misses, structure review, and create a better audit trail. That stance is also
more consistent with what adjacent industries actually adopt: manufacturing
uses CV for first-pass screening, radiology uses AI for triage and second-read
support, and pharmacy verification work favors uncertainty-aware hybrid review
rather than full replacement. The economics literature points in the same
direction: buyers need evidence of system-level value, not just model
performance, and that evidence is still limited in healthcare AI
([Vithlani et al., 2023](../bibliography.md#vithlani-et-al-2023),
[Kastrup et al., 2024](../bibliography.md#kastrup-et-al-2024)).

For the detailed evidence base and source-backed breakdown, see:

- `docs/experiments/adoption/workflow_acceptance.md`
- `docs/experiments/adoption/formal_risk_analysis.md`

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
