(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.PodiumCore = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function normalize(value) {
    return String(value || "").toLocaleLowerCase("zh-CN").normalize("NFKC").trim();
  }

  function competitionHaystack(item) {
    return normalize([
      item.title,
      item.organizer,
      item.region,
      item.summary,
      ...(item.types || []),
      ...(item.tags || []),
      ...(item.results || []).flatMap((result) => [result.project, result.team, result.track, result.award, result.summary])
    ].join(" "));
  }

  function matchesCompetition(item, filters) {
    const terms = normalize(filters.query).split(/\s+/).filter(Boolean);
    const haystack = competitionHaystack(item);
    return terms.every((term) => haystack.includes(term))
      && (!filters.organizer || item.organizer === filters.organizer)
      && (!filters.year || String(item.year) === filters.year)
      && (!filters.type || item.types.includes(filters.type))
      && (!filters.status || item.result_status === filters.status);
  }

  function filterCompetitions(competitions, filters) {
    return competitions.filter((item) => matchesCompetition(item, filters));
  }

  function composeDiscoveryQuery(keyword, tags, suffix) {
    return [String(keyword || "").trim(), ...(tags || []), String(suffix || "").trim()].filter(Boolean).join(" ");
  }

  function buildSearchUrl(target, query) {
    const fullQuery = composeDiscoveryQuery(query, [], target.query_suffix);
    return target.url_template.replace("{query}", encodeURIComponent(fullQuery));
  }

  return { normalize, competitionHaystack, matchesCompetition, filterCompetitions, composeDiscoveryQuery, buildSearchUrl };
}));
