from pathlib import Path
import cv2
from ultralytics import YOLO

MODEL_PATH = "runs/detect/runs/yolo11s_imgsz960_batch16/weights/best.pt"
IMAGE_PATH = "demo/separado90.jpg"
PRED_LABEL_PATH = "demo/separado90.txt"
RESULT_OUT_PATH = "demo/result/demo_test.jpg"
OVERLAY_OUT_PATH = "demo/overlay/demo_test.jpg"
CONF = 0.95
IMGSZ = 960

CLASS_NAMES = [
    "Scalpel n4",
    "Straight Dissection Clamp",
    "Straight Mayo Scissor",
    "Curved Mayo Scissor"
]

def draw_overlap(img, txt_path):
    img_h, img_w = img.shape[:2]

    with open(txt_path, "r") as f:
        annotations = f.readlines()

    for line in annotations:
        parts = line.strip().split()

        cls_id = int(parts[0])
        x_c, y_c, w, h = map(float, parts[1:5])

        x1 = int((x_c - w / 2) * img_w)
        y1 = int((y_c - h / 2) * img_h)
        x2 = int((x_c + w / 2) * img_w)
        y2 = int((y_c + h / 2) * img_h)

        text_pos = (x1, y2)

        class_name = CLASS_NAMES[cls_id]

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(img,f"Actual: {class_name}", text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    
    return img

def main():
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

    overlap = draw_overlap(overlay_bgr, PRED_LABEL_PATH)
    
    cv2.imwrite(RESULT_OUT_PATH, overlay_bgr)
    cv2.imwrite(OVERLAY_OUT_PATH, overlap)
    print('\nLatency (ms):')

    total = 0
    for type, latency in r.speed.items():
        print(f'\t{type}: {latency:.4f}')
        total += latency

    print(f'\nTotal Latency: {total:.4f}ms')

if __name__ == "__main__":
    main()