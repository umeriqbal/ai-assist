from typing import Any

from app.services.retrieval_service import RetrievalService
from app.tools.tool import Tool


class KnowledgeBaseSearchTool(Tool):
    """
    Tool that lets an agent search the indexed knowledge base for
    context relevant to the user's question.
    """

    def __init__(self, retrieval_service: RetrievalService) -> None:
        self._retrieval_service = retrieval_service

    @property
    def name(self) -> str:
        return "search_knowledge_base"

    @property
    def description(self) -> str:
        return (
            "Search the indexed knowledge base for information relevant "
            "to a query. Use this when answering questions that may "
            "depend on the organization's documents rather than general "
            "knowledge."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query.",
                },
            },
            "required": ["query"],
        }

    async def execute(self, **kwargs: Any) -> str:

        results = await self._retrieval_service.retrieve(query=kwargs["query"])

        if not results:
            return "No relevant results found in the knowledge base."

        return "\n\n".join(
            f"Source: {chunk.document.metadata.get('source', 'unknown')}\n"
            f"{chunk.document.page_content}"
            for chunk in results
        )
