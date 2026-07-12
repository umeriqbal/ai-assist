from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import get_agent_service, get_planning_service
from app.schemas.agent import (
    AgentChatRequest,
    AgentChatResponse,
    PlanRequest,
    PlanResponse,
)
from app.services.agent_service import AgentService
from app.services.planning_service import PlanningService

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post(
    "/chat",
    response_model=AgentChatResponse,
)
async def agent_chat(
    request: AgentChatRequest,
    service: AgentService = Depends(get_agent_service),
) -> AgentChatResponse:

    response = await service.chat(
        request.prompt,
    )

    return AgentChatResponse(
        response=response,
    )


@router.post(
    "/plan",
    response_model=PlanResponse,
)
async def agent_plan(
    request: PlanRequest,
    service: PlanningService = Depends(get_planning_service),
) -> PlanResponse:

    try:
        result = await service.run(request.goal)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PlanResponse(
        goal=result.plan.goal,
        steps=[step.description for step in result.plan.steps],
        step_results=result.step_results,
        answer=result.answer,
    )
