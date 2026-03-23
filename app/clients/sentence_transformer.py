from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np
from typing import List, Union, Optional
import logging
import threading

logger = logging.getLogger(__name__)


class SentenceTransformerClient:
    _instance = None
    _lock = threading.Lock()  # Đảm bảo thread-safe cho Singleton
    _initialized = False
    _model: Optional[SentenceTransformer] = None
    embedding_dimension: int

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        if self._initialized:
            return

        try:
            # Tự động chọn thiết bị tốt nhất (CUDA > MPS > CPU)
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"

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

    # ---------- Health check ----------

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
        if not isinstance(text, str):
            raise TypeError("encode() expects a single string")

        embedding = self.model.encode(
            text,
            convert_to_tensor=convert_to_tensor,
            normalize_embeddings=normalize,
            show_progress_bar=False,
        )

        if convert_to_tensor:
            print(f"Generated embedding (tensor): {embedding}")
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
        if not texts:
            return [] if not convert_to_tensor else torch.empty(0)

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_tensor=convert_to_tensor,
            normalize_embeddings=normalize,
            show_progress_bar=False,
        )

        if convert_to_tensor:
            return embeddings

        return embeddings.tolist()

    # ---------- Utilities ----------

    def get_embedding_dimension(self) -> int:
        return self.embedding_dimension

    @staticmethod
    def cosine_similarity(
        emb1: Union[List[float], np.ndarray, torch.Tensor],
        emb2: Union[List[float], np.ndarray, torch.Tensor],
    ) -> float:
        """Tính cosine similarity giữa 2 embeddings"""

        # Chuyển đổi đầu vào thành Tensor nếu cần
        v1 = (
            emb1
            if isinstance(emb1, torch.Tensor)
            else torch.tensor(emb1, dtype=torch.float)
        )
        v2 = (
            emb2
            if isinstance(emb2, torch.Tensor)
            else torch.tensor(emb2, dtype=torch.float)
        )

        if v1.shape != v2.shape:
            raise ValueError(
                f"Embedding dimensions do not match: {v1.shape} vs {v2.shape}"
            )

        # cos_sim trả về matrix, lấy giá trị đơn lẻ
        score = util.cos_sim(v1, v2)
        return float(score.item())


# Khởi tạo instance
sentence_transformer_client = SentenceTransformerClient()
