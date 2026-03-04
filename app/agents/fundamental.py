# Invest Today: Fundamental Analyst Agent
from typing import Dict, Any
from app.tools.market_data import MarketDataTool
from app.core.llm_service import llm_service

class FundamentalAnalystAgent:
    def analyze(self, symbol: str, state: Dict[str, Any] = None) -> str:
        """Perform fundamental analysis on a stock symbol."""
        # Reuse info from router if available
        data = None
        if state and "metadata" in state and "stock_info" in state["metadata"]:
            data = state["metadata"]["stock_info"]
        
        if not data:
            data = MarketDataTool.get_price_info(symbol)
        
        if "error" in data:
            return f"Fundamental Analysis Error: {data['error']}"

        prompt = f"""
        You are an expert Fundamental Analyst specializing in Indian companies.
        Analyze the following financial metrics for {symbol}:
        
        Current Price: {data.get('current_price')}
        Market Cap: {data.get('market_cap')}
        PE Ratio (Trailing): {data.get('pe_ratio')}
        Dividend Yield: {data.get('dividend_yield')}
        Return on Equity (ROE): {data.get('roe')}
        Debt to Equity: {data.get('debt_to_equity')}
        Price to Book (PB): {data.get('pb_ratio')}
        Source: {data.get('source')}
        
        Provide a concise fundamental analysis.
        Focus on:
        1. Valuation: P/E and P/B analysis compared to sector averages.
        2. Profitability & Efficiency: ROE analysis.
        3. Financial Leverage: Debt to Equity implications for an Indian context.
        4. Long-term Investment Thesis: Qualitative summary based on these metrics.
        
        Keep your response professional and focused on long-term value.
        """

        try:
            return llm_service.generate_content(prompt, model_type="analyst")
        except Exception as e:
            return f"Fundamental Analysis Generation Error: {str(e)}"
