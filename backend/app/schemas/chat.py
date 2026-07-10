from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat request.
    """

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class ChatResponse(BaseModel):
    """
    Chat response returned to the client.
    """

    response: str