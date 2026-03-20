import os

from langchain_core.tools import tool


@tool
def file_reader(filepath: str) -> str:
    """Read the contents of a local text file. Input must be a valid file path.
    Use this when the user wants to analyze or reference a local document.
    """
    try:
        if not os.path.exists(filepath):
            return f"File not found: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if len(content) > 4000:
            return content[:4000] + "\n... [truncated]"
        return content
    except Exception as e:
        return f"File read error: {str(e)}"
