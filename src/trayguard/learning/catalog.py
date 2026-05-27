from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from trayguard.learning.models import Instrument, InstrumentCatalog
from trayguard.learning.module import _require_keys


def load_instrument_catalog(path: str | Path) -> InstrumentCatalog:
    catalog_path = Path(path)
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    _require_keys(payload, {"catalog_id", "version", "name", "instruments"}, str(catalog_path))

    instruments = {
        row["id"]: Instrument(
            id=row["id"],
            display_name=row["display_name"],
            family=row.get("family", ""),
            aliases=list(row.get("aliases", [])),
            distinguishing_features=list(row.get("distinguishing_features", [])),
            image_refs=list(row.get("image_refs", [])),
            study_prompts=list(row.get("study_prompts", [])),
            local_verification_status=row.get("local_verification_status", "pending_review"),
        )
        for row in payload["instruments"]
    }

    if len(instruments) != len(payload["instruments"]):
        raise ValueError("Instrument catalog IDs must be unique.")

    return InstrumentCatalog(
        catalog_id=payload["catalog_id"],
        version=payload["version"],
        name=payload["name"],
        source_note=payload.get("source_note", ""),
        instruments=instruments,
    )
