from pydantic import BaseModel, ConfigDict

from app.agents.plan import Plan, PlanStep
from app.providers.base import LLMProvider


class _PlanStepsResponse(BaseModel):
    """
    Structured-output shape requested from the model. Only the steps
    are generated; `goal` is filled in from the caller's input rather
    than trusted to be echoed back verbatim.
    """

    model_config = ConfigDict(extra="forbid")

    steps: list[PlanStep]


class Planner:
    """
    Turns a goal into an ordered `Plan` using structured LLM output.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def create_plan(self, goal: str) -> Plan:

        goal = goal.strip()

        if not goal:
            raise ValueError("Goal cannot be empty.")

        prompt = (
            "Break the following goal into an ordered list of concrete, "
            "actionable steps needed to achieve it. Keep the plan minimal "
            "— only include steps that are actually necessary.\n\n"
            f"Goal: {goal}"
        )

        result = await self._provider.generate_structured(
            prompt=prompt,
            schema=_PlanStepsResponse.model_json_schema(),
            schema_name="plan_steps",
        )

        parsed = _PlanStepsResponse.model_validate(result)

        return Plan(goal=goal, steps=parsed.steps)
