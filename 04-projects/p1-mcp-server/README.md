# P1: MCP Server for Obsidian Vault

> 一句话：把 Obsidian 知识库暴露为 MCP 工具，让 Agent 可以直接搜索和引用你的笔记。

## 项目信息

- **对应课程**：AI Agent PM 12周学习计划 Week 3
- **难度**：★★☆☆☆
- **代码量**：~100行
- **技术栈**：Python, FastMCP SDK（兼容）

## 功能

3个MCP工具：
1. `search_notes(query)` — 搜索vault笔记内容
2. `get_daily_note(date)` — 获取指定日期的日记
3. `list_recent_notes(days, category)` — 近期笔记列表

## 快速开始

```bash
export VAULT_PATH=/path/to/your/obsidian/vault
python mcp-obsidian-server.py
```

## 接入Hermes

在Hermes的MCP配置中注册：
```json
{
  "mcpServers": {
    "obsidian-vault": {
      "command": "python",
      "args": ["mcp-obsidian-server.py"],
      "env": {"VAULT_PATH": "/path/to/vault"}
    }
  }
}
```

## 面试故事

> 我写了一个MCP Server连接个人知识库，Agent可以直接搜索和引用笔记。用了Python标准库实现，3个工具覆盖搜索、查询、列表三种典型场景。接入Hermes后，Agent能实时引用我学到的东西。

## 学习收获

- MCP协议的实践理解
- 工具定义和权限分级的设计
- Agent与本地文件的交互模式
