import copy
import json
import unittest

from src.transform.build_edtech_rounds import SOURCE, build_dataset
from src.validation.validate_edtech_rounds import validate_dataset


class TestEdTechRounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_seed_sample_is_valid(self):
        rows=build_dataset(self.manifest["observations"])
        validate_dataset(rows,self.manifest)
        self.assertEqual(len(rows),12)
        self.assertEqual(len({r["company_id"] for r in rows}),6)

    def test_rejects_duplicate_round_id(self):
        manifest=copy.deepcopy(self.manifest)
        rows=build_dataset(manifest["observations"])
        rows[1]["round_id"]=rows[0]["round_id"]
        with self.assertRaises(AssertionError):
            validate_dataset(rows,manifest)

    def test_rejects_wrong_currency(self):
        manifest=copy.deepcopy(self.manifest)
        rows=build_dataset(manifest["observations"])
        rows[0]["currency"]="EUR"
        with self.assertRaises(AssertionError):
            validate_dataset(rows,manifest)

    def test_rejects_missing_evidence(self):
        manifest=copy.deepcopy(self.manifest)
        rows=build_dataset(manifest["observations"])
        rows[0]["funding_source_url"]=""
        with self.assertRaises(AssertionError):
            validate_dataset(rows,manifest)

    def test_retains_b2_subseries(self):
        rows=build_dataset(self.manifest["observations"])
        by_id={r["round_id"]:r for r in rows}
        self.assertEqual(by_id["speak-2023-08-31"]["round_stage_reported"],"Series B-2")
        self.assertEqual(by_id["speak-2024-06-18"]["round_stage_reported"],"Series B-3")
        self.assertEqual(by_id["speak-2022-11-18"]["analysis_period"],"Transition")

    def test_preserves_unknown_stage(self):
        rows=build_dataset(self.manifest["observations"])
        magic=next(r for r in rows if r["round_id"]=="magic-2023-08-23")
        self.assertEqual(magic["stage_group"],"Unspecified")


if __name__ == "__main__":
    unittest.main()