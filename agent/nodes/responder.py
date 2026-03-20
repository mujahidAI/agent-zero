from langchain_core.messages import SystemMessage, AIMessage
from agent.state import AgentState
from agent.llm import llm
from agent.prompts.responder_prompt import get_responder_prompt

def responder(state: AgentState) -> dict:
    goal = state["goal"]
    answer_draft = state.get("answer_draft", "")
    tool_results = state.get("tool_results", [])
    plan = state["plan"]
    iteration_count = state.get("iteration_count", 0)

    evidence = ""
    if tool_results:
        for r in tool_results:
            evidence += f"\n- [{r['tool']}] {r['input']}\n  {r['result'][:400]}"

    system_prompt = get_responder_prompt(
        goal=goal,
        plan=plan,
        evidence=evidence,
        answer_draft=answer_draft,
        iteration_count=iteration_count,
    )

    response = llm.invoke([SystemMessage(content=system_prompt)])
    final_answer = response.content

    return {
        "final_answer": final_answer,
        "messages": [AIMessage(content=final_answer)]
    }