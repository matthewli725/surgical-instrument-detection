# Problem Explication

## Automated Surgical Tray Inspection Using Computer Vision

TrayGuard is a computer vision prototype for helping sterile processing
technicians identify and count instruments in a surgical tray. The long-term
goal is a camera-connected system that detects each instrument, compares the
visible tray contents against the required list, and clearly shows which
required tools are still missing.

This project addresses a documented sterile-processing workflow problem. Surgical instrument errors are commonly tied to
missing instruments, wrong instruments, broken or poorly functioning
instruments, and bioburden or debris. Recent studies also suggest that
visualization-heavy tasks such as identification, inspection, and sorting
account for most observed errors
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024),
[Nichol and Saari, 2023](../bibliography.md#nichol-and-saari-2023)). TrayGuard
is aims to reduce that burden by turning tray checking into a
guided visual verification task while preserving technician confirmation
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
In total, visualization-related tasks accounted for 88.6% of all observed errors. The
same study estimated that instrument delays cost the campus between
$6,751,058.06 and $9,421,590.11 in annual lost chargeable OR minutes
([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)). A separate
study analyzed 33,839 surgical instrument packages and identified 398 (1.18%) packaging errors. Wrong instrument
specifications, incomplete packages, and missing instruments were among the most
common errors
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
([Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)).

Hiring more staff is also not a simple substitute. A 2025 national survey of
U.S. sterile-processing workers describes a severe shortage of skilled SPD
technicians. It links the shortage to wage stagnation, high turnover, and
increasing instrument complexity
([Mácola et al., 2025](../bibliography.md#macola-et-al-2025)). Additionally, the training
pipeline is steep for sterile-processing workers. In an AORN Journal survey, most respondents estimated it takes three
to six months (60%) or six to twelve months (31%) to train employees to process general and
specialty instruments. The same paper calculated the 2008 cost to train one
technician to competence at $41,414 (~$65,000 today) including preceptor salary
([Chobin, 2010](../bibliography.md#chobin-2010)). More staff can increase
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
| Hire and train more SPD staff | Adds human capacity and expertise | Skilled-worker shortage, months-long training pipeline, recurring labor cost, persistent visual error risk | CV supports existing staff instead of depending on immediate hiring ([Chobin, 2010](../bibliography.md#chobin-2010), [Mácola et al., 2025](../bibliography.md#macola-et-al-2025), [Nichol et al., 2024](../bibliography.md#nichol-et-al-2024)) |
| RFID or barcode tracking | Strong traceability and utilization data | Requires item-level tags, engraving, readers, antennas, scanning workflow, integration, and ROI justification | CV can pilot visual assistance without modifying every tool ([Olivere et al., 2021](../bibliography.md#olivere-et-al-2021), [Kusuda et al., 2024](../bibliography.md#kusuda-et-al-2024), [Coustasse et al., 2013](../bibliography.md#coustasse-et-al-2013)) |
| Computer vision assistant | Low physical-infrastructure burden, rapid pilot, visual verification, uncertainty flags, screenshot/log evidence | Needs image-quality controls, confidence calibration, and human confirmation | Matches the visualization failure mode that dominates observed errors ([Nichol et al., 2024](../bibliography.md#nichol-et-al-2024), [Fayad et al., 2025](../bibliography.md#fayad-et-al-2025)) |

## Existing Product And Research Landscape

TrayGuard is not inventing visual tray verification from scratch. The product
space already includes a tray-detection patent, SteelcoBelimed's SUIS guided
packing system, Wellstar's reported RIF Robotics pilot, Atabuzzaman et al.'s
CSSD-oriented fine-grained classification work, da Silva et al.'s autonomous
tray-assembly prototype, and Deol et al.'s surgical-instrument detection and
counting study
([Sayani et al., 2018](../bibliography.md#sayani-et-al-2018),
[SteelcoBelimed, accessed 2026](../bibliography.md#steelcobelimed-accessed-2026),
[Atabuzzaman et al., 2025](../bibliography.md#atabuzzaman-et-al-2025),
[da Silva et al., 2026](../bibliography.md#da-silva-et-al-2026),
[Deol et al., 2024](../bibliography.md#deol-et-al-2024)).
The implication is strategic: the question is not whether computer vision could
be used for tray verification. The question is how such a system should be
positioned, evaluated, and limited. 

### Failure Modes And Customer Hesitations

The main risks fall into two groups. System-level risks include loss of human
agency, brittle workflow dependence, unclear exception handling, alert burden,
liability, training cost, and weak economic proof. CV-specific risks include
lighting shift, glare, occlusion, similar-class confusion, open-set objects,
and poorly calibrated confidence.

TrayGuard should reduce visual search burden, highlight likely misses, structure review, and create a better
audit trail. It should not replace SPD judgment, prove sterility, or make policy
decisions about unusual substitutions. The detailed risk register lives in
[`formal_risk_analysis.md`](../experiments/adoption/formal_risk_analysis.md),
and the design response lives in
[`system_design.md`](system_design.md#research-support-audit).

## Bibliography

See the [central bibliography](../bibliography.md) for full source details.
