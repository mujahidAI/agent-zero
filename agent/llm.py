import os
from functools import lru_cache

from langchain_openai import ChatOpenAI

# from langchain_groq import ChatGroq

@lru_cache
def get_llm():
    return ChatOpenAI(
        model="o3",
        api_key=os.getenv("OPENAI_API_KEY"),
    )


# @lru_cache
# def get_llm():
#     return ChatGroq(
#         model="llama-3.3-70b-versatile",
#         api_key=os.getenv("GROQ_API_KEY"),
#     )
