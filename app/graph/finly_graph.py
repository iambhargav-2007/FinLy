from langgraph.graph import StateGraph
from core.state import FinanceState

from agents.risk_reasonin import risk_reasoning_node
from agents.decision import decision_agent_node
from agents.action import action_execution_node
from agents.memory import memory_agent_node




graph = StateGraph(FinanceState)

graph.add_node("risk_reasoning", risk_reasoning_node)
graph.add_node("decision_agent", decision_agent_node)
graph.add_node("action_execution", action_execution_node)
graph.add_node("memory_agent", memory_agent_node)


graph.set_entry_point("risk_reasoning")
graph.add_edge("risk_reasoning", "decision_agent")
graph.add_edge("decision_agent", "action_execution")
graph.add_edge("action_execution", "memory_agent")


finly_graph = graph.compile()
