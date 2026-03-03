from langgraph.graph import StateGraph, END
from app.graph.state import InvestTodayState
from app.graph.nodes import (
    router_node,
    technical_analyst_node,
    fundamental_analyst_node,
    sentiment_analyst_node,
    risk_analyst_node,
    judge_node
)

def create_invest_today_graph():
    """
    Constructs the LangGraph workflow for Invest Today.
    """
    workflow = StateGraph(InvestTodayState)

    # Add Nodes
    workflow.add_node("router", router_node)
    workflow.add_node("technical_analyst", technical_analyst_node)
    workflow.add_node("fundamental_analyst", fundamental_analyst_node)
    workflow.add_node("sentiment_analyst", sentiment_analyst_node)
    workflow.add_node("risk_analyst", risk_analyst_node)
    workflow.add_node("judge", judge_node)

    # Define Edges
    workflow.set_entry_point("router")

    # After router, run all analysts in parallel
    workflow.add_edge("router", "technical_analyst")
    workflow.add_edge("router", "fundamental_analyst")
    workflow.add_edge("router", "sentiment_analyst")
    workflow.add_edge("router", "risk_analyst")

    # All analysts flow into the judge
    workflow.add_edge("technical_analyst", "judge")
    workflow.add_edge("fundamental_analyst", "judge")
    workflow.add_edge("sentiment_analyst", "judge")
    workflow.add_edge("risk_analyst", "judge")

    # Judge is the final step
    workflow.add_edge("judge", END)

    return workflow.compile()

# Generate the app instance
app = create_invest_today_graph()
