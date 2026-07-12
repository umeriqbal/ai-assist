import asyncio

import pytest

from app.agents.planner import Planner
from tests.conftest import FakeLLMProvider


def test_create_plan_returns_goal_and_parsed_steps():
    provider = FakeLLMProvider(
        structured_results=[
            {
                "steps": [
                    {"description": "Search the knowledge base for the policy"},
                    {"description": "Summarize the findings"},
                ]
            }
        ]
    )
    planner = Planner(provider=provider)

    plan = asyncio.run(planner.create_plan("Explain the vacation policy"))

    assert plan.goal == "Explain the vacation policy"
    assert len(plan.steps) == 2
    assert plan.steps[0].description == "Search the knowledge base for the policy"


def test_create_plan_uses_the_original_goal_even_if_model_would_diverge():
    provider = FakeLLMProvider(structured_results=[{"steps": []}])
    planner = Planner(provider=provider)

    plan = asyncio.run(planner.create_plan("  Explain the vacation policy  "))

    assert plan.goal == "Explain the vacation policy"


def test_create_plan_rejects_empty_goal():
    planner = Planner(provider=FakeLLMProvider())

    with pytest.raises(ValueError):
        asyncio.run(planner.create_plan("   "))


def test_create_plan_sends_goal_in_the_prompt():
    provider = FakeLLMProvider(structured_results=[{"steps": []}])
    planner = Planner(provider=provider)

    asyncio.run(planner.create_plan("Explain the vacation policy"))

    prompt, _, schema_name = provider.generate_structured_calls[0]
    assert "Explain the vacation policy" in prompt
    assert schema_name == "plan_steps"
