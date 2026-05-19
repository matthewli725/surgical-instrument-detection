# Surgical Instrument Lookalike Pair Catalog

## Short Answer

TrayGuard already has a declared lookalike set for the seeded basic/general tray:

- Metzenbaum scissors vs curved Mayo scissors;
- Kelly forceps vs Crile hemostat;
- Adson 1x2 forceps vs Brown-Adson forceps;
- Mayo-Hegar needle holder vs Olsen-Hegar needle holder;
- Allis tissue forceps vs Babcock tissue forceps;
- mosquito hemostat vs Kelly forceps.

That is enough for the current module acceptance requirement. A broader catalog
is useful as authoring support: it helps instructors choose meaningful
distractors, write study-card distinguishing features, generate pairwise quiz
items, and analyze `misidentified` errors separately from generic wrong answers.

The catalog should be treated as a candidate authoring list. Instrument names,
sizes, jaw patterns, catalog numbers, and accepted substitutions vary by
facility, manufacturer, specialty, and count sheet. Each pair must be verified
against the local teaching instruments before it becomes scored content.

## How To Use This Catalog

Use each pair as a candidate confusion, then convert it into local module data
only when the instructor has verified:

- both instruments appear in the local teaching set or distractor pool;
- the local names and aliases match how learners will see them;
- local photos show the distinguishing feature clearly;
- the distinction matters for the count sheet or learning objective.

Recommended data fields:

| Field | Purpose |
| --- | --- |
| `pair_id` | Stable identifier for scoring and reporting. |
| `instrument_a_id` | Expected or first instrument. |
| `instrument_b_id` | Lookalike, distractor, or alternate variant. |
| `family` | Functional family, such as cutting, clamping, grasping, suturing, suction, or retracting. |
| `confusion_basis` | Why learners may confuse them: silhouette, handles, curve, jaw pattern, teeth, tip width, size, or shared alias. |
| `distinguishing_feature` | The exact cue feedback should teach. |
| `local_verification_status` | `candidate`, `instructor_verified`, or `retired`. |
| `source_note` | Local tray/count-sheet note or reference used for authoring. |

## High-Value Starter Pairs

These pairs are good candidates for TrayGuard because they involve common
instrument families and visible features that can be taught with local photos.

| Pair | Family | Confusion Basis | Distinguishing Feature |
| --- | --- | --- | --- |
| Metzenbaum scissors vs curved Mayo scissors | Cutting/dissecting | Curved ring-handled scissors with similar length. | Metzenbaum blades are slimmer and more delicate; Mayo blades are heavier and broader. |
| Straight Mayo scissors vs curved Mayo scissors | Cutting | Same handle and blade family, different curve. | Check blade curvature and intended use. |
| Operating scissors vs Metzenbaum scissors | Cutting/dissecting | General scissor silhouette. | Compare blade profile, tip shape, and relative delicacy. |
| Iris scissors vs Metzenbaum scissors | Cutting/dissecting | Small delicate scissors. | Iris scissors are shorter and finer, often used for very delicate work. |
| Littauer suture scissors vs straight Mayo scissors | Cutting | Straight scissors used around sutures. | Littauer scissors have a notched blade tip for suture removal. |
| Kelly forceps vs Crile hemostat | Clamping/occluding | Similar curved hemostat silhouette and ring handles. | Kelly serrations are on the distal half of the jaws; Crile serrations run the full jaw length. |
| Mosquito hemostat vs Kelly forceps | Clamping/occluding | Same hemostat form at different scale. | Mosquito is shorter, finer, and more delicate. |
| Mosquito hemostat vs Crile hemostat | Clamping/occluding | Similar curved clamp shape. | Compare size and jaw length; mosquito is smaller. |
| Straight hemostat vs curved hemostat | Clamping/occluding | Same handle and ratchet, different shaft/jaw curve. | Check whether the jaws are straight or curved. |
| Kelly forceps vs Pean/Rochester-Pean forceps | Clamping/occluding | Ring-handled clamps with transverse serrations. | Pean/Rochester-Pean patterns are typically heavier/larger; verify local size and jaw details. |
| Crile hemostat vs Rochester-Carmalt forceps | Clamping/occluding | Curved ring-handled clamp silhouette. | Carmalt forceps have characteristic longitudinal serrations with cross-serrated tips. |
| Kocher/Ochsner forceps vs Kelly forceps | Clamping/occluding/grasping | Ring-handled clamps with similar profile. | Kocher/Ochsner has a tooth at the tip; Kelly does not. |
| Schnidt/tonsil forceps vs Mixter/right-angle forceps | Clamping/dissecting | Long curved or angled clamp silhouette. | Compare jaw angle, length, and specialty-specific shape. |
| Adson 1x2 forceps vs Brown-Adson forceps | Grasping/holding | Short thumb forceps with similar body. | Adson 1x2 has one tooth opposing two; Brown-Adson has multiple fine teeth. |
| Adson tissue forceps vs Adson dressing forceps | Grasping/holding | Same short thumb-forceps silhouette. | Tissue forceps have teeth; dressing forceps are non-toothed or serrated. |
| Adson forceps vs DeBakey forceps | Grasping/holding | Thumb forceps with narrow tips. | DeBakey forceps are longer with atraumatic longitudinal serrations. |
| Tissue forceps vs dressing forceps | Grasping/holding | Similar tweezer-like form. | Tissue forceps are toothed; dressing forceps are usually serrated without teeth. |
| Russian forceps vs Bonney forceps | Grasping/holding | Thumb forceps used for firm tissue. | Compare broad rounded Russian teeth against heavier toothed Bonney tips. |
| Mayo-Hegar needle holder vs Olsen-Hegar needle holder | Suturing/cutting | Ring-handled needle drivers with ratchets. | Olsen-Hegar includes integrated scissor blades; Mayo-Hegar does not. |
| Mayo-Hegar needle holder vs Crile-Wood needle holder | Suturing | Similar needle-holder silhouette. | Crile-Wood is typically finer and more delicate; verify local jaw length and size. |
| Mayo-Hegar needle holder vs hemostat | Suturing vs clamping | Ring handles and ratchet can look alike to novices. | Needle holders have short, broad, cross-hatched jaws for gripping needles. |
| Allis tissue forceps vs Babcock tissue forceps | Grasping/holding | Ring-handled tissue forceps with oval jaw area. | Allis has interlocking teeth; Babcock has smooth fenestrated jaws. |
| Allis tissue forceps vs Kocher/Ochsner forceps | Grasping/holding | Toothed ring-handled clamps. | Allis has multiple interlocking teeth along the jaw; Kocher/Ochsner has a terminal tooth. |
| Babcock tissue forceps vs Foerster sponge forceps | Grasping/holding | Ring-handled tools with fenestrated-looking jaws. | Foerster jaws are larger oval sponge-holding rings; Babcock jaws are smaller tissue-holding loops. |
| Backhaus towel clamp vs Jones towel clamp | Holding/accessory | Small pointed towel clamps. | Compare ratchet, handle form, and local towel-clamp pattern. |
| Senn retractor vs Army-Navy/Farabeuf retractor | Retracting/exposing | Handheld retractors with simple metal profile. | Senn is double-ended with a rake end; Army-Navy/Farabeuf has smooth blade ends. |
| Army-Navy retractor vs Richardson retractor | Retracting/exposing | Handheld right-angle retractor silhouette. | Richardson is larger/deeper with a single broad blade; Army-Navy is double-ended. |
| Richardson retractor vs Deaver retractor | Retracting/exposing | Large handheld retractors. | Deaver has a broad curved blade; Richardson has a right-angle blade. |
| Malleable/ribbon retractor vs Deaver retractor | Retracting/exposing | Flat curved metal retractor profile. | Malleable retractors are bendable flat strips; Deaver is a fixed curved retractor. |
| Yankauer suction tip vs Poole suction tube | Suction/aspiration | Tubular suction instruments. | Yankauer has a bulbous rigid oral tip; Poole has a perforated outer sleeve. |
| Frazier suction tip vs Baron suction tube | Suction/aspiration | Fine suction tubes. | Compare tip diameter, control vent, and specialty-specific length. |
| Freer elevator vs Cottle elevator | Probing/elevating | Double-ended ENT elevator silhouette. | Verify end shapes; many local variants differ subtly. |
| Penfield dissector variants | Neurosurgical/dissecting | Same handle family with numbered tips. | Identify the numbered tip shape, not just the handle. |
| Cobb elevator size variants | Orthopedic/elevating | Same instrument name with different widths. | Check blade width and catalog/count-sheet size. |
| Rongeur size or jaw-angle variants | Bone/orthopedic | Similar plier-like bone instruments. | Compare jaw angle, cup size, and single vs double action. |
| Curette size variants | Scraping/debriding | Same handle and cup form with numbered sizes. | Check cup diameter and count-sheet size. |

## Practical Recommendation

For the capstone, keep the scored content narrow:

1. Use the six existing lookalike pairs as the verified `basic_general_v1`
   scoring set.
2. Use this broader catalog as an instructor authoring checklist and future-work
   artifact.
3. Promote a candidate pair into a module only after local photos and local
   count-sheet language prove that the visual distinction is teachable.

That gives TrayGuard a defensible position: it supports reusable lookalike
authoring with local verification before scored use.
