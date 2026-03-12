from app.agent.state import InvestigationState
from app.domain.evidence import Evidence


class MetricsTool:
    async def run(self, state: InvestigationState) -> InvestigationState:
        # TODO: query metrics from Postgres
        state.evidence.append(Evidence(source="metrics", summary="Metrics evidence placeholder"))
        return state
