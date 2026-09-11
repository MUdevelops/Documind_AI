from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionLocal
from app.providers.embeddings.sentence_transformers_provider import get_embedding_provider
from app.providers.llm.ollama_provider import get_llm_provider

router = APIRouter(tags=["health"])


@router.get("/health", summary="Liveness/component health check")
def health():
    components = {"application": "ok"}

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        components["database"] = "ok"
    except Exception as exc:  # noqa: BLE001
        components["database"] = f"error: {exc}"

    try:
        embedder = get_embedding_provider()
        components["embedding_model"] = "ok" if embedder.is_available() else "unavailable"
    except Exception as exc:  # noqa: BLE001
        components["embedding_model"] = f"error: {exc}"

    try:
        llm = get_llm_provider()
        components["llm"] = "ok" if llm.is_available() else "unavailable"
    except Exception as exc:  # noqa: BLE001
        components["llm"] = f"error: {exc}"

    overall = "ok" if components["database"] == "ok" else "degraded"
    return {"status": overall, "components": components}
