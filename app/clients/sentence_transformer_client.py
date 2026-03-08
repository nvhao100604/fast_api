from sentence_transformers import SentenceTransformer
import torch

class SentenceTransformerClient:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, text: str):
        return self.model.encode(text).tolist()

sentence_client = SentenceTransformerClient()