from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.agent.planner import Planner
from app.agent.state import InvestigationState
from app.tools.deployment_tool import DeploymentTool
from app.tools.log_tool import LogTool
from app.tools.metrics_tool import MetricsTool
from app.tools.rag_tool import RagTool


tool_map = {
    "deployment": DeploymentTool(),
    "logs": LogTool(),
    "metrics": MetricsTool(),
    "rag": RagTool(),
}


class AgentOrchestrator:
    def __init__(self) -> None:
        self.planner = Planner()
        self._graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(dict)

        async def orchestrate(node_state: dict) -> dict:
            state: InvestigationState = node_state["state"]
            plan = self.planner.plan(state)
            for tool_name in plan:
                tool = tool_map[tool_name]
                state = await tool.run(state)
                state.tool_history.append(tool_name)
            return {"state": state}

        graph.add_node("orchestrate", orchestrate)
        graph.set_entry_point("orchestrate")
        graph.add_edge("orchestrate", END)
        return graph.compile()

    async def run(self, state: InvestigationState) -> InvestigationState:
        result = await self._graph.ainvoke({"state": state})
        return result["state"]
