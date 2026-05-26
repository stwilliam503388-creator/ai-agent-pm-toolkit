"""Tests for P5: Agent Evaluation Comparison Runner."""
import json
import os
import tempfile
import importlib.util

import pytest

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
    def test_create_eval_result(self):
        r = EvalResult(task_id="t1", agent_group="g1", score=4.0, time_s=10.0, tokens=5000)
        assert r.task_id == "t1"
        assert r.score == 4.0
        assert r.output == ""
        assert r.notes == ""


class TestTaskDefinitions:
    def test_five_tasks_defined(self):
        assert len(TASKS) == 5

    def test_tasks_have_required_fields(self):
        for task_id, task in TASKS.items():
            assert "name" in task
            assert "difficulty" in task
            assert "prompt" in task
            assert "eval_rubric" in task

    def test_eval_rubric_weights_sum_to_one(self):
        for task_id, task in TASKS.items():
            total = sum(task["eval_rubric"].values())
            assert abs(total - 1.0) < 0.01, f"{task_id} rubric sums to {total}"

    def test_all_difficulties_valid(self):
        valid = {"easy", "medium", "hard", "very_hard"}
        for task in TASKS.values():
            assert task["difficulty"] in valid


class TestAgentGroups:
    def test_three_groups_defined(self):
        assert len(AGENT_GROUPS) == 3

    def test_groups_have_required_fields(self):
        for group_id, group in AGENT_GROUPS.items():
            assert "name" in group
            assert "description" in group
            assert "base_score" in group
            assert "base_time" in group
            assert "base_tokens" in group

    def test_base_scores_in_valid_range(self):
        for group in AGENT_GROUPS.values():
            assert 1.0 <= group["base_score"] <= 5.0


class TestSimulateEval:
    def test_returns_eval_result(self):
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert isinstance(result, EvalResult)

    def test_score_within_bounds(self):
        for task in TASKS.values():
            for group_id in AGENT_GROUPS:
                result = simulate_eval(task, group_id)
                assert 1.0 <= result.score <= 5.0

    def test_time_is_positive(self):
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert result.time_s > 0

    def test_tokens_is_positive(self):
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert result.tokens > 0

    def test_deterministic_with_same_seed(self):
        task = list(TASKS.values())[0]
        r1 = simulate_eval(task, "hermes_native")
        r2 = simulate_eval(task, "hermes_native")
        assert r1.score == r2.score

    def test_output_contains_task_and_group_names(self):
        task = list(TASKS.values())[0]
        result = simulate_eval(task, "hermes_native")
        assert task["name"] in result.output
        assert AGENT_GROUPS["hermes_native"]["name"] in result.output


class TestAnalyzeResults:
    @pytest.fixture
    def sample_results(self):
        """Generate one round of results for all tasks and groups."""
        round_results = []
        for task in TASKS.values():
            for group_id in AGENT_GROUPS:
                round_results.append(simulate_eval(task, group_id))
        return [round_results]

    def test_returns_dict_with_group_names(self, sample_results):
        analysis = analyze_results(sample_results)
        for group in AGENT_GROUPS.values():
            assert group["name"] in analysis

    def test_analysis_has_expected_metrics(self, sample_results):
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
        analysis = analyze_results(sample_results)
        for stats in analysis.values():
            assert stats["min_score"] <= stats["avg_score"] <= stats["max_score"]

    def test_total_experiments_correct(self, sample_results):
        analysis = analyze_results(sample_results)
        for stats in analysis.values():
            assert stats["total_experiments"] == len(TASKS)

    def test_multiple_rounds(self):
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
    @pytest.fixture
    def report_data(self):
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
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "# Agent Evaluation Comparison Report" in report

    def test_report_contains_group_comparison_table(self, report_data):
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Group Comparison" in report
        assert "Avg Score" in report

    def test_report_contains_key_findings(self, report_data):
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Key Findings" in report
        assert "Best quality" in report
        assert "Most efficient" in report

    def test_report_contains_product_insights(self, report_data):
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Product Insights" in report

    def test_report_contains_statistical_notes(self, report_data):
        analysis, rounds = report_data
        report = generate_report(analysis, rounds)
        assert "## Statistical Notes" in report


class TestSaveRawData:
    def test_saves_valid_json(self):
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
