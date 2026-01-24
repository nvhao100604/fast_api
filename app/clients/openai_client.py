from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def openai_chat(system_prompt: str, user_message: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"{system_prompt}\nUser: {user_message}"
    )
    return response.output_text
