import asyncio

from app.agents.reflector import Reflector
from tests.conftest import FakeLLMProvider


def test_critique_returns_parsed_result():
    provider = FakeLLMProvider(
        structured_results=[{"is_satisfactory": False, "feedback": "missing detail"}]
    )
    reflector = Reflector(provider=provider)

    critique = asyncio.run(reflector.critique("What is X?", "X is a thing."))

    assert critique.is_satisfactory is False
    assert critique.feedback == "missing detail"


def test_critique_sends_question_and_answer_in_the_prompt():
    provider = FakeLLMProvider(
        structured_results=[{"is_satisfactory": True, "feedback": "good"}]
    )
    reflector = Reflector(provider=provider)

    asyncio.run(reflector.critique("What is X?", "X is a thing."))

    prompt, _, schema_name = provider.generate_structured_calls[0]
    assert "What is X?" in prompt
    assert "X is a thing." in prompt
    assert schema_name == "critique"
