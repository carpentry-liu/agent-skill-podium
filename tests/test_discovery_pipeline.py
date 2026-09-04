from __future__ import annotations

import datetime as dt
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discover_competitions", ROOT / "scripts" / "discover_competitions.py")
DISCOVERY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(DISCOVERY)


class DailyDiscoveryTests(unittest.TestCase):
    def test_unmarked_archive_mirror_is_rejected(self):
        repo = {
            "name": "agent-hackathon-copy",
            "full_name": "archive/agent-hackathon-copy",
            "description": "Standalone archived copy of a winning agent hackathon entry",
            "topics": ["agent", "hackathon"],
            "fork": False,
            "archived": False,
        }
        self.assertFalse(DISCOVERY.is_candidate(repo))

    def test_score_rewards_query_matches_and_recency(self):
        base = {
            "name": "agent-hackathon",
            "full_name": "example/agent-hackathon",
            "description": "official agent competition",
            "topics": ["ai-agent", "hackathon"],
            "pushed_at": "2026-08-28T00:00:00Z",
            "stargazers_count": 10,
        }
        today = dt.date(2026, 8, 29)
        one = DISCOVERY.score_candidate(base, {"agent hackathon"}, today)
        two = DISCOVERY.score_candidate(base, {"agent hackathon", "AI agent competition"}, today)
        self.assertGreater(two, one)
        older = dict(base, pushed_at="2026-05-01T00:00:00Z")
        self.assertGreater(one, DISCOVERY.score_candidate(older, {"agent hackathon"}, today))

    def test_non_github_candidate_is_rejected(self):
        data = {
            "schema_version": 1,
            "updated_at": "2026-08-29T09:00:00+08:00",
            "cadence": "daily",
            "candidates": [{
                "id": "1",
                "title": "copied list",
                "url": "https://example.com/list",
                "description": "agent competition",
                "matched_queries": ["agent hackathon"],
                "status": "unverified",
                "source_type": "official-domain-search",
                "pushed_at": "2026-08-28T00:00:00Z",
            }],
        }
        with self.assertRaisesRegex(ValueError, "GitHub lead must use GitHub HTTPS"):
            DISCOVERY.validate(data)

    def test_repository_bundle_is_synced(self):
        data_path = ROOT / "data" / "discovery.json"
        bundle_path = ROOT / "data" / "discovery.js"
        if not data_path.exists() or not bundle_path.exists():
            self.skipTest("initial discovery snapshot has not been generated")
        data = json.loads(data_path.read_text(encoding="utf-8"))
        DISCOVERY.validate(data)
        self.assertEqual(bundle_path.read_text(encoding="utf-8"), DISCOVERY.render_bundle(data))


if __name__ == "__main__":
    unittest.main()
