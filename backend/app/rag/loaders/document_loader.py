from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document


class DocumentLoader(ABC):
    """
    Base interface for all document loaders.
    """

    @property
    @abstractmethod
    def supported_extensions(self) -> tuple[str, ...]:
        """
        File extensions supported by this loader.
        """
        raise NotImplementedError

    @abstractmethod
    async def load(
        self,
        file_path: str | Path,
    ) -> list[Document]:
        """
        Load a document and return LangChain Documents.
        """
        raise NotImplementedError