import torch
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
print(torch.cuda.is_available())