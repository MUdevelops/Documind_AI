import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.message import Message, MessageRole
from app.models.user import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    CitationSchema,
    ConversationDetailResponse,
    ConversationResponse,
    MessageSchema,
)
from app.services.rag_service import answer_question

router = APIRouter(tags=["chat"])


def _get_owned_conversation(db: Session, conversation_id: str, user: User) -> Conversation:
    conv = db.get(Conversation, conversation_id)
    if conv is None or conv.owner_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")
    return conv


@router.post("/chat", response_model=ChatResponse, summary="Ask a question about your documents")
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Question cannot be empty")

    if payload.document_id:
        doc = db.get(Document, payload.document_id)
        if doc is None or doc.owner_id != current_user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")

    if payload.conversation_id:
        conversation = _get_owned_conversation(db, payload.conversation_id, current_user)
    else:
        conversation = Conversation(owner_id=current_user.id, title=question[:60])
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    db.add(Message(conversation_id=conversation.id, role=MessageRole.USER, content=question))
    db.commit()

    # Ownership of retrieved chunks is enforced inside answer_question via
    # owner_id filtering at the vector-store layer -- User A can never
    # retrieve User B's chunks through this call.
    result = answer_question(question, owner_id=current_user.id, document_id=payload.document_id)

    citations_payload = [c.__dict__ for c in result.citations]
    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=result.answer,
        citations_json=json.dumps(citations_payload),
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return ChatResponse(
        conversation_id=conversation.id,
        message_id=assistant_message.id,
        answer=result.answer,
        citations=[CitationSchema(**c) for c in citations_payload],
        insufficient_context=result.insufficient_context,
    )


@router.get(
    "/conversations", response_model=list[ConversationResponse], summary="List conversations"
)
def list_conversations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(Conversation)
        .filter(Conversation.owner_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
    summary="Get a conversation with its messages",
)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conv = _get_owned_conversation(db, conversation_id, current_user)
    messages = [
        MessageSchema(
            id=m.id,
            role=m.role,
            content=m.content,
            citations=[CitationSchema(**c) for c in json.loads(m.citations_json or "[]")],
            created_at=m.created_at,
        )
        for m in conv.messages
    ]
    return ConversationDetailResponse(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=messages,
    )


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a conversation",
)
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conv = _get_owned_conversation(db, conversation_id, current_user)
    db.delete(conv)
    db.commit()
    return None
