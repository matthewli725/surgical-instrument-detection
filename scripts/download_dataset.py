from pathlib import Path
import random
import shutil
import kagglehub

N = 20

# Download dataset
dataset_path = Path(kagglehub.dataset_download("dilavado/labeled-surgical-tools"))
print("Dataset downloaded to:", dataset_path)

# Source directories inside dataset
SRC_IMAGE_DIR = dataset_path / "Surgical-Dataset/Images/All/images"
SRC_LABEL_DIR = dataset_path / "Surgical-Dataset/Labels/label object names"

# Repo directories (relative to repo root)
BASE_DIR = Path(__file__).resolve().parents[1]

DST_IMAGE_DIR = BASE_DIR / "demo/images"
DST_LABEL_DIR = BASE_DIR / "demo/labels"

DST_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
DST_LABEL_DIR.mkdir(parents=True, exist_ok=True)

VALID_EXTS = {".jpg", ".jpeg", ".png"}

images = [p for p in SRC_IMAGE_DIR.iterdir() if p.suffix.lower() in VALID_EXTS]

selected = random.sample(images, N)
copied = 0

for img_path in selected:
    label_path = SRC_LABEL_DIR / f"{img_path.stem}.txt"

    if not label_path.exists():
        print(f"Skipping {img_path.name}, missing label")
        continue

    shutil.copy2(img_path, DST_IMAGE_DIR / img_path.name)
    shutil.copy2(label_path, DST_LABEL_DIR / label_path.name)

    copied += 1

print(f"Copied {copied} image-label pairs to demo/")