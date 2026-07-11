import asyncio

import pytest

from app.services.document_service import DocumentService


def test_create_document_returns_document_with_metadata():
    service = DocumentService()

    document = asyncio.run(
        service.create_document(
            text="Enterprise AI Assistant",
            source="unit-test",
        )
    )

    assert document.page_content == "Enterprise AI Assistant"
    assert document.metadata["source"] == "unit-test"
    assert "created_at" in document.metadata


def test_create_document_strips_whitespace():
    service = DocumentService()

    document = asyncio.run(
        service.create_document(text="   padded text   ")
    )

    assert document.page_content == "padded text"


def test_create_document_rejects_empty_text():
    service = DocumentService()

    with pytest.raises(ValueError):
        asyncio.run(service.create_document(text="   "))
