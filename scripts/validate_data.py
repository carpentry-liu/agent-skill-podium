#!/usr/bin/env python3
"""Validate Agent / Skill Podium's data without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "competitions.json"
DEFAULT_BUNDLE = ROOT / "data" / "competitions.js"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_STATUSES = {"open", "completed", "cancelled"}
ALLOWED_RESULT_STATUSES = {"verified", "partial", "pending"}
ALLOWED_TYPES = {"agent", "multi-agent", "live-agent", "mcp", "web-agent"}


def expected_bundle(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f"window.PODIUM_DATA = {payload};\n"


def _is_iso_date(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _is_https_url(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root: must be a JSON object"]

    for key in ("schema_version", "updated_at", "methodology", "discovery", "competitions"):
        if key not in data:
            errors.append(f"root: missing {key}")

    if not _is_iso_date(data.get("updated_at")):
        errors.append("updated_at: must use YYYY-MM-DD")

    methodology = data.get("methodology")
    if not isinstance(methodology, dict):
        errors.append("methodology: must be an object")
    else:
        for key in ("scope", "source_policy", "ranking_policy", "unknown_policy"):
            if not isinstance(methodology.get(key), str) or not methodology[key].strip():
                errors.append(f"methodology.{key}: must be a non-empty string")

    discovery = data.get("discovery")
    if not isinstance(discovery, dict):
        errors.append("discovery: must be an object")
    else:
        groups = discovery.get("tag_groups")
        if not isinstance(groups, list) or not groups:
            errors.append("discovery.tag_groups: must be a non-empty array")
        else:
            seen_group_ids: set[str] = set()
            all_tags: set[str] = set()
            for index, group in enumerate(groups):
                path = f"discovery.tag_groups[{index}]"
                if not isinstance(group, dict):
                    errors.append(f"{path}: must be an object")
                    continue
                group_id = group.get("id")
                if not isinstance(group_id, str) or not ID_PATTERN.fullmatch(group_id):
                    errors.append(f"{path}.id: must be kebab-case")
                elif group_id in seen_group_ids:
                    errors.append(f"{path}.id: duplicate {group_id}")
                seen_group_ids.add(group_id)
                tags = group.get("tags")
                if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
                    errors.append(f"{path}.tags: must be a non-empty string array")
                else:
                    duplicates = all_tags.intersection(tags)
                    if duplicates:
                        errors.append(f"{path}.tags: duplicate across groups: {sorted(duplicates)}")
                    all_tags.update(tags)

        targets = discovery.get("search_targets")
        if not isinstance(targets, list) or not targets:
            errors.append("discovery.search_targets: must be a non-empty array")
        else:
            target_ids: set[str] = set()
            for index, target in enumerate(targets):
                path = f"discovery.search_targets[{index}]"
                if not isinstance(target, dict):
                    errors.append(f"{path}: must be an object")
                    continue
                target_id = target.get("id")
                if not isinstance(target_id, str) or not ID_PATTERN.fullmatch(target_id):
                    errors.append(f"{path}.id: must be kebab-case")
                elif target_id in target_ids:
                    errors.append(f"{path}.id: duplicate {target_id}")
                target_ids.add(target_id)
                template = target.get("url_template")
                if not _is_https_url(str(template).replace("{query}", "query")) or "{query}" not in str(template):
                    errors.append(f"{path}.url_template: must be an HTTPS URL containing {{query}}")
                for key in ("label", "query_suffix"):
                    if not isinstance(target.get(key), str) or not target[key].strip():
                        errors.append(f"{path}.{key}: must be a non-empty string")

    competitions = data.get("competitions")
    if not isinstance(competitions, list) or not competitions:
        errors.append("competitions: must be a non-empty array")
        return errors

    seen_ids: set[str] = set()
    for index, item in enumerate(competitions):
        path = f"competitions[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path}: must be an object")
            continue

        item_id = item.get("id")
        if not isinstance(item_id, str) or not ID_PATTERN.fullmatch(item_id):
            errors.append(f"{path}.id: must be kebab-case")
        elif item_id in seen_ids:
            errors.append(f"{path}.id: duplicate {item_id}")
        seen_ids.add(item_id)

        for key in ("title", "organizer", "region", "summary", "verification_note"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{path}.{key}: must be a non-empty string")

        year = item.get("year")
        if not isinstance(year, int) or not 2000 <= year <= 2100:
            errors.append(f"{path}.year: must be an integer from 2000 to 2100")

        status = item.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{path}.status: unsupported value {status!r}")
        result_status = item.get("result_status")
        if result_status not in ALLOWED_RESULT_STATUSES:
            errors.append(f"{path}.result_status: unsupported value {result_status!r}")

        types = item.get("types")
        if not isinstance(types, list) or not types:
            errors.append(f"{path}.types: must be a non-empty array")
        elif len(types) != len(set(types)) or any(value not in ALLOWED_TYPES for value in types):
            errors.append(f"{path}.types: contains duplicate or unsupported values")

        tags = item.get("tags")
        required_tags = {item.get("organizer"), str(year), item.get("region")}
        if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            errors.append(f"{path}.tags: must be a non-empty string array")
        elif not required_tags.issubset(set(tags)):
            errors.append(f"{path}.tags: must include organizer, year, and region")

        if not _is_https_url(item.get("official_url")):
            errors.append(f"{path}.official_url: must be an HTTPS URL")
        if not _is_iso_date(item.get("verified_on")) or item.get("verified_on") is None:
            errors.append(f"{path}.verified_on: must use YYYY-MM-DD")

        dates = item.get("dates")
        if not isinstance(dates, dict):
            errors.append(f"{path}.dates: must be an object")
        else:
            for key in ("start", "end", "announced"):
                if key not in dates or not _is_iso_date(dates.get(key)):
                    errors.append(f"{path}.dates.{key}: must be null or YYYY-MM-DD")

        scale = item.get("scale")
        if not isinstance(scale, dict):
            errors.append(f"{path}.scale: must be an object")
        else:
            for key in ("participants", "submissions", "countries"):
                value = scale.get(key)
                if value is not None and (not isinstance(value, int) or value < 0):
                    errors.append(f"{path}.scale.{key}: must be null or a non-negative integer")

        results = item.get("results")
        if not isinstance(results, list):
            errors.append(f"{path}.results: must be an array")
            continue
        if result_status == "pending" and results:
            errors.append(f"{path}.results: pending competitions cannot contain results")
        if result_status in {"verified", "partial"} and not results:
            errors.append(f"{path}.results: verified competitions must contain results")

        seen_projects: set[tuple[str, str]] = set()
        ranks_by_track: dict[str, set[int]] = {}
        for result_index, result in enumerate(results):
            result_path = f"{path}.results[{result_index}]"
            if not isinstance(result, dict):
                errors.append(f"{result_path}: must be an object")
                continue
            for key in ("award", "track", "project", "summary"):
                if not isinstance(result.get(key), str) or not result[key].strip():
                    errors.append(f"{result_path}.{key}: must be a non-empty string")
            team = result.get("team")
            if team is not None and not isinstance(team, str):
                errors.append(f"{result_path}.team: must be null or a string")
            project_url = result.get("project_url")
            if project_url is not None and not _is_https_url(project_url):
                errors.append(f"{result_path}.project_url: must be null or an HTTPS URL")
            project_key = (str(result.get("track")), str(result.get("project")))
            if project_key in seen_projects:
                errors.append(f"{result_path}: duplicate project in track")
            seen_projects.add(project_key)
            rank = result.get("rank")
            if rank is not None:
                if not isinstance(rank, int) or rank < 1:
                    errors.append(f"{result_path}.rank: must be null or a positive integer")
                else:
                    track_ranks = ranks_by_track.setdefault(str(result.get("track")), set())
                    if rank in track_ranks:
                        errors.append(f"{result_path}.rank: duplicate rank {rank} in track")
                    track_ranks.add(rank)

    return errors


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--check-bundle", action="store_true", help="also require competitions.js to match the JSON source")
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    args = parser.parse_args()

    try:
        data = load_json(args.path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {args.path}: {exc}", file=sys.stderr)
        return 1

    errors = validate(data)
    if args.check_bundle:
        try:
            actual_bundle = args.bundle.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"bundle: cannot read {args.bundle}: {exc}")
        else:
            if actual_bundle != expected_bundle(data):
                errors.append("bundle: data/competitions.js is not synchronized; run scripts/sync_data_bundle.py")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(data['competitions'])} competitions validated from {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
