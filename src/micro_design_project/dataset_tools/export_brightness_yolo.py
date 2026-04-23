from __future__ import annotations

import argparse
import csv
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from micro_design_project.dataset_tools.export_collected_yolo import (
    IMAGE_EXTENSIONS,
    SessionAnnotation,
    load_class_names,
    load_session_annotation,
    render_annotation_labels,
    resolve_export_class_names,
)


BRIGHTNESS_STEMS: tuple[str, ...] = tuple(f"variant_{index:04d}" for index in range(1, 12))
SEPARATED_LAYOUTS = {"order1", "order2"}


@dataclass(frozen=True)
class SessionInfo:
    session_id: str
    background: str
    layout: str


@dataclass(frozen=True)
class BrightnessSample:
    session: SessionInfo
    brightness_rank: int
    brightness_stem: str
    image_path: Path
    label_path: Path
    annotation: SessionAnnotation | None = None

    @property
    def output_stem(self) -> str:
        return f"{self.session.session_id}_{self.brightness_stem}"


@dataclass(frozen=True)
class ExperimentStage:
    name: str
    description: str
    train_backgrounds: tuple[str, ...]
    train_layouts: tuple[str, ...]
    train_ranks: tuple[int, ...]
    test_backgrounds: tuple[str, ...]
    test_layouts: tuple[str, ...]
    test_ranks: tuple[int, ...]


ALL_RANKS = tuple(range(1, len(BRIGHTNESS_STEMS) + 1))
BRIGHTEST_ONLY_RANKS = (1,)
DARKEST_ONLY_RANKS = (len(BRIGHTNESS_STEMS),)
ALL_BUT_BRIGHTEST_RANKS = tuple(range(2, len(BRIGHTNESS_STEMS) + 1))
ALL_BUT_DARKEST_RANKS = tuple(range(1, len(BRIGHTNESS_STEMS)))
BRIGHT_RANKS = tuple(range(1, 7))
DIM_RANKS = tuple(range(7, len(BRIGHTNESS_STEMS) + 1))

EXPERIMENT_STAGES: tuple[ExperimentStage, ...] = (
    ExperimentStage(
        name="brightest_train_darker_test",
        description="Train on the brightest separated images and test on all darker separated images.",
        train_backgrounds=("matte", "reflective"),
        train_layouts=("order1", "order2"),
        train_ranks=BRIGHTEST_ONLY_RANKS,
        test_backgrounds=("matte", "reflective"),
        test_layouts=("order1", "order2"),
        test_ranks=ALL_BUT_BRIGHTEST_RANKS,
    ),
    ExperimentStage(
        name="darkest_train_brighter_test",
        description="Train on the darkest separated images and test on all brighter separated images.",
        train_backgrounds=("matte", "reflective"),
        train_layouts=("order1", "order2"),
        train_ranks=DARKEST_ONLY_RANKS,
        test_backgrounds=("matte", "reflective"),
        test_layouts=("order1", "order2"),
        test_ranks=ALL_BUT_DARKEST_RANKS,
    ),
    ExperimentStage(
        name="bright_train_dim_test",
        description="Train on brighter separated images and test on dimmer separated images.",
        train_backgrounds=("matte", "reflective"),
        train_layouts=("order1", "order2"),
        train_ranks=BRIGHT_RANKS,
        test_backgrounds=("matte", "reflective"),
        test_layouts=("order1", "order2"),
        test_ranks=DIM_RANKS,
    ),
    ExperimentStage(
        name="dim_train_bright_test",
        description="Train on dimmer separated images and test on brighter separated images.",
        train_backgrounds=("matte", "reflective"),
        train_layouts=("order1", "order2"),
        train_ranks=DIM_RANKS,
        test_backgrounds=("matte", "reflective"),
        test_layouts=("order1", "order2"),
        test_ranks=BRIGHT_RANKS,
    ),
    ExperimentStage(
        name="matte_train_reflective_test",
        description="Train on matte-background separated images and test on reflective-background separated images.",
        train_backgrounds=("matte",),
        train_layouts=("order1", "order2"),
        train_ranks=ALL_RANKS,
        test_backgrounds=("reflective",),
        test_layouts=("order1", "order2"),
        test_ranks=ALL_RANKS,
    ),
    ExperimentStage(
        name="reflective_train_matte_test",
        description="Train on reflective-background separated images and test on matte-background separated images.",
        train_backgrounds=("reflective",),
        train_layouts=("order1", "order2"),
        train_ranks=ALL_RANKS,
        test_backgrounds=("matte",),
        test_layouts=("order1", "order2"),
        test_ranks=ALL_RANKS,
    ),
    ExperimentStage(
        name="separated_train_overlay_test",
        description="Train on separated layouts and test on overlapping layouts across all brightness levels.",
        train_backgrounds=("matte", "reflective"),
        train_layouts=("order1", "order2"),
        train_ranks=ALL_RANKS,
        test_backgrounds=("matte", "reflective"),
        test_layouts=("overlay",),
        test_ranks=ALL_RANKS,
    ),
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard export-brightness-yolo",
        description=(
            "Export staged YOLO datasets for brightness-order experiments from collected session folders. "
            "Brightness is inferred from variant_0001 ... variant_0011 in capture order."
        ),
    )
    parser.add_argument("--input-dir", type=Path, default=Path("data/collected"), help="Collected session root.")
    parser.add_argument(
        "--classes-file",
        type=Path,
        help="Optional classes.txt path. Defaults to <input-dir>/classes.txt, then falls back to a single sibling classes.txt.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/brightness_yolo"),
        help="Directory that will contain one YOLO dataset per brightness experiment stage.",
    )
    parser.add_argument(
        "--stage",
        choices=[stage.name for stage in EXPERIMENT_STAGES],
        action="append",
        help="Stage to export. Can be passed more than once. Defaults to all stages.",
    )
    parser.add_argument(
        "--val-mode",
        choices=("train-copy", "none"),
        default="train-copy",
        help=(
            "How to populate YOLO validation data. 'train-copy' copies training images into val so every "
            "stage is trainable with these small controlled datasets. 'none' leaves val empty."
        ),
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing output directory.")
    return parser.parse_args(argv)


def parse_session_info(session_dir: Path) -> SessionInfo | None:
    parts = session_dir.name.split("-")
    if len(parts) != 3 or parts[1] != "background":
        return None
    background, _background_literal, layout = parts
    return SessionInfo(session_id=session_dir.name, background=background, layout=layout)


def brightness_rank_by_stem() -> dict[str, int]:
    return {stem: rank for rank, stem in enumerate(BRIGHTNESS_STEMS, start=1)}


def resolve_class_names(input_dir: Path, classes_file: Path | None) -> list[str]:
    if classes_file is not None:
        if not classes_file.exists():
            raise FileNotFoundError(f"Classes file not found: {classes_file}")
        return load_class_names(classes_file.parent)

    try:
        return resolve_export_class_names(input_dir)
    except FileNotFoundError:
        pass

    sibling_matches = sorted(input_dir.parent.glob("*/classes.txt"))
    if len(sibling_matches) == 1:
        return load_class_names(sibling_matches[0].parent)
    if sibling_matches:
        options = "\n".join(f"- {path}" for path in sibling_matches)
        raise FileNotFoundError(
            f"Could not infer a classes.txt for {input_dir}. Pass --classes-file explicitly.\nAvailable matches:\n{options}"
        )

    raise FileNotFoundError(
        f"Classes file not found in {input_dir}. Pass --classes-file explicitly."
    )


def discover_brightness_samples(
    input_dir: Path,
) -> tuple[dict[str, list[BrightnessSample]], dict[str, list[str]], list[Path]]:
    sessions_dir = input_dir / "sessions"
    if not sessions_dir.exists():
        raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")

    ranks_by_stem = brightness_rank_by_stem()
    samples_by_session: dict[str, list[BrightnessSample]] = {}
    missing_by_session: dict[str, list[str]] = {}
    ignored_images: list[Path] = []

    for session_dir in sorted(path for path in sessions_dir.iterdir() if path.is_dir()):
        session = parse_session_info(session_dir)
        if session is None:
            continue

        images_dir = session_dir / "images"
        labels_dir = session_dir / "labels"
        if not images_dir.exists() or not labels_dir.exists():
            continue
        annotation = load_session_annotation(session_dir)

        session_samples: list[BrightnessSample] = []
        seen_stems: set[str] = set()
        for image_path in sorted(images_dir.iterdir()):
            if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            rank = ranks_by_stem.get(image_path.stem)
            if rank is None:
                ignored_images.append(image_path)
                continue

            label_path = labels_dir / f"{image_path.stem}.txt"
            if not label_path.exists():
                raise FileNotFoundError(f"Missing label for {image_path}: expected {label_path}")

            seen_stems.add(image_path.stem)
            session_samples.append(
                BrightnessSample(
                    session=session,
                    brightness_rank=rank,
                    brightness_stem=image_path.stem,
                    image_path=image_path,
                    label_path=label_path,
                    annotation=annotation,
                )
            )

        if session_samples:
            samples_by_session[session.session_id] = sorted(session_samples, key=lambda sample: sample.brightness_rank)
            missing = [stem for stem in BRIGHTNESS_STEMS if stem not in seen_stems]
            if missing:
                missing_by_session[session.session_id] = missing

    if not samples_by_session:
        raise ValueError(f"No brightness samples found under {sessions_dir}")

    return samples_by_session, missing_by_session, ignored_images


def prepare_stage_output(stage_dir: Path, overwrite: bool) -> None:
    if stage_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists. Pass --overwrite to replace it: {stage_dir}")
        shutil.rmtree(stage_dir)

    for split in ("train", "val", "test"):
        (stage_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (stage_dir / "labels" / split).mkdir(parents=True, exist_ok=True)

    (stage_dir / "manifests").mkdir(parents=True, exist_ok=True)


def sample_matches(sample: BrightnessSample, *, backgrounds: set[str], layouts: set[str], ranks: set[int]) -> bool:
    return (
        sample.session.background in backgrounds
        and sample.session.layout in layouts
        and sample.brightness_rank in ranks
    )


def copy_sample(sample: BrightnessSample, stage_dir: Path, split: str, class_names: list[str]) -> str:
    image_dst = stage_dir / "images" / split / f"{sample.output_stem}{sample.image_path.suffix.lower()}"
    label_dst = stage_dir / "labels" / split / f"{sample.output_stem}.txt"
    shutil.copy2(sample.image_path, image_dst)
    if sample.annotation is None:
        shutil.copy2(sample.label_path, label_dst)
    else:
        label_dst.write_text(render_annotation_labels(sample.annotation, class_names), encoding="utf-8")
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


def sample_manifest_row(
    stage_name: str,
    split: str,
    relative_image_path: str,
    sample: BrightnessSample,
) -> dict[str, str | int]:
    return {
        "stage": stage_name,
        "split": split,
        "session_id": sample.session.session_id,
        "background": sample.session.background,
        "layout": sample.session.layout,
        "brightness_rank": sample.brightness_rank,
        "brightness_stem": sample.brightness_stem,
        "image": relative_image_path,
        "label": relative_image_path.replace("images/", "labels/").rsplit(".", maxsplit=1)[0] + ".txt",
    }


def write_sample_manifest(path: Path, rows: list[dict[str, str | int]]) -> None:
    fieldnames = [
        "stage",
        "split",
        "session_id",
        "background",
        "layout",
        "brightness_rank",
        "brightness_stem",
        "image",
        "label",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_stage_manifest(path: Path, stage: ExperimentStage) -> None:
    rows = [
        ("name", stage.name),
        ("description", stage.description),
        ("train_backgrounds", ",".join(stage.train_backgrounds)),
        ("train_layouts", ",".join(stage.train_layouts)),
        ("train_ranks", ",".join(str(rank) for rank in stage.train_ranks)),
        ("test_backgrounds", ",".join(stage.test_backgrounds)),
        ("test_layouts", ",".join(stage.test_layouts)),
        ("test_ranks", ",".join(str(rank) for rank in stage.test_ranks)),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("field", "value"))
        writer.writerows(rows)


def export_stage(
    stage: ExperimentStage,
    samples_by_session: dict[str, list[BrightnessSample]],
    output_dir: Path,
    class_names: list[str],
    overwrite: bool,
    val_mode: str,
) -> dict[str, int]:
    stage_dir = output_dir / stage.name
    prepare_stage_output(stage_dir, overwrite=overwrite)

    train_backgrounds = set(stage.train_backgrounds)
    train_layouts = set(stage.train_layouts)
    train_ranks = set(stage.train_ranks)
    test_backgrounds = set(stage.test_backgrounds)
    test_layouts = set(stage.test_layouts)
    test_ranks = set(stage.test_ranks)

    manifest_paths: dict[str, list[str]] = {"train": [], "val": [], "test": []}
    rows: list[dict[str, str | int]] = []

    for session_id in sorted(samples_by_session):
        for sample in samples_by_session[session_id]:
            if sample_matches(sample, backgrounds=train_backgrounds, layouts=train_layouts, ranks=train_ranks):
                relative_path = copy_sample(sample, stage_dir, "train", class_names)
                manifest_paths["train"].append(relative_path)
                rows.append(sample_manifest_row(stage.name, "train", relative_path, sample))

                if val_mode == "train-copy":
                    relative_val_path = copy_sample(sample, stage_dir, "val", class_names)
                    manifest_paths["val"].append(relative_val_path)
                    rows.append(sample_manifest_row(stage.name, "val", relative_val_path, sample))

            elif sample_matches(sample, backgrounds=test_backgrounds, layouts=test_layouts, ranks=test_ranks):
                relative_path = copy_sample(sample, stage_dir, "test", class_names)
                manifest_paths["test"].append(relative_path)
                rows.append(sample_manifest_row(stage.name, "test", relative_path, sample))

    for split, lines in manifest_paths.items():
        manifest_path = stage_dir / "manifests" / f"{split}.txt"
        manifest_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    write_sample_manifest(stage_dir / "manifests" / "samples.csv", rows)
    write_stage_manifest(stage_dir / "manifests" / "stage.csv", stage)
    write_data_yaml(stage_dir, class_names)
    return {split: len(lines) for split, lines in manifest_paths.items()}


def selected_stages(stage_names: list[str] | None) -> list[ExperimentStage]:
    if not stage_names:
        return list(EXPERIMENT_STAGES)
    stages_by_name = {stage.name: stage for stage in EXPERIMENT_STAGES}
    return [stages_by_name[name] for name in stage_names]


def print_missing_summary(missing_by_session: dict[str, list[str]]) -> None:
    if not missing_by_session:
        return
    print("Missing expected brightness images:")
    for session_id, missing_stems in sorted(missing_by_session.items()):
        print(f"  {session_id}: {', '.join(missing_stems)}")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    class_names = resolve_class_names(args.input_dir, args.classes_file)
    samples_by_session, missing_by_session, ignored_images = discover_brightness_samples(args.input_dir)
    stages = selected_stages(args.stage)

    print("=== Brightness YOLO Export ===")
    print(f"Input sessions: {len(samples_by_session)}")
    print(f"Classes: {len(class_names)}")
    print_missing_summary(missing_by_session)
    if ignored_images:
        print(f"Ignored non-brightness image(s): {len(ignored_images)}")

    for stage in stages:
        counts = export_stage(
            stage=stage,
            samples_by_session=samples_by_session,
            output_dir=args.output_dir,
            class_names=class_names,
            overwrite=args.overwrite,
            val_mode=args.val_mode,
        )
        print(
            f"{stage.name}: train={counts['train']} val={counts['val']} test={counts['test']} "
            f"({stage.description})"
        )

    print(f"\nWrote staged YOLO datasets to: {args.output_dir}")
