from __future__ import annotations

import copy
import json
import random
from pathlib import Path
from typing import Dict, Tuple

import hydra
import numpy as np
import torch
import torch.nn as nn
from omegaconf import DictConfig, OmegaConf
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def build_transforms(image_size: int) -> Tuple[transforms.Compose, transforms.Compose]:
    train_tfms = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=8),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.1, hue=0.02),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    eval_tfms = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    return train_tfms, eval_tfms


def build_dataloaders(cfg: DictConfig):
    train_tfms, eval_tfms = build_transforms(cfg.classifier_model.image_size)

    train_dataset = datasets.ImageFolder(cfg.classifier_data.train_dir, transform=train_tfms)
    val_dataset = datasets.ImageFolder(cfg.classifier_data.val_dir, transform=eval_tfms)
    test_dataset = datasets.ImageFolder(cfg.classifier_data.test_dir, transform=eval_tfms)

    train_loader = DataLoader(
        train_dataset,
        batch_size=cfg.classifier_trainer.batch_size,
        shuffle=True,
        num_workers=cfg.classifier_trainer.num_workers,
        pin_memory=cfg.classifier_trainer.pin_memory,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=cfg.classifier_trainer.batch_size,
        shuffle=False,
        num_workers=cfg.classifier_trainer.num_workers,
        pin_memory=cfg.classifier_trainer.pin_memory,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=cfg.classifier_trainer.batch_size,
        shuffle=False,
        num_workers=cfg.classifier_trainer.num_workers,
        pin_memory=cfg.classifier_trainer.pin_memory,
    )

    return train_dataset, val_dataset, test_dataset, train_loader, val_loader, test_loader


def freeze_backbone_if_needed(model: nn.Module, arch: str, freeze_backbone: bool) -> None:
    if not freeze_backbone:
        return

    for param in model.parameters():
        param.requires_grad = False

    if arch == "resnet18":
        for param in model.fc.parameters():
            param.requires_grad = True

    elif arch == "efficientnet_b0":
        for param in model.classifier.parameters():
            param.requires_grad = True

    else:
        raise ValueError(f"Unsupported arch for freezing: {arch}")


def build_model(cfg: DictConfig) -> nn.Module:
    arch = cfg.classifier_model.arch
    num_classes = cfg.classifier_data.num_classes
    pretrained = cfg.classifier_model.pretrained

    if arch == "resnet18":
        weights = models.ResNet18_Weights.DEFAULT if pretrained else None
        model = models.resnet18(weights=weights)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)

    elif arch == "efficientnet_b0":
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        model = models.efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)

    else:
        raise ValueError(f"Unsupported model arch: {arch}")

    freeze_backbone_if_needed(model, arch, cfg.classifier_model.freeze_backbone)
    return model


def build_optimizer(cfg: DictConfig, model: nn.Module):
    params = [p for p in model.parameters() if p.requires_grad]

    if cfg.classifier_trainer.optimizer.lower() == "adamw":
        return torch.optim.AdamW(
            params,
            lr=cfg.classifier_trainer.lr,
            weight_decay=cfg.classifier_trainer.weight_decay,
        )

    raise ValueError(f"Unsupported optimizer: {cfg.classifier_trainer.optimizer}")


def compute_accuracy(logits: torch.Tensor, targets: torch.Tensor) -> float:
    preds = logits.argmax(dim=1)
    correct = (preds == targets).sum().item()
    total = targets.size(0)
    return correct / total


def run_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer,
    device: torch.device,
    scaler: torch.cuda.amp.GradScaler,
    use_amp: bool,
    train: bool,
) -> Dict[str, float]:
    if train:
        model.train()
    else:
        model.eval()

    running_loss = 0.0
    running_correct = 0
    running_total = 0

    for images, targets in loader:
        images = images.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        if train:
            optimizer.zero_grad(set_to_none=True)

        with torch.set_grad_enabled(train):
            with torch.cuda.amp.autocast(enabled=use_amp):
                logits = model(images)
                loss = criterion(logits, targets)

            if train:
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()

        preds = logits.argmax(dim=1)
        running_loss += loss.item() * images.size(0)
        running_correct += (preds == targets).sum().item()
        running_total += images.size(0)

    epoch_loss = running_loss / max(running_total, 1)
    epoch_acc = running_correct / max(running_total, 1)

    return {
        "loss": epoch_loss,
        "acc": epoch_acc,
    }


@torch.no_grad()
def evaluate_per_class(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    class_names,
) -> Dict[str, Dict[str, float]]:
    model.eval()

    num_classes = len(class_names)
    correct_per_class = [0] * num_classes
    total_per_class = [0] * num_classes

    for images, targets in loader:
        images = images.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        logits = model(images)
        preds = logits.argmax(dim=1)

        for cls_idx in range(num_classes):
            cls_mask = (targets == cls_idx)
            cls_total = cls_mask.sum().item()
            if cls_total > 0:
                total_per_class[cls_idx] += cls_total
                correct_per_class[cls_idx] += ((preds == targets) & cls_mask).sum().item()

    out = {}
    for i, class_name in enumerate(class_names):
        total = total_per_class[i]
        acc = correct_per_class[i] / total if total > 0 else 0.0
        out[class_name] = {
            "count": total,
            "accuracy": acc,
        }

    return out


@hydra.main(version_base=None, config_path="../config", config_name="classifier_config")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    set_seed(cfg.classifier_trainer.seed)

    device = torch.device(
        "cuda" if cfg.classifier_trainer.device == "cuda" and torch.cuda.is_available() else "cpu"
    )

    train_dataset, val_dataset, test_dataset, train_loader, val_loader, test_loader = build_dataloaders(cfg)

    model = build_model(cfg).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = build_optimizer(cfg, model)
    scaler = torch.cuda.amp.GradScaler(enabled=cfg.classifier_trainer.use_amp and device.type == "cuda")

    run_dir = Path(cfg.classifier_trainer.project) / cfg.classifier_trainer.name
    run_dir.mkdir(parents=True, exist_ok=True)

    best_val_acc = -1.0
    best_state = None
    epochs_without_improvement = 0

    history = {
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": [],
    }

    for epoch in range(cfg.classifier_trainer.epochs):
        train_metrics = run_one_epoch(
            model=model,
            loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            scaler=scaler,
            use_amp=cfg.classifier_trainer.use_amp and device.type == "cuda",
            train=True,
        )

        val_metrics = run_one_epoch(
            model=model,
            loader=val_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            scaler=scaler,
            use_amp=cfg.classifier_trainer.use_amp and device.type == "cuda",
            train=False,
        )

        history["train_loss"].append(train_metrics["loss"])
        history["train_acc"].append(train_metrics["acc"])
        history["val_loss"].append(val_metrics["loss"])
        history["val_acc"].append(val_metrics["acc"])

        print(
            f"Epoch [{epoch + 1}/{cfg.classifier_trainer.epochs}] "
            f"train_loss={train_metrics['loss']:.4f} "
            f"train_acc={train_metrics['acc']:.4f} "
            f"val_loss={val_metrics['loss']:.4f} "
            f"val_acc={val_metrics['acc']:.4f}"
        )

        if val_metrics["acc"] > best_val_acc:
            best_val_acc = val_metrics["acc"]
            best_state = copy.deepcopy(model.state_dict())
            epochs_without_improvement = 0

            torch.save(best_state, run_dir / "best.pt")
            print(f"Saved best model to {run_dir / 'best.pt'}")
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= cfg.classifier_trainer.early_stopping_patience:
            print("Early stopping triggered.")
            break

    if best_state is not None:
        model.load_state_dict(best_state)

    test_metrics = run_one_epoch(
        model=model,
        loader=test_loader,
        criterion=criterion,
        optimizer=optimizer,
        device=device,
        scaler=scaler,
        use_amp=cfg.classifier_trainer.use_amp and device.type == "cuda",
        train=False,
    )

    per_class_test = evaluate_per_class(
        model=model,
        loader=test_loader,
        device=device,
        class_names=test_dataset.classes,
    )

    results = {
        "best_val_acc": best_val_acc,
        "test_loss": test_metrics["loss"],
        "test_acc": test_metrics["acc"],
        "class_to_idx": train_dataset.class_to_idx,
        "per_class_test": per_class_test,
        "history": history,
    }

    with open(run_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nFinal test results:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()