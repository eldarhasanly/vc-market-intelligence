from __future__ import annotations

import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data/processed/edtech_vc_holoniq_2019_2025_local.csv"

EXPECTED_YEARS = set(range(2019, 2026))
REQUIRED_COLUMNS = {
    "year", "edtech_vc_usd_billions", "metric_code", "geography", "currency",
    "price_basis", "capital_type", "value_precision", "source_provider",
    "source_publication_date", "source_url", "source_chart", "series_vintage",
}


def validate_frame(df: pd.DataFrame) -> None:
    if set(df.columns) != REQUIRED_COLUMNS:
        raise AssertionError(f"Unexpected schema: {sorted(set(df.columns) ^ REQUIRED_COLUMNS)}")
    if len(df) != 7:
        raise AssertionError(f"Expected 7 annual rows, received {len(df)}")
    if df["year"].isna().any() or df["year"].duplicated().any():
        raise AssertionError("Missing or duplicate years")
    if set(df["year"]) != EXPECTED_YEARS:
        raise AssertionError("Missing or unexpected years")
    if df.isna().any().any():
        raise AssertionError("Unexpected null field")
    if not all(math.isfinite(float(v)) and float(v) >= 0 for v in df["edtech_vc_usd_billions"]):
        raise AssertionError("Invalid funding values")
    constants = {
        "metric_code": "EDTECH_VC_INVESTMENT",
        "source_provider": "HolonIQ",
        "source_publication_date": "2025-12-19",
        "currency": "USD",
        "source_url": "https://www.holoniq.com/notes/2026-global-education-outlook",
    }
    for field, expected in constants.items():
        if set(df[field]) != {expected}:
            raise AssertionError(f"Inconsistent {field} value")


def main() -> None:
    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Missing: {DATA_FILE}; run build_edtech_market.py first")
    df = pd.read_csv(DATA_FILE)
    validate_frame(df)
    print("EdTech market benchmark validation: PASSED (7 annual observations, 2019–2025)")
    print("Publication snapshot: 2025-12-19 | Amounts: nominal USD billions")
    print("Warning: not licensed for automatic redistribution in this repository")


if __name__ == "__main__":
    main()