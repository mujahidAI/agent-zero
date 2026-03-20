import json

from langchain_core.messages import AIMessage, SystemMessage

from agent.dependencies import get_tool_names
from agent.llm import get_llm
from agent.prompts.reasoner_prompt import get_reasoner_prompt
from agent.state import AgentState


def reasoner(state: AgentState) -> dict:
    plan = state["plan"]
    current_step = state["current_step"]
    tool_results = state["tool_results"]
    reflection_notes = state.get("reflection_notes", "")
    iteration_count = state["iteration_count"]

    # Hard stop — force done if too many iterations
    if iteration_count >= 10:
        return {"is_done": True}

    tool_results_summary = ""
    if tool_results:
        for r in tool_results:
            tool_results_summary += f"\n- [{r['tool']}]: {r['result'][:300]}"

    current_task = (
        plan[current_step] if current_step < len(plan) else "All steps complete"
    )

    system_prompt = get_reasoner_prompt(
        current_task=current_task,
        current_step=current_step,
        total_steps=len(plan),
        plan=plan,
        tool_results_summary=tool_results_summary,
        reflection_notes=reflection_notes,
        tool_names=get_tool_names(),
    )

    response = get_llm().invoke([SystemMessage(content=system_prompt)])

    # Safely parse JSON response
    try:
        raw = response.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        decision = json.loads(raw.strip())
    except Exception:
        # Fallback if LLM doesn't return clean JSON
        decision = {
            "thought": "Failed to parse response",
            "action": "reflect",
            "action_input": "",
            "answer_draft": state.get("answer_draft", ""),
        }

    ai_message = AIMessage(content=decision["thought"])

    return {
        "messages": [ai_message],
        "answer_draft": decision.get("answer_draft", ""),
        "iteration_count": iteration_count + 1,
        "_decision": decision,  # temp field used by conditional edge
    }
