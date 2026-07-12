import asyncio

from app.agents.in_memory_conversation_memory import InMemoryConversationMemory


def test_get_history_returns_empty_list_for_unknown_conversation():
    memory = InMemoryConversationMemory()

    history = asyncio.run(memory.get_history("unknown"))

    assert history == []


def test_append_turn_then_get_history_returns_the_turn_in_order():
    memory = InMemoryConversationMemory()

    asyncio.run(memory.append_turn("c1", "hello", "hi there"))

    history = asyncio.run(memory.get_history("c1"))

    assert history == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi there"},
    ]


def test_multiple_turns_accumulate_in_order():
    memory = InMemoryConversationMemory()

    asyncio.run(memory.append_turn("c1", "first question", "first answer"))
    asyncio.run(memory.append_turn("c1", "second question", "second answer"))

    history = asyncio.run(memory.get_history("c1"))

    assert [m["content"] for m in history] == [
        "first question",
        "first answer",
        "second question",
        "second answer",
    ]


def test_conversations_are_isolated_by_id():
    memory = InMemoryConversationMemory()

    asyncio.run(memory.append_turn("c1", "a", "b"))
    asyncio.run(memory.append_turn("c2", "x", "y"))

    assert asyncio.run(memory.get_history("c1")) == [
        {"role": "user", "content": "a"},
        {"role": "assistant", "content": "b"},
    ]
    assert asyncio.run(memory.get_history("c2")) == [
        {"role": "user", "content": "x"},
        {"role": "assistant", "content": "y"},
    ]
