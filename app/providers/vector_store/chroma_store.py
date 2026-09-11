from functools import lru_cache
from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.providers.vector_store.base import VectorMatch, VectorStore

settings = get_settings()

_COLLECTION_NAME = "documind_chunks"


class ChromaVectorStore(VectorStore):
    """Persistent local vector store using ChromaDB. Data lives on disk at
    VECTOR_DB_PATH -- no external service or paid API required."""

    def __init__(self, path: str | None = None):
        import chromadb

        self._client = chromadb.PersistentClient(path=path or settings.VECTOR_DB_PATH)
        self._collection = self._client.get_or_create_collection(
            name=_COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )

    def upsert(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        self._collection.upsert(
            ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
        )

    def query(
        self,
        embedding: List[float],
        top_k: int,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[VectorMatch]:
        result = self._collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where or {},
        )
        matches: List[VectorMatch] = []
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        for i, vid in enumerate(ids):
            # Chroma with cosine space returns a distance in [0, 2]; convert to
            # a similarity score in roughly [0, 1] for display/thresholding.
            distance = distances[i] if i < len(distances) else 1.0
            score = max(0.0, 1.0 - distance / 2.0)
            matches.append(
                VectorMatch(
                    id=vid,
                    score=score,
                    metadata=metadatas[i] if i < len(metadatas) else {},
                    document_text=documents[i] if i < len(documents) else "",
                )
            )
        return matches

    def delete(self, ids: List[str]) -> None:
        if ids:
            self._collection.delete(ids=ids)

    def delete_by_document(self, owner_id: str, document_id: str) -> None:
        self._collection.delete(where={"document_id": document_id, "owner_id": owner_id})


@lru_cache
def get_vector_store() -> VectorStore:
    return ChromaVectorStore()
