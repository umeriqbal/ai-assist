from app.agents.supervisor_decision import SupervisorDecision
from app.providers.base import LLMProvider


class Supervisor:
    """
    Decides which specialist should act next given the conversation
    so far, using structured LLM output.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def decide(self, messages: list[dict]) -> SupervisorDecision:

        transcript = "\n".join(
            f"{message.get('name', message['role'])}: {message['content']}"
            for message in messages
        )

        prompt = (
            "You are coordinating two specialists to answer the user's "
            "request:\n"
            "- researcher: searches the knowledge base for relevant facts.\n"
            "- writer: has no tools; drafts or polishes the final answer "
            "from information already gathered.\n\n"
            "Given the conversation so far, decide which specialist should "
            "act next and exactly what they should do. Route to the "
            "researcher only if information is still needed. Route to the "
            "writer once enough information is available to compose a "
            "final answer. Choose 'finish' only after the writer has "
            "already produced a complete final answer.\n\n"
            f"Conversation so far:\n{transcript}"
        )

        result = await self._provider.generate_structured(
            prompt=prompt,
            schema=SupervisorDecision.model_json_schema(),
            schema_name="supervisor_decision",
        )

        return SupervisorDecision.model_validate(result)
