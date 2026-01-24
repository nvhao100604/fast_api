# from app.clients.openai_client import openai_chat
from app.prompts.loader import load_prompt

class ChatService:
    def handle_chat(self, req):
        system_prompt = load_prompt("chat.txt")
        # reply = openai_chat(system_prompt, req.message)
        reply = "This is a placeholder reply."
        return {"reply": reply}

chat_service = ChatService()
