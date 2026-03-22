from pydantic import BaseModel


class GoalRequest(BaseModel):
    """Goal request schema"""
    goal: str


class AgentResponse(BaseModel):
    """Agent response schema"""
    final_answer: str
    iterations: int
    steps_taken: list[str]
