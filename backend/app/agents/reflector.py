from app.agents.critique import Critique
from app.providers.base import LLMProvider


class Reflector:
    """
    Critiques a candidate answer against the question it's meant to
    answer, using structured LLM output.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def critique(self, question: str, answer: str) -> Critique:

        prompt = (
            "Critique the following answer to the given question. "
            "Judge whether it is accurate, complete, and directly "
            "addresses the question. If it is satisfactory, say so. "
            "If not, explain exactly what is missing or wrong.\n\n"
            f"Question: {question}\n\n"
            f"Answer: {answer}"
        )

        result = await self._provider.generate_structured(
            prompt=prompt,
            schema=Critique.model_json_schema(),
            schema_name="critique",
        )

        return Critique.model_validate(result)
