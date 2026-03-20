from fastapi import APIRouter, HTTPException

from agent.graph import agent_graph
from schema.schemas import AgentResponse, GoalRequest

router = APIRouter()


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: GoalRequest):
    if not request.goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty")

    try:
        initial_state = {
            "goal": request.goal,
            "messages": [],
            "plan": [],
            "current_step": 0,
            "tool_results": [],
            "reflection_notes": "",
            "answer_draft": "",
            "iteration_count": 0,
            "is_done": False,
            "final_answer": "",
        }

        result = await agent_graph.ainvoke(initial_state)

        steps_taken = [
            f"[{r['tool']}] {r['input'][:80]}" for r in result.get("tool_results", [])
        ]

        return AgentResponse(
            final_answer=result.get("final_answer", "No answer produced"),
            iterations=result.get("iteration_count", 0),
            steps_taken=steps_taken,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    return {"status": "ok"}
