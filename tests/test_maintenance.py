from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("maintain", SCRIPTS / "maintain.py")
MAINTAIN = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MAINTAIN
SPEC.loader.exec_module(MAINTAIN)


def discovery_fixture() -> dict:
    return {
        "schema_version": 1,
        "updated_at": "2026-08-31T09:00:00+08:00",
        "cadence": "daily",
        "source": "GitHub Search API",
        "source_note": "自动发现仅生成待核验线索。",
        "queries": ["agent hackathon"],
        "candidates": [
            {
                "id": "42",
                "title": "example/agent-hackathon",
                "url": "https://github.com/example/agent-hackathon",
                "description": "candidate",
                "owner": "example",
                "language": "Python",
                "stars": 0,
                "created_at": "2026-08-01T00:00:00Z",
                "pushed_at": "2026-08-30T00:00:00Z",
                "topics": [],
                "matched_queries": ["agent hackathon"],
                "score": 5.0,
                "status": "unverified",
                "source_type": "github-search",
            }
        ],
    }


class MaintenanceTests(unittest.TestCase):
    def test_report_path_is_confined_to_reports_directory(self) -> None:
        safe = MAINTAIN.resolve_report_path(Path("daily/check.md"))
        self.assertEqual(MAINTAIN.REPORTS_DIR / "daily" / "check.md", safe)
        self.assertEqual(
            MAINTAIN.REPORTS_DIR / "maintenance.md",
            MAINTAIN.resolve_report_path(Path("reports/maintenance.md")),
        )
        for unsafe in (
            Path("data/competitions.json"),
            Path("../outside.md"),
            ROOT / "scripts" / "maintain.md",
        ):
            with self.subTest(unsafe=unsafe):
                with self.assertRaisesRegex(ValueError, "reports/"):
                    MAINTAIN.resolve_report_path(unsafe)

    def test_existing_report_cannot_be_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reports = Path(directory) / "reports"
            reports.mkdir()
            existing = reports / "existing.md"
            existing.write_text("keep", encoding="utf-8")
            with mock.patch.object(MAINTAIN, "REPORTS_DIR", reports):
                with self.assertRaisesRegex(ValueError, "already exists"):
                    MAINTAIN.resolve_report_path(Path("existing.md"))
            self.assertEqual("keep", existing.read_text(encoding="utf-8"))

    def test_report_writer_uses_exclusive_create(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "nested" / "new.md"
            MAINTAIN.write_report(report, "first")
            with self.assertRaisesRegex(ValueError, "already exists"):
                MAINTAIN.write_report(report, "second")
            self.assertEqual("first", report.read_text(encoding="utf-8"))

    def test_unsafe_report_is_rejected_before_discovery_can_write(self) -> None:
        with mock.patch.object(MAINTAIN, "discover_leads") as discover:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    MAINTAIN.main(
                        [
                            "discover",
                            "--write-leads",
                            "--report",
                            str(ROOT / "data" / "competitions.json"),
                        ]
                    )

        self.assertEqual(raised.exception.code, 2)
        discover.assert_not_called()

    def test_discovery_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "discovery.json"
            bundle_path = Path(directory) / "discovery.js"
            with (
                mock.patch.object(MAINTAIN, "DISCOVERY_JSON", json_path),
                mock.patch.object(MAINTAIN, "DISCOVERY_BUNDLE", bundle_path),
                mock.patch.object(
                    MAINTAIN.discover_competitions,
                    "discover",
                    return_value=discovery_fixture(),
                ),
            ):
                data, action = MAINTAIN.discover_leads(limit=12, write_leads=False)

            self.assertEqual(data["candidates"][0]["status"], "unverified")
            self.assertIn("dry-run", action)
            self.assertFalse(json_path.exists())
            self.assertFalse(bundle_path.exists())

    def test_write_leads_only_creates_discovery_pair(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "discovery.json"
            bundle_path = Path(directory) / "discovery.js"
            with (
                mock.patch.object(MAINTAIN, "DISCOVERY_JSON", json_path),
                mock.patch.object(MAINTAIN, "DISCOVERY_BUNDLE", bundle_path),
                mock.patch.object(
                    MAINTAIN.discover_competitions,
                    "discover",
                    return_value=discovery_fixture(),
                ),
            ):
                _, action = MAINTAIN.discover_leads(limit=12, write_leads=True)

            self.assertIn("未核验候选池", action)
            self.assertTrue(json_path.is_file())
            self.assertTrue(bundle_path.is_file())
            self.assertIn('"status": "unverified"', json_path.read_text(encoding="utf-8"))

    def test_report_makes_evidence_boundary_and_failures_visible(self) -> None:
        report = MAINTAIN.render_report(
            mode="check",
            mutation="只读检查；未写入文件",
            steps=[MAINTAIN.Step("示例校验", "python check.py", False, "stale")],
            discovery=discovery_fixture(),
        )

        self.assertIn("总结：失败", report)
        self.assertIn("unverified", report)
        self.assertIn("不会写入正式赛果", report)
        self.assertIn("stale", report)


if __name__ == "__main__":
    unittest.main()
