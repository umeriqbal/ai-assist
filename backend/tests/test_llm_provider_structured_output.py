import asyncio

from tests.conftest import FakeLLMProvider


def test_generate_structured_returns_scripted_result():
    provider = FakeLLMProvider(structured_results=[{"goal": "g", "steps": []}])

    result = asyncio.run(
        provider.generate_structured(
            prompt="plan this",
            schema={"type": "object"},
            schema_name="plan",
        )
    )

    assert result == {"goal": "g", "steps": []}


def test_generate_structured_defaults_to_empty_dict_when_unscripted():
    provider = FakeLLMProvider()

    result = asyncio.run(
        provider.generate_structured(
            prompt="plan this",
            schema={"type": "object"},
            schema_name="plan",
        )
    )

    assert result == {}


def test_generate_structured_records_the_call():
    provider = FakeLLMProvider()
    schema = {"type": "object"}

    asyncio.run(
        provider.generate_structured(
            prompt="plan this",
            schema=schema,
            schema_name="plan",
        )
    )

    prompt, recorded_schema, schema_name = provider.generate_structured_calls[0]
    assert prompt == "plan this"
    assert recorded_schema == schema
    assert schema_name == "plan"
