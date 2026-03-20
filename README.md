# Agent Zero

A ReAct (Reason + Act) agent built with **LangGraph** and **FastAPI**, powered by **Llama 3.3 70B** via Groq.

## How It Works

The agent follows a loop: **Plan → Reason → Act → Reflect → Respond**.

```
User Goal
    ↓
 Planner → breaks goal into steps
    ↓
 Reasoner → decides: use a tool or reflect?
    ↓              ↓
 Tool Executor   Reflector → enough info? confident?
    ↓              ↓              ↓
    └─→ back to Reasoner    Responder → final answer
```

## Project Structure

```
agent-zero/
├── main.py                         # FastAPI app + router registration
├── schemas.py                      # Pydantic request/response models
├── routers/
│   └── agent.py                    # /run and /health endpoints
├── agent/
│   ├── llm.py                      # Shared LLM instance
│   ├── state.py                    # AgentState TypedDict
│   ├── graph.py                    # LangGraph wiring
│   ├── nodes/
│   │   ├── planner.py              # Breaks goal into subtasks
│   │   ├── reasoner.py             # Decides next action
│   │   ├── tool_executor.py        # Runs selected tool
│   │   ├── reflector.py            # Self-critique loop
│   │   └── responder.py            # Formats final answer
│   ├── prompts/
│   │   ├── planner_prompt.py
│   │   ├── reasoner_prompt.py
│   │   ├── reflector_prompt.py
│   │   └── responder_prompt.py
│   └── tools/
│       ├── search.py               # Tavily web search
│       ├── calculator.py           # Math expression evaluator
│       └── file_reader.py          # Local file reader
```

## Setup

```bash
# Clone and enter
git clone <repo-url>
cd agent-zero

# Install dependencies
uv sync

# Configure API keys
cp .env.example .env
# Edit .env with your keys:
#   GROQ_API_KEY=...
#   TAVILY_API_KEY=...
```

## Run

```bash
uv run uvicorn main:app --reload
```

## API

**POST** `/run` — Run the agent with a goal

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"goal": "Compare PostgreSQL vs MongoDB for a 10M record dataset"}'
```

Response:
```json
{
  "final_answer": "...",
  "iterations": 4,
  "steps_taken": [
    "[search] PostgreSQL pros and cons",
    "[search] MongoDB pros and cons",
    "[calculator] 10000000 * 0.10 / 1024"
  ]
}
```

**GET** `/health` — Health check

**GET** `/docs` — Swagger UI

## Tech Stack

- **LLM**: Llama 3.3 70B via Groq
- **Framework**: LangGraph + FastAPI
- **Tools**: Tavily Search, Calculator, File Reader
- **Package Manager**: uv
- **Linting**: Ruff
