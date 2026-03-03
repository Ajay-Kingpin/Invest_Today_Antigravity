import pytest
from fastapi.testclient import TestClient
from app.api.routes import app
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_stock_data_endpoint():
    with patch('app.tools.market_data.MarketDataTool.get_price_info') as mock_tool:
        mock_tool.return_value = {"symbol": "RELIANCE", "current_price": 2500.0}
        response = client.get("/stocks/RELIANCE")
        assert response.status_code == 200
        assert response.json()["symbol"] == "RELIANCE"

@pytest.mark.asyncio
async def test_analyze_endpoint():
    with patch('app.api.routes.create_invest_today_graph') as mock_graph_factory:
        mock_graph = mock_graph_factory.return_value
        mock_graph.invoke.return_value = {
            "symbol": "RELIANCE",
            "final_recommendation": "BUY",
            "reports": {"technical": "Bullish"},
            "errors": []
        }
        
        response = client.post("/analyze", json={"query": "Analyze RELIANCE"})
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "RELIANCE"
        assert data["final_recommendation"] == "BUY"
