from langchain_core.messages import SystemMessage, AIMessage
from agent.state import AgentState
from agent.llm import llm
from agent.prompts.reflector_prompt import get_reflector_prompt
import json

def reflector(state: AgentState) -> dict:
    plan = state["plan"]
    tool_results = state.get("tool_results", [])
    answer_draft = state.get("answer_draft", "")
    iteration_count = state.get("iteration_count", 0)
    goal = state["goal"]

    # Build tool results summary
    tool_results_summary = ""
    if tool_results:
        for r in tool_results:
            tool_results_summary += f"\n- [{r['tool']}] Input: {r['input']}\n  Result: {r['result'][:400]}"

    system_prompt = get_reflector_prompt(
        goal=goal,
        plan=plan,
        tool_results_summary=tool_results_summary,
        answer_draft=answer_draft,
        iteration_count=iteration_count,
    )

    response = llm.invoke([SystemMessage(content=system_prompt)])

    # Safely parse JSON
    try:
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        reflection = json.loads(raw.strip())
    except Exception:
        reflection = {
            "critique": "Could not parse reflection",
            "is_done": True,
            "reflection_notes": "Proceed with current draft",
            "confidence": 0.5
        }

    is_done = (
        reflection.get("is_done", False)
        or reflection.get("confidence", 0) >= 0.85
        or iteration_count >= 8
    )

    ai_message = AIMessage(
        content=f"Reflection: {reflection.get('critique', '')}"
    )

    return {
        "reflection_notes": reflection.get("reflection_notes", ""),
        "is_done": is_done,
        "messages": [ai_message]
    }
