from __future__ import annotations

from typing import TYPE_CHECKING
from collections import Counter
from pathlib import Path

import streamlit as st

from trayguard.app.state import AppState, TrayRequirement, ensure_worker_running
from trayguard.learning.models import TrayModule
from trayguard.learning.module import load_tray_module

if TYPE_CHECKING:
    from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODULE_PATH = PROJECT_ROOT / "config" / "tray_modules" / "50_pictures_demo_v1.json"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "weights" / "50_pictures_detection.pt"
FALLBACK_MODEL_PATH = PROJECT_ROOT / "yolo11s.pt"
DEFAULT_CAMERA_INDEX = 0


@st.cache_resource(show_spinner="Loading detection model...")
def load_model(model_path: str) -> YOLO:
    from ultralytics import YOLO

    return YOLO(model_path)


@st.cache_resource
def get_shared_state() -> AppState:
    return AppState()


@st.cache_resource(show_spinner="Loading tray module...")
def get_tray_module(module_path: str) -> TrayModule:
    return load_tray_module(module_path)


def parse_requirements(raw_value: str) -> list[TrayRequirement]:
    requirements: list[TrayRequirement] = []
    for line in raw_value.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if ":" in stripped:
            name, required = stripped.rsplit(":", maxsplit=1)
            try:
                count = max(1, int(required))
            except ValueError:
                count = 1
            display_name = name.strip()
            requirements.append(TrayRequirement(instrument_id=display_name, name=display_name, required=count))
        else:
            requirements.append(TrayRequirement(instrument_id=stripped, name=stripped, required=1))

    return requirements


def module_requirements(module: TrayModule) -> list[TrayRequirement]:
    requirements: list[TrayRequirement] = []
    for instrument_id, item in module.required_items.items():
        instrument = module.instruments[instrument_id]
        requirements.append(
            TrayRequirement(
                instrument_id=instrument_id,
                name=instrument.display_name,
                required=item.quantity,
                aliases=tuple(instrument.aliases),
            )
        )
    return requirements


def observed_count(requirement: TrayRequirement, counts: Counter[str]) -> int:
    names = (requirement.instrument_id, requirement.name, *requirement.aliases)
    return max(counts[name] for name in names)


def default_model_path() -> Path:
    if DEFAULT_MODEL_PATH.exists():
        return DEFAULT_MODEL_PATH
    return FALLBACK_MODEL_PATH


def render_controls(state: AppState) -> tuple[str, int]:
    st.sidebar.header("Run Settings")
    model_path = st.sidebar.text_input("Model weights", value=str(default_model_path()))
    camera_index = st.sidebar.number_input("Camera index", min_value=0, max_value=10, value=DEFAULT_CAMERA_INDEX, step=1)

    conf = st.sidebar.slider("Confidence threshold", 0.0, 1.0, state.conf, 0.01)
    imgsz = st.sidebar.slider("Image size", 320, 1280, state.imgsz, 32)

    with state.lock:
        state.conf = conf
        state.imgsz = imgsz

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Start", width='stretch'):
            with state.lock:
                if not state.worker_started and not state.worker_alive:
                    state.stop_requested = False
                state.running = True
                state.paused = False
    with col2:
        if st.button("Pause / Resume", width='stretch'):
            with state.lock:
                if state.running:
                    state.paused = not state.paused
    with col3:
        if st.button("Toggle Complete", width='stretch'):
            with state.lock:
                state.completed = not state.completed
    with col4:
        if st.button("Stop", width='stretch'):
            with state.lock:
                state.stop_requested = True
                state.running = False
                state.paused = False
                state.completed = False
                state.camera_error = None
                state.snapshot.prediction = None
                state.snapshot.annotated_frame = None
                state.snapshot.class_counts = Counter()

    return model_path, int(camera_index)


def render_status(state: AppState) -> None:
    with state.lock:
        running = state.running
        paused = state.paused
        completed = state.completed
        worker_alive = state.worker_alive
        camera_error = state.camera_error
        prediction = state.snapshot.prediction

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Camera", "Live" if worker_alive else "Offline")
    col2.metric("Run State", "Paused" if paused else "Running" if running else "Stopped")
    col3.metric("Tray", "Complete" if completed else "Open")
    col4.metric("Latency", f"{prediction['total_speed_ms']:.1f} ms" if prediction else "-")

    if camera_error:
        st.error(camera_error)


def render_checklist(requirements: list[TrayRequirement], counts: Counter[str]) -> None:
    st.subheader("Tray Checklist")

    if not requirements:
        st.info("No required items were found in the loaded tray module.")
        return

    for index, requirement in enumerate(requirements):
        observed = observed_count(requirement, counts)
        done = observed >= requirement.required
        st.checkbox(
            f"{requirement.name} ({observed}/{requirement.required})",
            value=done,
            disabled=True,
            key=f"requirement-{index}-{requirement.name}",
        )


@st.fragment(run_every="100ms")
def render_live_dashboard(state: AppState, requirements: list[TrayRequirement]) -> None:
    with state.lock:
        snapshot = state.snapshot
        annotated_frame = None if snapshot.annotated_frame is None else snapshot.annotated_frame.copy()
        counts = snapshot.class_counts.copy()

    render_status(state)
    left, right = st.columns([2, 1])
    with left:
        if annotated_frame is None:
            st.info("Press Start to begin detection.")
        else:
            st.image(annotated_frame, channels="BGR", width='stretch')
    with right:
        render_checklist(requirements, counts)


def main() -> None:
    st.set_page_config(page_title="TrayGuard Detection", layout="wide")
    st.title("TrayGuard Detection")

    state = get_shared_state()
    module_path = st.sidebar.text_input("Tray module", value=str(DEFAULT_MODULE_PATH))
    try:
        module = get_tray_module(str(Path(module_path).expanduser()))
        st.sidebar.caption(f"Loaded {module.name} ({module.module_id}, {module.total_required_units} required units)")
    except (OSError, ValueError) as exc:
        st.sidebar.warning(f"Tray module not loaded — running in detection-only mode: {exc}")
        module = None

    model_path, camera_index = render_controls(state)
    requirements = module_requirements(module) if module else []

    model_file = Path(model_path).expanduser()
    with state.lock:
        should_initialize = state.running or state.worker_started or state.worker_alive

    if should_initialize and not model_file.exists():
        st.warning(f"Model weights not found: {model_file}")
    elif should_initialize:
        model = load_model(str(model_file))
        ensure_worker_running(state, model, camera_index, str(model_file))

    render_live_dashboard(state, requirements)



if __name__ == "__main__":
    main()
