#!/usr/bin/env python3
"""Discover candidate Agent competitions from GitHub Search once per day."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "discovery.json"
DEFAULT_BUNDLE = ROOT / "data" / "discovery.js"
QUERIES = (
    "agent hackathon",
    "AI agent competition",
    "Agent Skill challenge",
    "MCP hackathon",
    "智能体 大赛",
    "智能体 挑战赛",
    "多智能体 竞赛",
    "Agent 技能 大赛",
)
SUBJECT_TERMS = ("agent", "智能体", "mcp", "skill", "技能", "multi-agent", "多智能体")
EVENT_TERMS = ("hackathon", "challenge", "competition", "contest", "大赛", "挑战赛", "竞赛", "黑客松")
def shanghai_day(now: dt.datetime | None = None) -> dt.date:
    current = now or dt.datetime.now(tz=dt.timezone.utc)
    return current.astimezone(ZoneInfo("Asia/Shanghai")).date()


def api_get(url: str, token: str | None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "agent-skill-podium-daily-discovery",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt == 2:
                raise RuntimeError(f"GitHub search failed: {error}") from error
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def searchable(repo: dict) -> str:
    return " ".join(
        [repo.get("name") or "", repo.get("full_name") or "", repo.get("description") or "", *(repo.get("topics") or [])]
    ).lower()


def is_candidate(repo: dict) -> bool:
    text = searchable(repo)
    return (
        not repo.get("fork")
        and not repo.get("archived")
        and any(term in text for term in SUBJECT_TERMS)
        and any(term in text for term in EVENT_TERMS)
    )


def score_candidate(repo: dict, matched_queries: set[str], today: dt.date) -> float:
    updated = dt.datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00")).date()
    age_days = max(0, (today - updated).days)
    recency = max(0, 90 - age_days) / 9
    popularity = math.log10(max(1, int(repo.get("stargazers_count") or 0)) + 1)
    official_hint = 2 if any(term in searchable(repo) for term in ("official", "官方", "organizer", "主办")) else 0
    return round(len(matched_queries) * 5 + recency + popularity + official_hint, 3)


def discover(token: str | None, lookback_days: int = 240, limit: int = 12) -> dict:
    today = shanghai_day()
    created_after = today - dt.timedelta(days=lookback_days)
    collected: dict[int, dict] = {}
    matches: dict[int, set[str]] = {}
    for query in QUERIES:
        qualified = f'"{query}" in:name,description created:>={created_after.isoformat()} archived:false fork:false'
        url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
            {"q": qualified, "sort": "updated", "order": "desc", "per_page": 10}
        )
        payload = api_get(url, token)
        for repo in payload.get("items", []):
            if not is_candidate(repo):
                continue
            repo_id = int(repo["id"])
            collected[repo_id] = repo
            matches.setdefault(repo_id, set()).add(query)

    ranked = sorted(
        collected.values(),
        key=lambda repo: (-score_candidate(repo, matches[int(repo["id"])], today), repo["full_name"].lower()),
    )[:limit]
    candidates = []
    for repo in ranked:
        repo_id = int(repo["id"])
        candidates.append(
            {
                "id": str(repo_id),
                "title": repo["full_name"],
                "url": repo["html_url"],
                "description": repo.get("description") or "该仓库暂无公开简介，请进入来源页核验。",
                "owner": repo["owner"]["login"],
                "language": repo.get("language"),
                "stars": int(repo.get("stargazers_count") or 0),
                "created_at": repo["created_at"],
                "pushed_at": repo["pushed_at"],
                "topics": (repo.get("topics") or [])[:8],
                "matched_queries": sorted(matches[repo_id]),
                "score": score_candidate(repo, matches[repo_id], today),
                "status": "unverified",
                "source_type": "github-search",
            }
        )
    return {
        "schema_version": 1,
        "updated_at": f"{today.isoformat()}T09:00:00+08:00",
        "cadence": "daily",
        "source": "GitHub Search API",
        "source_note": "自动发现仅生成待核验线索，不代表赛事官方身份、奖项或结果。",
        "queries": list(QUERIES),
        "candidates": candidates,
    }


def validate(data: dict) -> None:
    if data.get("schema_version") != 1 or data.get("cadence") != "daily":
        raise ValueError("discovery schema_version/cadence is invalid")
    dt.datetime.fromisoformat(data["updated_at"])
    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    seen = set()
    for index, candidate in enumerate(candidates):
        required = {"id", "title", "url", "description", "matched_queries", "status", "pushed_at", "source_type"}
        missing = required - set(candidate)
        if missing:
            raise ValueError(f"candidates[{index}] missing {sorted(missing)}")
        if candidate["id"] in seen:
            raise ValueError(f"duplicate candidate id: {candidate['id']}")
        seen.add(candidate["id"])
        if candidate["source_type"] != "github-search" or not candidate["url"].startswith("https://github.com/"):
            raise ValueError(f"candidates[{index}] GitHub lead must use GitHub HTTPS")
        if candidate["status"] != "unverified":
            raise ValueError(f"candidates[{index}] must remain unverified")
        if not candidate["matched_queries"]:
            raise ValueError(f"candidates[{index}] must include a discovery query")
        dt.datetime.fromisoformat(candidate["pushed_at"].replace("Z", "+00:00"))


def render_bundle(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return (
        "(function (root, factory) {\n"
        "  const data = factory();\n"
        "  if (typeof module === \"object\" && module.exports) module.exports = data;\n"
        "  if (root) root.AgentSkillDiscovery = data;\n"
        "})(typeof globalThis !== \"undefined\" ? globalThis : this, function () {\n"
        f"  return {payload};\n"
        "});\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--check-bundle", action="store_true")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    if args.check_bundle:
        data = json.loads(args.output.read_text(encoding="utf-8"))
        validate(data)
        expected = render_bundle(data)
        if not args.bundle.is_file() or args.bundle.read_text(encoding="utf-8") != expected:
            raise SystemExit("data/discovery.js is out of sync")
    else:
        data = discover(os.environ.get("GITHUB_TOKEN"), limit=max(1, min(args.limit, 30)))
        validate(data)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        args.bundle.write_text(render_bundle(data), encoding="utf-8")
    print(f"OK: {len(data['candidates'])} daily discovery leads validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
