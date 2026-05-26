# STAR 故事库 — 6个项目的故事素材

> 每个项目准备一个30秒的STAR故事，面试时信手拈来。

---

## P1: MCP Server for Obsidian Vault

| 要素 | 内容 |
|------|------|
| **S**ituation | 我的Obsidian知识库有500+篇笔记，但Agent无法直接搜索和引用这些知识 |
| **T**ask | 写一个MCP Server，让Agent能搜索笔记、获取日记、查看近期笔记 |
| **A**ction | 用Python FastMCP实现3个工具（search_notes/get_daily_note/list_recent_notes），接入Hermes配置 |
| **R**esult | Agent可以实时搜索我的知识库，回答问题时引用我的笔记。MCP协议的理解从理论变成实践 |

**30秒版本**：我写了一个MCP Server连接我的个人知识库，Agent可以直接搜索和引用500+篇笔记。用Python实现3个工具，覆盖了MCP协议的核心概念：工具定义、资源暴露、安全分级。

---

## P2: Cron Health Dashboard

| 要素 | 内容 |
|------|------|
| **S**ituation | 我有30个Agent定时任务，但不知道哪些在正常运行、哪些在退化 |
| **T**ask | 搭建一个可视化健康仪表盘，实时监控所有cron任务 |
| **A**ction | 用Python解析cron日志数据，生成终端彩色仪表盘。绿色=健康，红色=告警 |
| **R**esult | 30个任务的状态一目了然。发现并修复了3个持续退化的任务，整体健康度从82%提升到96% |

**30秒版本**：我为30个Agent定时任务搭建了健康仪表盘。用Python解析日志数据，实时显示每个任务的成功率、耗时和趋势。这让我从盲飞变成了有数据的管理。

---

## P3: Agent Security Test Suite

| 要素 | 内容 |
|------|------|
| **S**ituation | Agent有行动能力（写文件、调API），安全不是可选项 |
| **T**ask | 对我的Agent做系统性安全测试，模拟4类常见攻击 |
| **A**ction | 写了自动化测试脚本，覆盖Prompt注入、工具滥用、角色扮演、上下文泄露4大类 |
| **R**esult | 发现了3个防御缺口，修复后全部8项测试通过。把测试集成到部署流程中 |

**30秒版本**：我对Agent做了系统性安全测试，写了自动化脚本覆盖4类Prompt注入攻击。发现了3个防御缺口并修复。这套测试现在每次部署前自动跑。

---

## P4: Multi-Agent Writing System

| 要素 | 内容 |
|------|------|
| **S**ituation | 单Agent写长文经常遗漏关键信息，质量不稳定 |
| **T**ask | 设计一个4-Agent协作写作系统（研究员+写手+审稿人+协调者） |
| **A**ction | 用CrewAI定义4个Agent的角色和协作流程，同时准备了LangGraph降级方案 |
| **R**esult | Multi-Agent在长文场景质量提升明显。但发现对短文章来说，单Agent更快更便宜 |

**30秒版本**：我设计了一个4-Agent写作系统。研究员搜集信息，写手出初稿，审稿人检查事实，协调者把控最终质量。关键发现：Multi-Agent不是银弹——复杂任务值得用，简单任务单Agent更高效。

---

## P5: Agent Evaluation Comparison

| 要素 | 内容 |
|------|------|
| **S**ituation | Agent产品选型靠直觉，缺乏数据支撑 |
| **T**ask | 设计一个标准化的Agent评估对比实验 |
| **A**ction | 定义5个标准任务，对比3组Agent（Hermes/ECC/DeerFlow），各跑3轮消除随机性 |
| **R**esult | DeerFlow得分最高但Token贵50%。ECC在质量/成本比上最优。数据驱动选型 |

**30秒版本**：我设计了一个Agent评估实验，定义了5个标准化任务，对比了3组Agent配置。发现多Agent方案质量高但成本贵50%，为产品选型提供了数据基础而非直觉。

---

## P6: Video Knowledge Pipeline

| 要素 | 内容 |
|------|------|
| **S**ituation | 大量B站技术视频有价值但看完就忘，无法沉淀为知识 |
| **T**ask | 搭建一条从视频链接到结构化笔记的全自动管道 |
| **A**ction | 用Shell脚本串联yt-dlp下载+Whisper转写+LLM摘要+Obsidian归档 |
| **R**esult | 一条命令跑完全链路，视频知识自动沉淀到知识库。这是多模态Agent的端到端实践 |

**30秒版本**：我搭建了一个从B站视频到Obsidian笔记的全自动知识管道。视频链接->音频下载->Whisper转写->LLM摘要->归档，一条命令搞定。这是多模态Agent的端到端实践。
