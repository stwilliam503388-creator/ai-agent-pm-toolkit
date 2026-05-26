"""P5 Agent Evaluation Comparison Runner 测试 — 多 Agent 评估对比框架验证。

被测对象
--------
04-projects/p5-eval-compare/eval_runner.py
  - EvalResult          — 评估结果数据类（task_id, agent_group, score, time_s, tokens, output, notes）
  - TASKS               — 预定义的 5 个评估任务（含难度和评分权重）
  - AGENT_GROUPS        — 预定义的 3 个 agent 分组配置（含基础性能参数）
  - simulate_eval()     — 模拟单次评估，返回 EvalResult
  - analyze_results()   — 对多轮评估结果做统计分析（均值、极值、标准差等）
  - generate_report()   — 生成 Markdown 格式的对比报告
  - save_raw_data()     — 将原始评估数据保存为 JSON 文件

运行方式
--------
    # 运行全部 P5 测试
    pytest tests/test_p5_eval_runner.py -v

    # 只测试模拟评估逻辑
    pytest tests/test_p5_eval_runner.py::TestSimulateEval -v

    # 只测试统计分析
    pytest tests/test_p5_eval_runner.py::TestAnalyzeResults -v

测试策略
--------
- 数据类测试：验证 EvalResult 字段赋值和默认值（output/notes 默认为空字符串）
- 任务定义测试：验证任务数量、字段完整性、评分权重之和为 1.0、难度值合法
- Agent 分组测试：验证分组数量、字段完整性、基础分数在 [1.0, 5.0] 范围内
- simulate_eval 测试：验证返回类型、分数边界、时间/token 为正、确定性（相同输入相同输出）
- analyze_results 测试：验证统计指标存在性、min ≤ avg ≤ max 不变式、实验计数正确性
- generate_report 测试：验证报告中包含标题、对比表格、关键发现、产品洞察、统计说明
- save_raw_data 测试：验证 JSON 文件的可解析性、字段完整性（使用 tempfile 避免污染文件系统）

依赖
----
- pytest
- json, tempfile（标准库）
"""
import json
import os
import tempfile
import importlib.util

import pytest

# 源文件名无连字符，使用 importlib 动态加载
_spec = importlib.util.spec_from_file_location(
    "eval_runner",
    os.path.join(os.path.dirname(__file__), "..", "04-projects", "p5-eval-compare", "eval_runner.py"),
)
eval_runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eval_runner)

EvalResult = eval_runner.EvalResult
simulate_eval = eval_runner.simulate_eval
analyze_results = eval_runner.analyze_results
generate_report = eval_runner.generate_report
save_raw_data = eval_runner.save_raw_data
TASKS = eval_runner.TASKS
AGENT_GROUPS = eval_runner.AGENT_GROUPS


class TestEvalResultDataclass:
    """EvalResult 数据类测试 — 验证评估结果对象的创建和默认值。"""

    def test_create_eval_result(self):
        """创建 EvalResult 实例，验证字段赋值和 output/notes 默认为空字符串。"""
        r = EvalResult(task_id="t1", agent_group="g1", score=4.0, time_s=10.0, tokens=5000)
        assert r.task_id == "t1"
        assert r.score == 4.0
        assert r.output == ""
        assert r.notes == ""


class TestTaskDefinitions:
    """TASKS 任务定义测试 — 验证预定义评估任务的完整性和一致性。"""

    def test_five_tasks_defined(self):
        """应定义 5 个评估任务。"""
        assert len(TASKS) == 5

    def test_tasks_have_required_fields(self):
        """每个任务应包含 name、difficulty、prompt、eval_rubric 字段。"""
        for task_id, task in TASKS.items():
            assert "name" in task
            assert "difficulty" in task
            assert "prompt" in task
            assert "eval_rubric" in task

    def test_eval_rubric_weights_sum_to_one(self):
        """每个任务的 eval_rubric 权重之和应为 1.0（允许 0.01 误差）。"""
        for task_id, task in TASKS.items():
            total = sum(task["eval_rubric"].values())
            assert abs(total - 1.0) < 0.01, f"{task_id} rubric sums to {total}"

    def test_all_difficulties_valid(self):
        """任务难度应为 easy / medium / hard / very_hard 之一。"""
        valid = {"easy", "medium", "hard", "very_hard"}
        for task in TASKS.values():
            assert task["difficulty"] in valid


class TestAgentGroups:
    """AGENT_GROUPS 分组定义测试 — 验证 agent 分组配置的完整性。"""

    def test_three_groups_defined(self):
        """应定义 3 个 agent 分组。"""
        assert len(AGENT_GROUPS) == 3

    def test_groups_have_required_fields(self):
        """每个分组应包含 name、description、base_score、base_time、base_tokens 字段。"""
        for group_id, group in AGENT_GROUPS.items():
            assert "name" in group
            assert "description" in group
            assert "base_score" in group
            assert "base_time" in group
            assert "base_tokens" in group

    def test_base_scores_in_valid_range(self):
        """分组的 base_score 应在 [1.0, 5.0] 范围内。"""
        for group in AGENT_GROUPS.values():
            assert 1.0 <= group["base_score"] <= 5.0


class TestSimulateEval:
    """simulate_eval() 测试 — 验证单次评估模拟的返回值和约束条件。"""

    def test_returns_eval_result(self):
        """返回值应为 EvalResult 实例。"""
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert isinstance(result, EvalResult)

    def test_score_within_bounds(self):
        """所有任务 × 所有分组的评分应在 [1.0, 5.0] 范围内。"""
        for task in TASKS.values():
            for group_id in AGENT_GROUPS:
                result = simulate_eval(task, group_id)
                assert 1.0 <= result.score <= 5.0

    def test_time_is_positive(self):
        """评估耗时应为正数。"""
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert result.time_s > 0

    def test_tokens_is_positive(self):
        """token 消耗应为正数。"""
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert result.tokens > 0

    def test_deterministic_with_same_seed(self):
        """相同输入应产生相同输出（确定性模拟）。"""
        task = list(TASKS.values())[0]
        r1 = simulate_eval(task, "hermes_native")
        r2 = simulate_eval(task, "hermes_native")
        assert r1.score == r2.score

    def test_output_contains_task_and_group_names(self):
        """输出文本应包含任务名和分组名。"""
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert task["name"] in result.output
        assert AGENT_GROUPS["hermes_native"]["name"] in result.output


class TestAnalyzeResults:
    """analyze_results() 测试 — 验证多轮评估结果的统计分析逻辑。"""

    @pytest.fixture
    def sample_results(self):
        """生成一轮完整评估结果（所有任务 × 所有分组）。"""
        round_results = []
        for task in TASKS.values():
            for group_id in AGENT_GROUPS:
                round_results.append(simulate_eval(task, group_id))
        return [round_results]

    def test_returns_dict_with_group_names(self, sample_results):
        """分析结果应包含所有 agent 分组名作为键。"""
        analysis = analyze_results(sample_results)
        for group in AGENT_GROUPS.values():
            assert group["name"] in analysis

    def test_analysis_has_expected_metrics(self, sample_results):
        """每个分组应包含 avg_score、min/max_score、std_score、avg_time_s、avg_tokens 等指标。"""
        analysis = analyze_results(sample_results)
        for name, stats in analysis.items():
            assert "avg_score" in stats
            assert "min_score" in stats
            assert "max_score" in stats
            assert "std_score" in stats
            assert "avg_time_s" in stats
            assert "avg_tokens" in stats
            assert "score_per_1k_tokens" in stats
            assert "total_experiments" in stats

    def test_min_lte_avg_lte_max(self, sample_results):
        """min_score ≤ avg_score ≤ max_score 不变式应始终成立。"""
        analysis = analyze_results(sample_results)
        for stats in analysis.values():
            assert stats["min_score"] <= stats["avg_score"] <= stats["max_score"]

    def test_total_experiments_correct(self, sample_results):
        """实验总数应等于任务数量。"""
        analysis = analyze_results(sample_results)
        for stats in analysis.values():
            assert stats["total_experiments"] == len(TASKS)

    def test_multiple_rounds(self):
        """多轮评估时，实验总数应等于任务数 × 轮数。"""
        rounds = []
        for _ in range(3):
            round_results = []
            for task in TASKS.values():
                for group_id in AGENT_GROUPS:
                    round_results.append(simulate_eval(task, group_id))
            rounds.append(round_results)
        analysis = analyze_results(rounds)
        for stats in analysis.values():
            assert stats["total_experiments"] == len(TASKS) * 3


class TestGenerateReport:
    """generate_report() 测试 — 验证评估对比报告的 Markdown 格式和内容。"""

    @pytest.fixture
    def report_data(self):
        """生成 2 轮评估数据及其分析结果。"""
        rounds = []
        for _ in range(2):
            round_results = []
            for task in TASKS.values():
                for group_id in AGENT_GROUPS:
                    round_results.append(simulate_eval(task, group_id))
            rounds.append(round_results)
        analysis = analyze_results(rounds)
        return analysis, rounds

    def test_report_contains_header(self, report_data):
        """报告应包含 "# Agent Evaluation Comparison Report" 标题。"""
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "# Agent Evaluation Comparison Report" in report

    def test_report_contains_group_comparison_table(self, report_data):
        """报告应包含 "## Group Comparison" 分组对比表。"""
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Group Comparison" in report
        assert "Avg Score" in report

    def test_report_contains_key_findings(self, report_data):
        """报告应包含 "## Key Findings" 关键发现，含最佳质量和最高效分组。"""
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Key Findings" in report
        assert "Best quality" in report
        assert "Most efficient" in report

    def test_report_contains_product_insights(self, report_data):
        """报告应包含 "## Product Insights" 产品洞察。"""
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Product Insights" in report

    def test_report_contains_statistical_notes(self, report_data):
        """报告应包含 "## Statistical Notes" 统计说明。"""
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Statistical Notes" in report


class TestSaveRawData:
    """save_raw_data() 测试 — 验证原始评估数据的 JSON 持久化。"""

    def test_saves_valid_json(self):
        """保存的文件应为合法 JSON，包含正确的轮次和结果数量。"""
        results = []
        for task in TASKS.values():
            for group_id in AGENT_GROUPS:
                results.append(simulate_eval(task, group_id))
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            save_raw_data([results], filepath)
            with open(filepath) as f:
                data = json.load(f)
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["round"] == 1
            assert len(data[0]["results"]) == len(TASKS) * len(AGENT_GROUPS)
        finally:
            os.unlink(filepath)

    def test_results_have_expected_fields(self):
        """JSON 中每条结果应包含 task、group、score、time_s、tokens 字段。"""
        results = [simulate_eval(list(TASKS.values())[0], "hermes_native")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name
        try:
            save_raw_data([results], filepath)
            with open(filepath) as f:
                data = json.load(f)
            entry = data[0]["results"][0]
            assert "task" in entry
            assert "group" in entry
            assert "score" in entry
            assert "time_s" in entry
            assert "tokens" in entry
        finally:
            os.unlink(filepath)
