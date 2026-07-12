from dataclasses import dataclass

from app.agents.plan import Plan, PlanStep
from app.agents.planner import Planner
from app.providers.base import LLMProvider
from app.services.agent_service import AgentService


@dataclass
class PlanResult:
    """
    The outcome of running a plan end-to-end: the plan itself, each
    step's raw result, and the final synthesized answer.
    """

    plan: Plan
    step_results: list[str]
    answer: str


def _step_prompt(goal: str, step: PlanStep, prior_results: list[str]) -> str:

    prompt = f"Overall goal: {goal}\n\nCurrent step: {step.description}"

    if prior_results:
        prompt += "\n\nResults so far:\n" + "\n".join(
            f"- {result}" for result in prior_results
        )

    return prompt


def _synthesis_prompt(goal: str, plan: Plan, step_results: list[str]) -> str:

    results_block = "\n\n".join(
        f"Step {i}: {step.description}\nResult: {result}"
        for i, (step, result) in enumerate(zip(plan.steps, step_results), start=1)
    )

    return (
        f"Goal: {goal}\n\n"
        "The following steps were executed to achieve this goal:\n\n"
        f"{results_block}\n\n"
        "Using the results above, write a single, coherent final answer "
        "to the goal."
    )


class PlanningService:
    """
    Business service that plans a goal, executes each step, and
    synthesizes a final answer.
    """

    def __init__(
        self,
        planner: Planner,
        agent_service: AgentService,
        provider: LLMProvider,
    ) -> None:
        self._planner = planner
        self._agent_service = agent_service
        self._provider = provider

    async def run(self, goal: str) -> PlanResult:

        plan = await self._planner.create_plan(goal)

        if not plan.steps:
            answer = await self._provider.chat(prompt=goal)
            return PlanResult(plan=plan, step_results=[], answer=answer)

        step_results: list[str] = []

        for step in plan.steps:
            result = await self._agent_service.chat(
                _step_prompt(plan.goal, step, step_results)
            )
            step_results.append(result)

        answer = await self._provider.chat(
            prompt=_synthesis_prompt(plan.goal, plan, step_results)
        )

        return PlanResult(plan=plan, step_results=step_results, answer=answer)
