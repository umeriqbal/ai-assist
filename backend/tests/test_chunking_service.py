import asyncio

import pytest

from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService


def _service() -> ChunkingService:
    return ChunkingService(document_service=DocumentService())


def test_chunk_text_splits_long_text_into_multiple_chunks():
    service = _service()

    long_text = "word " * 1000

    chunks = asyncio.run(
        service.chunk_text(
            text=long_text,
            source="unit-test",
            chunk_size=200,
            chunk_overlap=20,
        )
    )

    assert len(chunks) > 1

    for index, chunk in enumerate(chunks):
        assert chunk.metadata["source"] == "unit-test"
        assert chunk.metadata["chunk_index"] == index
        assert chunk.metadata["chunk_count"] == len(chunks)
        assert "start_index" in chunk.metadata


def test_chunk_text_returns_single_chunk_for_short_text():
    service = _service()

    chunks = asyncio.run(
        service.chunk_text(
            text="short text",
            chunk_size=1000,
            chunk_overlap=200,
        )
    )

    assert len(chunks) == 1
    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[0].metadata["chunk_count"] == 1


def test_chunk_text_rejects_empty_text():
    service = _service()

    with pytest.raises(ValueError):
        asyncio.run(service.chunk_text(text="   "))


def test_chunk_text_rejects_overlap_larger_than_chunk_size():
    service = _service()

    with pytest.raises(ValueError):
        asyncio.run(
            service.chunk_text(
                text="some text",
                chunk_size=100,
                chunk_overlap=200,
            )
        )
