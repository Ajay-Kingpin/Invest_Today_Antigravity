# Invest Today: Technical Analyst Agent
import pandas as pd
import numpy as np
from typing import Dict, Any
from app.tools.market_data import MarketDataTool
from app.core.llm_service import llm_service

class TechnicalAnalystAgent:
    def analyze(self, symbol: str, state: Dict[str, Any] = None) -> str:
        """Perform technical analysis on a stock symbol."""
        df = MarketDataTool.get_historical_data(symbol, period="3mo")
        if df is None or df.empty:
            return f"Technical Analysis Error: Could not fetch historical data for {symbol}."

        # Calculate Indicators
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD Calculation
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        latest = df.iloc[-1]

        data_summary = {
            "symbol": symbol,
            "current_price": latest['Close'],
            "sma20": latest['SMA20'],
            "sma50": latest['SMA50'],
            "rsi": latest['RSI'],
            "macd": latest['MACD'],
            "signal_line": latest['Signal_Line'],
            "trend": "Upward" if latest['Close'] > latest['SMA20'] else "Downward"
        }

        prompt = f"""
        You are an expert Technical Analyst specializing in the Indian Stock Market (NSE/BSE).
        Analyze the following technical data for {symbol}:
        
        Current Price: {data_summary['current_price']:.2f}
        SMA 20: {data_summary['sma20']:.2f}
        SMA 50: {data_summary['sma50']:.2f}
        RSI (14): {data_summary['rsi']:.2f}
        MACD: {data_summary['macd']:.2f}
        Signal Line: {data_summary['signal_line']:.2f}
        Price vs SMA20: {data_summary['trend']}
        
        Provide a concise technical outlook.
        Identify:
        1. Support and Resistance levels (estimate from recent data).
        2. Bullish/Bearish signals from RSI and MACD.
        3. Short-term trend recommendation (Strong Buy, Buy, Hold, Sell, Strong Sell).
        
        Keep your response professional and data-driven.
        """

        try:
            return llm_service.generate_content(prompt, model_type="analyst")
        except Exception as e:
            return f"Technical Analysis Generation Error: {str(e)}"
