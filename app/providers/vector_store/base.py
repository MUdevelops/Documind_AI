from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypedDict


class VectorMatch(TypedDict):
    id: str
    score: float
    metadata: Dict[str, Any]
    document_text: str


class VectorStore(ABC):
    @abstractmethod
    def upsert(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        ...

    @abstractmethod
    def query(
        self,
        embedding: List[float],
        top_k: int,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[VectorMatch]:
        ...

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        ...

    @abstractmethod
    def delete_by_document(self, owner_id: str, document_id: str) -> None:
        ...
