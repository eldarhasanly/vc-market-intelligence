from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUTS = {
    "oecd_vc": "data/processed/oecd_vc_annual_2019_2025.csv",
    "oecd_ai": "data/processed/oecd_ai_benchmarks_2026.csv",
    "owid": "data/processed/owid_private_ai_genai_2019_2025.csv",
    "edtech_market": "data/processed/edtech_vc_holoniq_2019_2025_local.csv",
    "edtech_rounds": "data/processed/edtech_verified_rounds_2022_2025.csv",
}
MART_DIR = ROOT / "data" / "mart" / "powerbi"
STAGES = {"SEED", "START", "LATER"}
REQUIRED = {
    "oecd_vc": {"country_code", "country", "year", "stage_code", "stage", "vc_investment_usd_millions", "source_provider", "unit_code", "unit_multiplier_code", "currency_code"},
    "oecd_ai": {"year", "geography", "metric", "value", "unit", "source_publisher", "source_url"},
    "owid": {"year", "geography", "metric", "value_usd_bn_2021_prices", "unit", "source_provider", "source_url"},
    "edtech_market": {"year", "edtech_vc_usd_billions", "geography", "currency", "source_provider", "source_publication_date", "source_url", "series_vintage"},
    "edtech_rounds": {"round_id", "company_id", "company_name", "source_publication_date", "year", "quarter", "analysis_period", "round_stage_reported", "stage_group", "round_amount_usd_millions", "currency", "subsector", "ai_product_role", "lead_investor", "funding_source_url", "ai_evidence_url", "source_type"},
}


def read_sources(root: Path = ROOT) -> dict[str, pd.DataFrame]:
    missing = [rel for rel in INPUTS.values() if not (root / rel).is_file()]
    if missing:
        lines = "\n".join(f"  - {name}" for name in missing)
        raise FileNotFoundError(
            "Processed input(s) missing:\n" + lines +
            "\nRe-run the relevant extraction/transformation pipelines first.\n"
            "The HolonIQ local source snapshot must exist in data/raw/edtech/."
        )
    return {name: pd.read_csv(root / rel, low_memory=False) for name, rel in INPUTS.items()}


def _check_columns(name: str, df: pd.DataFrame) -> None:
    absent = REQUIRED[name] - set(df.columns)
    if absent:
        raise ValueError(f"{name}: missing required columns {sorted(absent)}")
    if df.empty:
        raise ValueError(f"{name}: input is empty")


def _numeric(df: pd.DataFrame, column: str, name: str, *, positive: bool = False) -> None:
    numbers = pd.to_numeric(df[column], errors="coerce")
    if numbers.isna().any() or not pd.Series(numbers).map(lambda x: pd.notna(x) and float("-inf") < float(x) < float("inf")).all():
        raise ValueError(f"{name}: non-numeric or missing {column}")
    if (numbers <= 0 if positive else numbers < 0).any():
        raise ValueError(f"{name}: unexpected nonpositive/negative {column}")


def _check_years(df: pd.DataFrame, name: str) -> None:
    years = pd.to_numeric(df["year"], errors="coerce")
    if years.isna().any() or not years.between(2019, 2025).all() or not (years % 1 == 0).all():
        raise ValueError(f"{name}: years must be integers within 2019–2025")


def _unique(df: pd.DataFrame, columns: list[str], name: str) -> None:
    if df[columns].isna().any().any() or df.duplicated(columns).any():
        raise ValueError(f"{name}: duplicate/null key {columns}")


def build_marts(sources: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Return local BI-ready tables without joining incompatible source universes."""
    for name, df in sources.items():
        if name not in REQUIRED:
            raise ValueError(f"Unrecognized source: {name}")
        _check_columns(name, df)
        _check_years(df, name)

    vc = sources["oecd_vc"].copy()
    _unique(vc, ["country_code", "year", "stage_code"], "oecd_vc")
    if not set(vc["stage_code"]).issubset(STAGES | {"_T"}):
        raise ValueError("oecd_vc: unknown stage classification")
    if set(vc["unit_code"]) != {"USD_EXC"} or set(vc["currency_code"]) != {"USD"} or set(vc["unit_multiplier_code"].astype(str)) != {"6"}:
        raise ValueError("oecd_vc: currency/unit inconsistent with USD millions")
    _numeric(vc, "vc_investment_usd_millions", "oecd_vc")
    _unique(vc[["country_code", "country"]].drop_duplicates(), ["country_code"], "DimOECDCountry")
    _unique(vc[["stage_code", "stage"]].drop_duplicates(), ["stage_code"], "DimOECDStage")

    owid = sources["owid"].copy()
    _unique(owid, ["year", "geography", "metric"], "owid")
    if set(owid["unit"]) != {"constant_2021_USD_billions"} or set(owid["geography"]) != {"World"}:
        raise ValueError("owid: unexpected unit or geography")
    if set(owid["metric"]) != {"private_ai_investment", "private_genai_investment"}:
        raise ValueError("owid: unexpected AI private-investment metric")
    _numeric(owid, "value_usd_bn_2021_prices", "owid")

    ai = sources["oecd_ai"].copy()
    _unique(ai, ["year", "geography", "metric"], "oecd_ai")
    if not set(ai["unit"]).issubset({"USD_billions", "percent"}):
        raise ValueError("oecd_ai: unexpected unit")
    _numeric(ai, "value", "oecd_ai")
    if (pd.to_numeric(ai.loc[ai["unit"] == "percent", "value"]) > 100).any():
        raise ValueError("oecd_ai: percentage >100")

    edtech = sources["edtech_market"].copy()
    _unique(edtech, ["year"], "edtech_market")
    if set(edtech["currency"]) != {"USD"} or set(edtech["source_provider"]) != {"HolonIQ"}:
        raise ValueError("edtech_market: unexpected source/currency")
    _numeric(edtech, "edtech_vc_usd_billions", "edtech_market")

    rounds = sources["edtech_rounds"].copy()
    _unique(rounds, ["round_id"], "edtech_rounds")
    if set(rounds["currency"]) != {"USD"}:
        raise ValueError("edtech_rounds: unsupported currency")
    _numeric(rounds, "round_amount_usd_millions", "edtech_rounds", positive=True)
    companies = rounds[["company_id", "company_name", "subsector", "ai_product_role"]].drop_duplicates().copy()
    _unique(companies, ["company_id"], "DimEdTechCompany")
    edtech_stages = rounds[["stage_group"]].drop_duplicates().copy()
    _unique(edtech_stages, ["stage_group"], "DimEdTechStage")

    # Total (_T) and stage component rows are intentionally separate fact tables.
    base = ["country_code", "year", "vc_investment_usd_millions", "source_provider"]
    total = vc.loc[vc["stage_code"] == "_T", base].copy()
    stage = vc.loc[vc["stage_code"].isin(STAGES), base[:2] + ["stage_code"] + base[2:]].copy()
    # Exclude partially reported stage mixes from composition denominators.
    complete = (
        stage.groupby(["country_code", "year"])["stage_code"]
        .nunique().rename("stage_count").reset_index()
    )
    complete = complete.loc[complete["stage_count"] == len(STAGES), ["country_code", "year"]]
    stage = stage.merge(complete, on=["country_code", "year"], how="inner", validate="many_to_one")
    _unique(total, ["country_code", "year"], "FactOECDVCTotal")
    _unique(stage, ["country_code", "year", "stage_code"], "FactOECDVCStage")

    # Same-grain/compatible-source check: stage components reconcile with totals
    # only where the source has all 3 component stages for a country-year.
    parts = stage.pivot(index=["country_code", "year"], columns="stage_code", values="vc_investment_usd_millions")
    full = parts.dropna(subset=sorted(STAGES)) if set(STAGES).issubset(parts.columns) else pd.DataFrame()
    if not full.empty:
        recon = full[sorted(STAGES)].sum(axis=1).rename("components").reset_index().merge(
            total, on=["country_code", "year"], how="left", validate="one_to_one"
        )
        if recon["vc_investment_usd_millions"].isna().any():
            raise ValueError("Missing OECD total where complete stage components exist")
        if ((recon["components"] - recon["vc_investment_usd_millions"]).abs() > 0.05).any():
            raise ValueError("OECD component stages do not reconcile to published totals")

    years = pd.DataFrame({"year": list(range(2019, 2026))})
    years["year_label"] = years["year"].astype(str)
    tables = {
        "DimYear": years,
        "DimOECDCountry": vc[["country_code", "country"]].drop_duplicates().sort_values("country_code"),
        "DimOECDStage": vc.loc[vc["stage_code"].isin(STAGES), ["stage_code", "stage"]].drop_duplicates().sort_values("stage_code"),
        "DimEdTechCompany": companies.sort_values("company_id"),
        "DimEdTechStage": edtech_stages.sort_values("stage_group"),
        "FactOECDVCTotal": total.sort_values(["country_code", "year"]),
        "FactOECDVCStage": stage.sort_values(["country_code", "year", "stage_code"]),
        "FactOWIDPrivateAI": owid.sort_values(["year", "metric"]),
        "FactOECDAIBenchmarks": ai.sort_values(["year", "geography", "metric"]),
        "FactEdTechMarket": edtech.sort_values("year"),
        "FactEdTechRounds": rounds.sort_values(["source_publication_date", "round_id"])[
            ["round_id", "company_id", "year", "quarter", "source_publication_date", "analysis_period",
             "stage_group", "round_stage_reported", "round_amount_usd_millions", "currency", "lead_investor",
             "funding_source_url", "ai_evidence_url", "source_type"]
        ],
    }
    return {name: frame.reset_index(drop=True) for name, frame in tables.items()}


def write_marts(tables: dict[str, pd.DataFrame], output_dir: Path = MART_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8", float_format="%.9f")


def main() -> None:
    marts = build_marts(read_sources())
    write_marts(marts)
    print(f"Power BI marts built: {len(marts)} tables in {MART_DIR}")
    for name, df in marts.items():
        print(f"  {name}: {len(df):,} rows")
    print("Do not aggregate different fact tables into one overall funding total.")


if __name__ == "__main__":
    main()