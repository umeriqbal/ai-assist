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
