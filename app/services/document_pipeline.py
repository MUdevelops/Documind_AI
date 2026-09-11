"""End-to-end document ingestion pipeline:

upload -> validate -> extract -> clean -> chunk -> embed -> vector index -> ready

Runs synchronously in a FastAPI BackgroundTask (see api/v1/documents.py). Each
stage updates Document.status so the frontend can poll progress, and any
failure is captured on Document.error_message rather than raised silently.
"""
import logging
import time
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.chunk import DocumentChunk
from app.models.document import Document, DocumentStatus
from app.providers.document_extractors.extractors import ExtractionError, get_extractor
from app.providers.embeddings.sentence_transformers_provider import get_embedding_provider
from app.providers.vector_store.chroma_store import get_vector_store
from app.utils.chunking import chunk_pages

logger = logging.getLogger(__name__)
settings = get_settings()


def process_document(db: Session, document_id: str) -> None:
    document = db.get(Document, document_id)
    if document is None:
        logger.error("process_document: document %s not found", document_id)
        return

    started = time.monotonic()
    try:
        document.status = DocumentStatus.EXTRACTING
        db.commit()

        extractor = get_extractor(document.file_type)
        pages = extractor.extract(Path(document.storage_path))
        document.page_count = len({p for p, _ in pages if p is not None}) or len(pages)

        document.status = DocumentStatus.CHUNKING
        db.commit()
        chunks = chunk_pages(pages, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        if not chunks:
            raise ExtractionError("Document produced no usable chunks")

        document.status = DocumentStatus.EMBEDDING
        db.commit()
        embedder = get_embedding_provider()
        if not embedder.is_available():
            raise RuntimeError(
                "Embedding model is not available. Install/download it and retry."
            )
        vectors = embedder.embed([c.text for c in chunks])

        vector_store = get_vector_store()
        vector_ids = [f"{document.id}:{c.index}" for c in chunks]
        vector_store.upsert(
            ids=vector_ids,
            embeddings=vectors,
            documents=[c.text for c in chunks],
            metadatas=[
                {
                    "document_id": document.id,
                    "owner_id": document.owner_id,
                    "filename": document.original_filename,
                    "page_number": c.page_number or 0,
                    "chunk_index": c.index,
                }
                for c in chunks
            ],
        )

        for c, vid in zip(chunks, vector_ids):
            db.add(
                DocumentChunk(
                    document_id=document.id,
                    owner_id=document.owner_id,
                    chunk_index=c.index,
                    page_number=c.page_number,
                    content=c.text,
                    vector_id=vid,
                )
            )

        document.chunk_count = len(chunks)
        document.status = DocumentStatus.READY
        document.error_message = None
        document.processing_duration_ms = int((time.monotonic() - started) * 1000)
        db.commit()

    except ExtractionError as exc:
        logger.warning("Extraction failed for %s: %s", document_id, exc)
        document.status = DocumentStatus.FAILED
        document.error_message = str(exc)
        document.processing_duration_ms = int((time.monotonic() - started) * 1000)
        db.commit()
    except Exception as exc:  # noqa: BLE001 - top-level pipeline guard
        logger.exception("Unexpected pipeline failure for %s", document_id)
        document.status = DocumentStatus.FAILED
        document.error_message = f"Processing failed: {exc}"
        document.processing_duration_ms = int((time.monotonic() - started) * 1000)
        db.commit()
