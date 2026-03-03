import pytest
from app.graph.state import InvestTodayState
from app.graph.nodes import router_node
from app.graph.workflow import create_invest_today_graph

def test_router_node_valid_symbol():
    state = {"query": "Analyze RELIANCE stock"}
    result = router_node(state)
    assert result["symbol"] == "RELIANCE"
    assert "errors" not in result or len(result["errors"]) == 0

def test_router_node_invalid_symbol():
    state = {"query": "Analyze this please"}
    result = router_node(state)
    assert "symbol" not in result or result.get("symbol") is None
    assert "errors" in result and len(result["errors"]) > 0

def test_graph_compilation():
    graph = create_invest_today_graph()
    assert graph is not None
    # Check if node names are present in the internal graph
    node_names = [node for node in graph.nodes]
    assert "router" in node_names

@pytest.mark.asyncio
async def test_full_graph_flow_mocked():
    """
    Test the full graph flow using mocked agent components.
    """
    from unittest.mock import patch, MagicMock
    
    graph = create_invest_today_graph()
    initial_state = {"query": "Analyze RELIANCE", "reports": {}, "errors": [], "metadata": {}}
    
    # Patch the analysis methods directly in the agent classes
    with patch('app.agents.technical.TechnicalAnalystAgent.analyze', return_value="Bullish"), \
         patch('app.agents.fundamental.FundamentalAnalystAgent.analyze', return_value="Strong"), \
         patch('app.agents.sentiment.SentimentAnalystAgent.analyze', return_value="Positive"), \
         patch('app.agents.risk.RiskAnalystAgent.analyze', return_value="Low"), \
         patch('app.agents.judge.JudgeAgent.synthesize', return_value="BUY"):
        
        # We need to use invoke since it's a compiled graph
        result = graph.invoke(initial_state)
        
        assert result["symbol"] == "RELIANCE"
        assert "technical" in result["reports"]
        assert result["final_recommendation"] == "BUY"
