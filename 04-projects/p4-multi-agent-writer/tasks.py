"""Task definitions for Multi-Agent Writing System - P4."""
from crewai import Task

def create_research_task(topic: str, researcher) -> Task:
    return Task(
        description=(
            f"Research the topic: '{topic}'. Find 5-7 key facts, trends, and expert opinions. "
            "Organize findings into a structured summary with: "
            "1) Key Facts, 2) Current Trends, 3) Expert Opinions, 4) Data Points. "
            "Cite sources where possible."
        ),
        expected_output="A structured research brief with 4 sections, 500-800 words.",
        agent=researcher,
    )

def create_writing_task(topic: str, writer) -> Task:
    return Task(
        description=(
            f"Write a 1000-1500 word article on '{topic}' based on the research brief. "
            "Structure: compelling headline, engaging intro, 3-4 body sections with subheadings, "
            "a conclusion with key takeaways. Target audience: product managers interested in AI. "
            "Tone: professional but approachable."
        ),
        expected_output="A complete first draft article, 1000-1500 words.",
        agent=writer,
    )

def create_review_task(reviewer) -> Task:
    return Task(
        description=(
            "Review the article draft for: "
            "1) Factual accuracy (verify key claims), "
            "2) Logical flow (transitions between sections), "
            "3) Tone consistency, "
            "4) Grammar and style. "
            "Provide a review with: (a) issues found, (b) severity (critical/minor), "
            "(c) suggested fix."
        ),
        expected_output="A structured review with issues and suggested fixes.",
        agent=reviewer,
    )

def create_final_task(coordinator) -> Task:
    return Task(
        description=(
            "Review the article draft and editor feedback. Incorporate all critical fixes. "
            "Resolve any conflicting feedback. Produce the final polished article. "
            "Add a brief editor's note at the end."
        ),
        expected_output="The final polished article ready for publication.",
        agent=coordinator,
    )
