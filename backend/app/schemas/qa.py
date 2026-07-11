from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """
    Incoming grounded question-answering request.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    k: int = Field(
        default=4,
        ge=1,
        le=20,
    )

    source: str | None = Field(
        default=None,
        max_length=200,
        description="Restrict retrieval to chunks indexed with this source.",
    )

    min_score: float | None = Field(
        default=None,
        ge=-1.0,
        le=1.0,
        description="Discard retrieved chunks scoring below this similarity threshold.",
    )


class AskResponse(BaseModel):
    """
    A grounded answer returned to the client.
    """

    answer: str
    sources: list[str]
    chunks_used: int
