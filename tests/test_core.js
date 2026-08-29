"use strict";

const assert = require("node:assert/strict");
const core = require("../core.js");

const competitions = [
  {
    title: "Security Agent Cup",
    organizer: "Example Org",
    year: 2026,
    region: "全球",
    summary: "Agent safety challenge",
    types: ["agent"],
    tags: ["安全", "MCP"],
    result_status: "verified",
    results: [{ project: "Shield", team: "Team A", track: "Overall", award: "First", summary: "Guardrail agent" }]
  },
  {
    title: "Education Skills Jam",
    organizer: "Other Org",
    year: 2025,
    region: "亚太",
    summary: "Classroom tools",
    types: ["mcp"],
    tags: ["教育", "Skill"],
    result_status: "pending",
    results: []
  }
];

assert.equal(core.filterCompetitions(competitions, { query: "安全 MCP", organizer: "", year: "", type: "", status: "" }).length, 1);
assert.equal(core.filterCompetitions(competitions, { query: "", organizer: "Other Org", year: "2025", type: "mcp", status: "pending" }).length, 1);
assert.equal(core.filterCompetitions(competitions, { query: "nonexistent", organizer: "", year: "", type: "", status: "" }).length, 0);

const composed = core.composeDiscoveryQuery("red teaming", ["Agent", "安全"], "winners results");
assert.equal(composed, "red teaming Agent 安全 winners results");

const url = core.buildSearchUrl(
  { url_template: "https://example.test/search?q={query}", query_suffix: "site:official.test" },
  "Agent 安全"
);
assert.match(url, /^https:\/\/example\.test\/search\?q=/);
assert.match(decodeURIComponent(url), /Agent 安全 site:official\.test/);

console.log("OK: core search and filter behavior");
