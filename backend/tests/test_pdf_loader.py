import asyncio

import pytest

from app.rag.loaders.document_loader import DocumentLoader
from app.rag.loaders.loader_factory import DocumentLoaderFactory
from app.rag.loaders.pdf_loader import PDFLoader
from tests.conftest import write_minimal_pdf


def test_pdf_loader_supports_pdf_extension():
    loader = PDFLoader()

    assert ".pdf" in loader.supported_extensions
    assert isinstance(loader, DocumentLoader)


def test_pdf_loader_extracts_text_from_a_real_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    write_minimal_pdf(pdf_path, "Hello PDF World")

    loader = PDFLoader()
    documents = asyncio.run(loader.load(pdf_path))

    assert len(documents) == 1
    assert "Hello PDF World" in documents[0].page_content
    assert documents[0].metadata["page"] == 0


def test_pdf_loader_rejects_missing_file():
    loader = PDFLoader()

    with pytest.raises(FileNotFoundError):
        asyncio.run(loader.load("/tmp/does-not-exist-12345.pdf"))


def test_loader_factory_selects_pdf_loader_for_pdf_extension():
    factory = DocumentLoaderFactory()

    loader = factory.get_loader("report.pdf")

    assert isinstance(loader, PDFLoader)


def test_loader_factory_rejects_unsupported_extension():
    factory = DocumentLoaderFactory()

    with pytest.raises(ValueError):
        factory.get_loader("report.docx")
