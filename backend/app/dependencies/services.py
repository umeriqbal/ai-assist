from functools import lru_cache

from app.agents.planner import Planner
from app.agents.reflector import Reflector
from app.dependencies.llm import (
    get_conversation_memory,
    get_embedding_model,
    get_openai_provider,
    get_vector_store,
)
from app.rag.document_ingestion_service import DocumentIngestionService
from app.rag.loaders.loader_factory import DocumentLoaderFactory
from app.services.agent_graph_service import AgentGraphService
from app.services.agent_service import AgentService
from app.services.chat_service import ChatService
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.document_upload_service import DocumentUploadService
from app.services.embedding_service import EmbeddingService
from app.services.evaluation_service import EvaluationService
from app.services.faithfulness_service import FaithfulnessService
from app.services.planning_service import PlanningService
from app.services.question_answering_service import QuestionAnsweringService
from app.services.reflection_service import ReflectionService
from app.services.retrieval_service import RetrievalService
from app.services.streaming_service import StreamingService
from app.services.vector_store_service import VectorStoreService
from app.tools.knowledge_base_search_tool import KnowledgeBaseSearchTool


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(
        provider=get_openai_provider(),
    )


@lru_cache
def get_streaming_service() -> StreamingService:
    return StreamingService(
        provider=get_openai_provider(),
    )


@lru_cache
def get_document_service() -> DocumentService:
    return DocumentService()


@lru_cache
def get_chunking_service() -> ChunkingService:
    return ChunkingService(
        document_service=get_document_service(),
    )


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(
        embedding_model=get_embedding_model(),
    )


@lru_cache
def get_vector_store_service() -> VectorStoreService:
    return VectorStoreService(
        chunking_service=get_chunking_service(),
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


@lru_cache
def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


@lru_cache
def get_question_answering_service() -> QuestionAnsweringService:
    return QuestionAnsweringService(
        retrieval_service=get_retrieval_service(),
        llm_provider=get_openai_provider(),
    )


@lru_cache
def get_document_ingestion_service() -> DocumentIngestionService:
    return DocumentIngestionService(
        loader_factory=DocumentLoaderFactory(),
    )


@lru_cache
def get_document_upload_service() -> DocumentUploadService:
    return DocumentUploadService(
        ingestion_service=get_document_ingestion_service(),
        vector_store_service=get_vector_store_service(),
    )


@lru_cache
def get_evaluation_service() -> EvaluationService:
    return EvaluationService(
        retrieval_service=get_retrieval_service(),
    )


@lru_cache
def get_faithfulness_service() -> FaithfulnessService:
    return FaithfulnessService(
        question_answering_service=get_question_answering_service(),
        llm_provider=get_openai_provider(),
    )


@lru_cache
def get_knowledge_base_search_tool() -> KnowledgeBaseSearchTool:
    return KnowledgeBaseSearchTool(
        retrieval_service=get_retrieval_service(),
    )


@lru_cache
def get_agent_service() -> AgentService:
    return AgentService(
        provider=get_openai_provider(),
        tools=[get_knowledge_base_search_tool()],
        memory=get_conversation_memory(),
    )


@lru_cache
def get_agent_graph_service() -> AgentGraphService:
    return AgentGraphService(
        provider=get_openai_provider(),
        tools=[get_knowledge_base_search_tool()],
    )


@lru_cache
def get_planner() -> Planner:
    return Planner(
        provider=get_openai_provider(),
    )


@lru_cache
def get_planning_service() -> PlanningService:
    return PlanningService(
        planner=get_planner(),
        agent_service=get_agent_service(),
        provider=get_openai_provider(),
    )


@lru_cache
def get_reflector() -> Reflector:
    return Reflector(
        provider=get_openai_provider(),
    )


@lru_cache
def get_reflection_service() -> ReflectionService:
    return ReflectionService(
        agent_service=get_agent_service(),
        reflector=get_reflector(),
    )