from __future__ import annotations

from pathlib import Path


DEFAULT_CLASSES = [
    "Scalpel n4",
    "Straight Dissection Clamp",
    "Straight Mayo Scissor",
    "Curved Mayo Scissor",
]


def load_class_names(classes_path: Path) -> list[str]:
    if classes_path.exists():
        class_names = [line.strip() for line in classes_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if class_names:
            return class_names

    return DEFAULT_CLASSES.copy()


def write_class_names(classes_path: Path, class_names: list[str]) -> None:
    classes_path.parent.mkdir(parents=True, exist_ok=True)
    classes_path.write_text("\n".join(class_names) + "\n", encoding="utf-8")
