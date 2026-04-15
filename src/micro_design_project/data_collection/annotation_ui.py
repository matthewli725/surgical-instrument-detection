from __future__ import annotations

import cv2

from micro_design_project.data_collection.drawing import draw_box, draw_status_lines
from micro_design_project.data_collection.models import Box


class ImageAnnotator:
    def __init__(
        self,
        image,
        class_names: list[str],
        boxes: list[Box] | None = None,
        min_box_size: int = 5,
    ) -> None:
        self.image = image
        self.class_names = class_names
        self.min_box_size = min_box_size
        self.boxes = list(boxes or [])
        self.drawing = False
        self.start: tuple[int, int] | None = None
        self.current: tuple[int, int] | None = None
        self.pending_box: tuple[int, int, int, int] | None = None
        self.label_buffer = ""
        self.status_message = ""
        self.confirm_new_label: str | None = None
        self.completion_query = ""
        self.completion_index = -1

    def annotate(self, window_name: str) -> list[Box] | None:
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self._handle_mouse)

        while True:
            cv2.imshow(window_name, self._render())
            key = cv2.waitKey(20) & 0xFF

            if self.pending_box is not None:
                self._handle_label_key(key)
                continue

            if key == ord("s"):
                cv2.destroyWindow(window_name)
                return self.boxes
            if key == ord("u"):
                if self.boxes:
                    removed = self.boxes.pop()
                    self.status_message = f"Removed box labeled '{removed.label}'"
            if key == ord("r"):
                cv2.destroyWindow(window_name)
                return None
            if key == ord("q"):
                cv2.destroyWindow(window_name)
                raise KeyboardInterrupt

    def _handle_mouse(self, event: int, x: int, y: int, _flags: int, _param: object) -> None:
        if self.pending_box is not None:
            return

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start = (x, y)
            self.current = (x, y)
            return

        if event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.current = (x, y)
            return

        if event == cv2.EVENT_LBUTTONUP and self.drawing and self.start is not None:
            self.drawing = False
            self.current = (x, y)
            x1, y1 = self.start
            x2, y2 = x, y

            if abs(x2 - x1) < self.min_box_size or abs(y2 - y1) < self.min_box_size:
                self.status_message = "Ignored tiny box. Drag a larger region."
                self.start = None
                self.current = None
                return

            self.pending_box = (x1, y1, x2, y2)
            self.label_buffer = ""
            self.status_message = ""
            self.confirm_new_label = None
            self.completion_query = ""
            self.completion_index = -1
            self.start = None
            self.current = None

    def _handle_label_key(self, key: int) -> None:
        if key == 255:
            return

        if self.confirm_new_label is not None:
            self._handle_new_label_confirmation(key)
            return

        if key in (10, 13):
            self._accept_pending_label()
            return

        if key == 27:
            self.pending_box = None
            self.label_buffer = ""
            return

        if key == 9:
            self._autocomplete_label()
            return

        if key in (8, 127):
            self.label_buffer = self.label_buffer[:-1]
            self.completion_query = ""
            self.completion_index = -1
            return

        if 32 <= key <= 126:
            self.label_buffer += chr(key)
            self.completion_query = ""
            self.completion_index = -1

    def _handle_new_label_confirmation(self, key: int) -> None:
        if key in (10, 13):
            self._add_pending_box(self.confirm_new_label)
            self.confirm_new_label = None
            return

        if key == 27:
            self.label_buffer = self.confirm_new_label
            self.confirm_new_label = None
            self.status_message = "New class canceled. Edit label or press ENTER again."

    def _accept_pending_label(self) -> None:
        if self.pending_box is None:
            return

        raw_label = self.label_buffer.strip()
        if not raw_label:
            self.pending_box = None
            self.label_buffer = ""
            return

        label = raw_label
        if raw_label.isdigit():
            class_id = int(raw_label)
            if 0 <= class_id < len(self.class_names):
                label = self.class_names[class_id]
            else:
                self.status_message = f"Invalid class {class_id}"
                return

        if label not in self.class_names:
            self.confirm_new_label = label
            self.status_message = f"New class '{label}'. ENTER adds it, ESC edits."
            return

        self._add_pending_box(label)

    def _add_pending_box(self, label: str) -> None:
        if self.pending_box is None:
            return

        if label not in self.class_names:
            self.class_names.append(label)
            self.status_message = f"Added new class: {label}"
        else:
            self.status_message = f"Added box: {label}"

        x1, y1, x2, y2 = self.pending_box
        self.boxes.append(Box(label=label, x1=x1, y1=y1, x2=x2, y2=y2))
        self.pending_box = None
        self.label_buffer = ""
        self.confirm_new_label = None
        self.completion_query = ""
        self.completion_index = -1

    def _autocomplete_label(self) -> None:
        query = self.completion_query or self.label_buffer.strip().lower()
        if not query:
            return

        matches = [name for name in self.class_names if query in name.lower()]
        if not matches:
            self.status_message = "No matching class."
            return

        self.completion_query = query
        self.completion_index = (self.completion_index + 1) % len(matches)
        self.label_buffer = matches[self.completion_index]
        self.status_message = f"Autocomplete {self.completion_index + 1}/{len(matches)}"

    def _render(self):
        rendered = self.image.copy()

        for box in self.boxes:
            draw_box(rendered, box, color=(0, 255, 0))

        if self.drawing and self.start is not None and self.current is not None:
            preview_box = Box(label="", x1=self.start[0], y1=self.start[1], x2=self.current[0], y2=self.current[1])
            draw_box(rendered, preview_box, color=(0, 255, 255))

        if self.pending_box is not None:
            x1, y1, x2, y2 = self.pending_box
            draw_box(rendered, Box(label="", x1=x1, y1=y1, x2=x2, y2=y2), color=(0, 255, 255))
            self._draw_label_prompt(rendered)

        help_lines = [
            "Annotate setup: draw boxes, then type label in this window",
            "TAB autocomplete | s lock setup | u undo | r retake | q quit",
        ]
        if self.status_message:
            help_lines.append(self.status_message)

        draw_status_lines(rendered, help_lines, top=25)
        return rendered

    def _draw_label_prompt(self, image) -> None:
        image_height, image_width = image.shape[:2]
        panel_height = min(235, image_height - 20)
        panel_width = min(760, image_width - 20)
        left = 10
        top = image_height - panel_height - 10

        overlay = image.copy()
        cv2.rectangle(overlay, (left, top), (left + panel_width, top + panel_height), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.78, image, 0.22, 0, image)
        cv2.rectangle(image, (left, top), (left + panel_width, top + panel_height), (255, 255, 255), 1)

        lines = [
            "Type label or class number, ENTER accepts, TAB autocompletes",
            "ESC discards this box | Backspace edits",
            f"Label: {self.label_buffer}_",
        ]

        if self.confirm_new_label is not None:
            lines.append(f"New class: {self.confirm_new_label}")
            lines.append("ENTER adds class | ESC returns to editing")
        else:
            lines.extend(self._class_suggestions())

        for idx, line in enumerate(lines[:7]):
            y = top + 28 + (idx * 31)
            cv2.putText(image, line, (left + 16, y), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 2, cv2.LINE_AA)

    def _class_suggestions(self) -> list[str]:
        query = self.label_buffer.strip().lower()
        if query:
            matches = [(idx, name) for idx, name in enumerate(self.class_names) if query in name.lower()]
        else:
            matches = list(enumerate(self.class_names))

        visible = [f"{idx}: {name}" for idx, name in matches[:5]]
        if len(matches) > 5:
            visible.append(f"... {len(matches) - 5} more matches")

        return visible or ["No matches. ENTER proposes a new class."]
