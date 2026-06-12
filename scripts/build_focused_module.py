import json
from pathlib import Path

# Read the full FGVC12 major laparotomy module
source = Path("/Users/matthewli/Projects/trayguard/config/tray_modules/fgvc12_major_laparotomy_tray_v1.json")
with open(source) as f:
    full = json.load(f)

# Selected instrument IDs
required_ids = [
    "fgvc12_major_scissors_mayo_straight_7in",
    "fgvc12_major_scissors_mayo_curved_7in",
    "fgvc12_major_scissors_metz_curved_7in",
    "fgvc12_major_clamp_kelly_6in",
    "fgvc12_major_clamp_crile_curved_5_1_2",
    "fgvc12_major_clamp_kocher_6in",
    "fgvc12_major_clamp_allis_6in",
    "fgvc12_major_clamp_babcock_6in",
    "fgvc12_major_forcep_adson_w_teeth",
    "fgvc12_major_forcep_debakey_8in_thoracic_tip",
    "fgvc12_major_needleholder_mayo_hegar_7in",
    "fgvc12_major_knife_handle_number_3_short",
]

distractor_ids = [
    "fgvc12_major_clamp_kelly_8in",
    "fgvc12_major_scissors_metz_curved_10in",
    "fgvc12_major_needleholder_mayo_hegar_8in",
    "fgvc12_major_clamp_babcock_9_5in",
]

all_ids = set(required_ids + distractor_ids)

# Filter instruments
instruments = [inst for inst in full["instruments"] if inst["id"] in all_ids]

# Filter marker_cards
marker_cards = [card for card in full["marker_cards"] if card["instrument_id"] in all_ids]

# Build required_items
required_items = [
    {
        "instrument_id": inst_id,
        "quantity": 1,
        "reference_number": f"TG-{i+1:03d}",
        "location_or_layer": "main"
    }
    for i, inst_id in enumerate(required_ids)
]

# Build lookalike pairs based on evidence from the basic_general_tray module
lookalike_pairs = [
    {
        "id": "lookalike_mayo_curved_metz_7in",
        "expected_id": "fgvc12_major_scissors_mayo_curved_7in",
        "selected_id": "fgvc12_major_scissors_metz_curved_7in",
        "feedback_message": "Mayo scissors have heavier, broader blades; Metzenbaum are slimmer and lighter for delicate tissue."
    },
    {
        "id": "lookalike_kelly_crile",
        "expected_id": "fgvc12_major_clamp_kelly_6in",
        "selected_id": "fgvc12_major_clamp_crile_curved_5_1_2",
        "feedback_message": "Check serration pattern: Kelly serrations are distal half; Crile serrations run the full jaw."
    },
    {
        "id": "lookalike_allis_babcock",
        "expected_id": "fgvc12_major_clamp_allis_6in",
        "selected_id": "fgvc12_major_clamp_babcock_6in",
        "feedback_message": "Allis has multiple interlocking teeth; Babcock has smooth fenestrated jaws."
    },
    {
        "id": "lookalike_adson_debakey",
        "expected_id": "fgvc12_major_forcep_adson_w_teeth",
        "selected_id": "fgvc12_major_forcep_debakey_8in_thoracic_tip",
        "feedback_message": "Adson is short with 1x2 teeth; DeBakey is long with atraumatic longitudinal serrations."
    },
    {
        "id": "lookalike_kelly_6_8in",
        "expected_id": "fgvc12_major_clamp_kelly_6in",
        "selected_id": "fgvc12_major_clamp_kelly_8in",
        "feedback_message": "Compare overall length: 6\" vs 8\"."
    },
    {
        "id": "lookalike_metz_7_10in",
        "expected_id": "fgvc12_major_scissors_metz_curved_7in",
        "selected_id": "fgvc12_major_scissors_metz_curved_10in",
        "feedback_message": "Compare overall length: 7\" vs 10\"."
    },
]

# Build assessment variants
assessment_variants = [
    {
        "id": "fgvc12_major_focused_v1_pre_a",
        "mode": "pre_test",
        "required_item_ids": required_ids,
        "distractor_item_ids": distractor_ids,
        "random_seed": "pre_a_2026_06",
        "feedback_enabled": False,
        "photo_view": "view_a"
    },
    {
        "id": "fgvc12_major_focused_v1_post_b",
        "mode": "post_test",
        "required_item_ids": required_ids,
        "distractor_item_ids": distractor_ids,
        "random_seed": "post_b_2026_06",
        "feedback_enabled": False,
        "photo_view": "view_b"
    }
]

module = {
    "module_id": "fgvc12_major_focused_v1",
    "version": "2026.06-fgvc12-subset",
    "name": "FGVC12 Major Laparotomy Focused Tray",
    "procedure_family": "major_laparotomy",
    "source_note": "Evidence-based subset of fgvc12_major_laparotomy_tray_v1. Selected instruments cover four primary families (cutting, clamping, grasping, suturing) and include documented lookalike pairs from the TrayGuard FDR requirements. Instructor verification required before pilot claims.",
    "evidence_sources": [
        {
            "label": "FGVC12 shared Google Drive major.zip",
            "url": "https://drive.google.com/file/d/1X3iO-FXL_7aOeOrdMNb3_oib0Les7lKD/view",
            "supports": [
                "Major tray images grouped by instrument class."
            ]
        },
        {
            "label": "TrayGuard FDR lookalike pairs",
            "url": "fdr/trayguard_paper.pdf",
            "supports": [
                "Mayo vs Metzenbaum, Kelly vs Crile, Allis vs Babcock, Adson vs DeBakey confusion documented in training literature."
            ]
        }
    ],
    "instruments": instruments,
    "required_items": required_items,
    "distractor_item_ids": distractor_ids,
    "lookalike_pairs": lookalike_pairs,
    "assessment_variants": assessment_variants,
    "marker_cards": marker_cards
}

output = Path("/Users/matthewli/Projects/trayguard/config/tray_modules/fgvc12_major_focused_v1.json")
with open(output, "w") as f:
    json.dump(module, f, indent=2)

print(f"Wrote {len(instruments)} instruments ({len(required_ids)} required + {len(distractor_ids)} distractors) to {output}")
print(f"Marker cards: {len(marker_cards)}")
