from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import get_question_answering_service
from app.schemas.qa import AskRequest, AskResponse
from app.services.question_answering_service import QuestionAnsweringService

router = APIRouter(
    tags=["Question Answering"],
)


@router.post(
    "/ask",
    response_model=AskResponse,
)
async def ask(
    request: AskRequest,
    service: QuestionAnsweringService = Depends(get_question_answering_service),
) -> AskResponse:

    try:
        result = await service.answer(
            question=request.question,
            k=request.k,
            source=request.source,
            min_score=request.min_score,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AskResponse(
        answer=result.answer,
        sources=result.sources,
        chunks_used=result.chunks_used,
    )
