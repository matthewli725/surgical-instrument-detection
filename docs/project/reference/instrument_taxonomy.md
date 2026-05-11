# Surgical Instrument Taxonomy

## Summary

The most defensible hierarchy for TrayGuard is:

1. surgical service, specialty, or procedure family;
2. tray, set, kit, or case cart configuration;
3. instrument function family;
4. specific instrument type;
5. variant attributes such as size, shape, jaw pattern, curve, tip, length,
   catalog number, manufacturer, local alias, and local tray position.

This should not be described as a fixed breakdown from "14 surgeries" unless a
specific hospital or course provides exactly fourteen procedure families. HSPA's
public instrument-resource page instead separates instruments in two overlapping
ways: by broad specialty/device area in the Sterile Processing Instrument
Manual, and by instrument family in *The World of Surgical Instruments*
([HSPA Surgical Instrument Resources, accessed 2026](../../bibliography.md#hspa-instrument-resources-accessed-2026)).
That makes HSPA a strong comprehensive webpage to cite, but not a source for one
universal fourteen-surgery taxonomy.

## Why Surgical Instruments Are Not Universal

TrayGuard should not claim that a universal instrument list or universal tray
template can cover every training case. The evidence supports a more careful
claim: public instrument names and families are reusable, but real trays are
localized by facility, procedure, surgeon, vendor, count sheet, and variant.

Support:

- HPN's count-sheet guidance makes the local list operationally authoritative:
  tray name, contents, quantities, sizes, and catalog/reference numbers belong
  on the count sheet, and technicians should follow that list rather than
  memory ([Nadeau, 2024](../../bibliography.md#nadeau-2024)).
- A surgical-tray rationalization review defines tray management around local
  decisions about which instruments belong in trays, how many to include, which
  trays support which procedures, and how many trays to stock
  ([dos Santos et al., 2021](../../bibliography.md#dos-santos-et-al-2021)).
- Ahmadi et al.'s tray-configuration model uses surgeon preference cards and
  procedure-specific instrument requests, showing that requested quantities and
  actual usage vary across surgeon-procedure combinations
  ([Ahmadi et al., 2023](../../bibliography.md#ahmadi-et-al-2023)).
- Medline separates standard, custom, and specialty trays; custom trays are
  built around the needs of a hospital, surgical team, procedure, or surgeon,
  while specialty trays may be vendor loaners
  ([Medline, 2025](../../bibliography.md#medline-custom-trays-2025)).
- STERIS describes loaner trays as instruments not owned or stored by the
  facility, usually loaned by a device manufacturer for specific procedures,
  with their own IFUs and count sheets
  ([STERIS, 2021](../../bibliography.md#steris-loaner-trays-2021)).

Implication: TrayGuard's data model should separate the canonical concept
(`Mayo scissors`) from the local training item: manufacturer, size, catalog
number, local alias, photo, quantity, tray role, acceptable substitute, and
lookalike distractors.

## Recommended Hierarchy For TrayGuard

| Layer | What It Means | Evidence And Design Use |
| --- | --- | --- |
| Surgical service, specialty, or procedure family | The clinical area or type of surgery that drives which trays are needed, such as general, OB/GYN, ENT, ophthalmic, cardiovascular/thoracic, laparoscopic, urology, robotic, orthopedic, neurosurgical/spinal, trauma/transplant, dental, implants, endoscopes/probes, or powered instruments. | HSPA's Sterile Processing Instrument Manual table of contents includes general instruments plus more than a dozen specialty/device chapters. Use this layer for curriculum modules and tray-group selection, not as a fixed global list. |
| Tray, set, kit, or case cart configuration | The bundled set of instruments assembled for a procedure or family of procedures. | A surgical-tray rationalization review defines surgical trays as containers holding instruments needed for a procedure or family of procedures and says tray management asks which instruments, how many, which trays map to which procedures, and how many trays to stock ([dos Santos et al., 2021](../../bibliography.md#dos-santos-et-al-2021)). |
| Count sheet / instrument tracking list | The authoritative local list of required instruments and quantities for a tray. | Alfred et al. describe SPD assembly work where technicians access the required instrument list in an instrument tracking system, including photos, and then ensure the tray matches the required number and types of instruments ([Alfred et al., 2021](../../bibliography.md#alfred-et-al-2021)). HPN also emphasizes following count sheets rather than memory and says count sheets should include tray name, contents, quantities, sizes, and catalog/reference numbers ([Nadeau, 2024](../../bibliography.md#nadeau-2024)). |
| Instrument function family | The functional class of tools, such as cutting/dissecting, clamping/occluding, grasping/holding, retracting/exposing, suturing/stapling, suctioning/aspirating, probing/dilating, measuring/diagnostic, accessory, viewing, powered, implant, or container/case items. | HSPA's inspection textbook table of contents separates common families such as scissors, needle holders, hemostatic/ring-handled forceps, retractors, tissue/dressing forceps, and suction tubes. General surgical-instrument references also classify tools by function, including cutting/dissecting, clamping, grasping/holding, probing, dilating, retracting, and suctioning ([Encyclopedia.com, 2018](../../bibliography.md#encyclopedia-surgical-instruments-2018)). |
| Specific instrument type | The named tool a learner must recognize, such as Mayo scissors, Metzenbaum scissors, Kelly forceps, Allis forceps, Babcock forceps, Richardson retractor, Yankauer suction tip, needle holder, or scalpel handle. | This is the level where novice identification practice should usually happen. It maps to HSPA's emphasis on instrument names, lengths, uses, inspection points, and photos. |
| Variant attributes | The details that separate lookalikes or local names: straight vs curved, sharp vs blunt, toothed vs non-toothed, delicate vs heavy, length, jaw shape, ring handle, ratchet, fenestration, manufacturer catalog number, specialty-specific version, and local alias. | This layer explains why immediate feedback matters. The learner may know the family, but still confuse visually similar variants. Count-sheet and HSPA sources support variant-level fields such as sizes, catalog/reference numbers, proper name, length, use, inspection points, and testing standards. |

## Is This HSPA's Taxonomy Or Shape Similarity?

It is mainly an SPD education and tray-assembly taxonomy. HSPA separates
instruments by specialty/device chapter and by instrument family. Count sheets
and instrument tracking systems then localize that taxonomy into each hospital's
actual trays.

Shape similarity is different. It is TrayGuard's computer-vision and assessment
lens for deciding which pairs are hardest to tell apart. For example, two tools
may be in the same family and look similar, such as straight vs curved Mayo
scissors, or they may share a ring-handled silhouette while having different
clinical roles. Shape similarity is therefore useful for test design, distractor
selection, and measuring pairwise confusion, but it should not replace the
industry-facing hierarchy above.

## Full-Stack Example: Major Orthopedic Tray

Toor et al. provide a concrete example from orthopedics. Their study observed
use of a major orthopedic tray at a large academic hospital across 80 procedures.
The tray was used by orthopedic surgeons for hip arthroplasty, knee
arthroplasty, trauma, and orthopedic oncology, and the paper publishes the tray's
instrument-level configuration before and after optimization
([Toor et al., 2022](../../bibliography.md#toor-et-al-2022)).

| Hierarchy Layer | Example From The Published Tray |
| --- | --- |
| Specialty / service | Orthopedic surgery |
| Procedure families | Hip arthroplasty, knee arthroplasty, trauma, orthopedic oncology |
| Tray / kit | Major orthopedic tray |
| Tray scale | 88 instruments in the current tray; optimized proposals of 47, 67, or 51 instruments depending on method |
| Cutting and dissecting | Straight Mayo scissors, curved Mayo scissors, Metz scissors, large bone cutter |
| Clamping and occluding | Bulldog forceps, short Kelly forceps, Kocher forceps, curved Crile hemostatic forceps |
| Grasping and holding | Lauer forceps, sponge sticks, Bayonet forceps, Bonnie forceps, McKenzie forceps, Adson forceps |
| Retracting and exposing | Jackson retractors, right-angle/Langenbeck retractors, long right-angle retractors, Israel rake retractors, pointer Hohmann retractors, six-prong rake retractors, four-prong rake retractors |
| Bone / orthopedic-specific tools | Leksell rongeur, small double-action rongeur, Cobb elevators, bone curettes, Howarth elevators |
| Measuring / accessory | Ruler, No. 3 blade handles, No. 3 long blade handles, sharp towel clips, dull Edna towel clips |
| Suction | No. 9 suction tip, No. 11 short suction tip |
| Variant attributes visible in the list | straight vs curved, short vs long, small/medium/large, toothed vs nontoothed, numbered suction tips, No. 1/2/3 curettes, Cobb elevator widths of 3/4 inch, 1/2 inch, and 3/8 inch |

This example is useful because it shows the full stack in one specialty without
inventing a taxonomy:

```text
Orthopedic surgery
-> major orthopedic tray
-> hip/knee arthroplasty, trauma, orthopedic oncology use cases
-> count-sheet-style instrument list
-> instrument families such as cutting, clamping, grasping, retracting, suction
-> specific instruments such as Mayo scissors, Kelly forceps, Jackson retractors
-> variants such as curved, short, long, toothed, nontoothed, numbered, and sized
```

For TrayGuard, a module based on this kind of tray should not ask learners only
"what is this instrument?" It should also ask which family it belongs to, which
nearby variants are plausible distractors, and whether the count sheet calls for
the short, long, toothed, nontoothed, small, medium, large, or numbered version.

## Purchased Demo Kit: Basic Dissection / Specimen-Preparation Set

The project purchased a basic student minor training surgical kit from Amazon:
https://www.amazon.com/Student-Minor-Traning-Surgical-PCS/dp/B0DM6RY6GR/

Use this kit as a local demo and photo-capture set for early TrayGuard authoring,
not as a sterile clinical tray or authoritative hospital count sheet. The kit is
best treated as a basic dissection/specimen-preparation set whose packaging or
listing labels may use loose names. Before any item becomes scored module
content, verify the physical tool, local photo, accepted alias, and family.

| Labeled or visible item | More accurate instrument name | Instrument family | Main use in the teaching module |
| --- | --- | --- | --- |
| "Dissecting tissue forceps" | Dissecting scissors, straight or slightly curved; blunt/blunt or sharp/blunt depending on tips | Scissors | Cutting soft tissue or specimen material. |
| "Lister bandage scissors" | Lister bandage scissors | Scissors | Cutting bandage, gauze, tape, or material near a surface; angled blade protects underlying material. |
| "3" handle | Scalpel handle No. 3 | Scalpel / cutting handle | Holds smaller surgical blades, commonly No. 10, 11, 12, or 15. |
| "4" handle | Scalpel handle No. 4 | Scalpel / cutting handle | Holds larger surgical blades, commonly No. 20-24. |
| "6 blades" | Sterile disposable scalpel blades | Blades | Cutting/dissection; blade number determines shape and use. |
| "Straight pean hemostat" | Straight Pean hemostatic forceps | Hemostats / locking forceps | Clamping tissue, tubing, vessels, or holding material. |
| "Curved pean hemostat" | Curved Pean hemostatic forceps | Hemostats / locking forceps | Clamping or holding, with curved jaws for access around structures. |
| "Mayo Hegar needle holder" | Mayo-Hegar needle holder | Needle holders | Holding suture needles; resembles a hemostat but has shorter, stronger jaws. |
| Serrated tweezers shown | Tissue forceps / dissecting forceps, serrated | Forceps | Grasping tissue or specimen material. |
| Plain narrow tweezers shown | Dressing forceps / thumb forceps | Forceps | Handling gauze, small objects, or delicate material. |
| "Butter fly prob" | Butterfly probe / grooved director, sometimes called a director probe | Probe / director | Exploring openings, guiding cuts, separating tissue planes. |
| "Probing rod" | Probe / seeker / dissecting probe | Probe | Pointing, teasing apart tissue, probing canals or cavities. |
| Chain with hooks | Tissue retractor hooks / S-hooks with chain | Retractors / hooks | Holding tissue or specimen parts aside. |
| Long flat metal tool in kit | Spatula / dissector / blunt probe | Probe / dissector | Lifting, separating, or scraping soft material. |
| Flat handled blade-like tool at far right | Scalpel handle or micro knife handle, depending on blade compatibility | Scalpel / knife handle | Cutting or fine dissection. |
| Ring-handled clamping tools in kit | Hemostatic forceps, likely mosquito or Pean-style depending on size | Hemostats / clamps | Clamping or gripping. |
| Ring-handled cutting tools in kit | Dissecting scissors | Scissors | Cutting tissue or specimen material. |

For first-pass organization, group the purchased kit into these families:

- scalpels and blades: scalpel handles No. 3 and No. 4, disposable blades;
- scissors: dissecting scissors and Lister bandage scissors;
- forceps: dissecting/tissue forceps and dressing/thumb forceps;
- hemostats and clamps: straight Pean hemostat, curved Pean hemostat, and
  any smaller mosquito-style clamps if present;
- needle holders: Mayo-Hegar needle holder;
- probes and directors: butterfly/grooved director, probing rod, and blunt
  probe/dissector;
- retractors/hooks: S-hooks or chain retractor components.

## Practical Class List For Modules

For the first TrayGuard curriculum modules, use these classes as the top-level
instrument families:

- cutting and dissecting;
- clamping and occluding;
- grasping and holding;
- retracting and exposing;
- suturing and stapling;
- suctioning, irrigating, and aspirating;
- probing and dilating;
- measuring and diagnostic;
- viewing and visualization;
- powered instruments;
- implants and implant-related tools;
- accessories, containers, and cases.

Then attach each specific instrument to one or more local trays. This lets the
platform support both ways a novice actually learns: by tool family and by the
tray they are expected to assemble.

## Comprehensive Webpage To Cite

The best single comprehensive webpage is HSPA's
[Surgical Instrument Resources](https://myhspa.org/education/publications/surgical-instrument-resources/).
It is not a free full instrument atlas, but its public page gives the clearest
professional taxonomy signal: specialty chapters, instrument-family chapters,
instrument names, photos, uses, lengths, inspection points, and testing
standards.
