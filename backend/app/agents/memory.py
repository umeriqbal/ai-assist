from abc import ABC, abstractmethod
from typing import Any


class ConversationMemory(ABC):
    """
    Interface implemented by all conversation memory stores.

    Stores the human-visible exchange (user message, final assistant
    answer) for a conversation — not the intermediate tool-call
    round-trips an agent may go through to produce that answer.
    """

    @abstractmethod
    async def get_history(self, conversation_id: str) -> list[dict[str, Any]]:
        """
        Return the stored turns for a conversation, oldest first.
        """
        raise NotImplementedError

    @abstractmethod
    async def append_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_message: str,
    ) -> None:
        """
        Record one user/assistant exchange for a conversation.
        """
        raise NotImplementedError
