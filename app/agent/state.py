from dataclasses import dataclass, field
from app.domain.evidence import Evidence


@dataclass
class InvestigationState:
    query: str
    service: str | None = None
    time_window: tuple[str | None, str | None] = (None, None)
    evidence: list[Evidence] = field(default_factory=list)
    tool_history: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    confidence: float = 0.0
