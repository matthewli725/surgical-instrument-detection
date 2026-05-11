# Week 03 Update

## Completed

- Completed the physical and software setup for data collection.
- Began varying lighting qualitatively with rough measurements on distance and
  angle.
- Researched BRDF and related material-property representations.
- Confirmed that human visual perception is dominated by a small number of
  major factors.
- Found that BRDF measurement requires special instruments such as a goniometer
  and tends to assume simple polygonal objects.
- Concluded that full BRDF measurement may be overkill for this prototype and
  began investigating RGB specularity-removal approaches instead.
- Found evidence that silverware and surgical tools can be made from the same
  class of steel alloy.

## Goals For Next Week

- Synthesize the research into one compelling project story.
- Perform a cost-benefit analysis across the full system:
  - CV versus other technologies versus human labor
  - CV risk factors
  - system-level operational risk factors
- Investigate CV risk factors:
  - lighting conditions in SPD environments
  - whether technicians work with overlapping instruments
  - whether CV can reliably identify similar instruments
  - how much training data similar-instrument recognition requires
- Investigate system risk factors:
  - whether the system would disrupt current workflows
  - whether there is enough space in SPD to include the system
  - whether the system is intuitive enough to plug and play
  - whether the system is easy to deploy
  - whether the system can be maintained and updated easily
- Design and perform experiments showing whether CV can detect similar objects
  and partially occluded objects.
- Collect more data for the lighting experiment.
- Preferably create a graph of light intensity versus detection rate or
  `mAP50-95` to show the lighting failure mode clearly.
