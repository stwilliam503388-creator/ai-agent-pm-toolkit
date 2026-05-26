"""Tests for P4: Multi-Agent Writer - estimate_pipeline_cost function.

Note: The task/agent creation functions depend on CrewAI which is not installed,
so we only test the standalone estimate_pipeline_cost function.
"""
import os
import importlib.util

import pytest

# Only load the estimate_pipeline_cost function from tasks.py
# We need to mock crewai since it's not installed
import sys
from unittest.mock import MagicMock

# Mock crewai before importing tasks.py
sys.modules["crewai"] = MagicMock()

_spec = importlib.util.spec_from_file_location(
    "tasks",
    os.path.join(os.path.dirname(__file__), "..", "04-projects", "p4-multi-agent-writer", "tasks.py"),
)
tasks_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tasks_module)

estimate_pipeline_cost = tasks_module.estimate_pipeline_cost


class TestEstimatePipelineCost:
    def test_simple_complexity(self):
        result = estimate_pipeline_cost("simple")
        assert "per_agent" in result
        assert "total_pipeline" in result
        assert result["per_agent"]["input_tokens"] == 3000
        assert result["per_agent"]["output_tokens"] == 1500

    def test_medium_complexity(self):
        result = estimate_pipeline_cost("medium")
        assert result["per_agent"]["input_tokens"] == 5000
        assert result["per_agent"]["output_tokens"] == 2500

    def test_complex_complexity(self):
        result = estimate_pipeline_cost("complex")
        assert result["per_agent"]["input_tokens"] == 8000
        assert result["per_agent"]["output_tokens"] == 4000

    def test_unknown_complexity_defaults_to_medium(self):
        result = estimate_pipeline_cost("unknown")
        medium = estimate_pipeline_cost("medium")
        assert result == medium

    def test_default_is_medium(self):
        result = estimate_pipeline_cost()
        medium = estimate_pipeline_cost("medium")
        assert result == medium

    def test_total_pipeline_is_4x_per_agent(self):
        result = estimate_pipeline_cost("simple")
        assert result["total_pipeline"]["input_tokens"] == result["per_agent"]["input_tokens"] * 4
        assert result["total_pipeline"]["output_tokens"] == result["per_agent"]["output_tokens"] * 4

    def test_total_cost_is_4x_base_cost(self):
        result = estimate_pipeline_cost("medium")
        expected_cost = round(result["per_agent"]["total_cost"] * 4, 4)
        assert result["total_pipeline"]["estimated_cost"] == expected_cost

    def test_all_complexities_have_positive_costs(self):
        for complexity in ["simple", "medium", "complex"]:
            result = estimate_pipeline_cost(complexity)
            assert result["per_agent"]["total_cost"] > 0
            assert result["total_pipeline"]["estimated_cost"] > 0

    def test_cost_increases_with_complexity(self):
        simple = estimate_pipeline_cost("simple")
        medium = estimate_pipeline_cost("medium")
        complex_ = estimate_pipeline_cost("complex")
        assert simple["total_pipeline"]["estimated_cost"] < medium["total_pipeline"]["estimated_cost"]
        assert medium["total_pipeline"]["estimated_cost"] < complex_["total_pipeline"]["estimated_cost"]
