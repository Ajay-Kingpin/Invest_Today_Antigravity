from typing import Dict, Any
from app.graph.state import InvestTodayState
from app.agents.technical import TechnicalAnalystAgent
from app.agents.fundamental import FundamentalAnalystAgent
from app.agents.sentiment import SentimentAnalystAgent
from app.agents.risk import RiskAnalystAgent
from app.agents.judge import JudgeAgent
import re

def router_node(state: InvestTodayState) -> Dict[str, Any]:
    """
    Extracts the stock symbol from the query and validates it.
    """
    query = state.get("query", "").upper()
    STOP_WORDS = {"ANALYZE", "CHECK", "RESEARCH", "GET", "SHOW", "STOCK", "INFO", "PRICE", "FOR", "THIS", "PLEASE", "DO", "HOW", "IS"}
    
    # Extract all uppercase words that look like potential tickers
    words = re.findall(r'\b[A-Z0-9-]{2,}\b', query) # At least 2 characters
    
    # Filter out stop words
    potential_symbols = [w for w in words if w not in STOP_WORDS]
    
    if potential_symbols:
        symbol = potential_symbols[0]
        return {"symbol": symbol, "errors": []}
    else:
        return {"errors": ["Could not extract a valid ticker symbol from the query."]}

def technical_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Technical Analysis."""
    symbol = state["symbol"]
    agent = TechnicalAnalystAgent()
    report = agent.analyze(symbol)
    return {"reports": {"technical": report}}

def fundamental_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Fundamental Analysis."""
    symbol = state["symbol"]
    agent = FundamentalAnalystAgent()
    report = agent.analyze(symbol)
    return {"reports": {"fundamental": report}}

def sentiment_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Sentiment Analysis."""
    symbol = state["symbol"]
    agent = SentimentAnalystAgent()
    report = agent.analyze(symbol)
    return {"reports": {"sentiment": report}}

def risk_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Risk Analysis."""
    symbol = state["symbol"]
    agent = RiskAnalystAgent()
    report = agent.analyze(symbol)
    return {"reports": {"risk": report}}

def judge_node(state: InvestTodayState) -> Dict[str, Any]:
    """
    The Judge Agent synthesizes all reports into a final recommendation.
    """
    symbol = state["symbol"]
    reports = state["reports"]
    agent = JudgeAgent()
    recommendation = agent.synthesize(symbol, reports)
    
    # Simple extraction of confidence score if present (optional enhancement)
    return {"final_recommendation": recommendation}
