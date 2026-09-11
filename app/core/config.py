"""Application configuration loaded from environment variables."""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "DocuMind"
    ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./documind.db"
    SECRET_KEY: str = Field(default="change-me-in-prod-please-min-32-chars")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    VECTOR_DB_PATH: str = "./data/chroma"
    UPLOAD_DIR: str = "./data/uploads"

    LLM_PROVIDER: str = "ollama"  # ollama | none
    LLM_MODEL: str = "llama3.1"
    LLM_BASE_URL: str = "http://localhost:11434"

    EMBEDDING_PROVIDER: str = "sentence_transformers"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024  # 20 MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx", "txt", "md"]

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000"

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.25

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
