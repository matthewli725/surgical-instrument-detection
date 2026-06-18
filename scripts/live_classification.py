from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np

from trayguard.classification import classify_image


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Live camera classification with YOLO via OpenCV window."
    )
    parser.add_argument("--weights", type=Path, default=Path("weights/50_pictures_classification.pt"))
    parser.add_argument("--camera", type=int, default=0, help="Camera index.")
    parser.add_argument("--imgsz", type=int, default=320, help="Inference image size (smaller = faster).")
    parser.add_argument("--top-k", type=int, default=3, help="Number of top predictions to show.")
    parser.add_argument("--conf", type=float, default=0.0, help="Minimum confidence to display.")
    return parser.parse_args(argv)


def _draw_text_line(
    frame: np.ndarray,
    text: str,
    x: int,
    y: int,
    scale: float = 0.65,
    color: tuple[int, int, int] = (255, 255, 255),
    bg_color: tuple[int, int, int] = (0, 0, 0),
) -> int:
    """Draw text with a dark background, return new y offset."""
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
    pad = 4
    cv2.rectangle(frame, (x - pad, y - th - pad), (x + tw + pad, y + pad), bg_color, -1)
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)
    return y + th + 16


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    from ultralytics import YOLO

    model = YOLO(str(args.weights))
    print(f"Model loaded: {len(model.names)} classes  |  device: {model.device}")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {args.camera}")

    conf = args.conf
    imgsz = args.imgsz
    top_k = args.top_k
    paused = False
    fps = 0.0
    frame_count = 0
    fps_timer = time.perf_counter()
    window_name = "Live Classification — q:quit  space:pause  +/-:conf  [/]:imgsz  1-9:top-k"

    cv2.namedWindow(window_name)

    try:
        while True:
            if not paused:
                ok, frame = cap.read()
                if not ok or frame is None:
                    time.sleep(0.03)
                    continue

                prediction = classify_image(model, frame, imgsz=imgsz, top_k=top_k)

                frame_count += 1
                if frame_count >= 10:
                    now = time.perf_counter()
                    fps = frame_count / (now - fps_timer)
                    fps_timer = now
                    frame_count = 0

                annotated = frame.copy()
                h, w = annotated.shape[:2]

                y = 30
                info_line = (
                    f"FPS: {fps:.1f}  |  conf: {conf:.2f}  |  imgsz: {imgsz}  |  "
                    f"latency: {prediction['total_speed_ms']:.0f} ms"
                )
                if paused:
                    info_line += "  PAUSED"
                y = _draw_text_line(annotated, info_line, 10, y, scale=0.55, color=(0, 255, 255))

                if not prediction["predictions"]:
                    y = _draw_text_line(annotated, "(no predictions above threshold)", 10, y)
                else:
                    y = _draw_text_line(annotated, f"Top {top_k} predictions:", 10, y)
                    for p in prediction["predictions"]:
                        if p["confidence"] < conf:
                            continue
                        label = f"{p['class_name']}  {p['confidence']:.3f}"
                        y = _draw_text_line(annotated, label, 10, y)
                        # confidence bar
                        bar_w = 200
                        bar_h = 10
                        bar_x = 10
                        bar_y = y - 12
                        filled = int(bar_w * p["confidence"])
                        cv2.rectangle(annotated, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (40, 40, 40), -1)
                        cv2.rectangle(annotated, (bar_x, bar_y), (bar_x + filled, bar_y + bar_h), (0, 255, 0), -1)

                cv2.imshow(window_name, annotated)
            else:
                time.sleep(0.05)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord(" "):
                paused = not paused
            elif key == ord("+") or key == ord("="):
                conf = min(1.0, conf + 0.05)
                print(f"conf: {conf:.2f}")
            elif key == ord("-") or key == ord("_"):
                conf = max(0.0, conf - 0.05)
                print(f"conf: {conf:.2f}")
            elif key == ord("]"):
                imgsz = min(1280, imgsz + 32)
                print(f"imgsz: {imgsz}")
            elif key == ord("["):
                imgsz = max(160, imgsz - 32)
                print(f"imgsz: {imgsz}")
            elif ord("1") <= key <= ord("9"):
                top_k = key - ord("0")
                print(f"top-k: {top_k}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
