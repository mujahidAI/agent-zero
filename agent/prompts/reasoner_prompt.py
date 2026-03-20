def get_reasoner_prompt(
    current_task: str,
    current_step: int,
    total_steps: int,
    plan: list[str],
    tool_results_summary: str,
    reflection_notes: str,
    tool_names: list[str],
) -> str:
    formatted_plan = "\n".join(f"{i+1}. {s}" for i, s in enumerate(plan))

    return f"""You are a reasoning agent working through a plan step by step.

Current task: {current_task}
Step {current_step + 1} of {total_steps}

Full plan:
{formatted_plan}

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
