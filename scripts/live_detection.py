from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np

from trayguard.detection import draw_detections, process_image


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Live camera detection with YOLO via OpenCV window."
    )
    parser.add_argument("--weights", type=Path, default=Path("weights/50_pictures_detection.pt"))
    parser.add_argument("--camera", type=int, default=0, help="Camera index.")
    parser.add_argument("--imgsz", type=int, default=320, help="Inference image size (smaller = faster).")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold.")
    return parser.parse_args(argv)


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
    paused = False
    fps = 0.0
    frame_count = 0
    fps_timer = time.perf_counter()
    window_name = "Live Detection — q:quit  space:pause  +/-:conf  [/]:imgsz"

    cv2.namedWindow(window_name)

    try:
        while True:
            if not paused:
                ok, frame = cap.read()
                if not ok or frame is None:
                    time.sleep(0.03)
                    continue

                prediction = process_image(model, frame, imgsz=imgsz, conf=conf)
                annotated = draw_detections(frame, prediction["detections"])

                frame_count += 1
                if frame_count >= 10:
                    now = time.perf_counter()
                    fps = frame_count / (now - fps_timer)
                    fps_timer = now
                    frame_count = 0

                info_lines = [
                    f"FPS: {fps:.1f}  |  conf: {conf:.2f}  |  imgsz: {imgsz}  |  "
                    f"latency: {prediction['total_speed_ms']:.0f} ms",
                    f"Detections: {len(prediction['detections'])}",
                ]
                if paused:
                    info_lines.insert(1, "PAUSED")

                y_offset = 30
                for line in info_lines:
                    cv2.putText(
                        annotated, line, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv2.LINE_AA,
                    )
                    y_offset += 24

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
                conf = max(0.05, conf - 0.05)
                print(f"conf: {conf:.2f}")
            elif key == ord("]"):
                imgsz = min(1280, imgsz + 32)
                print(f"imgsz: {imgsz}")
            elif key == ord("["):
                imgsz = max(160, imgsz - 32)
                print(f"imgsz: {imgsz}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
