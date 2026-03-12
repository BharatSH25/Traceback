from app.agent.agent_graph import AgentOrchestrator
from app.agent.state import InvestigationState
from app.llm.llm_client import LLMClient
from app.llm.prompt_builder import PromptBuilder
from app.models.request_models import InvestigationRequest
from app.models.response_models import RootCauseReport


class InvestigationService:
    def __init__(self) -> None:
        self.agent = AgentOrchestrator()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient()

    async def investigate(self, req: InvestigationRequest) -> RootCauseReport:
        state = InvestigationState(
            query=req.query,
            service=req.service,
            time_window=(req.start_time, req.end_time),
        )
        state = await self.agent.run(state)
        prompt = self.prompt_builder.build(state)
        return await self.llm.generate(prompt)
