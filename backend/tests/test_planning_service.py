import asyncio

from app.agents.planner import Planner
from app.providers.chat_result import ChatResult
from app.services.agent_service import AgentService
from app.services.planning_service import PlanningService
from app.tools.echo_tool import EchoTool
from tests.conftest import FakeLLMProvider


def _service(provider: FakeLLMProvider) -> PlanningService:
    return PlanningService(
        planner=Planner(provider=provider),
        agent_service=AgentService(provider=provider, tools=[EchoTool()]),
        provider=provider,
    )


def test_run_executes_each_step_and_synthesizes_a_final_answer():
    provider = FakeLLMProvider(
        response="final answer",
        structured_results=[
            {
                "steps": [
                    {"description": "step one"},
                    {"description": "step two"},
                ]
            }
        ],
        chat_with_tools_results=[
            ChatResult(output_text="result one"),
            ChatResult(output_text="result two"),
        ],
    )
    service = _service(provider)

    result = asyncio.run(service.run("Achieve the goal"))

    assert len(result.plan.steps) == 2
    assert result.step_results == ["result one", "result two"]
    assert result.answer == "final answer"

    synthesis_prompt = provider.chat_calls[0]
    assert "result one" in synthesis_prompt
    assert "result two" in synthesis_prompt


def test_run_with_no_steps_answers_directly_without_the_agent_loop():
    provider = FakeLLMProvider(
        response="direct answer",
        structured_results=[{"steps": []}],
    )
    service = _service(provider)

    result = asyncio.run(service.run("Trivial goal"))

    assert result.step_results == []
    assert result.answer == "direct answer"
    assert provider.chat_with_tools_calls == []
    assert provider.chat_calls[0] == "Trivial goal"


def test_later_steps_see_earlier_step_results():
    provider = FakeLLMProvider(
        response="final answer",
        structured_results=[
            {
                "steps": [
                    {"description": "step one"},
                    {"description": "step two"},
                ]
            }
        ],
        chat_with_tools_results=[
            ChatResult(output_text="result one"),
            ChatResult(output_text="result two"),
        ],
    )
    service = _service(provider)

    asyncio.run(service.run("Achieve the goal"))

    second_step_messages, _ = provider.chat_with_tools_calls[1]
    assert "result one" in second_step_messages[0]["content"]
