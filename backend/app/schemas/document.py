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


class ChunkRequest(BaseModel):
    """
    Incoming request to create and chunk a Document.
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

    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=8000,
    )

    chunk_overlap: int = Field(
        default=200,
        ge=0,
        le=4000,
    )


class ChunkResponse(BaseModel):
    """
    Chunked Documents returned to the client.
    """

    chunks: list[DocumentResponse]
    chunk_count: int


class EmbedRequest(ChunkRequest):
    """
    Incoming request to create, chunk, and embed a Document.
    """


class EmbeddedChunkResponse(BaseModel):
    """
    A single embedded chunk returned to the client.
    """

    content: str
    metadata: dict
    embedding: list[float]
    embedding_dimensions: int


class EmbedResponse(BaseModel):
    """
    Embedded chunks returned to the client.
    """

    chunks: list[EmbeddedChunkResponse]
    chunk_count: int
