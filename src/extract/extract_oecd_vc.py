from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

START_YEAR = 2019
END_YEAR = 2025

DATAFLOW = "OECD.SDD.TPS"
DATASET = "DSD_VC@DF_VC_INV"
VERSION = "1.0"

# Query:
# - all reference areas
# - all business-development stages
# - USD, exchange-rate converted
# - annual frequency
QUERY = "...USD_EXC.A"

BASE_URL = (
    "https://sdmx.oecd.org/public/rest/data/"
    f"{DATAFLOW},{DATASET},{VERSION}/{QUERY}"
)

PARAMS = {
    "startPeriod": START_YEAR,
    "endPeriod": END_YEAR,
    "dimensionAtObservation": "AllDimensions",
    "format": "csvfilewithlabels",
}

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "oecd_vc"

RAW_FILE = RAW_DIR / f"oecd_vc_investments_{START_YEAR}_{END_YEAR}_raw.csv"
METADATA_FILE = RAW_DIR / f"oecd_vc_investments_{START_YEAR}_{END_YEAR}_metadata.json"

def download_oecd_vc_data() -> tuple[bytes, str]:
    headers = {
        "User-Agent": "vc-market-intelligence-powerbi/1.0"
    }

    response = requests.get(
        BASE_URL,
        params=PARAMS,
        headers=headers,
        timeout=60,
    )

    response.raise_for_status()

    content = response.content

    if not content:
        raise ValueError("OECD API returned an empty response.")

    preview = content[:500].lower()

    if b"<html" in preview or b"<!doctype html" in preview:
        raise ValueError(
            "OECD API returned HTML instead of the expected CSV response."
        )

    return content, response.url


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def save_raw_data(content: bytes) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RAW_FILE.write_bytes(content)


def save_metadata(content: bytes, source_url: str) -> None:
    metadata = {
        "provider": "OECD",
        "dataset": "Venture capital investments (market statistics)",
        "dataflow": DATAFLOW,
        "dataset_id": DATASET,
        "dataset_version": VERSION,
        "start_year": START_YEAR,
        "end_year": END_YEAR,
        "frequency": "Annual",
        "unit_filter": "USD, exchange-rate converted",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "raw_file": RAW_FILE.name,
        "file_size_bytes": len(content),
        "sha256": calculate_sha256(content),
    }

    METADATA_FILE.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    print("Downloading OECD venture capital data...")

    content, source_url = download_oecd_vc_data()

    save_raw_data(content)
    save_metadata(content, source_url)

    print("Download complete.")
    print(f"Raw data: {RAW_FILE}")
    print(f"Metadata: {METADATA_FILE}")
    print(f"SHA-256: {calculate_sha256(content)}")


if __name__ == "__main__":
    main()