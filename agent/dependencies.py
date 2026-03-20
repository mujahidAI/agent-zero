from functools import lru_cache

from agent.tools import get_all_tools


@lru_cache
def get_tool_map() -> dict:
    tools = get_all_tools()
    return {t.name: t for t in tools}


@lru_cache
def get_tool_names() -> list[str]:
    return list(get_tool_map().keys())


def get_agent_graph():
    # Lazy import to avoid circular dependency: dependencies → graph → nodes → dependencies
    from agent.graph import build_graph

    return build_graph()
