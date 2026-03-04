from typing import Dict, Any
from app.graph.state import InvestTodayState
from app.agents.technical import TechnicalAnalystAgent
from app.agents.fundamental import FundamentalAnalystAgent
from app.agents.sentiment import SentimentAnalystAgent
from app.agents.risk import RiskAnalystAgent
from app.agents.judge import JudgeAgent
from app.tools.market_data import MarketDataTool
import re
import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"📍 Router: Validating symbol {symbol}...")
        
        # Validate that it's an Indian stock
        stock_info = MarketDataTool.get_price_info(symbol)
        if "error" in stock_info:
            error_msg = f"{symbol} is not a part of the Indian stock market (NSE/BSE). Please enter a valid Indian stock ticker."
            logger.warning(f"📍 Router: Validation failed for {symbol}: {stock_info['error']}")
            return {"errors": [error_msg]}
            
        logger.info(f"📍 Router: Validated symbol {symbol}")
        # Pass the fetched info along to avoid redundant calls later
        return {
            "symbol": symbol, 
            "errors": [], 
            "metadata": {"stock_info": stock_info}
        }
    else:
        logger.warning(f"📍 Router: No symbol found in query '{query}'")
        return {"errors": ["Could not extract a valid ticker symbol from the query."]}

def technical_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Technical Analysis."""
    symbol = state["symbol"]
    logger.info(f"🛠️ Technical Node: Starting for {symbol}")
    agent = TechnicalAnalystAgent()
    report = agent.analyze(symbol, state)
    logger.info(f"🛠️ Technical Node: Completed for {symbol}")
    return {"reports": {"technical": report}}

def fundamental_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Fundamental Analysis."""
    symbol = state["symbol"]
    logger.info(f"📊 Fundamental Node: Starting for {symbol}")
    agent = FundamentalAnalystAgent()
    report = agent.analyze(symbol, state)
    logger.info(f"📊 Fundamental Node: Completed for {symbol}")
    return {"reports": {"fundamental": report}}

def sentiment_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Sentiment Analysis."""
    symbol = state["symbol"]
    logger.info(f"📉 Sentiment Node: Starting for {symbol}")
    agent = SentimentAnalystAgent()
    report = agent.analyze(symbol, state)
    logger.info(f"📉 Sentiment Node: Completed for {symbol}")
    return {"reports": {"sentiment": report}}

def risk_analyst_node(state: InvestTodayState) -> Dict[str, Any]:
    """Node for Risk Analysis."""
    symbol = state["symbol"]
    logger.info(f"⚖️ Risk Node: Starting for {symbol}")
    agent = RiskAnalystAgent()
    report = agent.analyze(symbol, state)
    logger.info(f"⚖️ Risk Node: Completed for {symbol}")
    return {"reports": {"risk": report}}

def judge_node(state: InvestTodayState) -> Dict[str, Any]:
    """
    The Judge Agent synthesizes all reports into a final recommendation.
    """
    symbol = state["symbol"]
    reports = state.get("reports", {})
    
    # Fan-in check: Ensure all 4 analyst reports are available
    expected_analysts = {"technical", "fundamental", "sentiment", "risk"}
    missing = expected_analysts - set(reports.keys())
    
    if missing:
        logger.info(f"👨‍⚖️ Judge Node: Waiting for analysts ({len(reports)}/4 complete). Missing: {missing}")
        # In current StateGraph, return an empty dict to signal no state update from this call
        # but the node still finishes. We need to handle this in workflow.py too or here.
        return {} 

    logger.info(f"👨‍⚖️ Judge Node: All reports received. Synthesizing verdict for {symbol}...")
    agent = JudgeAgent()
    recommendation = agent.synthesize(symbol, reports)
    logger.info(f"👨‍⚖️ Judge Node: Synthesis complete for {symbol}")
    
    return {"final_recommendation": recommendation}
