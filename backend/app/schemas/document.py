from pydantic import BaseModel, Field


class DocumentCreateRequest(BaseModel):
    """
    Incoming request to create a Document.
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=50000,
    )

    source: str = Field(
        default="manual-upload",
        max_length=200,
    )


class DocumentResponse(BaseModel):
    """
    Document returned to the client.
    """

    content: str
    metadata: dict
