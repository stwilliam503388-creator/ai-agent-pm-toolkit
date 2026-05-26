"""Task definitions for Multi-Agent Writing System - P4.

Each task defines what an agent should produce, the expected output format,
and quality criteria for downstream coordination.
"""
from crewai import Task


def create_research_task(topic: str, researcher) -> Task:
    """Task 1: Research the topic and produce a structured brief."""
    return Task(
        description=(
            f"Research the topic: '{topic}'. Follow this structure:\n"
            "1) **Key Facts** (5-7 verified facts with sources)\n"
            "2) **Current Trends** (3-4 emerging patterns, note confidence: high/medium/low)\n"
            "3) **Expert Opinions** (2-3 notable viewpoints, attribute to specific experts)\n"
            "4) **Data Points** (3-5 quantitative data points with year and source)\n"
            "5) **Contrarian View** (1 respected dissenting opinion, if any)\n\n"
            "Constraints:\n"
            "- Every claim must be sourced or marked [NEEDS VERIFICATION]\n"
            "- Distinguish established facts from opinions explicitly\n"
            "- Target length: 500-800 words\n"
            "- If sources conflict, note the disagreement rather than picking sides"
        ),
        expected_output=(
            "A structured research brief with 5 sections as specified above. "
            "500-800 words. All claims sourced or flagged."
        ),
        agent=researcher,
    )


def create_writing_task(topic: str, writer) -> Task:
    """Task 2: Write the first draft based on research brief."""
    return Task(
        description=(
            f"Write a 1000-1500 word article on '{topic}' based on the research brief.\n\n"
            "Structure:\n"
            "- **Compelling headline** (under 15 words, promise a specific insight)\n"
            "- **Hook** (first 50 words: open with a surprising fact or provocative question)\n"
            "- **3-4 body sections** with clear subheadings\n"
            "- **Conclusion** with 3 actionable takeaways for PMs\n\n"
            "Style rules:\n"
            "- Lead with the most interesting insight, not background\n"
            "- One idea per paragraph\n"
            "- Replace jargon with plain language whenever possible\n"
            "- Use concrete examples, not abstract descriptions\n"
            "- Bold key phrases for scanning readers\n\n"
            "Target audience: Product managers interested in AI Agent technology.\n"
            "Tone: Professional but conversational. Write like Ben Thompson "
            "(Stratechery) meets a really good product review."
        ),
        expected_output=(
            "A complete first draft article, 1000-1500 words, "
            "with headline, hook, 3-4 body sections, and conclusion. "
            "Ready for editorial review."
        ),
        agent=writer,
    )


def create_review_task(reviewer) -> Task:
    """Task 3: Review the draft for accuracy and quality."""
    return Task(
        description=(
            "Review the article draft thoroughly. Check for:\n\n"
            "1) **Factual Accuracy**\n"
            "   - Verify every number, statistic, and date\n"
            "   - Check that product names and company attributions are correct\n"
            "   - Flag any unsupported claim as [NEEDS CITATION]\n\n"
            "2) **Logical Flow**\n"
            "   - Does each section follow naturally from the previous?\n"
            "   - Are there any logical leaps without explanation?\n\n"
            "3) **Tone Consistency**\n"
            "   - Professional but conversational throughout?\n"
            "   - Any sections that sound academic or marketing-heavy?\n\n"
            "4) **Grammar & Style**\n"
            "   - Typos, grammar errors, awkward phrasing\n"
            "   - Overused words or phrases\n\n"
            "Output format:\n"
            "```\n"
            "## Issues Found\n"
            "### Critical (must fix before publish)\n"
            "- [Location] Issue description | Suggested fix\n\n"
            "### Minor (nice to fix)\n"
            "- [Location] Issue description | Suggested fix\n\n"
            "## Overall Assessment\n"
            "Publish ready? [YES / NO / WITH FIXES]\n"
            "Strongest section: [name]\n"
            "Weakest section: [name]\n"
            "```"
        ),
        expected_output=(
            "A structured review with categorized issues (Critical/Minor), "
            "suggested fixes for each, and an overall publish-readiness assessment."
        ),
        agent=reviewer,
    )


def create_final_task(coordinator) -> Task:
    """Task 4: Incorporate feedback and produce the final piece."""
    return Task(
        description=(
            "Review the draft and editorial feedback. Your job:\n\n"
            "1) **Resolve all Critical issues** from the review\n"
            "   - Apply suggested fixes or find alternative solutions\n"
            "   - If reviewer and writer disagree on a point, make the judgment call\n\n"
            "2) **Incorporate Minor issues** where value is clear\n"
            "   - Skip minor fixes that would weaken the writer's voice\n\n"
            "3) **Add Editor's Note** at the end (2-3 sentences)\n"
            "   - Why this topic matters now\n"
            "   - One limitation of the analysis (honesty builds trust)\n\n"
            "4) **Quality Gate Check**\n"
            "   - Headline compelling? (Would a busy PM click it?)\n"
            "   - Hook grabs attention in first 10 seconds?\n"
            "   - Conclusion has actionable takeaways?\n"
            "   - Any remaining [NEEDS CITATION] markers? (should be 0)\n\n"
            "If the draft doesn't meet the bar, don't publish. "
            "Flag what needs to be rewritten rather than polishing a weak piece."
        ),
        expected_output=(
            "The final polished article, all critical fixes applied, "
            "with an Editor's Note appended. Publication-ready."
        ),
        agent=coordinator,
    )


# === Pipeline Metrics (for optimization) ===
def estimate_pipeline_cost(topic_complexity: str = "medium") -> dict:
    """Estimate token usage and cost for the pipeline.
    
    These are rough estimates based on GPT-4o pricing ($2.50/$10 per 1M tokens).
    Adjust for your actual model and usage patterns.
    """
    estimates = {
        "simple": {"input_tokens": 3000, "output_tokens": 1500, "total_cost": 0.0225},
        "medium": {"input_tokens": 5000, "output_tokens": 2500, "total_cost": 0.0375},
        "complex": {"input_tokens": 8000, "output_tokens": 4000, "total_cost": 0.0600},
    }
    base = estimates.get(topic_complexity, estimates["medium"])
    # 4 agents = 4x the base cost
    return {
        "per_agent": base,
        "total_pipeline": {
            "input_tokens": base["input_tokens"] * 4,
            "output_tokens": base["output_tokens"] * 4,
            "estimated_cost": round(base["total_cost"] * 4, 4),
        },
    }
