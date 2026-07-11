"""
Faithfulness Prompt Builder

Formats a question, its generated answer, and the context it was
grounded in into a judge prompt for an LLMProvider, asking it to
verify whether the answer is fully supported by the context.

Responsibilities:
- Ask the model to check the answer against the context only.
- Request a strict, parseable JSON verdict.

Does NOT:
- Call any LLM
- Parse the model's response
"""

_INSTRUCTIONS = (
    "You are a strict fact-checker. Given the CONTEXT and an ANSWER "
    "that was generated from it, determine whether every claim in the "
    "ANSWER is directly supported by the CONTEXT. Do not use outside "
    "knowledge to judge correctness — only check whether the CONTEXT "
    "supports the ANSWER.\n\n"
    "Respond with ONLY a JSON object in this exact shape, no other "
    "text, no markdown formatting:\n"
    '{"faithful": true or false, "unsupported_claims": '
    '["specific phrase or claim from the answer not supported by the '
    'context", ...]}\n\n'
    "If every claim is supported, unsupported_claims must be an empty "
    "list."
)


class FaithfulnessPromptBuilder:
    """
    Builds a judge prompt for faithfulness evaluation.
    """

    @staticmethod
    def build(
        question: str,
        answer: str,
        context: list[str],
    ) -> str:

        context_block = "\n\n".join(context)

        return (
            f"{_INSTRUCTIONS}\n\n"
            f"CONTEXT:\n{context_block}\n\n"
            f"QUESTION: {question}\n\n"
            f"ANSWER: {answer}\n\n"
            f"JSON:"
        )
