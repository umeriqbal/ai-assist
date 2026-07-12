import asyncio

import pytest

from app.agents.reflector import Reflector
from app.providers.chat_result import ChatResult
from app.services.agent_service import AgentService
from app.services.reflection_service import ReflectionService
from app.tools.echo_tool import EchoTool
from tests.conftest import FakeLLMProvider


def _service(provider: FakeLLMProvider, max_iterations: int = 3) -> ReflectionService:
    return ReflectionService(
        agent_service=AgentService(provider=provider, tools=[EchoTool()]),
        reflector=Reflector(provider=provider),
        max_iterations=max_iterations,
    )


def test_run_returns_first_answer_when_immediately_satisfactory():
    provider = FakeLLMProvider(
        chat_with_tools_results=[ChatResult(output_text="draft answer")],
        structured_results=[{"is_satisfactory": True, "feedback": "looks good"}],
    )
    service = _service(provider)

    result = asyncio.run(service.run("What is X?"))

    assert result.answer == "draft answer"
    assert len(result.drafts) == 1
    assert result.drafts[0].was_satisfactory is True
    assert len(provider.chat_with_tools_calls) == 1


def test_run_revises_once_then_stops_when_satisfied():
    provider = FakeLLMProvider(
        chat_with_tools_results=[
            ChatResult(output_text="draft one"),
            ChatResult(output_text="draft two"),
        ],
        structured_results=[
            {"is_satisfactory": False, "feedback": "missing X"},
            {"is_satisfactory": True, "feedback": "now good"},
        ],
    )
    service = _service(provider)

    result = asyncio.run(service.run("What is X?"))

    assert result.answer == "draft two"
    assert len(result.drafts) == 2
    assert result.drafts[0].was_satisfactory is False
    assert result.drafts[1].was_satisfactory is True

    revision_messages, _ = provider.chat_with_tools_calls[1]
    assert "missing X" in revision_messages[0]["content"]
    assert "draft one" in revision_messages[0]["content"]


def test_run_stops_at_iteration_limit_without_raising():
    provider = FakeLLMProvider(
        chat_with_tools_results=[
            ChatResult(output_text="draft zero"),
            ChatResult(output_text="draft one"),
            ChatResult(output_text="draft two"),
        ],
        structured_results=[
            {"is_satisfactory": False, "feedback": "f1"},
            {"is_satisfactory": False, "feedback": "f2"},
        ],
    )
    service = _service(provider, max_iterations=2)

    result = asyncio.run(service.run("What is X?"))

    assert result.answer == "draft two"
    assert len(result.drafts) == 2
    assert len(provider.chat_with_tools_calls) == 3
    assert len(provider.generate_structured_calls) == 2


def test_run_rejects_empty_question():
    service = _service(FakeLLMProvider())

    with pytest.raises(ValueError):
        asyncio.run(service.run("   "))
