# Day 47 — 跑第一轮评估 - 记录原始数据

## 今日目标

3个Agent各跑一次5个任务，记录原始输出和指标。

---

## 核心概念

## 1. 执行流程

对每个任务：
1. 组A跑一次->记录输出+耗时+Token
2. 组B跑一次->同上
3. 组C跑一次->同上

## 2. 数据记录格式

创建 raw-results-round-1.json：
```json
{
  "round": 1,
  "tasks": [
    {
      "id": "task1",
      "results": {
        "hermes": {"output": "...", "time_s": 23, "tokens": 8500, "score": 3.5},
        "ecc": {"output": "...", "time_s": 18, "tokens": 7200, "score": 4.0},
        "deerflow": {"output": "...", "time_s": 35, "tokens": 12000, "score": 4.2}
      }
    }
  ]
}
```

---

## 今日产出

- [ ] 跑完第一轮所有15组实验
- [ ] 记录原始数据到 raw-results-round-1.json
- [ ] 初步观察各组的差异

---

## 面试要点

数据不会说谎。评估实验的结果是你面试时最硬的论据。
