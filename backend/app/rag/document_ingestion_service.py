from pathlib import Path

from langchain_core.documents import Document

from app.rag.loaders.loader_factory import (
    DocumentLoaderFactory,
)


class DocumentIngestionService:
    """
    Coordinates document ingestion.

    This service delegates file loading to the appropriate
    document loader selected by the factory.
    """

    def __init__(
        self,
        loader_factory: DocumentLoaderFactory | None = None,
    ) -> None:
        self._loader_factory = (
            loader_factory or DocumentLoaderFactory()
        )

    async def ingest(
        self,
        file_path: str | Path,
    ) -> list[Document]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        loader = self._loader_factory.get_loader(path)

        return await loader.load(path)