from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


VALID_SPLITS = {"train", "val", "test"}
VALID_OPEN_SET_ROLES = {"known", "unknown_similar_distractor"}


@dataclass(frozen=True)
class SourceSample:
    sample_id: str
    image_path: Path
    label_path: Path | None
    source_type: str
    open_set_role: str
    class_name: str
    pair_family: str
    scene_id: str
    condition_id: str
    mesh_id: str
    mesh_split: str
    physical_instance_id: str
    session_id: str
    split_assignments: dict[str, str]
    raw_row: dict[str, str]


@dataclass(frozen=True)
class PairFamily:
    name: str
    members: tuple[str, ...]
    distractor_role: str | None
    description: str


@dataclass(frozen=True)
class StageDefinition:
    name: str
    description: str
    split_column: str
    allowed_source_types: tuple[str, ...]
    include_open_set_roles: tuple[str, ...]
    rationale: str
    what_it_proves: str
    mesh_policy: str
    instance_policy: str
    condition_policy: str
    stage_group: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard export-shape-similarity-yolo",
        description=(
            "Export staged YOLO datasets for the shape-similarity synthetic-to-real experiment "
            "from a manifest-driven source dataset."
        ),
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/shape_similarity_source"),
        help="Source dataset root containing samples.csv plus image/label assets.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/shape_similarity/default_experiment.json"),
        help="Experiment config JSON defining known classes, pair families, and stage rules.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/shape_similarity_yolo"),
        help="Directory that will contain one YOLO dataset per exported stage.",
    )
    parser.add_argument(
        "--stage",
        action="append",
        help="Optional stage name to export. Pass more than once to limit the export.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing stage directories in the output root.",
    )
    return parser.parse_args(argv)


def load_experiment_config(config_path: Path) -> tuple[list[str], list[PairFamily], list[StageDefinition]]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    known_classes = payload.get("known_classes")
    if not isinstance(known_classes, list) or not all(isinstance(name, str) and name for name in known_classes):
        raise ValueError(f"{config_path} must define a non-empty 'known_classes' string list.")

    pair_families: list[PairFamily] = []
    for raw_pair in payload.get("pair_families", []):
        if not isinstance(raw_pair, dict):
            raise ValueError(f"Invalid pair family entry in {config_path}: {raw_pair!r}")
        members = raw_pair.get("members", [])
        if not isinstance(members, list) or not all(isinstance(name, str) and name for name in members):
            raise ValueError(f"Pair family members must be a non-empty string list: {raw_pair!r}")
        pair_families.append(
            PairFamily(
                name=str(raw_pair["name"]),
                members=tuple(members),
                distractor_role=str(raw_pair["distractor_role"]) if raw_pair.get("distractor_role") else None,
                description=str(raw_pair.get("description", "")),
            )
        )

    stages: list[StageDefinition] = []
    for raw_stage in payload.get("stages", []):
        if not isinstance(raw_stage, dict):
            raise ValueError(f"Invalid stage entry in {config_path}: {raw_stage!r}")
        stages.append(
            StageDefinition(
                name=str(raw_stage["name"]),
                description=str(raw_stage["description"]),
                split_column=str(raw_stage["split_column"]),
                allowed_source_types=tuple(str(value) for value in raw_stage["allowed_source_types"]),
                include_open_set_roles=tuple(str(value) for value in raw_stage["include_open_set_roles"]),
                rationale=str(raw_stage["rationale"]),
                what_it_proves=str(raw_stage["what_it_proves"]),
                mesh_policy=str(raw_stage["mesh_policy"]),
                instance_policy=str(raw_stage["instance_policy"]),
                condition_policy=str(raw_stage["condition_policy"]),
                stage_group=str(raw_stage.get("stage_group", raw_stage["name"])),
            )
        )

    if not stages:
        raise ValueError(f"{config_path} must define at least one stage.")
    return known_classes, pair_families, stages


def resolve_stage_selection(stages: list[StageDefinition], requested_names: Sequence[str] | None) -> list[StageDefinition]:
    if not requested_names:
        return stages
    stages_by_name = {stage.name: stage for stage in stages}
    missing = [name for name in requested_names if name not in stages_by_name]
    if missing:
        raise KeyError(f"Unknown stage(s): {', '.join(missing)}")
    return [stages_by_name[name] for name in requested_names]


def resolve_path(base_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else (base_dir / path)


def load_source_samples(input_dir: Path, stages: list[StageDefinition], known_classes: list[str]) -> list[SourceSample]:
    samples_csv = input_dir / "samples.csv"
    if not samples_csv.exists():
        raise FileNotFoundError(f"Missing source manifest: {samples_csv}")

    required_columns = {
        "sample_id",
        "image",
        "source_type",
        "open_set_role",
        "class_name",
        "pair_family",
        "scene_id",
        "condition_id",
        "mesh_id",
        "mesh_split",
        "physical_instance_id",
        "session_id",
    }
    required_columns.update(stage.split_column for stage in stages)

    samples: list[SourceSample] = []
    with samples_csv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{samples_csv} is missing a header row.")
        missing = sorted(column for column in required_columns if column not in reader.fieldnames)
        if missing:
            raise ValueError(f"{samples_csv} is missing required column(s): {', '.join(missing)}")

        for row in reader:
            image_path = resolve_path(input_dir, row["image"])
            if not image_path.exists():
                raise FileNotFoundError(f"Image referenced in {samples_csv} does not exist: {image_path}")

            raw_label = (row.get("label") or "").strip()
            label_path = resolve_path(input_dir, raw_label) if raw_label else None
            if label_path is not None and not label_path.exists():
                raise FileNotFoundError(f"Label referenced in {samples_csv} does not exist: {label_path}")

            open_set_role = row["open_set_role"].strip()
            if open_set_role not in VALID_OPEN_SET_ROLES:
                raise ValueError(
                    f"Unsupported open_set_role '{open_set_role}' for sample {row['sample_id']}. "
                    f"Expected one of {sorted(VALID_OPEN_SET_ROLES)}."
                )

            class_name = row["class_name"].strip()
            if open_set_role == "known" and class_name not in known_classes:
                raise ValueError(
                    f"Known sample {row['sample_id']} uses class '{class_name}', which is not in known_classes."
                )
            if open_set_role != "known" and class_name and class_name not in known_classes:
                raise ValueError(
                    f"Open-set sample {row['sample_id']} should leave class_name blank or use a known class placeholder."
                )
            if open_set_role != "known" and label_path is None:
                pass

            split_assignments = {stage.split_column: row[stage.split_column].strip() for stage in stages}
            for split_column, split_name in split_assignments.items():
                if split_name and split_name not in VALID_SPLITS:
                    raise ValueError(
                        f"Sample {row['sample_id']} has invalid split '{split_name}' in column '{split_column}'."
                    )

            samples.append(
                SourceSample(
                    sample_id=row["sample_id"].strip(),
                    image_path=image_path,
                    label_path=label_path,
                    source_type=row["source_type"].strip(),
                    open_set_role=open_set_role,
                    class_name=class_name,
                    pair_family=row["pair_family"].strip(),
                    scene_id=row["scene_id"].strip(),
                    condition_id=row["condition_id"].strip(),
                    mesh_id=row["mesh_id"].strip(),
                    mesh_split=row["mesh_split"].strip(),
                    physical_instance_id=row["physical_instance_id"].strip(),
                    session_id=row["session_id"].strip(),
                    split_assignments=split_assignments,
                    raw_row=row,
                )
            )

    if not samples:
        raise ValueError(f"No samples found in {samples_csv}")
    return samples


def prepare_stage_output(stage_dir: Path, overwrite: bool) -> None:
    if stage_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists. Pass --overwrite to replace it: {stage_dir}")
        shutil.rmtree(stage_dir)

    for split in VALID_SPLITS:
        (stage_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (stage_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
    (stage_dir / "manifests").mkdir(parents=True, exist_ok=True)


def write_data_yaml(stage_dir: Path, known_classes: list[str]) -> None:
    lines = [
        f"path: {stage_dir.as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]
    for index, class_name in enumerate(known_classes):
        lines.append(f"  {index}: {class_name}")
    (stage_dir / "data.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_stage_manifest(stage_dir: Path, stage: StageDefinition) -> None:
    rows = [
        {"field": "name", "value": stage.name},
        {"field": "stage_group", "value": stage.stage_group},
        {"field": "description", "value": stage.description},
        {"field": "split_column", "value": stage.split_column},
        {"field": "allowed_source_types", "value": ",".join(stage.allowed_source_types)},
        {"field": "include_open_set_roles", "value": ",".join(stage.include_open_set_roles)},
        {"field": "rationale", "value": stage.rationale},
        {"field": "what_it_proves", "value": stage.what_it_proves},
        {"field": "mesh_policy", "value": stage.mesh_policy},
        {"field": "instance_policy", "value": stage.instance_policy},
        {"field": "condition_policy", "value": stage.condition_policy},
    ]
    write_csv(stage_dir / "manifests" / "stage.csv", rows, fieldnames=("field", "value"))


def write_pair_manifest(stage_dir: Path, pair_families: list[PairFamily]) -> None:
    rows = [
        {
            "pair_family": pair.name,
            "members": ",".join(pair.members),
            "distractor_role": pair.distractor_role or "",
            "description": pair.description,
        }
        for pair in pair_families
    ]
    write_csv(
        stage_dir / "manifests" / "pairs.csv",
        rows,
        fieldnames=("pair_family", "members", "distractor_role", "description"),
    )


def should_include_sample(sample: SourceSample, stage: StageDefinition) -> bool:
    split_name = sample.split_assignments.get(stage.split_column, "")
    return (
        sample.source_type in stage.allowed_source_types
        and sample.open_set_role in stage.include_open_set_roles
        and split_name in VALID_SPLITS
    )


def copy_sample(sample: SourceSample, stage_dir: Path, split_name: str) -> tuple[str, str]:
    stem = f"{sample.sample_id}_{sample.image_path.stem}"
    image_dst = stage_dir / "images" / split_name / f"{stem}{sample.image_path.suffix.lower()}"
    label_dst = stage_dir / "labels" / split_name / f"{stem}.txt"
    shutil.copy2(sample.image_path, image_dst)
    if sample.label_path is None:
        label_dst.write_text("", encoding="utf-8")
    else:
        shutil.copy2(sample.label_path, label_dst)
    return (
        f"images/{split_name}/{image_dst.name}",
        f"labels/{split_name}/{label_dst.name}",
    )


def export_stage(
    stage: StageDefinition,
    samples: list[SourceSample],
    output_dir: Path,
    known_classes: list[str],
    pair_families: list[PairFamily],
    *,
    overwrite: bool,
) -> dict[str, int]:
    stage_dir = output_dir / stage.name
    prepare_stage_output(stage_dir, overwrite=overwrite)

    manifest_rows: list[dict[str, str]] = []
    split_lists: dict[str, list[str]] = {split: [] for split in VALID_SPLITS}

    for sample in samples:
        if not should_include_sample(sample, stage):
            continue
        split_name = sample.split_assignments[stage.split_column]
        relative_image, relative_label = copy_sample(sample, stage_dir, split_name)
        split_lists[split_name].append(relative_image)
        manifest_rows.append(
            {
                "stage": stage.name,
                "stage_group": stage.stage_group,
                "split": split_name,
                "sample_id": sample.sample_id,
                "source_type": sample.source_type,
                "open_set_role": sample.open_set_role,
                "class_name": sample.class_name,
                "pair_family": sample.pair_family,
                "scene_id": sample.scene_id,
                "condition_id": sample.condition_id,
                "mesh_id": sample.mesh_id,
                "mesh_split": sample.mesh_split,
                "physical_instance_id": sample.physical_instance_id,
                "session_id": sample.session_id,
                "image": relative_image,
                "label": relative_label,
            }
        )

    for split_name, image_paths in split_lists.items():
        manifest_path = stage_dir / "manifests" / f"{split_name}.txt"
        manifest_path.write_text("\n".join(image_paths) + ("\n" if image_paths else ""), encoding="utf-8")

    write_data_yaml(stage_dir, known_classes)
    write_stage_manifest(stage_dir, stage)
    write_pair_manifest(stage_dir, pair_families)
    write_csv(
        stage_dir / "manifests" / "samples.csv",
        manifest_rows,
        fieldnames=(
            "stage",
            "stage_group",
            "split",
            "sample_id",
            "source_type",
            "open_set_role",
            "class_name",
            "pair_family",
            "scene_id",
            "condition_id",
            "mesh_id",
            "mesh_split",
            "physical_instance_id",
            "session_id",
            "image",
            "label",
        ),
    )
    return {split_name: len(paths) for split_name, paths in split_lists.items()}


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    known_classes, pair_families, all_stages = load_experiment_config(args.config)
    stages = resolve_stage_selection(all_stages, args.stage)
    samples = load_source_samples(args.input_dir, stages, known_classes)

    print("=== Shape Similarity YOLO Export ===")
    print(f"Config: {args.config}")
    print(f"Known classes: {len(known_classes)}")
    print(f"Pair families: {len(pair_families)}")
    print(f"Source samples: {len(samples)}")

    for stage in stages:
        counts = export_stage(
            stage,
            samples,
            args.output_dir,
            known_classes,
            pair_families,
            overwrite=args.overwrite,
        )
        print(
            f"{stage.name}: train={counts['train']} val={counts['val']} test={counts['test']} "
            f"({stage.description})"
        )

    print(f"\nWrote staged shape-similarity datasets to: {args.output_dir}")


if __name__ == "__main__":
    main()
