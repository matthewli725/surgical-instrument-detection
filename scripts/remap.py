from pathlib import Path

DATASET_ROOT = Path("seed_data")
SPLITS = ["train", "val"]

# coarse class order for YOLO:
# 0 scissors, 1 clamp, 2 forceps, 3 scalpel, 4 syringe
DETAILED_ID_TO_COARSE_ID = {
    0: 0,  # Episiotomy Scissors -> scissors
    3: 0,  # Mayo Scissors -> scissors
    5: 0,  # Stitch Scissors -> scissors
    2: 1,  # Hemostat -> clamp
    1: 2,  # Forceps -> forceps
    4: 3,  # Scalpel -> scalpel
    6: 4,  # Syringe -> syringe
}

OUT_ROOT = Path("seed_data_coarse")

def remap_split(split: str):
    in_lbl = DATASET_ROOT / "labels" / split
    out_lbl = OUT_ROOT / "labels" / split
    out_lbl.mkdir(parents=True, exist_ok=True)

    for txt in in_lbl.glob("*.txt"):
        lines = txt.read_text().strip().splitlines()
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            old_id = int(float(parts[0]))
            if old_id not in DETAILED_ID_TO_COARSE_ID:
                continue
            parts[0] = str(DETAILED_ID_TO_COARSE_ID[old_id])
            new_lines.append(" ".join(parts))
        (out_lbl / txt.name).write_text("\n".join(new_lines) + ("\n" if new_lines else ""))

def copy_images():
    for split in SPLITS:
        src = DATASET_ROOT / "images" / split
        dst = OUT_ROOT / "images" / split
        dst.mkdir(parents=True, exist_ok=True)
        for img in src.glob("*.jpg"):
            (dst / img.name).write_bytes(img.read_bytes())

def write_yaml():
    yaml = OUT_ROOT / "data.yaml"
    yaml.write_text(
        f"""path: {OUT_ROOT.as_posix()}
train: images/train
val: images/val

names:
  0: scissors
  1: clamp
  2: forceps
  3: scalpel
  4: syringe
"""
    )

if __name__ == "__main__":
    copy_images()
    for s in SPLITS:
        remap_split(s)
    write_yaml()