from app.rag.embeddings.embedding_model import EmbeddingModel
from app.rag.embeddings.openai_embedding_model import (
    OpenAIEmbeddingModel,
)


class EmbeddingModelFactory:
    """
    Factory responsible for creating embedding models.
    """

    @staticmethod
    def create() -> EmbeddingModel:
        return OpenAIEmbeddingModel()