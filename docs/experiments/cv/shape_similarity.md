# Similar-Looking Tools

TrayGuard needs a controlled way to test whether it can separate tools that
share almost the same silhouette. This experiment is now defined as a staged
synthetic-to-real transfer study rather than a single generic fine-grained test.

## What This Test Answers

The narrow question is:

- Can TrayGuard learn discriminative cues for visually similar tool classes?
- How much does synthetic data help when real same-pair data is scarce?

The study is intentionally limited. It does not claim readiness for real
surgical instruments. It claims only that:

- fine-grained pairwise recognition can be tested under controlled tray-like
  conditions
- pairwise confusion risk can be measured directly
- synthetic data can reduce real-data requirements if synthetic pretraining
  beats a matched small-real-data baseline

## Default Pair Families

The v1 pipeline centers on intentionally difficult pairs:

- straight vs curved scissors
- straight vs curved clamp or hemostat-like tools
- narrow-tip vs broad-tip tweezer or plier-like tools
- one unknown-but-similar distractor family used only for open-set stress

These are proxy categories, not a claim of surgical-instrument coverage.

## Dataset Design

Simulation is the primary data source in v1.

- Blender or BlenderProc can be used for the synthetic side, and the repo now
  includes a bundled Blender-side planning and rendering scaffold.
- The real-proxy transfer branch still uses separately captured proxy images.
- Public 3D assets are acceptable for research prototyping if their licenses
  allow research use and the assumptions are documented.
- The initial scene family stays simple: overhead camera, tray-like plane,
  metallic materials, moderate pose variation, mild spacing variation, and only
  light clutter.
- Domain randomization should vary lighting, material roughness, camera
  distance, rotation, and tray or background texture.

The v1 design explicitly avoids full operating-room realism, articulated
physics-heavy scenes, and large clutter stacks.

## Staged Experiment Logic

The split policy is aligned to the claim being tested, not to raw image count.

### 1. `synthetic_seen_condition`

- Train and test on synthetic data from the same seen rendering domain.
- Hold out rendered scene instances between train, validation, and test.
- Meshes may overlap between train and test unless held-out mesh variants are
  explicitly provided.

This is the floor. Success here means interpolation inside the simulator.

### 2. `synthetic_heldout_condition`

- Train on one synthetic condition subset.
- Test on held-out lighting, material, camera, or background settings.
- Keep the split rationale explicit in the exported stage manifest.

Success here means the model learned more than one rendering setup.

### 3. `synthetic_to_real_transfer`

This stage is evaluated through two matched training conditions on the same
small real proxy dataset:

- `real_small_from_scratch`
- `synthetic_pretrain_plus_real_small`

The real set should prefer held-out physical instances when possible. If only
one instance exists for a class, the study should mark that as weaker evidence
and fall back to held-out sessions or conditions.

The main evidence for simulation value is improvement of
`synthetic_pretrain_plus_real_small` over `real_small_from_scratch`.

## What Each Split Proves

- Success on same-mesh synthetic test means interpolation inside the simulator.
- Success on held-out synthetic conditions means the model learned more than
  one rendering setup.
- Success on real proxy evaluation means the representation transfers beyond
  the renderer.
- Improvement after synthetic pretraining means simulation reduced the amount of
  real data needed for the same fine-grained task.

## Headline Metrics

Standard detector metrics still matter, but pairwise confusion is the headline.

Required outputs are:

- per-class precision and recall
- pairwise confusion matrix across the similar classes
- count of high-confidence wrong-similar-class predictions
- confidence histograms for correct vs wrong predictions
- unknown false-positive rate for similar distractors
- qualitative examples of the hardest failures

The most important result is not average mAP. It is whether any selected pair
still produces confident wrong-class predictions.

## Product Interpretation

| Result Pattern | What It Means | Product Response |
| --- | --- | --- |
| Similar pairs separate reliably | TrayGuard can support more specific tray checks | Keep class labels specific |
| One pair still confuses at high confidence | The riskiest failure mode remains | Make that pair a mandatory review pair |
| Confusion is mostly low confidence | The detector is failing more safely | Route those cases into a "needs review" workflow |
| Unknown similar distractors trigger known labels | Open-set behavior is unsafe | Add more data, stronger thresholds, or a separate rejection workflow |

## What We Are Not Claiming

- Proxy tools do not prove performance on all surgical instruments.
- Synthetic success alone does not prove deployment readiness.
- Fine-tuning on a small real set is useful evidence only if synthetic
  pretraining improves that matched baseline.
- Real transfer results are weaker if the dataset lacks held-out physical
  instances.

## Related Reproducibility Note

The pipeline details, source-manifest schema, stage export commands, and
training and validation commands are documented in
[`docs/experiments/reproducibility/shape_similarity_yolo_reproducibility.md`](../reproducibility/shape_similarity_yolo_reproducibility.md).

## Bibliography

See the [central bibliography](../../bibliography.md) for full source details.
