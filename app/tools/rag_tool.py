from app.agent.state import InvestigationState
from app.domain.evidence import Evidence
from app.rag.pipeline.rag_pipeline import RagPipeline


class RagTool:
    def __init__(self) -> None:
        self.pipeline = RagPipeline()

    async def run(self, state: InvestigationState) -> InvestigationState:
        context = await self.pipeline.run(state.query)
        if context:
            state.evidence.append(Evidence(source="docs", summary=context))
        return state
