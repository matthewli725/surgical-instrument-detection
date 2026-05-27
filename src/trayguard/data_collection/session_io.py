from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import cv2

from trayguard.data_collection.models import Box, CollectionSession


def create_session(
    output_dir: Path,
    prefix: str,
    image,
    boxes: list[Box],
    class_names: list[str],
    image_ext: str,
) -> CollectionSession:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"{prefix}_{timestamp}"
    session_dir = output_dir / "sessions" / session_id
    session = CollectionSession(
        session_id=session_id,
        session_dir=session_dir,
        class_names=class_names,
        boxes=list(boxes),
        image_width=image.shape[1],
        image_height=image.shape[0],
        image_ext=image_ext,
    )

    session.images_dir.mkdir(parents=True, exist_ok=True)
    session.labels_dir.mkdir(parents=True, exist_ok=True)
    save_image_with_shared_labels(session, image, "reference")
    save_metadata(session)
    return session


def save_image_with_shared_labels(session: CollectionSession, image, stem: str) -> tuple[Path, Path]:
    image_path = session.images_dir / f"{stem}.{session.image_ext}"
    label_path = session.labels_dir / f"{stem}.txt"

    cv2.imwrite(str(image_path), image)
    write_yolo_labels(label_path, session.boxes, session.class_names, session.image_width, session.image_height)

    if image_path.name not in session.saved_images:
        session.saved_images.append(image_path.name)

    return image_path, label_path


def write_yolo_labels(
    label_path: Path,
    boxes: list[Box],
    class_names: list[str],
    image_width: int,
    image_height: int,
) -> None:
    class_to_id = {name: idx for idx, name in enumerate(class_names)}
    label_lines = [
        box.normalized_yolo(image_width=image_width, image_height=image_height, class_id=class_to_id[box.label])
        for box in boxes
    ]
    label_path.write_text("\n".join(label_lines) + ("\n" if label_lines else ""), encoding="utf-8")


def save_metadata(session: CollectionSession) -> None:
    metadata = {
        "session_id": session.session_id,
        "image_width": session.image_width,
        "image_height": session.image_height,
        "image_ext": session.image_ext,
        "class_names": session.class_names,
        "boxes": [box.to_dict() for box in session.boxes],
        "saved_images": session.saved_images,
        "next_variant_index": session.next_variant_index,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    session.metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def rewrite_session_labels(session: CollectionSession) -> None:
    for image_path in sorted(session.images_dir.iterdir()):
        if image_path.is_file():
            label_path = session.labels_dir / f"{image_path.stem}.txt"
            write_yolo_labels(label_path, session.boxes, session.class_names, session.image_width, session.image_height)
