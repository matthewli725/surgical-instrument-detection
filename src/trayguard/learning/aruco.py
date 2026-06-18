from __future__ import annotations

import base64
from pathlib import Path

import cv2
import numpy as np

from trayguard.learning.models import DetectedCard


ARUCO_DICTIONARY_NAME = "DICT_APRILTAG_36h11"


def aruco_dictionary():
    return cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, ARUCO_DICTIONARY_NAME))


def decode_data_url(data_url: str):
    _, _, payload = data_url.partition(",")
    raw = base64.b64decode(payload or data_url)
    array = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Could not decode image payload.")
    return frame


def detect_aruco_cards(frame, marker_map: dict[int, str]) -> list[DetectedCard]:
    dictionary = aruco_dictionary()
    detector = cv2.aruco.ArucoDetector(dictionary, cv2.aruco.DetectorParameters())
    corners, ids, _rejected = detector.detectMarkers(frame)
    if ids is None:
        return []

    detections: list[DetectedCard] = []
    for marker_id, marker_corners in zip(ids.flatten().tolist(), corners):
        detections.append(
            DetectedCard(
                marker_id=int(marker_id),
                instrument_id=marker_map.get(int(marker_id)),
                corners=np.asarray(marker_corners[0], dtype=float).round(2).tolist(),
            )
        )
    return detections


def generate_marker_png(marker_id: int, destination: Path, size_px: int = 420) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    marker = cv2.aruco.generateImageMarker(aruco_dictionary(), int(marker_id), int(size_px))
    margin = max(24, size_px // 10)
    canvas = np.full((size_px + margin * 2, size_px + margin * 2), 255, dtype=np.uint8)
    canvas[margin:margin + size_px, margin:margin + size_px] = marker
    ok = cv2.imwrite(str(destination), canvas)
    if not ok:
        raise RuntimeError(f"Failed to write marker image: {destination}")
    return destination
