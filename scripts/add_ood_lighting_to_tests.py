from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path
from typing import Sequence


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
DEFAULT_SESSION_DIR = Path("data/collected/sessions/setup_20260416_095507")
DEFAULT_DATASETS_DIR = Path("data/spoon_lighting_yolo")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one out-of-distribution lighting session to the test split of every staged YOLO dataset.",
    )
    parser.add_argument(
        "--session-dir",
        type=Path,
        default=DEFAULT_SESSION_DIR,
        help="Collected session directory to append as OOD test data.",
    )
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=DEFAULT_DATASETS_DIR,
        help="Root containing staged YOLO datasets.",
    )
    return parser.parse_args(argv)


def find_split_datasets(datasets_dir: Path) -> list[Path]:
    if not datasets_dir.exists():
        raise FileNotFoundError(f"Staged YOLO dataset root not found: {datasets_dir}")

    dataset_dirs = [
        path
        for path in sorted(datasets_dir.iterdir())
        if path.is_dir() and (path / "data.yaml").exists()
    ]
    if not dataset_dirs:
        raise ValueError(f"No staged YOLO datasets found under: {datasets_dir}")

    return dataset_dirs


def session_image_dir(session_dir: Path) -> Path:
    images_dir = session_dir / "images"
    return images_dir if images_dir.exists() else session_dir


def session_label_dir(session_dir: Path) -> Path:
    labels_dir = session_dir / "labels"
    return labels_dir if labels_dir.exists() else session_dir


def discover_session_images(session_dir: Path) -> list[Path]:
    if not session_dir.exists():
        raise FileNotFoundError(f"OOD session not found: {session_dir}")

    images_dir = session_image_dir(session_dir)
    images = [
        path
        for path in sorted(images_dir.iterdir())
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    if not images:
        raise ValueError(f"No images found for OOD session: {images_dir}")

    labels_dir = session_label_dir(session_dir)
    missing_labels = [
        labels_dir / f"{image_path.stem}.txt"
        for image_path in images
        if not (labels_dir / f"{image_path.stem}.txt").exists()
    ]
    if missing_labels:
        missing = "\n".join(f"  {path}" for path in missing_labels)
        raise FileNotFoundError(f"Missing OOD label file(s):\n{missing}")

    return images


def read_manifest(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_manifest(path: Path, lines: list[str]) -> None:
    unique_lines = sorted(dict.fromkeys(lines))
    path.write_text("\n".join(unique_lines) + ("\n" if unique_lines else ""), encoding="utf-8")


def read_samples(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return default_sample_fieldnames(), []

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or default_sample_fieldnames()), list(reader)


def default_sample_fieldnames() -> list[str]:
    return [
        "stage",
        "split",
        "session_id",
        "condition_id",
        "condition_key",
        "condition_name",
        "image",
        "label",
    ]


def write_samples(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def ensure_ood_condition(path: Path) -> None:
    fieldnames = ["condition_id", "condition_key", "condition_name", "role"]
    rows: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

    rows = [row for row in rows if row.get("condition_key") != "out_of_distribution"]
    rows.append(
        {
            "condition_id": "ood",
            "condition_key": "out_of_distribution",
            "condition_name": "out-of-distribution lighting",
            "role": "test",
        }
    )

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_session_to_dataset(dataset_dir: Path, session_dir: Path, image_paths: list[Path]) -> int:
    session_id = session_dir.name
    labels_dir = session_label_dir(session_dir)
    stage_name = dataset_dir.name

    image_out_dir = dataset_dir / "images" / "test"
    label_out_dir = dataset_dir / "labels" / "test"
    image_out_dir.mkdir(parents=True, exist_ok=True)
    label_out_dir.mkdir(parents=True, exist_ok=True)

    new_manifest_lines: list[str] = []
    new_sample_rows: list[dict[str, str]] = []

    for image_path in image_paths:
        output_stem = f"{session_id}_ood_{image_path.stem}"
        image_dst = image_out_dir / f"{output_stem}{image_path.suffix.lower()}"
        label_dst = label_out_dir / f"{output_stem}.txt"

        shutil.copy2(image_path, image_dst)
        shutil.copy2(labels_dir / f"{image_path.stem}.txt", label_dst)

        image_rel = f"images/test/{image_dst.name}"
        label_rel = f"labels/test/{label_dst.name}"
        new_manifest_lines.append(image_rel)
        new_sample_rows.append(
            {
                "stage": stage_name,
                "split": "test",
                "session_id": session_id,
                "condition_id": "ood",
                "condition_key": "out_of_distribution",
                "condition_name": "out-of-distribution lighting",
                "image": image_rel,
                "label": label_rel,
            }
        )

    test_manifest_path = dataset_dir / "manifests" / "test.txt"
    current_manifest_lines = [
        line
        for line in read_manifest(test_manifest_path)
        if not line.startswith(f"images/test/{session_id}_ood_")
    ]
    write_manifest(test_manifest_path, [*current_manifest_lines, *new_manifest_lines])

    samples_path = dataset_dir / "manifests" / "samples.csv"
    fieldnames, current_rows = read_samples(samples_path)
    current_rows = [
        row
        for row in current_rows
        if not (
            row.get("session_id") == session_id
            and row.get("split") == "test"
            and row.get("condition_key") == "out_of_distribution"
        )
    ]
    write_samples(samples_path, fieldnames, [*current_rows, *new_sample_rows])
    ensure_ood_condition(dataset_dir / "manifests" / "conditions.csv")

    return len(new_manifest_lines)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    image_paths = discover_session_images(args.session_dir)
    dataset_dirs = find_split_datasets(args.datasets_dir)

    print("=== Append OOD Lighting Test Set ===")
    print(f"OOD session: {args.session_dir}")
    print(f"OOD images: {len(image_paths)}")
    print(f"Datasets: {len(dataset_dirs)}")
    print()

    for dataset_dir in dataset_dirs:
        count = append_session_to_dataset(dataset_dir, args.session_dir, image_paths)
        print(f"{dataset_dir.name}: added {count} OOD test image(s)")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from None
