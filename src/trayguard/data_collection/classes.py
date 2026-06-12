from __future__ import annotations

from pathlib import Path

from trayguard.learning.module import load_tray_module

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TRAY_MODULE_PATH = PROJECT_ROOT / "config" / "tray_modules" / "fgvc12_major_focused_v1.json"


def module_class_names(module_path: Path = DEFAULT_TRAY_MODULE_PATH) -> list[str]:
    module = load_tray_module(module_path)
    return [instrument.display_name for instrument in module.instruments.values()]


DEFAULT_CLASSES = module_class_names()


def load_class_names(classes_path: Path) -> list[str]:
    if classes_path.exists():
        class_names = [line.strip() for line in classes_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if class_names:
            return class_names

    return DEFAULT_CLASSES.copy()


def write_class_names(classes_path: Path, class_names: list[str]) -> None:
    classes_path.parent.mkdir(parents=True, exist_ok=True)
    classes_path.write_text("\n".join(class_names) + "\n", encoding="utf-8")
