from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...
