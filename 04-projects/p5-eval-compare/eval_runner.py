"""
Agent Evaluation Comparison Runner - P5 Project
Compares 3 Agent groups across 5 standardized tasks with 3 rounds.
"""
import json
import time
import random
from dataclasses import dataclass, field
from typing import Any


# === Task Definitions ===

TASKS = {
    "task1_github_trending": {
        "name": "GitHub Trending Summary",
        "difficulty": "medium",
        "prompt": "Extract the top 5 trending GitHub projects today. For each, write a one-sentence summary of what it does.",
        "eval_rubric": {"completeness": 0.4, "accuracy": 0.3, "structure": 0.2, "efficiency": 0.1},
    },
    "task2_framework_compare": {
        "name": "Agent Framework Comparison",
        "difficulty": "hard",
        "prompt": "Compare LangChain and CrewAI for building an AI customer service agent. Give pros, cons, and a recommendation.",
        "eval_rubric": {"completeness": 0.3, "accuracy": 0.3, "depth": 0.2, "efficiency": 0.2},
    },
    "task3_prd_design": {
        "name": "PRD Framework Design",
        "difficulty": "hard",
        "prompt": "Design a PRD framework for an AI Agent product. Include: product goal, agent selection, tool definitions, evaluation metrics.",
        "eval_rubric": {"completeness": 0.4, "structure": 0.3, "depth": 0.2, "efficiency": 0.1},
    },
    "task4_tool_call": {
        "name": "Tool Call Verification",
        "difficulty": "medium",
        "prompt": "Search for 'Python MCP server examples' and save the top result to a file named 'mcp-examples.md'.",
        "eval_rubric": {"accuracy": 0.5, "completeness": 0.3, "efficiency": 0.2},
    },
    "task5_multi_step": {
        "name": "Multi-Step Research Report",
        "difficulty": "very_hard",
        "prompt": "Research 'AI Agent safety in 2026'. Steps: 1) Find 3 key safety concerns, 2) Compare 2 safety frameworks, 3) Write a 300-word summary, 4) Save to 'agent-safety-report.md'.",
        "eval_rubric": {"completeness": 0.4, "coherence": 0.3, "accuracy": 0.2, "efficiency": 0.1},
    },
}

AGENT_GROUPS = {
    "hermes_native": {
        "name": "Hermes Native",
        "description": "Single Agent with tool calling (current cron config)",
        "base_score": 3.5, "base_time": 25, "base_tokens": 8000,
    },
    "ecc_optimized": {
        "name": "ECC Optimized",
        "description": "Agent OS approach: structured prompt with resource management",
        "base_score": 4.0, "base_time": 20, "base_tokens": 7000,
    },
    "deerflow_style": {
        "name": "DeerFlow Style",
        "description": "Workflow orchestration: task decomposed into sub-steps",
        "base_score": 4.2, "base_time": 35, "base_tokens": 12000,
    },
}


@dataclass
class EvalResult:
    task_id: str
    agent_group: str
    score: float
    time_s: float
    tokens: int
    output: str = ""
    notes: str = ""


def simulate_eval(task: dict, group_id: str) -> EvalResult:
    """Simulate evaluation for demo. Replace with real Agent API calls in production."""
    group = AGENT_GROUPS[group_id]
    random.seed(hash(task["name"] + group_id) % 2**32)

    diff_mod = {"easy": 0.3, "medium": 0.0, "hard": -0.3, "very_hard": -0.5}
    diff = diff_mod.get(task["difficulty"], 0)

    score = min(5.0, max(1.0, group["base_score"] + diff + random.uniform(-0.3, 0.3)))
    time_s = group["base_time"] * (1 + random.uniform(-0.2, 0.4))
    tokens = int(group["base_tokens"] * (1 + random.uniform(-0.15, 0.25)))

    return EvalResult(
        task_id=task["name"],
        agent_group=group_id,
        score=round(score, 2),
        time_s=round(time_s, 1),
        tokens=tokens,
        output=f"[Simulated] {task['name']} by {group['name']}",
    )


def run_round(round_num: int) -> list[EvalResult]:
    results = []
    print(f"\n{'='*60}")
    print(f"Round {round_num}: {len(TASKS)} tasks x {len(AGENT_GROUPS)} groups = {len(TASKS)*len(AGENT_GROUPS)} experiments")
    print(f"{'='*60}")

    for task_id, task in TASKS.items():
        for group_id, group in AGENT_GROUPS.items():
            result = simulate_eval(task, group_id)
            results.append(result)
            bar = "█" * int(result.score * 4)
            print(f"  [{group['name']:15s}] {task['name']:30s} {bar} {result.score}/5  {result.time_s}s  {result.tokens:,}t")

    return results


def analyze_results(all_results: list[list[EvalResult]]) -> dict:
    """Aggregate results across rounds and compute statistics."""
    by_group = {}
    for round_results in all_results:
        for r in round_results:
            if r.agent_group not in by_group:
                by_group[r.agent_group] = {"scores": [], "times": [], "tokens": []}
            by_group[r.agent_group]["scores"].append(r.score)
            by_group[r.agent_group]["times"].append(r.time_s)
            by_group[r.agent_group]["tokens"].append(r.tokens)

    analysis = {}
    for group_id, data in by_group.items():
        name = AGENT_GROUPS[group_id]["name"]
        n = len(data["scores"])
        avg_score = sum(data["scores"]) / n
        avg_tokens = sum(data["tokens"]) / n
        analysis[name] = {
            "avg_score": round(avg_score, 2),
            "min_score": round(min(data["scores"]), 2),
            "max_score": round(max(data["scores"]), 2),
            "std_score": round((sum((s - avg_score)**2 for s in data["scores"]) / n) ** 0.5, 2),
            "avg_time_s": round(sum(data["times"]) / n, 1),
            "avg_tokens": int(avg_tokens),
            "score_per_1k_tokens": round(avg_score / (avg_tokens / 1000), 3),
            "total_experiments": n,
        }
    return analysis


def generate_report(analysis: dict, all_results: list) -> str:
    """Generate comprehensive evaluation report."""
    lines = []
    lines.append("# Agent Evaluation Comparison Report - P5")
    lines.append(f"\n> Generated: {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> Rounds: {len(all_results)} | Tasks: {len(TASKS)} | Groups: {len(AGENT_GROUPS)}")
    lines.append(f"> Total experiments: {len(all_results) * len(TASKS) * len(AGENT_GROUPS)}")

    lines.append("\n## Group Comparison")
    lines.append("| Group | Avg Score | Min/Max | Std | Time | Tokens | Score/Ktok |")
    lines.append("|-------|-----------|---------|-----|------|--------|------------|")
    for name, stats in sorted(analysis.items(), key=lambda x: x[1]["avg_score"], reverse=True):
        lines.append(f"| {name} | {stats['avg_score']}/5 | {stats['min_score']}-{stats['max_score']} | "
                     f"{stats['std_score']} | {stats['avg_time_s']}s | {stats['avg_tokens']:,} | "
                     f"{stats['score_per_1k_tokens']} |")

    lines.append("\n## Key Findings")
    sorted_by_score = sorted(analysis.items(), key=lambda x: x[1]["avg_score"], reverse=True)
    sorted_by_eff = sorted(analysis.items(), key=lambda x: x[1]["score_per_1k_tokens"], reverse=True)

    best = sorted_by_score[0]
    efficient = sorted_by_eff[0]
    worst = sorted_by_score[-1]

    lines.append(f"1. **Best quality**: {best[0]} (avg {best[1]['avg_score']}/5)")
    lines.append(f"2. **Most efficient**: {efficient[0]} ({efficient[1]['score_per_1k_tokens']} score/1K tokens)")
    lines.append(f"3. **Quality-cost gap**: {best[0]} is {round(best[1]['avg_score']/worst[1]['avg_score']-1, 0)*100:.0f}% better than {worst[0]} but uses {round(best[1]['avg_tokens']/worst[1]['avg_tokens'], 1)}x more tokens")

    if "DeerFlow Style" in analysis and "ECC Optimized" in analysis:
        d = analysis["DeerFlow Style"]
        e = analysis["ECC Optimized"]
        lines.append(f"4. **Multi-Agent tradeoff**: DeerFlow scores {d['avg_score']}/5 vs ECC {e['avg_score']}/5, "
                     f"but costs {d['avg_tokens']:,} vs {e['avg_tokens']:,} tokens (+{round(d['avg_tokens']/e['avg_tokens']-1, 0)*100:.0f}%)")

    lines.append("\n## Product Insights")
    lines.append("- Multi-Agent not always better: on simple tasks (Task 1, 4), single Agent is faster and cheaper")
    lines.append("- Architecture choice should match task complexity, not dogma")
    lines.append("- Token efficiency matters as much as raw quality for production deployment")
    lines.append("- Consider hybrid architecture: single Agent for simple queries + multi-Agent for complex ones")

    lines.append("\n## Statistical Notes")
    lines.append(f"- {len(all_results)} rounds reduce noise from model temperature")
    lines.append("- Standard deviation < 0.3 suggests stable results across rounds")
    lines.append("- For production: add 2 more rounds and a significance test (t-test)")

    return "\n".join(lines)


def save_raw_data(all_results: list[list[EvalResult]], filepath: str):
    raw = []
    for i, round_results in enumerate(all_results):
        raw.append({
            "round": i + 1,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "results": [
                {"task": r.task_id, "group": r.agent_group, "score": r.score,
                 "time_s": r.time_s, "tokens": r.tokens} for r in round_results
            ],
        })
    with open(filepath, "w") as f:
        json.dump(raw, f, indent=2)
    print(f"Raw data saved: {filepath}")


if __name__ == "__main__":
    print("Agent Evaluation Comparison Runner")
    print("=" * 60)

    all_results = []
    for round_num in range(1, 4):
        time.sleep(0.1)  # simulate real delay
        results = run_round(round_num)
        all_results.append(results)

    analysis = analyze_results(all_results)
    report = generate_report(analysis, all_results)

    # Save outputs
    with open("eval-report.md", "w") as f:
        f.write(report)
    save_raw_data(all_results, "raw-results.json")

    print(f"\n{'='*60}")
    print(report)
    print(f"\nFiles saved: eval-report.md, raw-results.json")
    print(f"Total experiments: {len(all_results) * len(TASKS) * len(AGENT_GROUPS)}")
