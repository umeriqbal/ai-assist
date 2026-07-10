from langchain_core.documents import Document

from app.providers.embedding_provider import EmbeddingProvider
from app.rag.document_service import DocumentService
from app.rag.text_splitter import DocumentTextSplitter
from app.rag.vector_store import VectorStore


class RAGService:
    """
    Coordinates the complete Retrieval-Augmented Generation workflow.

    Responsibilities:
    - Create LangChain Documents
    - Split documents into chunks
    - Generate embeddings
    - Store vectors
    - Perform semantic search
    """

    def __init__(
        self,
        document_service: DocumentService,
        text_splitter: DocumentTextSplitter,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._document_service = document_service
        self._text_splitter = text_splitter
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    async def ingest_document(
        self,
        text: str,
        metadata: dict | None = None,
    ) -> int:
        """
        Ingest a document into the vector store.

        Returns:
            Number of chunks stored.
        """

        document = await self._document_service.create_document(
            text=text,
            metadata=metadata,
        )

        chunks = self._text_splitter.split(document)

        embeddings = await self._embedding_provider.embed_batch(
            [
                chunk.page_content
                for chunk in chunks
            ]
        )

        await self._vector_store.add_documents(
            documents=chunks,
            embeddings=embeddings,
        )

        return len(chunks)

    async def search(
        self,
        query: str,
        k: int = 5,
    ) -> list[Document]:
        """
        Perform semantic search.
        """

        query_embedding = await self._embedding_provider.embed(
            query,
        )

        return await self._vector_store.similarity_search(
            embedding=query_embedding,
            k=k,
        )