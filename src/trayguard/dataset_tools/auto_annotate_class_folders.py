from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard auto-annotate-class-folders",
        description="Auto-annotate class-folder images with bounding boxes via background subtraction, then split into YOLO and classification datasets.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/cv/50 pictures"),
        help="Root directory containing class subfolders.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/cv/50_pictures_auto"),
        help="Output root for YOLO and classification datasets.",
    )
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.8,
        help="Fraction of images per class assigned to train.",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Fraction of images per class assigned to val.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible splitting.",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=10,
        help="Pixels to add around each detected bounding box.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory.",
    )
    parser.add_argument(
        "--class-name-file",
        default="_class_name.txt",
        help="Filename inside each class folder that stores the class name.",
    )
    return parser.parse_args(argv)


def validate_ratios(train_ratio: float, val_ratio: float) -> None:
    total = train_ratio + val_ratio
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"train + val ratios must sum to 1.0, got {total:.6f}")


def discover_classes(input_dir: Path, class_name_file: str) -> list[tuple[str, Path]]:
    """Return list of (class_name, class_dir) sorted by class_name."""
    classes: list[tuple[str, Path]] = []
    for class_dir in sorted(input_dir.iterdir()):
        if not class_dir.is_dir():
            continue
        marker = class_dir / class_name_file
        if not marker.exists():
            continue
        class_name = marker.read_text(encoding="utf-8").strip()
        if not class_name:
            continue
        classes.append((class_name, class_dir))
    return classes


def discover_images(class_dir: Path) -> list[Path]:
    images = [
        path
        for path in class_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images)


def find_bounding_box(image_path: Path, padding: int = 10) -> tuple[int, int, int, int] | None:
    """Return (x1, y1, x2, y2) for the largest contour, or None if none found."""
    img = cv2.imread(str(image_path))
    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)

    height, width = img.shape[:2]
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(width, x + w + padding)
    y2 = min(height, y + h + padding)

    if x2 <= x1 or y2 <= y1:
        return None

    return (x1, y1, x2, y2)


def bbox_to_yolo(
    x1: int, y1: int, x2: int, y2: int, image_width: int, image_height: int, class_id: int
) -> str:
    cx = (x1 + x2) / 2.0 / image_width
    cy = (y1 + y2) / 2.0 / image_height
    w = (x2 - x1) / image_width
    h = (y2 - y1) / image_height
    return f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"


def split_class_images(
    images: list[Path],
    train_ratio: float,
    seed: int,
) -> tuple[list[Path], list[Path]]:
    rng = random.Random(seed)
    shuffled = images[:]
    rng.shuffle(shuffled)
    train_count = int(len(shuffled) * train_ratio)
    return shuffled[:train_count], shuffled[train_count:]


def prepare_output(output_dir: Path, overwrite: bool) -> None:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(
                f"Output directory already exists. Pass --overwrite to replace it: {output_dir}"
            )
        shutil.rmtree(output_dir)

    # YOLO structure
    for split in ("train", "val"):
        (output_dir / "yolo" / "images" / split).mkdir(parents=True, exist_ok=True)
        (output_dir / "yolo" / "labels" / split).mkdir(parents=True, exist_ok=True)

    # Classification structure
    (output_dir / "cls" / "train").mkdir(parents=True, exist_ok=True)
    (output_dir / "cls" / "val").mkdir(parents=True, exist_ok=True)


def copy_and_annotate(
    images: list[Path],
    split: str,
    class_name: str,
    class_id: int,
    output_dir: Path,
    padding: int,
    prefix: str = "",
) -> tuple[int, int]:
    """Copy images and write labels. Returns (copied_count, annotated_count).
    The *prefix* is prepended to each output filename to avoid collisions
    when multiple classes use the same source filenames."""
    copied = 0
    annotated = 0
    yolo_images_dir = output_dir / "yolo" / "images" / split
    yolo_labels_dir = output_dir / "yolo" / "labels" / split
    cls_split_dir = output_dir / "cls" / split / class_name
    cls_split_dir.mkdir(parents=True, exist_ok=True)

    for image_path in images:
        stem = f"{prefix}_{image_path.stem}" if prefix else image_path.stem

        # Detection: copy image
        image_dst = yolo_images_dir / f"{stem}{image_path.suffix.lower()}"
        shutil.copy2(image_path, image_dst)

        # Detection: write label
        label_dst = yolo_labels_dir / f"{stem}.txt"
        img = cv2.imread(str(image_path))
        if img is None:
            label_dst.write_text("", encoding="utf-8")
        else:
            height, width = img.shape[:2]
            bbox = find_bounding_box(image_path, padding=padding)
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                label_text = bbox_to_yolo(x1, y1, x2, y2, width, height, class_id)
                label_dst.write_text(label_text + "\n", encoding="utf-8")
                annotated += 1
            else:
                label_dst.write_text("", encoding="utf-8")

        # Classification: copy image to class folder
        cls_image_dst = cls_split_dir / f"{stem}{image_path.suffix.lower()}"
        shutil.copy2(image_path, cls_image_dst)

        copied += 1

    return copied, annotated


def write_data_yaml(output_dir: Path, class_names: list[str]) -> None:
    yolo_dir = output_dir / "yolo"
    lines = [
        f"path: {yolo_dir.as_posix()}",
        "train: images/train",
        "val: images/val",
        "",
        "names:",
    ]
    for idx, name in enumerate(class_names):
        lines.append(f"  {idx}: {name}")
    (yolo_dir / "data.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    validate_ratios(args.train_ratio, args.val_ratio)

    classes = discover_classes(args.input_dir, args.class_name_file)
    if not classes:
        raise ValueError(f"No class folders found in {args.input_dir}")

    prepare_output(args.output_dir, args.overwrite)

    class_names = [name for name, _dir in classes]
    class_name_to_id = {name: idx for idx, name in enumerate(class_names)}

    print("=== Auto-Annotation Summary ===")
    print(f"Input: {args.input_dir}")
    print(f"Classes: {len(class_names)}")
    print(f"Padding: {args.padding}px")
    print(f"Split: {args.train_ratio:.0%} train / {args.val_ratio:.0%} val")
    print()

    total_images = 0
    total_annotated = 0

    for class_name, class_dir in classes:
        images = discover_images(class_dir)
        if not images:
            print(f"  {class_name}: no images found — skipped")
            continue

        train_images, val_images = split_class_images(images, args.train_ratio, args.seed)
        class_id = class_name_to_id[class_name]

        prefix = class_dir.name

        train_copied, train_annotated = copy_and_annotate(
            train_images, "train", class_name, class_id, args.output_dir, args.padding, prefix=prefix
        )
        val_copied, val_annotated = copy_and_annotate(
            val_images, "val", class_name, class_id, args.output_dir, args.padding, prefix=prefix
        )

        total_images += train_copied + val_copied
        total_annotated += train_annotated + val_annotated

        print(
            f"  {class_name}: {len(images)} images — "
            f"train {train_copied} ({train_annotated} annotated), "
            f"val {val_copied} ({val_annotated} annotated)"
        )

    write_data_yaml(args.output_dir, class_names)

    print()
    print(f"Total images: {total_images}")
    print(f"Total annotated: {total_annotated}")
    print(f"YOLO dataset: {args.output_dir / 'yolo'}")
    print(f"Classification dataset: {args.output_dir / 'cls'}")
    print(f"Data yaml: {args.output_dir / 'yolo' / 'data.yaml'}")
