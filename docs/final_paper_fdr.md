# Final Paper FDR

## Formulate The Problem Precisely

In sterile processing
departments (SPDs), technicians receive used instruments from the OR, clean and
decontaminate them, inspect each item for soil or damage, check function,
assemble procedure-specific trays from count sheets, package trays for
sterilization, run sterilization, store sterile sets, and distribute
them back for surgical use. This work is detailed, high-volume, and highly
local: a technician must know the hospital's instrument names, tray lists,
surgeon preferences, replacement rules, and inspection expectations.

Mistakes can occur at several points in that workflow. A technician may miss
residual soil, overlook a crack or broken tip, confuse two visually similar
instruments, place the wrong size or pattern into a tray, omit an instrument,
add an extra instrument, assemble a device incorrectly, use the wrong count
sheet, package a set incompletely, or fail to catch a sterilization or
documentation problem. In the OR, those mistakes appear as missing, wrong,
extra, damaged, contaminated, nonfunctional, incorrectly assembled, or otherwise
unavailable instruments.

Published rates vary by hospital, measurement method, and error definition, but
the available evidence suggests that these are recurring operational failures,
not isolated accidents. Alfred et al. analyzed 3,900 tray defects across 41,799
cases, or roughly 9 defects per 100 cases, and found that 55.0% of recorded
defects occurred during assembly
([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). Zhu et al. found
398 packaging errors among 33,839 surgical instrument packages, or about 1.2%
of packages, including wrong specifications, incomplete packages, and missing
instruments ([Zhu et al., 2019](bibliography.md#zhu-et-al-2019)). Nichol et al.
observed 236 surgical instrument errors affecting 147 cases, with most errors
tied to visualization work such as inspection, identification, function
checking, and tray assembly
([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)).

The general problem is therefore:

> Sterile processing workflows do not always reliably produce complete,
> correct, functional, sterile, and ready-for-use surgical instrument sets.


## Position And Justify The Problem

### Context

The problem appears across the reusable stainless surgical instrument chain. A simplified
SPD-to-OR cycle includes the following stages
([George et al., 2024](bibliography.md#george-et-al-2024)):

1. Point-of-use preparation: at the end of a procedure, instruments are
   prepared for transfer from the OR to sterile processing. This can include
   gross cleaning, use of sterile water, and enzymatic pretreatment to keep
   material from drying on instruments.

2. Transport to sterile processing: used instruments are moved from the OR or
   procedural area to the sterile processing unit.

3. Decontamination: instruments are cleaned and decontaminated. George et al.
   describe manual scrubbing, ultrasonic cleaning, and automated washer systems
   as common parts of this stage.

4. Assembly and inspection: after decontamination, instruments move to the
   assembly area. Technicians inspect instruments, assemble instrument pans or
   sets, replace missing items, and place instruments into containers or wraps
   for sterilization.

5. Sterilization: packaged instruments are sterilized using methods appropriate
   to the device and material. George et al. describe high-temperature methods
   such as autoclave sterilization and low-temperature methods such as chemical
   or radiation-based sterilization.

6. Storage: once sterilized, instruments and trays are cooled as needed and
   placed in storage until they are required again.

7. Return to use: when needed for surgery, stored instruments are obtained and
   brought back to the OR for the next case.

Nichol and Saari's risk model provides a more detailed version of this cycle:
for simple instruments, they mapped 104 human tasks and found that 91% of
modeled error risk occurred during the sterile-processing portion of the cycle,
especially the decontamination and assembly-and-inspection steps
([Nichol and Saari, 2023b](bibliography.md#nichol-and-saari-risk-modeling-2023)).
Those steps are high risk because they contain the most complicated,
non-routine tasks: instruments must be separated, cleaned, inspected for
bioburden and damage, identified, sorted, and rebuilt into the correct tray, and
all eight highest-risk tasks in the model involved human visualization,
inspection, identification, or sorting.

### Narrowing The Problem

Within the full SPD-to-OR cycle, this project narrows to tray reconstruction
and verification: the point where cleaned instruments are inspected,
identified, matched to count sheets, and rebuilt into procedure-specific trays.
This is the most defensible focus because the highest-risk parts of the cycle
depend on human visualization, sorting, and local tray knowledge.

This focus also addresses a likely stakeholder objection. Even if a tray comes
from a specific surgery and is expected to return with the same contents, it
does not remain a sealed, unchanged kit during reprocessing. Instruments are
transported to decontamination, opened, separated, disassembled when required,
manually cleaned or transferred onto washer racks, and exposed to mechanical
washing before moving to the clean preparation area
([STERIS, accessed 2026](bibliography.md#steris-cleaning-instruments-accessed-2026),
[CDC](bibliography.md#cdc),
[Public Health Ontario, 2013](bibliography.md#public-health-ontario-2013),
[Medline, 2026](bibliography.md#medline-transport-2026)). After cleaning,
technicians manually rebuild sets against tray-specific count sheets, creating
opportunities for items to be mixed between sets, left behind, substituted from
backup inventory, or misidentified because of incomplete count-sheet data,
local jargon, or look-alike instruments
([Purdue University, accessed 2026](bibliography.md#purdue-count-sheets-accessed-2026),
[Alfred et al., 2021](bibliography.md#alfred-et-al-2021),
[Nadeau, 2024](bibliography.md#nadeau-2024)).

Observed error studies support this narrowed focus. Nichol et al. found that
the largest observed error category was Missing+, which included missing,
wrong, and extra instruments, and connected many errors to visualization work
such as inspection, identification, and function checks
([Nichol et al., 2024](bibliography.md#nichol-et-al-2024)). Alfred et al. found
missing instruments to be the most commonly reported assembly defect and linked
tray defects to OR delays, training, production pressure, inventory,
nomenclature, technology, and workspace constraints
([Alfred et al., 2021](bibliography.md#alfred-et-al-2021)). Zhu et al. found
packaging errors such as wrong instrument specifications, incomplete packages,
and missing instruments in a hospital surgical-instrument tracking system
([Zhu et al., 2019](bibliography.md#zhu-et-al-2019)).

### Why The Problem Is Important And To Whom

Instrument readiness matters because surgery is time-sensitive,
coordination-heavy work. When an instrument set is wrong, incomplete, unclean,
damaged, or unavailable, the OR team may need to pause, search for replacement
instruments, open backup trays, change the procedure flow, or delay the case
([Nichol et al., 2024](bibliography.md#nichol-et-al-2024),
[Pennsylvania Patient Safety Authority, 2006](https://patientsafety.pa.gov/ADVISORIES/Pages/200603_20.aspx)).

Dirty or damaged instruments add a direct safety concern. A 2024 hospital
inspection reported pitting, stains, sticky residue, rust, scratches, and other
concerns in randomly selected ready-for-use trays
([Association of Health Care Journalists, 2024](https://www.hospitalinspections.org/report-detail/SNXU11)).
The Pennsylvania Patient Safety Authority warns that contaminated instruments
can put patients at risk of surgical site infection and can also cause lost OR
time if discovered after a procedure has begun
([Pennsylvania Patient Safety Authority, 2006](https://patientsafety.pa.gov/ADVISORIES/Pages/200603_20.aspx)).

The stakeholders include:

- Patients, who depend on sterile, functional instruments during surgery.
- Surgeons and OR teams, who need complete and usable sets to maintain
  procedure flow.
- SPD technicians, who perform detailed, high-volume work under production
  pressure.
- SPD supervisors and educators, who manage training, quality assurance,
  staffing, documentation, and feedback loops.
- Hospitals, which lose time and capacity when instrument issues delay cases or
  require rework.

### General Interest Beyond One Local Practice

This problem is broadly relevant because reusable surgical instruments, SPDs,
procedure-specific trays, count sheets, sterilization records, and OR
dependence on prepared sets are common across hospitals. The exact instruments,
tray lists, vendor systems, and surgeon preferences vary by site, while the
readiness challenge repeats across settings: hospitals must transform complex,
locally defined instrument requirements into complete and ready surgical sets.

The local tray-reconstruction problem connects to broader work on surgical
tray optimization, inventory visibility, and instrument-set readiness. dos
Santos et al. describe tray rationalization as deciding which instruments and
quantities belong in which trays and which trays are needed for procedures
([dos Santos et al., 2021](bibliography.md#dos-santos-et-al-2021)). A 2025
industry benchmark report summarized by Healthcare Purchasing News found that
58% of surveyed SPD and OR leaders reported surgery delays caused by instrument
sets that were missing, incomplete, or not ready on time
([HPN, 2025](https://www.hpnonline.com/sterile-processing/news/55330330/benchmark-report-identifies-fundamental-risks-in-sterile-processing-operations)).
The same benchmark report emphasized human error, inventory gaps, limited data
visibility, and real-time visibility into tray and instrument location as major
readiness concerns
([Aesculap and Ascendco Health, 2025](https://www.aesculapusa.com/content/dam/aesculap-us/us/website/aesculap-inc/healthcareprofessionals/surgical-asset-management-solutions/2025%20Surgical%20Asset%20Management%20Industry%20Benchmark%20Report%20Aesculap%20Ascendco%20Health%20UPDATE.pdf)).

This makes the problem generalizable without making it generic: each hospital
has its own instruments and tray rules, but many hospitals face the same
underlying need to verify that a locally defined set is complete, correct,
clean, functional, and available before surgery.

### Ensure The Problem Is Solvable

The full readiness problem remains too broad for one final project because it
includes staffing, inventory, cleaning practice, sterilization capacity,
scheduling, tracking systems, and OR-SPD communication. The solvable project
scope is narrower: tray readiness and verification during reconstruction.

This scope can be demonstrated without a live hospital deployment because it
can use representative instrument sets, tray-specific count sheets, distractor
items, inspection criteria, and simulated tray-building tasks. Success can be
measured through observable outcomes such as whether a learner or prototype
correctly identifies missing, wrong, extra, damaged, or miscounted instruments;
how long verification takes; and whether feedback improves performance across
repeated practice.

The resulting research question is:

> How can a small training and verification system help users detect missing,
> wrong, extra, damaged, or miscounted instruments in a locally defined surgical
> tray before that tray is considered ready for use?
