from __future__ import annotations

from ultralytics import YOLO

STAGES: dict[str, tuple[str, str]] = {
    "matte -> reflective": (
        "weights/surgical_kit_matte_train_reflective_test.pt",
        "data/cv/surgical_kit_proxy/lighting/matte_train_reflective_test/data.yaml",
    ),
    "reflective -> matte": (
        "weights/surgical_kit_reflective_train_matte_test.pt",
        "data/cv/surgical_kit_proxy/lighting/reflective_train_matte_test/data.yaml",
    ),
    "shape_similarity": (
        "weights/surgical_kit_shape_similarity_real_proxy.pt",
        "data/cv/surgical_kit_proxy/shape_similarity_real_proxy/data.yaml",
    ),
}

for name, (weight, data) in STAGES.items():
    print(f"\n=== {name} ===")
    model = YOLO(weight)
    metrics = model.val(data=data, plots=False)
    for idx, cls_id in enumerate(metrics.ap_class_index):
        print(f"  {metrics.names[cls_id]}: AP50={metrics.box.ap50[idx]:.3f}")
