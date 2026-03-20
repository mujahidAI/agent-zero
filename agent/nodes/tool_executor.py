from langchain_core.messages import HumanMessage

from agent.dependencies import get_tool_map
from agent.state import AgentState


def tool_executor(state: AgentState) -> dict:
    decision = state.get("_decision", {})
    tool_name = decision.get("action", "")
    tool_input = decision.get("action_input", "")
    tool_map = get_tool_map()

    if tool_name not in tool_map:
        result = f"Tool '{tool_name}' not found. Available: {list(tool_map.keys())}"
    else:
        try:
            tool = tool_map[tool_name]
            result = tool.invoke(tool_input)

            # Some tools return list of dicts (e.g. Tavily) — normalize to string
            if isinstance(result, list):
                result = "\n".join(item.get("content", str(item)) for item in result)
            else:
                result = str(result)

        except Exception as e:
            result = f"Tool execution error: {str(e)}"

    updated_tool_results = state.get("tool_results", []) + [
        {"tool": tool_name, "input": tool_input, "result": result}
    ]

    current_step = state.get("current_step", 0)
    plan = state.get("plan", [])
    next_step = min(current_step + 1, len(plan) - 1)

    return {
        "tool_results": updated_tool_results,
        "current_step": next_step,
        "messages": [
            HumanMessage(content=f"Tool `{tool_name}` returned: {result[:500]}")
        ],
    }
