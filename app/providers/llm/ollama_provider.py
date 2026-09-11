import logging
from functools import lru_cache

import httpx

from app.core.config import get_settings
from app.providers.llm.base import LLMProvider

logger = logging.getLogger(__name__)
settings = get_settings()


class OllamaProvider(LLMProvider):
    """Talks to a locally running Ollama instance (https://ollama.com).
    Fully free/local -- no API key required. Install with:
        curl -fsSL https://ollama.com/install.sh | sh
        ollama pull llama3.1
    """

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.LLM_BASE_URL).rstrip("/")
        self.model = model or settings.LLM_MODEL

    def is_available(self) -> bool:
        try:
            r = httpx.get(f"{self.base_url}/api/tags", timeout=3.0)
            return r.status_code == 200
        except Exception as exc:  # pragma: no cover - depends on env
            logger.info("Ollama not reachable at %s: %s", self.base_url, exc)
            return False

    def generate(self, prompt: str, system: str | None = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system or "",
            "stream": False,
        }
        try:
            resp = httpx.post(
                f"{self.base_url}/api/generate", json=payload, timeout=120.0
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as exc:
            raise RuntimeError(f"LLM generation failed: {exc}") from exc


class NullLLMProvider(LLMProvider):
    """Explicit 'no LLM configured' provider. Never fabricates an answer."""

    def is_available(self) -> bool:
        return False

    def generate(self, prompt: str, system: str | None = None) -> str:
        raise RuntimeError("No LLM provider is configured or reachable.")


@lru_cache
def get_llm_provider() -> LLMProvider:
    if settings.LLM_PROVIDER == "ollama":
        return OllamaProvider()
    return NullLLMProvider()
