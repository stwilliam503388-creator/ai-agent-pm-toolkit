# P4: Multi-Agent Writing System

> 一句话：4-Agent协作写作系统（研究员+写手+审稿人+协调者）。

## 项目信息

- **对应课程**：AI Agent PM 12周学习计划 Week 5-6
- **难度**：★★★★☆
- **代码量**：~300行
- **技术栈**：CrewAI（主方案）/ LangGraph（降级方案）

## 架构

```
用户输入主题
  -> Agent1 研究员：搜索信息，输出摘要
  -> Agent2 写手：根据摘要写初稿
  -> Agent3 审稿人：检查事实和语气
  -> Agent4 协调者：汇总最终输出
```

## 快速开始

```bash
pip install crewai  # 或 pip install langgraph（降级方案）
python crewai_writer.py "2026 AI Agent Industry Trends"
```

## 双方案设计

- **CrewAI版**：完整4-Agent协作，适合展示Multi-Agent能力
- **LangGraph降级版**：轻量链式调用，适合环境受限时快速跑通

## 面试故事

> 我设计了一个4-Agent写作系统。研究员搜集信息，写手生成初稿，审稿人检查事实，协调者把控最终质量。对比单Agent，Multi-Agent在深度长文场景质量提升明显。

## 学习收获

- Multi-Agent协作的设计模式
- Agent间通信和工作流编排
- 降级方案的设计思维
