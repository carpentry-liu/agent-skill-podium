---
name: agent-competition-scout
description: 搜索、核验、去重并维护 AI Agent、Agent Skill、MCP 与多智能体比赛赛果；适用于调研近期赛事、获奖项目或更新比赛领奖台数据，不把参赛者自述和二手汇总当作名次证据。
---

# Agent Competition Scout

Turn scattered competition announcements into a traceable results dataset. Preserve the organizer's award structure instead of inventing a cross-event ranking.

## Choose the mode

- **Scout:** Search and report candidates without changing files when the user only asks what exists.
- **Maintain:** Update `data/competitions.json` only when the user asks to add, refresh, or organize results in this repository.

Before research or maintenance, read [references/source-policy.md](references/source-policy.md). Before editing data, also read [references/data-schema.md](references/data-schema.md).

## Research

1. Convert the request into several narrow queries using relevant topic, industry, organizer, year, and region tags from `data/competitions.json` under `discovery`.
2. Search the internet. Start with organizers' official domains, then official competition pages and organizer-maintained GitHub repositories. Use Devpost, Kaggle, Hugging Face, or participant repositories to find project details only after placement is supported by acceptable evidence.
3. Record the event name, organizer, dates, scope, award wording, winner or project, team, project link, official results link, and the date checked.
4. Separate confirmed facts from unknown fields. Do not infer rank from page order, prize amount, popularity, stars, likes, finalist status, or a project's own README.
5. Deduplicate by organizer, event identity, edition or year, and official URL. Treat renamed editions and regional tracks as one event when the organizer presents them as one result set.

## Maintain the dataset

1. Inspect the existing event IDs and results before adding data.
2. Add or update the smallest affected records in `data/competitions.json`. Keep exact official award names. Set `rank` only for explicit numerical ordering; use `null` for category, regional, grand-prize, and honorable-mention labels without an official numerical rank.
3. Use `result_status: "pending"` with an empty `results` array when an official event is active but has not announced winners. Use `partial` when the included rows are a clearly disclosed selection from a larger official result set.
4. Set unavailable fields to `null` and explain material gaps in `verification_note`. A missing project link is not a reason to omit a confirmed winner.
5. Set `verified_on` to the actual verification date and update the dataset-level `updated_at` when data changes.
6. Run:

   ```text
   python scripts/sync_data_bundle.py
   python scripts/validate_data.py --check-bundle
   python -m unittest discover -s tests -v
   ```

   The generated `data/competitions.js` is required so the static page also works when opened directly from disk.

7. Review the diff for accidental claims, duplicated events, changed source URLs, and unsupported rankings.

## Return a verification receipt

Report:

- queries and source domains searched;
- events added, updated, left pending, or skipped;
- evidence level for every accepted result;
- unresolved fields and why they remain unknown;
- validation commands and outcomes.

Do not publish, open issues, change repository visibility, or push commits unless the user separately authorizes those actions.
