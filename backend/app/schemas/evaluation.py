from pydantic import BaseModel, Field


class EvaluationCaseRequest(BaseModel):
    """
    A single labeled retrieval test case.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    expected_sources: list[str] = Field(
        ...,
        min_length=1,
        description="Sources that should appear among the retrieved chunks.",
    )


class EvaluateRetrievalRequest(BaseModel):
    """
    Incoming request to evaluate retrieval quality against a labeled set.
    """

    cases: list[EvaluationCaseRequest] = Field(
        ...,
        min_length=1,
    )

    k: int = Field(
        default=4,
        ge=1,
        le=20,
    )


class EvaluationCaseResultResponse(BaseModel):
    """
    The outcome of one evaluation case.
    """

    question: str
    expected_sources: list[str]
    retrieved_sources: list[str]
    recall: float
    precision: float


class EvaluateRetrievalResponse(BaseModel):
    """
    Aggregate retrieval evaluation results returned to the client.
    """

    results: list[EvaluationCaseResultResponse]
    mean_recall: float
    mean_precision: float
    case_count: int


class EvaluateFaithfulnessRequest(BaseModel):
    """
    Incoming request to evaluate whether a generated answer is
    faithful to its retrieved context.
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
    )

    min_score: float | None = Field(
        default=None,
        ge=-1.0,
        le=1.0,
    )


class EvaluateFaithfulnessResponse(BaseModel):
    """
    Faithfulness evaluation results returned to the client.
    """

    question: str
    answer: str
    is_faithful: bool | None
    unsupported_claims: list[str]
    raw_verdict: str
