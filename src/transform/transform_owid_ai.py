from __future__ import annotations

from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "owid"
OUTPUT = ROOT / "data" / "processed" / "owid_private_ai_genai_2019_2025.csv"
START_YEAR = 2019
END_YEAR = 2025
SERIES = {
    "private_ai_investment": "private-investment-in-artificial-intelligence",
    "private_genai_investment": "global-investment-in-generative-ai",
}


def parse_one(path: Path, metric: str, slug: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}; first run src/extract/extract_owid_ai.py")
    raw = pd.read_csv(path)
    required = {"Entity", "Year"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Missing OWID identifier columns in {path}: {required - set(raw.columns)}")
    indicators = [col for col in raw.columns if col not in {"Entity", "Code", "Year"}]
    if len(indicators) != 1:
        raise ValueError(f"Expected exactly one investment indicator in {path}, got: {indicators}")
    indicator = indicators[0]
    world = raw.loc[raw["Entity"].astype(str).str.strip() == "World", ["Year", indicator]].copy()
    if world.empty:
        raise ValueError(f"World series not found in {path}")
    world["Year"] = pd.to_numeric(world["Year"], errors="raise")
    if world["Year"].isna().any() or not (world["Year"] % 1 == 0).all():
        raise ValueError(f"Noninteger or missing years in {path}")
    world["Year"] = world["Year"].astype(int)
    world = world.loc[world["Year"].between(START_YEAR, END_YEAR)].copy()
    if world["Year"].duplicated().any():
        raise ValueError(f"Duplicate World/year observations for {metric}")
    expected = set(range(START_YEAR, END_YEAR + 1))
    actual = set(world["Year"].tolist())
    if actual != expected:
        raise ValueError(f"Incomplete {metric} annual coverage; missing={sorted(expected - actual)}; unexpected={sorted(actual - expected)}")
    world[indicator] = pd.to_numeric(world[indicator], errors="raise")
    if world[indicator].isna().any() or not world[indicator].map(math.isfinite).all():
        raise ValueError(f"Missing or nonfinite investment values for {metric}")
    if (world[indicator] < 0).any():
        raise ValueError(f"Negative investment values for {metric}")
    return pd.DataFrame({
        "year": world["Year"].astype(int),
        "geography": "World",
        "metric": metric,
        "value_usd_bn_2021_prices": world[indicator].astype(float) / 1_000_000_000,
        "unit": "constant_2021_USD_billions",
        "source_provider": "Our World in Data",
        "original_provider": "Quid via AI Index Report (2026); U.S. Bureau of Labor Statistics (2026)",
        "source_url": f"https://ourworldindata.org/grapher/{slug}",
        "original_indicator": indicator,
    })


def build_table(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    frames = [parse_one(raw_dir / f"{slug}.csv", metric, slug) for metric, slug in SERIES.items()]
    return pd.concat(frames, ignore_index=True).sort_values(["year", "metric"]).reset_index(drop=True)


def main() -> None:
    result = build_table()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False, float_format="%.9f")
    print(f"Wrote {len(result)} observations to {OUTPUT}")
    print(result.groupby("metric").agg(years=("year", "nunique"), observations=("year", "size")).to_string())
    print("Scope: external private AI investment; NOT VC-only; constant 2021 US dollars.")


if __name__ == "__main__":
    main()