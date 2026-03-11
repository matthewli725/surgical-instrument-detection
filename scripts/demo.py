from pathlib import Path
import cv2
from ultralytics import YOLO

MODEL_PATH = "runs/detect/runs/yolo11s_imgsz960_batch16/weights/best.pt"

IMAGE_DIR = Path("demo/images")
LABEL_DIR = Path("demo/labels")

RESULT_DIR = Path("demo/result")
OVERLAY_DIR = Path("demo/overlay")

CONF = 0.75
IMGSZ = 960

RESULT_DIR.mkdir(parents=True, exist_ok=True)
OVERLAY_DIR.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = [
    "Scalpel n4",
    "Straight Dissection Clamp",
    "Straight Mayo Scissor",
    "Curved Mayo Scissor"
]

def draw_overlap(img: cv2.Mat, txt_path: Path) -> cv2.Mat:
    """Draws ground truth boxes from label file on the image.
    Args:
        img: The image to draw on (BGR format).
        txt_path: Path to the label file containing annotations.
    Returns:
        Image with ground truth boxes drawn.
    """
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

def process_image(model: YOLO, image_path: Path) -> None:

    # Assumes label file has same name as image but with .txt extension
    label_path = LABEL_DIR / f"{image_path.stem}.txt"
    result_out_path = RESULT_DIR / image_path.name
    overlay_out_path = OVERLAY_DIR / image_path.name

    # Run inference
    results = model.predict(
        source=str(image_path),
        imgsz=IMGSZ,
        conf=CONF,
        save=False,
        verbose=False
    )
    r = results[0]

    # Print detected classes and confidences
    names = model.names
    if r.boxes is not None and len(r.boxes) > 0:
        for cls, conf in zip(r.boxes.cls.tolist(), r.boxes.conf.tolist()):
            print(f"  {names[int(cls)]}: {conf:.3f}")
    else:
        print("  No detections.")

    # Draw predictions on image
    img_with_preds = r.plot()
    cv2.imwrite(str(result_out_path), img_with_preds)

    # Draw ground truth boxes and save overlay
    overlay_with_gt = draw_overlap(img_with_preds, label_path)
    cv2.imwrite(str(overlay_out_path), overlay_with_gt)

    # Print latency information
    print("  Latency (ms):")
    total = 0
    for stage, latency in r.speed.items():
        print(f"    {stage}: {latency:.4f}")
        total += latency
    print(f"  Total: {total:.4f} ms")

def main():
    # Load model
    model = YOLO(MODEL_PATH)
    
    # Get image paths
    image_paths = sorted(
        [p for p in IMAGE_DIR.iterdir()]
    )

    if not image_paths:
        print(f"No images found in {IMAGE_DIR}")
        return

    # Process each image
    for image_path in image_paths:
        process_image(model, image_path)

if __name__ == "__main__":
    main()