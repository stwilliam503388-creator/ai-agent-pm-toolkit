# P2: Cron Health Dashboard

> 一句话：为30个Agent定时任务搭建可视化健康仪表盘。

## 项目信息

- **对应课程**：AI Agent PM 12周学习计划 Week 4
- **难度**：★★☆☆☆
- **代码量**：~150行
- **技术栈**：Python, ANSI terminal colors

## 功能

- 解析Hermes cron job数据
- 终端彩色可视化仪表盘
- 成功率分色显示（绿>95%, 黄90-95%, 红<90%）
- 任务延迟监控
- 整体健康度摘要

## 快速开始

```bash
python cron-dashboard.py
python cron-dashboard.py --save  # 保存到文件
```

## 面试故事

> 我为30个Agent定时任务搭建了完整的健康监控仪表盘。实时显示每个任务的成功率、耗时、延迟和趋势。绿色正常，红色告警，让运维从盲飞变成可视化。

## 学习收获

- Agent可观测性的实践理解
- 终端UI设计
- 监控指标的定义与可视化
