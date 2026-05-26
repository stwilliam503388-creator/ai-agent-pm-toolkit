# P5: Agent Evaluation Comparison Experiment

一句话：3组Agent配置 x 5个标准任务 x 3轮评估的对比实验。

## 项目信息

- **对应课程**：AI Agent PM 12周学习计划 Week 7-8
- **难度**：★★★☆☆
- **代码量**：~200行
- **技术栈**：Python (stdlib + dataclasses)

## 实验设计

```
5个标准化任务 (GitHub Trending / Framework Compare / PRD Design / Tool Call / Multi-Step)
  x 3组Agent (Hermes Native / ECC Optimized / DeerFlow Style)
  x 3轮评估
  = 45次实验
```

## 快速开始

```bash
cd 04-projects/p5-eval-compare
python eval_runner.py
# 输出: eval-report.md + raw-results.json
```

## 评估维度

| 维度 | 权重 | 说明 |
|------|------|------|
| Completeness | 30-40% | 是否覆盖所有要求 |
| Accuracy | 20-50% | 事实准确性 |
| Structure | 20-30% | 组织清晰度 |
| Efficiency | 10-20% | Token使用效率 |

## 面试故事

我设计了一个Agent评估框架，对比了3种架构在5个任务上的表现。做了3轮实验排除随机性。发现Multi-Agent在复杂任务上质量高但成本多50%。这是数据驱动的产品选型思维。

## 学习收获

- Agent评估的实验设计方法
- 多维指标对比（质量+成本+速度）
- 统计显著性在评估中的重要性
