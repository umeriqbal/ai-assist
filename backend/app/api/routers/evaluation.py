from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import get_evaluation_service, get_faithfulness_service
from app.schemas.evaluation import (
    EvaluateFaithfulnessRequest,
    EvaluateFaithfulnessResponse,
    EvaluateRetrievalRequest,
    EvaluateRetrievalResponse,
    EvaluationCaseResultResponse,
)
from app.services.evaluation_service import EvaluationCase, EvaluationService
from app.services.faithfulness_service import FaithfulnessService

router = APIRouter(
    prefix="/evaluate",
    tags=["Evaluation"],
)


@router.post(
    "/retrieval",
    response_model=EvaluateRetrievalResponse,
)
async def evaluate_retrieval(
    request: EvaluateRetrievalRequest,
    service: EvaluationService = Depends(get_evaluation_service),
) -> EvaluateRetrievalResponse:

    cases = [
        EvaluationCase(
            question=case.question,
            expected_sources=case.expected_sources,
        )
        for case in request.cases
    ]

    try:
        report = await service.evaluate_retrieval(
            cases=cases,
            k=request.k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return EvaluateRetrievalResponse(
        results=[
            EvaluationCaseResultResponse(
                question=result.question,
                expected_sources=result.expected_sources,
                retrieved_sources=result.retrieved_sources,
                recall=result.recall,
                precision=result.precision,
            )
            for result in report.results
        ],
        mean_recall=report.mean_recall,
        mean_precision=report.mean_precision,
        case_count=len(report.results),
    )


@router.post(
    "/faithfulness",
    response_model=EvaluateFaithfulnessResponse,
)
async def evaluate_faithfulness(
    request: EvaluateFaithfulnessRequest,
    service: FaithfulnessService = Depends(get_faithfulness_service),
) -> EvaluateFaithfulnessResponse:

    try:
        result = await service.evaluate(
            question=request.question,
            k=request.k,
            source=request.source,
            min_score=request.min_score,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return EvaluateFaithfulnessResponse(
        question=result.question,
        answer=result.answer,
        is_faithful=result.is_faithful,
        unsupported_claims=result.unsupported_claims,
        raw_verdict=result.raw_verdict,
    )
