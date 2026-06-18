#!/usr/bin/env bash
set -euo pipefail

BASE="model=yolo11s trainer.imgsz=640 trainer.batch=16 trainer.device=0 trainer.deterministic=true"

uv run trayguard train --export-weights weights/surgical_kit_matte_train_reflective_test.pt \
  $BASE \
  data.name=surgical_kit_matte \
  data.root=data/cv/surgical_kit_proxy/lighting/matte_train_reflective_test \
  data.yolo_data=data/cv/surgical_kit_proxy/lighting/matte_train_reflective_test/data.yaml \
  trainer.name=surgical_kit_matte

uv run trayguard train --export-weights weights/surgical_kit_reflective_train_matte_test.pt \
  $BASE \
  data.name=surgical_kit_reflective \
  data.root=data/cv/surgical_kit_proxy/lighting/reflective_train_matte_test \
  data.yolo_data=data/cv/surgical_kit_proxy/lighting/reflective_train_matte_test/data.yaml \
  trainer.name=surgical_kit_reflective

uv run trayguard train --export-weights weights/surgical_kit_shape_similarity_real_proxy.pt \
  $BASE \
  data.name=surgical_kit_shape \
  data.root=data/cv/surgical_kit_proxy/shape_similarity_real_proxy \
  data.yolo_data=data/cv/surgical_kit_proxy/shape_similarity_real_proxy/data.yaml \
  trainer.name=surgical_kit_shape
