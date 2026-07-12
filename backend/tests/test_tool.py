import asyncio

from app.tools.echo_tool import EchoTool


def test_echo_tool_exposes_name_and_description():
    tool = EchoTool()

    assert tool.name == "echo"
    assert tool.description


def test_echo_tool_parameters_declare_required_text_argument():
    tool = EchoTool()

    assert tool.parameters["type"] == "object"
    assert "text" in tool.parameters["properties"]
    assert tool.parameters["required"] == ["text"]


def test_echo_tool_execute_returns_input_unchanged():
    tool = EchoTool()

    result = asyncio.run(tool.execute(text="hello"))

    assert result == "hello"
