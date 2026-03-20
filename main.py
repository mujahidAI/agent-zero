from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from routers.agent import router as agent_router

app = FastAPI(
    title="agent-zero",
    description="A ReAct agent built with LangGraph",
    version="1.0.0",
)

app.include_router(agent_router)