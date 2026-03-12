from dataclasses import dataclass


@dataclass
class Evidence:
    source: str
    summary: str
    timestamp: str | None = None
