#!/usr/bin/env python3
"""Run Agent / Skill Podium maintenance through one auditable entrypoint."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import discover_competitions


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
DISCOVERY_JSON = ROOT / "data" / "discovery.json"
DISCOVERY_BUNDLE = ROOT / "data" / "discovery.js"


@dataclass(frozen=True)
class Step:
    name: str
    command: str
    ok: bool
    output: str


def resolve_report_path(value: Path) -> Path:
    """Resolve a new Markdown report inside the repository's reports directory."""
    if value.is_absolute():
        target = value.resolve()
    elif value.parts and value.parts[0].lower() == "reports":
        target = (ROOT / value).resolve()
    else:
        target = (REPORTS_DIR / value).resolve()
    reports_root = REPORTS_DIR.resolve()
    try:
        relative = target.relative_to(reports_root)
    except ValueError as error:
        raise ValueError("report path must stay inside the repository reports/ directory") from error
    if relative == Path(".") or target.suffix.lower() != ".md":
        raise ValueError("report path must name a .md file inside reports/")
    if target.exists():
        raise ValueError(f"report already exists; choose a new filename: {target}")
    return target


def write_report(path: Path, content: str) -> None:
    """Create a report atomically; never replace an existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
    except FileExistsError as error:
        raise ValueError(f"report already exists; choose a new filename: {path}") from error


def run_step(name: str, command: list[str]) -> Step:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return Step(
        name=name,
        command=subprocess.list2cmdline(command),
        ok=completed.returncode == 0,
        output=completed.stdout.strip(),
    )


def verification_steps(*, synchronize: bool) -> list[Step]:
    sync_command = [sys.executable, "scripts/sync_data_bundle.py"]
    if not synchronize:
        sync_command.append("--check")
    return [
        run_step("正式赛果数据包同步", sync_command),
        run_step(
            "正式赛果校验",
            [sys.executable, "scripts/validate_data.py", "--check-bundle"],
        ),
        run_step(
            "未核验线索数据包校验",
            [sys.executable, "scripts/discover_competitions.py", "--check-bundle"],
        ),
        run_step(
            "Python 测试",
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ),
        run_step("前端核心测试", ["node", "tests/test_core.js"]),
    ]


def discover_leads(*, limit: int, write_leads: bool) -> tuple[dict, str]:
    data = discover_competitions.discover(
        os.environ.get("GITHUB_TOKEN"), limit=max(1, min(limit, 30))
    )
    discover_competitions.validate(data)
    if write_leads:
        DISCOVERY_JSON.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        DISCOVERY_BUNDLE.write_text(
            discover_competitions.render_bundle(data), encoding="utf-8"
        )
        action = "已写入未核验候选池及其浏览器数据包"
    else:
        action = "dry-run：未写入任何文件"
    return data, action


def render_report(
    *,
    mode: str,
    mutation: str,
    steps: list[Step],
    discovery: dict | None = None,
) -> str:
    overall = all(step.ok for step in steps)
    lines = [
        "# Agent / Skill 领奖台维护报告",
        "",
        f"- 模式：`{mode}`",
        f"- 文件变更：{mutation}",
        f"- 总结：{'通过' if overall else '失败'}",
        "- 数据边界：自动发现结果始终是 `unverified` 线索，不会写入正式赛果。",
    ]
    if discovery is not None:
        candidates = discovery.get("candidates", [])
        lines.extend(
            [
                f"- 本次搜索：{len(discovery.get('queries', []))} 组查询，{len(candidates)} 条候选",
                "",
                "## 未核验候选摘要",
                "",
            ]
        )
        if candidates:
            for candidate in candidates:
                lines.append(
                    f"- [{candidate['title']}]({candidate['url']}) — "
                    f"`{candidate['status']}`，匹配 {len(candidate['matched_queries'])} 组查询"
                )
        else:
            lines.append("- 本次没有发现候选。")

    lines.extend(["", "## 自动化步骤", ""])
    for step in steps:
        lines.extend(
            [
                f"### {'通过' if step.ok else '失败'} · {step.name}",
                "",
                f"`{step.command}`",
                "",
                "```text",
                step.output or "（命令没有输出）",
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    check = subparsers.add_parser(
        "check", help="只读校验数据包、结构和全部测试"
    )
    check.add_argument("--report", type=Path, help="另存 Markdown 报告")

    refresh = subparsers.add_parser(
        "refresh", help="同步正式赛果数据包，再运行全部校验和测试"
    )
    refresh.add_argument(
        "--dry-run", action="store_true", help="只检查是否需要同步，不写文件"
    )
    refresh.add_argument("--report", type=Path, help="另存 Markdown 报告")

    discover = subparsers.add_parser(
        "discover", help="联网搜索 GitHub 候选；默认只预览，不写数据"
    )
    write_group = discover.add_mutually_exclusive_group()
    write_group.add_argument(
        "--dry-run",
        action="store_true",
        help="预览未核验候选（默认行为，显式写出便于脚本阅读）",
    )
    write_group.add_argument(
        "--write-leads",
        action="store_true",
        help="仅更新 discovery.json/js；不会改正式赛果",
    )
    discover.add_argument("--limit", type=int, default=12)
    discover.add_argument("--report", type=Path, help="另存 Markdown 报告")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report_path = resolve_report_path(args.report) if args.report else None
    except ValueError as error:
        parser.error(str(error))
    discovery = None
    if args.mode == "check":
        mutation = "只读检查；未写入文件"
        steps = verification_steps(synchronize=False)
    elif args.mode == "refresh":
        synchronize = not args.dry_run
        mutation = (
            "dry-run：只读检查；未写入文件"
            if args.dry_run
            else "仅同步由 competitions.json 生成的 competitions.js"
        )
        steps = verification_steps(synchronize=synchronize)
    else:
        try:
            discovery, mutation = discover_leads(
                limit=args.limit, write_leads=args.write_leads
            )
        except (OSError, RuntimeError, ValueError) as error:
            print(f"ERROR: discovery failed: {error}", file=sys.stderr)
            return 1
        steps = verification_steps(synchronize=False)

    report = render_report(
        mode=args.mode, mutation=mutation, steps=steps, discovery=discovery
    )
    print(report, end="")
    if report_path:
        try:
            write_report(report_path, report)
        except ValueError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
    return 0 if all(step.ok for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
