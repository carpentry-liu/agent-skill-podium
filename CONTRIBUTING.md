# 贡献指南

感谢你帮助维护 Agent / Skill 赛果档案。重点不是收录数量，而是每条名次都能回到官方证据。

## 提交新赛事

1. 先搜索 `data/competitions.json`，按主办方、名称、年份、地区和官方 URL 检查重复。
2. 找到能直接证明结果的官方来源：主办方官网、官方博客、官方赛事结果页或主办方维护的 GitHub。
3. 参照 `references/source-policy.md` 标记证据等级。只有 A/B 级默认可以直接收录；C 级必须在 `verification_note` 说明原因；D 级只能作为线索。
4. 按 `references/data-schema.md` 添加或更新记录。
5. 官方没有数字排名时，将 `rank` 设为 `null` 并保留原奖项名称。
6. 缺少项目链接或规模数据时使用 `null`，不要猜测。
7. 更新 `updated_at` 和该赛事的 `verified_on`。
8. 用统一入口同步并验证数据：

   ```powershell
   python scripts/maintain.py refresh
   ```

   该命令会同步正式数据包、检查未核验候选数据包，并运行 Python 与前端测试。
   只想预检时使用 `python scripts/maintain.py refresh --dry-run`。

## PR 描述应包含

- 赛事名称、主办方、届次或年份；
- 直接支持奖项的官方来源；
- 项目页或仓库链接（若官方提供）；
- 核验日期；
- 是完整结果、前三、主要奖项精选还是待开奖；
- 无法确认的字段及原因；
- 本地验证结果。

## 修改搜索入口

搜索标签和目标平台位于 `data/competitions.json` 的 `discovery`。新增搜索目标时：

- `url_template` 必须是 HTTPS，并包含 `{query}`；
- `query_suffix` 应缩小来源范围，而不是添加未经证实的结论；
- 不要在静态前端加入需要泄露密钥或绕过 CORS 的抓取逻辑；
- 运行 Bundle 同步与全部测试。

如需刷新每日 GitHub 候选，先运行 `python scripts/maintain.py discover --dry-run`
阅读候选报告；确认后再运行 `python scripts/maintain.py discover --write-leads`。
这个入口只更新 `data/discovery.json/js`，不会自动晋升任何候选。

## Commit 规范

使用 Conventional Commits，例如：

```text
data: add verified 2026 agent challenge results
fix: preserve category awards without numeric ranks
docs: clarify evidence requirements
```
