from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    """
    Incoming agent chat request.
    """

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class AgentChatResponse(BaseModel):
    """
    Agent chat response returned to the client.
    """

    response: str


class PlanRequest(BaseModel):
    """
    Incoming plan-and-execute request.
    """

    goal: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class PlanResponse(BaseModel):
    """
    Plan-and-execute response returned to the client.
    """

    goal: str
    steps: list[str]
    step_results: list[str]
    answer: str
