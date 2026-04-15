from __future__ import annotations

import argparse
import random
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


@dataclass(frozen=True)
class CollectedSample:
    session_id: str
    image_path: Path
    label_path: Path

    @property
    def output_stem(self) -> str:
        return f"{self.session_id}_{self.image_path.stem}"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard export-yolo",
        description="Flatten collected setup sessions into a YOLO train/val/test dataset."
    )
    parser.add_argument("--input-dir", type=Path, default=Path("data/collected"), help="Collected session root.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/collected_yolo"), help="YOLO dataset output root.")
    parser.add_argument("--train-ratio", type=float, default=0.7, help="Fraction of setup sessions assigned to train.")
    parser.add_argument("--val-ratio", type=float, default=0.2, help="Fraction of setup sessions assigned to val.")
    parser.add_argument("--test-ratio", type=float, default=0.1, help="Fraction of setup sessions assigned to test.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for session-level splitting.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing output directory.")
    return parser.parse_args(argv)


def load_class_names(input_dir: Path) -> list[str]:
    classes_path = input_dir / "classes.txt"
    if not classes_path.exists():
        raise FileNotFoundError(f"Classes file not found: {classes_path}")

    class_names = [line.strip() for line in classes_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not class_names:
        raise ValueError(f"Classes file is empty: {classes_path}")

    return class_names


def validate_ratios(train_ratio: float, val_ratio: float, test_ratio: float) -> None:
    total = train_ratio + val_ratio + test_ratio
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Split ratios must sum to 1.0, got {total:.6f}")


def discover_samples(input_dir: Path) -> dict[str, list[CollectedSample]]:
    sessions_dir = input_dir / "sessions"
    if not sessions_dir.exists():
        raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")

    samples_by_session: dict[str, list[CollectedSample]] = {}

    for session_dir in sorted(p for p in sessions_dir.iterdir() if p.is_dir()):
        images_dir = session_dir / "images"
        labels_dir = session_dir / "labels"
        if not images_dir.exists() or not labels_dir.exists():
            continue

        session_samples: list[CollectedSample] = []
        for image_path in sorted(images_dir.iterdir()):
            if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            label_path = labels_dir / f"{image_path.stem}.txt"
            if not label_path.exists():
                raise FileNotFoundError(f"Missing label for {image_path}: expected {label_path}")

            session_samples.append(
                CollectedSample(
                    session_id=session_dir.name,
                    image_path=image_path,
                    label_path=label_path,
                )
            )

        if session_samples:
            samples_by_session[session_dir.name] = session_samples

    if not samples_by_session:
        raise ValueError(f"No collected samples found under {sessions_dir}")

    return samples_by_session


def split_sessions(
    session_ids: list[str],
    train_ratio: float,
    val_ratio: float,
    seed: int,
) -> dict[str, list[str]]:
    shuffled = session_ids[:]
    random.Random(seed).shuffle(shuffled)

    total = len(shuffled)
    if total == 1:
        return {"train": shuffled, "val": [], "test": []}

    train_count = max(1, int(total * train_ratio))
    val_count = int(total * val_ratio)

    if train_count + val_count > total:
        val_count = total - train_count

    return {
        "train": shuffled[:train_count],
        "val": shuffled[train_count:train_count + val_count],
        "test": shuffled[train_count + val_count:],
    }


def prepare_output(output_dir: Path, overwrite: bool) -> None:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists. Pass --overwrite to replace it: {output_dir}")
        shutil.rmtree(output_dir)

    for split in ("train", "val", "test"):
        (output_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (output_dir / "labels" / split).mkdir(parents=True, exist_ok=True)

    (output_dir / "manifests").mkdir(parents=True, exist_ok=True)


def copy_samples(
    split_name: str,
    session_ids: list[str],
    samples_by_session: dict[str, list[CollectedSample]],
    output_dir: Path,
) -> int:
    copied_count = 0
    manifest_lines: list[str] = []

    for session_id in session_ids:
        for sample in samples_by_session[session_id]:
            image_dst = output_dir / "images" / split_name / f"{sample.output_stem}{sample.image_path.suffix.lower()}"
            label_dst = output_dir / "labels" / split_name / f"{sample.output_stem}.txt"

            shutil.copy2(sample.image_path, image_dst)
            shutil.copy2(sample.label_path, label_dst)
            manifest_lines.append(f"images/{split_name}/{image_dst.name}")
            copied_count += 1

    manifest_path = output_dir / "manifests" / f"{split_name}.txt"
    manifest_path.write_text("\n".join(manifest_lines) + ("\n" if manifest_lines else ""), encoding="utf-8")
    return copied_count


def write_data_yaml(output_dir: Path, class_names: list[str]) -> None:
    lines = [
        f"path: {output_dir.as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]

    for idx, class_name in enumerate(class_names):
        lines.append(f"  {idx}: {class_name}")

    (output_dir / "data.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    validate_ratios(args.train_ratio, args.val_ratio, args.test_ratio)

    class_names = load_class_names(args.input_dir)
    samples_by_session = discover_samples(args.input_dir)
    session_splits = split_sessions(
        session_ids=sorted(samples_by_session),
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
    )

    prepare_output(args.output_dir, overwrite=args.overwrite)

    print("=== Export Summary ===")
    print(f"Input sessions: {len(samples_by_session)}")
    print(f"Classes: {len(class_names)}")

    for split_name, session_ids in session_splits.items():
        copied_count = copy_samples(split_name, session_ids, samples_by_session, args.output_dir)
        print(f"{split_name}: {len(session_ids)} session(s), {copied_count} image(s)")

    write_data_yaml(args.output_dir, class_names)
    print(f"\nWrote YOLO dataset to: {args.output_dir}")
    print(f"Use data file: {args.output_dir / 'data.yaml'}")
