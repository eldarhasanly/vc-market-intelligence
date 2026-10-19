from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "owid"
SERIES = {
    "private_ai_investment": "private-investment-in-artificial-intelligence",
    "private_genai_investment": "global-investment-in-generative-ai",
}


def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "VCMarketIntelligencePortfolio/1.0 (educational research)"})
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch(session: requests.Session, url: str, kind: str) -> bytes:
    response = session.get(url, timeout=(10, 60))
    response.raise_for_status()
    content = response.content
    if not content:
        raise ValueError(f"Empty {kind} response: {url}")
    if kind == "CSV":
        header = content[:2500].decode("utf-8-sig", errors="replace").splitlines()[0]
        if "Entity" not in header or "Year" not in header:
            raise ValueError(f"Unexpected CSV schema in {url}: {header[:200]}")
    else:
        if not isinstance(json.loads(content), dict):
            raise ValueError(f"Unexpected metadata JSON in {url}")
    return content


def save_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    query = urlencode({"v": 1, "csvType": "full", "useColumnShortNames": "false"})
    manifest = {"retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "datasets": {}}
    with get_session() as session:
        for metric, slug in SERIES.items():
            root = f"https://ourworldindata.org/grapher/{slug}"
            csv_url = f"{root}.csv?{query}"
            meta_url = f"{root}.metadata.json?{query}"
            csv_content = fetch(session, csv_url, "CSV")
            meta_content = fetch(session, meta_url, "JSON")
            csv_path = RAW_DIR / f"{slug}.csv"
            meta_path = RAW_DIR / f"{slug}.metadata.json"
            save_bytes(csv_path, csv_content)
            save_bytes(meta_path, meta_content)
            manifest["datasets"][metric] = {
                "slug": slug,
                "csv_url": csv_url,
                "metadata_url": meta_url,
                "csv_sha256": hashlib.sha256(csv_content).hexdigest(),
                "metadata_sha256": hashlib.sha256(meta_content).hexdigest(),
                "csv_bytes": len(csv_content),
                "metadata_bytes": len(meta_content),
            }
            print(f"Downloaded {metric}: {len(csv_content):,} CSV bytes")
    save_bytes(RAW_DIR / "extraction_manifest.json", json.dumps(manifest, indent=2).encode("utf-8"))
    print("Raw downloads and SHA-256 manifest saved to data/raw/owid/")


if __name__ == "__main__":
    main()