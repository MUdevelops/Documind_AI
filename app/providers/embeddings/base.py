from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return one embedding vector per input text."""

    @abstractmethod
    def is_available(self) -> bool:
        """Whether the underlying model/runtime is ready to use."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        ...
