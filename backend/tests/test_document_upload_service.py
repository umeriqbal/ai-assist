import asyncio

from app.rag.document_ingestion_service import DocumentIngestionService
from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.document_upload_service import DocumentUploadService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from tests.conftest import FakeEmbeddingModel, write_minimal_pdf


def _service() -> DocumentUploadService:
    vector_store = InMemoryVectorStore()

    return DocumentUploadService(
        ingestion_service=DocumentIngestionService(),
        vector_store_service=VectorStoreService(
            chunking_service=ChunkingService(document_service=DocumentService()),
            embedding_service=EmbeddingService(embedding_model=FakeEmbeddingModel()),
            vector_store=vector_store,
        ),
    )


def test_upload_ingests_and_indexes_a_real_pdf(tmp_path):
    pdf_path = tmp_path / "policy.pdf"
    write_minimal_pdf(pdf_path, "Employees get 25 vacation days")

    service = _service()

    result = asyncio.run(
        service.upload(file_path=pdf_path, source="hr-policy.pdf")
    )

    assert result.source == "hr-policy.pdf"
    assert result.pages_loaded == 1
    assert result.chunks_indexed >= 1


def test_upload_overrides_metadata_source_with_the_given_name(tmp_path):
    pdf_path = tmp_path / "original-temp-name.pdf"
    write_minimal_pdf(pdf_path, "some content")

    vector_store = InMemoryVectorStore()
    embedding_model = FakeEmbeddingModel()
    service = DocumentUploadService(
        ingestion_service=DocumentIngestionService(),
        vector_store_service=VectorStoreService(
            chunking_service=ChunkingService(document_service=DocumentService()),
            embedding_service=EmbeddingService(embedding_model=embedding_model),
            vector_store=vector_store,
        ),
    )

    asyncio.run(service.upload(file_path=pdf_path, source="friendly-name.pdf"))

    query_vector = asyncio.run(embedding_model.embed_query("anything"))
    results = asyncio.run(vector_store.similarity_search(query_vector, k=1))

    assert results[0].document.metadata["source"] == "friendly-name.pdf"
    assert "created_at" in results[0].document.metadata
    assert "page" in results[0].document.metadata
