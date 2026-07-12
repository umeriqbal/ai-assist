from collections.abc import AsyncIterator
from typing import Any

from app.providers.base import LLMProvider
from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.rag.embeddings.embedding_model import EmbeddingModel
from app.tools.tool import Tool


class FakeEmbeddingModel(EmbeddingModel):
    """
    Deterministic, network-free stand-in for OpenAIEmbeddingModel.
    """

    def __init__(self, dimensions: int = 8) -> None:
        self.dimensions = dimensions
        self.embed_documents_calls: list[list[str]] = []

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.embed_documents_calls.append(texts)
        return [[float(len(text))] * self.dimensions for text in texts]

    async def embed_query(self, text: str) -> list[float]:
        return [float(len(text))] * self.dimensions


class FakeLLMProvider(LLMProvider):
    """
    Deterministic, network-free stand-in for OpenAIProvider.
    """

    def __init__(
        self,
        response: str = "fake answer",
        chat_with_tools_results: list[ChatResult] | None = None,
    ) -> None:
        self.response = response
        self.chat_calls: list[str] = []
        self._chat_with_tools_results = list(chat_with_tools_results or [])
        self.chat_with_tools_calls: list[
            tuple[list[dict[str, Any]], list[Tool]]
        ] = []

    async def health_check(self) -> bool:
        return True

    async def chat(self, prompt: str) -> str:
        self.chat_calls.append(prompt)
        return self.response

    async def stream_chat(self, prompt: str) -> AsyncIterator[str]:
        for token in self.response.split():
            yield token

    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[Tool],
    ) -> ChatResult:
        self.chat_with_tools_calls.append((messages, tools))

        if self._chat_with_tools_results:
            return self._chat_with_tools_results.pop(0)

        return ChatResult(output_text=self.response)

    def tool_result_messages(
        self,
        tool_call: ToolCall,
        result: str,
    ) -> list[dict[str, Any]]:
        return [
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.name,
                "content": result,
            }
        ]


_MINIMAL_PDF_TEMPLATE = """%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length {length} >>
stream
{content}
endstream
endobj
xref
0 6
0000000000 65535 f
trailer
<< /Size 6 /Root 1 0 R >>
startxref
0
%%EOF
"""


def write_minimal_pdf(path, text: str) -> None:
    """
    Write a minimal, hand-crafted single-page PDF containing `text`,
    readable by pypdf. Used to test PDF ingestion without depending
    on a PDF-generation library.
    """

    content = f"BT /F1 24 Tf 72 712 Td ({text}) Tj ET"
    pdf = _MINIMAL_PDF_TEMPLATE.format(length=len(content), content=content)
    path.write_bytes(pdf.encode())
