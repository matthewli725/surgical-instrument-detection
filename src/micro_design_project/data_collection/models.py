from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Box:
    label: str
    x1: int
    y1: int
    x2: int
    y2: int

    def normalized_yolo(self, image_width: int, image_height: int, class_id: int) -> str:
        x_min, x_max = sorted((self.x1, self.x2))
        y_min, y_max = sorted((self.y1, self.y2))

        x_center = ((x_min + x_max) / 2) / image_width
        y_center = ((y_min + y_max) / 2) / image_height
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height

        return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

    def to_dict(self) -> dict[str, int | str]:
        return {
            "label": self.label,
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
        }


@dataclass
class CollectionSession:
    session_id: str
    session_dir: Path
    class_names: list[str]
    boxes: list[Box]
    image_width: int
    image_height: int
    image_ext: str
    saved_images: list[str] = field(default_factory=list)
    next_variant_index: int = 1

    @property
    def images_dir(self) -> Path:
        return self.session_dir / "images"

    @property
    def labels_dir(self) -> Path:
        return self.session_dir / "labels"

    @property
    def metadata_path(self) -> Path:
        return self.session_dir / "metadata.json"
