"""SQLAlchemy engine/session setup. Works with SQLite (dev) or PostgreSQL (prod)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables directly (used for local/dev + tests).
    Production deployments should use Alembic migrations instead."""
    from app.models import user, document, chunk, conversation, message  # noqa: F401

    Base.metadata.create_all(bind=engine)
