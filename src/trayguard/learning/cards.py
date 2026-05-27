from __future__ import annotations

from pathlib import Path

from trayguard.learning.aruco import generate_marker_png
from trayguard.learning.models import TrayModule


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
    return paths
