from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Input must be a valid Python math expression.
    Examples: '2 + 2', '100 * 1.08', '(500 * 12) / 100'
    """
    try:
        allowed = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
        }
        result = eval(expression, allowed)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"
