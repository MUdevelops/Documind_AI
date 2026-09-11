"""Text extraction for PDF, DOCX, TXT and Markdown files.

Each extractor returns a list of (page_number_or_None, text) tuples so the
pipeline can preserve page-level citations where the format supports it.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple


class ExtractionError(Exception):
    pass


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, path: Path) -> List[Tuple[Optional[int], str]]:
        ...


class PdfExtractor(BaseExtractor):
    def extract(self, path: Path) -> List[Tuple[Optional[int], str]]:
        try:
            import fitz  # PyMuPDF
        except ImportError as exc:  # pragma: no cover
            raise ExtractionError("PyMuPDF is not installed") from exc

        pages: List[Tuple[Optional[int], str]] = []
        try:
            with fitz.open(path) as doc:
                if doc.page_count == 0:
                    raise ExtractionError("PDF has no pages")
                for i, page in enumerate(doc):
                    text = page.get_text("text").strip()
                    if text:
                        pages.append((i + 1, text))
        except Exception as exc:
            raise ExtractionError(f"Failed to parse PDF: {exc}") from exc

        if not pages:
            raise ExtractionError("No extractable text found in PDF (it may be scanned/image-only)")
        return pages


class DocxExtractor(BaseExtractor):
    def extract(self, path: Path) -> List[Tuple[Optional[int], str]]:
        try:
            import docx
        except ImportError as exc:  # pragma: no cover
            raise ExtractionError("python-docx is not installed") from exc

        try:
            d = docx.Document(str(path))
            paragraphs = [p.text for p in d.paragraphs if p.text.strip()]
        except Exception as exc:
            raise ExtractionError(f"Failed to parse DOCX: {exc}") from exc

        text = "\n".join(paragraphs).strip()
        if not text:
            raise ExtractionError("DOCX file contains no extractable text")
        return [(None, text)]


class PlainTextExtractor(BaseExtractor):
    def extract(self, path: Path) -> List[Tuple[Optional[int], str]]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace").strip()
        except Exception as exc:
            raise ExtractionError(f"Failed to read text file: {exc}") from exc
        if not text:
            raise ExtractionError("File is empty")
        return [(None, text)]


_EXTRACTORS = {
    "pdf": PdfExtractor(),
    "docx": DocxExtractor(),
    "txt": PlainTextExtractor(),
    "md": PlainTextExtractor(),
}


def get_extractor(file_type: str) -> BaseExtractor:
    extractor = _EXTRACTORS.get(file_type.lower().lstrip("."))
    if extractor is None:
        raise ExtractionError(f"Unsupported file type: {file_type}")
    return extractor
