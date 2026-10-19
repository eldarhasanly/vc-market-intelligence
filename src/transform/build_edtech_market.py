from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = ROOT / "data/raw/edtech/holoniq_2026_outlook_2019_2025_local.csv"
OUTPUT_FILE = ROOT / "data/processed/edtech_vc_holoniq_2019_2025_local.csv"

EXPECTED_YEARS = set(range(2019, 2026))
SOURCE_URL = "https://www.holoniq.com/notes/2026-global-education-outlook"
SOURCE_PUBLICATION_DATE = "2025-12-19"


def build_dataset(raw: pd.DataFrame) -> pd.DataFrame:
    """Normalize and annotate a frozen HolonIQ chart transcription."""
    expected_columns = {"year", "edtech_vc_usd_billions"}
    if set(raw.columns) != expected_columns:
        raise ValueError(
            f"Expected columns {sorted(expected_columns)}, found {sorted(raw.columns)}"
        )

    if raw.empty:
        raise ValueError("Input contains no observations")

    output = raw.copy()
    output["year"] = pd.to_numeric(output["year"], errors="raise")
    if output["year"].isna().any() or not (output["year"] % 1 == 0).all():
        raise ValueError("Year must be a non-null integer")
    output["year"] = output["year"].astype(int)

    output["edtech_vc_usd_billions"] = pd.to_numeric(
        output["edtech_vc_usd_billions"], errors="raise"
    )
    if not output["edtech_vc_usd_billions"].notna().all():
        raise ValueError("Funding contains null values")
    if not output["edtech_vc_usd_billions"].map(lambda x: pd.notna(x) and x >= 0 and x < float("inf")).all():
        raise ValueError("Funding contains invalid, infinite, or negative values")

    if output["year"].duplicated().any():
        raise ValueError("Duplicate years found")
    if set(output["year"]) != EXPECTED_YEARS:
        raise ValueError(
            f"Year coverage must be 2019–2025; found {sorted(output['year'].tolist())}"
        )

    output["metric_code"] = "EDTECH_VC_INVESTMENT"
    output["geography"] = "Global (HolonIQ coverage)"
    output["currency"] = "USD"
    output["price_basis"] = "Nominal USD; historical FX at funding date"
    output["capital_type"] = "Venture capital (excludes private equity)"
    output["value_precision"] = "Reported chart figures; rounded to USD 0.1B"
    output["source_provider"] = "HolonIQ"
    output["source_publication_date"] = SOURCE_PUBLICATION_DATE
    output["source_url"] = SOURCE_URL
    output["source_chart"] = "Figure 2: Global Education Venture Capital Funding, 2010–2025"
    output["series_vintage"] = "2026 Global Education Outlook (December 2025 release)"
    output = output.sort_values("year").reset_index(drop=True)
    return output


def main() -> None:
    if not INPUT_FILE.is_file():
        raise FileNotFoundError(
            f"Missing local HolonIQ chart transcription: {INPUT_FILE}\n"
            "Place the source snapshot in data/raw/edtech/; see docs/edtech_market_methodology.md."
        )
    processed = build_dataset(pd.read_csv(INPUT_FILE))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(OUTPUT_FILE, index=False)
    print(f"Built local EdTech benchmark: {OUTPUT_FILE}")
    print(f"Years: {processed['year'].min()}–{processed['year'].max()} | Rows: {len(processed)}")
    print("Source vintage: December 2025 HolonIQ Global Education Outlook")
    print("Note: provider-derived rows remain local; do not commit this CSV.")


if __name__ == "__main__":
    main()