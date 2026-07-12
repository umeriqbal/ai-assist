from fastapi import APIRouter, Depends

from app.dependencies.services import get_agent_service
from app.schemas.agent import AgentChatRequest, AgentChatResponse
from app.services.agent_service import AgentService

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
