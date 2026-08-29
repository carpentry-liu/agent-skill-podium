from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_data", ROOT / "scripts" / "validate_data.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class CompetitionDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "data" / "competitions.json").read_text(encoding="utf-8"))

    def test_repository_data_is_valid(self) -> None:
        self.assertEqual([], VALIDATOR.validate(self.data))

    def test_duplicate_competition_id_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["competitions"][1]["id"] = data["competitions"][0]["id"]
        self.assertTrue(any("duplicate" in error for error in VALIDATOR.validate(data)))

    def test_pending_competition_cannot_claim_results(self) -> None:
        data = copy.deepcopy(self.data)
        data["competitions"][0]["results"] = [copy.deepcopy(data["competitions"][1]["results"][0])]
        self.assertTrue(any("pending competitions" in error for error in VALIDATOR.validate(data)))

    def test_insecure_official_source_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["competitions"][0]["official_url"] = "http://example.test/results"
        self.assertTrue(any("official_url" in error for error in VALIDATOR.validate(data)))

    def test_search_target_requires_query_placeholder(self) -> None:
        data = copy.deepcopy(self.data)
        data["discovery"]["search_targets"][0]["url_template"] = "https://example.test/search"
        self.assertTrue(any("{query}" in error for error in VALIDATOR.validate(data)))

    def test_bundle_serialization_is_deterministic(self) -> None:
        bundle = VALIDATOR.expected_bundle(self.data)
        self.assertTrue(bundle.startswith("window.PODIUM_DATA = {"))
        self.assertTrue(bundle.endswith(";\n"))
        self.assertIn("WebMCP", bundle)


if __name__ == "__main__":
    unittest.main()
