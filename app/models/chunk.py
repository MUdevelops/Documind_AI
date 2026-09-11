import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class DocumentChunk(Base):
    """Metadata row for a chunk. The embedding vector itself lives in the
    vector store (Chroma); this row is the source-of-truth for text + citation
    metadata and lets us enforce per-user ownership at the SQL layer too."""

    __tablename__ = "document_chunks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    document_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("documents.id"), index=True
    )
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)

    chunk_index: Mapped[int] = mapped_column(Integer)
    page_number: Mapped[int] = mapped_column(Integer, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    vector_id: Mapped[str] = mapped_column(String(64), index=True)

    document = relationship("Document", back_populates="chunks")
