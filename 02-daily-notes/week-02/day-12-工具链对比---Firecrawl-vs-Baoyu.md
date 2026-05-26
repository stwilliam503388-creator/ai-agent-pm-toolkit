# Day 12 — 工具链对比 - Firecrawl vs Baoyu

## 今日目标

用同一个URL实测Firecrawl和baoyu-url-to-markdown的抓取成功率，做技术选型对比。

---

## 核心概念

## 1. 为什么做工具链对比

你已经在用baoyu-url-to-markdown做网页抓取。Firecrawl是123k Stars的明星项目。选哪个？不靠感觉，靠数据。

## 2. 对比维度

| 维度 | Firecrawl | baoyu-url-to-markdown |
|------|-----------|----------------------|
| 抓取方式 | API + 浏览器渲染 | Chrome CDP |
| 反爬能力 | 内置反反爬 | 依赖CDP的隐身能力 |
| JS渲染 | 支持 | 支持 |
| 输出格式 | Markdown/HTML/Screenshot | Markdown |
| 成本 | 免费额度+付费 | 免费（本地浏览器） |
| 部署 | 云端API | 本地 |

## 3. 实测方法

选3类URL各测3个：
- 类型A：静态博客/文档（应该都好抓）
- 类型B：JS渲染页面（看谁渲染更完整）
- 类型C：反爬严格的网站（看谁抓得到）

记录每个URL的：抓取成功率、内容完整度、耗时。

---

## 今日产出

- [ ] 选3类URL各3个做实测
- [ ] 创建 tools-comparison-report.md
- [ ] 给出选型结论：迁移到Firecrawl还是继续用baoyu

---

## 面试要点

**Q1：为什么PM需要关注工具链选型？**
- 工具链直接影响数据质量->影响Agent输出质量
- 成本差异可能很大（云端API vs 本地免费）
- 技术选型是PM的核心决策权之一
- 面试时能说出Firecrawl和它的竞品，展示技术广度
