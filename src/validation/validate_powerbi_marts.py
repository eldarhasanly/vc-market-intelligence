from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.transform.build_powerbi_marts import MART_DIR

EXPECTED = {
    "DimYear", "DimOECDCountry", "DimOECDStage", "DimEdTechCompany", "DimEdTechStage",
    "FactOECDVCTotal", "FactOECDVCStage", "FactOWIDPrivateAI", "FactOECDAIBenchmarks",
    "FactEdTechMarket", "FactEdTechRounds",
}


def _key_unique(frame: pd.DataFrame, keys: list[str], name: str) -> None:
    if frame[keys].isna().any().any() or frame.duplicated(keys).any():
        raise AssertionError(f"{name}: invalid/duplicate natural key {keys}")


def _fk(fact: pd.DataFrame, dimension: pd.DataFrame, key: str, fact_name: str) -> None:
    if fact[key].isna().any() or not set(fact[key]).issubset(set(dimension[key])):
        raise AssertionError(f"{fact_name}: orphaned relationship on {key}")


def validate(tables: dict[str, pd.DataFrame]) -> None:
    if set(tables) != EXPECTED:
        raise AssertionError(f"Unexpected Power BI tables: {set(tables) ^ EXPECTED}")
    for name, table in tables.items():
        if table.empty:
            raise AssertionError(f"{name}: empty table")

    dim_keys = {
        "DimYear": ["year"],
        "DimOECDCountry": ["country_code"],
        "DimOECDStage": ["stage_code"],
        "DimEdTechCompany": ["company_id"],
        "DimEdTechStage": ["stage_group"],
    }
    for name, keys in dim_keys.items():
        _key_unique(tables[name], keys, name)
    fact_keys = {
        "FactOECDVCTotal": ["country_code", "year"],
        "FactOECDVCStage": ["country_code", "year", "stage_code"],
        "FactOWIDPrivateAI": ["year", "geography", "metric"],
        "FactOECDAIBenchmarks": ["year", "geography", "metric"],
        "FactEdTechMarket": ["year"],
        "FactEdTechRounds": ["round_id"],
    }
    for name, keys in fact_keys.items():
        _key_unique(tables[name], keys, name)

    for name in fact_keys:
        _fk(tables[name], tables["DimYear"], "year", name)
    for name in ["FactOECDVCTotal", "FactOECDVCStage"]:
        _fk(tables[name], tables["DimOECDCountry"], "country_code", name)
    _fk(tables["FactOECDVCStage"], tables["DimOECDStage"], "stage_code", "FactOECDVCStage")
    _fk(tables["FactEdTechRounds"], tables["DimEdTechCompany"], "company_id", "FactEdTechRounds")
    _fk(tables["FactEdTechRounds"], tables["DimEdTechStage"], "stage_group", "FactEdTechRounds")

    # These are separate fact universes. These checks prevent a silent unit or
    # measure-category switch in the materialized dataset.
    owid = tables["FactOWIDPrivateAI"]
    if set(owid["unit"]) != {"constant_2021_USD_billions"}:
        raise AssertionError("OWID price basis unexpectedly changed")
    if set(owid["metric"]) != {"private_ai_investment", "private_genai_investment"}:
        raise AssertionError("OWID indicator universe changed")
    if set(tables["FactOECDAIBenchmarks"]["unit"]) - {"USD_billions", "percent"}:
        raise AssertionError("OECD.AI benchmark units changed")
    if set(tables["FactEdTechMarket"]["currency"]) != {"USD"}:
        raise AssertionError("HolonIQ currency changed")
    if set(tables["FactEdTechRounds"]["currency"]) != {"USD"}:
        raise AssertionError("Round currency changed")

    rounds = tables["FactEdTechRounds"]
    d = pd.to_datetime(rounds["source_publication_date"], errors="coerce")
    if d.isna().any() or (d.dt.year != rounds["year"]).any():
        raise AssertionError("Curated round source publication dates mismatch year")
    if (pd.to_numeric(rounds["round_amount_usd_millions"]) <= 0).any():
        raise AssertionError("Curated round amount must be positive")
    if set(rounds["analysis_period"]) - {"Pre-GPT", "Transition", "Post-GPT"}:
        raise AssertionError("Unknown round analysis period")
    if set(tables["DimOECDStage"]["stage_code"]) - {"SEED", "START", "LATER"}:
        raise AssertionError("OECD stage dimension includes noncomponent rows")

    # The total and component fact tables must not duplicate their grain.
    # Their numeric columns should be aggregated only through their own measures.
    total = tables["FactOECDVCTotal"]
    stage = tables["FactOECDVCStage"]
    component = stage.pivot(index=["country_code", "year"], columns="stage_code", values="vc_investment_usd_millions")
    if {"SEED", "START", "LATER"}.issubset(component.columns):
        full = component.dropna(subset=["SEED", "START", "LATER"])
        if not full.empty:
            comparison = full[["SEED", "START", "LATER"]].sum(axis=1).rename("stage_sum").reset_index().merge(
                total, on=["country_code", "year"], how="left", validate="one_to_one"
            )
            if comparison["vc_investment_usd_millions"].isna().any():
                raise AssertionError("Missing OECD country total for full-stage subset")
            if ((comparison["stage_sum"] - comparison["vc_investment_usd_millions"]).abs() > 0.05).any():
                raise AssertionError("Stage and total fact reconciliation failed")


def read_marts(directory: Path = MART_DIR) -> dict[str, pd.DataFrame]:
    missing = sorted(name for name in EXPECTED if not (directory / f"{name}.csv").is_file())
    if missing:
        raise FileNotFoundError("Missing marts: " + ", ".join(missing) + " — run the mart builder first")
    return {name: pd.read_csv(directory / f"{name}.csv", low_memory=False) for name in sorted(EXPECTED)}


def main() -> None:
    marts = read_marts()
    validate(marts)
    print(f"Power BI mart validation: PASSED ({len(marts)} tables)")
    print("OECD total and stage facts: separated and reconciled where complete.")
    print("OWID constant-price private investment and nominal VC: never combined.")
    print("EdTech rounds: curated company sample, not full-market share.")


if __name__ == "__main__":
    main()