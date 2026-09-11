from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    document_id: Optional[str] = None


class CitationSchema(BaseModel):
    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    score: float
    excerpt: str


class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    citations: List[CitationSchema]
    insufficient_context: bool


class MessageSchema(BaseModel):
    id: str
    role: str
    content: str
    citations: List[CitationSchema]
    created_at: datetime


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageSchema]


class SearchResultSchema(BaseModel):
    document_id: str
    filename: str
    excerpt: str
    score: float
    page_number: int
    chunk_index: int


class AnalyticsResponse(BaseModel):
    document_count: int
    processed_documents: int
    failed_documents: int
    conversation_count: int
    message_count: int
    total_storage_bytes: int
    total_chunks: int
