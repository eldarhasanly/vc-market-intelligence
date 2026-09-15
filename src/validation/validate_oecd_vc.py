from __future__ import annotations

from pathlib import Path
import pandas as pd

START_YEAR = 2019
END_YEAR = 2025

EXPECTED_STAGES = {
    "_T": "Total",
    "SEED": "Seed",
    "START": "Start-up and other early stage",
    "LATER": "Later stage venture",
}

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / f"oecd_vc_annual_{START_YEAR}_{END_YEAR}.csv"
)

REQUIRED_COLUMNS = {
    "source_provider",
    "source_dataset_id",
    "country_code",
    "country",
    "stage_code",
    "stage",
    "year",
    "vc_investment_usd_millions",
    "observation_status_code",
    "observation_status",
    "unit_code",
    "unit",
    "unit_multiplier_code",
    "unit_multiplier",
    "currency_code",
    "currency",
}

def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_FILE}\n"
            "Run src/transform/transform_oecd_vc.py first."
        )

    return pd.read_csv(DATA_FILE)

def validate_required_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(df.columns)

    if missing:
        raise AssertionError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

def validate_keys(df: pd.DataFrame) -> None:
    key_columns = [
        "country_code",
        "stage_code",
        "year",
    ]

    if df[key_columns].isna().any().any():
        raise AssertionError("Analytical key contains missing values.")

    duplicate_count = df.duplicated(
        subset=key_columns
    ).sum()

    if duplicate_count:
        raise AssertionError(
            f"Found {duplicate_count} duplicate analytical keys."
        )

def validate_values(df: pd.DataFrame) -> None:
    investment = df["vc_investment_usd_millions"]

    if investment.isna().any():
        raise AssertionError(
            "Investment measure contains missing values."
        )

    negative_count = (investment < 0).sum()

    if negative_count:
        raise AssertionError(
            f"Found {negative_count} negative investment values."
        )

def validate_time_scope(df: pd.DataFrame) -> None:
    expected_years = set(range(START_YEAR, END_YEAR + 1))
    actual_years = set(df["year"].unique())

    if actual_years != expected_years:
        raise AssertionError(
            f"Unexpected year coverage. "
            f"Expected {sorted(expected_years)}, "
            f"found {sorted(actual_years)}."
        )

def validate_stages(df: pd.DataFrame) -> None:
    actual_stages = set(df["stage_code"].unique())
    expected_stages = set(EXPECTED_STAGES)

    unexpected = actual_stages - expected_stages
    missing = expected_stages - actual_stages

    if unexpected:
        raise AssertionError(
            f"Unexpected stage codes: {sorted(unexpected)}"
        )

    if missing:
        raise AssertionError(
            f"Expected stage codes not found: {sorted(missing)}"
        )

def validate_units(df: pd.DataFrame) -> None:
    expectations = {
        "source_provider": {"OECD"},
        "unit_code": {"USD_EXC"},
        "unit_multiplier_code": {6},
        "currency_code": {"USD"},
    }

    for column, expected_values in expectations.items():
        actual_values = set(df[column].dropna().unique())

        if actual_values != expected_values:
            raise AssertionError(
                f"Unexpected values in {column}: {actual_values}. "
                f"Expected: {expected_values}."
            )

def print_coverage_report(df: pd.DataFrame) -> None:
    countries = df["country_code"].nunique()
    years = df["year"].nunique()
    stages = df["stage_code"].nunique()

    theoretical_rows = countries * years * stages
    observed_rows = len(df)
    missing_combinations = theoretical_rows - observed_rows

    print("\nCoverage")
    print("--------")
    print(f"Countries: {countries}")
    print(f"Years: {years}")
    print(f"Stages: {stages}")
    print(f"Observed rows: {observed_rows:,}")
    print(f"Possible country-year-stage combinations: {theoretical_rows:,}")
    print(f"Unreported combinations: {missing_combinations:,}")
    print(
        f"Panel coverage: "
        f"{observed_rows / theoretical_rows:.1%}"
    )

    print("\nRows by stage")
    print("-------------")

    stage_counts = (
        df.groupby(["stage_code", "stage"])
        .size()
        .sort_values(ascending=False)
    )

    for (code, stage), count in stage_counts.items():
        print(f"{code:>5} | {stage:<35} | {count:>4}")

def print_zero_report(df: pd.DataFrame) -> None:
    zero_count = (
        df["vc_investment_usd_millions"] == 0
    ).sum()

    print("\nZero-value observations")
    print("-----------------------")
    print(f"Zero values: {zero_count:,}")
    print(
        "Zero observations are retained as valid reported values."
    )

def check_total_consistency(df: pd.DataFrame) -> None:
    pivot = df.pivot_table(
        index=["country_code", "country", "year"],
        columns="stage_code",
        values="vc_investment_usd_millions",
        aggfunc="first",
    )

    required = ["_T", "SEED", "START", "LATER"]

    comparable = pivot.dropna(subset=required).copy()

    if comparable.empty:
        print("\nTotal consistency")
        print("-----------------")
        print("No complete country-year groups available.")
        return

    comparable["component_sum"] = (
        comparable["SEED"]
        + comparable["START"]
        + comparable["LATER"]
    )

    comparable["difference"] = (
        comparable["_T"] - comparable["component_sum"]
    ).abs()

    tolerance = 0.05

    mismatches = comparable[
        comparable["difference"] > tolerance
    ]

    print("\nTotal consistency")
    print("-----------------")
    print(
        f"Comparable country-year groups: {len(comparable):,}"
    )
    print(
        f"Groups differing by more than "
        f"${tolerance:.2f}M: {len(mismatches):,}"
    )

    if len(mismatches):
        print(
            "Note: differences are reported diagnostically and "
            "are not automatically treated as source errors."
        )


def main() -> None:
    print("Validating processed OECD VC data...")

    df = load_data()

    validate_required_columns(df)
    validate_keys(df)
    validate_values(df)
    validate_time_scope(df)
    validate_stages(df)
    validate_units(df)

    print("\nHard validation checks: PASSED")

    print_coverage_report(df)
    print_zero_report(df)
    check_total_consistency(df)

    print("\nValidation complete.")


if __name__ == "__main__":
    main()