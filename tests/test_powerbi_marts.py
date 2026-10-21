from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.transform.build_powerbi_marts import build_marts, write_marts
from src.validation.validate_powerbi_marts import validate, read_marts


def small_inputs() -> dict[str, pd.DataFrame]:
    vc = pd.DataFrame([
        {"country_code": "USA", "country": "United States", "year": 2024,
         "stage_code": code, "stage": label, "vc_investment_usd_millions": amount,
         "source_provider": "OECD", "unit_code": "USD_EXC", "unit_multiplier_code": 6, "currency_code": "USD"}
        for code, label, amount in [
            ("_T", "Total", 35.0), ("SEED", "Seed", 5.0),
            ("START", "Start-up and other early stage", 10.0),
            ("LATER", "Later stage venture", 20.0)
        ]
    ])
    ai = pd.DataFrame([{"year": 2024, "geography": "World", "metric": "ai_vc", "value": 10.0,
                        "unit": "USD_billions", "source_publisher": "OECD", "source_url": "https://example.org"}])
    owid = pd.DataFrame([{"year": 2024, "geography": "World", "metric": metric,
                          "value_usd_bn_2021_prices": amount, "unit": "constant_2021_USD_billions",
                          "source_provider": "Our World in Data", "source_url": "https://example.org"}
                         for metric, amount in [("private_ai_investment", 20.0), ("private_genai_investment", 8.0)]])
    market = pd.DataFrame([{"year": 2024, "edtech_vc_usd_billions": 2.4,
                            "geography": "Global (HolonIQ coverage)", "currency": "USD",
                            "source_provider": "HolonIQ", "source_publication_date": "2025-12-19",
                            "source_url": "https://example.org", "series_vintage": "Test"}])
    rounds = pd.DataFrame([{"round_id": "sample1", "company_id": "firm1", "company_name": "Example EdTech",
                            "source_publication_date": "2024-05-08", "year": 2024, "quarter": "Q2",
                            "analysis_period": "Post-GPT", "round_stage_reported": "Seed", "stage_group": "Seed",
                            "round_amount_usd_millions": 2.0, "currency": "USD", "subsector": "Language Learning",
                            "ai_product_role": "AI-native", "lead_investor": "Test Investor", "funding_source_url": "https://example.org",
                            "ai_evidence_url": "https://example.org", "source_type": "Company announcement"}])
    return {"oecd_vc": vc, "oecd_ai": ai, "owid": owid,
            "edtech_market": market, "edtech_rounds": rounds}


class TestPowerBIMarts(unittest.TestCase):
    def test_separate_total_and_stage_facts(self) -> None:
        tables = build_marts(small_inputs())
        self.assertEqual(len(tables["FactOECDVCTotal"]), 1)
        self.assertEqual(len(tables["FactOECDVCStage"]), 3)
        self.assertEqual(tables["FactOECDVCTotal"]["vc_investment_usd_millions"].sum(), 35.0)
        self.assertEqual(tables["FactOECDVCStage"]["vc_investment_usd_millions"].sum(), 35.0)
        self.assertNotIn("_T", set(tables["DimOECDStage"]["stage_code"]))
        validate(tables)

    def test_rejects_duplicate_round_ids(self) -> None:
        data = small_inputs()
        data["edtech_rounds"] = pd.concat([data["edtech_rounds"], data["edtech_rounds"]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            build_marts(data)

    def test_rejects_stage_reconciliation_failure(self) -> None:
        data = small_inputs()
        data["oecd_vc"].loc[data["oecd_vc"]["stage_code"] == "START", "vc_investment_usd_millions"] = 100.0
        with self.assertRaisesRegex(ValueError, "reconcile"):
            build_marts(data)

    def test_rejects_owid_price_basis_change(self) -> None:
        data = small_inputs()
        data["owid"]["unit"] = "nominal_USD_billions"
        with self.assertRaisesRegex(ValueError, "unit or geography"):
            build_marts(data)

    def test_rejects_company_dimension_conflict(self) -> None:
        data = small_inputs()
        other = data["edtech_rounds"].copy()
        other["round_id"] = "sample2"
        other["company_name"] = "Different Name"
        data["edtech_rounds"] = pd.concat([data["edtech_rounds"], other], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "DimEdTechCompany"):
            build_marts(data)

    def test_csv_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            write_marts(build_marts(small_inputs()), output)
            validate(read_marts(output))
            self.assertTrue((output / "FactEdTechRounds.csv").exists())
            self.assertEqual(len(list(output.glob("*.csv"))), 11)


if __name__ == "__main__":
    unittest.main()