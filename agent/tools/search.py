from langchain_community.tools.tavily_search import TavilySearchResults


def get_search_tool():
    return TavilySearchResults(
        max_results=5,
        description="Search the web for current information on any topic.",
    )
