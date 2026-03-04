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
    workflow.add_node("dispatch", lambda state: state) # Dummy dispatch for fan-out
    workflow.add_node("technical_analyst", technical_analyst_node)
    workflow.add_node("fundamental_analyst", fundamental_analyst_node)
    workflow.add_node("sentiment_analyst", sentiment_analyst_node)
    workflow.add_node("risk_analyst", risk_analyst_node)
    workflow.add_node("judge", judge_node)

    # Define Edges
    workflow.set_entry_point("router")

    # Conditional router logic
    def route_after_router(state: InvestTodayState):
        if state.get("errors"):
            return "end"
        return "continue"

    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "end": END,
            "continue": "dispatch"
        }
    )

    # Parallel fan-out from dispatch
    workflow.add_edge("dispatch", "technical_analyst")
    workflow.add_edge("dispatch", "fundamental_analyst")
    workflow.add_edge("dispatch", "sentiment_analyst")
    workflow.add_edge("dispatch", "risk_analyst")

    # All analysts flow into the judge
    workflow.add_edge("technical_analyst", "judge")
    workflow.add_edge("fundamental_analyst", "judge")
    workflow.add_edge("sentiment_analyst", "judge")
    workflow.add_edge("risk_analyst", "judge")

    # Define a conditional edge for judge
    def should_continue(state: InvestTodayState):
        if state.get("final_recommendation"):
            return "end"
        return "wait"

    workflow.add_conditional_edges(
        "judge",
        should_continue,
        {
            "end": END,
            "wait": END # In LangGraph, if multiple branches hit END, it waits for all.
                        # The real fix is ensuring judge_node doesn't return a partial state.
        }
    )

    return workflow.compile()

# Generate the app instance
app = create_invest_today_graph()
