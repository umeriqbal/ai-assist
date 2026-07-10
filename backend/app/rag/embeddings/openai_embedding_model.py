from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.rag.embeddings.embedding_model import EmbeddingModel


class OpenAIEmbeddingModel(EmbeddingModel):
    """
    OpenAI implementation of the embedding model interface.
    """

    def __init__(self) -> None:
        self._embeddings = OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.openai_embedding_model,
        )

    def get_embeddings(self) -> Embeddings:
        return self._embeddings