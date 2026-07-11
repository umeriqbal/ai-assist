from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import get_document_service
from app.schemas.document import DocumentCreateRequest, DocumentResponse
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
