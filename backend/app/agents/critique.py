from pydantic import BaseModel, ConfigDict


class Critique(BaseModel):
    """
    A self-assessment of a candidate answer against the question it's
    meant to answer.
    """

    model_config = ConfigDict(extra="forbid")

    is_satisfactory: bool
    feedback: str
