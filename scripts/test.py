import torch
from ultralytics import YOLO
from trayguard.detection import process_image, draw_detections
import cv2

device = "cpu"  # MPS is slower for YOLO11n — NMS ops bottleneck
model = YOLO("weights/50_pictures_detection.pt")
if device != "cpu":
    model.to(device)
print(f"Model loaded: {model.names}  |  device: {device}")

img = cv2.imread("data/cv/50_pictures_auto/yolo/images/val/forcep_1_sample_000002.jpg")
result = process_image(model, img)
print(f"Detections: {len(result['detections'])}")
for d in result["detections"]:
    print(f"  {d['class_name']} ({d['confidence']:.2f}): {d['bbox_xyxy']}")
print(f"Latency: {result['total_speed_ms']:.1f} ms ({1_000 / result['total_speed_ms']:.1f} fps)")

annotated = draw_detections(img, result["detections"])
out_path = "runs/inference/forcep_1_sample_000002.jpg"
cv2.imwrite(out_path, annotated)
print(f"Saved: {out_path}")