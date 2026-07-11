from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import get_chunking_service, get_document_service
from app.schemas.document import (
    ChunkRequest,
    ChunkResponse,
    DocumentCreateRequest,
    DocumentResponse,
)
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService

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
