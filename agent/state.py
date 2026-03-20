from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    goal: str
    plan: list[str]
    current_step: int
    tool_results: list[dict]
    reflection_notes: str
    answer_draft: str
    iteration_count: int
    is_done: bool
    final_answer: str
