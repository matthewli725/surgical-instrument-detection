import cv2
from pathlib import Path

IMAGE_DIR = Path("dataset/seed_data")
OUTPUT_VIDEO = "seed_video.mp4"
FPS = 10

images = sorted(IMAGE_DIR.glob("*.jpg"))

frame = cv2.imread(str(images[0]))
height, width, _ = frame.shape

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (width, height))

for img_path in images:
    frame = cv2.imread(str(img_path))
    video.write(frame)

video.release()