from app.agent.state import InvestigationState


class PromptBuilder:
    def build(self, state: InvestigationState) -> str:
        evidence_lines = [f"- {e.source}: {e.summary}" for e in state.evidence]
        evidence_block = "\n".join(evidence_lines)
        return (
            "You are an incident investigator.\n"
            f"Query: {state.query}\n\n"
            "Evidence:\n"
            f"{evidence_block}\n"
            "Provide a root cause analysis with confidence and next steps."
        )
