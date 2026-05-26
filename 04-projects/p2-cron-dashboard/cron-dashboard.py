"""
Cron Health Dashboard - P2 Project
Parses midnight-check data and generates terminal dashboard.
"""
import json
import subprocess
import sys
from datetime import datetime
from collections import defaultdict


# ANSI color codes
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"


def fetch_cron_data() -> list[dict]:
    """Fetch cron job status via hermes cronjob list (or mock for testing)."""
    try:
        result = subprocess.run(
            ["hermes", "cronjob", "list", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout).get("jobs", [])
    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        pass

    # Mock data for demo
    return [
        {"name": "GitHub Trending", "last_status": "ok", "last_run_hours": 2.1, "avg_duration_s": 23, "success_rate_7d": 0.96},
        {"name": "AI Interview Daily", "last_status": "ok", "last_run_hours": 5.5, "avg_duration_s": 41, "success_rate_7d": 0.88},
        {"name": "Morning Briefing", "last_status": "ok", "last_run_hours": 1.2, "avg_duration_s": 35, "success_rate_7d": 0.94},
        {"name": "Evening Briefing", "last_status": "ok", "last_run_hours": 3.0, "avg_duration_s": 32, "success_rate_7d": 0.91},
        {"name": "Concept Extract", "last_status": "ok", "last_run_hours": 0.5, "avg_duration_s": 15, "success_rate_7d": 0.99},
        {"name": "Config Backup", "last_status": "fail", "last_run_hours": 12.0, "avg_duration_s": 5, "success_rate_7d": 0.75},
        {"name": "Orphan Checker", "last_status": "ok", "last_run_hours": 4.0, "avg_duration_s": 18, "success_rate_7d": 0.93},
    ]


def color_rate(rate: float) -> str:
    if rate >= 0.95:
        return f"{GREEN}{rate:.0%}{RESET}"
    elif rate >= 0.90:
        return f"{YELLOW}{rate:.0%}{RESET}"
    return f"{RED}{rate:.0%}{RESET}"


def trend_icon(rate: float) -> str:
    if rate >= 0.95:
        return f"{GREEN}↗ stable{RESET}"
    elif rate >= 0.85:
        return f"{YELLOW}→ watch{RESET}"
    return f"{RED}↘ degrade{RESET}"


def render_dashboard(jobs: list[dict]) -> str:
    lines = []
    lines.append(f"{BOLD}┌{'='*68}┐{RESET}")
    lines.append(f"{BOLD}│{' Cron Health Dashboard':<58}{datetime.now().strftime('%H:%M'):>10} │{RESET}")
    lines.append(f"{BOLD}├{'='*68}┤{RESET}")
    lines.append(f"{BOLD}│ {'Task':<24} {'Success':<8} {'Time':<7} {'Lag':<7} {'Trend':<16} │{RESET}")
    lines.append(f"{BOLD}│{'-'*24} {'-'*8} {'-'*7} {'-'*7} {'-'*16} │{RESET}")

    ok_count = 0
    for job in sorted(jobs, key=lambda j: j["success_rate_7d"]):
        name = job["name"][:23]
        rate = color_rate(job["success_rate_7d"])
        dur = f"{job['avg_duration_s']}s"
        lag = f"{job['last_run_hours']:.1f}h"
        trend = trend_icon(job["success_rate_7d"])
        lines.append(f"│ {name:<24} {rate:<24} {dur:<7} {lag:<7} {trend:<30} │")

        if job["last_status"] == "ok":
            ok_count += 1

    lines.append(f"{BOLD}├{'='*68}┤{RESET}")
    lines.append(f"{BOLD}│ Summary: {ok_count}/{len(jobs)} jobs OK | "
                 f"Overall health: {color_rate(ok_count / len(jobs))}{' '*(27-len(str(ok_count))-len(str(len(jobs))))}{BOLD}│{RESET}")
    lines.append(f"{BOLD}└{'='*68}┘{RESET}")

    return "\n".join(lines)


if __name__ == "__main__":
    jobs = fetch_cron_data()
    dashboard = render_dashboard(jobs)
    print(dashboard)

    # Optionally write to file
    if "--save" in sys.argv:
        output = "/tmp/cron-dashboard-output.md"
        with open(output, "w") as f:
            f.write(f"```\n{dashboard}\n```\n")
        print(f"\nDashboard saved to {output}")
