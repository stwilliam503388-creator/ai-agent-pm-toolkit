# Day 20 — P1收尾 - MCP Server接入与测试

## 今日目标

把MCP Server接入Hermes配置，端到端验证3个工具。

---

## 核心概念

## 1. 接入Hermes

在Hermes的MCP配置中注册Server：
```json
{"mcpServers": {"obsidian-vault": {"command": "python", "args": ["mcp-obsidian-server.py"]}}}
```

## 2. 测试清单

- search_notes("RAG") -> 返回包含RAG的笔记
- get_daily_note("2026-05-20") -> 返回当天笔记
- list_recent_notes(7, "概念") -> 返回最近7天概念笔记
- 错误处理：搜不存在的日期？
- 边界：空vault、超大笔记

## 3. P1面试故事

我写了一个MCP Server连接个人知识库，Agent可以直接搜索和引用我的笔记。FastMCP框架，3个工具，覆盖搜索、查询、列表三种场景。

---

## 今日产出

- [ ] 接入Hermes配置
- [ ] 通过3个工具功能测试
- [ ] 记录P1面试故事要点

---

## 面试要点

P1是面试讲MCP故事的素材。记住：做了什么、用了什么、验证了什么。
