# Dataset schema

`data/competitions.json` is the maintained source. `data/competitions.js` is a generated, browser-friendly mirror for direct `file://` use.

## Root fields

- `schema_version`: schema revision.
- `updated_at`: last material dataset update, `YYYY-MM-DD`.
- `methodology`: public explanation of scope, sources, ranking, and unknowns.
- `discovery`: configurable tag groups and external search targets.
- `competitions`: event records.

## Competition record

Required fields:

- `id`: stable kebab-case ID, normally `<organizer>-<event>-<year>`.
- `title`, `organizer`, `year`, `region`, `summary`.
- `types`: one or more of `agent`, `multi-agent`, `live-agent`, `mcp`, `web-agent`.
- `tags`: discovery terms; include the exact organizer, year string, and region.
- `status`: `open`, `completed`, or `cancelled`.
- `result_status`: `verified`, `partial`, or `pending`.
- `dates`: `start`, `end`, `announced`; each is `YYYY-MM-DD` or `null`.
- `official_url`: HTTPS source supporting status or result.
- `verified_on`: actual date the source was checked.
- `verification_note`: coverage and important unknowns.
- `scale`: `participants`, `submissions`, `countries`; non-negative integers or `null`.
- `results`: award records; empty only when results are pending.

## Result record

- `award`: organizer's award wording.
- `rank`: positive integer only for explicit numerical placement; otherwise `null`.
- `track`: official track, category, region, or `Overall`.
- `project`: project or recipient name.
- `team`: team, person, or organization; `null` when absent.
- `summary`: concise factual description supported by the organizer or linked project page.
- `project_url`: canonical HTTPS project or repository URL; `null` when not published.

## Search targets

Each target has a stable `id`, display `label`, `query_suffix`, and HTTPS `url_template` containing `{query}`. The webpage URL-encodes the composed query and replaces this placeholder. Search targets discover candidates; they do not change the dataset or imply verification.
