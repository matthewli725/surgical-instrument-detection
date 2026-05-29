from __future__ import annotations

import argparse
import csv
import difflib
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError


API_URL = "https://api.openverse.engineering/v1/images/"
USER_AGENT = "TrayGuard local educational flashcard builder"
SEARCH_TERMS = [
    "surgical instrument",
    "surgical forceps",
    "surgical scissors",
    "scalpel handle",
    "hemostat forceps",
    "needle holder surgical",
    "surgical retractor",
    "surgical clamp instrument",
    "surgical probe instrument",
    "medical forceps instrument",
]
KEYWORDS = {
    "adson",
    "allis",
    "babcock",
    "clamp",
    "crile",
    "curette",
    "debakey",
    "dissector",
    "forceps",
    "hegar",
    "hemostat",
    "holder",
    "kelly",
    "mayo",
    "metzenbaum",
    "mosquito",
    "needle",
    "probe",
    "retractor",
    "scalpel",
    "scissor",
    "senn",
    "speculum",
    "surgical",
    "towel",
}


def slug(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return re.sub(r"_+", "_", value)[:110] or "openverse_instrument"


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def normalized_name(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"\.[A-Za-z0-9]+$", "", value)
    value = re.sub(r"\([^)]*\)", " ", value)
    value = re.sub(r"\b\d{3,}\b", " ", value)
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value).lower()
    return re.sub(r"\s+", " ", value).strip()


def looks_relevant(item: dict[str, Any]) -> bool:
    text = f"{normalized_name(item.get('title', ''))} {normalized_name(item.get('tags', []).__str__())}"
    return any(keyword in text for keyword in KEYWORDS)


def api_search(term: str, page: int, page_size: int) -> dict[str, Any]:
    params = urllib.parse.urlencode({"q": term, "page": page, "page_size": page_size})
    request = urllib.request.Request(f"{API_URL}?{params}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    time.sleep(0.2)
    return payload


def extension_from_url(url: str) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        return suffix
    return ".jpg"


def download(url: str, destination: Path) -> bool:
    if destination.exists() and destination.stat().st_size > 0:
        return True
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(response.read())
        time.sleep(0.15)
        return True
    except (HTTPError, URLError, TimeoutError):
        return False


def load_existing_names(paths: list[Path]) -> list[tuple[str, str, str]]:
    names: list[tuple[str, str, str]] = []
    for path in paths:
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload.get("instruments", []):
            names.append((payload.get("catalog_id") or payload.get("module_id") or path.stem, row["id"], row["display_name"]))
    return names


def duplicate_rows(new_rows: list[dict[str, Any]], existing: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for new in new_rows:
        new_norm = normalized_name(new["display_name"])
        for source, existing_id, existing_name in existing:
            existing_norm = normalized_name(existing_name)
            ratio = difflib.SequenceMatcher(None, new_norm, existing_norm).ratio()
            if ratio >= 0.68 or new_norm in existing_norm or existing_norm in new_norm:
                rows.append(
                    {
                        "new_catalog_id": new["id"],
                        "new_display_name": new["display_name"],
                        "existing_source": source,
                        "existing_id": existing_id,
                        "existing_display_name": existing_name,
                        "similarity": round(ratio, 3),
                    }
                )
    return sorted(rows, key=lambda row: (-row["similarity"], row["new_display_name"]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an Openverse surgical instrument flashcard catalog.")
    parser.add_argument("--output", type=Path, default=Path("config/instrument_catalogs/openverse_surgical_instruments_v1.json"))
    parser.add_argument("--asset-dir", type=Path, default=Path("data/instruments/openverse_surgical_instruments_v1"))
    parser.add_argument("--duplicate-report", type=Path, default=Path("docs/project/reference/openverse_duplicate_candidates.csv"))
    parser.add_argument("--max-images", type=int, default=80)
    parser.add_argument("--page-size", type=int, default=20)
    args = parser.parse_args()

    seen_urls: set[str] = set()
    seen_ids: set[str] = set()
    instruments: list[dict[str, Any]] = []
    for term in SEARCH_TERMS:
        page = 1
        while len(instruments) < args.max_images:
            payload = api_search(term, page, args.page_size)
            results = payload.get("results", [])
            if not results:
                break
            for item in results:
                if len(instruments) >= args.max_images:
                    break
                url = item.get("thumbnail") or item.get("url")
                if not url or url in seen_urls or not looks_relevant(item):
                    continue
                seen_urls.add(url)

                title = clean_text(item.get("title") or "Openverse surgical instrument")
                instrument_id = f"openverse_{slug(title)}"
                suffix = 2
                while instrument_id in seen_ids:
                    instrument_id = f"openverse_{slug(title)}_{suffix}"
                    suffix += 1
                seen_ids.add(instrument_id)

                image_path = args.asset_dir / f"{instrument_id}{extension_from_url(url)}"
                if not download(url, image_path):
                    continue

                creator = clean_text(item.get("creator") or "")
                license_name = clean_text(item.get("license") or "")
                license_version = clean_text(item.get("license_version") or "")
                source = clean_text(item.get("source") or item.get("provider") or "Openverse")
                attribution = "; ".join(
                    part for part in [f"Openverse: {title}", creator, f"{license_name} {license_version}".strip(), source] if part
                )
                instruments.append(
                    {
                        "id": instrument_id,
                        "display_name": title,
                        "family": f"Openverse / {source}",
                        "aliases": [term],
                        "distinguishing_features": [
                            clean_text(item.get("foreign_landing_url") or item.get("url") or "")[:220],
                            f"Openverse license: {license_name} {license_version}".strip(),
                        ],
                        "image_refs": [
                            {
                                "id": "view_a",
                                "path": str(image_path),
                                "source": "openverse",
                                "approved_for_study": True,
                                "approved_for_assessment": False,
                                "attribution": attribution,
                                "license": f"{license_name} {license_version}".strip(),
                                "url": item.get("foreign_landing_url") or item.get("url") or "",
                            }
                        ],
                        "study_prompts": [{"id": "name", "prompt": "Name this instrument or instrument reference.", "answer": title}],
                        "local_verification_status": "external_dataset_unverified",
                    }
                )
            page += 1
            if page > payload.get("page_count", page):
                break
        if len(instruments) >= args.max_images:
            break

    payload = {
        "catalog_id": "openverse_surgical_instruments_v1",
        "version": "2026.05-local",
        "name": "Openverse Surgical Instrument Catalog",
        "source_note": "Generated from Openverse image search metadata. Use for study/reference cards; verify exact labels and source pages before assessment use.",
        "instruments": instruments,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    existing = load_existing_names(
        [
            Path("config/instrument_catalogs/hospitools_dslr_v1.json"),
            Path("config/instrument_catalogs/wikimedia_commons_surgical_instruments_v1.json"),
            Path("config/tray_modules/basic_general_tray_v1.json"),
        ]
    )
    duplicates = duplicate_rows(instruments, existing)
    args.duplicate_report.parent.mkdir(parents=True, exist_ok=True)
    with args.duplicate_report.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "new_catalog_id",
                "new_display_name",
                "existing_source",
                "existing_id",
                "existing_display_name",
                "similarity",
            ],
        )
        writer.writeheader()
        writer.writerows(duplicates)

    print(f"Wrote {len(instruments)} Openverse catalog instruments to {args.output}")
    print(f"Wrote {len(duplicates)} duplicate candidates to {args.duplicate_report}")


if __name__ == "__main__":
    main()
