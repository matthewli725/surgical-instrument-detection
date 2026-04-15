from __future__ import annotations

import argparse
import random
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import kagglehub


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = "dilavado/labeled-surgical-tools"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "lavado"
DEFAULT_CLASS_NAMES = (
    "Scalpel n4",
    "Straight Dissection Clamp",
    "Straight Mayo Scissor",
    "Curved Mayo Scissor",
)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
SPLITS = ("train", "val", "test")


@dataclass(frozen=True)
class Sample:
    image_path: Path
    label_path: Path | None

    @property
    def stem(self) -> str:
        return self.image_path.stem


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the Lavado surgical tools dataset from Kaggle and export it "
            "as a YOLO dataset under data/lavado."
        )
    )
    parser.add_argument("--dataset", default=DEFAULT_DATASET, help="Kaggle dataset slug.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="YOLO dataset output directory. Defaults to <project-root>/data/lavado.",
    )
    parser.add_argument("--train-ratio", type=float, default=0.7, help="Fraction of images assigned to train.")
    parser.add_argument("--val-ratio", type=float, default=0.2, help="Fraction of images assigned to val.")
    parser.add_argument("--test-ratio", type=float, default=0.1, help="Fraction of images assigned to test.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic image splitting.")
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Fail if the output directory already exists instead of rebuilding it.",
    )
    parser.add_argument(
        "--require-labels",
        action="store_true",
        help="Fail when an image has no matching label file instead of writing an empty YOLO label.",
    )
    return parser.parse_args(argv)


def validate_ratios(train_ratio: float, val_ratio: float, test_ratio: float) -> None:
    total = train_ratio + val_ratio + test_ratio
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Split ratios must sum to 1.0, got {total:.6f}")
    if any(ratio < 0 for ratio in (train_ratio, val_ratio, test_ratio)):
        raise ValueError("Split ratios must be non-negative.")


def resolve_project_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def download_dataset(dataset: str) -> Path:
    dataset_path = Path(kagglehub.dataset_download(dataset))
    if not dataset_path.exists():
        raise FileNotFoundError(f"Kaggle download did not produce a directory: {dataset_path}")
    return dataset_path


def find_first_existing(root: Path, candidates: Iterable[Path]) -> Path:
    for candidate in candidates:
        candidate_path = root / candidate
        if candidate_path.exists():
            return candidate_path
    searched = ", ".join(str(root / candidate) for candidate in candidates)
    raise FileNotFoundError(f"Could not locate expected dataset directory. Searched: {searched}")


def locate_lavado_dirs(dataset_path: Path) -> tuple[Path, Path]:
    images_dir = find_first_existing(
        dataset_path,
        (
            Path("Surgical-Dataset/Images/All/images"),
            Path("Images/All/images"),
            Path("images"),
        ),
    )
    labels_dir = find_first_existing(
        dataset_path,
        (
            Path("Surgical-Dataset/Labels/label object names"),
            Path("Labels/label object names"),
            Path("labels"),
        ),
    )
    return images_dir, labels_dir


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def discover_samples(images_dir: Path, labels_dir: Path, require_labels: bool) -> list[Sample]:
    image_paths = sorted((path for path in images_dir.iterdir() if is_image(path)), key=lambda path: path.name)
    if not image_paths:
        raise ValueError(f"No images found in {images_dir}")

    samples: list[Sample] = []
    missing_labels: list[Path] = []

    for image_path in image_paths:
        label_path = labels_dir / f"{image_path.stem}.txt"
        if label_path.exists():
            samples.append(Sample(image_path=image_path, label_path=label_path))
            continue

        if require_labels:
            missing_labels.append(label_path)
        else:
            samples.append(Sample(image_path=image_path, label_path=None))

    if missing_labels:
        preview = "\n".join(f"  - {path}" for path in missing_labels[:10])
        suffix = "" if len(missing_labels) <= 10 else f"\n  ... and {len(missing_labels) - 10} more"
        raise FileNotFoundError(f"Missing labels for {len(missing_labels)} image(s):\n{preview}{suffix}")

    return samples


def split_samples(
    samples: list[Sample],
    train_ratio: float,
    val_ratio: float,
    seed: int,
) -> dict[str, list[Sample]]:
    shuffled = samples[:]
    random.Random(seed).shuffle(shuffled)

    train_count = int(len(shuffled) * train_ratio)
    val_count = int(len(shuffled) * val_ratio)

    return {
        "train": shuffled[:train_count],
        "val": shuffled[train_count:train_count + val_count],
        "test": shuffled[train_count + val_count:],
    }


def prepare_output(output_dir: Path, overwrite: bool) -> None:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists: {output_dir}")
        shutil.rmtree(output_dir)

    for split in SPLITS:
        (output_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (output_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
    (output_dir / "manifests").mkdir(parents=True, exist_ok=True)


def export_split(split: str, samples: list[Sample], output_dir: Path) -> tuple[int, int]:
    empty_label_count = 0
    manifest_lines: list[str] = []

    for sample in samples:
        image_dst = output_dir / "images" / split / sample.image_path.name
        label_dst = output_dir / "labels" / split / f"{sample.stem}.txt"

        shutil.copy2(sample.image_path, image_dst)
        if sample.label_path is None:
            label_dst.touch()
            empty_label_count += 1
        else:
            shutil.copy2(sample.label_path, label_dst)

        manifest_lines.append(f"images/{split}/{image_dst.name}")

    manifest_path = output_dir / "manifests" / f"{split}.txt"
    manifest_path.write_text("\n".join(manifest_lines) + ("\n" if manifest_lines else ""), encoding="utf-8")
    return len(samples), empty_label_count


def write_data_yaml(output_dir: Path, class_names: Sequence[str]) -> None:
    lines = [
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]

    for idx, class_name in enumerate(class_names):
        lines.append(f"  {idx}: {class_name}")

    (output_dir / "data.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(output_dir: Path, dataset: str, source_path: Path, seed: int) -> None:
    readme = "\n".join(
        [
            "# Lavado YOLO Dataset",
            "",
            f"Source Kaggle dataset: `{dataset}`",
            f"Local Kaggle cache used for this export: `{source_path}`",
            f"Split seed: `{seed}`",
            "",
            "Generated by:",
            "",
            "```sh",
            "uv run python scripts/download_dataset.py",
            "```",
            "",
        ]
    )
    (output_dir / "README.md").write_text(readme, encoding="utf-8")


def print_summary(splits: dict[str, list[Sample]], empty_labels_by_split: dict[str, int], output_dir: Path) -> None:
    print("=== Lavado YOLO Dataset ===")
    for split in SPLITS:
        total = len(splits[split])
        empty = empty_labels_by_split[split]
        print(f"{split}: {total} image(s), {empty} empty label file(s)")
    print(f"\nWrote YOLO dataset to: {output_dir}")
    print(f"Use data file: {output_dir / 'data.yaml'}")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    validate_ratios(args.train_ratio, args.val_ratio, args.test_ratio)

    output_dir = resolve_project_path(args.output_dir)
    source_path = download_dataset(args.dataset)
    images_dir, labels_dir = locate_lavado_dirs(source_path)

    samples = discover_samples(
        images_dir=images_dir,
        labels_dir=labels_dir,
        require_labels=args.require_labels,
    )
    splits = split_samples(
        samples=samples,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )

    prepare_output(output_dir, overwrite=not args.no_overwrite)

    empty_labels_by_split: dict[str, int] = {}
    for split in SPLITS:
        _, empty_labels = export_split(split, splits[split], output_dir)
        empty_labels_by_split[split] = empty_labels

    write_data_yaml(output_dir, DEFAULT_CLASS_NAMES)
    write_readme(output_dir, args.dataset, source_path, args.seed)
    print_summary(splits, empty_labels_by_split, output_dir)


if __name__ == "__main__":
    main()
