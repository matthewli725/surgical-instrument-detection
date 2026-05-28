from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import hydra
import yaml
from hydra.utils import get_original_cwd
from omegaconf import DictConfig, OmegaConf
from PIL import Image
from tqdm import tqdm


IMG_EXTS = {".jpg", ".jpeg", ".png"}


def resolve_path(root: Path, path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else root / path


def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def normalize_name(name: str) -> str:
    return (
        str(name)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
        .replace("/", "_")
    )


def clean_folder_name(name: str) -> str:
    return (
        str(name)
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("(", "")
        .replace(")", "")
    )


def parse_names(names) -> dict[int, str]:
    """
    Handles either:
      names:
        0: Scalpel n4
        1: Straight Mayo Scissor

    or:
      names:
        - Scalpel n4
        - Straight Mayo Scissor
    """
    if isinstance(names, list):
        return {i: str(name) for i, name in enumerate(names)}

    if isinstance(names, dict):
        return {int(k): str(v) for k, v in names.items()}

    raise ValueError("data.yaml names must be either a list or dict")


def get_dataset_root(data_yaml_path: Path) -> Path:
    data = load_yaml(data_yaml_path)

    if "path" not in data:
        return data_yaml_path.parent

    dataset_root = Path(data["path"])

    if dataset_root.is_absolute():
        return dataset_root

    return data_yaml_path.parent / dataset_root


def resolve_split_path(data_yaml_path: Path, split_name: str) -> Path | None:
    data = load_yaml(data_yaml_path)

    if split_name not in data or data[split_name] is None:
        return None

    dataset_root = get_dataset_root(data_yaml_path)
    split_value = Path(str(data[split_name]))

    if split_value.is_absolute():
        return split_value

    candidates = [
        dataset_root / split_value,
        data_yaml_path.parent / split_value,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        f"Could not resolve split path for '{split_name}'. Tried: {candidates}"
    )


def resolve_image_from_split_line(
    line: str,
    data_yaml_path: Path,
    split_file_path: Path,
) -> Path:
    dataset_root = get_dataset_root(data_yaml_path)
    line_path = Path(line.strip())

    if line_path.is_absolute():
        return line_path

    candidates = [
        dataset_root / line_path,
        data_yaml_path.parent / line_path,
        split_file_path.parent / line_path,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def get_image_paths_for_split(data_yaml_path: Path, split_name: str) -> list[Path]:
    split_path = resolve_split_path(data_yaml_path, split_name)

    if split_path is None:
        return []

    image_paths: list[Path] = []

    if split_path.is_file():
        with open(split_path, "r") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                image_path = resolve_image_from_split_line(
                    line=line,
                    data_yaml_path=data_yaml_path,
                    split_file_path=split_path,
                )

                if image_path.exists() and image_path.suffix.lower() in IMG_EXTS:
                    image_paths.append(image_path)

    elif split_path.is_dir():
        image_paths = [
            p for p in sorted(split_path.rglob("*"))
            if p.suffix.lower() in IMG_EXTS
        ]

    else:
        raise FileNotFoundError(f"Could not find split path: {split_path}")

    return image_paths


def find_label_path(image_path: Path, source_dataset_root: Path) -> Path:
    """
    Converts:
      datasets/dataset_obj_detection/images/test/img.jpg

    into:
      datasets/dataset_obj_detection/labels/test/img.txt
    """
    stem_txt = f"{image_path.stem}.txt"

    candidates = []

    try:
        rel = image_path.relative_to(source_dataset_root)
        parts = list(rel.parts)

        if "images" in parts:
            image_index = parts.index("images")
            parts[image_index] = "labels"
            candidates.append(source_dataset_root / Path(*parts).with_suffix(".txt"))
    except ValueError:
        pass

    candidates.append(source_dataset_root / "labels" / image_path.parent.name / stem_txt)
    candidates.append(source_dataset_root / "labels" / stem_txt)
    candidates.append(image_path.with_suffix(".txt"))

    for candidate in candidates:
        if candidate.exists():
            return candidate

    print(f"WARNING: label not found for image: {image_path}")
    print("Tried:")
    for candidate in candidates:
        print(f"  {candidate}")

    return candidates[0]

def yolo_to_xyxy(
    x_center: float,
    y_center: float,
    w: float,
    h: float,
    img_w: int,
    img_h: int,
    padding: float = 0.0,
):
    box_w = w * img_w
    box_h = h * img_h

    x1 = (x_center * img_w) - (box_w / 2)
    y1 = (y_center * img_h) - (box_h / 2)
    x2 = (x_center * img_w) + (box_w / 2)
    y2 = (y_center * img_h) + (box_h / 2)

    pad_x = box_w * padding
    pad_y = box_h * padding

    x1 -= pad_x
    y1 -= pad_y
    x2 += pad_x
    y2 += pad_y

    x1 = max(0, min(int(x1), img_w - 1))
    y1 = max(0, min(int(y1), img_h - 1))
    x2 = max(0, min(int(x2), img_w - 1))
    y2 = max(0, min(int(y2), img_h - 1))

    return x1, y1, x2, y2


def read_yolo_label_file(label_path: Path) -> list[list[str]]:
    if not label_path.exists():
        return []

    rows = []

    with open(label_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 5:
                continue

            rows.append(parts)

    return rows


def build_fine_to_general_mapping(
    fine_names: dict[int, str],
    cfg_mapping: dict,
) -> dict[int, str]:
    """
    Takes config like:
      fine_to_general:
        Scalpel n4: scalpel
        Straight Dissection Clamp: clamp
        Straight Mayo Scissor: scissors
        Curved Mayo Scissor: scissors

    Returns:
      {0: "scalpel", 1: "clamp", ...}
    """
    exact_map = {str(k): str(v) for k, v in cfg_mapping.items()}
    normalized_map = {normalize_name(k): str(v) for k, v in cfg_mapping.items()}

    output = {}

    for fine_id, fine_name in fine_names.items():
        if fine_name in exact_map:
            output[fine_id] = exact_map[fine_name]
            continue

        norm = normalize_name(fine_name)

        if norm in normalized_map:
            output[fine_id] = normalized_map[norm]
            continue

        raise KeyError(
            f"No fine_to_general mapping found for class '{fine_name}'. "
            f"Add it to build_2stage_datasets.yaml."
        )

    return output


def build_general_dataset(
    root: Path,
    cfg: DictConfig,
    source_data_yaml: Path,
    fine_names: dict[int, str],
    fine_to_general: dict[int, str],
    general_names: list[str],
):
    source_dataset_root = get_dataset_root(source_data_yaml)
    output_dir = resolve_path(root, cfg.output.general_detection_dir)

    if output_dir.exists() and cfg.output.overwrite:
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    general_name_to_id = {name: i for i, name in enumerate(general_names)}

    manifest_rows = []
    label_count = 0
    image_count = 0

    for split in cfg.splits:
        image_paths = get_image_paths_for_split(source_data_yaml, split)

        out_img_dir = output_dir / "images" / split
        out_lbl_dir = output_dir / "labels" / split

        out_img_dir.mkdir(parents=True, exist_ok=True)
        out_lbl_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nBuilding general YOLO split: {split} ({len(image_paths)} images)")

        for image_path in tqdm(image_paths):
            label_path = find_label_path(image_path, source_dataset_root)
            label_rows = read_yolo_label_file(label_path)

            out_image_path = out_img_dir / image_path.name
            out_label_path = out_lbl_dir / f"{image_path.stem}.txt"

            shutil.copy2(image_path, out_image_path)

            new_label_lines = []

            for parts in label_rows:
                fine_id = int(float(parts[0]))
                x, y, w, h = parts[1:5]

                fine_name = fine_names[fine_id]
                general_name = fine_to_general[fine_id]
                general_id = general_name_to_id[general_name]

                new_label_lines.append(f"{general_id} {x} {y} {w} {h}")

                manifest_rows.append(
                    {
                        "split": split,
                        "image": str(out_image_path),
                        "source_image": str(image_path),
                        "source_label": str(label_path),
                        "fine_id": fine_id,
                        "fine_class": fine_name,
                        "general_id": general_id,
                        "general_class": general_name,
                    }
                )

                label_count += 1

            with open(out_label_path, "w") as f:
                f.write("\n".join(new_label_lines))

                if len(new_label_lines) > 0:
                    f.write("\n")

            image_count += 1

    data_yaml = {
        "path": str(output_dir.resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {i: name for i, name in enumerate(general_names)},
    }

    save_yaml(output_dir / "data.yaml", data_yaml)

    with open(output_dir / "general_manifest.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "split",
                "image",
                "source_image",
                "source_label",
                "fine_id",
                "fine_class",
                "general_id",
                "general_class",
            ],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    with open(output_dir / "fine_to_general.json", "w") as f:
        json.dump(
            {
                "fine_names": fine_names,
                "fine_to_general": fine_to_general,
                "general_names": general_names,
            },
            f,
            indent=2,
        )

    print("\nGeneral YOLO dataset created:")
    print(f"  output: {output_dir}")
    print(f"  images: {image_count}")
    print(f"  labels: {label_count}")
    print(f"  data.yaml: {output_dir / 'data.yaml'}")


def build_specific_classifier_datasets(
    root: Path,
    cfg: DictConfig,
    source_data_yaml: Path,
    fine_names: dict[int, str],
    fine_to_general: dict[int, str],
):
    source_dataset_root = get_dataset_root(source_data_yaml)
    output_dir = resolve_path(root, cfg.output.specific_classifier_dir)

    if output_dir.exists() and cfg.output.overwrite:
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    crop_count_by_general = {}

    for split in cfg.splits:
        image_paths = get_image_paths_for_split(source_data_yaml, split)

        print(f"\nBuilding specific classifier crops: {split} ({len(image_paths)} images)")

        for image_path in tqdm(image_paths):
            label_path = find_label_path(image_path, source_dataset_root)
            label_rows = read_yolo_label_file(label_path)

            if not label_rows:
                continue

            image = Image.open(image_path).convert("RGB")
            img_w, img_h = image.size

            box_index = 0

            for parts in label_rows:
                fine_id = int(float(parts[0]))
                x_center = float(parts[1])
                y_center = float(parts[2])
                box_w = float(parts[3])
                box_h = float(parts[4])

                fine_name = fine_names[fine_id]
                general_name = fine_to_general[fine_id]

                x1, y1, x2, y2 = yolo_to_xyxy(
                    x_center=x_center,
                    y_center=y_center,
                    w=box_w,
                    h=box_h,
                    img_w=img_w,
                    img_h=img_h,
                    padding=float(cfg.crop.padding),
                )

                if x2 <= x1 or y2 <= y1:
                    continue

                crop = image.crop((x1, y1, x2, y2))

                general_folder = clean_folder_name(general_name)
                fine_folder = clean_folder_name(fine_name)

                out_dir = output_dir / general_folder / split / fine_folder
                out_dir.mkdir(parents=True, exist_ok=True)

                crop_name = f"{image_path.stem}_box{box_index}_{fine_folder}.jpg"
                crop_path = out_dir / crop_name

                crop.save(crop_path, quality=95)

                crop_count_by_general[general_name] = crop_count_by_general.get(general_name, 0) + 1

                manifest_rows.append(
                    {
                        "split": split,
                        "source_image": str(image_path),
                        "source_label": str(label_path),
                        "crop_path": str(crop_path),
                        "general_class": general_name,
                        "fine_class": fine_name,
                        "fine_id": fine_id,
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    }
                )

                box_index += 1

    manifest_path = output_dir / "specific_classifier_manifest.csv"

    with open(manifest_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "split",
                "source_image",
                "source_label",
                "crop_path",
                "general_class",
                "fine_class",
                "fine_id",
                "x1",
                "y1",
                "x2",
                "y2",
            ],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    summary = {
        "output_dir": str(output_dir),
        "crop_count_by_general": crop_count_by_general,
        "note": (
            "Each folder under this directory is one general-class-specific "
            "classifier dataset in ImageFolder format."
        ),
    }

    with open(output_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\nSpecific classifier crop datasets created:")
    print(f"  output: {output_dir}")
    print(f"  manifest: {manifest_path}")

    for general_name, count in crop_count_by_general.items():
        print(f"  {general_name}: {count} crops")


@hydra.main(version_base=None, config_path="../config", config_name="2_stage_datasets")
def main(cfg: DictConfig):
    root = Path(get_original_cwd())

    print(OmegaConf.to_yaml(cfg))

    source_data_yaml = resolve_path(root, cfg.source.data_yaml)
    source_data = load_yaml(source_data_yaml)

    fine_names = parse_names(source_data["names"])
    fine_to_general = build_fine_to_general_mapping(
        fine_names=fine_names,
        cfg_mapping=cfg.mapping.fine_to_general,
    )

    general_names = list(cfg.mapping.general_names)

    print("\nFine classes:")
    for fine_id, fine_name in fine_names.items():
        print(f"  {fine_id}: {fine_name} -> {fine_to_general[fine_id]}")

    print("\nGeneral classes:")
    for i, name in enumerate(general_names):
        print(f"  {i}: {name}")

    build_general_dataset(
        root=root,
        cfg=cfg,
        source_data_yaml=source_data_yaml,
        fine_names=fine_names,
        fine_to_general=fine_to_general,
        general_names=general_names,
    )

    build_specific_classifier_datasets(
        root=root,
        cfg=cfg,
        source_data_yaml=source_data_yaml,
        fine_names=fine_names,
        fine_to_general=fine_to_general,
    )


if __name__ == "__main__":
    main()