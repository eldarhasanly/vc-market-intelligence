from __future__ import annotations

from pathlib import Path
import pandas as pd

START_YEAR = 2019
END_YEAR = 2025

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "oecd_vc"
    / f"oecd_vc_investments_{START_YEAR}_{END_YEAR}_raw.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    PROCESSED_DIR
    / f"oecd_vc_annual_{START_YEAR}_{END_YEAR}.csv"
)


REQUIRED_COLUMNS = {
    "STRUCTURE_ID",
    "REF_AREA",
    "Reference area",
    "MEASURE",
    "BUSINESS_DEVELOPMENT_STAGE",
    "Business development stage",
    "UNIT_MEASURE",
    "Unit of measure",
    "FREQ",
    "TIME_PERIOD",
    "OBS_VALUE",
    "OBS_STATUS",
    "Observation status",
    "UNIT_MULT",
    "Unit multiplier",
    "CURRENCY",
    "Currency",
}


COLUMN_MAPPING = {
    "STRUCTURE_ID": "source_dataset_id",
    "REF_AREA": "country_code",
    "Reference area": "country",
    "BUSINESS_DEVELOPMENT_STAGE": "stage_code",
    "Business development stage": "stage",
    "TIME_PERIOD": "year",
    "OBS_VALUE": "vc_investment_usd_millions",
    "OBS_STATUS": "observation_status_code",
    "Observation status": "observation_status",
    "UNIT_MEASURE": "unit_code",
    "Unit of measure": "unit",
    "UNIT_MULT": "unit_multiplier_code",
    "Unit multiplier": "unit_multiplier",
    "CURRENCY": "currency_code",
    "Currency": "currency",
}


def load_raw_data() -> pd.DataFrame:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw OECD file not found: {RAW_FILE}\n"
            "Run src/extract/extract_oecd_vc.py first."
        )

    return pd.read_csv(
        RAW_FILE,
        dtype={
            "REF_AREA": "string",
            "BUSINESS_DEVELOPMENT_STAGE": "string",
            "MEASURE": "string",
            "UNIT_MEASURE": "string",
            "FREQ": "string",
            "OBS_STATUS": "string",
            "CURRENCY": "string",
        },
    )


def validate_schema(df: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required OECD columns: "
            + ", ".join(sorted(missing_columns))
        )


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    validate_schema(df)

    filtered = df.loc[
        (df["MEASURE"] == "VC_INV_MKT")
        & (df["UNIT_MEASURE"] == "USD_EXC")
        & (df["FREQ"] == "A")
    ].copy()

    processed = filtered[list(COLUMN_MAPPING)].rename(
        columns=COLUMN_MAPPING
    )

    processed["year"] = pd.to_numeric(
        processed["year"],
        errors="raise",
    ).astype("int64")

    processed["vc_investment_usd_millions"] = pd.to_numeric(
        processed["vc_investment_usd_millions"],
        errors="coerce",
    )

    processed = processed.loc[
        processed["year"].between(START_YEAR, END_YEAR)
    ].copy()

    processed.insert(0, "source_provider", "OECD")

    key_columns = [
        "country_code",
        "stage_code",
        "year",
    ]

    duplicate_count = processed.duplicated(
        subset=key_columns,
        keep=False,
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} rows with duplicate analytical keys."
        )

    processed = processed.sort_values(
        ["country", "year", "stage_code"]
    ).reset_index(drop=True)

    return processed


def print_summary(df: pd.DataFrame) -> None:
    print("\nTransformation summary")
    print("----------------------")
    print(f"Rows: {len(df):,}")
    print(f"Countries: {df['country_code'].nunique():,}")
    print(
        f"Years: {df['year'].min()}–{df['year'].max()}"
    )
    print(
        "Missing investment values: "
        f"{df['vc_investment_usd_millions'].isna().sum():,}"
    )

    print("\nStages:")
    for code, label in (
        df[["stage_code", "stage"]]
        .drop_duplicates()
        .sort_values("stage_code")
        .itertuples(index=False, name=None)
    ):
        print(f"  {code}: {label}")

    print("\nObservation statuses:")
    for code, label in (
        df[
            [
                "observation_status_code",
                "observation_status",
            ]
        ]
        .drop_duplicates()
        .sort_values("observation_status_code")
        .itertuples(index=False, name=None)
    ):
        print(f"  {code}: {label}")


def save_processed_data(df: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )


def main() -> None:
    print("Loading raw OECD VC data...")

    raw = load_raw_data()

    print(f"Raw rows: {len(raw):,}")

    processed = transform_data(raw)

    save_processed_data(processed)

    print_summary(processed)

    print(f"\nProcessed file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()