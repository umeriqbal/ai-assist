from typing import Any

from app.agents.memory import ConversationMemory


class InMemoryConversationMemory(ConversationMemory):
    """
    Process-local, non-persistent conversation memory. Data lives only
    for the lifetime of the process holding this instance.
    """

    def __init__(self) -> None:
        self._conversations: dict[str, list[dict[str, Any]]] = {}

    async def get_history(self, conversation_id: str) -> list[dict[str, Any]]:
        return list(self._conversations.get(conversation_id, []))

    async def append_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_message: str,
    ) -> None:
        history = self._conversations.setdefault(conversation_id, [])
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})
