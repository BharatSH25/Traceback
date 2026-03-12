from app.agent.state import InvestigationState
from app.domain.evidence import Evidence


class DeploymentTool:
    async def run(self, state: InvestigationState) -> InvestigationState:
        # TODO: query deployments from Postgres
        state.evidence.append(Evidence(source="deployment", summary="Deployment evidence placeholder"))
        return state
