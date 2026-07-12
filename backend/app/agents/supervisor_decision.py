from typing import Literal

from pydantic import BaseModel, ConfigDict


class SupervisorDecision(BaseModel):
    """
    A supervisor's routing decision: which specialist should act next
    (or whether the task is done), and what that specialist should do.
    """

    model_config = ConfigDict(extra="forbid")

    next: Literal["researcher", "writer", "finish"]
    instructions: str
