from __future__ import annotations

import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = PROJECT_ROOT / "src" / "config" / "oecd_ai_report_2026.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "oecd_ai_benchmarks_2026.csv"
FIELDS = ["year", "geography", "metric", "value", "unit", "precision", "source_publisher", "source_publication_date", "source_url", "underlying_provider", "evidence", "note"]


def main() -> None:
    source = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    observations = source["observations"]
    records = []
    for item in observations:
        records.append({
            "year": int(item["year"]),
            "geography": item["geography"],
            "metric": item["metric"],
            "value": item["value"],
            "unit": item["unit"],
            "precision": item["precision"],
            "source_publisher": source["publisher"],
            "source_publication_date": source["publication_date"],
            "source_url": source["source_url"],
            "underlying_provider": source["underlying_provider"],
            "evidence": item["evidence"],
            "note": item["note"],
        })
    records.sort(key=lambda r: (r["year"], r["geography"], r["metric"]))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} source-attributed observations to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()