# Invest Today: Judge Agent
from typing import Dict
from app.core.config import settings
import google.generativeai as genai

class JudgeAgent:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.JUDGE_MODEL)

    def synthesize(self, symbol: str, reports: Dict[str, str]) -> str:
        """Synthesize multiple specialist reports into a final recommendation."""
        
        prompt = f"""
        You are 'The Judge', the chief investment strategist at Invest Today.
        Your goal is to provide a final investment recommendation for {symbol} by synthesizing reports from specialized analysts.
        
        Analyst Reports:
        
        --- TECHNICAL REPORT ---
        {reports.get('technical', 'No technical report available.')}
        
        --- FUNDAMENTAL REPORT ---
        {reports.get('fundamental', 'No fundamental report available.')}
        
        --- SENTIMENT REPORT ---
        {reports.get('sentiment', 'No sentiment report available.')}
        
        --- RISK REPORT ---
        {reports.get('risk', 'No risk report available.')}
        
        Synthesis Tasks:
        1. Weigh the arguments from each specialist.
        2. Resolve any conflicts (e.g., Bullish Technicals vs. Bearish Fundamentals).
        3. Provide a FINAL RECOMMENDATION: Strong Buy, Buy, Hold, Sell, or Strong Sell.
        4. Assign a Confidence Score (0-100%).
        5. provide a "Bottom Line" summary for a retail investor.
        
        Be decisive, objective, and thorough. Use 'Gemini 1.5 Pro' reasoning to find the nuance.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Final Judgement Generation Error: {str(e)}"
