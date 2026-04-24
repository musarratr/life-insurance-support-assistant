import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else BASE_DIR / path


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATABASE_PATH = resolve_path(os.getenv("DATABASE_PATH", "./life_insurance_assistant.db"))
KNOWLEDGE_BASE_PATH = resolve_path(
    os.getenv("KNOWLEDGE_BASE_PATH", "./data/life_insurance_kb.md")
)
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
