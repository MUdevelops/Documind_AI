"""Retrieval-augmented generation: embed the question, search the user's own
vectors, build a grounded prompt, and ask the local LLM. Never fabricates an
answer when there isn't enough context, and never mixes documents across
users -- every vector query is filtered by owner_id."""
from dataclasses import dataclass
from typing import List

from app.core.config import get_settings
from app.providers.embeddings.sentence_transformers_provider import get_embedding_provider
from app.providers.llm.ollama_provider import get_llm_provider
from app.providers.vector_store.chroma_store import get_vector_store

settings = get_settings()

_SYSTEM_PROMPT = (
    "You are DocuMind, a careful assistant that answers questions ONLY using "
    "the provided document excerpts. If the excerpts do not contain enough "
    "information to answer, say clearly that you could not find the answer "
    "in the user's documents. Cite the source filename inline like [1], [2] "
    "matching the numbered excerpts. Never invent facts not present in the excerpts."
)


@dataclass
class Citation:
    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    score: float
    excerpt: str


@dataclass
class RagResult:
    answer: str
    citations: List[Citation]
    insufficient_context: bool


def answer_question(question: str, owner_id: str, document_id: str | None = None) -> RagResult:
    embedder = get_embedding_provider()
    vector_store = get_vector_store()
    llm = get_llm_provider()

    query_vector = embedder.embed([question])[0]
    where = {"owner_id": owner_id}
    if document_id:
        where = {"$and": [{"owner_id": owner_id}, {"document_id": document_id}]}

    matches = vector_store.query(query_vector, top_k=settings.TOP_K, where=where)
    matches = [m for m in matches if m["score"] >= settings.SIMILARITY_THRESHOLD]

    if not matches:
        return RagResult(
            answer=(
                "I couldn't find any relevant information in your documents to "
                "answer that question. Try rephrasing, or upload a document that "
                "covers this topic."
            ),
            citations=[],
            insufficient_context=True,
        )

    context_blocks = []
    citations: List[Citation] = []
    for i, m in enumerate(matches, start=1):
        meta = m["metadata"]
        context_blocks.append(f"[{i}] (source: {meta.get('filename')})\n{m['document_text']}")
        citations.append(
            Citation(
                document_id=meta.get("document_id", ""),
                filename=meta.get("filename", "unknown"),
                page_number=int(meta.get("page_number") or 0),
                chunk_index=int(meta.get("chunk_index") or 0),
                score=round(m["score"], 4),
                excerpt=m["document_text"][:300],
            )
        )

    context_text = "\n\n".join(context_blocks)
    prompt = (
        f"Document excerpts:\n\n{context_text}\n\n"
        f"Question: {question}\n\nAnswer using only the excerpts above."
    )

    if not llm.is_available():
        return RagResult(
            answer=(
                "The local LLM is not currently available, so I can't generate an "
                "answer right now. Your relevant document excerpts are listed as "
                "citations below -- start Ollama (see README) and try again."
            ),
            citations=citations,
            insufficient_context=False,
        )

    answer = llm.generate(prompt, system=_SYSTEM_PROMPT)
    return RagResult(answer=answer, citations=citations, insufficient_context=False)
