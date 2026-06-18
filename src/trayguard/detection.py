from __future__ import annotations

from typing import Any

import cv2
import numpy as np
from ultralytics import YOLO

from trayguard.data_collection.classes import resolve_class_name


def process_image(
    model: YOLO,
    image: np.ndarray,
    imgsz: int = 640,
    conf: float = 0.25,
) -> dict[str, Any]:
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy.ndarray")

    results = model.predict(
        source=image,
        imgsz=imgsz,
        conf=conf,
        save=False,
        verbose=False,
    )
    result = results[0]

    detections: list[dict[str, Any]] = []
    if result.boxes is not None and len(result.boxes) > 0:
        xyxy = result.boxes.xyxy.cpu().numpy()
        cls_ids = result.boxes.cls.cpu().numpy().astype(int)
        confs = result.boxes.conf.cpu().numpy()

        for box, cls_id, score in zip(xyxy, cls_ids, confs):
            x1, y1, x2, y2 = box.tolist()
            detections.append(
                {
                    "class_id": int(cls_id),
                    "class_name": resolve_class_name(model.names[int(cls_id)]),
                    "confidence": float(score),
                    "bbox_xyxy": [int(x1), int(y1), int(x2), int(y2)],
                }
            )

    speed_ms = {stage: float(latency) for stage, latency in result.speed.items()}

    return {
        "detections": detections,
        "speed_ms": speed_ms,
        "total_speed_ms": float(sum(speed_ms.values())),
        "orig_shape": tuple(result.orig_shape),
    }


def draw_detections(
    image: np.ndarray,
    detections: list[dict[str, Any]],
) -> np.ndarray:
    annotated = image.copy()

    for detection in detections:
        x1, y1, x2, y2 = detection["bbox_xyxy"]
        label = f'{detection["class_name"]} {detection["confidence"]:.2f}'

        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            annotated,
            label,
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    return annotated
