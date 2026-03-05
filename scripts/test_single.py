from pathlib import Path
import cv2
from ultralytics import YOLO

MODEL_PATH = "runs/segment/general/weights/best.pt"
IMAGE_PATH = "dataset/overlap/4938_jpg.rf.821b3b0159f1445a436faf098c033271.jpg"
OUT_PATH = "test_pred_overlay.jpg"
CONF = 0.25
IMGSZ = 1024

model = YOLO(MODEL_PATH)

results = model.predict(
    source=IMAGE_PATH,
    imgsz=IMGSZ,
    conf=CONF,
    save=False,
    verbose=False
)

r = results[0]

names = model.names
if r.boxes is not None and len(r.boxes) > 0:
    for cls, conf in zip(r.boxes.cls.tolist(), r.boxes.conf.tolist()):
        print(f"{names[int(cls)]}: {conf:.3f}")
else:
    print("No detections.")

overlay_bgr = r.plot()

cv2.imwrite(OUT_PATH, overlay_bgr)
print(f"Saved overlay to: {Path(OUT_PATH).resolve()}")