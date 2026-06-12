#!/usr/bin/env bash
set -euo pipefail

BASE="model=yolo11s trainer.imgsz=640 trainer.batch=16 trainer.device=0 trainer.deterministic=true"

uv run trayguard train --export-weights weights/spoon_lighting_reference.pt \
  $BASE \
  data.name=spoon_lighting_reference \
  data.root=data/cv/spoon_lighting/reference_only \
  data.yolo_data=data/cv/spoon_lighting/reference_only/data.yaml \
  trainer.name=spoon_lighting_reference

uv run trayguard train --export-weights weights/spoon_lighting_reference_plus_45.pt \
  $BASE \
  data.name=spoon_lighting_ref_45 \
  data.root=data/cv/spoon_lighting/reference_plus_45 \
  data.yolo_data=data/cv/spoon_lighting/reference_plus_45/data.yaml \
  trainer.name=spoon_lighting_ref_45

uv run trayguard train --export-weights weights/spoon_lighting_reference_plus_45_90.pt \
  $BASE \
  data.name=spoon_lighting_ref_45_90 \
  data.root=data/cv/spoon_lighting/reference_plus_45_90 \
  data.yolo_data=data/cv/spoon_lighting/reference_plus_45_90/data.yaml \
  trainer.name=spoon_lighting_ref_45_90
