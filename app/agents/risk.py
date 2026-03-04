# Invest Today: Risk Analyst Agent
from typing import Dict, Any
from app.tools.news import NewsTool
from app.tools.economic import EconomicTool
from app.core.llm_service import llm_service

class RiskAnalystAgent:
    def __init__(self):
        self.news_tool = NewsTool()

    def analyze(self, symbol: str, state: Dict[str, Any] = None) -> str:
        """Analyze specific and macro risks for a stock."""
        macro_data = EconomicTool.get_india_macro_data()
        
        # Also check for regulatory news specifically
        regulatory_news = self.news_tool.get_company_news(f"{symbol} SEBI regulation", limit=3)
        regulatory_text = "\n".join([f"- {item.get('title')}" for item in regulatory_news]) if regulatory_news else "No specific regulatory news found."

        prompt = f"""
        You are a Risk Analyst for Indian Capital Markets.
        Evaluate various risk factors for {symbol} based on the following:
        
        Macro Trends (India):
        - GDP Growth: {macro_data.get('gdp_growth', 'N/A')}
        - Inflation: {macro_data.get('inflation', 'N/A')}
        - Unemployment: {macro_data.get('unemployment', 'N/A')}
        - USD/INR Exchange Rate: {macro_data.get('usd_inr', 'N/A')}
        - RBI Repo Rate: {macro_data.get('repo_rate', 'N/A')}
        
        Recent News/Regulatory Context:
        {regulatory_text}
        
        Identify:
        1. Specific Risks: Promoter pledging, regulatory scrutiny (SEBI), or legal issues.
        2. Macro Risks: Impact of USD/INR volatility and RBI interest rate trajectory on {symbol}'s sector.
        3. Sector-Specific Risks: Competition or disruption.
        4. Risk Rating: Low, Moderate, High, or Extreme.
        
        Keep the analysis sharp and cautionary.
        """

        try:
            return llm_service.generate_content(prompt, model_type="analyst")
        except Exception as e:
            return f"Risk Analysis Generation Error: {str(e)}"
