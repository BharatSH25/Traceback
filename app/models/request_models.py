from pydantic import BaseModel


class InvestigationRequest(BaseModel):
    query: str
    service: str | None = None
    start_time: str | None = None
    end_time: str | None = None
