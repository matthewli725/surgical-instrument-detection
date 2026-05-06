from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import cv2

from micro_design_project.data_collection.annotation_ui import ImageAnnotator
from micro_design_project.data_collection.camera import capture_reference_image, run_variant_capture
from micro_design_project.data_collection.classes import load_class_names, write_class_names
from micro_design_project.data_collection.session_io import create_session


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard collect",
        description="Capture webcam setup sessions and reuse annotations across lighting variants."
    )
    parser.add_argument("--camera-index", type=int, default=1, help="OpenCV camera index to use.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/collected"), help="Directory for session data.")
    parser.add_argument("--prefix", default="setup", help="Filename prefix for session IDs.")
    parser.add_argument("--classes-file", type=Path, default=None, help="Optional path to an existing classes.txt file.")
    parser.add_argument("--image-ext", choices=["jpg", "png"], default="jpg", help="Image format to save.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    output_dir = args.output_dir
    classes_path = args.classes_file or output_dir / "classes.txt"
    class_names = load_class_names(classes_path)
    status_message = "Ready to collect a reference setup."
    saved_sessions = 0

    try:
        while True:
            reference_image = capture_reference_image(args.camera_index, status_message=status_message)
            annotator = ImageAnnotator(reference_image, class_names)
            boxes = annotator.annotate("Annotate Setup Reference")

            if boxes is None:
                status_message = "Retaking setup reference."
                continue

            session = create_session(
                output_dir=output_dir,
                prefix=args.prefix,
                image=reference_image,
                boxes=boxes,
                class_names=class_names,
                image_ext=args.image_ext,
            )
            write_class_names(classes_path, class_names)
            saved_sessions += 1
            status_message = "Saved reference. Vary lighting, then save variants."

            while True:
                action = run_variant_capture(args.camera_index, session, status_message, classes_path)
                if action == "new":
                    status_message = "Starting a new setup."
                    break
                status_message = "Updated setup. Continue saving lighting variants."
    except KeyboardInterrupt:
        print(f"\nStopped data collection. Saved {saved_sessions} setup session(s) to {output_dir / 'sessions'}.")
    finally:
        cv2.destroyAllWindows()
