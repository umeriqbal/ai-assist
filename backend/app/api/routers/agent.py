import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.services import (
    get_agent_graph_service,
    get_agent_service,
    get_mcp_agent_service,
    get_multi_agent_service,
    get_planning_service,
    get_reflection_service,
)
from app.schemas.agent import (
    AgentChatRequest,
    AgentChatResponse,
    AgentTurnResponse,
    CollaborateRequest,
    CollaborateResponse,
    DraftResponse,
    PlanRequest,
    PlanResponse,
    ReflectRequest,
    ReflectResponse,
)
from app.services.agent_graph_service import AgentGraphService
from app.services.agent_service import AgentService
from app.services.multi_agent_service import MultiAgentService
from app.services.planning_service import PlanningService
from app.services.reflection_service import ReflectionService

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

    conversation_id = request.conversation_id or str(uuid.uuid4())

    try:
        response = await service.chat(
            request.prompt,
            conversation_id=conversation_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AgentChatResponse(
        response=response,
        conversation_id=conversation_id,
    )


@router.post(
    "/graph-chat",
    response_model=AgentChatResponse,
)
async def agent_graph_chat(
    request: AgentChatRequest,
    service: AgentGraphService = Depends(get_agent_graph_service),
) -> AgentChatResponse:

    conversation_id = request.conversation_id or str(uuid.uuid4())

    response = await service.chat(
        request.prompt,
        conversation_id=conversation_id,
    )

    return AgentChatResponse(
        response=response,
        conversation_id=conversation_id,
    )


@router.post(
    "/mcp-chat",
    response_model=AgentChatResponse,
)
async def agent_mcp_chat(
    request: AgentChatRequest,
    service: AgentService = Depends(get_mcp_agent_service),
) -> AgentChatResponse:

    conversation_id = request.conversation_id or str(uuid.uuid4())

    try:
        response = await service.chat(
            request.prompt,
            conversation_id=conversation_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AgentChatResponse(
        response=response,
        conversation_id=conversation_id,
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


@router.post(
    "/reflect",
    response_model=ReflectResponse,
)
async def agent_reflect(
    request: ReflectRequest,
    service: ReflectionService = Depends(get_reflection_service),
) -> ReflectResponse:

    try:
        result = await service.run(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReflectResponse(
        answer=result.answer,
        drafts=[
            DraftResponse(
                answer=draft.answer,
                feedback=draft.critique_feedback,
                was_satisfactory=draft.was_satisfactory,
            )
            for draft in result.drafts
        ],
    )


@router.post(
    "/collaborate",
    response_model=CollaborateResponse,
)
async def agent_collaborate(
    request: CollaborateRequest,
    service: MultiAgentService = Depends(get_multi_agent_service),
) -> CollaborateResponse:

    try:
        result = await service.run(request.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return CollaborateResponse(
        answer=result.answer,
        transcript=[
            AgentTurnResponse(agent=turn.agent, message=turn.message)
            for turn in result.transcript
        ],
    )
