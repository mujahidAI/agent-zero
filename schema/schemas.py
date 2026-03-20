from pydantic import BaseModel


class GoalRequest(BaseModel):
    goal: str


class AgentResponse(BaseModel):
    final_answer: str
    iterations: int
    steps_taken: list[str]
