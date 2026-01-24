from pathlib import Path

def load_prompt(filename: str) -> str:
    path = Path("app/prompts") / filename
    return path.read_text(encoding="utf-8")
