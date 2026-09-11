"""DocuMind CLI.

Usage:
    python -m app.cli health
    python -m app.cli reindex
    python -m app.cli create-admin --email admin@example.com --password changeme123
"""
import argparse
import sys

from app.core.security import hash_password
from app.db.session import SessionLocal, init_db
from app.models.document import Document, DocumentStatus
from app.models.user import User
from app.services.document_pipeline import process_document


def cmd_health(_args) -> int:
    from app.providers.embeddings.sentence_transformers_provider import get_embedding_provider
    from app.providers.llm.ollama_provider import get_llm_provider

    init_db()
    embed_ok = get_embedding_provider().is_available()
    llm_ok = get_llm_provider().is_available()
    print(f"database: ok")
    print(f"embedding_model: {'ok' if embed_ok else 'unavailable'}")
    print(f"llm: {'ok' if llm_ok else 'unavailable'}")
    return 0


def cmd_reindex(_args) -> int:
    init_db()
    db = SessionLocal()
    try:
        docs = db.query(Document).filter(Document.status != DocumentStatus.READY).all()
        print(f"Reindexing {len(docs)} document(s)...")
        for doc in docs:
            process_document(db, doc.id)
            print(f"  {doc.id} -> {doc.status}")
    finally:
        db.close()
    return 0


def cmd_create_admin(args) -> int:
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == args.email.lower()).first()
        if existing:
            print(f"User {args.email} already exists.")
            return 1
        user = User(
            email=args.email.lower(),
            full_name="Admin",
            hashed_password=hash_password(args.password),
        )
        db.add(user)
        db.commit()
        print(f"Created user {user.email} ({user.id})")
    finally:
        db.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("health", help="Check DB/embedding/LLM health").set_defaults(func=cmd_health)
    sub.add_parser("reindex", help="Reprocess all non-ready documents").set_defaults(
        func=cmd_reindex
    )

    p_admin = sub.add_parser("create-admin", help="Create a user account")
    p_admin.add_argument("--email", required=True)
    p_admin.add_argument("--password", required=True)
    p_admin.set_defaults(func=cmd_create_admin)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
