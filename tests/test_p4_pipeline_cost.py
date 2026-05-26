"""P4 Multi-Agent Writer 管线成本估算测试 — estimate_pipeline_cost() 函数验证。

被测对象
--------
04-projects/p4-multi-agent-writer/tasks.py
  - estimate_pipeline_cost(complexity) — 根据复杂度等级估算 4-agent 写作管线的 token 用量和费用

运行方式
--------
    # 运行全部 P4 测试
    pytest tests/test_p4_pipeline_cost.py -v

    # 测试某个具体复杂度
    pytest tests/test_p4_pipeline_cost.py::TestEstimatePipelineCost::test_simple_complexity -v

测试策略
--------
- tasks.py 依赖 CrewAI 库（未安装），因此在导入前用 MagicMock 替换 sys.modules["crewai"]
- 只测试不依赖 CrewAI 的独立函数 estimate_pipeline_cost()
- 覆盖三种复杂度等级：simple / medium / complex
- 验证未知复杂度回退到 medium 默认值
- 验证 total_pipeline 是 per_agent 的 4 倍（管线有 4 个 agent）
- 验证成本随复杂度单调递增

复杂度参数说明
--------------
- "simple"  → input_tokens=3000, output_tokens=1500
- "medium"  → input_tokens=5000, output_tokens=2500
- "complex" → input_tokens=8000, output_tokens=4000
- 其他值    → 默认使用 "medium" 配置

依赖
----
- pytest
- unittest.mock（用于 mock crewai）
"""
import os
import importlib.util

import pytest

# 源文件依赖 CrewAI 库（未安装），需要在导入前 mock
import sys
from unittest.mock import MagicMock

# 在导入 tasks.py 之前，将 crewai 模块替换为 MagicMock
sys.modules["crewai"] = MagicMock()

# 源文件名无连字符，但路径较深，同样使用 importlib 动态加载

_spec = importlib.util.spec_from_file_location(
    "tasks",
    os.path.join(os.path.dirname(__file__), "..", "04-projects", "p4-multi-agent-writer", "tasks.py"),
)
tasks_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tasks_module)

estimate_pipeline_cost = tasks_module.estimate_pipeline_cost


class TestEstimatePipelineCost:
    """estimate_pipeline_cost() 函数测试 — 验证三种复杂度的成本估算逻辑。

    测试覆盖：
    - 三种复杂度（simple/medium/complex）的 token 数量
    - 未知复杂度回退到 medium
    - 无参数调用默认使用 medium
    - total_pipeline = per_agent × 4（管线含 4 个 agent）
    - 成本随复杂度单调递增
    """

    def test_simple_complexity(self):
        """simple 复杂度：input_tokens=3000, output_tokens=1500。"""
        result = estimate_pipeline_cost("simple")
        assert "per_agent" in result
        assert "total_pipeline" in result
        assert result["per_agent"]["input_tokens"] == 3000
        assert result["per_agent"]["output_tokens"] == 1500

    def test_medium_complexity(self):
        """medium 复杂度：input_tokens=5000, output_tokens=2500。"""
        result = estimate_pipeline_cost("medium")
        assert result["per_agent"]["input_tokens"] == 5000
        assert result["per_agent"]["output_tokens"] == 2500

    def test_complex_complexity(self):
        """complex 复杂度：input_tokens=8000, output_tokens=4000。"""
        result = estimate_pipeline_cost("complex")
        assert result["per_agent"]["input_tokens"] == 8000
        assert result["per_agent"]["output_tokens"] == 4000

    def test_unknown_complexity_defaults_to_medium(self):
        """传入未知字符串（如 "unknown"）应回退到 medium 配置。"""
        result = estimate_pipeline_cost("unknown")
        medium = estimate_pipeline_cost("medium")
        assert result == medium

    def test_default_is_medium(self):
        """不传参数时默认使用 medium 配置。"""
        result = estimate_pipeline_cost()
        medium = estimate_pipeline_cost("medium")
        assert result == medium

    def test_total_pipeline_is_4x_per_agent(self):
        """total_pipeline 的 token 数应为 per_agent 的 4 倍。"""
        result = estimate_pipeline_cost("simple")
        assert result["total_pipeline"]["input_tokens"] == result["per_agent"]["input_tokens"] * 4
        assert result["total_pipeline"]["output_tokens"] == result["per_agent"]["output_tokens"] * 4

    def test_total_cost_is_4x_base_cost(self):
        """total_pipeline 的费用应为 per_agent 费用的 4 倍（四舍五入到 4 位小数）。"""
        result = estimate_pipeline_cost("medium")
        expected_cost = round(result["per_agent"]["total_cost"] * 4, 4)
        assert result["total_pipeline"]["estimated_cost"] == expected_cost

    def test_all_complexities_have_positive_costs(self):
        """所有复杂度等级的费用应为正数。"""
        for complexity in ["simple", "medium", "complex"]:
            result = estimate_pipeline_cost(complexity)
            assert result["per_agent"]["total_cost"] > 0
            assert result["total_pipeline"]["estimated_cost"] > 0

    def test_cost_increases_with_complexity(self):
        """费用应随复杂度递增：simple < medium < complex。"""
        simple = estimate_pipeline_cost("simple")
        medium = estimate_pipeline_cost("medium")
        complex_ = estimate_pipeline_cost("complex")
        assert simple["total_pipeline"]["estimated_cost"] < medium["total_pipeline"]["estimated_cost"]
        assert medium["total_pipeline"]["estimated_cost"] < complex_["total_pipeline"]["estimated_cost"]
