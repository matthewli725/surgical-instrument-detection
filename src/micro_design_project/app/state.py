from __future__ import annotations

import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

import cv2
from ultralytics import YOLO

from micro_design_project.detection import draw_detections, process_image


@dataclass
class TrayRequirement:
    name: str
    required: int = 1


@dataclass
class DetectionSnapshot:
    prediction: dict[str, Any] | None = None
    annotated_frame: Any = None
    class_counts: Counter[str] = field(default_factory=Counter)


@dataclass
class AppState:
    running: bool = False
    paused: bool = False
    completed: bool = False
    stop_requested: bool = False
    conf: float = 0.25
    imgsz: int = 640

    snapshot: DetectionSnapshot = field(default_factory=DetectionSnapshot)
    worker_started: bool = False
    worker_alive: bool = False
    camera_error: str | None = None

    lock: threading.Lock = field(default_factory=threading.Lock)


def detection_counts(prediction: dict[str, Any] | None) -> Counter[str]:
    counts: Counter[str] = Counter()
    if prediction is None:
        return counts

    for detection in prediction["detections"]:
        counts[detection["class_name"]] += 1
    return counts


def draw_status_banner(frame: Any, completed: bool) -> Any:
    annotated = frame.copy()
    status_text = "COMPLETED" if completed else "IN PROGRESS"
    cv2.putText(
        annotated,
        status_text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0) if completed else (0, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return annotated


def video_worker(state: AppState, model: YOLO, camera_index: int) -> None:
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        with state.lock:
            state.camera_error = f"Could not open camera index {camera_index}"
            state.worker_alive = False
        return

    with state.lock:
        state.camera_error = None
        state.worker_alive = True

    try:
        while True:
            with state.lock:
                stop_requested = state.stop_requested
                running = state.running
                paused = state.paused
                conf = state.conf
                imgsz = state.imgsz
                completed = state.completed

            if stop_requested:
                break

            if not running or paused:
                time.sleep(0.03)
                continue

            ok, frame = cap.read()
            if not ok or frame is None:
                with state.lock:
                    state.camera_error = "Failed to read frame from camera"
                time.sleep(0.05)
                continue

            prediction = process_image(model, frame, imgsz=imgsz, conf=conf)
            annotated = draw_detections(frame, prediction["detections"])
            annotated = draw_status_banner(annotated, completed=completed)

            with state.lock:
                state.snapshot = DetectionSnapshot(
                    prediction=prediction,
                    annotated_frame=annotated,
                    class_counts=detection_counts(prediction),
                )

            time.sleep(0.01)
    finally:
        cap.release()
        with state.lock:
            state.worker_alive = False
            state.worker_started = False
            state.stop_requested = False


def ensure_worker_running(state: AppState, model: YOLO, camera_index: int) -> None:
    with state.lock:
        should_start = not state.worker_started or not state.worker_alive

    if not should_start:
        return

    worker = threading.Thread(
        target=video_worker,
        args=(state, model, camera_index),
        daemon=True,
    )
    worker.start()

    with state.lock:
        state.worker_started = True
        state.worker_alive = True
