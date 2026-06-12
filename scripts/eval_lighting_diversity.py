from __future__ import annotations

from ultralytics import YOLO

STAGES: dict[str, tuple[str, str]] = {
    "reference only": (
        "weights/spoon_lighting_reference.pt",
        "data/cv/spoon_lighting/reference_only/data.yaml",
    ),
    "reference + 45": (
        "weights/spoon_lighting_reference_plus_45.pt",
        "data/cv/spoon_lighting/reference_plus_45/data.yaml",
    ),
    "reference + 45 + 90": (
        "weights/spoon_lighting_reference_plus_45_90.pt",
        "data/cv/spoon_lighting/reference_plus_45_90/data.yaml",
    ),
}

for name, (weight, data) in STAGES.items():
    print(f"\n=== {name} ===")
    model = YOLO(weight)
    metrics = model.val(data=data, plots=False)
    print(f"  P={metrics.box.mp:.3f}, R={metrics.box.mr:.3f}, "
          f"mAP50={metrics.box.map50:.3f}, mAP50-95={metrics.box.map:.3f}")
    for idx, cls_id in enumerate(metrics.ap_class_index):
        print(f"  {metrics.names[cls_id]}: AP50={metrics.box.ap50[idx]:.3f}")
