import asyncio

from app.rag.stores.in_memory_vector_store import InMemoryVectorStore
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService
from app.tools.knowledge_base_search_tool import KnowledgeBaseSearchTool
from tests.conftest import FakeEmbeddingModel


def _tool() -> tuple[VectorStoreService, KnowledgeBaseSearchTool]:
    embedding_service = EmbeddingService(embedding_model=FakeEmbeddingModel())
    vector_store = InMemoryVectorStore()

    indexer = VectorStoreService(
        chunking_service=ChunkingService(document_service=DocumentService()),
        embedding_service=embedding_service,
        vector_store=vector_store,
    )
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    return indexer, KnowledgeBaseSearchTool(retrieval_service=retrieval_service)


def test_tool_declares_a_required_query_argument():
    _, tool = _tool()

    assert tool.name == "search_knowledge_base"
    assert tool.parameters["required"] == ["query"]


def test_execute_returns_indexed_content_for_a_matching_query():
    indexer, tool = _tool()

    asyncio.run(
        indexer.index_text(
            text="The vacation policy allows 20 days per year.",
            source="hr-policy.txt",
        )
    )

    result = asyncio.run(tool.execute(query="vacation policy"))

    assert "vacation policy" in result
    assert "hr-policy.txt" in result


def test_execute_reports_no_results_when_nothing_indexed():
    _, tool = _tool()

    result = asyncio.run(tool.execute(query="anything"))

    assert result == "No relevant results found in the knowledge base."
