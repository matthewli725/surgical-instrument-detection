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
from urllib.error import HTTPError
from pathlib import Path
from typing import Any


API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "TrayGuard local educational flashcard builder"
DEFAULT_CATEGORIES = [
    "Category:Surgical instruments",
    "Category:Forceps",
    "Category:Scalpels",
    "Category:Surgical scissors",
]
DEFAULT_SEARCH_TERMS = [
    "Adson forceps",
    "Allis forceps",
    "Babcock forceps",
    "Brown-Adson forceps",
    "Crile forceps",
    "DeBakey forceps",
    "Kelly forceps",
    "Mayo scissors",
    "Metzenbaum scissors",
    "Mosquito forceps",
    "Needle holder",
    "Olsen-Hegar",
    "Retractor surgical instrument",
    "Senn retractor",
    "Scalpel handle",
    "Hemostat surgical instrument",
    "Towel clip surgical instrument",
    "Surgical probe",
    "Surgical dissector",
]
KEYWORDS = {
    "adson",
    "allis",
    "babcock",
    "brown",
    "clamp",
    "crile",
    "curette",
    "debakey",
    "dissector",
    "elevator",
    "forceps",
    "hegar",
    "hemostat",
    "holder",
    "kelly",
    "lancet",
    "mayo",
    "metzenbaum",
    "mosquito",
    "needle",
    "probe",
    "retractor",
    "rongeur",
    "scalpel",
    "scissors",
    "senn",
    "speculum",
    "surgical",
    "towel",
    "trocar",
}


def api_get(params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({**params, "format": "json"})
    request = urllib.request.Request(f"{API_URL}?{query}", headers={"User-Agent": USER_AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
            time.sleep(0.2)
            return payload
        except HTTPError as exc:
            if exc.code != 429 or attempt == 5:
                raise
            time.sleep(2 + attempt * 2)
    raise RuntimeError("unreachable")


def strip_markup(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def slug(value: str) -> str:
    value = value.removeprefix("File:")
    value = re.sub(r"\.[A-Za-z0-9]+$", "", value)
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return re.sub(r"_+", "_", value)[:110] or "commons_instrument"


def normalized_name(value: str) -> str:
    value = value.removeprefix("File:")
    value = re.sub(r"\.[A-Za-z0-9]+$", "", value)
    value = value.replace("_", " ")
    value = re.sub(r"\([^)]*\)", " ", value)
    value = re.sub(r"\b\d{3,}\b", " ", value)
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value).lower()
    return re.sub(r"\s+", " ", value).strip()


def looks_relevant(title: str, description: str = "") -> bool:
    text = f"{normalized_name(title)} {normalized_name(description)}"
    return any(keyword in text for keyword in KEYWORDS)


def category_file_titles(category: str, max_depth: int) -> set[str]:
    titles: set[str] = set()
    seen_categories = {category}
    queue = [(category, 0)]
    while queue:
        current, depth = queue.pop(0)
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": current,
            "cmtype": "file|subcat",
            "cmlimit": "500",
        }
        while True:
            payload = api_get(params)
            for member in payload.get("query", {}).get("categorymembers", []):
                title = member["title"]
                if member["ns"] == 6:
                    titles.add(title)
                elif member["ns"] == 14 and depth < max_depth and title not in seen_categories:
                    seen_categories.add(title)
                    queue.append((title, depth + 1))
            if "continue" not in payload:
                break
            params.update(payload["continue"])
    return titles


def search_file_titles(term: str) -> set[str]:
    titles: set[str] = set()
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": term,
        "gsrnamespace": "6",
        "gsrlimit": "50",
        "prop": "info",
    }
    try:
        payload = api_get(params)
    except HTTPError as exc:
        if exc.code == 429:
            return titles
        raise
    for page in payload.get("query", {}).get("pages", {}).values():
        titles.add(page["title"])
    return titles


def image_info(titles: list[str]) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for index in range(0, len(titles), 50):
        chunk = titles[index : index + 50]
        payload = api_get(
            {
                "action": "query",
                "titles": "|".join(chunk),
                "prop": "imageinfo",
                "iiprop": "url|mime|extmetadata",
                "iiurlwidth": "1200",
            }
        )
        for page in payload.get("query", {}).get("pages", {}).values():
            if page.get("missing") or not page.get("imageinfo"):
                continue
            info = page["imageinfo"][0]
            if not str(info.get("mime", "")).startswith("image/"):
                continue
            results[page["title"]] = info
    return results


def safe_extension(url: str, mime: str) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".svg"}:
        return suffix
    if mime == "image/png":
        return ".png"
    if mime == "image/webp":
        return ".webp"
    if mime == "image/svg+xml":
        return ".svg"
    return ".jpg"


def download(url: str, destination: Path) -> bool:
    if destination.exists() and destination.stat().st_size > 0:
        return True
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(response.read())
            time.sleep(0.25)
            return True
        except HTTPError as exc:
            if exc.code != 429 or attempt == 4:
                return False
            time.sleep(4 + attempt * 4)
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
            ratio = difflib.SequenceMatcher(None, new_norm, normalized_name(existing_name)).ratio()
            if ratio >= 0.68 or new_norm in normalized_name(existing_name) or normalized_name(existing_name) in new_norm:
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
    parser = argparse.ArgumentParser(description="Build a Wikimedia Commons surgical instrument flashcard catalog.")
    parser.add_argument("--output", type=Path, default=Path("config/instrument_catalogs/wikimedia_commons_surgical_instruments_v1.json"))
    parser.add_argument("--asset-dir", type=Path, default=Path("assets/instruments/wikimedia_commons_surgical_instruments_v1"))
    parser.add_argument("--duplicate-report", type=Path, default=Path("docs/project/reference/card_duplicate_candidates.csv"))
    parser.add_argument("--max-images", type=int, default=260)
    parser.add_argument("--category-depth", type=int, default=1)
    parser.add_argument("--max-download-failures", type=int, default=5)
    parser.add_argument("--no-search", action="store_true", help="Use category members only; avoids extra Commons search API calls.")
    args = parser.parse_args()

    titles: set[str] = set()
    for category in DEFAULT_CATEGORIES:
        titles.update(category_file_titles(category, args.category_depth))
    if not args.no_search:
        for term in DEFAULT_SEARCH_TERMS:
            titles.update(search_file_titles(term))

    title_candidates = [title for title in sorted(titles) if looks_relevant(title)]
    title_candidates = title_candidates[: max(args.max_images * 4, args.max_images)]
    info_by_title = image_info(title_candidates)
    instruments: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    download_failures = 0
    for title, info in sorted(info_by_title.items(), key=lambda item: normalized_name(item[0])):
        metadata = info.get("extmetadata", {})
        description = strip_markup(metadata.get("ImageDescription", {}).get("value", ""))
        if not looks_relevant(title, description):
            continue

        clean_name = normalized_name(title).title()
        if not clean_name:
            continue
        instrument_id = f"commons_{slug(title)}"
        if instrument_id in used_ids:
            continue
        used_ids.add(instrument_id)

        image_url = info.get("thumburl") or info.get("url")
        if not image_url:
            continue
        extension = safe_extension(image_url, info.get("mime", ""))
        image_path = args.asset_dir / f"{instrument_id}{extension}"
        if not download(image_url, image_path):
            download_failures += 1
            if download_failures >= args.max_download_failures:
                break
            continue

        license_name = strip_markup(metadata.get("LicenseShortName", {}).get("value", ""))
        usage_terms = strip_markup(metadata.get("UsageTerms", {}).get("value", ""))
        artist = strip_markup(metadata.get("Artist", {}).get("value", ""))
        credit = strip_markup(metadata.get("Credit", {}).get("value", ""))
        attribution = "; ".join(part for part in [f"Wikimedia Commons: {title}", artist, license_name or usage_terms] if part)

        instruments.append(
            {
                "id": instrument_id,
                "display_name": clean_name,
                "family": "Wikimedia Commons / surgical instrument reference",
                "aliases": [title.removeprefix("File:")],
                "distinguishing_features": [
                    description[:220] if description else "Open image reference from Wikimedia Commons.",
                    f"Commons license: {license_name or usage_terms or 'see source page'}",
                ],
                "image_refs": [
                    {
                        "id": "view_a",
                        "path": str(image_path),
                        "source": "wikimedia_commons",
                        "approved_for_study": True,
                        "approved_for_assessment": False,
                        "attribution": attribution,
                        "credit": credit,
                        "license": license_name or usage_terms,
                        "url": info.get("descriptionurl", info.get("url", "")),
                    }
                ],
                "study_prompts": [
                    {"id": "name", "prompt": "Name this instrument or instrument reference.", "answer": clean_name}
                ],
                "local_verification_status": "external_dataset_unverified",
            }
        )
        if len(instruments) >= args.max_images:
            break

    payload = {
        "catalog_id": "wikimedia_commons_surgical_instruments_v1",
        "version": "2026.05-local",
        "name": "Wikimedia Commons Surgical Instrument Catalog",
        "source_note": "Generated from freely licensed Wikimedia Commons file/category/search metadata. Use for study/reference cards; verify exact labels before assessment use.",
        "instruments": instruments,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    existing = load_existing_names(
        [
            Path("config/instrument_catalogs/hospitools_dslr_v1.json"),
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

    print(f"Wrote {len(instruments)} Commons catalog instruments to {args.output}")
    print(f"Wrote {len(duplicates)} duplicate candidates to {args.duplicate_report}")


if __name__ == "__main__":
    main()
