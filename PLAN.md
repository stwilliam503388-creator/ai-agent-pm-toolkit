# AI Agent PM 完整项目生成方案

> 目标：把 12 周学习计划的所有产出物一次性本地生成 → 推 GitHub
> 执行方式：分 7 个 Phase，每个 Phase 用 `execute_code` Python 脚本批量写入文件
> 预计总文件数：~140 个 | 总字数：~15 万字 | 总代码行：~1000 行

---

## 项目结构（已创建）

```
ai-agent-pm-toolkit/
├── README.md                          # 项目介绍 + 使用指南
├── PLAN.md                            # 本文件
├── 01-learning-plan/
│   └── AI-Agent-PM-12周学习计划.md     # ✅ 已复制
├── 02-daily-notes/
│   ├── week-01/  ~ week-12/           # 84 篇学习笔记（每篇 800-3000 字）
├── 03-exams/
│   ├── self-tests/                    # 8 次周测（w1-w8, w10-w11）
│   ├── mock-interviews/               # 3 次模拟面试题
│   ├── final-exam/                    # 期末笔试 + 口试题
│   └── templates/                     # 自测模板 + 面试评分模板 + README模板
├── 04-projects/
│   ├── p1-mcp-server/                 # ~100 行 Python
│   ├── p2-cron-dashboard/             # ~150 行 Python
│   ├── p3-security-test/              # ~80 行 Python
│   ├── p4-multi-agent-writer/         # ~300 行 Python
│   ├── p5-eval-compare/               # ~200 行 Python
│   └── p6-video-pipeline/             # Shell 脚本 + 文档
├── 05-reference/
│   ├── knowledge-system.md            # 6 层知识体系详解
│   ├── resource-index.md              # 31 个资源速查
│   └── star-stories.md                # 6 个项目 STAR 故事
├── 06-outputs/
│   ├── prd-templates/                 # PRD 模板 v1/v2/v3
│   ├── design-philosophy.md           # 5 种 Agent 设计哲学
│   ├── interview-strategy.md          # 面试策略 + 高频考点
│   └── comparison-reports/
│       ├── product-comparison-table.md # 6 产品对比表
│       └── company-interview-analysis.md # 公司面经分析
└── .gitignore
```

---

## 执行顺序（7 个 Phase）

### Phase 1：84 天学习笔记（最重，先跑）

使用 `execute_code` 脚本，一次生成 84 个 .md 文件。

**生成策略**：
- 每篇 800-2000 字，知识整理语气
- 结构固定：今日目标 / 核心概念 / 关键对比 / 今日产出 / 面试要点
- 从学习计划的 Day 1-84 表中逐天提取主题，生成对应内容
- 每周 7 篇，放到 `02-daily-notes/week-XX/` 下

**执行**：告诉我 "执行 Phase 1"，我会用 execute_code 批量生成。

---

### Phase 2：考试系统（自测 + 模拟面试 + 期末考 + 模板）

**内容**：
- 8 次周测（w1-w8, w10-w11），每次 5 题（2概念+2选型+1设计），附参考答案
- 3 次模拟面试（w2基线/w5产品分析/w9项目拷打），每次 6 题
- 期末笔试（概念+案例+产品设计三部分）
- 期末口试（自我介绍+问答+反问）
- 3 个模板：self-test-template.md, mock-interview-score-template.md, project-readme-template.md

**执行**：告诉我 "执行 Phase 2"

---

### Phase 3：6 个实战项目代码

| 项目 | 文件 | 行数 | 难度 |
|------|------|------|------|
| P1 MCP Server | `mcp-obsidian-server.py` + README.md | ~100 | ★★ |
| P2 Cron 仪表盘 | `cron-dashboard.py` + `健康看板.md` | ~150 | ★★ |
| P3 安全测试 | `agent-security-test-suite.py` + `security-test-report.md` | ~80 | ★★ |
| P4 Multi-Agent | `crewai_writer.py` + `agents.py` + `tasks.py` + README.md | ~300 | ★★★★ |
| P5 评估实验 | `eval_runner.py` + `eval-report.md` + README.md | ~200 | ★★★ |
| P6 视频管道 | `run_pipeline.sh` + README.md | ~50 | ★★★ |

**注意**：P4 有备选降级——如果 CrewAI 依赖不装，改用 LangGraph 链式调用版本。

**执行**：告诉我 "执行 Phase 3"

---

### Phase 4：关键产出物

- **PRD 模板 v1/v2/v3**（06-outputs/prd-templates/）
  - v1：基础版（产品目标、Agent选型、工具定义、评估、异常处理、安全）
  - v2：迭代版（加数据驱动决策、A/B测试设计）
  - v3：完整版（加设计哲学决策章节）
- **设计哲学文档**（06-outputs/design-philosophy.md）
  - OS派 / 导演派 / 触手派 / 记忆派 / 专才派 五种流派深度分析
- **面试策略文档**（06-outputs/interview-strategy.md）
- **STAR 故事库**（05-reference/star-stories.md）
- **产品对比报告**（06-outputs/comparison-reports/product-comparison-table.md）
- **公司面经分析**（06-outputs/comparison-reports/company-interview-analysis.md）

**执行**：告诉我 "执行 Phase 4"

---

### Phase 5：参考文档

- **6 层知识体系详解**（05-reference/knowledge-system.md）
- **31 个资源速查索引**（05-reference/resource-index.md）

**执行**：告诉我 "执行 Phase 5"

---

### Phase 6：README.md + .gitignore

项目根 README，包含：
- 项目简介
- 目录结构导航
- 使用指南（怎么用这套内容学习）
- 面试产出物索引

**执行**：告诉我 "执行 Phase 6"

---

### Phase 7：推 GitHub

```bash
cd /Users/liuwei/ai-agent-pm-toolkit
git init
git add .
git commit -m "feat: AI Agent PM 12周完整学习项目 — 84篇笔记+6个项目+全套考试系统"
gh repo create ai-agent-pm-toolkit --public --source=. --push
```

**执行**：告诉我 "执行 Phase 7"

---

## 执行方式

每次告诉我一个 Phase 编号，如 "执行 Phase 1"，我会用 `execute_code` Python 脚本批量生成文件。

**为什么不用 delegate_task**：已验证 3 个并行子 agent 全部被中断，execute_code 单脚本批量写入更可靠更快。

**预计总时间**：
- Phase 1（84篇笔记）：~5 分钟（execute_code 批量）
- Phase 2-6：各 1-2 分钟
- Phase 7（推送）：30 秒
- **总计：~15 分钟**

---

## 生成质量保证

每篇笔记保证：
- 至少 800 字实质内容（不灌水）
- 含可检查的具体产出物
- 含 2-3 道面试要点
- 知识整理语气（非教学语气）

代码项目保证：
- 可独立运行（有 `if __name__ == "__main__"` 自测）
- 英文注释
- 附 README.md
