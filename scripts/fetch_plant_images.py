#!/usr/bin/env python3
"""Download reusable catalogue photos from Wikimedia Commons and link them locally."""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import re
import sqlite3
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = ROOT / "localdata" / "almanac.db"
DEFAULT_IMAGE_DIR = ROOT / "localdata" / "plant_images"
DEFAULT_MANIFEST = ROOT / "localdata" / "plant-image-sources.json"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "my-garden-catalogue/1.0 (private educational plant almanac)"

SEARCH_OVERRIDES = {
    "Lebanese Cucumber": "Lebanese cucumber Cucumis sativus",
    "Telegraph Improved Cucumber": "Telegraph Improved cucumber",
    "Basil - Genovese": "Genovese basil Ocimum basilicum",
    "Bergamot - Lemon Mint": "Monarda citriodora lemon mint",
    "Broccoli - Purple Sprouting": "purple sprouting broccoli",
    "Bunching Onion - Winter Ishikura": "Ishikura bunching onion",
    "Carrot - Cosmic Purple": "Cosmic Purple carrot",
    "Carrot - Nantes": "Nantes carrot",
    "Carrot - Solar Yellow": "yellow carrot",
    "Eggplant - Casper": "Casper white eggplant",
    "Eggplant - Tsakoniki": "Tsakoniki eggplant",
    "Grass Jelly": "Cyclea barbata plant",
    "Japanese Raisin Tree": "Hovenia dulcis tree",
    "Lettuce - Buttercrunch": "Buttercrunch lettuce",
    "Lilly of the Valley": "Convallaria majalis lily of the valley",
    "Marigold - French Marigold": "Tagetes patula French marigold",
    "Pea - Greenfeast": "Greenfeast pea Pisum sativum",
    "Pea - Oregon Dwarf": "Oregon Dwarf snow pea",
    "Radish - French Breakfast": "French Breakfast radish",
    "Stepover Apples": "stepover apple tree espalier",
    "Sunflower - Golden Prominence F1": "Helianthus annuus sunflower plant",
    "Sweet Corn Terrific F1": "sweet corn Zea mays plant",
    "Tomato - Black Krim": "Black Krim tomato",
}

# Visually reviewed choices for searches where the first result was a scan,
# illustration, prepared food, or a different cultivar.
PINNED_TITLES = {
    8: "File:Cucumis sativus 0001.JPG",
    9: "File:Lobularia maritima Porto Covo 2022-1.jpg",
    12: "File:Purple (133472799).jpg",
    13: "File:Starr-090519-8038-Allium fistulosum-crop-Kula-Maui (24328807153).jpg",
    14: "File:Dark carrot.jpg",
    15: "File:Fresh orange carrots.jpg",
    17: "File:Starr-090713-2635-Solanum melongena-white fruit-Lahaina-Maui (24876145261).jpg",
    18: "File:Starr-130312-2414-Solanum melongena-fruit black globe and striped mauve and white-Pali o Waipio Huelo-Maui (25207292225).jpg",
    19: "File:Cyclea barbata 393265361.jpg",
    21: "File:Hyssopus-officinalis-flowers.jpg",
    22: "File:Hovenia dulcis Japanese Raisin Tree ყუნწშაქარა.JPG",
    27: "File:Starr 081009-0039 Pisum sativum var. macrocarpum.jpg",
    28: "File:Radish 3371103037 4ab07db0bf o.jpg",
}

BLOCKED_TITLE_WORDS = {
    "botanical illustration", "distribution", "drawing", "herbarium", "icon",
    "logo", "map", "range", "seed packet", "stamp",
}


def clean_html(value: str) -> str:
    plain = re.sub(r"<[^>]+>", " ", value or "")
    return " ".join(html.unescape(plain).split())


def api_json(params: dict[str, str | int]) -> dict:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{COMMONS_API}?{query}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def commons_candidates(query: str) -> list[dict]:
    payload = api_json({
        "action": "query", "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 20,
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1200, "format": "json", "formatversion": 2, "origin": "*",
    })
    return payload.get("query", {}).get("pages", [])


def commons_file(title: str) -> dict:
    payload = api_json({
        "action": "query", "titles": title, "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1200,
        "format": "json", "formatversion": 2, "origin": "*",
    })
    page = payload.get("query", {}).get("pages", [{}])[0]
    if not page.get("imageinfo"):
        raise RuntimeError(f"Pinned Commons image was not found: {title}")
    return page


def is_reusable(info: dict) -> bool:
    metadata = info.get("extmetadata", {})
    license_name = metadata.get("LicenseShortName", {}).get("value", "")
    usage_terms = metadata.get("UsageTerms", {}).get("value", "")
    license_text = f"{license_name} {usage_terms}".lower()
    return "creative commons" in license_text or "cc " in license_text or "public domain" in license_text


def choose_image(queries: list[str], used_titles: set[str]) -> tuple[dict, str]:
    fallback = None
    for query in queries:
        for page in commons_candidates(query):
            title = page.get("title", "")
            lowered = title.lower()
            info = (page.get("imageinfo") or [{}])[0]
            if title in used_titles or any(word in lowered for word in BLOCKED_TITLE_WORDS):
                continue
            if info.get("mime") not in {"image/jpeg", "image/png", "image/webp"}:
                continue
            if not is_reusable(info):
                continue
            candidate = (page, query)
            if info.get("width", 0) >= 800 and info.get("height", 0) >= 500:
                return candidate
            fallback = fallback or candidate
        time.sleep(0.1)
    if fallback:
        return fallback
    raise RuntimeError(f"No reusable image found for searches: {queries!r}")


def extension_for(info: dict) -> str:
    mime = info.get("mime", "image/jpeg")
    return {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(
        mime, mimetypes.guess_extension(mime) or ".jpg"
    )


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(5 * 1024 * 1024 + 1)
    if not data or len(data) > 5 * 1024 * 1024:
        raise RuntimeError(f"Image is empty or larger than 5 MB: {url}")
    destination.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--replace", nargs="*", type=int, default=[],
        help="Plant IDs to download again after reviewing search results",
    )
    args = parser.parse_args()
    args.image_dir.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(args.database)
    connection.row_factory = sqlite3.Row
    plants = connection.execute(
        "SELECT id, common_name, scientific_name, slug FROM plant_references ORDER BY id"
    ).fetchall()
    existing_rows = {
        row["plant_reference_id"]: row["filename"]
        for row in connection.execute("SELECT plant_reference_id, filename FROM plant_images")
    }
    existing_manifest = {}
    if args.manifest.exists():
        existing_manifest = {
            item["plant_reference_id"]: item
            for item in json.loads(args.manifest.read_text())["images"]
        }

    replace_ids = set(args.replace)
    used_titles = {
        item["commons_title"] for plant_id, item in existing_manifest.items()
        if plant_id not in replace_ids
    }
    records = []
    for plant in plants:
        if (
            plant["id"] not in replace_ids
            and plant["id"] in existing_rows
            and plant["id"] in existing_manifest
        ):
            records.append(existing_manifest[plant["id"]])
            continue

        primary = SEARCH_OVERRIDES.get(
            plant["common_name"], f'{plant["common_name"]} {plant["scientific_name"]} plant'
        )
        queries = [primary, f'{plant["scientific_name"]} plant', plant["common_name"]]
        if plant["id"] in PINNED_TITLES:
            page = commons_file(PINNED_TITLES[plant["id"]])
            matched_query = "reviewed Commons file"
        else:
            page, matched_query = choose_image(list(dict.fromkeys(queries)), used_titles)
        info = page["imageinfo"][0]
        metadata = info.get("extmetadata", {})
        filename = f'{plant["id"]:02d}-{plant["slug"]}{extension_for(info)}'
        destination = args.image_dir / filename
        download(info.get("thumburl") or info["url"], destination)

        old_filename = existing_rows.get(plant["id"])
        if old_filename and old_filename != filename:
            (args.image_dir / old_filename).unlink(missing_ok=True)

        connection.execute("DELETE FROM plant_images WHERE plant_reference_id = ?", (plant["id"],))
        connection.execute(
            "INSERT INTO plant_images (plant_reference_id, filename) VALUES (?, ?)",
            (plant["id"], filename),
        )
        used_titles.add(page["title"])
        records.append({
            "plant_reference_id": plant["id"], "plant": plant["common_name"],
            "filename": filename, "matched_query": matched_query,
            "commons_title": page["title"], "description_url": info.get("descriptionurl"),
            "original_url": info.get("url"),
            "creator": clean_html(metadata.get("Artist", {}).get("value", "Unknown")),
            "credit": clean_html(metadata.get("Credit", {}).get("value", "")),
            "license": clean_html(metadata.get("LicenseShortName", {}).get("value", "")),
            "license_url": metadata.get("LicenseUrl", {}).get("value"),
        })
        print(f'{plant["id"]:02d}/{len(plants)} {plant["common_name"]}: {page["title"]}')
        time.sleep(0.15)

    connection.commit()
    connection.close()
    manifest = {
        "format": "my-garden-plant-image-sources-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Wikimedia Commons", "images": records,
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Linked {len(records)} images and wrote {args.manifest}")


if __name__ == "__main__":
    main()
