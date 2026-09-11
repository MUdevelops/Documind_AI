"""Fixed-size, overlapping character chunking with page tracking.

A simple, dependency-free splitter. Good enough for general prose; swapping
in a token-aware splitter is a drop-in change behind this same function
signature if needed later.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Chunk:
    text: str
    page_number: Optional[int]
    index: int


def chunk_pages(
    pages: List[Tuple[Optional[int], str]], chunk_size: int, overlap: int
) -> List[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 4)

    chunks: List[Chunk] = []
    index = 0
    for page_number, text in pages:
        text = text.strip()
        if not text:
            continue
        start = 0
        n = len(text)
        while start < n:
            end = min(start + chunk_size, n)
            piece = text[start:end].strip()
            if piece:
                chunks.append(Chunk(text=piece, page_number=page_number, index=index))
                index += 1
            if end == n:
                break
            start = end - overlap
    return chunks
