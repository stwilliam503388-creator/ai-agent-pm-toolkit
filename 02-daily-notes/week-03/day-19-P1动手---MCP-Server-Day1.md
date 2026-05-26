# Day 19 — P1动手 - MCP Server Day1

## 今日目标

用Python FastMCP实现一个连接Obsidian vault的MCP Server。今天完成3个工具的基本实现。

---

## 核心概念

## 1. 项目目标

写一个MCP Server，暴露Obsidian vault为3个工具：
- search_notes(query)：搜索笔记内容
- get_daily_note(date)：获取指定日期笔记
- list_recent_notes(days, category)：近期笔记列表

## 2. 技术栈

FastMCP(Python MCP SDK) + 文件系统读取（直接读.md文件）

## 3. search_notes实现思路

1. 遍历vault目录所有.md文件
2. 对每个文件grep关键词
3. 返回匹配文件名+匹配行+上下文

## 4. 今日产出

- mcp-obsidian-server.py（3个工具的功能代码）
- 用MCP Inspector本地验证

---

## 今日产出

- [ ] 完成mcp-obsidian-server.py初版
- [ ] search_notes可用
- [ ] get_daily_note可用
- [ ] list_recent_notes可用

---

## 面试要点

今天的重点是写代码。这个项目是你面试时讲MCP故事的素材。
