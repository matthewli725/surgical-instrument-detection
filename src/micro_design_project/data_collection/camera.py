from __future__ import annotations

from pathlib import Path

import cv2

from micro_design_project.data_collection.annotation_ui import ImageAnnotator
from micro_design_project.data_collection.classes import write_class_names
from micro_design_project.data_collection.drawing import draw_box, draw_status_lines
from micro_design_project.data_collection.models import CollectionSession
from micro_design_project.data_collection.session_io import (
    rewrite_session_labels,
    save_image_with_shared_labels,
    save_metadata,
)


def capture_reference_image(camera_index: int, status_message: str = ""):
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        raise RuntimeError(f"Could not open webcam at index {camera_index}")

    window_name = "Capture Setup Reference"
    cv2.namedWindow(window_name)

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("Could not read a frame from the webcam.")

            preview = frame.copy()
            lines = ["New setup: SPACE/c capture reference | q quit"]
            if status_message:
                lines.append(status_message)
            draw_status_lines(preview, lines)
            cv2.imshow(window_name, preview)
            key = cv2.waitKey(20) & 0xFF

            if key in (ord(" "), ord("c")):
                return frame
            if key == ord("q"):
                raise KeyboardInterrupt
    finally:
        camera.release()
        cv2.destroyWindow(window_name)


def run_variant_capture(
    camera_index: int,
    session: CollectionSession,
    status_message: str,
    classes_path: Path,
) -> str:
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        raise RuntimeError(f"Could not open webcam at index {camera_index}")

    window_name = "Capture Lighting Variants"
    cv2.namedWindow(window_name)

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("Could not read a frame from the webcam.")

            preview = frame.copy()
            for box in session.boxes:
                draw_box(preview, box, color=(0, 255, 0))

            lines = [
                f"Setup {session.session_id}: SPACE/c save lighting variant",
                "e edit boxes | n new setup | q quit",
                status_message,
            ]
            draw_status_lines(preview, lines)
            cv2.imshow(window_name, preview)
            key = cv2.waitKey(20) & 0xFF

            if key in (ord(" "), ord("c")):
                stem = f"variant_{session.next_variant_index:04d}"
                image_path, _label_path = save_image_with_shared_labels(session, frame, stem)
                session.next_variant_index += 1
                save_metadata(session)
                status_message = f"Saved {image_path.name} with shared labels."
            elif key == ord("e"):
                cv2.destroyWindow(window_name)
                camera.release()
                updated_boxes = ImageAnnotator(frame, session.class_names, boxes=session.boxes).annotate("Edit Setup Boxes")
                if updated_boxes is None:
                    return "continue"

                session.boxes = updated_boxes
                write_class_names(classes_path, session.class_names)
                rewrite_session_labels(session)
                save_metadata(session)
                return "continue"
            elif key == ord("n"):
                return "new"
            elif key == ord("q"):
                raise KeyboardInterrupt
    finally:
        camera.release()
        cv2.destroyWindow(window_name)
