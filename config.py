import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SURPRISE_THRESHOLD = float(os.getenv("SURPRISE_THRESHOLD", "0.7"))
MEMORY_MAX_SIZE = int(os.getenv("MEMORY_MAX_SIZE", "1000"))

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 1
GROQ_MAX_TOKENS = 1024
GROQ_TOP_P = 1

JOB_SEARCH_PARAMS = {
    "max_results": 10,
    "search_depth": "advanced"
}

