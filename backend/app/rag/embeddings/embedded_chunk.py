from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class EmbeddedChunk:
    """
    A chunk paired with its embedding vector.
    """

    document: Document
    vector: list[float]
