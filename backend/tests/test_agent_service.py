import asyncio

import pytest

from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.services.agent_service import AgentService
from app.tools.echo_tool import EchoTool
from tests.conftest import FakeLLMProvider


def test_chat_returns_text_answer_when_no_tool_is_needed():
    provider = FakeLLMProvider(response="hello there")
    agent = AgentService(provider=provider, tools=[EchoTool()])

    answer = asyncio.run(agent.chat("hi"))

    assert answer == "hello there"


def test_chat_executes_requested_tool_and_returns_final_answer():
    provider = FakeLLMProvider(
        chat_with_tools_results=[
            ChatResult(
                tool_calls=[
                    ToolCall(id="call_1", name="echo", arguments={"text": "hi"})
                ]
            ),
            ChatResult(output_text="the echo tool said: hi"),
        ]
    )
    agent = AgentService(provider=provider, tools=[EchoTool()])

    answer = asyncio.run(agent.chat("echo hi"))

    assert answer == "the echo tool said: hi"
    assert len(provider.chat_with_tools_calls) == 2

    second_call_messages, _ = provider.chat_with_tools_calls[1]
    assert any(m.get("content") == "hi" for m in second_call_messages)


def test_chat_feeds_error_back_for_unknown_tool_instead_of_crashing():
    provider = FakeLLMProvider(
        chat_with_tools_results=[
            ChatResult(
                tool_calls=[
                    ToolCall(id="call_1", name="does_not_exist", arguments={})
                ]
            ),
            ChatResult(output_text="handled the error"),
        ]
    )
    agent = AgentService(provider=provider, tools=[EchoTool()])

    answer = asyncio.run(agent.chat("do something unsupported"))

    assert answer == "handled the error"

    second_call_messages, _ = provider.chat_with_tools_calls[1]
    assert any("unknown tool" in m.get("content", "") for m in second_call_messages)


def test_chat_raises_when_iteration_limit_is_exceeded():
    always_calls_tool = ChatResult(
        tool_calls=[ToolCall(id="call_1", name="echo", arguments={"text": "hi"})]
    )
    provider = FakeLLMProvider(
        chat_with_tools_results=[always_calls_tool] * 10,
    )
    agent = AgentService(provider=provider, tools=[EchoTool()], max_iterations=3)

    with pytest.raises(RuntimeError):
        asyncio.run(agent.chat("loop forever"))

    assert len(provider.chat_with_tools_calls) == 3
