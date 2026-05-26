# P3: Agent Security Test Suite

> 一句话：对Agent做4类Prompt注入红队测试。

## 项目信息

- **对应课程**：AI Agent PM 12周学习计划 Week 4
- **难度**：★★☆☆☆
- **代码量**：~80行（测试逻辑）
- **技术栈**：Python

## 功能

4类安全测试：
1. Prompt注入 — 篡改Agent指令
2. 工具滥用 — 让Agent调用危险工具
3. 角色扮演 — 绕过安全限制
4. 上下文泄露 — 窃取对话历史

## 快速开始

```bash
python agent-security-test-suite.py
```

## 面试故事

> 我对Agent做过系统性安全测试，发现并修复了3类漏洞。把测试集成到CI/CD，确保每次发布都通过安全检查。

## 学习收获

- Agent安全攻击面认知
- PM视角的安全需求定义
- 安全与体验的平衡设计
