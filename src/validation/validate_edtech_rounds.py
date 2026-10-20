from __future__ import annotations
import csv
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from src.transform.build_edtech_rounds import SOURCE, OUTPUT, COLUMNS, build_dataset


def validate_dataset(rows: list[dict], manifest: dict) -> None:
    if not rows:
        raise AssertionError("Dataset is empty")
    if len(rows) != len(manifest.get("observations",[])):
        raise AssertionError("Record count does not match source manifest")
    ids = [r["round_id"] for r in rows]
    if len(set(ids)) != len(ids):
        raise AssertionError("Duplicate round IDs")
    triples=set()
    for r in rows:
        if set(r)!=set(COLUMNS):
            raise AssertionError(f"Schema mismatch for {r.get('round_id')}")
        day=date.fromisoformat(r["source_publication_date"])
        if not 2022 <= day.year <= 2025:
            raise AssertionError("Year outside 2022-2025")
        if int(r["year"])!=day.year:
            raise AssertionError("Year differs from date")
        if r["quarter"] != f"Q{(day.month-1)//3+1}":
            raise AssertionError("Quarter differs from date")
        if r["currency"] != "USD":
            raise AssertionError("Unsupported currency")
        amount=float(r["round_amount_usd_millions"])
        if not 0 < amount < 10000:
            raise AssertionError("Invalid single-round amount")
        if r["ai_product_role"] not in {"AI-native", "AI-enabled"}:
            raise AssertionError("Unexpected AI product role")
        if r["stage_group"] not in {"Seed", "Early", "Late/Growth", "Unspecified"}:
            raise AssertionError("Unexpected stage group")
        for field in ("funding_source_url","ai_evidence_url"):
            link=urlparse(r[field])
            if link.scheme!="https" or not link.netloc:
                raise AssertionError(f"Invalid {field}")
        key=(r["company_id"],r["source_publication_date"],r["round_stage_reported"])
        if key in triples:
            raise AssertionError(f"Duplicate company/date/stage: {key}")
        triples.add(key)
    source_rows=build_dataset(manifest["observations"])
    for source_row, actual_row in zip(source_rows,rows):
        for name in COLUMNS:
            if str(source_row[name] if source_row[name] is not None else "") != str(actual_row[name] if actual_row[name] is not None else ""):
                raise AssertionError(f"CSV differs from manifest for {name} on {source_row['round_id']}")


def main() -> None:
    manifest=json.loads(SOURCE.read_text(encoding="utf-8"))
    if not OUTPUT.exists():
        raise FileNotFoundError("Run python src/transform/build_edtech_rounds.py first")
    with OUTPUT.open(encoding="utf-8-sig",newline="") as file:
        rows=list(csv.DictReader(file))
    validate_dataset(rows,manifest)
    print(f"EdTech funding-round validation: PASSED ({len(rows)} rounds; {len({r['company_id'] for r in rows})} companies)")
    print("Warning: purposeful case-study sample, NOT a market-complete funding series.")

if __name__ == "__main__":
    main()