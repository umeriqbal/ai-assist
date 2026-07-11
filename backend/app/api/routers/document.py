from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import (
    get_chunking_service,
    get_document_service,
    get_embedding_service,
    get_vector_store_service,
)
from app.schemas.document import (
    ChunkRequest,
    ChunkResponse,
    DocumentCreateRequest,
    DocumentResponse,
    EmbedRequest,
    EmbeddedChunkResponse,
    EmbedResponse,
    IndexRequest,
    IndexResponse,
    SearchRequest,
    SearchResponse,
    SearchResultResponse,
)
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
)
async def create_document(
    request: DocumentCreateRequest,
    service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:

    try:
        document = await service.create_document(
            text=request.text,
            source=request.source,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return DocumentResponse(
        content=document.page_content,
        metadata=document.metadata,
    )


@router.post(
    "/chunks",
    response_model=ChunkResponse,
)
async def chunk_document(
    request: ChunkRequest,
    service: ChunkingService = Depends(get_chunking_service),
) -> ChunkResponse:

    try:
        chunks = await service.chunk_text(
            text=request.text,
            source=request.source,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ChunkResponse(
        chunks=[
            DocumentResponse(
                content=chunk.page_content,
                metadata=chunk.metadata,
            )
            for chunk in chunks
        ],
        chunk_count=len(chunks),
    )


@router.post(
    "/embeddings",
    response_model=EmbedResponse,
)
async def embed_document(
    request: EmbedRequest,
    chunking_service: ChunkingService = Depends(get_chunking_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> EmbedResponse:

    try:
        chunks = await chunking_service.chunk_text(
            text=request.text,
            source=request.source,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    embedded_chunks = await embedding_service.embed_chunks(chunks)

    return EmbedResponse(
        chunks=[
            EmbeddedChunkResponse(
                content=embedded_chunk.document.page_content,
                metadata=embedded_chunk.document.metadata,
                embedding=embedded_chunk.vector,
                embedding_dimensions=len(embedded_chunk.vector),
            )
            for embedded_chunk in embedded_chunks
        ],
        chunk_count=len(embedded_chunks),
    )


@router.post(
    "/index",
    response_model=IndexResponse,
)
async def index_document(
    request: IndexRequest,
    service: VectorStoreService = Depends(get_vector_store_service),
) -> IndexResponse:

    try:
        chunk_count = await service.index_text(
            text=request.text,
            source=request.source,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return IndexResponse(chunk_count=chunk_count)


@router.post(
    "/search",
    response_model=SearchResponse,
)
async def search_documents(
    request: SearchRequest,
    service: VectorStoreService = Depends(get_vector_store_service),
) -> SearchResponse:

    try:
        results = await service.search(
            query=request.query,
            k=request.k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SearchResponse(
        results=[
            SearchResultResponse(
                content=result.document.page_content,
                metadata=result.document.metadata,
                score=result.score,
            )
            for result in results
        ],
        result_count=len(results),
    )
