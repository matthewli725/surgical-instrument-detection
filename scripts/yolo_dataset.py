from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import shutil
from typing import Iterable

# =========================
# Configuration
# =========================

@dataclass(frozen=True)
class DatasetConfig:
    dataset_root: Path
    output_root: Path

    images_dir: Path
    labels_dir: Path

    class_names: list[str]

    image_extensions: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    label_extension: str = ".txt"

    train_ratio: float = 0.7
    val_ratio: float = 0.2
    test_ratio: float = 0.1

    seed: int = 42

    # If True, create empty label files when an image has no label file.
    # This is valid for YOLO object detection when the image truly has no objects.
    create_empty_labels_for_missing: bool = True

    # If True, overwrite files already present in the output dataset.
    overwrite_output: bool = True

    # Optional manifest files listing image paths inside the YOLO dataset.
    write_split_manifests: bool = True


CONFIG = DatasetConfig(
    dataset_root=Path("data/Surgical-Dataset"),
    output_root=Path("data/lavado"),
    images_dir=Path("data/Surgical-Dataset/Images/All/images"),
    labels_dir=Path("data/Surgical-Dataset/Labels/label object names"),
    class_names=[
        "Scalpel n4",
        "Straight Dissection Clamp",
        "Straight Mayo Scissor",
        "Curved Mayo Scissor",
    ],
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1,
    seed=42,
    create_empty_labels_for_missing=True,
    overwrite_output=True,
    write_split_manifests=True,
)

# =========================
# Data model
# =========================

@dataclass(frozen=True)
class Sample:
    image_path: Path
    label_path: Path | None

    @property
    def image_name(self) -> str:
        return self.image_path.name

    @property
    def stem(self) -> str:
        return self.image_path.stem


# =========================
# Validation helpers
# =========================

def validate_config(config: DatasetConfig) -> None:
    total = config.train_ratio + config.val_ratio + config.test_ratio
    if abs(total - 1.0) > 1e-9:
        raise ValueError(
            f"Split ratios must sum to 1.0, got {total:.6f} "
            f"(train={config.train_ratio}, val={config.val_ratio}, test={config.test_ratio})"
        )

    if not config.images_dir.exists():
        raise FileNotFoundError(f"Images directory not found: {config.images_dir}")

    if not config.labels_dir.exists():
        raise FileNotFoundError(f"Labels directory not found: {config.labels_dir}")


def ensure_output_dirs(output_root: Path) -> None:
    for split in ("train", "val", "test"):
        (output_root / "images" / split).mkdir(parents=True, exist_ok=True)
        (output_root / "labels" / split).mkdir(parents=True, exist_ok=True)

    (output_root / "manifests").mkdir(parents=True, exist_ok=True)


# =========================
# Discovery
# =========================

def is_image_file(path: Path, allowed_exts: Iterable[str]) -> bool:
    return path.is_file() and path.suffix.lower() in set(ext.lower() for ext in allowed_exts)


def discover_image_files(images_dir: Path, image_extensions: tuple[str, ...]) -> list[Path]:
    files = [p for p in images_dir.iterdir() if is_image_file(p, image_extensions)]
    return sorted(files, key=lambda p: p.name)


def build_samples(config: DatasetConfig) -> list[Sample]:
    image_files = discover_image_files(config.images_dir, config.image_extensions)
    samples: list[Sample] = []

    for image_path in image_files:
        candidate_label = config.labels_dir / f"{image_path.stem}{config.label_extension}"
        label_path = candidate_label if candidate_label.exists() else None
        samples.append(Sample(image_path=image_path, label_path=label_path))

    return samples


# =========================
# Reporting
# =========================

def summarize_samples(samples: list[Sample]) -> None:
    total = len(samples)
    with_labels = sum(1 for s in samples if s.label_path is not None)
    without_labels = total - with_labels

    print("=== Dataset Summary ===")
    print(f"Discovered images: {total}")
    print(f"Images with labels: {with_labels}")
    print(f"Images without labels: {without_labels}")


# =========================
# Split logic
# =========================

def split_samples(
    samples: list[Sample],
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> tuple[list[Sample], list[Sample], list[Sample]]:
    rng = random.Random(seed)
    shuffled = samples[:]
    rng.shuffle(shuffled)

    total = len(shuffled)
    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)
    test_count = total - train_count - val_count

    train_samples = shuffled[:train_count]
    val_samples = shuffled[train_count:train_count + val_count]
    test_samples = shuffled[train_count + val_count:]

    assert len(train_samples) + len(val_samples) + len(test_samples) == total
    assert len(test_samples) == test_count

    return train_samples, val_samples, test_samples


def print_split_summary(
    train_samples: list[Sample],
    val_samples: list[Sample],
    test_samples: list[Sample],
) -> None:
    print("\n=== Split Summary ===")
    print(f"Train: {len(train_samples)}")
    print(f"Val:   {len(val_samples)}")
    print(f"Test:  {len(test_samples)}")


# =========================
# Copy/export
# =========================

def copy_file(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists() and not overwrite:
        return
    shutil.copy2(src, dst)


def write_empty_file(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.touch()


def export_split(
    samples: list[Sample],
    split_name: str,
    config: DatasetConfig,
) -> None:
    dst_images_dir = config.output_root / "images" / split_name
    dst_labels_dir = config.output_root / "labels" / split_name

    missing_label_count = 0

    for sample in samples:
        dst_image = dst_images_dir / sample.image_name
        dst_label = dst_labels_dir / f"{sample.stem}{config.label_extension}"

        copy_file(sample.image_path, dst_image, overwrite=config.overwrite_output)

        if sample.label_path is not None:
            copy_file(sample.label_path, dst_label, overwrite=config.overwrite_output)
        elif config.create_empty_labels_for_missing:
            write_empty_file(dst_label, overwrite=config.overwrite_output)
            missing_label_count += 1

    if missing_label_count:
        print(
            f"[INFO] {split_name}: created {missing_label_count} empty label files "
            f"for images without annotation files"
        )


# =========================
# Manifest / YAML
# =========================

def write_data_yaml(config: DatasetConfig) -> None:
    yaml_path = config.output_root / "data.yaml"

    lines = [
        f"path: {config.output_root.as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]

    for idx, class_name in enumerate(config.class_names):
        lines.append(f"  {idx}: {class_name}")

    yaml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(split_name: str, samples: list[Sample], output_root: Path) -> None:
    manifest_path = output_root / "manifests" / f"{split_name}.txt"
    lines = [f"images/{split_name}/{sample.image_name}" for sample in samples]
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# =========================
# Orchestration
# =========================

def build_yolo_dataset(config: DatasetConfig) -> None:
    validate_config(config)
    ensure_output_dirs(config.output_root)

    samples = build_samples(config)
    summarize_samples(samples)

    train_samples, val_samples, test_samples = split_samples(
        samples=samples,
        train_ratio=config.train_ratio,
        val_ratio=config.val_ratio,
        test_ratio=config.test_ratio,
        seed=config.seed,
    )
    print_split_summary(train_samples, val_samples, test_samples)

    export_split(train_samples, "train", config)
    export_split(val_samples, "val", config)
    export_split(test_samples, "test", config)

    write_data_yaml(config)

    if config.write_split_manifests:
        write_manifest("train", train_samples, config.output_root)
        write_manifest("val", val_samples, config.output_root)
        write_manifest("test", test_samples, config.output_root)

    print("\nDone")


def main() -> None:
    build_yolo_dataset(CONFIG)


if __name__ == "__main__":
    main()