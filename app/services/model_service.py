
class ModelService:
    def __init__(self):
        pass
    def reply(self, text: str) -> str:
        return f"M la con cho {text}"
    
    def model_Loaded(self) -> bool:
        return True
    
model_service = ModelService()