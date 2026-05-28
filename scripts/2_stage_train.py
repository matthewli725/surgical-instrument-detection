from __future__ import annotations

import csv
import html
import json
import os
import random
import shutil
import webbrowser
from pathlib import Path

import hydra
import numpy as np
import torch
import torch.nn as nn
import yaml
from hydra.utils import get_original_cwd
from omegaconf import DictConfig, OmegaConf
from PIL import Image, ImageDraw, ImageFont
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import (
    efficientnet_b0,
    EfficientNet_B0_Weights,
    resnet18,
    ResNet18_Weights,
)
from tqdm import tqdm
from ultralytics import YOLO


def resolve_path(root: Path, path: str | Path | None) -> Path | None:
    if path is None:
        return None

    path = Path(path)
    return path if path.is_absolute() else root / path


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_checkpoint(path: Path, device: str):
    try:
        return torch.load(path, map_location=device, weights_only=False)
    except TypeError:
        return torch.load(path, map_location=device)


def safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def clean_name(name: str) -> str:
    return (
        str(name)
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

def get_general_detector_weights(root: Path, cfg: DictConfig) -> Path:
    data_yaml_path = resolve_path(root, cfg.general_detector.data_yaml)

    if cfg.general_detector.train:
        model = YOLO(cfg.general_detector.model)

        results = model.train(
            data=str(data_yaml_path),
            epochs=cfg.general_detector.epochs,
            imgsz=cfg.general_detector.imgsz,
            batch=cfg.general_detector.batch,
            project=str(resolve_path(root, cfg.general_detector.project)),
            name=cfg.general_detector.run_name,
            exist_ok=True,
        )

        weights = Path(results.save_dir) / "weights" / "best.pt"

        if not weights.exists():
            raise FileNotFoundError(f"Training finished but weights were not found: {weights}")

        return weights

    run_dir = resolve_path(root, cfg.general_detector.run_dir)
    weights = run_dir / "weights" / "best.pt"

    if not weights.exists():
        raise FileNotFoundError(f"Could not find general detector weights: {weights}")

    return weights


def freeze_model_backbone(model: nn.Module):
    for param in model.parameters():
        param.requires_grad = False


def build_classifier(model_cfg: DictConfig, num_classes: int) -> nn.Module:
    arch = str(model_cfg.arch).lower()
    pretrained = bool(model_cfg.pretrained)
    dropout = float(model_cfg.dropout)
    freeze_backbone = bool(model_cfg.freeze_backbone)

    if arch == "efficientnet_b0":
        weights = EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = efficientnet_b0(weights=weights)

        if freeze_backbone:
            freeze_model_backbone(model)

        in_features = model.classifier[1].in_features

        if dropout > 0:
            model.classifier[1] = nn.Sequential(
                nn.Dropout(dropout),
                nn.Linear(in_features, num_classes),
            )
        else:
            model.classifier[1] = nn.Linear(in_features, num_classes)

        return model

    if arch == "resnet18":
        weights = ResNet18_Weights.DEFAULT if pretrained else None
        model = resnet18(weights=weights)

        if freeze_backbone:
            freeze_model_backbone(model)

        in_features = model.fc.in_features

        if dropout > 0:
            model.fc = nn.Sequential(
                nn.Dropout(dropout),
                nn.Linear(in_features, num_classes),
            )
        else:
            model.fc = nn.Linear(in_features, num_classes)

        return model

    raise ValueError(
        f"Unknown classifier architecture '{arch}'. "
        "Supported: efficientnet_b0, resnet18"
    )


def get_transforms(imgsz: int):
    train_tfms = transforms.Compose(
        [
            transforms.Resize((imgsz, imgsz)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(8),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    eval_tfms = transforms.Compose(
        [
            transforms.Resize((imgsz, imgsz)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    return train_tfms, eval_tfms


def make_loader(dataset, batch_size: int, shuffle: bool, num_workers: int):
    use_workers = num_workers > 0

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available(),
        persistent_workers=use_workers,
        prefetch_factor=2 if use_workers else None,
    )


def run_one_epoch(model, loader, optimizer, loss_fn, device, train: bool):
    model.train() if train else model.eval()

    total_loss = 0.0
    correct = 0
    total = 0

    for images, labels in tqdm(loader, leave=False):
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        if train:
            optimizer.zero_grad(set_to_none=True)

        with torch.set_grad_enabled(train):
            logits = model(images)
            loss = loss_fn(logits, labels)

            if train:
                loss.backward()
                optimizer.step()

        total_loss += loss.item() * images.size(0)

        preds = logits.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += images.size(0)

    avg_loss = total_loss / max(total, 1)
    acc = correct / max(total, 1)

    return avg_loss, acc


def write_passthrough_classifier(run_dir: Path, general_class: str, class_names: list[str]) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)

    passthrough_path = run_dir / "passthrough.json"

    with open(passthrough_path, "w") as f:
        json.dump(
            {
                "general_class": general_class,
                "class_names": class_names,
                "chosen_class": class_names[0],
                "reason": "Only one specific class exists, so no classifier was trained.",
            },
            f,
            indent=2,
        )

    print(f"\nSkipping classifier for '{general_class}' because it only has one variant.")
    print(f"Saved passthrough file to: {passthrough_path}")

    return passthrough_path


def train_specific_classifier(
    root: Path,
    cfg: DictConfig,
    general_detector_weights: Path,
) -> dict:
    train_cfg = cfg.specific_classifier
    model_cfg = cfg.classifier_model

    general_class = clean_name(train_cfg.general_class)

    data_dir = resolve_path(root, train_cfg.data_dir)

    if data_dir is None:
        data_dir = resolve_path(root, cfg.specific_classifier.base_data_dir) / general_class

    if not data_dir.exists():
        raise FileNotFoundError(f"Specific classifier dataset not found: {data_dir}")

    train_dir = data_dir / "train"
    val_dir = data_dir / "val"
    test_dir = data_dir / "test"

    if not train_dir.exists():
        raise FileNotFoundError(f"Missing train folder: {train_dir}")

    run_dir = resolve_path(root, train_cfg.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(general_detector_weights, run_dir / "stage1_general_detector_best.pt")

    train_tfms, eval_tfms = get_transforms(model_cfg.image_size)

    train_ds = datasets.ImageFolder(train_dir, transform=train_tfms)
    val_ds = datasets.ImageFolder(val_dir, transform=eval_tfms) if val_dir.exists() else None
    test_ds = datasets.ImageFolder(test_dir, transform=eval_tfms) if test_dir.exists() else None

    class_names = train_ds.classes
    num_classes = len(class_names)

    with open(run_dir / "class_names.json", "w") as f:
        json.dump(class_names, f, indent=2)

    if num_classes <= 1 and train_cfg.skip_single_variant:
        passthrough_path = write_passthrough_classifier(
            run_dir=run_dir,
            general_class=general_class,
            class_names=class_names,
        )

        return {
            "general_class": general_class,
            "type": "passthrough",
            "class_names": class_names,
            "run_dir": str(run_dir),
            "passthrough_path": str(passthrough_path),
        }

    train_loader = make_loader(
        train_ds,
        batch_size=train_cfg.batch,
        shuffle=True,
        num_workers=train_cfg.num_workers,
    )

    val_loader = (
        make_loader(
            val_ds,
            batch_size=train_cfg.batch,
            shuffle=False,
            num_workers=train_cfg.num_workers,
        )
        if val_ds is not None
        else None
    )

    test_loader = (
        make_loader(
            test_ds,
            batch_size=train_cfg.batch,
            shuffle=False,
            num_workers=train_cfg.num_workers,
        )
        if test_ds is not None
        else None
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = build_classifier(
        model_cfg=model_cfg,
        num_classes=num_classes,
    ).to(device)

    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=train_cfg.lr,
        weight_decay=train_cfg.weight_decay,
    )

    loss_fn = nn.CrossEntropyLoss()

    best_val_acc = -1.0
    best_path = run_dir / "best.pt"

    log_path = run_dir / "classifier_train.log"
    results_path = run_dir / "results.json"

    history = []

    print("\n==============================")
    print(f"Training specific classifier for: {general_class}")
    print(f"Model: {model_cfg.name}")
    print(f"Specific classes: {class_names}")
    print(f"Dataset: {data_dir}")
    print(f"Run dir: {run_dir}")
    print("==============================")

    with open(log_path, "w") as log_file:
        log_file.write(f"general_class={general_class}\n")
        log_file.write(f"classifier_name={model_cfg.name}\n")
        log_file.write(f"classifier_arch={model_cfg.arch}\n")
        log_file.write(f"class_names={class_names}\n")
        log_file.write(f"dataset={data_dir}\n")
        log_file.write(f"general_detector_weights={general_detector_weights}\n")
        log_file.write(f"run_dir={run_dir}\n\n")

        for epoch in range(train_cfg.epochs):
            print(f"\n[{general_class} classifier] epoch {epoch + 1}/{train_cfg.epochs}")

            train_loss, train_acc = run_one_epoch(
                model=model,
                loader=train_loader,
                optimizer=optimizer,
                loss_fn=loss_fn,
                device=device,
                train=True,
            )

            if val_loader is not None:
                val_loss, val_acc = run_one_epoch(
                    model=model,
                    loader=val_loader,
                    optimizer=optimizer,
                    loss_fn=loss_fn,
                    device=device,
                    train=False,
                )
            else:
                val_loss, val_acc = train_loss, train_acc

            line = (
                f"epoch={epoch + 1} "
                f"train_loss={train_loss:.4f} "
                f"train_acc={train_acc:.4f} "
                f"val_loss={val_loss:.4f} "
                f"val_acc={val_acc:.4f}"
            )

            print(line)
            log_file.write(line + "\n")
            log_file.flush()

            history.append(
                {
                    "epoch": epoch + 1,
                    "train_loss": train_loss,
                    "train_acc": train_acc,
                    "val_loss": val_loss,
                    "val_acc": val_acc,
                }
            )

            if val_acc > best_val_acc:
                best_val_acc = val_acc

                torch.save(
                    {
                        "general_class": general_class,
                        "model_name": model_cfg.name,
                        "model_arch": model_cfg.arch,
                        "model_cfg": OmegaConf.to_container(model_cfg, resolve=True),
                        "model_state": model.state_dict(),
                        "class_names": class_names,
                        "num_classes": num_classes,
                        "imgsz": model_cfg.image_size,
                    },
                    best_path,
                )

                print(f"saved best classifier: {best_path}")
                log_file.write(f"saved best classifier: {best_path}\n")
                log_file.flush()

    test_loss = None
    test_acc = None

    if test_loader is not None:
        ckpt = load_checkpoint(best_path, device)
        model.load_state_dict(ckpt["model_state"])

        test_loss, test_acc = run_one_epoch(
            model=model,
            loader=test_loader,
            optimizer=optimizer,
            loss_fn=loss_fn,
            device=device,
            train=False,
        )

        print(f"\n[{general_class} classifier test] loss={test_loss:.4f} acc={test_acc:.4f}")

    results = {
        "general_class": general_class,
        "type": "classifier",
        "model_name": model_cfg.name,
        "model_arch": model_cfg.arch,
        "dataset": str(data_dir),
        "run_dir": str(run_dir),
        "best_path": str(best_path),
        "best_val_acc": best_val_acc,
        "test_loss": test_loss,
        "test_acc": test_acc,
        "class_names": class_names,
        "history": history,
    }

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    return results


def load_specific_classifier(ckpt_path: Path, device: str):
    ckpt = load_checkpoint(ckpt_path, device)

    class_names = ckpt["class_names"]
    imgsz = ckpt["imgsz"]

    model_cfg = OmegaConf.create(ckpt["model_cfg"])
    model_cfg.pretrained = False

    model = build_classifier(
        model_cfg=model_cfg,
        num_classes=len(class_names),
    )

    model.load_state_dict(ckpt["model_state"])
    model.to(device)
    model.eval()

    general_class = ckpt["general_class"]

    return model, class_names, imgsz, general_class


def get_classifier_transform(imgsz: int):
    return transforms.Compose(
        [
            transforms.Resize((imgsz, imgsz)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def classify_crop(model, class_names, crop: Image.Image, imgsz: int, device: str):
    tfm = get_classifier_transform(imgsz)
    x = tfm(crop.convert("RGB")).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0]
        conf, idx = probs.max(dim=0)

    return class_names[idx.item()], float(conf.item())


def find_test_images(root: Path, cfg: DictConfig) -> list[Path]:
    image_dir = resolve_path(root, cfg.pipeline_test.image_dir)

    if image_dir is None or not image_dir.exists():
        raise FileNotFoundError(f"Test image folder not found: {image_dir}")

    image_paths = [
        p for p in sorted(image_dir.rglob("*"))
        if p.suffix.lower() in ".jpg"
    ]

    prefix = str(cfg.pipeline_test.filename_prefix).lower()

    if prefix:
        image_paths = [
            p for p in image_paths
            if p.name.lower().startswith(prefix)
        ]

    if cfg.pipeline_test.max_images is not None:
        image_paths = image_paths[: cfg.pipeline_test.max_images]

    if len(image_paths) == 0:
        raise RuntimeError(
            f"No test images found in {image_dir} with prefix '{prefix}'"
        )

    return image_paths


def get_font(size: int = 18):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str):
    x, y = xy
    font = get_font(18)

    bbox = draw.textbbox((x, y), text, font=font)
    pad = 5

    draw.rectangle(
        [
            bbox[0] - pad,
            bbox[1] - pad,
            bbox[2] + pad,
            bbox[3] + pad,
        ],
        fill="black",
    )

    draw.text((x, y), text, fill="white", font=font)


def clip_box(x1, y1, x2, y2, width: int, height: int):
    x1 = max(0, min(int(x1), width - 1))
    y1 = max(0, min(int(y1), height - 1))
    x2 = max(0, min(int(x2), width - 1))
    y2 = max(0, min(int(y2), height - 1))

    return x1, y1, x2, y2


def run_separado_test(
    root: Path,
    cfg: DictConfig,
    general_detector_weights: Path,
    classifier_result: dict,
):
    if not cfg.pipeline_test.enabled:
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"

    image_paths = find_test_images(root, cfg)

    output_dir = resolve_path(root, cfg.pipeline_test.output_dir)
    annotated_dir = output_dir / "annotated"
    crops_dir = output_dir / "crops"

    output_dir.mkdir(parents=True, exist_ok=True)
    annotated_dir.mkdir(parents=True, exist_ok=True)

    if cfg.pipeline_test.save_crops:
        crops_dir.mkdir(parents=True, exist_ok=True)

    detector = YOLO(str(general_detector_weights))

    selected_general_class = clean_name(cfg.specific_classifier.general_class)

    stage2_type = classifier_result["type"]

    classifier = None
    class_names = None
    classifier_imgsz = None

    if stage2_type == "classifier":
        classifier_path = Path(classifier_result["best_path"])
        classifier, class_names, classifier_imgsz, saved_general_class = load_specific_classifier(
            classifier_path,
            device,
        )
        selected_general_class = clean_name(saved_general_class)

    elif stage2_type == "passthrough":
        passthrough_path = Path(classifier_result["passthrough_path"])

        with open(passthrough_path, "r") as f:
            passthrough_info = json.load(f)

        passthrough_class = passthrough_info["chosen_class"]

    else:
        passthrough_class = None

    rows = []
    annotated_images = []

    print("\nRunning final separado test...")
    print(f"Images: {len(image_paths)}")
    print(f"Selected specific classifier general class: {selected_general_class}")

    for image_idx, image_path in enumerate(tqdm(image_paths, desc="separado two-stage test")):
        image = Image.open(image_path).convert("RGB")
        width, height = image.size

        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)

        results = detector.predict(
            source=str(image_path),
            imgsz=cfg.general_detector.imgsz,
            conf=cfg.pipeline_test.det_conf,
            verbose=False,
        )

        result = results[0]

        annotated_path = annotated_dir / f"{image_idx:04d}_{image_path.stem}_2stage.jpg"

        if result.boxes is None or len(result.boxes) == 0:
            draw_label(draw, (12, 12), "NO DETECTIONS")
            annotated.save(annotated_path)
            annotated_images.append(annotated_path)

            rows.append(
                {
                    "image": safe_relative(image_path, root),
                    "annotated_image": safe_relative(annotated_path, root),
                    "general_class": "",
                    "general_conf": "",
                    "specific_class": "",
                    "specific_conf": "",
                    "stage2_type": "none",
                    "x1": "",
                    "y1": "",
                    "x2": "",
                    "y2": "",
                    "crop_path": "",
                }
            )

            continue

        for box_idx, box in enumerate(result.boxes):
            x1, y1, x2, y2 = box.xyxy[0].cpu().tolist()
            x1, y1, x2, y2 = clip_box(x1, y1, x2, y2, width, height)

            if x2 <= x1 or y2 <= y1:
                continue

            general_id = int(box.cls[0].item())
            general_class = str(detector.names[general_id])
            general_conf = float(box.conf[0].item())

            crop = image.crop((x1, y1, x2, y2))

            crop_path_str = ""

            if cfg.pipeline_test.save_crops:
                crop_path = crops_dir / f"{image_idx:04d}_{image_path.stem}_box{box_idx}_{clean_name(general_class)}.jpg"
                crop.save(crop_path, quality=95)
                crop_path_str = safe_relative(crop_path, root)

            if clean_name(general_class) == selected_general_class and stage2_type == "classifier":
                specific_class, specific_conf = classify_crop(
                    model=classifier,
                    class_names=class_names,
                    crop=crop,
                    imgsz=classifier_imgsz,
                    device=device,
                )
                this_stage2_type = "specific_classifier"

            elif clean_name(general_class) == selected_general_class and stage2_type == "passthrough":
                specific_class = passthrough_class
                specific_conf = 1.0
                this_stage2_type = "passthrough"

            else:
                specific_class = general_class
                specific_conf = general_conf
                this_stage2_type = "general_only"

            label = f"{general_class} {general_conf:.2f} -> {specific_class} {specific_conf:.2f}"

            draw.rectangle([x1, y1, x2, y2], outline="red", width=4)
            draw_label(draw, (x1, max(0, y1 - 28)), label)

            rows.append(
                {
                    "image": safe_relative(image_path, root),
                    "annotated_image": safe_relative(annotated_path, root),
                    "general_class": general_class,
                    "general_conf": general_conf,
                    "specific_class": specific_class,
                    "specific_conf": specific_conf,
                    "stage2_type": this_stage2_type,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "crop_path": crop_path_str,
                }
            )

        annotated.save(annotated_path)
        annotated_images.append(annotated_path)

    csv_path = output_dir / "separado_two_stage_predictions.csv"

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "image",
                "annotated_image",
                "general_class",
                "general_conf",
                "specific_class",
                "specific_conf",
                "stage2_type",
                "x1",
                "y1",
                "x2",
                "y2",
                "crop_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    summary_path = output_dir / "separado_test_summary.json"

    with open(summary_path, "w") as f:
        json.dump(
            {
                "num_images": len(image_paths),
                "num_predictions": len([r for r in rows if r["general_class"] != ""]),
                "selected_general_class": selected_general_class,
                "general_detector_weights": str(general_detector_weights),
                "classifier_result": classifier_result,
                "csv_path": str(csv_path),
            },
            f,
            indent=2,
        )

    print(f"\nSaved annotated images to: {annotated_dir}")
    print(f"Saved crops to: {crops_dir}")
    print(f"Saved CSV predictions to: {csv_path}")
    print(f"Saved test summary to: {summary_path}")


@hydra.main(version_base=None, config_path="../config", config_name="2_stage")
def main(cfg: DictConfig):
    torch.backends.cudnn.benchmark = True

    root = Path(get_original_cwd())

    set_seed(cfg.seed)

    print(OmegaConf.to_yaml(cfg))

    general_detector_weights = get_general_detector_weights(root, cfg)

    print(f"\nStage 1 general detector weights: {general_detector_weights}")

    if cfg.general_detector.test:
        detector = YOLO(str(general_detector_weights))

        detector.val(
            data=str(resolve_path(root, cfg.general_detector.data_yaml)),
            split=cfg.pipeline_test.yolo_val_split,
            imgsz=cfg.general_detector.imgsz,
        )

    classifier_result = train_specific_classifier(
        root=root,
        cfg=cfg,
        general_detector_weights=general_detector_weights,
    )

    run_separado_test(
        root=root,
        cfg=cfg,
        general_detector_weights=general_detector_weights,
        classifier_result=classifier_result,
    )

    summary_path = resolve_path(root, cfg.summary_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with open(summary_path, "w") as f:
        json.dump(
            {
                "stage1_general_detector_weights": str(general_detector_weights),
                "specific_classifier": classifier_result,
            },
            f,
            indent=2,
        )

    print(f"\nSaved two-stage summary to: {summary_path}")


if __name__ == "__main__":
    main()