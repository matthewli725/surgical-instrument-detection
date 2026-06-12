from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import cv2
import yaml

YOLO_DIR = Path("data/cv/50_pictures_auto/yolo")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


@dataclass
class AnnotatedSample:
    split: str
    image_path: Path
    class_id: int
    class_name: str
    bbox_xyxy: tuple[int, int, int, int]  # (x1, y1, x2, y2)
    confidence: float | None


def load_class_names(data_yaml: Path) -> list[str]:
    with open(data_yaml) as f:
        cfg = yaml.safe_load(f)
    return [cfg["names"][i] for i in range(len(cfg["names"]))]


def discover_samples(yolo_dir: Path, class_names: list[str]) -> list[AnnotatedSample]:
    samples: list[AnnotatedSample] = []

    for split in ("train", "val"):
        labels_dir = yolo_dir / "labels" / split
        images_dir = yolo_dir / "images" / split

        if not labels_dir.exists():
            continue

        for label_path in sorted(labels_dir.iterdir()):
            if label_path.suffix != ".txt":
                continue

            stem = label_path.stem

            image_path: Path | None = None
            for ext in IMAGE_EXTENSIONS:
                candidate = images_dir / f"{stem}{ext}"
                if candidate.exists():
                    image_path = candidate
                    break

            if image_path is None:
                continue

            text = label_path.read_text(encoding="utf-8").strip()
            if not text:
                continue

            parts = text.split()
            class_id = int(parts[0])
            cx, cy, w, h = map(float, parts[1:5])
            confidence = float(parts[5]) if len(parts) > 5 else None

            img = cv2.imread(str(image_path))
            if img is None:
                continue
            height, width = img.shape[:2]

            x1 = int((cx - w / 2) * width)
            y1 = int((cy - h / 2) * height)
            x2 = int((cx + w / 2) * width)
            y2 = int((cy + h / 2) * height)

            samples.append(
                AnnotatedSample(
                    split=split,
                    image_path=image_path,
                    class_id=class_id,
                    class_name=class_names[class_id] if class_id < len(class_names) else f"class_{class_id}",
                    bbox_xyxy=(max(0, x1), max(0, y1), min(width, x2), min(height, y2)),
                    confidence=confidence,
                )
            )

    return samples


def draw_sample(sample: AnnotatedSample, index: int, total: int) -> cv2.Mat:
    img = cv2.imread(str(sample.image_path))
    if img is None:
        img = cv2.imread(str(sample.image_path.parent / f"{sample.image_path.stem}.jpg"))
    if img is None:
        img = 128 * cv2.ones((480, 640, 3), dtype="uint8")
        cv2.putText(img, "IMAGE NOT FOUND", (160, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    x1, y1, x2, y2 = sample.bbox_xyxy

    color = (0, 255, 0)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    label = sample.class_name
    if sample.confidence is not None:
        label += f" {sample.confidence:.2f}"

    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    label_y = max(y1 - 8, th + 6)
    cv2.rectangle(img, (x1, label_y - th - 4), (x1 + tw + 6, label_y + 4), color, -1)
    cv2.putText(img, label, (x1 + 3, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

    info = f"{sample.image_path.name}  |  class {sample.class_id}: {sample.class_name}  |  {sample.split}  |  ({index + 1}/{total})"
    cv2.rectangle(img, (0, 0), (len(info) * 8 + 20, 28), (0, 0, 0), -1)
    cv2.putText(img, info, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    bbox_info = f"bbox: [{x1}, {y1}, {x2}, {y2}]  ({x2 - x1}x{y2 - y1}px)"
    cv2.putText(img, bbox_info, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

    return img


def main():
    data_yaml = YOLO_DIR / "data.yaml"
    if not data_yaml.exists():
        print(f"data.yaml not found: {data_yaml}")
        return

    class_names = load_class_names(data_yaml)
    print(f"Classes ({len(class_names)}): {', '.join(class_names)}")

    samples = discover_samples(YOLO_DIR, class_names)
    if not samples:
        print("No annotated samples found.")
        return

    print(f"Loaded {len(samples)} samples (train={sum(1 for s in samples if s.split=='train')}, val={sum(1 for s in samples if s.split=='val')})")
    print()
    print("Controls:")
    print("  d / a     next / previous")
    print("  w / s     jump ±10")
    print("  → / ←     next / previous (macOS: may not work)")
    print("  ↑ / ↓     jump ±10 (macOS: may not work)")
    print("  g         go to index (type in terminal)")
    print("  q / ESC   quit")
    print()

    index = 0
    total = len(samples)
    window_name = "Annotated Dataset Browser — d/a next  w/s ±10  g goto  q quit"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 960, 720)

    while True:
        sample = samples[index]
        img = draw_sample(sample, index, total)
        cv2.imshow(window_name, img)

        key = cv2.waitKey(0) & 0xFF  # waitKey for reliable cross-platform ASCII

        if key == ord("q") or key == 27:  # q or ESC
            break
        elif key in (ord("d"), 0x27):  # d or right arrow mapped value
            index = min(total - 1, index + 1)
        elif key in (ord("a"), 0x25):  # a or left arrow mapped value
            index = max(0, index - 1)
        elif key in (ord("w"), 0x26):  # w or up arrow mapped value
            index = max(0, index - 10)
        elif key in (ord("s"), 0x28):  # s or down arrow mapped value
            index = min(total - 1, index + 10)
        elif key == ord("g"):
            goto = input(f"Go to image (1-{total}): ").strip()
            try:
                idx = int(goto) - 1
                if 0 <= idx < total:
                    index = idx
            except ValueError:
                pass

    cv2.destroyAllWindows()
    print(f"Stopped at image {index + 1}/{total}.")


if __name__ == "__main__":
    main()
