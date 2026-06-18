from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError


API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "TrayGuard simple general-surgery flashcard builder"
WIKIMEDIA_MAX_DOWNLOAD_BPS = 25_000_000 / 8
DOWNLOAD_CHUNK_SIZE = 256 * 1024

TARGET_CATEGORIES = [
    "Category:Adson forceps",
    "Category:Allis forceps",
    "Category:Babcock clamp",
    "Category:Dissecting forceps",
    "Category:Hemostatic forceps",
    "Category:Kocher's forceps",
    "Category:Needle holders",
    "Category:Slotted Foerster forceps",
    "Category:Surgical clamps",
    "Category:Surgical forceps",
    "Category:Surgical retractors",
    "Category:Surgical scissors",
    "Category:Towel clamps",
    "Category:Mayo scissors",
    "Category:Scalpels",
]

SEARCH_TERMS = [
    "Adson forceps",
    "Allis tissue forceps",
    "Babcock clamp surgical instrument",
    "Backhaus towel clamp",
    "DeBakey forceps",
    "dissecting forceps surgical instrument",
    "Foerster sponge forceps",
    "hemostatic forceps",
    "Kelly forceps surgical instrument",
    "Kocher forceps",
    "Mayo scissors surgical instrument",
    "Metzenbaum scissors",
    "needle holder surgical instrument",
    "Senn retractor",
    "Weitlaner retractor",
    "Deaver retractor",
    "scalpel handle surgical instrument",
]

MANUAL_SEED_TITLES = [
    "File:Adson 00.jpg",
    "File:Adson 01.jpg",
    "File:Adson 03.jpg",
    "File:Adson 04.jpg",
    "File:Adson 05.jpg",
    "File:Adson 06.jpg",
    "File:Allis clamp 01.JPG",
    "File:Allis clamp 02.JPG",
    "File:Allis clamp 03.JPG",
    "File:Allis tissue forceps.jpg",
    "File:Babcock clamp2.jpg",
    "File:Babcock.JPG",
    "File:Debakey forceps.jpg",
    "File:Gunting Mayo Berbilah Lengkung.jpg",
    "File:Gunting Mayo Berbilah Lurus.jpg",
    "File:Mayo scissors 02.jpg",
    "File:Mayo scissors.jpg",
    "File:Mayo surgical scissors.jpg",
    "File:Metzenbaum scissors.jpg",
    "File:Hemostat 01.jpg",
    "File:Hemostat 03.jpg",
    "File:Hemostat 04.jpg",
    "File:Hemostat 05.jpg",
    "File:Hemostat Clamp.JPG",
    "File:Hemostatic clamp 01.JPG",
    "File:Hemostatic forceps 01.jpg",
    "File:Hemostatic forceps, grooved bent with box lock 01.jpg",
    "File:Kocher clamp 01.JPG",
    "File:Kocher's forceps with toothed jaw.jpg",
    "File:Pinza kocher.jpg",
    "File:Right Angle Clamp 01.JPG",
    "File:Right Angle Clamp.JPG",
    "File:Surgical clamp 00.jpg",
    "File:Surgical clamp 01.jpg",
    "File:Surgical clamp 02.jpg",
    "File:Surgical clamp 03.jpg",
    "File:Surgical clamp 04.jpg",
    "File:Surgical clamp 06.jpg",
    "File:Clamp for drep.JPG",
    "File:Towel Clamps 01.jpg",
    "File:Towel Clips 06.jpg",
]

ALLOW_TERMS = {
    "adson",
    "allis",
    "babcock",
    "backhaus",
    "clamp",
    "deaver",
    "debakey",
    "dissecting",
    "foerster",
    "forceps",
    "hemostat",
    "hemostatic",
    "kelly",
    "kocher",
    "mayo",
    "metzenbaum",
    "needle",
    "retractor",
    "scalpel",
    "scissors",
    "senn",
    "sponge",
    "towel",
    "weitlaner",
}

REJECT_TERMS = {
    "arthroscopic",
    "bronze",
    "catheter",
    "collection",
    "curette",
    "dental",
    "disposable",
    "endoscope",
    "endoscopic",
    "gynecological",
    "historical",
    "hysteroscope",
    "laparoscope",
    "laparoscopic",
    "lithotomy",
    "multiple",
    "plastic",
    "procedure",
    "set",
    "sets",
    "speculum",
    "tray",
    "trocar",
    "vacuum",
}

LABEL_OVERRIDES = {
    "File:Adson 00.jpg": "Adson Forceps",
    "File:Adson 01.jpg": "Adson Forceps",
    "File:Adson 03.jpg": "Adson Forceps",
    "File:Adson 04.jpg": "Adson Forceps",
    "File:Adson 05.jpg": "Adson Forceps",
    "File:Adson 06.jpg": "Adson Forceps",
    "File:Gunting Mayo Berbilah Lengkung.jpg": "Mayo Scissors, Curved",
    "File:Gunting Mayo Berbilah Lurus.jpg": "Mayo Scissors, Straight",
    "File:Kocher's forceps with toothed jaw.jpg": "Kocher Forceps With Toothed Jaw",
    "File:Pinza kocher.jpg": "Kocher Forceps",
    "File:Towel Clips 06.jpg": "Towel Clamp",
}


def api_get(params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({**params, "format": "json"})
    request = urllib.request.Request(f"{API_URL}?{query}", headers={"User-Agent": USER_AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                payload = json.load(response)
            time.sleep(0.75)
            return payload
        except HTTPError as exc:
            if exc.code != 429 or attempt == 5:
                raise
            time.sleep(8 + attempt * 6)
    raise RuntimeError("unreachable")


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def normalized(value: str) -> str:
    value = value.removeprefix("File:")
    value = re.sub(r"\.[A-Za-z0-9]+$", "", value)
    value = value.replace("_", " ")
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value).lower()
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str) -> str:
    value = normalized(value)
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return re.sub(r"_+", "_", value)[:100] or "commons_instrument"


def candidate_label(title: str) -> str:
    if title in LABEL_OVERRIDES:
        return LABEL_OVERRIDES[title]
    name = normalized(title)
    name = re.sub(r"\b\d{2,}\b", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name.title() if name else title.removeprefix("File:")


def looks_in_scope(title: str, description: str = "") -> bool:
    text = f"{normalized(title)} {normalized(description)}"
    words = set(text.split())
    if words & REJECT_TERMS:
        return False
    return bool(words & ALLOW_TERMS)


def category_file_titles(category: str) -> set[str]:
    titles: set[str] = set()
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmtype": "file",
        "cmlimit": "500",
    }
    while True:
        try:
            payload = api_get(params)
        except HTTPError as exc:
            if exc.code == 429:
                break
            raise
        for member in payload.get("query", {}).get("categorymembers", []):
            titles.add(member["title"])
        if "continue" not in payload:
            break
        params.update(payload["continue"])
    return titles


def search_file_titles(term: str) -> set[str]:
    titles: set[str] = set()
    try:
        payload = api_get(
            {
                "action": "query",
                "generator": "search",
                "gsrsearch": term,
                "gsrnamespace": "6",
                "gsrlimit": "50",
                "prop": "info",
            }
        )
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
        try:
            payload = api_get(
                {
                    "action": "query",
                    "titles": "|".join(chunk),
                    "prop": "imageinfo",
                    "iiprop": "url|mime|size|extmetadata",
                    "iiurlwidth": "1200",
                }
            )
        except HTTPError as exc:
            if exc.code == 429:
                break
            raise
        for page in payload.get("query", {}).get("pages", {}).values():
            if page.get("missing") or not page.get("imageinfo"):
                continue
            info = page["imageinfo"][0]
            mime = str(info.get("mime", ""))
            if not mime.startswith("image/"):
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
                started_at = time.monotonic()
                bytes_written = 0
                with destination.open("wb") as handle:
                    while True:
                        chunk = response.read(DOWNLOAD_CHUNK_SIZE)
                        if not chunk:
                            break
                        handle.write(chunk)
                        bytes_written += len(chunk)
                        minimum_elapsed = bytes_written / WIKIMEDIA_MAX_DOWNLOAD_BPS
                        actual_elapsed = time.monotonic() - started_at
                        if actual_elapsed < minimum_elapsed:
                            time.sleep(minimum_elapsed - actual_elapsed)
            time.sleep(0.8)
            return True
        except (HTTPError, URLError, TimeoutError):
            destination.unlink(missing_ok=True)
            time.sleep(1.5 + attempt)
    return False


def build_catalog(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, str]]]:
    titles: set[str] = set()
    title_sources: dict[str, set[str]] = {}
    if args.manual_seed_only:
        for title in MANUAL_SEED_TITLES:
            titles.add(title)
            title_sources.setdefault(title, set()).add("manual Commons category seed")
    else:
        for title in MANUAL_SEED_TITLES:
            titles.add(title)
            title_sources.setdefault(title, set()).add("manual Commons category seed")
        for category in TARGET_CATEGORIES:
            for title in category_file_titles(category):
                titles.add(title)
                title_sources.setdefault(title, set()).add(category)
        for term in SEARCH_TERMS:
            for title in search_file_titles(term):
                titles.add(title)
                title_sources.setdefault(title, set()).add(f"search:{term}")

    infos = image_info(sorted(title for title in titles if looks_in_scope(title)))
    instruments: list[dict[str, Any]] = []
    review_rows: list[dict[str, str]] = []
    used_ids: set[str] = set()
    for title, info in sorted(infos.items(), key=lambda item: normalized(item[0])):
        metadata = info.get("extmetadata", {})
        description = clean_text(metadata.get("ImageDescription", {}).get("value", ""))
        is_manual_seed = "manual Commons category seed" in title_sources.get(title, set())
        if is_manual_seed:
            if not looks_in_scope(title):
                continue
        elif not looks_in_scope(title, description):
            continue

        width = int(info.get("thumbwidth") or info.get("width") or 0)
        height = int(info.get("thumbheight") or info.get("height") or 0)
        if width < args.min_width or height < args.min_height:
            continue

        image_url = info.get("thumburl") or info.get("url")
        if not image_url:
            continue

        base_id = f"commons_simple_{slug(title)}"
        instrument_id = base_id
        suffix = 2
        while instrument_id in used_ids:
            instrument_id = f"{base_id}_{suffix}"
            suffix += 1
        used_ids.add(instrument_id)

        extension = safe_extension(image_url, info.get("mime", ""))
        image_path = args.asset_dir / f"{instrument_id}{extension}"
        if not download(image_url, image_path):
            continue

        license_name = clean_text(metadata.get("LicenseShortName", {}).get("value", ""))
        usage_terms = clean_text(metadata.get("UsageTerms", {}).get("value", ""))
        artist = clean_text(metadata.get("Artist", {}).get("value", ""))
        credit = clean_text(metadata.get("Credit", {}).get("value", ""))
        source_url = info.get("descriptionurl", info.get("url", ""))
        label = candidate_label(title)
        attribution = "; ".join(part for part in [f"Wikimedia Commons: {title}", artist, license_name or usage_terms] if part)
        source_list = ", ".join(sorted(title_sources.get(title, [])))

        instruments.append(
            {
                "id": instrument_id,
                "display_name": label,
                "family": "Wikimedia Commons / simple general-surgery instrument",
                "aliases": [title.removeprefix("File:")],
                "distinguishing_features": [
                    description[:220] if description else "Single-instrument Wikimedia Commons reference.",
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
                        "url": source_url,
                    }
                ],
                "study_prompts": [{"id": "name", "prompt": "Name this instrument.", "answer": label}],
                "local_verification_status": "external_dataset_unverified",
                "curation_note": "auto-screened for simple general-surgery flashcard review",
            }
        )
        review_rows.append(
            {
                "id": instrument_id,
                "display_name": label,
                "title": title,
                "source": source_list,
                "license": license_name or usage_terms,
                "source_url": source_url,
                "image_path": str(image_path),
                "screening_status": "auto_included_pending_review",
            }
        )
        if len(instruments) >= args.max_images:
            break

    payload = {
        "catalog_id": "wikimedia_commons_simple_general_surgery_v1",
        "version": "2026.05-local",
        "name": "Wikimedia Commons Simple General Surgery Instruments",
        "source_note": (
            "Generated from Wikimedia Commons categories and searches for handheld general-surgery instruments. "
            "Auto-screened to exclude laparoscopic/endoscopic tools, sets, trays, procedure scenes, plastic disposables, and off-scope terms. "
            "Review each card before assessment use."
        ),
        "instruments": instruments,
    }
    return payload, review_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a simple general-surgery Commons flashcard catalog.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("config/instrument_catalogs/wikimedia_commons_simple_general_surgery_v1.json"),
    )
    parser.add_argument(
        "--asset-dir",
        type=Path,
        default=Path("data/instruments/wikimedia_commons_simple_general_surgery_v1"),
    )
    parser.add_argument(
        "--review-csv",
        type=Path,
        default=Path("docs/project/reference/wikimedia_commons_simple_general_surgery_review.csv"),
    )
    parser.add_argument("--max-images", type=int, default=80)
    parser.add_argument("--min-width", type=int, default=240)
    parser.add_argument("--min-height", type=int, default=180)
    parser.add_argument("--manual-seed-only", action="store_true", help="Use the hand-screened Commons file seed list only.")
    args = parser.parse_args()

    payload, review_rows = build_catalog(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    args.review_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.review_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "display_name", "title", "source", "license", "source_url", "image_path", "screening_status"],
        )
        writer.writeheader()
        writer.writerows(review_rows)

    print(f"Wrote {len(payload['instruments'])} instruments to {args.output}")
    print(f"Wrote review CSV to {args.review_csv}")


if __name__ == "__main__":
    main()
