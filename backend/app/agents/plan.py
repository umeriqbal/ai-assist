from pydantic import BaseModel, ConfigDict


class PlanStep(BaseModel):
    """
    A single subtask on the way to a goal.
    """

    model_config = ConfigDict(extra="forbid")

    description: str


class Plan(BaseModel):
    """
    An ordered set of subtasks a `Planner` believes will achieve a goal.
    """

    model_config = ConfigDict(extra="forbid")

    goal: str
    steps: list[PlanStep]
