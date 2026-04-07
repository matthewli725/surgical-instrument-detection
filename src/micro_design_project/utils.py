from typing import Any
import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO


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
    r = results[0]

    names = model.names
    detections: list[dict[str, Any]] = []

    if r.boxes is not None and len(r.boxes) > 0:
        xyxy = r.boxes.xyxy.cpu().numpy()
        cls_ids = r.boxes.cls.cpu().numpy().astype(int)
        confs = r.boxes.conf.cpu().numpy()

        for box, cls_id, score in zip(xyxy, cls_ids, confs):
            x1, y1, x2, y2 = box.tolist()
            detections.append(
                {
                    "class_id": int(cls_id),
                    "class_name": names[int(cls_id)],
                    "confidence": float(score),
                    "bbox_xyxy": [int(x1), int(y1), int(x2), int(y2)],
                }
            )

    speed_ms = {stage: float(latency) for stage, latency in r.speed.items()}
    total_speed_ms = float(sum(speed_ms.values()))

    return {
        "detections": detections,
        "speed_ms": speed_ms,
        "total_speed_ms": total_speed_ms,
        "orig_shape": tuple(r.orig_shape),
    }


def draw_detections(
    image: np.ndarray,
    detections: list[dict[str, Any]],
) -> np.ndarray:
    annotated = image.copy()

    for det in detections:
        x1, y1, x2, y2 = det["bbox_xyxy"]
        label = f'{det["class_name"]} {det["confidence"]:.2f}'

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