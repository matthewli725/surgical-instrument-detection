from __future__ import annotations

import argparse
import csv
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from micro_design_project.dataset_tools.export_collected_yolo import IMAGE_EXTENSIONS, load_class_names


@dataclass(frozen=True)
class LightingCondition:
    id: int
    stem: str
    key: str
    name: str


@dataclass(frozen=True)
class LightingStage:
    name: str
    train_condition_ids: tuple[int, ...]

    @property
    def test_condition_ids(self) -> tuple[int, ...]:
        return tuple(
            condition.id
            for condition in LIGHTING_CONDITIONS
            if condition.id not in self.train_condition_ids
        )


@dataclass(frozen=True)
class LightingSample:
    session_id: str
    condition: LightingCondition
    image_path: Path
    label_path: Path

    @property
    def output_stem(self) -> str:
        return f"{self.session_id}_{self.condition.key}"


LIGHTING_CONDITIONS: tuple[LightingCondition, ...] = (
    LightingCondition(0, "reference", "reference_left_light", "reference - left light on"),
    LightingCondition(1, "variant_0001", "right_light", "right light on"),
    LightingCondition(2, "variant_0002", "both_lights", "both lights on"),
    LightingCondition(3, "variant_0003", "phone_camera_above", "phone camera above"),
    LightingCondition(4, "variant_0004", "flashlight_45_right", "flashlight 45 degree right"),
    LightingCondition(5, "variant_0005", "flashlight_90_right", "flashlight 90 degree right"),
    LightingCondition(6, "variant_0006", "flashlight_45_top", "flashlight 45 degree top"),
    LightingCondition(7, "variant_0007", "flashlight_90_top", "flashlight 90 degree top"),
    LightingCondition(8, "variant_0008", "flashlight_45_left", "flashlight 45 degree left"),
    LightingCondition(9, "variant_0009", "flashlight_90_left", "flashlight 90 degree left"),
    LightingCondition(10, "variant_0010", "flashlight_45_bottom", "flashlight 45 degree bottom"),
    LightingCondition(11, "variant_0011", "flashlight_90_bottom", "flashlight 90 degree bottom"),
)

LIGHTING_STAGES: tuple[LightingStage, ...] = (
    LightingStage("reference_only", (0,)),
    LightingStage("reference_plus_45", (0, 4, 6, 8, 10)),
    LightingStage("reference_plus_45_90", (0, 4, 5, 6, 7, 8, 9, 10, 11)),
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard export-lighting-yolo",
        description=(
            "Export collected spoon lighting sessions into staged YOLO datasets. "
            "Each stage trains on selected lighting conditions and tests on the remaining known conditions."
        ),
    )
    parser.add_argument("--input-dir", type=Path, default=Path("data/collected"), help="Collected session root.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/spoon_lighting_yolo"),
        help="Directory that will contain one YOLO dataset per lighting stage.",
    )
    parser.add_argument(
        "--stage",
        choices=[stage.name for stage in LIGHTING_STAGES],
        action="append",
        help="Stage to export. Can be passed more than once. Defaults to all stages.",
    )
    parser.add_argument(
        "--val-mode",
        choices=("train-copy", "none"),
        default="train-copy",
        help=(
            "How to populate YOLO validation data. 'train-copy' copies training images into val so every "
            "stage is trainable with tiny reference-only data. 'none' leaves val empty."
        ),
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing output directory.")
    return parser.parse_args(argv)


def condition_by_id() -> dict[int, LightingCondition]:
    return {condition.id: condition for condition in LIGHTING_CONDITIONS}


def condition_by_stem() -> dict[str, LightingCondition]:
    return {condition.stem: condition for condition in LIGHTING_CONDITIONS}


def discover_lighting_samples(input_dir: Path) -> tuple[dict[str, list[LightingSample]], list[Path]]:
    sessions_dir = input_dir / "sessions"
    if not sessions_dir.exists():
        raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")

    known_by_stem = condition_by_stem()
    samples_by_session: dict[str, list[LightingSample]] = {}
    ignored_images: list[Path] = []

    for session_dir in sorted(path for path in sessions_dir.iterdir() if path.is_dir()):
        images_dir = session_dir / "images"
        labels_dir = session_dir / "labels"
        if not images_dir.exists() or not labels_dir.exists():
            continue

        session_samples: list[LightingSample] = []
        for image_path in sorted(images_dir.iterdir()):
            if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            condition = known_by_stem.get(image_path.stem)
            if condition is None:
                ignored_images.append(image_path)
                continue

            label_path = labels_dir / f"{image_path.stem}.txt"
            if not label_path.exists():
                raise FileNotFoundError(f"Missing label for {image_path}: expected {label_path}")

            session_samples.append(
                LightingSample(
                    session_id=session_dir.name,
                    condition=condition,
                    image_path=image_path,
                    label_path=label_path,
                )
            )

        if session_samples:
            samples_by_session[session_dir.name] = sorted(
                session_samples,
                key=lambda sample: sample.condition.id,
            )

    if not samples_by_session:
        raise ValueError(f"No known lighting samples found under {sessions_dir}")

    return samples_by_session, ignored_images


def prepare_stage_output(stage_dir: Path, overwrite: bool) -> None:
    if stage_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists. Pass --overwrite to replace it: {stage_dir}")
        shutil.rmtree(stage_dir)

    for split in ("train", "val", "test"):
        (stage_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (stage_dir / "labels" / split).mkdir(parents=True, exist_ok=True)

    (stage_dir / "manifests").mkdir(parents=True, exist_ok=True)


def copy_sample(sample: LightingSample, stage_dir: Path, split: str) -> str:
    image_dst = stage_dir / "images" / split / f"{sample.output_stem}{sample.image_path.suffix.lower()}"
    label_dst = stage_dir / "labels" / split / f"{sample.output_stem}.txt"
    shutil.copy2(sample.image_path, image_dst)
    shutil.copy2(sample.label_path, label_dst)
    return f"images/{split}/{image_dst.name}"


def write_data_yaml(stage_dir: Path, class_names: list[str]) -> None:
    lines = [
        f"path: {stage_dir.as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]
    for idx, class_name in enumerate(class_names):
        lines.append(f"  {idx}: {class_name}")

    (stage_dir / "data.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_stage(
    stage: LightingStage,
    samples_by_session: dict[str, list[LightingSample]],
    output_dir: Path,
    class_names: list[str],
    overwrite: bool,
    val_mode: str,
) -> dict[str, int]:
    stage_dir = output_dir / stage.name
    prepare_stage_output(stage_dir, overwrite=overwrite)

    train_ids = set(stage.train_condition_ids)
    test_ids = set(stage.test_condition_ids)
    manifest_paths: dict[str, list[str]] = {"train": [], "val": [], "test": []}
    rows: list[dict[str, str | int]] = []

    for session_id in sorted(samples_by_session):
        for sample in samples_by_session[session_id]:
            if sample.condition.id in train_ids:
                split = "train"
            elif sample.condition.id in test_ids:
                split = "test"
            else:
                continue

            relative_image_path = copy_sample(sample, stage_dir, split)
            manifest_paths[split].append(relative_image_path)
            rows.append(sample_manifest_row(stage.name, split, relative_image_path, sample))

            if split == "train" and val_mode == "train-copy":
                relative_val_path = copy_sample(sample, stage_dir, "val")
                manifest_paths["val"].append(relative_val_path)
                rows.append(sample_manifest_row(stage.name, "val", relative_val_path, sample))

    for split, lines in manifest_paths.items():
        manifest_path = stage_dir / "manifests" / f"{split}.txt"
        manifest_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    write_sample_manifest(stage_dir / "manifests" / "samples.csv", rows)
    write_conditions_manifest(stage_dir / "manifests" / "conditions.csv", stage)
    write_data_yaml(stage_dir, class_names)
    return {split: len(lines) for split, lines in manifest_paths.items()}


def sample_manifest_row(
    stage_name: str,
    split: str,
    relative_image_path: str,
    sample: LightingSample,
) -> dict[str, str | int]:
    return {
        "stage": stage_name,
        "split": split,
        "session_id": sample.session_id,
        "condition_id": sample.condition.id,
        "condition_key": sample.condition.key,
        "condition_name": sample.condition.name,
        "image": relative_image_path,
        "label": relative_image_path.replace("images/", "labels/").rsplit(".", maxsplit=1)[0] + ".txt",
    }


def write_sample_manifest(path: Path, rows: list[dict[str, str | int]]) -> None:
    fieldnames = [
        "stage",
        "split",
        "session_id",
        "condition_id",
        "condition_key",
        "condition_name",
        "image",
        "label",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_conditions_manifest(path: Path, stage: LightingStage) -> None:
    train_ids = set(stage.train_condition_ids)
    test_ids = set(stage.test_condition_ids)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["condition_id", "condition_key", "condition_name", "role"])
        writer.writeheader()
        for condition in LIGHTING_CONDITIONS:
            role = "train" if condition.id in train_ids else "test" if condition.id in test_ids else "unused"
            writer.writerow(
                {
                    "condition_id": condition.id,
                    "condition_key": condition.key,
                    "condition_name": condition.name,
                    "role": role,
                }
            )


def selected_stages(stage_names: list[str] | None) -> list[LightingStage]:
    if not stage_names:
        return list(LIGHTING_STAGES)

    stages_by_name = {stage.name: stage for stage in LIGHTING_STAGES}
    return [stages_by_name[name] for name in stage_names]


def print_condition_plan(stage: LightingStage) -> None:
    by_id = condition_by_id()
    train_names = ", ".join(by_id[condition_id].key for condition_id in stage.train_condition_ids)
    test_names = ", ".join(by_id[condition_id].key for condition_id in stage.test_condition_ids)
    print(f"{stage.name}:")
    print(f"  train: {train_names}")
    print(f"  test:  {test_names}")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    class_names = load_class_names(args.input_dir)
    samples_by_session, ignored_images = discover_lighting_samples(args.input_dir)
    stages = selected_stages(args.stage)

    print("=== Lighting YOLO Export ===")
    print(f"Input sessions: {len(samples_by_session)}")
    print(f"Classes: {len(class_names)}")
    if args.val_mode == "train-copy":
        print("Validation split: copy of training split; use test metrics for lighting generalization.")
    if ignored_images:
        print(f"Ignored unknown lighting image(s): {len(ignored_images)}")
        for image_path in ignored_images[:10]:
            print(f"  {image_path}")
        if len(ignored_images) > 10:
            print(f"  ... and {len(ignored_images) - 10} more")
    print()

    for stage in stages:
        print_condition_plan(stage)
        counts = export_stage(
            stage=stage,
            samples_by_session=samples_by_session,
            output_dir=args.output_dir,
            class_names=class_names,
            overwrite=args.overwrite,
            val_mode=args.val_mode,
        )
        print(f"  wrote: train={counts['train']}, val={counts['val']}, test={counts['test']}")
        print(f"  data:  {args.output_dir / stage.name / 'data.yaml'}")
        print()

