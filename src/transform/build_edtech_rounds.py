from __future__ import annotations
import csv
import json
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT_ROOT / "src/config/edtech_verified_rounds_2022_2025.json"
OUTPUT = PROJECT_ROOT / "data/processed/edtech_verified_rounds_2022_2025.csv"
COLUMNS = [
    "round_id", "company_id", "company_name", "source_publication_date",
    "year", "quarter", "analysis_period", "round_stage_reported", "stage_group",
    "round_amount_usd_millions", "currency", "subsector", "ai_product_role",
    "lead_investor", "funding_source_url", "ai_evidence_url", "source_type",
]


def classify_period(date_string: str) -> str:
    d = date.fromisoformat(date_string)
    if d < date(2022, 10, 1):
        return "Pre-GPT"
    if d < date(2023, 1, 1):
        return "Transition"
    return "Post-GPT"


def stage_group(stage: str) -> str:
    if stage == "Seed":
        return "Seed"
    if stage in ("Series A", "Series B", "Series B-2", "Series B-3"):
        return "Early"
    if stage == "Series C":
        return "Late/Growth"
    if stage == "Unspecified":
        return "Unspecified"
    raise ValueError(f"Unexpected source funding stage: {stage!r}")


def build_dataset(observations: list[dict]) -> list[dict]:
    """Transform manually verified funding disclosures into fact rows."""
    rows=[]
    for original in observations:
        d=date.fromisoformat(original["source_publication_date"])
        row={**original,
             "year":d.year,
             "quarter":f"Q{(d.month-1)//3+1}",
             "analysis_period":classify_period(original["source_publication_date"]),
             "stage_group":stage_group(original["round_stage_reported"]),
        }
        rows.append({name:row.get(name) for name in COLUMNS})
    return sorted(rows,key=lambda r:(r["source_publication_date"],r["round_id"]))


def write_dataset(rows: list[dict], destination: Path = OUTPUT) -> None:
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open("w",encoding="utf-8",newline="") as file:
        writer=csv.DictWriter(file,fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    manifest=json.loads(SOURCE.read_text(encoding="utf-8"))
    rows=build_dataset(manifest["observations"])
    write_dataset(rows)
    print(f"Created: {OUTPUT}")
    print(f"Rounds: {len(rows)}; Companies: {len({r['company_id'] for r in rows})}")
    print(f"Purposeful sample amount: ${sum(float(r['round_amount_usd_millions']) for r in rows):,.1f}M (NOT market total)")

if __name__ == "__main__":
    main()