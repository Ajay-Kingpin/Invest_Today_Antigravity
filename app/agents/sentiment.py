# Invest Today: Sentiment Analyst Agent
from typing import List, Dict, Any
from app.tools.news import NewsTool
from app.core.llm_service import llm_service

class SentimentAnalystAgent:
    def __init__(self):
        self.news_tool = NewsTool()

    def analyze(self, symbol: str, state: Dict[str, Any] = None) -> str:
        """Analyze market sentiment based on recent news."""
        news = self.news_tool.get_company_news(symbol)
        
        if not news or (len(news) == 1 and "error" in news[0]):
            return f"Sentiment Analysis Error: Could not fetch news for {symbol}."

        news_text = "\n".join([f"- {item.get('title')}" for item in news])
        
        prompt = f"""
        You are a Sentiment Analyst for the Indian Stock Market.
        Analyze the following news headlines related to {symbol}:
        
        {news_text}
        
        Tasks:
        1. Summarize the key themes in the news.
        2. Assign a sentiment score for each headline (Positive, Neutral, Negative).
        3. Provide an overall Sentiment Score (-1.0 to 1.0) where 1.0 is extremely bullish and -1.0 is extremely bearish.
        4. Explain the "Why" behind the overall score.
        
        Keep your response concise and objective.
        """

        try:
            return llm_service.generate_content(prompt, model_type="analyst")
        except Exception as e:
            return f"Sentiment Analysis Generation Error: {str(e)}"
