from langgraph.graph import END, StateGraph

from agent.nodes.planner import planner
from agent.nodes.reasoner import reasoner
from agent.nodes.reflector import reflector
from agent.nodes.responder import responder
from agent.nodes.tool_executor import tool_executor
from agent.state import AgentState


def route_reasoner(state: AgentState) -> str:
    """Conditional edge: routes reasoner output to tool_executor or reflector."""
    decision = state.get("_decision", {})
    action = decision.get("action", "reflect")

    from agent.tools import get_all_tools
    tool_names = [t.name for t in get_all_tools()]

    if action in tool_names:
        return "tool_executor"
    return "reflector"


def route_reflector(state: AgentState) -> str:
    """Conditional edge: routes reflector output to reasoner or responder."""
    if state.get("is_done", False):
        return "responder"
    return "reasoner"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # --- Register nodes ---
    graph.add_node("planner", planner)
    graph.add_node("reasoner", reasoner)
    graph.add_node("tool_executor", tool_executor)
    graph.add_node("reflector", reflector)
    graph.add_node("responder", responder)

    # --- Entry point ---
    graph.set_entry_point("planner")

    # --- Linear edges ---
    graph.add_edge("planner", "reasoner")
    graph.add_edge("tool_executor", "reasoner")  # always loops back

    # --- Conditional edges ---
    graph.add_conditional_edges(
        "reasoner",
        route_reasoner,
        {
            "tool_executor": "tool_executor",
            "reflector": "reflector"
        }
    )

    graph.add_conditional_edges(
        "reflector",
        route_reflector,
        {
            "reasoner": "reasoner",
            "responder": "responder"
        }
    )

    # --- Terminal edge ---
    graph.add_edge("responder", END)

    return graph.compile()


# Compiled graph instance — imported by FastAPI
agent_graph = build_graph()
