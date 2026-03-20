from .calculator import calculator
from .file_reader import file_reader
from .search import get_search_tool


def get_all_tools():
    return [calculator, file_reader, get_search_tool()]
