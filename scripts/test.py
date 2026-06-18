import cv2
from ultralytics import YOLO

from trayguard.detection import draw_detections, process_image

device = "cpu"  # MPS is slower for YOLO11n — NMS ops bottleneck
model = YOLO("weights/50_pictures_detection.pt")
if device != "cpu":
    model.to(device)
print(f"Model loaded: {model.names}  |  device: {device}")

img_path = "data/cv/50_pictures_auto/yolo/images/val/forcep_1_sample_000002.jpg"
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Could not read image: {img_path}")

result = process_image(model, img)
print(f"Detections: {len(result['detections'])}")
for d in result["detections"]:
    print(f"  {d['class_name']} ({d['confidence']:.2f}): {d['bbox_xyxy']}")
print(
    f"Latency: {result['total_speed_ms']:.1f} ms ({1_000 / result['total_speed_ms']:.1f} fps)"
)

annotated = draw_detections(img, result["detections"])
out_path = "runs/inference/forcep_1_sample_000002.jpg"
cv2.imwrite(out_path, annotated)
print(f"Saved: {out_path}")
