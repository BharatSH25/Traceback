from app.agent.state import InvestigationState


class Planner:
    def plan(self, state: InvestigationState) -> list[str]:
        # Simple heuristic plan; replace with richer logic later.
        return ["deployment", "logs", "metrics", "rag"]
