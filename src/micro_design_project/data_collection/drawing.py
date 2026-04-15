from __future__ import annotations

import cv2

from micro_design_project.data_collection.models import Box


def draw_status_lines(image, lines: list[str], top: int = 25) -> None:
    for i, line in enumerate(lines):
        y = top + (i * 25)
        cv2.putText(image, line, (12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(image, line, (12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)


def draw_box(image, box: Box, color: tuple[int, int, int]) -> None:
    x1, x2 = sorted((box.x1, box.x2))
    y1, y2 = sorted((box.y1, box.y2))
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    if box.label:
        cv2.putText(image, box.label, (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2, cv2.LINE_AA)
