# Invest Today: Fundamental Analyst Agent
from typing import Dict, Any
from app.tools.market_data import MarketDataTool
from app.core.config import settings
import google.generativeai as genai

class FundamentalAnalystAgent:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.ANALYST_MODEL)

    def analyze(self, symbol: str) -> str:
        """Perform fundamental analysis on a stock symbol."""
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
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Fundamental Analysis Generation Error: {str(e)}"
