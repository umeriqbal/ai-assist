from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Interface implemented by all agent tools.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """
        JSON Schema describing the arguments accepted by `execute`.
        """
        raise NotImplementedError

    @abstractmethod
    async def execute(self, **kwargs: Any) -> str:
        raise NotImplementedError
