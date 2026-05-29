from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Sequence

import cv2

from trayguard.data_collection.drawing import draw_status_lines


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard collect-class-folder",
        description="Rapidly capture single-instrument images into one folder per class.",
    )
    parser.add_argument("--camera-index", type=int, default=0, help="OpenCV camera index to use.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/cv/class_folder_raw"),
        help="Directory where class folders will be created.",
    )
    parser.add_argument("--prefix", default="sample", help="Filename prefix for captured images.")
    parser.add_argument("--image-ext", choices=["jpg", "png"], default="jpg", help="Image format to save.")
    return parser.parse_args(argv)


def class_name_to_folder(class_name: str) -> str:
    folder_name = re.sub(r"[^A-Za-z0-9._-]+", "_", class_name.strip().lower())
    folder_name = folder_name.strip("._-")
    if not folder_name:
        raise ValueError("Class name must include at least one letter or number.")
    return folder_name


def prepare_class_dir(output_dir: Path, class_name: str) -> Path:
    folder_name = class_name_to_folder(class_name)
    class_dir = output_dir / folder_name
    suffix = 2

    while class_dir.exists():
        marker_path = class_dir / "_class_name.txt"
        if not marker_path.exists() or marker_path.read_text(encoding="utf-8").strip() == class_name:
            break
        class_dir = output_dir / f"{folder_name}_{suffix:02d}"
        suffix += 1

    class_dir.mkdir(parents=True, exist_ok=True)
    marker_path = class_dir / "_class_name.txt"
    if not marker_path.exists():
        marker_path.write_text(f"{class_name}\n", encoding="utf-8")

    return class_dir


def next_sample_index(class_dir: Path, prefix: str, image_ext: str) -> int:
    pattern = re.compile(rf"^{re.escape(prefix)}_(\d+)\.{re.escape(image_ext)}$", re.IGNORECASE)
    max_index = 0

    for path in class_dir.iterdir():
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match is None:
            continue
        max_index = max(max_index, int(match.group(1)))

    return max_index + 1


def draw_class_prompt(frame, class_buffer: str, status_message: str) -> None:
    lines = [
        "New class: type a class name in this window",
        "ENTER start capture | Backspace edit | ESC clear | q quit",
        f"Class: {class_buffer}_",
    ]
    if status_message:
        lines.append(status_message)
    draw_status_lines(frame, lines)


def draw_capture_status(
    frame,
    class_name: str,
    class_dir: Path,
    prefix: str,
    next_index: int,
    image_ext: str,
    saved_for_class: int,
    total_saved: int,
    status_message: str,
) -> None:
    lines = [
        f"Class: {class_name} | folder: {class_dir.name}",
        "SPACE/c save image | n new class | q quit",
        f"Saved this class: {saved_for_class} | total: {total_saved}",
        f"Next file: {prefix}_{next_index:06d}.{image_ext}",
    ]
    if status_message:
        lines.append(status_message)
    draw_status_lines(frame, lines)


def save_frame(frame, class_dir: Path, prefix: str, image_ext: str, sample_index: int) -> Path:
    image_path = class_dir / f"{prefix}_{sample_index:06d}.{image_ext}"
    ok = cv2.imwrite(str(image_path), frame)
    if not ok:
        raise RuntimeError(f"Could not write image: {image_path}")
    return image_path


def handle_prompt_key(key: int, class_buffer: str) -> tuple[str, bool, bool]:
    if key == 255:
        return class_buffer, False, False
    if key in (10, 13):
        return class_buffer, True, False
    if key == ord("q"):
        return class_buffer, False, True
    if key == 27:
        return "", False, False
    if key in (8, 127):
        return class_buffer[:-1], False, False
    if 32 <= key <= 126:
        return class_buffer + chr(key), False, False
    return class_buffer, False, False


def run_capture(
    camera_index: int,
    output_dir: Path,
    prefix: str,
    image_ext: str,
) -> int:
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        raise RuntimeError(f"Could not open webcam at index {camera_index}")

    window_name = "Class Folder Capture"
    cv2.namedWindow(window_name)

    class_buffer = ""
    class_name: str | None = None
    class_dir: Path | None = None
    next_index = 1
    saved_for_class = 0
    total_saved = 0
    status_message = "Enter the instrument class before capturing."

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("Could not read a frame from the webcam.")

            preview = frame.copy()

            if class_name is None or class_dir is None:
                draw_class_prompt(preview, class_buffer, status_message)
                cv2.imshow(window_name, preview)
                key = cv2.waitKey(20) & 0xFF
                class_buffer, accepted, should_quit = handle_prompt_key(key, class_buffer)

                if should_quit:
                    return total_saved
                if accepted:
                    requested_class = class_buffer.strip()
                    if not requested_class:
                        status_message = "Type a class name before pressing ENTER."
                        continue
                    try:
                        class_dir = prepare_class_dir(output_dir, requested_class)
                    except ValueError as exc:
                        status_message = str(exc)
                        continue

                    class_name = requested_class
                    next_index = next_sample_index(class_dir, prefix, image_ext)
                    saved_for_class = 0
                    status_message = f"Capturing into {class_dir}."
                continue

            draw_capture_status(
                preview,
                class_name=class_name,
                class_dir=class_dir,
                prefix=prefix,
                next_index=next_index,
                image_ext=image_ext,
                saved_for_class=saved_for_class,
                total_saved=total_saved,
                status_message=status_message,
            )
            cv2.imshow(window_name, preview)
            key = cv2.waitKey(20) & 0xFF

            if key in (ord(" "), ord("c")):
                image_path = save_frame(frame, class_dir, prefix, image_ext, next_index)
                next_index += 1
                saved_for_class += 1
                total_saved += 1
                status_message = f"Saved {image_path.name}."
            elif key == ord("n"):
                class_buffer = ""
                class_name = None
                class_dir = None
                next_index = 1
                saved_for_class = 0
                status_message = "Enter the next instrument class."
            elif key == ord("q"):
                return total_saved
    finally:
        camera.release()
        cv2.destroyWindow(window_name)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    try:
        total_saved = run_capture(
            camera_index=args.camera_index,
            output_dir=args.output_dir,
            prefix=args.prefix,
            image_ext=args.image_ext,
        )
    except KeyboardInterrupt:
        print(f"\nStopped class-folder capture. Images are under {args.output_dir}.")
        return

    print(f"Saved {total_saved} image(s) under {args.output_dir}.")
