from __future__ import annotations

from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed" / "owid_private_ai_genai_2019_2025.csv"
YEARS = set(range(2019, 2026))
METRICS = {"private_ai_investment", "private_genai_investment"}
REQUIRED = {
    "year", "geography", "metric", "value_usd_bn_2021_prices", "unit",
    "source_provider", "original_provider", "source_url", "original_indicator"
}


def validate(df: pd.DataFrame) -> None:
    missing_cols = REQUIRED - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {sorted(missing_cols)}")
    if df[sorted(REQUIRED)].isna().any().any():
        raise ValueError("Null fields detected")
    if len(df) != 14:
        raise ValueError(f"Expected 14 rows (7 years × 2 metrics), got {len(df)}")
    if df.duplicated(["year", "geography", "metric"]).any():
        raise ValueError("Duplicate year/geography/metric analytical keys")
    if set(df["metric"]) != METRICS:
        raise ValueError("Missing or unexpected investment metric")
    if set(df["geography"]) != {"World"}:
        raise ValueError("Unexpected geographic scope")
    if set(df["unit"]) != {"constant_2021_USD_billions"}:
        raise ValueError("Incompatible currency/price basis")
    if set(df["source_provider"]) != {"Our World in Data"}:
        raise ValueError("Unexpected source provider")
    for metric, sub in df.groupby("metric"):
        if set(sub["year"]) != YEARS:
            raise ValueError(f"Incomplete coverage for {metric}")
    amounts = pd.to_numeric(df["value_usd_bn_2021_prices"], errors="raise")
    if amounts.isna().any() or not amounts.map(math.isfinite).all() or (amounts < 0).any():
        raise ValueError("Investment amounts are missing, nonfinite or negative")
    if not df["source_url"].astype(str).str.startswith("https://ourworldindata.org/grapher/").all():
        raise ValueError("Unexpected source URLs")


def main() -> None:
    if not DATA.exists():
        raise FileNotFoundError(f"Missing processed CSV: {DATA}; run the transformation first")
    validate(pd.read_csv(DATA))
    print("OWID AI/GenAI time-series validation: PASSED (14 observations, 2019–2025).")
    print("Do not sum these series with OECD nominal VC figures or assume VC-only coverage.")


if __name__ == "__main__":
    main()