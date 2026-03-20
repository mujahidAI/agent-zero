from langchain_core.messages import SystemMessage, AIMessage
from agent.state import AgentState
from agent.tools import get_all_tools
from agent.llm import llm
from agent.prompts.reasoner_prompt import get_reasoner_prompt
import json

tools = get_all_tools()
tool_names = [t.name for t in tools]


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

    system_prompt = f"""You are a reasoning agent working through a plan step by step.

Current task: {current_task}
Step {current_step + 1} of {len(plan)}

Full plan:
{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(plan))}

Tool results so far:
{tool_results_summary if tool_results_summary else "None yet"}

Reflection notes from previous loop:
{reflection_notes if reflection_notes else "None"}

Available tools: {tool_names}

Your job: Decide what to do next.

Respond in this EXACT JSON format, nothing else:
{{
  "thought": "your reasoning here",
  "action": "tool_name OR 'reflect'",
  "action_input": "input for the tool, or empty string if action is reflect",
  "answer_draft": "your current best answer based on what you know so far"
}}

Rules:
- If you need information → pick a tool from {tool_names}
- If you have enough info for this step → action should be "reflect"
- action_input must be a plain string, not a dict
"""

    response = llm.invoke([SystemMessage(content=system_prompt)])

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
