from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.document import Document, DocumentStatus
from app.models.message import Message
from app.models.user import User
from app.schemas.chat import AnalyticsResponse

router = APIRouter(tags=["analytics"])


@router.get("/analytics", response_model=AnalyticsResponse, summary="Real usage analytics")
def analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc_q = db.query(Document).filter(Document.owner_id == current_user.id)
    document_count = doc_q.count()
    processed = doc_q.filter(Document.status == DocumentStatus.READY).count()
    failed = doc_q.filter(Document.status == DocumentStatus.FAILED).count()
    total_storage = doc_q.with_entities(func.coalesce(func.sum(Document.size_bytes), 0)).scalar()
    total_chunks = doc_q.with_entities(func.coalesce(func.sum(Document.chunk_count), 0)).scalar()

    conversation_count = (
        db.query(Conversation).filter(Conversation.owner_id == current_user.id).count()
    )
    message_count = (
        db.query(Message)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .filter(Conversation.owner_id == current_user.id)
        .count()
    )

    return AnalyticsResponse(
        document_count=document_count,
        processed_documents=processed,
        failed_documents=failed,
        conversation_count=conversation_count,
        message_count=message_count,
        total_storage_bytes=int(total_storage or 0),
        total_chunks=int(total_chunks or 0),
    )
