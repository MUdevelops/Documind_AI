from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User
from app.providers.embeddings.sentence_transformers_provider import get_embedding_provider
from app.providers.vector_store.chroma_store import get_vector_store
from app.schemas.chat import SearchResultSchema

router = APIRouter(tags=["search"])
settings = get_settings()


@router.get("/search", response_model=list[SearchResultSchema], summary="Semantic document search")
def search(
    q: str = Query(..., min_length=1),
    top_k: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    embedder = get_embedding_provider()
    if not embedder.is_available():
        return []

    vector = embedder.embed([q])[0]
    matches = get_vector_store().query(vector, top_k=top_k, where={"owner_id": current_user.id})

    return [
        SearchResultSchema(
            document_id=m["metadata"].get("document_id", ""),
            filename=m["metadata"].get("filename", "unknown"),
            excerpt=m["document_text"][:300],
            score=round(m["score"], 4),
            page_number=int(m["metadata"].get("page_number") or 0),
            chunk_index=int(m["metadata"].get("chunk_index") or 0),
        )
        for m in matches
        if m["score"] >= settings.SIMILARITY_THRESHOLD
    ]
