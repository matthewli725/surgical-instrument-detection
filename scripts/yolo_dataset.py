from pathlib import Path
import random
import shutil

DATASET_ROOT = Path("dataset/Surgical-Dataset")
OUTPUT_ROOT = Path("datasets/dataset_obj_detection")

IMAGES_DIR = DATASET_ROOT / "Images" / "All" / "images"
LABEL_DIR = DATASET_ROOT / "Labels" / "label object names"

TRAIN_LIST = DATASET_ROOT / "Test-Train Groups" / "train-obj_detector.txt"
TEST_LIST = DATASET_ROOT / "Test-Train Groups" / "test-obj_detector.txt"

VAL_RATIO = 0.2
SEED = 42

CLASS_NAMES = [
    "Scalpel n4",
    "Straight Dissection Clamp",
    "Straight Mayo Scissor",
    "Curved Mayo Scissor",
]

random.seed(SEED)


def read_image_names(txt_path: Path):
    """
    Reads lines like:
    /home/roboticslab/darknet/Dataset/images/bisturi216.jpg

    Returns:
    ['bisturi216.jpg', ...]
    """
    image_names = []
    with open(txt_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                image_names.append(Path(line).name)

    return image_names


def make_dirs(base: Path):
    for split in ["train", "val", "test"]:
        (base / "images" / split).mkdir(parents=True, exist_ok=True)
        (base / "labels" / split).mkdir(parents=True, exist_ok=True)

    (base / "split").mkdir(parents=True, exist_ok=True)


def copy_one_sample(image_name: str, split: str):
    stem = Path(image_name).stem

    src_img = IMAGES_DIR / image_name
    src_lbl = LABEL_DIR / f"{stem}.txt"

    dst_img = OUTPUT_ROOT / "images" / split / image_name
    dst_lbl = OUTPUT_ROOT / "labels" / split / f"{stem}.txt"

    if not src_img.exists():
        print(f"[WARNING] Missing image: {src_img}")
        return

    shutil.copy2(src_img, dst_img)

    if src_lbl.exists():
        shutil.copy2(src_lbl, dst_lbl)
    else:
        # empty label file if image has no object
        dst_lbl.touch()
        print(f"[WARNING] Missing label: {src_lbl} -> created empty label file")


def copy_split(image_names, split: str):
    for image_name in image_names:
        copy_one_sample(image_name, split)


def write_yaml():
    yaml_path = OUTPUT_ROOT / "data.yaml"

    lines = [
        f"path: {OUTPUT_ROOT.as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "",
        "names:",
    ]

    for i, name in enumerate(CLASS_NAMES):
        lines.append(f"  {i}: {name}")

    with open(yaml_path, "w") as f:
        f.write("\n".join(lines) + "\n")


def write_rewritten_path_lists(train_names, val_names, test_names):
    """
    Writes txt files with rewritten paths like:
    dataset/images/all/bisturi216.jpg
    """
    def write_list(file_path: Path, names):
        with open(file_path, "w") as f:
            for name in names:
                f.write(f"dataset/images/all/{name}\n")

    write_list(OUTPUT_ROOT / "split_lists" / "train.txt", train_names)
    write_list(OUTPUT_ROOT / "split_lists" / "val.txt", val_names)
    write_list(OUTPUT_ROOT / "split_lists" / "test.txt", test_names)


def main():
    make_dirs(OUTPUT_ROOT)

    train_full = read_image_names(TRAIN_LIST)
    test_images = read_image_names(TEST_LIST)

    random.shuffle(train_full)
    val_count = int(len(train_full) * VAL_RATIO)

    val_images = train_full[:val_count]
    train_images = train_full[val_count:]

    print(f"Total original train images: {len(train_full)}")
    print(f"Train split: {len(train_images)}")
    print(f"Val split: {len(val_images)}")
    print(f"Test split: {len(test_images)}")

    copy_split(train_images, "train")
    copy_split(val_images, "val")
    copy_split(test_images, "test")

    write_rewritten_path_lists(train_images, val_images, test_images)
    write_yaml()

    print("\nDone")


if __name__ == "__main__":
    main()