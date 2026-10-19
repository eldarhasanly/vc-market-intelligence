from __future__ import annotations

import unittest
import pandas as pd

from src.transform.build_edtech_market import build_dataset
from src.validation.validate_edtech_market import validate_frame


def fixture() -> pd.DataFrame:
    # Synthetic values are intentionally unrelated to the source series.
    return pd.DataFrame({
        "year": list(range(2019, 2026)),
        "edtech_vc_usd_billions": [2., 3., 4., 3.2, 2.1, 1.9, 2.4],
    })


class EdTechPipelineTests(unittest.TestCase):
    def test_valid_series(self):
        validate_frame(build_dataset(fixture()))

    def test_duplicate_year_rejected(self):
        rows = fixture()
        rows.loc[6, "year"] = 2024
        with self.assertRaises(ValueError):
            build_dataset(rows)

    def test_missing_year_rejected(self):
        with self.assertRaises(ValueError):
            build_dataset(fixture().iloc[:6])

    def test_negative_funding_rejected(self):
        rows = fixture()
        rows.loc[1, "edtech_vc_usd_billions"] = -1
        with self.assertRaises(ValueError):
            build_dataset(rows)

    def test_unexpected_column_rejected(self):
        rows = fixture()
        rows["foo"] = 1
        with self.assertRaises(ValueError):
            build_dataset(rows)

    def test_nan_rejected(self):
        rows = fixture()
        rows.loc[1, "edtech_vc_usd_billions"] = float("nan")
        with self.assertRaises(ValueError):
            build_dataset(rows)


if __name__ == "__main__":
    unittest.main()