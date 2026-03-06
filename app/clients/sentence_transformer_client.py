from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


class SentenceTransformerClient:
    """
    Singleton client cho SentenceTransformer
    Default model: sentence-transformers/all-MiniLM-L6-v2
    """

    _instance = None
    _initialized = False

    _model: SentenceTransformer | None = None
    embedding_dimension: int

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        if self._initialized:
            return

        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model_name = model_name

            logger.info(f"Loading SentenceTransformer model: {model_name}")
            logger.info(f"Using device: {self.device}")

            self._model = SentenceTransformer(model_name, device=self.device)
            self.embedding_dimension = self._model.get_sentence_embedding_dimension()
            self._initialized = True

            logger.info(
                f"Model loaded successfully. "
                f"Embedding dimension: {self.embedding_dimension}"
            )

        except Exception as e:
            logger.exception("Failed to initialize SentenceTransformerClient")
            raise RuntimeError("SentenceTransformer initialization failed") from e

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            raise RuntimeError("Model is not initialized")
        return self._model

    # ---------- Encoding ----------

    def encode(
        self,
        text: str,
        *,
        convert_to_tensor: bool = False,
        normalize: bool = False,
    ) -> Union[List[float], torch.Tensor]:
        """
        Encode một câu text thành embedding

        Args:
            text: Chuỗi cần encode
            convert_to_tensor: True -> torch.Tensor
            normalize: Chuẩn hóa vector (L2 norm)

        Returns:
            Embedding vector
        """
        if not isinstance(text, str):
            raise TypeError("encode() expects a single string")

        embedding = self.model.encode(
            text,
            convert_to_tensor=convert_to_tensor,
            normalize_embeddings=normalize,
        )

        if convert_to_tensor:
            return embedding

        return embedding.tolist()

    def encode_batch(
        self,
        texts: List[str],
        *,
        batch_size: int = 32,
        convert_to_tensor: bool = False,
        normalize: bool = False,
    ) -> Union[List[List[float]], torch.Tensor]:
        """
        Encode nhiều câu text

        Args:
            texts: Danh sách chuỗi
            batch_size: Kích thước batch
            convert_to_tensor: True -> torch.Tensor
            normalize: Chuẩn hóa vector

        Returns:
            List embeddings hoặc torch.Tensor
        """
        if not texts:
            return [] if not convert_to_tensor else torch.empty(0)

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_tensor=convert_to_tensor,
            normalize_embeddings=normalize,
        )

        if convert_to_tensor:
            return embeddings

        return embeddings.tolist()

    # ---------- Utilities ----------

    def get_embedding_dimension(self) -> int:
        return self.embedding_dimension

    @staticmethod
    def cosine_similarity(
        emb1: Union[List[float], np.ndarray],
        emb2: Union[List[float], np.ndarray],
    ) -> float:
        """
        Tính cosine similarity giữa 2 embeddings
        Sử dụng sentence-transformers.util.cos_sim
        """

        # Convert về torch.Tensor (yêu cầu của util.cos_sim)
        v1 = torch.tensor(emb1, dtype=torch.float)
        v2 = torch.tensor(emb2, dtype=torch.float)

        if v1.shape != v2.shape:
            raise ValueError("Embedding dimensions do not match")

        # cos_sim trả về tensor shape (1, 1)
        score = util.cos_sim(v1, v2)

        return float(score.item())

# ---------- Singleton instance ----------
sentence_transformer_client = SentenceTransformerClient()
