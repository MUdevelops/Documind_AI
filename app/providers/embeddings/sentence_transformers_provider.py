import logging
from functools import lru_cache
from typing import List

from app.core.config import get_settings
from app.providers.embeddings.base import EmbeddingProvider

logger = logging.getLogger(__name__)
settings = get_settings()


class SentenceTransformersProvider(EmbeddingProvider):
    """Local, free embedding provider backed by the sentence-transformers
    library. Model weights are downloaded once from Hugging Face on first use
    and cached locally afterward -- no paid API required."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self._model = None
        self._dim = 384  # default for all-MiniLM-L6-v2

    def _load(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self._dim = self._model.get_sentence_embedding_dimension()
        return self._model

    def is_available(self) -> bool:
        try:
            self._load()
            return True
        except Exception as exc:  # pragma: no cover - depends on env
            logger.warning("Embedding model unavailable: %s", exc)
            return False

    def embed(self, texts: List[str]) -> List[List[float]]:
        model = self._load()
        vectors = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        return [v.tolist() for v in vectors]

    @property
    def dimension(self) -> int:
        return self._dim


@lru_cache
def get_embedding_provider() -> EmbeddingProvider:
    if settings.EMBEDDING_PROVIDER == "sentence_transformers":
        return SentenceTransformersProvider()
    raise ValueError(f"Unknown EMBEDDING_PROVIDER: {settings.EMBEDDING_PROVIDER}")
