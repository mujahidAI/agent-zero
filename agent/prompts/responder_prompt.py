def get_responder_prompt(
    goal: str,
    plan: list[str],
    evidence: str,
    answer_draft: str,
    iteration_count: int,
) -> str:
    formatted_plan = "\n".join(f"{i+1}. {s}" for i, s in enumerate(plan))

    return f"""You are a response formatting agent.
Your job is to take a rough answer draft and all collected evidence,
and produce a final, clean, well-structured answer for the user.

Original goal: {goal}

Plan that was followed:
{formatted_plan}

Evidence collected:
{evidence if evidence else "None"}

Answer draft:
{answer_draft if answer_draft else "No draft available"}

Loops taken: {iteration_count}

Instructions:
- Write a clear, structured final answer
- Use headers and bullet points where appropriate
- Include specific data/numbers from tool results
- End with a concrete recommendation or conclusion
- Do NOT mention the internal plan, tools, or agent process
- Write as if responding directly to the user
"""
