from langchain_core.documents import Document


class DocumentFactory:

    @staticmethod
    def create(
        text: str,
        metadata: dict | None = None
    ) -> Document:

        return Document(
            page_content=text,
            metadata=metadata or {}
        )