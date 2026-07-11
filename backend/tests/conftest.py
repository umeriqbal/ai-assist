from collections.abc import AsyncIterator

from app.providers.base import LLMProvider
from app.rag.embeddings.embedding_model import EmbeddingModel


class FakeEmbeddingModel(EmbeddingModel):
    """
    Deterministic, network-free stand-in for OpenAIEmbeddingModel.
    """

    def __init__(self, dimensions: int = 8) -> None:
        self.dimensions = dimensions
        self.embed_documents_calls: list[list[str]] = []

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.embed_documents_calls.append(texts)
        return [[float(len(text))] * self.dimensions for text in texts]

    async def embed_query(self, text: str) -> list[float]:
        return [float(len(text))] * self.dimensions


class FakeLLMProvider(LLMProvider):
    """
    Deterministic, network-free stand-in for OpenAIProvider.
    """

    def __init__(self, response: str = "fake answer") -> None:
        self.response = response
        self.chat_calls: list[str] = []

    async def health_check(self) -> bool:
        return True

    async def chat(self, prompt: str) -> str:
        self.chat_calls.append(prompt)
        return self.response

    async def stream_chat(self, prompt: str) -> AsyncIterator[str]:
        for token in self.response.split():
            yield token
