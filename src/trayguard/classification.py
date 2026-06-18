from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Sequence

import cv2
import numpy as np
from ultralytics import YOLO

from trayguard.data_collection.classes import resolve_class_name


def classify_image(
    model: YOLO,
    image: np.ndarray,
    imgsz: int = 640,
    top_k: int = 5,
) -> dict[str, Any]:
    results = model.predict(
        source=image, imgsz=imgsz, save=False, verbose=False,
    )
    result = results[0]

    predictions: list[dict[str, Any]] = []
    if result.probs is not None:
        probs = result.probs.data.cpu().numpy()
        top_indices = probs.argsort()[-top_k:][::-1]
        for idx in top_indices:
            predictions.append({
                "class_id": int(idx),
                "class_name": resolve_class_name(model.names[int(idx)]),
                "confidence": float(probs[idx]),
            })

    speed_ms = {stage: float(latency) for stage, latency in result.speed.items()}
    return {
        "predictions": predictions,
        "speed_ms": speed_ms,
        "total_speed_ms": float(sum(speed_ms.values())),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trayguard classify-image",
        description="Classify a single image using a trained YOLO classification model.",
    )
    parser.add_argument("--model", type=Path, default=Path("weights/50_pictures_classification.pt"))
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("image", type=Path, help="Path to image file.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    if not args.image.exists():
        raise FileNotFoundError(f"Image not found: {args.image}")

    model = YOLO(str(args.model))
    print(f"Model loaded: {len(model.names)} classes  |  device: {model.device}")

    img = cv2.imread(str(args.image))
    if img is None:
        raise ValueError(f"Could not read image: {args.image}")

    result = classify_image(model, img, imgsz=args.imgsz, top_k=args.top_k)
    print(f"Latency: {result['total_speed_ms']:.1f} ms")
    print()
    for p in result["predictions"]:
        print(f"  {p['class_name']:<40} {p['confidence']:.4f}")
