import asyncio

import pytest

from app.providers.chat_result import ChatResult
from app.services.agent_service import AgentService
from app.services.multi_agent_service import MultiAgentService
from app.tools.echo_tool import EchoTool
from tests.conftest import FakeLLMProvider


def _service(provider: FakeLLMProvider, max_iterations: int = 6) -> MultiAgentService:
    return MultiAgentService(
        provider=provider,
        researcher=AgentService(provider=provider, tools=[EchoTool()]),
        writer=AgentService(provider=provider, tools=[]),
        max_iterations=max_iterations,
    )


def test_run_routes_researcher_then_writer_then_finishes():
    provider = FakeLLMProvider(
        structured_results=[
            {"next": "researcher", "instructions": "find the fact"},
            {"next": "writer", "instructions": "write the answer"},
            {"next": "finish", "instructions": ""},
        ],
        chat_with_tools_results=[
            ChatResult(output_text="the fact is X"),
            ChatResult(output_text="Final answer: X"),
        ],
    )
    service = _service(provider)

    result = asyncio.run(service.run("What is the fact?"))

    assert result.answer == "Final answer: X"
    assert [t.agent for t in result.transcript] == ["researcher", "writer"]
    assert result.transcript[0].message == "the fact is X"
    assert result.transcript[1].message == "Final answer: X"


def test_run_rejects_empty_prompt():
    service = _service(FakeLLMProvider())

    with pytest.raises(ValueError):
        asyncio.run(service.run("   "))


def test_run_raises_when_iteration_limit_is_exceeded():
    provider = FakeLLMProvider(
        structured_results=[{"next": "researcher", "instructions": "loop"}] * 20,
        chat_with_tools_results=[ChatResult(output_text="result")] * 20,
    )
    service = _service(provider, max_iterations=2)

    with pytest.raises(RuntimeError):
        asyncio.run(service.run("loop forever"))
