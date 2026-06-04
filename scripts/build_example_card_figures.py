"""Render example TrayGuard study card front and back as PNG figures.

Usage:
    python scripts/build_example_card_figures.py

Reads:  config/tray_modules/fgvc12_combined_tray_v1.json
        outputs/cards/fgvc12_combined_tray_v1/markers/aruco_053_fgvc12_major_clamp_kelly_8in_fgvc12.png
        data/instruments/fgvc12_major_tray_v1/fgvc12_major_clamp_kelly_8in_view_a.jpg
Writes: final_paper/source/figures/card_front_example.png
        final_paper/source/figures/card_back_example.png
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "config" / "tray_modules" / "fgvc12_combined_tray_v1.json"
MARKER_PATH = (
    REPO_ROOT
    / "outputs"
    / "cards"
    / "fgvc12_combined_tray_v1"
    / "markers"
    / "aruco_053_fgvc12_major_clamp_kelly_8in_fgvc12.png"
)
PHOTO_PATH = (
    REPO_ROOT
    / "data"
    / "instruments"
    / "fgvc12_major_tray_v1"
    / "fgvc12_major_clamp_kelly_8in_view_a.jpg"
)
OUT_DIR = REPO_ROOT / "final_paper" / "source" / "figures"
FRONT_OUT = OUT_DIR / "card_front_example.png"
BACK_OUT = OUT_DIR / "card_back_example.png"


CARD_SIZE = (1200, 900)
CARD_BG = (244, 244, 240)
CARD_BORDER = (34, 34, 34)
TEXT_PRIMARY = (17, 17, 17)
TEXT_MUTED = (85, 85, 85)
ACCENT = (60, 90, 140)


def _load_fonts() -> dict[str, ImageFont.FreeTypeFont]:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    font_path = next((p for p in candidates if Path(p).exists()), None)
    if font_path is None:
        font_path = ImageFont.load_default()
        base = ImageFont.load_default()
        return {
            "title": base,
            "h2": base,
            "body": base,
            "small": base,
            "tiny": base,
        }
    return {
        "title": ImageFont.truetype(font_path, 56),
        "h2": ImageFont.truetype(font_path, 30),
        "body": ImageFont.truetype(font_path, 26),
        "small": ImageFont.truetype(font_path, 22),
        "tiny": ImageFont.truetype(font_path, 18),
    }


def _draw_card_frame(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [(0, 0), (canvas.width - 1, canvas.height - 1)],
        outline=CARD_BORDER,
        width=4,
    )


def _text_centered(draw: ImageDraw.ImageDraw, text: str, y: int,
                    font: ImageFont.ImageFont, fill: tuple[int, int, int],
                    canvas_width: int) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (canvas_width - text_w) // 2
    draw.text((x, y), text, font=font, fill=fill)


def _wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont,
                max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def _standardize_photo(source: Path, target_max: tuple[int, int]) -> Image.Image:
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    image.thumbnail(target_max, Image.Resampling.LANCZOS)
    return image


def _paste_marker(canvas: Image.Image, marker: Image.Image) -> None:
    border = 10
    framed = Image.new("RGB", (marker.width + border * 2, marker.height + border * 2), (255, 255, 255))
    framed.paste(marker, (border, border))
    x = canvas.width - framed.width - 16
    y = 16
    canvas.paste(framed, (x, y))


def render_front(marker_path: Path, photo_path: Path) -> Image.Image:
    canvas = Image.new("RGB", CARD_SIZE, CARD_BG)
    _draw_card_frame(canvas)

    photo = _standardize_photo(photo_path, (1080, 780))
    px = (canvas.width - photo.width) // 2
    py = (canvas.height - photo.height) // 2
    canvas.paste(photo, (px, py))

    marker = Image.open(marker_path).convert("RGB")
    marker_target = 200
    marker = marker.resize((marker_target, marker_target), Image.Resampling.NEAREST)
    _paste_marker(canvas, marker)

    draw = ImageDraw.Draw(canvas)
    fonts = _load_fonts()
    _text_centered(draw, "Card front · assessment mode · no text", canvas.height - 50,
                   fonts["tiny"], TEXT_MUTED, canvas.width)

    return canvas


def render_back(instrument: dict) -> Image.Image:
    canvas = Image.new("RGB", CARD_SIZE, CARD_BG)
    _draw_card_frame(canvas)
    draw = ImageDraw.Draw(canvas)
    fonts = _load_fonts()

    pad = 70
    text_w = canvas.width - 2 * pad

    display_name = instrument["display_name"]
    family = instrument["family"]
    module_aliases = instrument.get("aliases", [])
    aliases = ", ".join(a for a in module_aliases if a.startswith("CLAMP"))
    extra_aliases = [a for a in module_aliases if not a.startswith("CLAMP")]
    attribution = instrument.get("image_refs", [{}])[0].get("attribution", "Pending source")

    # ── Header ──
    draw.text((pad, pad), display_name, font=fonts["title"], fill=TEXT_PRIMARY)
    name_bbox = draw.textbbox((pad, pad), display_name, font=fonts["title"])
    title_bottom = name_bbox[3] + 16

    sub_text = f"Family: {family}    ·    Catalog: {aliases}"
    wrapped_sub = _wrap_lines(draw, sub_text, fonts["body"], text_w)
    sub_y = title_bottom
    for line in wrapped_sub:
        draw.text((pad, sub_y), line, font=fonts["body"], fill=TEXT_MUTED)
        sub_y += 34

    # ── Key identification features ──
    id_features = [
        "Curved jaws with ring handles",
        "Transverse serrations on distal half of jaws",
        "8-inch overall length",
    ]
    features_y = sub_y + 24
    draw.text((pad, features_y), "Key identification features", font=fonts["h2"], fill=ACCENT)
    bullet_y = features_y + 50
    for feature in id_features:
        draw.text((pad + 8, bullet_y), "•", font=fonts["body"], fill=TEXT_PRIMARY)
        wrapped = _wrap_lines(draw, feature, fonts["body"], text_w - 32)
        for i, line in enumerate(wrapped):
            draw.text((pad + 34, bullet_y + i * 32), line, font=fonts["body"], fill=TEXT_PRIMARY)
        bullet_y += 32 * len(wrapped) + 10

    # ── Common lookalikes ──
    lookalikes = [
        "Crile clamp — serrations run full jaw (Kelly: distal half only)",
        "Kocher clamp — single tooth at tip (Kelly: no tooth)",
        'Kelly 6" / Kelly 12" — same jaw shape, different length',
    ]
    lookalikes_y = bullet_y + 20
    draw.text((pad, lookalikes_y), "Common lookalikes", font=fonts["h2"], fill=ACCENT)
    bullet_y2 = lookalikes_y + 50
    for lookalike in lookalikes:
        draw.text((pad + 8, bullet_y2), "•", font=fonts["body"], fill=TEXT_PRIMARY)
        wrapped = _wrap_lines(draw, lookalike, fonts["body"], text_w - 32)
        for i, line in enumerate(wrapped):
            draw.text((pad + 34, bullet_y2 + i * 32), line, font=fonts["body"], fill=TEXT_PRIMARY)
        bullet_y2 += 32 * len(wrapped) + 10

    # ── Extra aliases ──
    if extra_aliases:
        extra_y = bullet_y2 + 16
        extra_text = f"Also known as: {', '.join(extra_aliases)}"
        draw.text((pad, extra_y), extra_text, font=fonts["small"], fill=TEXT_MUTED)

    footer_y = canvas.height - 36
    draw.text((pad, footer_y), f"Source: {attribution}", font=fonts["tiny"], fill=TEXT_MUTED)

    return canvas


def main() -> None:
    if not MODULE_PATH.exists():
        raise SystemExit(f"Module JSON not found: {MODULE_PATH}")
    if not MARKER_PATH.exists():
        raise SystemExit(f"Marker PNG not found: {MARKER_PATH}")
    if not PHOTO_PATH.exists():
        raise SystemExit(f"Photo not found: {PHOTO_PATH}")

    module = json.loads(MODULE_PATH.read_text(encoding="utf-8"))
    instrument = next(
        inst for inst in module["instruments"]
        if inst["id"] == "fgvc12_major_clamp_kelly_8in"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    front = render_front(MARKER_PATH, PHOTO_PATH)
    front.save(FRONT_OUT, optimize=True)
    print(f"  wrote {FRONT_OUT}")

    back = render_back(instrument)
    back.save(BACK_OUT, optimize=True)
    print(f"  wrote {BACK_OUT}")


if __name__ == "__main__":
    main()
