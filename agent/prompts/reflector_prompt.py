def get_reflector_prompt(
    goal: str,
    plan: list[str],
    tool_results_summary: str,
    answer_draft: str,
    iteration_count: int,
) -> str:
    formatted_plan = "\n".join(f"{i+1}. {s}" for i, s in enumerate(plan))

    return f"""You are a self-critique agent. Your job is to review the current answer draft
and decide if it fully satisfies the original goal.

Original goal: {goal}

Full plan:
{formatted_plan}

Tool results collected:
{tool_results_summary if tool_results_summary else "None"}

Current answer draft:
{answer_draft if answer_draft else "No draft yet"}

Iteration count: {iteration_count}

Respond in this EXACT JSON format, nothing else:
{{
  "critique": "what is missing or weak in the current draft",
  "is_done": true or false,
  "reflection_notes": "specific instructions for the reasoner on what to do next",
  "confidence": 0.0 to 1.0
}}

Rules for is_done:
- Set true if the draft fully addresses all parts of the goal
- Set true if iteration_count >= 8 (force stop)
- Set true if confidence >= 0.85
- Set false if key information is still missing
"""
