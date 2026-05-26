# P6: Video Knowledge Pipeline

一句话：B站视频 -> 音频 -> 转写 -> 摘要 -> Obsidian 的全自动知识管道。

## 项目信息

- **对应课程**：AI Agent PM 12周学习计划 Week 2-8（贯穿项目）
- **难度**：★★★☆☆
- **代码量**：~50行Shell
- **技术栈**：Shell, yt-dlp, Whisper, Python

## 管道流程

```
B站视频链接
  -> yt-dlp 下载音频
  -> Whisper 转写文字
  -> LLM 提炼摘要+提取概念
  -> 自动写入Obsidian+更新索引
```

## 快速开始

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh "https://www.bilibili.com/video/BVxxxxxx"
```

## 前置依赖

```bash
brew install yt-dlp ffmpeg
pip install openai-whisper
```

## 面试故事

我搭建了一个从视频链接到结构化笔记的全自动管道。B站视频 -> 音频下载 -> Whisper转写 -> LLM摘要 -> Obsidian归档，一条命令跑完全链路。这是多模态Agent的端到端实践。

## 学习收获

- 多模态数据处理管道设计
- 工具链集成（yt-dlp + Whisper + LLM）
- 自动化知识管理思维
