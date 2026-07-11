"""
Prompt Builder

Formats a question and its retrieved context into a single prompt
string for an LLMProvider.

Responsibilities:
- Inject retrieved chunks as labeled context.
- Instruct the model to answer only from that context.

Does NOT:
- Call any LLM or embedding API
- Decide which chunks are relevant (that is retrieval/source selection)
"""

from langchain_core.documents import Document

_INSTRUCTIONS = (
    "You are an enterprise assistant. Answer the question using ONLY "
    "the context below. If the context does not contain the answer, "
    "say you don't know instead of guessing. Do not use any knowledge "
    "outside of the provided context."
)


class PromptBuilder:
    """
    Builds a grounded question-answering prompt.
    """

    @staticmethod
    def build(
        question: str,
        documents: list[Document],
    ) -> str:

        context_blocks = [
            f"[Source: {document.metadata.get('source', 'unknown')}]\n"
            f"{document.page_content}"
            for document in documents
        ]

        context = "\n\n".join(context_blocks)

        return (
            f"{_INSTRUCTIONS}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            f"Answer:"
        )
