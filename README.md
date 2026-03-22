# Agent Zero

A **FastAPI** service that runs a ReAct (Reason + Act) agent: **LangGraph** orchestrates the workflow, **Groq** hosts **Llama 3.3 70B**, and **Tavily** provides web search. Dependencies are managed with **uv**; the app ships in a **multi-stage Docker** image based on `python:3.12-slim`.

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
├── schema/
│   └── schemas.py                  # Pydantic request/response models
├── routers/
│   └── agent.py                    # /run and /health endpoints
├── agent/
│   ├── dependencies.py             # Dependency injection providers
│   ├── llm.py                      # LLM provider (get_llm)
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

**Local (development)**

```bash
uv run uvicorn main:app --reload
```

**Docker**

Build and run the production image (same layout as CI):

```bash
docker build -t agent-zero .
docker run --rm -p 8000:8000 \
  -e GROQ_API_KEY=... \
  -e TAVILY_API_KEY=... \
  agent-zero
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

## Deployment

CI deploys on push to `master` (Docker Hub → Oracle VM; keys via GitHub secrets). **Live:** [http://141.148.79.204:8000/docs](http://141.148.79.204:8000/docs)

## Architecture

The project uses **dependency injection** — no hardcoded globals:

- **`agent/llm.py`** — `get_llm()` returns the LLM instance (cached via `@lru_cache`)
- **`agent/dependencies.py`** — centralized providers: `get_tool_map()`, `get_tool_names()`, `get_agent_graph()`
- **Router** — uses FastAPI `Depends(get_agent_graph)` to inject the graph
- **Nodes** — call `get_llm()` and `get_tool_names()` at runtime, not import time

This makes testing, model swapping, and tool changes easy — modify one provider function, everything picks it up.

## Tech Stack

| Area | Choice |
|------|--------|
| Runtime | Python 3.12 |
| API | FastAPI |
| Agent | LangGraph (ReAct-style loop) |
| LLM | Llama 3.3 70B via Groq |
| Web search | Tavily |
| Other tools | Calculator, file reader |
| Packaging | uv; multi-stage Docker (`python:3.12-slim`) |
| Linting | Ruff |
