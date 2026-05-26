"""P2 Cron Health Dashboard 测试 — 终端仪表盘的渲染与数据逻辑验证。

被测对象
--------
04-projects/p2-cron-dashboard/cron-dashboard.py
  - color_rate(rate)    — 按成功率返回带 ANSI 颜色的百分比字符串
  - trend_icon(rate)    — 按成功率返回趋势图标（稳定 / 观察 / 降级）
  - fetch_cron_data()   — 获取 cron 任务状态（无 hermes 时返回 mock 数据）
  - render_dashboard()  — 生成完整的终端仪表盘字符串

运行方式
--------
    # 运行全部 P2 测试
    pytest tests/test_p2_cron_dashboard.py -v

    # 只测试颜色阈值逻辑
    pytest tests/test_p2_cron_dashboard.py::TestColorRate -v

测试策略
--------
- color_rate 和 trend_icon 是纯函数，直接传入边界值验证输出中的 ANSI 颜色码
- fetch_cron_data 在无 hermes CLI 的环境下会自动返回 mock 数据，测试验证 mock 数据结构
- render_dashboard 测试验证输出字符串中包含表头、任务名、摘要等关键内容

ANSI 颜色阈值说明
-----------------
- ≥ 0.95 → 绿色 (GREEN)
- ≥ 0.90 → 黄色 (YELLOW)
- < 0.90 → 红色 (RED)

趋势阈值说明
-----------
- ≥ 0.95 → ↗ stable（稳定）
- ≥ 0.85 → → watch（观察）
- < 0.85 → ↘ degrade（降级）

依赖
----
- pytest
"""
import os
import sys
import importlib.util

import pytest

# 源文件名含连字符，使用 importlib 动态加载
_spec = importlib.util.spec_from_file_location(
    "cron_dashboard",
    os.path.join(os.path.dirname(__file__), "..", "04-projects", "p2-cron-dashboard", "cron-dashboard.py"),
)
cron_dashboard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cron_dashboard)

color_rate = cron_dashboard.color_rate
trend_icon = cron_dashboard.trend_icon
render_dashboard = cron_dashboard.render_dashboard
fetch_cron_data = cron_dashboard.fetch_cron_data
GREEN = cron_dashboard.GREEN
YELLOW = cron_dashboard.YELLOW
RED = cron_dashboard.RED
RESET = cron_dashboard.RESET


class TestColorRate:
    """color_rate() 函数测试 — 验证成功率 → ANSI 颜色映射的边界行为。

    关键边界值：0.95（绿黄分界）、0.90（黄红分界）
    测试覆盖：精确阈值、略低于阈值、极端值（0.0 和 1.0）
    """

    def test_high_rate_green(self):
        """0.99 应渲染为绿色，显示 "99%"。"""
        result = color_rate(0.99)
        assert GREEN in result
        assert "99%" in result

    def test_exact_threshold_95_green(self):
        """0.95 正好是绿色阈值，应为绿色。"""
        result = color_rate(0.95)
        assert GREEN in result

    def test_medium_rate_yellow(self):
        """0.92 处于 [0.90, 0.95) 区间，应为黄色。"""
        result = color_rate(0.92)
        assert YELLOW in result

    def test_exact_threshold_90_yellow(self):
        """0.90 正好是黄色阈值，应为黄色。"""
        result = color_rate(0.90)
        assert YELLOW in result

    def test_low_rate_red(self):
        """0.75 低于 0.90，应为红色。"""
        result = color_rate(0.75)
        assert RED in result

    def test_zero_rate_red(self):
        """0.0 应为红色。"""
        result = color_rate(0.0)
        assert RED in result

    def test_perfect_rate_green(self):
        """1.0（100% 成功率）应为绿色。"""
        result = color_rate(1.0)
        assert GREEN in result

    def test_just_below_95_yellow(self):
        """0.949 略低于 0.95 阈值，应为黄色而非绿色。"""
        result = color_rate(0.949)
        assert YELLOW in result

    def test_just_below_90_red(self):
        """0.899 略低于 0.90 阈值，应为红色而非黄色。"""
        result = color_rate(0.899)
        assert RED in result


class TestTrendIcon:
    """trend_icon() 函数测试 — 验证成功率 → 趋势图标映射。

    阈值：0.95（稳定/观察分界）、0.85（观察/降级分界）
    """

    def test_stable_trend(self):
        """0.96 ≥ 0.95 应显示 "stable"（↗ 稳定）并使用绿色。"""
        result = trend_icon(0.96)
        assert "stable" in result
        assert GREEN in result

    def test_watch_trend(self):
        """0.90 处于 [0.85, 0.95) 区间，应显示 "watch"（→ 观察）并使用黄色。"""
        result = trend_icon(0.90)
        assert "watch" in result
        assert YELLOW in result

    def test_degrade_trend(self):
        """0.80 < 0.85 应显示 "degrade"（↘ 降级）并使用红色。"""
        result = trend_icon(0.80)
        assert "degrade" in result
        assert RED in result

    def test_exact_threshold_95_stable(self):
        """0.95 正好是稳定阈值。"""
        result = trend_icon(0.95)
        assert "stable" in result

    def test_exact_threshold_85_watch(self):
        """0.85 正好是观察阈值。"""
        result = trend_icon(0.85)
        assert "watch" in result

    def test_just_below_85_degrade(self):
        """0.849 略低于 0.85，应为降级。"""
        result = trend_icon(0.849)
        assert "degrade" in result


class TestFetchCronData:
    """fetch_cron_data() 函数测试 — 验证 mock 数据的结构与取值范围。

    当测试环境未安装 hermes CLI 时，fetch_cron_data() 会自动返回内置的 mock 数据。
    这组测试验证 mock 数据的字段完整性和数值合理性。
    """

    def test_returns_list(self):
        """返回值应为非空列表。"""
        data = fetch_cron_data()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_mock_data_has_required_fields(self):
        """每条 cron 任务记录应包含 name、last_status、success_rate_7d、avg_duration_s、last_run_hours。"""
        data = fetch_cron_data()
        for job in data:
            assert "name" in job
            assert "last_status" in job
            assert "success_rate_7d" in job
            assert "avg_duration_s" in job
            assert "last_run_hours" in job

    def test_mock_data_rates_in_range(self):
        """所有任务的 7 天成功率应在 [0.0, 1.0] 范围内。"""
        data = fetch_cron_data()
        for job in data:
            assert 0.0 <= job["success_rate_7d"] <= 1.0


class TestRenderDashboard:
    """render_dashboard() 函数测试 — 验证终端仪表盘输出内容的正确性。

    测试覆盖：
    - 基本渲染（无异常、非空输出）
    - 表头 "Cron Health Dashboard" 存在
    - 任务名显示
    - 摘要行格式（"X/Y jobs OK"）
    - 失败任务计数正确
    - 按成功率升序排列（最差的排在最前）
    """

    def test_renders_without_error(self):
        """使用 mock 数据渲染应返回非空字符串，不抛出异常。"""
        jobs = fetch_cron_data()
        dashboard = render_dashboard(jobs)
        assert isinstance(dashboard, str)
        assert len(dashboard) > 0

    def test_contains_header(self):
        """输出应包含 "Cron Health Dashboard" 标题。"""
        jobs = fetch_cron_data()
        dashboard = render_dashboard(jobs)
        assert "Cron Health Dashboard" in dashboard

    def test_contains_job_names(self):
        """输出应包含传入的任务名。"""
        jobs = [{"name": "TestJob", "last_status": "ok", "last_run_hours": 1.0, "avg_duration_s": 10, "success_rate_7d": 0.95}]
        dashboard = render_dashboard(jobs)
        assert "TestJob" in dashboard

    def test_contains_summary(self):
        """输出应包含摘要行，含 "Summary" 和 "jobs OK" 字样。"""
        jobs = fetch_cron_data()
        dashboard = render_dashboard(jobs)
        assert "Summary" in dashboard
        assert "jobs OK" in dashboard

    def test_single_job(self):
        """单个成功任务应显示 "1/1 jobs OK"。"""
        jobs = [{"name": "Solo", "last_status": "ok", "last_run_hours": 0.5, "avg_duration_s": 5, "success_rate_7d": 1.0}]
        dashboard = render_dashboard(jobs)
        assert "1/1 jobs OK" in dashboard

    def test_failed_job_counted_correctly(self):
        """2 个任务中 1 个失败，摘要应显示 "1/2 jobs OK"。"""
        jobs = [
            {"name": "Good", "last_status": "ok", "last_run_hours": 1, "avg_duration_s": 5, "success_rate_7d": 0.99},
            {"name": "Bad", "last_status": "fail", "last_run_hours": 10, "avg_duration_s": 5, "success_rate_7d": 0.5},
        ]
        dashboard = render_dashboard(jobs)
        assert "1/2 jobs OK" in dashboard

    def test_jobs_sorted_by_success_rate(self):
        """任务应按成功率升序排列，成功率低的排在前面。"""
        jobs = [
            {"name": "HighRate", "last_status": "ok", "last_run_hours": 1, "avg_duration_s": 5, "success_rate_7d": 0.99},
            {"name": "LowRate", "last_status": "fail", "last_run_hours": 10, "avg_duration_s": 5, "success_rate_7d": 0.5},
        ]
        dashboard = render_dashboard(jobs)
        # LowRate（低成功率）应排在 HighRate（高成功率）之前
        assert dashboard.index("LowRate") < dashboard.index("HighRate")
