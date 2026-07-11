from langchain_core.documents import Document

from app.rag.prompts.prompt_builder import PromptBuilder


def test_build_includes_the_question():
    prompt = PromptBuilder.build(
        question="How much vacation do employees get?",
        documents=[Document(page_content="25 days per year.")],
    )

    assert "How much vacation do employees get?" in prompt


def test_build_includes_all_chunk_contents():
    documents = [
        Document(page_content="First chunk content."),
        Document(page_content="Second chunk content."),
    ]

    prompt = PromptBuilder.build(question="anything", documents=documents)

    assert "First chunk content." in prompt
    assert "Second chunk content." in prompt


def test_build_labels_each_chunk_with_its_source():
    documents = [
        Document(page_content="Policy text.", metadata={"source": "hr-policy.txt"}),
    ]

    prompt = PromptBuilder.build(question="anything", documents=documents)

    assert "hr-policy.txt" in prompt


def test_build_instructs_the_model_to_use_only_the_context():
    prompt = PromptBuilder.build(
        question="anything",
        documents=[Document(page_content="content")],
    )

    assert "ONLY" in prompt
    assert "don't know" in prompt
