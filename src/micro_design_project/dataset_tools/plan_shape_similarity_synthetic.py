from __future__ import annotations

import argparse
import csv
import json
import random
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


STAGE_SPLIT_COLUMNS = (
    "stage_seen_split",
    "stage_heldout_split",
    "transfer_pretrain_split",
    "transfer_real_split",
)


@dataclass(frozen=True)
class AssetRecord:
    asset_id: str
    class_name: str
    pair_family: str
    mesh_path: Path
    mesh_split: str
    open_set_role: str
    scale_hint_meters: float


@dataclass(frozen=True)
class StageRenderPlan:
    name: str
    split_column: str
    train_per_asset: int
    val_per_asset: int
    test_per_asset: int
    train_condition_ids: tuple[str, ...]
    test_condition_ids: tuple[str, ...]
    train_mesh_splits: tuple[str, ...]
    test_mesh_splits: tuple[str, ...]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard plan-shape-similarity-synthetic",
        description=(
            "Create a Blender-ready scene plan and source manifest for the shape-similarity synthetic dataset."
        ),
    )
    parser.add_argument(
        "--experiment-config",
        type=Path,
        default=Path("config/shape_similarity/default_experiment.json"),
        help="Shape-similarity experiment config with known classes and stage names.",
    )
    parser.add_argument(
        "--render-config",
        type=Path,
        default=Path("config/shape_similarity/blenderproc_v1.json"),
        help="Synthetic render planning config with counts and randomization ranges.",
    )
    parser.add_argument(
        "--assets-config",
        type=Path,
        default=Path("config/shape_similarity/blender_assets.template.json"),
        help="Asset catalog JSON listing mesh files and class assignments.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/shape_similarity_source"),
        help="Output root for the source manifest, scene plan, images, and labels.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional override for the render planning seed.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the output directory if it already exists.",
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def prepare_output_dir(output_dir: Path, overwrite: bool) -> None:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists. Pass --overwrite to replace it: {output_dir}")
        shutil.rmtree(output_dir)

    (output_dir / "images" / "synthetic").mkdir(parents=True, exist_ok=True)
    (output_dir / "labels" / "synthetic").mkdir(parents=True, exist_ok=True)
    (output_dir / "metadata" / "synthetic").mkdir(parents=True, exist_ok=True)
    (output_dir / "manifests").mkdir(parents=True, exist_ok=True)


def load_known_classes(experiment_config: dict[str, Any]) -> tuple[list[str], dict[str, str]]:
    known_classes = experiment_config.get("known_classes")
    if not isinstance(known_classes, list) or not all(isinstance(name, str) and name for name in known_classes):
        raise ValueError("Experiment config must define a non-empty known_classes list.")

    family_by_class: dict[str, str] = {}
    for raw_pair in experiment_config.get("pair_families", []):
        if not isinstance(raw_pair, dict):
            continue
        family_name = str(raw_pair["name"])
        for class_name in raw_pair.get("members", []):
            if isinstance(class_name, str) and class_name:
                family_by_class[class_name] = family_name
    return known_classes, family_by_class


def load_assets(
    assets_config: dict[str, Any],
    known_classes: list[str],
    family_by_class: dict[str, str],
) -> list[AssetRecord]:
    raw_assets = assets_config.get("assets")
    if not isinstance(raw_assets, list) or not raw_assets:
        raise ValueError("Assets config must define a non-empty assets list.")

    assets: list[AssetRecord] = []
    for raw_asset in raw_assets:
        if not isinstance(raw_asset, dict):
            raise ValueError(f"Invalid asset entry: {raw_asset!r}")
        class_name = str(raw_asset["class_name"])
        if class_name not in known_classes:
            raise ValueError(f"Asset {raw_asset.get('asset_id')} uses unknown class '{class_name}'.")
        mesh_path = Path(str(raw_asset["mesh_path"]))
        if not mesh_path.exists():
            raise FileNotFoundError(f"Mesh path does not exist for asset {raw_asset.get('asset_id')}: {mesh_path}")
        assets.append(
            AssetRecord(
                asset_id=str(raw_asset["asset_id"]),
                class_name=class_name,
                pair_family=str(raw_asset.get("pair_family") or family_by_class.get(class_name, "")),
                mesh_path=mesh_path,
                mesh_split=str(raw_asset.get("mesh_split", "shared")),
                open_set_role=str(raw_asset.get("open_set_role", "known")),
                scale_hint_meters=float(raw_asset.get("scale_hint_meters", 0.16)),
            )
        )

    known_assets = [asset for asset in assets if asset.open_set_role == "known"]
    if not known_assets:
        raise ValueError("Assets config did not provide any known assets.")

    assets_by_class: dict[str, list[AssetRecord]] = {class_name: [] for class_name in known_classes}
    for asset in known_assets:
        assets_by_class[asset.class_name].append(asset)

    missing_classes = [class_name for class_name, class_assets in assets_by_class.items() if not class_assets]
    if missing_classes:
        raise ValueError(f"Assets config is missing known assets for class(es): {', '.join(missing_classes)}")
    return known_assets


def tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"Expected a non-empty list of strings, got {value!r}")
    return tuple(value)


def load_stage_plans(render_config: dict[str, Any]) -> list[StageRenderPlan]:
    raw_stage_generation = render_config.get("stage_generation")
    if not isinstance(raw_stage_generation, dict) or not raw_stage_generation:
        raise ValueError("Render config must define stage_generation.")

    stage_plans: list[StageRenderPlan] = []
    for stage_name, raw_stage in raw_stage_generation.items():
        if not isinstance(raw_stage, dict):
            raise ValueError(f"Invalid stage_generation entry for {stage_name!r}")
        split_column = str(raw_stage["split_column"])
        if split_column not in STAGE_SPLIT_COLUMNS:
            raise ValueError(f"Unsupported split column '{split_column}' for stage '{stage_name}'.")
        train_condition_ids = tuple_of_strings(raw_stage["train_condition_ids"])
        test_condition_ids = tuple_of_strings(raw_stage.get("test_condition_ids") or raw_stage["train_condition_ids"])
        stage_plans.append(
            StageRenderPlan(
                name=stage_name,
                split_column=split_column,
                train_per_asset=int(raw_stage["train_per_asset"]),
                val_per_asset=int(raw_stage["val_per_asset"]),
                test_per_asset=int(raw_stage["test_per_asset"]),
                train_condition_ids=train_condition_ids,
                test_condition_ids=test_condition_ids,
                train_mesh_splits=tuple_of_strings(raw_stage.get("train_mesh_splits", ["shared", "heldout"])),
                test_mesh_splits=tuple_of_strings(raw_stage.get("test_mesh_splits", ["shared", "heldout"])),
            )
        )
    return stage_plans


def choose_assets_by_split(
    assets: list[AssetRecord],
    *,
    class_name: str,
    allowed_mesh_splits: tuple[str, ...],
) -> list[AssetRecord]:
    matching = [
        asset
        for asset in assets
        if asset.class_name == class_name and asset.mesh_split in allowed_mesh_splits and asset.open_set_role == "known"
    ]
    return matching


def random_value(rng: random.Random, min_value: float, max_value: float) -> float:
    return min_value + (max_value - min_value) * rng.random()


def scene_entry(
    *,
    sample_id: str,
    stage_name: str,
    split_name: str,
    split_column: str,
    asset: AssetRecord,
    class_id: int,
    output_dir: Path,
    condition_id: str,
    rng: random.Random,
    render_config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    scene_defaults = render_config["scene_defaults"]
    resolution = render_config["render_resolution"]
    xy_jitter = scene_defaults["xy_jitter_m"]
    rotation_deg_range = scene_defaults["rotation_deg_range"]
    camera_distance_range = scene_defaults["camera_distance_range"]
    light_energy_range = scene_defaults["light_energy_range"]
    roughness_range = scene_defaults["material_roughness_range"]
    tray_color_options = tuple_of_strings(scene_defaults["tray_color_options"])

    image_rel = Path("images") / "synthetic" / f"{sample_id}.png"
    label_rel = Path("labels") / "synthetic" / f"{sample_id}.txt"
    metadata_rel = Path("metadata") / "synthetic" / f"{sample_id}.json"

    render_metadata = {
        "sample_id": sample_id,
        "scene_id": f"{stage_name}_{split_name}_{sample_id}",
        "stage_name": stage_name,
        "split_name": split_name,
        "image_path": str((output_dir / image_rel).resolve()),
        "label_path": str((output_dir / label_rel).resolve()),
        "metadata_path": str((output_dir / metadata_rel).resolve()),
        "mesh_path": str(asset.mesh_path.resolve()),
        "mesh_id": asset.asset_id,
        "mesh_split": asset.mesh_split,
        "class_name": asset.class_name,
        "class_id": class_id,
        "pair_family": asset.pair_family,
        "condition_id": condition_id,
        "resolution": {
            "width": int(resolution["width"]),
            "height": int(resolution["height"]),
        },
        "tray": {
            "size_m": scene_defaults["tray_size_m"],
            "base_color": rng.choice(tray_color_options),
            "roughness": round(random_value(rng, roughness_range[0], roughness_range[1]), 4),
        },
        "camera": {
            "distance_m": round(random_value(rng, camera_distance_range[0], camera_distance_range[1]), 4),
            "look_at_xyz": [0.0, 0.0, 0.0],
        },
        "lighting": {
            "energy": round(random_value(rng, light_energy_range[0], light_energy_range[1]), 2),
            "x_m": round(random_value(rng, -0.35, 0.35), 4),
            "y_m": round(random_value(rng, -0.25, 0.25), 4),
            "z_m": round(random_value(rng, 0.45, 0.85), 4),
        },
        "target_object": {
            "location_xyz": [
                round(random_value(rng, -xy_jitter[0], xy_jitter[0]), 4),
                round(random_value(rng, -xy_jitter[1], xy_jitter[1]), 4),
                0.0,
            ],
            "rotation_euler_deg": [0.0, 0.0, round(random_value(rng, rotation_deg_range[0], rotation_deg_range[1]), 3)],
            "scale_hint_meters": asset.scale_hint_meters,
            "material_metallic": 1.0,
            "material_roughness": round(random_value(rng, roughness_range[0], roughness_range[1]), 4),
        },
    }

    source_row = {
        "sample_id": sample_id,
        "image": image_rel.as_posix(),
        "label": label_rel.as_posix(),
        "source_type": "synthetic",
        "open_set_role": asset.open_set_role,
        "class_name": asset.class_name,
        "pair_family": asset.pair_family,
        "scene_id": render_metadata["scene_id"],
        "condition_id": condition_id,
        "mesh_id": asset.asset_id,
        "mesh_split": asset.mesh_split,
        "physical_instance_id": "not_applicable",
        "session_id": stage_name,
        "stage_seen_split": "",
        "stage_heldout_split": "",
        "transfer_pretrain_split": "",
        "transfer_real_split": "",
    }
    source_row[split_column] = split_name
    return render_metadata, source_row


def build_plan(
    *,
    output_dir: Path,
    known_classes: list[str],
    assets: list[AssetRecord],
    stage_plans: list[StageRenderPlan],
    render_config: dict[str, Any],
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rng = random.Random(seed)
    class_to_id = {class_name: index for index, class_name in enumerate(known_classes)}

    scene_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []

    for stage_plan in stage_plans:
        for class_name in known_classes:
            train_assets = choose_assets_by_split(
                assets,
                class_name=class_name,
                allowed_mesh_splits=stage_plan.train_mesh_splits,
            )
            test_assets = choose_assets_by_split(
                assets,
                class_name=class_name,
                allowed_mesh_splits=stage_plan.test_mesh_splits,
            )
            if not train_assets:
                raise ValueError(
                    f"Stage '{stage_plan.name}' has no train assets for class '{class_name}' "
                    f"under mesh splits {stage_plan.train_mesh_splits}."
                )
            if not test_assets:
                raise ValueError(
                    f"Stage '{stage_plan.name}' has no test assets for class '{class_name}' "
                    f"under mesh splits {stage_plan.test_mesh_splits}."
                )

            split_specs = (
                ("train", stage_plan.train_per_asset, train_assets, stage_plan.train_condition_ids),
                ("val", stage_plan.val_per_asset, train_assets, stage_plan.train_condition_ids),
                ("test", stage_plan.test_per_asset, test_assets, stage_plan.test_condition_ids),
            )
            for split_name, count_per_asset, split_assets, condition_ids in split_specs:
                for asset in split_assets:
                    for sample_index in range(count_per_asset):
                        sample_id = f"{stage_plan.name}_{asset.asset_id}_{split_name}_{sample_index:04d}"
                        condition_id = condition_ids[sample_index % len(condition_ids)]
                        scene_row, source_row = scene_entry(
                            sample_id=sample_id,
                            stage_name=stage_plan.name,
                            split_name=split_name,
                            split_column=stage_plan.split_column,
                            asset=asset,
                            class_id=class_to_id[class_name],
                            output_dir=output_dir,
                            condition_id=condition_id,
                            rng=rng,
                            render_config=render_config,
                        )
                        scene_rows.append(scene_row)
                        source_rows.append(source_row)
    return scene_rows, source_rows


def write_scene_plan(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def write_metadata(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    experiment_config = load_json(args.experiment_config)
    render_config = load_json(args.render_config)
    assets_config = load_json(args.assets_config)
    known_classes, family_by_class = load_known_classes(experiment_config)
    assets = load_assets(assets_config, known_classes, family_by_class)
    stage_plans = load_stage_plans(render_config)

    seed = int(args.seed if args.seed is not None else render_config.get("seed", 42))
    prepare_output_dir(args.output_dir, args.overwrite)

    scene_rows, source_rows = build_plan(
        output_dir=args.output_dir,
        known_classes=known_classes,
        assets=assets,
        stage_plans=stage_plans,
        render_config=render_config,
        seed=seed,
    )

    write_scene_plan(args.output_dir / "manifests" / "scene_plan.jsonl", scene_rows)
    write_csv(
        args.output_dir / "samples.csv",
        source_rows,
        fieldnames=(
            "sample_id",
            "image",
            "label",
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
            "stage_seen_split",
            "stage_heldout_split",
            "transfer_pretrain_split",
            "transfer_real_split",
        ),
    )
    write_csv(
        args.output_dir / "manifests" / "asset_inventory.csv",
        [
            {
                "asset_id": asset.asset_id,
                "class_name": asset.class_name,
                "pair_family": asset.pair_family,
                "mesh_path": str(asset.mesh_path.resolve()),
                "mesh_split": asset.mesh_split,
                "open_set_role": asset.open_set_role,
                "scale_hint_meters": asset.scale_hint_meters,
            }
            for asset in assets
        ],
        fieldnames=(
            "asset_id",
            "class_name",
            "pair_family",
            "mesh_path",
            "mesh_split",
            "open_set_role",
            "scale_hint_meters",
        ),
    )
    write_metadata(
        args.output_dir / "manifests" / "planning_metadata.json",
        {
            "seed": seed,
            "experiment_config": str(args.experiment_config),
            "render_config": str(args.render_config),
            "assets_config": str(args.assets_config),
            "planned_scenes": len(scene_rows),
            "known_classes": known_classes,
            "stage_names": [stage.name for stage in stage_plans],
        },
    )

    print("=== Shape Similarity Synthetic Planner ===")
    print(f"Output directory: {args.output_dir}")
    print(f"Seed: {seed}")
    print(f"Known classes: {len(known_classes)}")
    print(f"Assets: {len(assets)}")
    print(f"Planned renders: {len(scene_rows)}")
    print(f"Scene plan: {args.output_dir / 'manifests' / 'scene_plan.jsonl'}")
    print(f"Source manifest: {args.output_dir / 'samples.csv'}")


if __name__ == "__main__":
    main()
