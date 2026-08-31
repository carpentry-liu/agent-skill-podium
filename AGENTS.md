# Repository guidance

## Purpose

Maintain a static, source-traceable index of AI Agent, Agent Skill, MCP, and multi-agent competition results, plus the `agent-competition-scout` skill used to research them.

## Non-negotiable data rules

- Prefer organizer-owned result pages and official competition pages.
- Participant claims and secondary lists are leads, not placement evidence.
- Preserve award wording and track boundaries.
- Use a numeric `rank` only when the organizer explicitly publishes one.
- Keep unknown fields `null`; explain material gaps in `verification_note`.
- Do not introduce browser-side scraping or credentials. This is a static site.
- Daily discovery data is an unverified lead feed. Never promote an automated lead into `data/competitions.json` without official result evidence.

## Validation

After changing `data/competitions.json`, always run:

```text
python scripts/maintain.py refresh
```

For a read-only repository check, run `python scripts/maintain.py check`. For live
candidate discovery, preview with `python scripts/maintain.py discover --dry-run`
before explicitly choosing `--write-leads`; discovery can only update the
unverified `data/discovery.json/js` pair.

For skill changes, also run the `skill-creator` quick validator against the repository root.

## Frontend

- Keep production dependencies at zero.
- Preserve direct `file://` usability via `data/competitions.js`.
- Maintain keyboard access, visible focus, responsive layout, and reduced-motion behavior.
- Render external data with DOM text APIs rather than unescaped HTML strings.
