import hashlib
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.chunk import DocumentChunk
from app.models.document import Document, DocumentStatus
from app.models.user import User
from app.providers.vector_store.chroma_store import get_vector_store
from app.schemas.document import DocumentListResponse, DocumentResponse, DocumentStatusResponse
from app.services.document_pipeline import process_document

router = APIRouter(prefix="/documents", tags=["documents"])
settings = get_settings()


def _safe_extension(filename: str) -> str:
    ext = Path(filename).suffix.lower().lstrip(".")
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '.{ext}'. Allowed: {settings.ALLOWED_EXTENSIONS}",
        )
    return ext


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document for processing",
)
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ext = _safe_extension(file.filename or "")

    content = file.file.read()
    if len(content) == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Uploaded file is empty")
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"File exceeds max upload size of {settings.MAX_UPLOAD_SIZE} bytes",
        )

    checksum = hashlib.sha256(content).hexdigest()
    duplicate = (
        db.query(Document)
        .filter(Document.owner_id == current_user.id, Document.checksum == checksum)
        .first()
    )
    if duplicate:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"This file was already uploaded as document {duplicate.id}",
        )

    upload_dir = Path(settings.UPLOAD_DIR) / current_user.id
    upload_dir.mkdir(parents=True, exist_ok=True)
    # Safe, non-guessable stored filename -- never trust the client filename
    # for the on-disk path (path traversal protection).
    stored_name = f"{uuid.uuid4()}.{ext}"
    storage_path = upload_dir / stored_name
    storage_path.write_bytes(content)

    document = Document(
        owner_id=current_user.id,
        filename=stored_name,
        original_filename=Path(file.filename or "upload").name,
        file_type=ext,
        size_bytes=len(content),
        checksum=checksum,
        storage_path=str(storage_path),
        status=DocumentStatus.UPLOADED,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    background_tasks.add_task(_process_in_background, document.id)
    return document


def _process_in_background(document_id: str) -> None:
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        process_document(db, document_id)
    finally:
        db.close()


@router.get("", response_model=DocumentListResponse, summary="List the current user's documents")
def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    status_filter: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Document).filter(Document.owner_id == current_user.id)
    if search:
        q = q.filter(Document.original_filename.ilike(f"%{search}%"))
    if status_filter:
        q = q.filter(Document.status == status_filter)
    total = q.count()
    items = (
        q.order_by(Document.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return DocumentListResponse(items=items, total=total, page=page, page_size=page_size)


def _get_owned_document(db: Session, document_id: str, user: User) -> Document:
    document = db.get(Document, document_id)
    if document is None or document.owner_id != user.id:
        # Same error whether missing or owned by someone else -- avoids
        # leaking which document IDs exist to other users.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return document


@router.get("/{document_id}", response_model=DocumentResponse, summary="Get a document")
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_owned_document(db, document_id, current_user)


@router.get(
    "/{document_id}/status", response_model=DocumentStatusResponse, summary="Get processing status"
)
def get_document_status(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = _get_owned_document(db, document_id, current_user)
    return DocumentStatusResponse(
        id=document.id,
        status=document.status,
        error_message=document.error_message,
        chunk_count=document.chunk_count,
        page_count=document.page_count,
    )


@router.delete(
    "/{document_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a document"
)
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = _get_owned_document(db, document_id, current_user)

    get_vector_store().delete_by_document(current_user.id, document.id)
    db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete()

    try:
        Path(document.storage_path).unlink(missing_ok=True)
    except OSError:
        pass

    db.delete(document)
    db.commit()
    return None
