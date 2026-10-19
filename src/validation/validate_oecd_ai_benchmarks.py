from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "processed" / "oecd_ai_benchmarks_2026.csv"
SOURCE = ROOT / "src" / "config" / "oecd_ai_report_2026.json"
EXPECTED_UNIT = {
    "ai_vc": "USD_billions",
    "genai_vc": "USD_billions",
    "total_vc": "USD_billions",
    "ai_it_infrastructure_and_hosting_vc": "USD_billions",
    "ai_share_of_total_vc": "percent",
    "ai_mega_deal_share_of_ai_vc": "percent",
}


def run() -> None:
    with CSV.open(encoding="utf-8", newline="") as f:
        data = list(csv.DictReader(f))
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert data, "Benchmark table is empty"
    assert len(data) == len(source["observations"]), "Source / output row-count mismatch"
    original = {
        (int(item["year"]), item["geography"], item["metric"]): item
        for item in source["observations"]
    }
    keys = [(x["year"], x["geography"], x["metric"]) for x in data]
    assert len(set(keys)) == len(keys), "Duplicate year/geography/metric keys"

    vals = {}
    for r in data:
        year, geography, metric = int(r["year"]), r["geography"], r["metric"]
        amount = float(r["value"])
        assert 2019 <= year <= 2025, ("Unexpected year", year)
        assert metric in EXPECTED_UNIT, ("Unknown metric", metric)
        assert r["unit"] == EXPECTED_UNIT[metric], ("Inconsistent unit", metric)
        assert amount >= 0, ("Negative value", metric)
        if r["unit"] == "percent":
            assert amount <= 100, ("Invalid percentage", metric)
        assert (year, geography, metric) in original, "Output observation absent from the cited input"
        origin = original[(year, geography, metric)]
        assert amount == float(origin["value"]), ("Source value mismatch", year, geography, metric)
        assert r["unit"] == origin["unit"]
        assert r["precision"] == origin["precision"]
        assert r["evidence"] == origin["evidence"]
        assert r["source_url"] == source["source_url"]
        assert r["underlying_provider"] == "Preqin"
        assert r["evidence"].strip(), "Missing published evidence label"
        vals[(year, geography, metric)] = amount

    def v(year, geography, metric):
        return vals[(year, geography, metric)]

    # Allow ~1 percentage point of rounding as OECD publishes to nearest whole percent.
    assert abs(100 * v(2025,"World","ai_vc") / v(2025,"World","total_vc") - v(2025,"World","ai_share_of_total_vc")) < 1
    assert v(2025,"World","genai_vc") <= v(2025,"World","ai_vc")
    assert v(2025,"World","ai_it_infrastructure_and_hosting_vc") <= v(2025,"World","ai_vc")
    region_total = sum(v(2025,g,"ai_vc") for g in ["United States", "EU27", "China", "United Kingdom"])
    assert region_total <= v(2025,"World","ai_vc"), "Geographic totals exceed World AI VC"
    print(f"OECD AI benchmark validation: PASSED ({len(data)} observations)")
    print("Note: this is a sparse set of published benchmarks, not a complete annual panel.")


if __name__ == "__main__":
    run()