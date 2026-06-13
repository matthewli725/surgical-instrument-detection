from __future__ import annotations

import html
import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

from trayguard.learning.aruco import generate_marker_png
from trayguard.learning.models import Instrument, MarkerCard, TrayModule


FLASHCARD_IMAGE_SIZE = (1200, 900)
FLASHCARD_IMAGE_BACKGROUND = (244, 244, 240)
FLASHCARD_MARKER_SIZE = 190
FLASHCARD_MARKER_MARGIN = 24


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


def _emptiest_marker_position(canvas: Image.Image, marker_size: int) -> tuple[int, int]:
    rgb = canvas.convert("RGB")
    background = Image.new("RGB", rgb.size, FLASHCARD_IMAGE_BACKGROUND)
    diff = ImageChops.difference(rgb, background).convert("L")
    margin = FLASHCARD_MARKER_MARGIN
    candidates = [
        (margin, margin),
        (rgb.width - marker_size - margin, margin),
        (margin, rgb.height - marker_size - margin),
        (rgb.width - marker_size - margin, rgb.height - marker_size - margin),
    ]
    scores = []
    for x, y in candidates:
        crop = diff.crop((x, y, x + marker_size, y + marker_size))
        scores.append((sum(crop.getdata()), x, y))
    _, x, y = min(scores)
    return x, y


def _paste_marker(canvas: Image.Image, marker_path: Path) -> None:
    marker = Image.open(marker_path).convert("RGB").resize(
        (FLASHCARD_MARKER_SIZE, FLASHCARD_MARKER_SIZE),
        Image.Resampling.NEAREST,
    )
    border = 10
    framed = Image.new(
        "RGB",
        (FLASHCARD_MARKER_SIZE + border * 2, FLASHCARD_MARKER_SIZE + border * 2),
        "white",
    )
    framed.paste(marker, (border, border))
    x, y = _emptiest_marker_position(canvas, framed.width)
    canvas.paste(framed, (x, y))


def _standardize_flashcard_image(source: Path, target: Path, marker_path: Path | None = None) -> None:
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    cropped = image.crop(_content_bbox(image))
    cropped.thumbnail((FLASHCARD_IMAGE_SIZE[0] - 48, FLASHCARD_IMAGE_SIZE[1] - 48), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", FLASHCARD_IMAGE_SIZE, FLASHCARD_IMAGE_BACKGROUND)
    x = (canvas.width - cropped.width) // 2
    y = (canvas.height - cropped.height) // 2
    canvas.paste(cropped, (x, y))
    if marker_path is not None:
        _paste_marker(canvas, marker_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, quality=92)


def _copy_flashcard_image(instrument: Instrument, output_dir: Path, marker_path: Path | None = None) -> tuple[str, str]:
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
            _standardize_flashcard_image(source, target, marker_path)
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


def _lookalike_lines(instrument_id: str, instruments: dict[str, Instrument], lookalikes: list[LookalikePair]) -> str:
    lines: list[str] = []
    for pair in lookalikes:
        partner_id = None
        if pair.expected_id == instrument_id:
            partner_id = pair.selected_id
        elif pair.selected_id == instrument_id:
            partner_id = pair.expected_id
        if partner_id and partner_id in instruments:
            partner = instruments[partner_id]
            lines.append(f"{html.escape(partner.display_name)} — {html.escape(pair.feedback_message)}")
    if not lines:
        lines.append("No documented lookalikes for this module.")
    return "".join(f"<li>{line}</li>" for line in lines)


def _write_flashcard_deck(
    title: str,
    instruments: dict[str, Instrument],
    marker_cards: list[MarkerCard],
    output_dir: Path,
    lookalikes: list[LookalikePair] | None = None,
) -> Path:
    flashcard_path = output_dir / "flashcards.html"

    marker_ids = _marker_by_instrument(marker_cards)
    instrument_list = list(instruments.values())

    image_cache: dict[str, tuple[str, str]] = {}
    for instrument in instrument_list:
        marker_id = marker_ids.get(instrument.id)
        marker_path = None
        if marker_id is not None:
            marker_dir = output_dir / "markers"
            marker_dir.mkdir(parents=True, exist_ok=True)
            marker_path = marker_dir / f"apriltag_{marker_id:03d}_{instrument.id}_flashcard.png"
            generate_marker_png(marker_id, marker_path)
        image_src, attribution = _copy_flashcard_image(instrument, output_dir, marker_path)
        image_cache[instrument.id] = (image_src, attribution)

    pages: list[str] = []

    for i in range(0, len(instrument_list), 4):
        chunk = instrument_list[i:i+4]
        while len(chunk) < 4:
            chunk.append(None)

        image_cells: list[str] = []
        text_cells: list[str] = []

        for instrument in chunk:
            if instrument is None:
                image_cells.append("<div class='empty'></div>")
                text_cells.append("<div class='empty'></div>")
                continue

            image_src, attribution = image_cache[instrument.id]

            if image_src:
                image_cells.append(
                    f"<img src='{html.escape(image_src)}' alt='{html.escape(instrument.display_name)}'>"
                )
            else:
                image_cells.append("<div class='placeholder'>Image pending</div>")

            first_alias = instrument.aliases[0] if instrument.aliases else instrument.id
            features_html = _features(instrument)
            lookalike_html = _lookalike_lines(instrument.id, instruments, lookalikes or [])

            text_cells.append(
                "<div class='text-card'>"
                f"<h2>{html.escape(instrument.display_name)}</h2>"
                f"<p class='subtitle'>Family: {html.escape(instrument.family)} · Catalog: {html.escape(first_alias)}</p>"
                f"<h3>Key identification features</h3>"
                f"<ul>{features_html}</ul>"
                f"<h3>Common lookalikes</h3>"
                f"<ul>{lookalike_html}</ul>"
                f"<p class='aka'>Also known as: {html.escape(', '.join(instrument.aliases))}</p>"
                f"<p class='source'>{html.escape(attribution or 'Pending source')}</p>"
                "</div>"
            )

        if len(text_cells) == 4:
            text_cells = [text_cells[2], text_cells[3], text_cells[0], text_cells[1]]
        pages.append("<div class='page'><div class='image-grid'>" + "".join(image_cells) + "</div></div>")
        pages.append("<div class='page'><div class='text-grid'>" + "".join(text_cells) + "</div></div>")

    flashcard_path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html><head><meta charset='utf-8'><title>TrayGuard Flashcards</title>",
                "<style>",
                "@page{margin:0}",
                "body{margin:0;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;color:#1a1a1a;background:#f5f5f0}",
                ".page{page-break-after:always}",
                ".image-grid,.text-grid{display:grid;grid-template-columns:50% 50%;grid-template-rows:50% 50%;width:100vw;height:100vh}",
                ".image-grid>*,.text-grid>*{box-sizing:border-box}",
                ".image-grid>.empty,.text-grid>.empty{}",
                ".image-grid img{width:100%;height:100%;object-fit:contain;background:#f7f7f7}",
                ".text-card{padding:32px 36px;box-sizing:border-box;overflow:hidden;background:#f5f5f0}",
                ".text-card h2{font-size:30px;font-weight:700;margin:0 0 4px;color:#111}",
                ".text-card .subtitle{font-size:15px;color:#666;margin:0 0 20px}",
                ".text-card h3{font-size:17px;font-weight:600;color:#2563eb;margin:16px 0 6px}",
                ".text-card ul{margin:4px 0 0;padding-left:18px}",
                ".text-card li{font-size:15px;margin:4px 0;line-height:1.4}",
                ".text-card .aka{font-size:14px;color:#888;font-style:italic;margin:14px 0 0}",
                ".placeholder{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#f7f7f7;color:#555}",
                ".source{font-size:12px;color:#888;margin:16px 0 0;border-top:1px solid #ddd;padding-top:8px}",
                "</style>",
                "</head><body>",
                *pages,
                "</body></html>",
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
        "</head><body><h1>TrayGuard Neutral AprilTag Cards</h1><div class='grid'>",
    ]
    marker_dir = output_dir / "markers"
    marker_dir.mkdir(parents=True, exist_ok=True)
    for card in module.marker_cards:
        marker_path = marker_dir / f"apriltag_{card.marker_id:03d}_{card.card_id}.png"
        generate_marker_png(card.marker_id, marker_path)
        paths.append(marker_path)
        rows.append(
            "<section class='card'>"
            f"<img class='marker' src='markers/{marker_path.name}' alt='AprilTag marker {card.marker_id}'>"
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
        module.marker_cards,
        output_dir,
        lookalikes=module.lookalike_pairs,
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
    return [_write_flashcard_deck(title, instruments, marker_cards, output_dir)]
