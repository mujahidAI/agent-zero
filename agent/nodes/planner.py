from langchain_core.messages import HumanMessage, SystemMessage
from agent.state import AgentState
from agent.llm import llm
from agent.prompts.planner_prompt import PLANNER_SYSTEM


def planner(state: AgentState) -> dict:
    goal = state["goal"]

    messages = [
        SystemMessage(content=PLANNER_SYSTEM),
        HumanMessage(content=f"Goal: {goal}"),
    ]

    response = llm.invoke(messages)
    raw_plan = response.content

    # Parse numbered list into a clean Python list
    steps = []
    for line in raw_plan.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            # Strip the number prefix e.g. "1. " or "1) "
            step = line.split(".", 1)[-1].split(")", 1)[-1].strip()
            steps.append(step)

    return {
        "plan": steps,
        "current_step": 0,
        "iteration_count": 0,
        "is_done": False,
        "tool_results": [],
        "messages": [HumanMessage(content=f"Goal: {goal}")],
    }
