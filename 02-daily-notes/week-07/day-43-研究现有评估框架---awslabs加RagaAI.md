# Day 43 — 研究现有评估框架 - awslabs加RagaAI

## 今日目标

研究两个Agent评估框架（awslabs/agent-evaluation和RagaAI-Catalyst），了解业界评估标准。

---

## 核心概念

## 1. awslabs/agent-evaluation (363 Stars)

AWS官方的Agent评估框架：
- 任务定义范式：标准化Agent测试任务的定义方式
- 评分体系：多维度自动化评估
- 基准数据集：内置多种Agent测试场景

## 2. RagaAI-Catalyst评估API

- 评估维度：成功率、延迟、Token效率、幻觉率
- 对比框架：A/B测试不同Agent配置
- 可视化：评估结果自动生成图表

## 3. 对比产品阵容确定

评估对比的三组Agent：
1. Hermes原生（你的cron job当前配置）
2. ECC优化版（用ECC的Agent OS理念优化Prompt）
3. DeerFlow风格版（用DeerFlow的编排理念重组任务流）

---

## 今日产出

- [ ] 阅读awslabs/agent-evaluation文档
- [ ] 了解RagaAI评估API
- [ ] 确定3组对比Agent的配置方案

---

## 面试要点

**Q1：如何设计一个客观的Agent评估方案？**
- 5个标准化任务（同一任务给3个Agent各跑一次）
- 4维评分（成功率/耗时/Token/完整度）
- 3轮重复（排除随机性）
