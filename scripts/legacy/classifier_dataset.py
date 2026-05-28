from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image
import math


DETECTION_DATASET_ROOT = Path("datasets/dataset_obj_detection")
OUTPUT_ROOT = Path("datasets/dataset_classifier")

SPLITS = ["train", "val", "test"]

CLASS_NAMES: Dict[int, str] = {
    0: "scalpel_n4",
    1: "straight_dissection_clamp",
    2: "straight_mayo_scissor",
    3: "curved_mayo_scissor",
}

PADDING_FRAC = 0.10

MIN_CROP_SIZE = 4

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def ensure_dirs() -> None:
    for split in SPLITS:
        for class_name in CLASS_NAMES.values():
            (OUTPUT_ROOT / split / class_name).mkdir(parents=True, exist_ok=True)


def find_image_files(split: str) -> List[Path]:
    image_dir = DETECTION_DATASET_ROOT / "images" / split
    if not image_dir.exists():
        raise FileNotFoundError(f"Missing image directory: {image_dir}")

    return sorted(
        [p for p in image_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    )

def yolo_to_xyxy(
    x_center: float,
    y_center: float,
    width: float,
    height: float,
    img_w: int,
    img_h: int,
) -> Tuple[int, int, int, int]:
    """
    Convert normalized YOLO box to pixel xyxy.
    """
    x_c = x_center * img_w
    y_c = y_center * img_h
    w = width * img_w
    h = height * img_h

    x1 = x_c - w / 2
    y1 = y_c - h / 2
    x2 = x_c + w / 2
    y2 = y_c + h / 2

    return int(math.floor(x1)), int(math.floor(y1)), int(math.ceil(x2)), int(math.ceil(y2))

def add_padding(
    x1: int, y1: int, x2: int, y2: int, img_w: int, img_h: int, pad_frac: float
) -> Tuple[int, int, int, int]:
    bw = x2 - x1
    bh = y2 - y1

    pad_x = int(round(bw * pad_frac))
    pad_y = int(round(bh * pad_frac))

    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(img_w, x2 + pad_x)
    y2 = min(img_h, y2 + pad_y)

    return x1, y1, x2, y2


def is_valid_crop(x1: int, y1: int, x2: int, y2: int) -> bool:
    return (x2 - x1) >= MIN_CROP_SIZE and (y2 - y1) >= MIN_CROP_SIZE


def parse_label_file(label_path: Path) -> List[Tuple[int, float, float, float, float]]:
    """
    Returns a list of tuples:
    (class_id, x_center, y_center, width, height)
    """
    rows = []

    if not label_path.exists():
        return rows

    with open(label_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 5:
                print(f"[WARNING] Skipping malformed line in {label_path} line {line_num}: {line}")
                continue

            try:
                class_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
            except ValueError:
                print(f"[WARNING] Skipping non-numeric line in {label_path} line {line_num}: {line}")
                continue

            if class_id not in CLASS_NAMES:
                print(f"[WARNING] Unknown class_id={class_id} in {label_path} line {line_num}")
                continue

            rows.append((class_id, x_center, y_center, width, height))

    return rows


def build_crops_for_split(split: str) -> int:
    image_paths = find_image_files(split)
    crop_count = 0

    for image_path in image_paths:
        label_path = DETECTION_DATASET_ROOT / "labels" / split / f"{image_path.stem}.txt"
        rows = parse_label_file(label_path)

        if not rows:
            continue

        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            print(f"[WARNING] Could not open image {image_path}: {e}")
            continue

        img_w, img_h = image.size

        for obj_idx, (class_id, x_center, y_center, width, height) in enumerate(rows):
            x1, y1, x2, y2 = yolo_to_xyxy(x_center, y_center, width, height, img_w, img_h)
            x1, y1, x2, y2 = add_padding(x1, y1, x2, y2, img_w, img_h, PADDING_FRAC)

            if not is_valid_crop(x1, y1, x2, y2):
                print(
                    f"[WARNING] Invalid/small crop skipped for {image_path.name} "
                    f"obj_idx={obj_idx} class_id={class_id}"
                )
                continue

            crop = image.crop((x1, y1, x2, y2))

            class_name = CLASS_NAMES[class_id]
            out_name = f"{image_path.stem}_obj{obj_idx}_cls{class_id}.jpg"
            out_path = OUTPUT_ROOT / split / class_name / out_name

            crop.save(out_path, quality=95)
            crop_count += 1

    return crop_count


def main() -> None:
    ensure_dirs()

    total = 0
    for split in SPLITS:
        count = build_crops_for_split(split)
        total += count
        print(f"[INFO] Built {count} crops for split='{split}'")

    print(f"[INFO] Done. Total crops saved: {total}")
    print(f"[INFO] Output dataset: {OUTPUT_ROOT.resolve()}")


if __name__ == "__main__":
    main()