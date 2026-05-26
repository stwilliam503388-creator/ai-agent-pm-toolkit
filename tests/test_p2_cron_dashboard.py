"""Tests for P2: Cron Health Dashboard."""
import os
import sys
import importlib.util

import pytest

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
    def test_high_rate_green(self):
        result = color_rate(0.99)
        assert GREEN in result
        assert "99%" in result

    def test_exact_threshold_95_green(self):
        result = color_rate(0.95)
        assert GREEN in result

    def test_medium_rate_yellow(self):
        result = color_rate(0.92)
        assert YELLOW in result

    def test_exact_threshold_90_yellow(self):
        result = color_rate(0.90)
        assert YELLOW in result

    def test_low_rate_red(self):
        result = color_rate(0.75)
        assert RED in result

    def test_zero_rate_red(self):
        result = color_rate(0.0)
        assert RED in result

    def test_perfect_rate_green(self):
        result = color_rate(1.0)
        assert GREEN in result

    def test_just_below_95_yellow(self):
        result = color_rate(0.949)
        assert YELLOW in result

    def test_just_below_90_red(self):
        result = color_rate(0.899)
        assert RED in result


class TestTrendIcon:
    def test_stable_trend(self):
        result = trend_icon(0.96)
        assert "stable" in result
        assert GREEN in result

    def test_watch_trend(self):
        result = trend_icon(0.90)
        assert "watch" in result
        assert YELLOW in result

    def test_degrade_trend(self):
        result = trend_icon(0.80)
        assert "degrade" in result
        assert RED in result

    def test_exact_threshold_95_stable(self):
        result = trend_icon(0.95)
        assert "stable" in result

    def test_exact_threshold_85_watch(self):
        result = trend_icon(0.85)
        assert "watch" in result

    def test_just_below_85_degrade(self):
        result = trend_icon(0.849)
        assert "degrade" in result


class TestFetchCronData:
    def test_returns_list(self):
        """Without hermes installed, should return mock data."""
        data = fetch_cron_data()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_mock_data_has_required_fields(self):
        data = fetch_cron_data()
        for job in data:
            assert "name" in job
            assert "last_status" in job
            assert "success_rate_7d" in job
            assert "avg_duration_s" in job
            assert "last_run_hours" in job

    def test_mock_data_rates_in_range(self):
        data = fetch_cron_data()
        for job in data:
            assert 0.0 <= job["success_rate_7d"] <= 1.0


class TestRenderDashboard:
    def test_renders_without_error(self):
        jobs = fetch_cron_data()
        dashboard = render_dashboard(jobs)
        assert isinstance(dashboard, str)
        assert len(dashboard) > 0

    def test_contains_header(self):
        jobs = fetch_cron_data()
        dashboard = render_dashboard(jobs)
        assert "Cron Health Dashboard" in dashboard

    def test_contains_job_names(self):
        jobs = [{"name": "TestJob", "last_status": "ok", "last_run_hours": 1.0, "avg_duration_s": 10, "success_rate_7d": 0.95}]
        dashboard = render_dashboard(jobs)
        assert "TestJob" in dashboard

    def test_contains_summary(self):
        jobs = fetch_cron_data()
        dashboard = render_dashboard(jobs)
        assert "Summary" in dashboard
        assert "jobs OK" in dashboard

    def test_single_job(self):
        jobs = [{"name": "Solo", "last_status": "ok", "last_run_hours": 0.5, "avg_duration_s": 5, "success_rate_7d": 1.0}]
        dashboard = render_dashboard(jobs)
        assert "1/1 jobs OK" in dashboard

    def test_failed_job_counted_correctly(self):
        jobs = [
            {"name": "Good", "last_status": "ok", "last_run_hours": 1, "avg_duration_s": 5, "success_rate_7d": 0.99},
            {"name": "Bad", "last_status": "fail", "last_run_hours": 10, "avg_duration_s": 5, "success_rate_7d": 0.5},
        ]
        dashboard = render_dashboard(jobs)
        assert "1/2 jobs OK" in dashboard

    def test_jobs_sorted_by_success_rate(self):
        jobs = [
            {"name": "HighRate", "last_status": "ok", "last_run_hours": 1, "avg_duration_s": 5, "success_rate_7d": 0.99},
            {"name": "LowRate", "last_status": "fail", "last_run_hours": 10, "avg_duration_s": 5, "success_rate_7d": 0.5},
        ]
        dashboard = render_dashboard(jobs)
        # LowRate should appear before HighRate (sorted ascending by rate)
        assert dashboard.index("LowRate") < dashboard.index("HighRate")
