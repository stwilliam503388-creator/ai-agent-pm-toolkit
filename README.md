# AI Agent PM Toolkit — 12周完整学习项目

> 一个AI Agent产品经理的完整学习输出：84篇笔记 + 6个项目代码 + 全套考试系统 + 面试策略。
> 不只是学，是做出能被看到的东西。

---

## 这是什么

2026年，AI Agent PM是最稀缺的产品经理方向。这个项目是我12周系统学习的全部产出物：

- **84篇每日学习笔记**（46,000+字）
- **6个实战项目**（~1,000行Python/Shell代码）
- **10次周测 + 3次模拟面试 + 期末大考**
- **PRD模板(v1-v3) + 设计哲学 + 面试策略 + STAR故事库**

---

## 目录结构

```
ai-agent-pm-toolkit/
├── README.md                           # 本文件
├── PLAN.md                             # 生成方案与执行计划
├── .gitignore
│
├── 01-learning-plan/                   # 学习计划主文档
│   └── AI-Agent-PM-12周学习计划.md      # 841行完整计划
│
├── 02-daily-notes/                     # 84篇每日学习笔记
│   ├── week-01/ ~ week-12/             # 每周7篇
│
├── 03-exams/                           # 考试系统
│   ├── self-tests/                     # 10次每周自测（含参考答案）
│   ├── mock-interviews/                # 3次模拟面试题
│   ├── final-exam/                     # 期末笔试+口试题
│   └── templates/                      # 考试模板
│
├── 04-projects/                        # 6个实战项目
│   ├── p1-mcp-server/                  # MCP Server (~100行)
│   ├── p2-cron-dashboard/              # Cron健康仪表盘 (~150行)
│   ├── p3-security-test/               # Agent安全测试套件 (~80行)
│   ├── p4-multi-agent-writer/          # Multi-Agent写作系统 (~300行)
│   ├── p5-eval-compare/                # Agent评估对比实验 (~200行)
│   └── p6-video-pipeline/              # 视频知识管道 (~50行)
│
├── 05-reference/                       # 参考资料
│   ├── knowledge-system.md             # 6层知识体系详解
│   ├── resource-index.md               # 31个资源速查索引
│   └── star-stories.md                 # 6个项目STAR故事
│
└── 06-outputs/                         # 关键产出物
    ├── prd-templates/                  # PRD模板 v1/v2/v3
    ├── design-philosophy.md            # 5种Agent设计哲学
    ├── interview-strategy.md           # 面试策略+高频考点
    └── comparison-reports/             # 产品对比+公司面经
```

---

## 怎么使用

### 如果你是AI Agent PM学习者

1. 从 `01-learning-plan/` 开始，了解12周的整体结构
2. 按周顺序读 `02-daily-notes/` 的笔记
3. 每周末做 `03-exams/self-tests/` 的自测题
4. 每2周做一次模拟面试
5. 跟着 `04-projects/` 的项目动手写代码

### 如果你在准备Agent PM面试

1. 先看 `06-outputs/interview-strategy.md` 了解高频考点
2. 看 `05-reference/star-stories.md` 准备你的项目故事
3. 做 `03-exams/mock-interviews/` 的模拟面试题
4. 看 `06-outputs/design-philosophy.md` 建立产品设计框架

### 如果你好奇Agent产品设计

1. 看 `06-outputs/design-philosophy.md` 了解5种设计流派
2. 看 `06-outputs/comparison-reports/product-comparison-table.md` 对比6个明星产品
3. 看 `04-projects/p5-eval-compare/` 了解如何用数据评估Agent

---

## 核心产出物

| 产出 | 文件 | 面试价值 |
|------|------|---------|
| 学习笔记 | 84篇, 46K字 | 知识广度 |
| 项目代码 | 6个, ~1K行 | 动手能力 |
| 自测题 | 10次, 含答案 | 知识深度 |
| 模拟面试 | 3次, 含产品分析题 | 面试模拟 |
| PRD模板 | v1/v2/v3 | 产品方法论 |
| 设计哲学 | 5种流派分析 | 独立思考 |
| 评估实验 | 3组x5任务x3轮 | 数据驱动 |
| STAR故事 | 6个项目故事 | 面试叙事 |

---

## 技术覆盖

- **LLM基础**: Transformer, Tokenization, 推理参数
- **Agent核心**: ReAct, Tool Use, Planning, Memory
- **工具协议**: Function Calling, MCP, A2A
- **RAG**: 分块策略, 向量库, Embedding, Reranker, RAGAS评估
- **评估安全**: 监控指标, 告警体系, Prompt注入, Guardrails
- **产品商业**: PRD设计, 设计哲学, 成本模型, 面试策略

---

## 借鉴与引用

本项目学习内容参考了大量优秀的 GitHub 开源项目和社区资源，在此致谢。

### Agent 产品与框架（设计哲学来源）

| 项目 | Stars | 在本项目中的引用 |
|------|-------|-----------------|
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | ⭐189K | Week 5 产品拆解 — OS派代表 |
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | ⭐105K | Week 5 产品拆解 — 专才派代表 |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | ⭐95K | Week 5 产品拆解 — 触手派代表 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | ⭐78K | Week 5 参考 — 跨会话记忆系统 |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | ⭐69K | Week 5 产品拆解 — 编排派代表 |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | ⭐59K | Week 5 参考 — 多 Harness Agent OS |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | ⭐57K | Week 3 记忆系统设计 — 记忆派代表 |
| [aaif-goose/goose](https://github.com/aaif-goose/goose) | ⭐46K | Week 5 产品拆解 — 基金会治理派代表 |

### Agent 开发工具与框架

| 项目 | Stars | 在本项目中的引用 |
|------|-------|-----------------|
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | ⭐123K | Week 2 工具链对比 — 网页抓取引擎 |
| [raga-ai-hub/RagaAI-Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst) | ⭐16K | Week 4+7 — Agent 可观测性 SDK |
| [openlit/openlit](https://github.com/openlit/openlit) | ⭐2.5K | Week 4 — OpenTelemetry 原生可观测性 |
| [mozilla-ai/any-agent](https://github.com/mozilla-ai/any-agent) | ⭐1.2K | Week 2 — 跨框架统一调用接口 |
| [awslabs/agent-evaluation](https://github.com/awslabs/agent-evaluation) | ⭐363 | Week 7 — AWS 官方 Agent 评估框架 |

### 学习教程与案例库

| 项目 | Stars | 在本项目中的引用 |
|------|-------|-----------------|
| [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) | ⭐18K+ | Week 5 — 500+ Agent 落地案例 |
| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | ⭐5.7K | Phase 1 — 手搓 Agent 框架教程 |
| [adongwanai/AgentGuide](https://github.com/adongwanai/AgentGuide) | ⭐5.1K | Week 11 — Agent 开发+面试全指南 |
| [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) | — | 40+ LangGraph 实用示例参考 |
| [Scodive/AI-Agent-Guide](https://github.com/Scodive/AI-Agent-Guide) | — | 架构全景 + 关键技术论文索引 |
| [caramaschiHG/awesome-ai-agents-2026](https://github.com/caramaschiHG/awesome-ai-agents-2026) | ⭐909 | Week 5 — 300+ 资源生态图 |

### 面试资源

| 项目 | Stars | 在本项目中的引用 |
|------|-------|-----------------|
| [WeThinkIn/AIGC-Interview-Book](https://github.com/WeThinkIn/AIGC-Interview-Book) | ⭐3.8K | Week 11 — 《三年面试五年模拟》 |
| [bcefghj/ai-agent-interview-guide](https://github.com/bcefghj/ai-agent-interview-guide) | ⭐987 | 全程 — 200+ 中文面试题 |
| [smile-struggler/kaomian](https://github.com/smile-struggler/kaomian) | ⭐53 | Week 11 — 大厂面经频次统计 |
| [Zchary1106/agent-interview-hub](https://github.com/Zchary1106/agent-interview-hub) | ⭐25 | Week 11 — 按公司分类面经库 |
| [chusimin/AIPM-Skills](https://github.com/chusimin/AIPM-Skills) | ⭐41 | Week 6 — Claude Skills 工具链 |

### 在线资源

- [crackpminterview.com](https://crackpminterview.com) — 英文 AI PM 面试 6 类核心题型
- [lockedinai.com](https://lockedinai.com) — 56 道 AI PM 面试题 + 样答
- [igotanoffer.com](https://igotanoffer.com) — 真实 AI PM 面试题（Amazon/Microsoft/eBay）
- [anthropic.com/research](https://anthropic.com/research) — MCP/A2A/安全最新论文
- [openai.com/index](https://openai.com/index) — Agents SDK / GPTs 更新
- [artefact.com/blog/ai-cost-calculator](https://artefact.com/blog/ai-cost-calculator) — Token 成本估算器

> 以上项目的所有权利归原作者所有。本项目仅在学习过程中引用和参考了这些资源的内容与方法论。

---

## 关于作者

12周前，我是一个想转AI Agent PM的产品经理。
12周后，我有了这个仓库——84篇笔记、6个项目、全套考试、面试策略。

这个仓库就是我的简历。

---

**Start**: 2026-05-17 → **Deadline**: 2026-08-15
**License**: MIT
