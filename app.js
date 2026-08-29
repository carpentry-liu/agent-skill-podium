(function () {
  "use strict";

  const TYPE_LABELS = {
    agent: "Agent 应用",
    skill: "Agent Skill",
    "multi-agent": "多智能体",
    "live-agent": "实时智能体",
    mcp: "MCP / Skill",
    "web-agent": "Agent 原生 Web"
  };
  const STATUS_LABELS = {
    verified: "已核验",
    partial: "已核验·精选",
    pending: "待开奖"
  };

  const data = window.PODIUM_DATA;
  const core = window.PodiumCore;
  if (!data || !Array.isArray(data.competitions)) {
    document.getElementById("result-summary").textContent = "数据没有正确加载，请检查 data/competitions.js。";
    return;
  }

  const elements = {
    form: document.getElementById("filters"),
    search: document.getElementById("search"),
    organizer: document.getElementById("organizer"),
    year: document.getElementById("year"),
    type: document.getElementById("type"),
    status: document.getElementById("status"),
    sort: document.getElementById("sort"),
    reset: document.getElementById("reset"),
    emptyReset: document.getElementById("empty-reset"),
    results: document.getElementById("results"),
    empty: document.getElementById("empty-state"),
    summary: document.getElementById("result-summary"),
    template: document.getElementById("competition-template")
  };

  function text(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = value;
    return node;
  }

  function link(className, label, url, ariaLabel) {
    const node = document.createElement("a");
    node.className = className;
    node.href = url;
    node.target = "_blank";
    node.rel = "noopener noreferrer";
    node.textContent = label;
    if (ariaLabel) node.setAttribute("aria-label", ariaLabel);
    return node;
  }

  function appendTag(container, label, modifier) {
    container.appendChild(text("span", `tag${modifier ? ` ${modifier}` : ""}`, label));
  }

  function appendFact(container, label, value) {
    const row = document.createElement("div");
    row.className = "fact";
    row.append(text("span", "", label), text("strong", "", value));
    container.appendChild(row);
  }

  function renderWinner(result) {
    const row = document.createElement("article");
    row.className = "winner";

    const rank = document.createElement("div");
    rank.className = "winner__rank";
    rank.textContent = result.rank ? `第 ${result.rank} 名` : result.award;
    rank.appendChild(text("small", "", result.track || "官方奖项"));

    const project = document.createElement("div");
    project.className = "winner__project";
    project.appendChild(text("h4", "", result.project));
    project.appendChild(text("span", "winner__team", result.team ? `团队：${result.team}` : "团队信息待补充"));

    const summary = text("p", "winner__summary", result.summary);

    row.append(rank, project, summary);
    if (result.project_url) {
      row.appendChild(link("winner__link", "查看项目", result.project_url, `打开 ${result.project} 项目页面（新窗口）`));
    } else {
      row.appendChild(text("span", "winner__missing", "暂无链接"));
    }
    return row;
  }

  function renderCard(item, index) {
    const fragment = elements.template.content.cloneNode(true);
    const card = fragment.querySelector(".competition-card");
    card.style.animationDelay = `${Math.min(index, 6) * 65}ms`;
    fragment.querySelector(".competition-card__serial").textContent = `赛事\n${String(index + 1).padStart(2, "0")}`;
    fragment.querySelector("h3").textContent = item.title;
    fragment.querySelector(".competition-card__dek").textContent = item.summary;

    const tags = fragment.querySelector(".tag-row");
    appendTag(tags, STATUS_LABELS[item.result_status], item.result_status === "pending" ? "tag--pending" : "tag--status");
    item.types.forEach((type) => appendTag(tags, TYPE_LABELS[type] || type));

    const facts = fragment.querySelector(".competition-card__facts");
    appendFact(facts, "主办方", item.organizer);
    appendFact(facts, "年份", String(item.year));
    appendFact(facts, "范围", item.region);
    if (item.scale && item.scale.submissions) appendFact(facts, "提交数", item.scale.submissions.toLocaleString("zh-CN"));

    const podium = fragment.querySelector(".podium");
    if (item.results.length) {
      item.results.forEach((result) => podium.appendChild(renderWinner(result)));
    } else {
      const pending = document.createElement("div");
      pending.className = "empty-state";
      pending.append(text("span", "", "…"), text("h3", "", "官方尚未公布赛果"), text("p", "", item.verification_note));
      podium.appendChild(pending);
    }

    const ticket = fragment.querySelector(".source-ticket");
    const top = document.createElement("div");
    top.append(text("h4", "", "信息来源"), text("p", "source-ticket__seal", item.result_status === "pending" ? "官方待开奖" : "官方已核验"));
    const detail = document.createElement("div");
    detail.append(
      text("p", "", `最近核验：${item.verified_on}`),
      text("p", "", item.verification_note),
      link("", "查看官方结果", item.official_url, `打开 ${item.title} 官方来源（新窗口）`)
    );
    ticket.append(top, detail);
    return fragment;
  }

  function readFilters() {
    return {
      query: elements.search.value,
      organizer: elements.organizer.value,
      year: elements.year.value,
      type: elements.type.value,
      status: elements.status.value
    };
  }

  function sortCompetitions(items) {
    const sorted = [...items];
    if (elements.sort.value === "most-results") {
      return sorted.sort((a, b) => b.results.length - a.results.length || b.year - a.year);
    }
    if (elements.sort.value === "organizer") {
      return sorted.sort((a, b) => a.organizer.localeCompare(b.organizer, "zh-CN") || b.year - a.year);
    }
    return sorted.sort((a, b) => b.year - a.year || a.title.localeCompare(b.title, "zh-CN"));
  }

  function render() {
    const filtered = sortCompetitions(core.filterCompetitions(data.competitions, readFilters()));
    elements.results.replaceChildren(...filtered.map(renderCard));
    elements.empty.hidden = filtered.length !== 0;
    elements.results.hidden = filtered.length === 0;
    const awardCount = filtered.reduce((sum, item) => sum + item.results.length, 0);
    elements.summary.textContent = `共 ${filtered.length} 场赛事，${awardCount} 条获奖记录`;
  }

  function option(value, label) {
    const node = document.createElement("option");
    node.value = value;
    node.textContent = label;
    return node;
  }

  function populateFilters() {
    [...new Set(data.competitions.map((item) => item.organizer))].sort().forEach((value) => elements.organizer.appendChild(option(value, value)));
    [...new Set(data.competitions.map((item) => item.year))].sort((a, b) => b - a).forEach((value) => elements.year.appendChild(option(String(value), String(value))));
    [...new Set(data.competitions.flatMap((item) => item.types))].sort().forEach((value) => elements.type.appendChild(option(value, TYPE_LABELS[value] || value)));
    [...new Set(data.competitions.map((item) => item.result_status))].forEach((value) => elements.status.appendChild(option(value, STATUS_LABELS[value] || value)));
  }

  function updateScoreboard() {
    document.getElementById("competition-count").textContent = String(data.competitions.length);
    document.getElementById("winner-count").textContent = String(data.competitions.reduce((sum, item) => sum + item.results.length, 0));
    document.getElementById("organizer-count").textContent = String(new Set(data.competitions.map((item) => item.organizer)).size);
    document.getElementById("updated-at").textContent = data.updated_at;
  }

  function initDiscovery() {
    const discovery = data.discovery;
    if (!discovery) return;
    const keyword = document.getElementById("discovery-keyword");
    const groupsNode = document.getElementById("tag-groups");
    const preview = document.getElementById("query-preview");
    const sourceLinks = document.getElementById("source-links");
    const localFilter = document.getElementById("filter-from-tags");
    const selected = new Set();

    function composedQuery(includeGlobalSuffix) {
      return core.composeDiscoveryQuery(keyword.value, [...selected], includeGlobalSuffix ? discovery.query_suffix : "");
    }

    function refreshDiscovery() {
      const baseQuery = composedQuery(true);
      preview.textContent = baseQuery;
      sourceLinks.replaceChildren(...discovery.search_targets.map((target) => {
        const url = core.buildSearchUrl(target, baseQuery);
        const node = link("", `${target.label}  ↗`, url, `在 ${target.label} 搜索（新窗口）`);
        return node;
      }));
    }

    discovery.tag_groups.forEach((group) => {
      const section = document.createElement("section");
      section.className = "tag-group";
      section.appendChild(text("h3", "", group.label));
      const chips = document.createElement("div");
      chips.className = "tag-group__chips";
      group.tags.forEach((tag) => {
        const chip = text("button", "discovery-chip", tag);
        chip.type = "button";
        chip.setAttribute("aria-pressed", "false");
        chip.addEventListener("click", () => {
          if (selected.has(tag)) selected.delete(tag); else selected.add(tag);
          chip.setAttribute("aria-pressed", String(selected.has(tag)));
          refreshDiscovery();
        });
        chips.appendChild(chip);
      });
      section.appendChild(chips);
      groupsNode.appendChild(section);
    });

    keyword.addEventListener("input", refreshDiscovery);
    localFilter.addEventListener("click", () => {
      elements.search.value = composedQuery(false);
      render();
      document.getElementById("desk-title").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    refreshDiscovery();
  }

  function initDailyDiscovery() {
    const daily = window.AgentSkillDiscovery;
    const list = document.getElementById("daily-discovery-list");
    const empty = document.getElementById("daily-discovery-empty");
    const updated = document.getElementById("daily-discovery-updated");
    if (!daily || !Array.isArray(daily.candidates)) {
      empty.hidden = false;
      updated.textContent = "自动数据暂不可用";
      return;
    }
    updated.textContent = `北京时间 ${daily.updated_at.slice(0, 10)} · ${daily.candidates.length} 条待核验`;
    const cards = daily.candidates.slice(0, 6).map((candidate, index) => {
      const card = document.createElement("article");
      card.className = "lead-card";
      const top = document.createElement("div");
      top.className = "lead-card__top";
      top.append(text("span", "lead-card__rank", String(index + 1).padStart(2, "0")), text("span", "lead-card__status", "待核验"));
      const title = link("lead-card__title", candidate.title, candidate.url, `打开 ${candidate.title} GitHub 仓库（新窗口）`);
      const description = text("p", "lead-card__description", candidate.description);
      const queries = document.createElement("div");
      queries.className = "lead-card__queries";
      (candidate.matched_queries || []).slice(0, 2).forEach((query) => queries.appendChild(text("span", "", query)));
      const meta = document.createElement("p");
      meta.className = "lead-card__meta";
      const language = candidate.language || "语言未标注";
      const stars = ` · ★ ${candidate.stars || 0}`;
      meta.textContent = `GitHub 候选 · ${language}${stars} · 最近发现 ${String(candidate.pushed_at || "").slice(0, 10)}`;
      card.append(top, title, description, queries, meta);
      return card;
    });
    list.replaceChildren(...cards);
    empty.hidden = cards.length !== 0;
  }

  function resetAll() {
    elements.form.reset();
    render();
    elements.search.focus();
  }

  populateFilters();
  updateScoreboard();
  initDailyDiscovery();
  initDiscovery();
  render();

  elements.form.addEventListener("input", render);
  elements.form.addEventListener("change", render);
  elements.form.addEventListener("reset", () => window.requestAnimationFrame(render));
  elements.emptyReset.addEventListener("click", resetAll);
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      elements.search.focus();
    }
    if (event.key === "Escape" && document.activeElement === elements.search) {
      elements.search.value = "";
      render();
    }
  });

}());
