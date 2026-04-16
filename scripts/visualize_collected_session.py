from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import cv2


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
DEFAULT_COLLECTED_DIR = Path("data/collected")
WINDOW_NAME = "Collected Session Review"


@dataclass(frozen=True)
class Box:
    class_id: int
    label: str
    x1: int
    y1: int
    x2: int
    y2: int


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize collected session images with YOLO bounding boxes for manual verification.",
    )
    parser.add_argument(
        "session",
        nargs="?",
        help=(
            "Session directory, session id, or session id suffix. "
            "Defaults to the latest session containing images."
        ),
    )
    parser.add_argument(
        "--collected-dir",
        type=Path,
        default=DEFAULT_COLLECTED_DIR,
        help="Collected data root containing classes.txt and sessions/.",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1400,
        help="Maximum display width. Larger images are scaled down for viewing.",
    )
    parser.add_argument(
        "--max-height",
        type=int,
        default=900,
        help="Maximum display height. Larger images are scaled down for viewing.",
    )
    parser.add_argument(
        "--debug-keys",
        action="store_true",
        help="Print raw OpenCV key codes. Useful if arrow keys do not work on this platform.",
    )
    return parser.parse_args(argv)


def session_has_images(session_dir: Path) -> bool:
    images_dir = session_dir / "images"
    if not images_dir.exists():
        return False
    return any(path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS for path in images_dir.iterdir())


def resolve_session(session_arg: str | None, collected_dir: Path) -> Path:
    sessions_dir = collected_dir / "sessions"
    if not sessions_dir.exists():
        raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")

    sessions = sorted(path for path in sessions_dir.iterdir() if path.is_dir())
    if session_arg is None:
        non_empty_sessions = [path for path in sessions if session_has_images(path)]
        if not non_empty_sessions:
            raise ValueError(f"No sessions with images found under: {sessions_dir}")
        return non_empty_sessions[-1]

    direct_path = Path(session_arg)
    if direct_path.exists():
        return direct_path

    exact = sessions_dir / session_arg
    if exact.exists():
        return exact

    matches = [path for path in sessions if path.name.endswith(session_arg) or session_arg in path.name]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        options = "\n".join(f"  {path.name}" for path in matches)
        raise ValueError(f"Session selector matched multiple sessions:\n{options}")

    raise FileNotFoundError(f"Could not find session matching: {session_arg}")


def load_class_names(collected_dir: Path, session_dir: Path) -> list[str]:
    metadata_path = session_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        class_names = metadata.get("class_names", [])
        if class_names:
            return [str(name) for name in class_names]

    classes_path = collected_dir / "classes.txt"
    if not classes_path.exists():
        raise FileNotFoundError(f"Classes file not found: {classes_path}")

    class_names = [line.strip() for line in classes_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not class_names:
        raise ValueError(f"Classes file is empty: {classes_path}")
    return class_names


def list_images(session_dir: Path) -> list[Path]:
    images_dir = session_dir / "images"
    if not images_dir.exists():
        raise FileNotFoundError(f"Session images directory not found: {images_dir}")

    images = sorted(
        path for path in images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not images:
        raise ValueError(f"No images found in session: {images_dir}")
    return images


def load_boxes(label_path: Path, class_names: list[str], width: int, height: int) -> list[Box]:
    if not label_path.exists():
        return []

    boxes: list[Box] = []
    for line_number, line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue

        parts = stripped.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid YOLO label row at {label_path}:{line_number}: {line}")

        class_id = int(parts[0])
        x_center, y_center, box_width, box_height = (float(value) for value in parts[1:])
        x1 = round((x_center - box_width / 2) * width)
        y1 = round((y_center - box_height / 2) * height)
        x2 = round((x_center + box_width / 2) * width)
        y2 = round((y_center + box_height / 2) * height)
        label = class_names[class_id] if 0 <= class_id < len(class_names) else f"class_{class_id}"
        boxes.append(
            Box(
                class_id=class_id,
                label=label,
                x1=max(0, min(width - 1, x1)),
                y1=max(0, min(height - 1, y1)),
                x2=max(0, min(width - 1, x2)),
                y2=max(0, min(height - 1, y2)),
            )
        )

    return boxes


def color_for_class(class_id: int) -> tuple[int, int, int]:
    palette = (
        (55, 126, 255),
        (80, 220, 120),
        (255, 180, 60),
        (230, 90, 220),
        (70, 210, 230),
        (230, 230, 80),
        (120, 140, 255),
        (80, 180, 255),
    )
    return palette[class_id % len(palette)]


def draw_text_with_shadow(
    image,
    text: str,
    origin: tuple[int, int],
    scale: float = 0.65,
    color: tuple[int, int, int] = (255, 255, 255),
) -> None:
    cv2.putText(image, text, origin, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(image, text, origin, cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)


def draw_boxes(image, boxes: list[Box]) -> None:
    for box in boxes:
        color = color_for_class(box.class_id)
        cv2.rectangle(image, (box.x1, box.y1), (box.x2, box.y2), color, 2)
        label_origin = (box.x1, max(24, box.y1 - 8))
        draw_text_with_shadow(image, box.label, label_origin, scale=0.62, color=color)


def draw_overlay(image, session_dir: Path, image_path: Path, index: int, total: int, box_count: int) -> None:
    lines = [
        f"{session_dir.name}  {index + 1}/{total}  {image_path.name}",
        f"boxes: {box_count}   left/right: previous/next   up/down: jump 5   q/esc: quit",
    ]
    for row, line in enumerate(lines):
        draw_text_with_shadow(image, line, (12, 28 + row * 28), scale=0.65)


def fit_to_window(image, max_width: int, max_height: int):
    height, width = image.shape[:2]
    scale = min(max_width / width, max_height / height, 1.0)
    if scale >= 1.0:
        return image
    resized_width = max(1, round(width * scale))
    resized_height = max(1, round(height * scale))
    return cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_AREA)


def render_image(
    image_path: Path,
    session_dir: Path,
    class_names: list[str],
    index: int,
    total: int,
    max_width: int,
    max_height: int,
):
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    height, width = image.shape[:2]
    label_path = session_dir / "labels" / f"{image_path.stem}.txt"
    boxes = load_boxes(label_path, class_names, width, height)
    draw_boxes(image, boxes)
    draw_overlay(image, session_dir, image_path, index, total, len(boxes))
    return fit_to_window(image, max_width=max_width, max_height=max_height)


LEFT_KEYS = {2, 81, 63234, 2424832}
RIGHT_KEYS = {3, 83, 63235, 2555904}
UP_KEYS = {0, 82, 63232, 2490368}
DOWN_KEYS = {1, 84, 63233, 2621440}


def normalize_key(key: int) -> int:
    return key & 0xFF if key >= 0 else key


def run_viewer(
    session_dir: Path,
    collected_dir: Path,
    max_width: int,
    max_height: int,
    debug_keys: bool,
) -> None:
    class_names = load_class_names(collected_dir, session_dir)
    image_paths = list_images(session_dir)
    index = 0

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    print(f"Reviewing session: {session_dir}")
    print("Controls: left/right previous/next, up/down jump 5, q or esc quit")

    while True:
        rendered = render_image(
            image_paths[index],
            session_dir=session_dir,
            class_names=class_names,
            index=index,
            total=len(image_paths),
            max_width=max_width,
            max_height=max_height,
        )
        cv2.imshow(WINDOW_NAME, rendered)

        key = cv2.waitKeyEx(0)
        normalized = normalize_key(key)
        if debug_keys:
            print(f"key={key} normalized={normalized}")

        if normalized in (ord("q"), 27):
            break
        if key in LEFT_KEYS or normalized in LEFT_KEYS or normalized in (ord("a"), ord("h"), ord("p")):
            index = (index - 1) % len(image_paths)
        elif key in RIGHT_KEYS or normalized in RIGHT_KEYS or normalized in (ord("d"), ord("l"), ord("n"), ord(" ")):
            index = (index + 1) % len(image_paths)
        elif key in UP_KEYS or normalized in UP_KEYS or normalized in (ord("w"), ord("k")):
            index = max(0, index - 5)
        elif key in DOWN_KEYS or normalized in DOWN_KEYS or normalized in (ord("s"), ord("j")):
            index = min(len(image_paths) - 1, index + 5)
        elif normalized == ord("0"):
            index = 0
        elif normalized == ord("$"):
            index = len(image_paths) - 1

    cv2.destroyAllWindows()


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    session_dir = resolve_session(args.session, args.collected_dir)
    run_viewer(
        session_dir=session_dir,
        collected_dir=args.collected_dir,
        max_width=args.max_width,
        max_height=args.max_height,
        debug_keys=args.debug_keys,
    )


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from None
