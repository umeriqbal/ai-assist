from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class ScoredChunk:
    """
    A chunk returned from similarity search, paired with its
    cosine similarity score against the query (higher is more similar).
    """

    document: Document
    score: float
