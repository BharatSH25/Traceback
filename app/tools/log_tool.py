from app.agent.state import InvestigationState
from app.domain.evidence import Evidence


class LogTool:
    async def run(self, state: InvestigationState) -> InvestigationState:
        # TODO: query logs from Postgres
        state.evidence.append(Evidence(source="logs", summary="Log evidence placeholder"))
        return state
