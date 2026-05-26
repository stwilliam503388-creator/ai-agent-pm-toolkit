"""
Multi-Agent Writing System - P4 Project (CrewAI version)
4 Agents: Researcher -> Writer -> Reviewer -> Coordinator
"""
from crewai import Crew, Process
from agents import researcher, writer, reviewer, coordinator
from tasks import (
    create_research_task, create_writing_task,
    create_review_task, create_final_task,
)


def run_writing_pipeline(topic: str) -> str:
    """Run the full 4-agent writing pipeline."""

    # Create tasks with dependencies
    research_task = create_research_task(topic, researcher)
    writing_task = create_writing_task(topic, writer)
    review_task = create_review_task(reviewer)
    final_task = create_final_task(coordinator)

    # Set up the crew
    crew = Crew(
        agents=[researcher, writer, reviewer, coordinator],
        tasks=[research_task, writing_task, review_task, final_task],
        process=Process.sequential,  # Execute tasks in order
        verbose=True,
    )

    print(f"Starting writing pipeline for topic: {topic}")
    print(f"Agents: {[a.role for a in crew.agents]}")
    print(f"Tasks: 4 (sequential)")

    result = crew.kickoff()
    return result


# === LangGraph fallback (simpler version if CrewAI is too heavy) ===

def run_langgraph_fallback(topic: str) -> str:
    """
    Lightweight fallback using LangGraph StateGraph.
    Use this if CrewAI installation is problematic.
    """
    try:
        from langgraph.graph import StateGraph, END
        from typing import TypedDict
    except ImportError:
        return f"LangGraph not installed. Run: pip install langgraph\nTopic: {topic}\n[Fallback: manual workflow needed]"

    class WriterState(TypedDict):
        topic: str
        research: str
        draft: str
        review: str
        final: str

    def research_node(state: WriterState) -> WriterState:
        state["research"] = (
            f"Research on '{state['topic']}': "
            f"Key trends identified, 3 expert sources reviewed. "
            f"Summary: [research output for {state['topic']}]"
        )
        return state

    def write_node(state: WriterState) -> WriterState:
        state["draft"] = (
            f"# {state['topic']}\n\n"
            f"## Introduction\nBased on research findings...\n\n"
            f"## Key Findings\n{state['research']}\n\n"
            f"## Conclusion\nIn summary..."
        )
        return state

    def review_node(state: WriterState) -> WriterState:
        state["review"] = "Review: accuracy OK, flow good, minor grammar fixes needed."
        return state

    def final_node(state: WriterState) -> WriterState:
        state["final"] = f"{state['draft']}\n\n---\n*Reviewed and approved.*"
        return state

    workflow = StateGraph(WriterState)
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("review", review_node)
    workflow.add_node("final", final_node)
    workflow.set_entry_point("research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "review")
    workflow.add_edge("review", "final")
    workflow.add_edge("final", END)

    app = workflow.compile()
    result = app.invoke({"topic": topic})
    return result["final"]


if __name__ == "__main__":
    import sys

    topic = sys.argv[1] if len(sys.argv) > 1 else "2026 AI Agent Industry Trends"

    # Try CrewAI first, fall back to LangGraph
    try:
        import crewai  # noqa
        print("Using CrewAI pipeline...")
        output = run_writing_pipeline(topic)
    except ImportError:
        print("CrewAI not installed. Using LangGraph fallback...")
        output = run_langgraph_fallback(topic)

    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(output)
