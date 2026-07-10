from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.embedding_provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    OpenAI implementation of the EmbeddingProvider interface.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        response = await self._client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
        )

        return response.data[0].embedding

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        response = await self._client.embeddings.create(
            model=settings.openai_embedding_model,
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]