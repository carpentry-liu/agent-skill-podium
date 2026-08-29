window.PODIUM_DATA = {
  "schema_version": "1.1.0",
  "updated_at": "2026-08-29",
  "methodology": {
    "scope": "公开举办、主题明确涉及 AI Agent、Agent Skill、MCP 或多智能体系统的竞赛与黑客松。",
    "source_policy": "赛事名次必须由主办方官网、官方博客、官方竞赛页或主办方维护的 GitHub 证明。项目页用于补充作品细节，不能单独证明名次。",
    "ranking_policy": "仅在官方明确给出数字名次时填写 rank；一等奖、最佳实践奖、大奖、地区奖和类别奖保持官方奖项名称，不自行换算成总排名。",
    "unknown_policy": "官方没有公布的信息使用 null、空数组或待补充说明，不依据二手榜单、搜索摘要或项目自述猜测。"
  },
  "discovery": {
    "query_suffix": "AI Agent 智能体 Skill 技能 MCP 多智能体 competition hackathon 大赛 挑战赛 winners results 获奖 赛果",
    "tag_groups": [
      {
        "id": "topic",
        "label": "主题",
        "tags": [
          "Agent",
          "Skill",
          "MCP",
          "multi-agent",
          "安全",
          "智能攻防"
        ]
      },
      {
        "id": "industry",
        "label": "行业",
        "tags": [
          "医疗",
          "企业协作",
          "开发者工具",
          "教育",
          "可持续",
          "生活服务",
          "游戏",
          "网络安全",
          "AI PC"
        ]
      },
      {
        "id": "organizer",
        "label": "主办方",
        "tags": [
          "Google Cloud",
          "Microsoft",
          "AWS",
          "OpenAI",
          "火山引擎",
          "扣子 Coze",
          "字节跳动",
          "腾讯云",
          "阿里云",
          "魔搭 ModelScope"
        ]
      },
      {
        "id": "year-region",
        "label": "年份 / 地区",
        "tags": [
          "2026",
          "2025",
          "2024",
          "全球",
          "中国大陆",
          "中国",
          "北美",
          "亚太",
          "日本"
        ]
      }
    ],
    "search_targets": [
      {
        "id": "official",
        "label": "主办方官方域名",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "(site:openai.com OR site:cloud.google.com OR site:developers.googleblog.com OR site:devblogs.microsoft.com OR site:aws.amazon.com OR site:volcengine.com OR site:developer.volcengine.com OR site:coze.cn OR site:cloud.tencent.com OR site:developer.cloud.tencent.com OR site:tch.cloud.tencent.com OR site:aliyun.com OR site:developer.aliyun.com OR site:modelscope.cn)"
      },
      {
        "id": "china-official",
        "label": "中国大陆主办方官网",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "(site:volcengine.com OR site:developer.volcengine.com OR site:coze.cn OR site:cloud.tencent.com OR site:developer.cloud.tencent.com OR site:tch.cloud.tencent.com OR site:aliyun.com OR site:developer.aliyun.com OR site:modelscope.cn)"
      },
      {
        "id": "volcengine-coze",
        "label": "火山引擎 / 扣子",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "(site:volcengine.com OR site:developer.volcengine.com OR site:coze.cn)"
      },
      {
        "id": "tencent-cloud",
        "label": "腾讯云",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "(site:cloud.tencent.com OR site:developer.cloud.tencent.com OR site:tch.cloud.tencent.com)"
      },
      {
        "id": "aliyun-modelscope",
        "label": "阿里云 / 魔搭",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "(site:aliyun.com OR site:developer.aliyun.com OR site:modelscope.cn)"
      },
      {
        "id": "github",
        "label": "GitHub",
        "url_template": "https://github.com/search?q={query}&type=repositories",
        "query_suffix": "winner OR winners"
      },
      {
        "id": "devpost",
        "label": "Devpost",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "site:devpost.com"
      },
      {
        "id": "kaggle",
        "label": "Kaggle",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "site:kaggle.com/competitions"
      },
      {
        "id": "hugging-face",
        "label": "Hugging Face",
        "url_template": "https://www.google.com/search?q={query}",
        "query_suffix": "site:huggingface.co/spaces"
      }
    ]
  },
  "competitions": [
    {
      "id": "modelscope-ai-pc-agent-skills-2026",
      "title": "AI PC Agent Skills 征文活动",
      "organizer": "Intel / OpenVINO / 魔搭社区",
      "year": 2026,
      "region": "中国大陆",
      "types": [
        "agent",
        "skill",
        "multi-agent"
      ],
      "tags": [
        "Agent",
        "Skill",
        "multi-agent",
        "AI PC",
        "开发者工具",
        "Intel / OpenVINO / 魔搭社区",
        "魔搭 ModelScope",
        "2026",
        "中国大陆",
        "中国",
        "亚太"
      ],
      "status": "completed",
      "result_status": "verified",
      "dates": {
        "start": null,
        "end": null,
        "announced": "2026-04-30"
      },
      "official_url": "https://modelscope.cn/events/242/AI%20PC%20Agent%20Skills%20%E5%BE%81%E6%96%87%E6%B4%BB%E5%8A%A8",
      "verified_on": "2026-08-29",
      "verification_note": "魔搭官方赛事页公布全部 10 组最佳实践奖，并明确注明排名不分先后；因此所有 rank 均保留为 null，不把页面顺序解释为名次。",
      "summary": "Intel、OpenVINO 中文社区与魔搭社区联合评选面向 AI PC 的本地 Agent Skill，强调端侧运行、隐私与可复用工作流。",
      "scale": {
        "participants": 83,
        "submissions": null,
        "countries": null
      },
      "results": [
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "「拍照即问」本地 AI 文档助手（scan-and-ask）",
          "team": "孙丰举",
          "summary": "让扫描件与照片在本地完成 OCR 和文档问答，隐私数据不离开设备。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "InfoBridge：AI PC 本地多受众信息适配",
          "team": "吴祀霖",
          "summary": "用本地多智能体 Skill 把同一材料适配为不同受众版本。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "个人知识库智能管家（基于本地 RAG 的私有知识问答系统）",
          "team": "周博远",
          "summary": "以 OpenVINO、向量检索和本地模型构建私有知识问答。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "OCR 财务提取 Skill",
          "team": "刘文昌",
          "summary": "在本地批量识别票据、提取财务字段并生成复核清单。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "智能科研写作副驾驶（cloud-edge-writing）",
          "team": "陈冬冬",
          "summary": "面向科研写作工作流的端云协同 Agent Skill。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "用 OpenVINO 与 OpenClaw Skill 打造端侧营销海报审核助手",
          "team": "冯亦根",
          "summary": "用端侧推理完成营销海报审核工作流。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "让敏感文件不出电脑：基于 AI PC 的本地隐私数据检查 Skill",
          "team": "李悦",
          "summary": "在本地检查文件中的敏感数据，减少外发隐私风险。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "Email Concierge：跑在 AI PC 本地的智能邮件管家",
          "team": "戴宏伟",
          "summary": "离线读取上下文并调用本地工具生成邮件回复草稿。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "AI PC Daily Memory 工作记忆助手",
          "team": "董伟君",
          "summary": "为日常工作提供运行在 AI PC 上的本地记忆辅助。",
          "project_url": null
        },
        {
          "award": "最佳实践奖",
          "rank": null,
          "track": "最佳实践奖",
          "project": "本地身份保险柜 + 自动填表协调 Skill",
          "team": "张成旭",
          "summary": "把身份字段留在本地保险柜，并协调浏览器和办公软件自动填表。",
          "project_url": null
        }
      ]
    },
    {
      "id": "tencent-cloud-agent-pentest-challenge-2026",
      "title": "第二届腾讯云黑客松智能渗透挑战赛",
      "organizer": "腾讯云",
      "year": 2026,
      "region": "中国大陆",
      "types": [
        "agent",
        "multi-agent"
      ],
      "tags": [
        "Agent",
        "multi-agent",
        "安全",
        "智能攻防",
        "网络安全",
        "腾讯云",
        "2026",
        "中国大陆",
        "中国",
        "亚太"
      ],
      "status": "completed",
      "result_status": "partial",
      "dates": {
        "start": null,
        "end": "2026-04-25",
        "announced": "2026-04-27"
      },
      "official_url": "https://developer.cloud.tencent.com/article/2661083",
      "verified_on": "2026-08-29",
      "verification_note": "腾讯云官方复盘明确点名主赛场冠军和“零界”平行赛场第一名，但正文未给出其他名次；本数据不从图片或页面顺序补推亚军、季军。",
      "summary": "以 Agent 架构、任务调度和多 Solver 协作为核心的智能渗透挑战，官方复盘称共有 610 支队伍参赛。",
      "scale": {
        "participants": null,
        "submissions": null,
        "countries": null
      },
      "results": [
        {
          "award": "冠军",
          "rank": 1,
          "track": "智能渗透主赛场",
          "project": "ai小分队",
          "team": "绿盟科技",
          "summary": "采用 Agent 架构与 Harness 构建三层底座，以 Manager 调度多个 Solver。",
          "project_url": null
        },
        {
          "award": "第一名",
          "rank": 1,
          "track": "“零界”平行赛场",
          "project": "yhy战队",
          "team": null,
          "summary": "凭借 Agent 设计和策略调度获得平行赛场第一名。",
          "project_url": null
        }
      ]
    },
    {
      "id": "volcengine-coze-game-agent-challenge-2024",
      "title": "AI 智能体线上挑战赛——游戏主题快闪",
      "organizer": "火山引擎 / 扣子",
      "year": 2024,
      "region": "中国大陆",
      "types": [
        "agent"
      ],
      "tags": [
        "Agent",
        "游戏",
        "生活服务",
        "火山引擎 / 扣子",
        "火山引擎",
        "扣子 Coze",
        "字节跳动",
        "2024",
        "中国大陆",
        "中国",
        "亚太"
      ],
      "status": "completed",
      "result_status": "partial",
      "dates": {
        "start": "2024-09-12",
        "end": "2024-10-13",
        "announced": "2024-10-16"
      },
      "official_url": "https://developer.volcengine.com/activities/7413321752799150117",
      "verified_on": "2026-08-29",
      "verification_note": "火山引擎开发者社区官方活动页公布完整获奖表；当前精选一等奖和全部二等奖。二等奖为并列奖项层级，rank 保持 null，不臆造内部先后。",
      "summary": "基于扣子专业版与豆包大模型制作游戏主题 Bot 的线上挑战赛，官方活动页显示 607 人参与。",
      "scale": {
        "participants": 607,
        "submissions": null,
        "countries": null
      },
      "results": [
        {
          "award": "一等奖",
          "rank": null,
          "track": "游戏主题快闪",
          "project": "天命人助手",
          "team": null,
          "summary": "官方活动页列为本场游戏主题智能体挑战赛一等奖。",
          "project_url": null
        },
        {
          "award": "二等奖",
          "rank": null,
          "track": "游戏主题快闪",
          "project": "规则怪谈解密游戏",
          "team": null,
          "summary": "官方活动页列为本场游戏主题智能体挑战赛二等奖。",
          "project_url": null
        },
        {
          "award": "二等奖",
          "rank": null,
          "track": "游戏主题快闪",
          "project": "游戏帮：黑神话悟空",
          "team": null,
          "summary": "官方活动页列为本场游戏主题智能体挑战赛二等奖。",
          "project_url": null
        }
      ]
    },
    {
      "id": "openai-webmcp-challenge-2026",
      "title": "The WebMCP Challenge",
      "organizer": "OpenAI",
      "year": 2026,
      "region": "全球",
      "types": [
        "mcp",
        "web-agent"
      ],
      "tags": [
        "Agent",
        "Skill",
        "MCP",
        "开发者工具",
        "OpenAI",
        "2026",
        "全球"
      ],
      "status": "open",
      "result_status": "pending",
      "dates": {
        "start": "2026-08-25",
        "end": "2026-09-03",
        "announced": null
      },
      "official_url": "https://openai.com/webmcp-challenge/",
      "verified_on": "2026-08-29",
      "verification_note": "官方页面写明计划于 2026-09-23 公布 Top 10；核验时仍在征集，尚无获奖名单。",
      "summary": "面向 Agent 原生网页体验的 WebMCP 挑战，要求参赛作品通过结构化工具让人和智能体更好地共同使用 Web 应用。",
      "scale": {
        "participants": null,
        "submissions": null,
        "countries": null
      },
      "results": []
    },
    {
      "id": "microsoft-agent-academy-2026",
      "title": "Agent Academy Hackathon 2026",
      "organizer": "Microsoft",
      "year": 2026,
      "region": "全球",
      "types": [
        "agent",
        "multi-agent",
        "mcp"
      ],
      "tags": [
        "Agent",
        "MCP",
        "multi-agent",
        "企业协作",
        "开发者工具",
        "Microsoft",
        "2026",
        "全球"
      ],
      "status": "completed",
      "result_status": "partial",
      "dates": {
        "start": "2026-05-12",
        "end": "2026-06-02",
        "announced": "2026-06-18"
      },
      "official_url": "https://devblogs.microsoft.com/powerplatform/agent-academy-hackathon-winners/",
      "verified_on": "2026-08-29",
      "verification_note": "Microsoft 官方结果页按多个 Track 排名；首版精选 Operative Track 的官方前三名，完整赛果请查看来源页。",
      "summary": "围绕 Copilot Studio、MCP、Agent Flow 与多智能体编排的全球黑客松；Operative Track 面向高级编排与安全场景。",
      "scale": {
        "participants": null,
        "submissions": null,
        "countries": null
      },
      "results": [
        {
          "award": "First place",
          "rank": 1,
          "track": "Operative Track",
          "project": "VendorGuard",
          "team": "@experienceswithanishh",
          "summary": "多智能体供应商合同合规系统，编排四个专家 Agent 按 15 条规则完成审查。",
          "project_url": "https://github.com/experienceswithanishh/vendorguard-copilot-studio"
        },
        {
          "award": "Second place",
          "rank": 2,
          "track": "Operative Track",
          "project": "Engagement Hub",
          "team": "@leila-marspooner",
          "summary": "把客户材料转化为风险分析、交付简报和可审计的人机协作流程。",
          "project_url": "https://github.com/leila-marspooner/engagement-hub-agent"
        },
        {
          "award": "Third place",
          "rank": 3,
          "track": "Operative Track",
          "project": "FrostByte AI Advisor",
          "team": "@JBearCode",
          "summary": "面向冰淇淋门店经营者的双 Agent 顾问，区分读取分析与 Dataverse 写入。",
          "project_url": "https://github.com/JBearCode/frostbyte-ai-advisor"
        }
      ]
    },
    {
      "id": "google-gemini-live-agent-challenge-2026",
      "title": "Gemini Live Agent Challenge 2026",
      "organizer": "Google Cloud",
      "year": 2026,
      "region": "全球",
      "types": [
        "agent",
        "live-agent",
        "multi-agent"
      ],
      "tags": [
        "Agent",
        "multi-agent",
        "医疗",
        "生活服务",
        "Google Cloud",
        "2026",
        "全球"
      ],
      "status": "completed",
      "result_status": "partial",
      "dates": {
        "start": null,
        "end": null,
        "announced": "2026-05-15"
      },
      "official_url": "https://cloud.google.com/blog/topics/developers-practitioners/winners-and-highlights-of-the-gemini-live-agent-challenge",
      "verified_on": "2026-08-29",
      "verification_note": "Google Cloud 官方结果页列出大奖、三个类别奖、三个专项奖与荣誉提名；首版收录大奖和五个主要奖项。",
      "summary": "以 Gemini Live API、ADK 和 Google Cloud 构建可看、可听、可说、可实时行动的多模态智能体。",
      "scale": {
        "participants": 11878,
        "submissions": 1536,
        "countries": 151
      },
      "results": [
        {
          "award": "Grand Prize winner",
          "rank": null,
          "track": "Grand Prize",
          "project": "ORION",
          "team": "Aditya Shukla",
          "summary": "用于机器人手术的语音驱动智能协作节点，让外科医生无需离开无菌操作即可获取信息。",
          "project_url": "https://devpost.com/software/orion-operating-room-intelligent-orchestration-node"
        },
        {
          "award": "The Live Agent winner",
          "rank": null,
          "track": "Live Agent",
          "project": "drone-copilot",
          "team": "Bryen Param",
          "summary": "让用户用实时自然语言控制无人机完成导航和视觉巡检。",
          "project_url": "https://devpost.com/software/drone-copilot"
        },
        {
          "award": "Creative Storyteller winner",
          "rank": null,
          "track": "Storyteller",
          "project": "Sankofa",
          "team": "Jeremiah Somoine",
          "summary": "把零散家族史转化为可实时对话的多模态沉浸叙事。",
          "project_url": "https://devpost.com/software/sankofa-y47f9p"
        },
        {
          "award": "UI Navigator winner",
          "rank": null,
          "track": "UI Navigator",
          "project": "Moonwalk",
          "team": "Enaiho Uwas Paul, Aman Kumar Sah",
          "summary": "通过语音和记忆偏好控制桌面工作流的免手操作助手。",
          "project_url": "https://devpost.com/software/moonwalk-tojsay"
        },
        {
          "award": "Best multimodal integration and UX",
          "rank": null,
          "track": "Special Award",
          "project": "Wand",
          "team": "David Li",
          "summary": "结合语音与指向手势完成网页导航和操作的浏览器智能体。",
          "project_url": "https://devpost.com/software/wand-a-live-agent-that-sees-browses-and-clicks-with-you"
        },
        {
          "award": "Best technical execution and architecture",
          "rank": null,
          "track": "Special Award",
          "project": "JohnKeats.AI",
          "team": "Matthew Keats",
          "summary": "根据音高、节奏和语气等线索实时回应情绪的语音陪伴智能体。",
          "project_url": "https://devpost.com/software/johnkeats-ai"
        }
      ]
    },
    {
      "id": "google-adk-hackathon-2025",
      "title": "Agent Development Kit Hackathon 2025",
      "organizer": "Google Cloud",
      "year": 2025,
      "region": "全球",
      "types": [
        "agent",
        "multi-agent"
      ],
      "tags": [
        "Agent",
        "multi-agent",
        "教育",
        "可持续",
        "企业协作",
        "Google Cloud",
        "2025",
        "全球",
        "北美",
        "亚太"
      ],
      "status": "completed",
      "result_status": "partial",
      "dates": {
        "start": null,
        "end": null,
        "announced": "2025-09-02"
      },
      "official_url": "https://cloud.google.com/blog/products/ai-machine-learning/adk-hackathon-results-winners-and-highlights",
      "verified_on": "2026-08-29",
      "verification_note": "Google Cloud 官方结果页列出 1 个大奖、4 个地区奖和 3 个荣誉提名；首版收录大奖与全部地区奖。",
      "summary": "使用 Google ADK 设计与编排多智能体协作的全球赛事，覆盖自动化、分析、客户服务和内容生成。",
      "scale": {
        "participants": 10400,
        "submissions": 477,
        "countries": 62
      },
      "results": [
        {
          "award": "Grand Prize",
          "rank": null,
          "track": "Grand Prize",
          "project": "SalesShortcut",
          "team": "Merdan Durdyyev, Sergazy Nurbavliyev",
          "summary": "以 34 个专门 Agent 自动完成销售线索、调研、提案与外联。",
          "project_url": "https://devpost.com/software/salesshortcut"
        },
        {
          "award": "North America regional winner",
          "rank": null,
          "track": "North America",
          "project": "Energy Agent AI",
          "team": "David Babu",
          "summary": "通过 ADK 编排多智能体改造能源客户管理。",
          "project_url": "https://devpost.com/software/energy-agent-ai"
        },
        {
          "award": "Latin America regional winner",
          "rank": null,
          "track": "Latin America",
          "project": "Edu.AI",
          "team": "Giovanna Moeller",
          "summary": "为巴西教育场景提供作文评价、个性化学习计划与跨学科模拟题。",
          "project_url": "https://devpost.com/software/edu-ai-multi-agent-educational-system-for-brazil"
        },
        {
          "award": "Asia Pacific regional winner",
          "rank": null,
          "track": "Asia Pacific",
          "project": "GreenOps",
          "team": "Aishwarya Nathani, Nikhil Mankani",
          "summary": "持续审计、预测和优化云基础设施可持续性的智能体团队。",
          "project_url": "https://devpost.com/software/greenops-gzp4aj"
        },
        {
          "award": "EMEA regional winner",
          "rank": null,
          "track": "EMEA",
          "project": "Nexora-AI",
          "team": "Matthias Meierlohr, Luca Bozzetti, Erliassystems, Markus Huber",
          "summary": "结合互动课程、图像、测验与智能支持的个性化教育系统。",
          "project_url": "https://devpost.com/software/teachai-upzofa"
        }
      ]
    },
    {
      "id": "aws-summit-japan-agent-hackathon-2025",
      "title": "AWS Summit Japan 2025 生成 AI Agent Hackathon",
      "organizer": "AWS",
      "year": 2025,
      "region": "日本",
      "types": [
        "agent"
      ],
      "tags": [
        "Agent",
        "生活服务",
        "企业协作",
        "AWS",
        "2025",
        "亚太",
        "日本"
      ],
      "status": "completed",
      "result_status": "verified",
      "dates": {
        "start": "2025-05-01",
        "end": "2025-06-26",
        "announced": "2025-07-31"
      },
      "official_url": "https://aws.amazon.com/jp/blogs/news/aiagent_hackathon_report/",
      "verified_on": "2026-08-29",
      "verification_note": "AWS 日本官方博客明确列出最优秀奖、准优胜和第 3 名。官方材料未提供三个项目的独立仓库链接。",
      "summary": "以“把 AI Agent 用到极致来实现某种目标”为主题，从 14 支入选团队中评出决赛六强与前三名。",
      "scale": {
        "participants": null,
        "submissions": null,
        "countries": 1
      },
      "results": [
        {
          "award": "最優秀賞",
          "rank": 1,
          "track": "Overall",
          "project": "KanpAI",
          "team": "WhiteBox お酒同好会",
          "summary": "围绕聚会交流设计、整合电话等能力并以 Agent 推动持续互动的生活服务。",
          "project_url": null
        },
        {
          "award": "準優勝",
          "rank": 2,
          "track": "Overall",
          "project": "プロジェクト引継ぎAI",
          "team": "チームぶち上げ",
          "summary": "让 AI 承担项目全局视角，降低人员变动时的知识交接成本。",
          "project_url": null
        },
        {
          "award": "第3位",
          "rank": 3,
          "track": "Overall",
          "project": "おそとびより",
          "team": "かっぱときゅうりと味噌",
          "summary": "面向育儿家庭的外出决策支持，并通过用户反馈持续改进。",
          "project_url": null
        }
      ]
    }
  ]
};
