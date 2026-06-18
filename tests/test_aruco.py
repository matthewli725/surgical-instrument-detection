from __future__ import annotations

import cv2
import pytest

from trayguard.learning.aruco import detect_aruco_cards, generate_marker_png


def test_generated_marker_can_be_detected(tmp_path):
    if not hasattr(cv2, "aruco"):
        pytest.skip("OpenCV ArUco module unavailable")

    marker_path = generate_marker_png(7, tmp_path / "marker.png")
    frame = cv2.imread(str(marker_path))
    detections = detect_aruco_cards(frame, {7: "forceps"})

    assert detections
    assert detections[0].marker_id == 7
    assert detections[0].instrument_id == "forceps"
