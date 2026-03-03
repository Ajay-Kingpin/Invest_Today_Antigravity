from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.graph.workflow import create_invest_today_graph
import os

app = FastAPI(title="Invest Today API", description="AI-powered Indian Stock Market Analysis")

class AnalysisRequest(BaseModel):
    query: str

class AnalysisResponse(BaseModel):
    symbol: str
    final_recommendation: str
    reports: Dict[str, str]
    errors: List[str]

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """
    Run the full LangGraph orchestration for a stock query.
    """
    try:
        # Create the graph (compiled instance)
        graph = create_invest_today_graph()
        
        # Initial state
        initial_state = {
            "query": request.query,
            "reports": {},
            "errors": [],
            "metadata": {}
        }
        
        # Invoke the graph
        # Note: LangGraph invoke is synchronous in our current implementation, 
        # but we use async def for the route for better scalability.
        result = graph.invoke(initial_state)
        
        if result.get("errors") and not result.get("symbol"):
            raise HTTPException(status_code=400, detail=result["errors"][0])
            
        return AnalysisResponse(
            symbol=result.get("symbol", "N/A"),
            final_recommendation=result.get("final_recommendation", "No recommendation generated."),
            reports=result.get("reports", {}),
            errors=result.get("errors", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/stocks/{symbol}")
def get_stock_data(symbol: str):
    """
    Direct endpoint for fetching current market data.
    """
    from app.tools.market_data import MarketDataTool
    data = MarketDataTool.get_price_info(symbol)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data
