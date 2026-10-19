from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


transform = load_module(ROOT / "src" / "transform" / "transform_owid_ai.py", "transform_owid_ai")
validation = load_module(ROOT / "src" / "validation" / "validate_owid_ai.py", "validate_owid_ai")


class OWIDPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)
        for metric, slug in transform.SERIES.items():
            source = pd.DataFrame({
                "Entity": ["World"] * 7 + ["United States"],
                "Code": ["OWID_WRL"] * 7 + ["USA"],
                "Year": list(range(2019, 2026)) + [2025],
                "Investment amount": [float(1_000_000_000 * (y - 2018)) for y in range(2019, 2026)] + [3.0],
            })
            source.to_csv(self.dir / f"{slug}.csv", index=False)

    def tearDown(self):
        self.temp.cleanup()

    def test_build_and_validate(self):
        result = transform.build_table(self.dir)
        self.assertEqual(len(result), 14)
        self.assertEqual(result["value_usd_bn_2021_prices"].min(), 1.0)
        validation.validate(result)

    def test_missing_year_is_an_error(self):
        slug = transform.SERIES["private_genai_investment"]
        p = self.dir / f"{slug}.csv"
        df = pd.read_csv(p)
        df = df.loc[~((df["Entity"] == "World") & (df["Year"] == 2020))]
        df.to_csv(p, index=False)
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            transform.build_table(self.dir)

    def test_negative_values_are_an_error(self):
        slug = transform.SERIES["private_ai_investment"]
        p = self.dir / f"{slug}.csv"
        df = pd.read_csv(p)
        df.loc[(df["Entity"] == "World") & (df["Year"] == 2024), "Investment amount"] = -1
        df.to_csv(p, index=False)
        with self.assertRaisesRegex(ValueError, "Negative"):
            transform.build_table(self.dir)


if __name__ == "__main__":
    unittest.main()