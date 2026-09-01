---
name: agent-competition-scout
description: 搜索、核验、去重并维护 AI Agent、Agent Skill、MCP 与多智能体比赛赛果；适用于调研近期赛事、获奖项目或更新比赛领奖台数据。在线赛果网站：https://carpentry-liu.github.io/agent-skill-podium/
---

# Agent / Skill 比赛情报站

把分散在各个平台的比赛公告整理为可追溯的赛果数据。保留主办方原始奖项结构，不擅自创造跨赛事总排名。

**在线档案：** [carpentry-liu.github.io/agent-skill-podium](https://carpentry-liu.github.io/agent-skill-podium/) — 不安装 Skill 也能直接浏览、搜索和筛选当前已核验赛果。

## 选择工作模式

- **检索模式：** 用户只想了解有哪些比赛或获奖项目时，联网搜索并回报候选，不修改文件。
- **维护模式：** 只有用户明确要求新增、刷新或整理本仓库赛果时，才更新 `data/competitions.json`。

开始检索或维护前先读 [references/source-policy.md](references/source-policy.md)；需要编辑数据时，再读 [references/data-schema.md](references/data-schema.md)。

## 检索比赛与赛果

1. 根据用户关心的主题、行业、主办方、年份和地区，把请求拆成多组精确查询；可参考 `data/competitions.json` 中 `discovery` 的标签。
2. 联网搜索时，先找主办方官方网站、官方赛事页面和主办方维护的 GitHub 仓库。只有在名次已由合格证据支持后，才使用 Devpost、Kaggle、Hugging Face 或参赛者仓库补充项目细节。
3. 记录赛事名称、主办方、日期、范围、官方奖项原文、获奖者或项目、团队、项目链接、官方结果链接和核验日期。
4. 明确区分已确认事实与未知字段。不得根据页面顺序、奖金多少、热度、Star、点赞、入围状态或项目自己的 README 推断名次。
5. 按主办方、赛事身份、届次/年份和官方 URL 去重。主办方把改名届次或区域赛道视为同一结果集时，也按一个赛事处理。

## 维护正式赛果数据

1. 新增前先检查已有赛事 ID 和结果，避免重复。
2. 只修改 `data/competitions.json` 中受影响的最小记录，保留官方奖项原文。只有主办方明确给出数字顺序时才填写 `rank`；分类奖、区域奖、全场大奖或荣誉提名没有官方数字名次时使用 `null`。
3. 官方赛事尚未公布获奖者时，使用 `result_status: "pending"` 和空 `results`；只收录更大官方结果集的一部分时，使用 `partial` 并明确说明范围。
4. 无法确认的字段设为 `null`，在 `verification_note` 说明重要缺口。缺少项目链接不应成为遗漏已确认获奖者的理由。
5. `verified_on` 写真实核验日期；数据发生变化时同步更新数据集级 `updated_at`。
6. 运行统一维护入口：

   ```text
   python scripts/maintain.py refresh
   ```

   该命令会同步 `data/competitions.js`，校验正式赛果和未核验线索数据包，并运行 Python 与前端测试。只读预检使用 `python scripts/maintain.py refresh --dry-run`。生成的 `data/competitions.js` 用于保证静态页面直接从本地磁盘打开时仍能工作。

7. 检查差异中是否出现意外断言、重复赛事、来源 URL 变化或缺乏证据的名次。

## 返回核验回执

回执必须包含：

- 使用过的查询词和来源域名；
- 新增、更新、保持待公布或跳过的赛事；
- 每条采纳结果的证据等级；
- 尚未确认的字段及其原因；
- 执行过的验证命令和结果。

除非用户另行明确授权，不发布网站、不创建 Issue、不改变仓库可见性，也不推送提交。

## 刷新未核验线索

用户要求从 GitHub 搜索新赛事线索时，使用：

```text
python scripts/maintain.py discover --dry-run
```

该命令会实时发现候选，但不写文件。审阅报告后，只有用户明确要求更新线索源时才能使用 `--write-leads`。这个参数只能写入 `data/discovery.json` 和 `data/discovery.js`，绝不能把线索自动晋升到 `data/competitions.json`。正式名次仍必须经过前述证据核验。命令使用公开 GitHub Search，不会把浏览器抓取逻辑或凭据放进静态网站。
