# Day 9 — A2A协议与跨框架实战

## 今日目标

理解A2A协议的设计动机，掌握A2A vs MCP的核心区别，体验any-agent跨框架调用。

---

## 核心概念

## 1. A2A协议：Agent之间如何协作

A2A (Agent-to-Agent) 是Google推出的Agent间通信协议。如果说MCP解决了Agent怎么调用工具，A2A解决的是Agent之间怎么对话和协作。

核心设计：
- **Agent Card**：每个Agent发布一张能力卡片，描述自己能做什么
- **Task**：Agent之间通过Task传递工作
- **Artifact**：工作成果以Artifact形式返回

## 2. A2A vs MCP：不是竞争，是互补

| 维度 | MCP | A2A |
|------|-----|-----|
| 通信方向 | Agent -> 工具（垂直） | Agent <-> Agent（水平） |
| 交互模式 | 单次调用 | 持续协作 |
| 提出方 | Anthropic | Google |
| 适用场景 | 查数据库、调API | 多Agent协作、任务分发 |
| 协议风格 | REST-like | Task-oriented |

面试加分回答：这两个协议不会互相替代。就像你不会用HTTP替代WebSocket——场景不同。

## 3. any-agent：跨框架调用的桥梁

mozilla-ai/any-agent是一个统一接口，让你用同一套代码调用LangChain/CrewAI/AutoGen等不同框架的Agent。

PM价值：做工具链选型时，不用绑定具体框架。先跑通，再决定用哪个。

---

## 今日产出

- [ ] 完成A2A vs MCP对比表
- [ ] 用any-agent跑一次跨框架调用
- [ ] 写any-agent试用记录

---


---

## A2A vs MCP：一张表说清楚

| 维度 | MCP | A2A |
|------|-----|-----|
| 解决什么问题 | Agent怎么调用工具 | Agent之间怎么协作 |
| 通信模式 | 请求-响应（同步） | 任务-结果（异步） |
| 提出者 | Anthropic | Google |
| 设计哲学 | 工具是资源，统一管理 | Agent是节点，去中心化协作 |
| 类比 | USB-C协议 | HTTP协议 |
| 谁更需要 | 单Agent + 多工具 | 多Agent系统 |
| 成熟度 | v1.0，200+ Server | 早期，Google内部推动 |
| 与Function Calling关系 | MCP封装FC | 无关 |

核心认知：MCP和A2A不是竞争关系。一个管工具，一个管Agent。就像你不会用HTTP替代USB-C。

### 什么时候A2A过度设计

如果你的系统只有2-3个Agent，且协作流程固定，不需要A2A。直接硬编码Agent间的调用关系更简单、更快、更可调试。

A2A的价值在Agent数量和类型都不确定时的动态发现和协作。小系统不需要。

---

## 面试要点

**Q1：什么时候需要A2A？**
- 多个Agent协作完成复杂任务
- 需要Agent之间的能力互补（一个做研究，一个做写作）
- 分布式Agent系统（不同Agent部署在不同服务器）
- 简单场景不需要，MCP+单Agent就够了

**Q2：PM为什么需要了解A2A？**
- 它是多云/多供应商Agent生态的基础协议
- 理解A2A能帮你设计更灵活的Agent产品架构
- 2025-2026面试热点，展示知识广度
