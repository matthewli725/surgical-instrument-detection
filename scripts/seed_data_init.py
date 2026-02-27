import shutil
from pathlib import Path

SOURCE_IMAGES_DIR = Path("dataset/overlap")
DEST_IMAGES_DIR = Path("dataset/seed_data")
NUM_IMAGES = 100

DEST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

images = sorted(SOURCE_IMAGES_DIR.glob("*.jpg"))

selected_images = images[:NUM_IMAGES]

for img_path in selected_images:
    shutil.copy2(img_path, DEST_IMAGES_DIR / img_path.name)