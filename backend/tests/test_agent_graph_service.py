import asyncio

import pytest

from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.services.agent_graph_service import AgentGraphService
from app.tools.echo_tool import EchoTool
from tests.conftest import FakeLLMProvider


def test_chat_returns_text_answer_when_no_tool_is_needed():
    provider = FakeLLMProvider(response="hello there")
    service = AgentGraphService(provider=provider, tools=[EchoTool()])

    answer = asyncio.run(service.chat("hi", conversation_id="c1"))

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
    service = AgentGraphService(provider=provider, tools=[EchoTool()])

    answer = asyncio.run(service.chat("echo hi", conversation_id="c1"))

    assert answer == "the echo tool said: hi"


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
    service = AgentGraphService(provider=provider, tools=[EchoTool()])

    answer = asyncio.run(service.chat("do something unsupported", conversation_id="c1"))

    assert answer == "handled the error"


def test_chat_raises_when_iteration_limit_is_exceeded():
    always_calls_tool = ChatResult(
        tool_calls=[ToolCall(id="call_1", name="echo", arguments={"text": "hi"})]
    )
    provider = FakeLLMProvider(chat_with_tools_results=[always_calls_tool] * 20)
    service = AgentGraphService(provider=provider, tools=[EchoTool()], max_iterations=2)

    with pytest.raises(RuntimeError):
        asyncio.run(service.chat("loop forever", conversation_id="c1"))


def test_chat_remembers_prior_turns_under_the_same_conversation_id():
    provider = FakeLLMProvider(response="an answer")
    service = AgentGraphService(provider=provider, tools=[EchoTool()])

    asyncio.run(service.chat("first question", conversation_id="c1"))
    asyncio.run(service.chat("second question", conversation_id="c1"))

    second_call_messages, _ = provider.chat_with_tools_calls[1]
    contents = [m["content"] for m in second_call_messages]
    assert "first question" in contents
    assert "second question" in contents


def test_chat_does_not_leak_history_across_different_conversation_ids():
    provider = FakeLLMProvider(response="an answer")
    service = AgentGraphService(provider=provider, tools=[EchoTool()])

    asyncio.run(service.chat("first question", conversation_id="c1"))
    asyncio.run(service.chat("unrelated question", conversation_id="c2"))

    second_call_messages, _ = provider.chat_with_tools_calls[1]
    contents = [m["content"] for m in second_call_messages]
    assert contents == ["unrelated question"]
