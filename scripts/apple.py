import threading
import time
from dataclasses import dataclass, field
from typing import Any

import cv2
import streamlit as st
from ultralytics import YOLO

from micro_design_project.utils import process_image, draw_detections

MODEL_PATH = "runs/detect/runs/yolo11s_imgsz960_batch16/weights/best.pt"
PHONE_CAMERA_INDEX = 0


@dataclass
class AppState:
    running: bool = False
    paused: bool = False
    completed: bool = False
    conf: float = 0.25
    imgsz: int = 640

    latest_pred: dict[str, Any] | None = None
    latest_frame: Any = None
    latest_annotated: Any = None

    worker_started: bool = False
    worker_alive: bool = False
    camera_error: str | None = None

    lock: threading.Lock = field(default_factory=threading.Lock)


@st.cache_resource
def load_model() -> YOLO:
    return YOLO(MODEL_PATH)


@st.cache_resource
def get_shared_state() -> AppState:
    return AppState()


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
                running = state.running
                paused = state.paused
                conf = state.conf
                imgsz = state.imgsz
                completed = state.completed

            if not running or paused:
                time.sleep(0.03)
                continue

            ok, frame = cap.read()
            if not ok or frame is None:
                with state.lock:
                    state.camera_error = "Failed to read frame from camera"
                time.sleep(0.05)
                continue

            pred = process_image(model, frame, imgsz=imgsz, conf=conf)
            annotated = draw_detections(frame, pred["detections"])

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

            with state.lock:
                state.latest_frame = frame.copy()
                state.latest_annotated = annotated.copy()
                state.latest_pred = pred

            time.sleep(0.01)

    finally:
        cap.release()
        with state.lock:
            state.worker_alive = False


def ensure_worker_running() -> None:
    state = get_shared_state()
    model = load_model()

    with state.lock:
        should_start = not state.worker_started or not state.worker_alive

    if should_start:
        worker = threading.Thread(
            target=video_worker,
            args=(state, model, PHONE_CAMERA_INDEX),
            daemon=True,
        )
        worker.start()
        with state.lock:
            state.worker_started = True


st.set_page_config(page_title="Hybrid Detection UI", layout="wide")
st.title("Hybrid Object Detection UI")

state = get_shared_state()
ensure_worker_running()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Start"):
        with state.lock:
            state.running = True
            state.paused = False

with col2:
    if st.button("Pause / Resume"):
        with state.lock:
            if state.running:
                state.paused = not state.paused

with col3:
    if st.button("Completed"):
        with state.lock:
            state.completed = not state.completed

with col4:
    if st.button("Stop"):
        with state.lock:
            state.running = False
            state.paused = False
            state.completed = False
            state.latest_pred = None
            state.latest_frame = None
            state.latest_annotated = None

conf = st.slider("Confidence threshold", 0.0, 1.0, 0.25, 0.01)
imgsz = st.slider("Image size", 320, 1280, 640, 32)

with state.lock:
    state.conf = conf
    state.imgsz = imgsz


@st.fragment(run_every="200ms")
def live_view():
    with state.lock:
        latest_pred = state.latest_pred
        latest_annotated = None if state.latest_annotated is None else state.latest_annotated.copy()
        running = state.running
        paused = state.paused
        completed = state.completed
        worker_alive = state.worker_alive
        camera_error = state.camera_error

    st.write(
        {
            "running": running,
            "paused": paused,
            "completed": completed,
            "worker_alive": worker_alive,
            "camera_error": camera_error,
        }
    )

    if latest_pred is not None:
        st.write(
            {
                "num_detections": len(latest_pred["detections"]),
                "latency_ms": latest_pred["total_speed_ms"],
            }
        )

    if latest_annotated is not None:
        st.image(latest_annotated, channels="BGR", caption="Live annotated frame")
    else:
        st.info("No frame yet. Press Start.")


live_view()

st.markdown("---")
st.subheader("Checklist")
st.checkbox("Phone")
st.checkbox("Keys")
st.checkbox("Wallet")
st.checkbox("Bottle")