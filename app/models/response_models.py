from pydantic import BaseModel


class RootCauseReport(BaseModel):
    primary_cause: str
    contributing_factors: list[str] = []
    timeline: list[str] = []
    evidence: list[str] = []
    confidence: float = 0.0
    next_steps: list[str] = []
