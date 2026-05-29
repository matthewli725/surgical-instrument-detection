from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize collected session class names to lowercase snake_case, "
            "collapse duplicate classes, and regenerate YOLO labels from metadata."
        )
    )
    parser.add_argument(
        "roots",
        nargs="+",
        type=Path,
        help="Collected dataset roots to normalize, e.g. data/cv/collected data/cv/collected_matthew",
    )
    return parser.parse_args()


def normalize_label(label: str) -> str:
    normalized = label.strip().lower()
    normalized = re.sub(r"[\s\-]+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_]", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.strip("_")


def write_yolo_labels(
    label_path: Path,
    boxes: list[dict[str, Any]],
    class_names: list[str],
    image_width: int,
    image_height: int,
) -> None:
    class_to_id = {name: idx for idx, name in enumerate(class_names)}
    lines: list[str] = []
    for box in boxes:
        label = box["label"]
        x1, x2 = sorted((int(box["x1"]), int(box["x2"])))
        y1, y2 = sorted((int(box["y1"]), int(box["y2"])))
        x_center = ((x1 + x2) / 2) / image_width
        y_center = ((y1 + y2) / 2) / image_height
        width = (x2 - x1) / image_width
        height = (y2 - y1) / image_height
        lines.append(f"{class_to_id[label]} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def normalize_session(session_dir: Path) -> list[str]:
    metadata_path = session_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    raw_class_names = metadata.get("class_names", [])
    raw_boxes = metadata.get("boxes", [])
    image_width = int(metadata["image_width"])
    image_height = int(metadata["image_height"])

    normalized_boxes: list[dict[str, Any]] = []
    used_labels: list[str] = []
    for box in raw_boxes:
        normalized_box = dict(box)
        normalized_box["label"] = normalize_label(str(box["label"]))
        normalized_boxes.append(normalized_box)
        if normalized_box["label"] not in used_labels:
            used_labels.append(normalized_box["label"])

    normalized_class_names: list[str] = []
    for class_name in raw_class_names:
        normalized = normalize_label(str(class_name))
        if normalized and normalized not in normalized_class_names:
            normalized_class_names.append(normalized)

    for label in used_labels:
        if label not in normalized_class_names:
            normalized_class_names.append(label)

    metadata["class_names"] = normalized_class_names
    metadata["boxes"] = normalized_boxes
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    labels_dir = session_dir / "labels"
    images_dir = session_dir / "images"
    for image_path in sorted(images_dir.iterdir()):
        if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        label_path = labels_dir / f"{image_path.stem}.txt"
        write_yolo_labels(label_path, normalized_boxes, normalized_class_names, image_width, image_height)

    return normalized_class_names


def normalize_root(root: Path) -> None:
    sessions_dir = root / "sessions"
    if not sessions_dir.exists():
        raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")

    combined_class_names: list[str] = []
    session_count = 0
    for session_dir in sorted(path for path in sessions_dir.iterdir() if path.is_dir()):
        metadata_path = session_dir / "metadata.json"
        if not metadata_path.exists():
            continue
        class_names = normalize_session(session_dir)
        for class_name in class_names:
            if class_name not in combined_class_names:
                combined_class_names.append(class_name)
        session_count += 1

    classes_path = root / "classes.txt"
    if combined_class_names or classes_path.exists():
        classes_path.write_text("\n".join(combined_class_names) + ("\n" if combined_class_names else ""), encoding="utf-8")

    print(f"{root}: normalized {session_count} session(s)")
    print(f"  classes: {', '.join(combined_class_names)}")


def main() -> None:
    args = parse_args()
    for root in args.roots:
        normalize_root(root)


if __name__ == "__main__":
    main()
