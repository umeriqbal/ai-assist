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
