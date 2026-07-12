import asyncio

from app.providers.chat_result import ChatResult
from app.providers.tool_call import ToolCall
from app.tools.echo_tool import EchoTool
from tests.conftest import FakeLLMProvider


def test_chat_with_tools_defaults_to_a_plain_text_result():
    provider = FakeLLMProvider(response="hello")

    result = asyncio.run(
        provider.chat_with_tools(
            messages=[{"role": "user", "content": "hi"}],
            tools=[EchoTool()],
        )
    )

    assert result.output_text == "hello"
    assert result.has_tool_calls is False


def test_chat_with_tools_can_return_a_requested_tool_call():
    scripted = ChatResult(
        output_text=None,
        tool_calls=[ToolCall(id="call_1", name="echo", arguments={"text": "hi"})],
    )
    provider = FakeLLMProvider(chat_with_tools_results=[scripted])

    result = asyncio.run(
        provider.chat_with_tools(
            messages=[{"role": "user", "content": "say hi via the echo tool"}],
            tools=[EchoTool()],
        )
    )

    assert result.has_tool_calls is True
    assert result.tool_calls[0].name == "echo"
    assert result.tool_calls[0].arguments == {"text": "hi"}


def test_chat_with_tools_records_messages_and_tools_passed_in():
    provider = FakeLLMProvider()
    messages = [{"role": "user", "content": "hi"}]
    tools = [EchoTool()]

    asyncio.run(provider.chat_with_tools(messages=messages, tools=tools))

    recorded_messages, recorded_tools = provider.chat_with_tools_calls[0]
    assert recorded_messages == messages
    assert recorded_tools == tools
