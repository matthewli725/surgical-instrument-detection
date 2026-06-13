"""Render example TrayGuard study card front and back as PNG figures.

Uses Playwright to render actual HTML flashcards and screenshot them,
so the figures match the live card design exactly.

Usage:
    uv run --group fdr python scripts/build_example_card_figures.py

Reads:  config/tray_modules/fgvc12_major_focused_v1.json
        data/instruments/fgvc12_major_tray_v1/fgvc12_major_clamp_kelly_8in_view_a.jpg
Writes: fdr/source/figures/card_front_example.png
        fdr/source/figures/card_back_example.png
"""
from __future__ import annotations

import base64
import html
import json
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

from trayguard.learning.aruco import generate_marker_png
from trayguard.learning.cards import _standardize_flashcard_image

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "config" / "tray_modules" / "fgvc12_major_focused_v1.json"
OUT_DIR = REPO_ROOT / "fdr" / "source" / "figures"
FRONT_OUT = OUT_DIR / "card_front_example.png"
BACK_OUT = OUT_DIR / "card_back_example.png"
TEMP_DIR = REPO_ROOT / "outputs" / "card_figures_temp"

INSTRUMENT_ID = "fgvc12_major_clamp_kelly_8in"

_CARD_CSS = """
body{margin:0;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;background:#f5f5f0}
img{width:100vw;height:100vh;object-fit:contain;display:block;background:#f7f7f7}
.text-card{width:100vw;height:100vh;padding:32px 36px;box-sizing:border-box;overflow:hidden;background:#f5f5f0;color:#1a1a1a}
.text-card h2{font-size:30px;font-weight:700;margin:0 0 4px;color:#111}
.text-card .subtitle{font-size:15px;color:#666;margin:0 0 20px}
.text-card h3{font-size:17px;font-weight:600;color:#2563eb;margin:16px 0 6px}
.text-card ul{margin:4px 0 0;padding-left:18px}
.text-card li{font-size:15px;margin:4px 0;line-height:1.4}
.text-card .aka{font-size:14px;color:#888;font-style:italic;margin:14px 0 0}
.text-card .source{font-size:12px;color:#888;margin:16px 0 0;border-top:1px solid #ddd;padding-top:8px}
"""


def _build_front_html(image_data_b64: str, mime: str) -> str:
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + _CARD_CSS
        + "</style></head><body>"
        f"<img src='data:{mime};base64,{image_data_b64}'>"
        "</body></html>"
    )


def _build_back_html(instrument: dict, attribution: str,
                     lookalike_pairs: list[dict],
                     all_instruments: dict[str, dict]) -> str:
    first_alias = instrument["aliases"][0] if instrument["aliases"] else instrument["id"]
    features_html = "".join(
        f"<li>{html.escape(f)}</li>" for f in instrument.get("distinguishing_features", [])
    )
    lookalike_html = _lookalike_lines(instrument["id"], lookalike_pairs, all_instruments)
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + _CARD_CSS
        + "</style></head><body>"
        "<div class='text-card'>"
        f"<h2>{html.escape(instrument['display_name'])}</h2>"
        f"<p class='subtitle'>Family: {html.escape(instrument['family'])} · Catalog: {html.escape(first_alias)}</p>"
        f"<h3>Key identification features</h3>"
        f"<ul>{features_html}</ul>"
        f"<h3>Common lookalikes</h3>"
        f"<ul>{lookalike_html}</ul>"
        f"<p class='aka'>Also known as: {html.escape(', '.join(instrument['aliases']))}</p>"
        f"<p class='source'>{html.escape(attribution)}</p>"
        "</div>"
        "</body></html>"
    )


def _lookalike_lines(instrument_id: str, lookalike_pairs: list[dict],
                     instruments: dict[str, dict]) -> str:
    lines: list[str] = []
    for pair in lookalike_pairs:
        partner_id = None
        if pair["expected_id"] == instrument_id:
            partner_id = pair["selected_id"]
        elif pair["selected_id"] == instrument_id:
            partner_id = pair["expected_id"]
        if partner_id and partner_id in instruments:
            partner = instruments[partner_id]
            lines.append(
                f"{html.escape(partner['display_name'])} — {html.escape(pair['feedback_message'])}"
            )
    if not lines:
        lines.append("No documented lookalikes for this module.")
    return "".join(f"<li>{line}</li>" for line in lines)


def _image_data_uri(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    suffix = path.suffix.lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(suffix.lstrip("."), "image/png")
    return b64, mime


def main() -> None:
    if not MODULE_PATH.exists():
        raise SystemExit(f"Module JSON not found: {MODULE_PATH}")

    module = json.loads(MODULE_PATH.read_text(encoding="utf-8"))
    instrument = next(
        inst for inst in module["instruments"]
        if inst["id"] == INSTRUMENT_ID
    )
    marker = next(
        mc for mc in module["marker_cards"]
        if mc["instrument_id"] == INSTRUMENT_ID
    )
    ref = next(
        r for r in instrument["image_refs"] if r.get("approved_for_study")
    )
    source = REPO_ROOT / str(ref["path"])
    if not source.exists():
        raise SystemExit(f"Source image not found: {source}")

    marker_dir = TEMP_DIR / "markers"
    marker_dir.mkdir(parents=True, exist_ok=True)
    marker_path = marker_dir / f"aruco_{marker['marker_id']:03d}_{INSTRUMENT_ID}.png"
    generate_marker_png(marker["marker_id"], marker_path)

    image_dir = TEMP_DIR / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / f"{INSTRUMENT_ID}_standardized.jpg"
    _standardize_flashcard_image(source, image_path, marker_path)

    attribution = ref.get("attribution", "Pending source")
    instruments_by_id = {inst["id"]: inst for inst in module["instruments"]}

    image_b64, image_mime = _image_data_uri(image_path)
    front_html = _build_front_html(image_b64, image_mime)
    back_html = _build_back_html(
        instrument, attribution,
        module.get("lookalike_pairs", []),
        instruments_by_id,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        page = browser.new_page(
            viewport={"width": 600, "height": 450},
            device_scale_factor=2,
        )

        page.set_content(front_html)
        page.screenshot(path=str(FRONT_OUT), full_page=True)
        print(f"  wrote {FRONT_OUT}")

        page.set_content(back_html)
        page.screenshot(path=str(BACK_OUT), full_page=True)
        print(f"  wrote {BACK_OUT}")

        browser.close()

    shutil.rmtree(TEMP_DIR, ignore_errors=True)


if __name__ == "__main__":
    main()
