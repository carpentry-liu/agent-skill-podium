from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.paths: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag == "script" else None
        if key and values.get(key):
            self.paths.append(values[key] or "")


def local_target(base: Path, raw: str) -> Path | None:
    parsed = urlparse(raw)
    if parsed.scheme or parsed.netloc or raw.startswith("#"):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    return (base / path).resolve()


class RepositoryIntegrityTests(unittest.TestCase):
    def test_index_local_assets_exist(self) -> None:
        parser = AssetParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        missing = [str(path) for raw in parser.paths if (path := local_target(ROOT, raw)) and not path.exists()]
        self.assertEqual([], missing)

    def test_markdown_relative_links_exist(self) -> None:
        missing: list[str] = []
        for markdown in ROOT.rglob("*.md"):
            if ".validation-deps" in markdown.parts:
                continue
            content = markdown.read_text(encoding="utf-8")
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                target = local_target(markdown.parent, raw)
                if target and not target.exists():
                    missing.append(f"{markdown.relative_to(ROOT)} -> {raw}")
        self.assertEqual([], missing)

    def test_json_schema_document_parses(self) -> None:
        schema = json.loads((ROOT / "data" / "competitions.schema.json").read_text(encoding="utf-8"))
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
        self.assertIn("competition", schema["$defs"])


if __name__ == "__main__":
    unittest.main()
