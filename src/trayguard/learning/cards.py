from __future__ import annotations

import html
import hashlib
import re
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

from trayguard.learning.aruco import generate_marker_png
from trayguard.learning.models import Instrument, MarkerCard, TrayModule


FLASHCARD_IMAGE_SIZE = (900, 620)
FLASHCARD_IMAGE_BACKGROUND = (244, 244, 240)


def _content_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    rgb = image.convert("RGB")
    corner_samples = [
        rgb.getpixel((0, 0)),
        rgb.getpixel((rgb.width - 1, 0)),
        rgb.getpixel((0, rgb.height - 1)),
        rgb.getpixel((rgb.width - 1, rgb.height - 1)),
    ]
    background = tuple(sorted(channel)[len(channel) // 2] for channel in zip(*corner_samples))
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, background)).convert("L")
    mask = diff.point(lambda value: 255 if value > 18 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        return (0, 0, rgb.width, rgb.height)

    pad_x = max(8, int((bbox[2] - bbox[0]) * 0.08))
    pad_y = max(8, int((bbox[3] - bbox[1]) * 0.08))
    return (
        max(0, bbox[0] - pad_x),
        max(0, bbox[1] - pad_y),
        min(rgb.width, bbox[2] + pad_x),
        min(rgb.height, bbox[3] + pad_y),
    )


def _standardize_flashcard_image(source: Path, target: Path) -> None:
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    cropped = image.crop(_content_bbox(image))
    cropped.thumbnail((FLASHCARD_IMAGE_SIZE[0] - 80, FLASHCARD_IMAGE_SIZE[1] - 80), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", FLASHCARD_IMAGE_SIZE, FLASHCARD_IMAGE_BACKGROUND)
    x = (canvas.width - cropped.width) // 2
    y = (canvas.height - cropped.height) // 2
    canvas.paste(cropped, (x, y))
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, quality=92)


def _reference_length(instrument: Instrument) -> str:
    text = f"{instrument.display_name} {' '.join(instrument.aliases)}"
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches)\b", text, flags=re.IGNORECASE)
    if match:
        return f"{match.group(1)} in"
    return ""


def _copy_flashcard_image(instrument: Instrument, output_dir: Path) -> tuple[str, str]:
    for ref in instrument.image_refs:
        if not ref.get("approved_for_study"):
            continue
        source = Path(str(ref.get("path", "")))
        if not source.exists():
            continue
        image_dir = output_dir / "images"
        image_dir.mkdir(parents=True, exist_ok=True)
        safe_id = instrument.id[:70]
        digest = hashlib.sha1(instrument.id.encode("utf-8")).hexdigest()[:10]
        if source.suffix.lower() == ".svg":
            target = image_dir / f"{safe_id}_{digest}{source.suffix.lower()}"
            shutil.copy2(source, target)
        else:
            target = image_dir / f"{safe_id}_{digest}_standardized.jpg"
            _standardize_flashcard_image(source, target)
        return f"images/{target.name}", str(ref.get("attribution", ""))
    return "", ""


def _marker_by_instrument(marker_cards: list[MarkerCard]) -> dict[str, int]:
    markers: dict[str, int] = {}
    for card in marker_cards:
        markers.setdefault(card.instrument_id, card.marker_id)
    return markers


def _features(instrument: Instrument) -> str:
    if not instrument.distinguishing_features:
        return "<li>Feature notes pending instructor verification.</li>"
    return "".join(f"<li>{html.escape(feature)}</li>" for feature in instrument.distinguishing_features)


def _flashcard_html(
    instruments: dict[str, Instrument],
    required_quantities: dict[str, int],
    marker_cards: list[MarkerCard],
    output_dir: Path,
) -> str:
    cards: list[str] = []
    marker_ids = _marker_by_instrument(marker_cards)
    for instrument in instruments.values():
        required_quantity = required_quantities.get(instrument.id)
        count_label = str(required_quantity) if required_quantity is not None else "Reference card"
        image_src, attribution = _copy_flashcard_image(instrument, output_dir)
        reference_length = _reference_length(instrument)
        marker_id = marker_ids.get(instrument.id)
        marker_src = ""
        if marker_id is not None:
            marker_path = output_dir / f"aruco_{marker_id:03d}_{instrument.id}_flashcard.png"
            generate_marker_png(marker_id, marker_path)
            marker_src = marker_path.name
        image_html = (
            f"<img src='{html.escape(image_src)}' alt='{html.escape(instrument.display_name)}'>"
            if image_src
            else "<div class='image-placeholder'>Image pending</div>"
        )
        marker_html = (
            f"<img class='marker-small' src='{html.escape(marker_src)}' alt='ArUco marker {marker_id}'>"
            if marker_src
            else ""
        )
        cards.append(
            "<section class='flashcard'>"
            "<div class='front'>"
            f"{image_html}"
            f"{marker_html}"
            "</div>"
            "<div class='back'>"
            f"<h2>{html.escape(instrument.display_name)}</h2>"
            f"<p><strong>Family:</strong> {html.escape(instrument.family)}</p>"
            f"<p><strong>Tray count:</strong> {html.escape(count_label)}</p>"
            f"<p><strong>Reference length:</strong> {html.escape(reference_length or 'Pending verification')}</p>"
            f"<p><strong>Aliases:</strong> {html.escape(', '.join(instrument.aliases) or '-')}</p>"
            f"<ul>{_features(instrument)}</ul>"
            f"<p class='source'><strong>Image/license:</strong> {html.escape(attribution or 'Pending source')}</p>"
            "</div>"
            "</section>"
        )
    return "\n".join(cards)


def _write_flashcard_deck(
    title: str,
    instruments: dict[str, Instrument],
    required_quantities: dict[str, int],
    marker_cards: list[MarkerCard],
    output_dir: Path,
) -> Path:
    flashcard_path = output_dir / "flashcards.html"
    flashcard_path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html><head><meta charset='utf-8'><title>TrayGuard Flashcards</title>",
                "<style>",
                "body{font-family:Arial,sans-serif;margin:24px;color:#111}",
                ".deck{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}",
                ".flashcard{border:1px solid #222;display:grid;grid-template-columns:1fr 1fr;min-height:260px;break-inside:avoid}",
                ".front,.back{padding:14px}.front{border-right:1px solid #ddd;display:grid;grid-template-rows:1fr auto;gap:8px;align-items:center}",
                "img{max-width:100%;height:190px;object-fit:contain;background:#f7f7f7}.marker-small{height:78px;justify-self:end;background:#fff}",
                ".image-placeholder{height:190px;display:flex;align-items:center;justify-content:center;background:#f7f7f7;color:#555;border:1px dashed #999}",
                "h1{margin:0 0 16px}h2{font-size:18px;margin:0 0 10px}p{font-size:13px;margin:6px 0}li{font-size:13px;margin:4px 0}.source{font-size:10px;color:#555}",
                "@media print{body{margin:10mm}.deck{gap:10px}.flashcard{page-break-inside:avoid}}",
                "</style></head><body>",
                f"<h1>{html.escape(title)} Flashcards</h1>",
                "<div class='deck'>",
                _flashcard_html(instruments, required_quantities, marker_cards, output_dir),
                "</div></body></html>",
            ]
        ),
        encoding="utf-8",
    )
    return flashcard_path


def print_cards(module: TrayModule, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    rows: list[str] = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><title>TrayGuard Cards</title>",
        "<style>body{font-family:Arial,sans-serif}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.card{border:1px solid #222;padding:16px;break-inside:avoid}.marker{width:180px;height:180px}.meta{font-size:12px;color:#555}</style>",
        "</head><body><h1>TrayGuard Neutral ArUco Cards</h1><div class='grid'>",
    ]
    for card in module.marker_cards:
        marker_path = output_dir / f"aruco_{card.marker_id:03d}_{card.card_id}.png"
        generate_marker_png(card.marker_id, marker_path)
        paths.append(marker_path)
        rows.append(
            "<section class='card'>"
            f"<img class='marker' src='{marker_path.name}' alt='ArUco marker {card.marker_id}'>"
            f"<p class='meta'>Card {card.card_id} | Marker {card.marker_id}</p>"
            "</section>"
        )
    rows.append("</div></body></html>")
    index_path = output_dir / "index.html"
    index_path.write_text("\n".join(rows), encoding="utf-8")
    paths.append(index_path)
    flashcard_path = _write_flashcard_deck(
        module.name,
        module.instruments,
        {instrument_id: item.quantity for instrument_id, item in module.required_items.items()},
        module.marker_cards,
        output_dir,
    )
    paths.append(flashcard_path)
    return paths


def print_instrument_catalog_cards(
    title: str,
    instruments: dict[str, Instrument],
    output_dir: Path,
    *,
    marker_start: int = 1000,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    marker_cards = [
        MarkerCard(marker_id=marker_start + index, instrument_id=instrument.id, card_id=f"{instrument.id}_catalog")
        for index, instrument in enumerate(instruments.values())
    ]
    return [_write_flashcard_deck(title, instruments, {}, marker_cards, output_dir)]
