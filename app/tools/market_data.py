import yfinance as yf
from nsepython import nse_quote_ltp, nse_get_fno_lot_sizes
import pandas as pd
from typing import Dict, Any, Optional

class MarketDataTool:
    @staticmethod
    def get_price_info(symbol: str) -> Dict[str, Any]:
        """Fetch real-time price info using yfinance and nsepython fallback."""
        try:
            # Add suffix for Indian markets if not present
            if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
                ticker_symbol = f"{symbol}.NS"
            else:
                ticker_symbol = symbol
            
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "current_price": info.get("currentPrice"),
                "day_high": info.get("dayHigh"),
                "day_low": info.get("dayLow"),
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "roe": info.get("returnOnEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "pb_ratio": info.get("priceToBook"),
                "source": "yfinance"
            }
        except Exception as e:
            # Fallback to nsepython for LTP if yfinance fails
            try:
                ltp = nse_quote_ltp(symbol)
                return {
                    "symbol": symbol,
                    "current_price": ltp,
                    "source": "nsepython",
                    "note": f"Limited data available via fallback. Error: {str(e)}"
                }
            except Exception as e2:
                return {"error": f"Failed to fetch data for {symbol}: {str(e2)}"}

    @staticmethod
    def get_historical_data(symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """Fetch historical price data for technical analysis."""
        if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
            symbol = f"{symbol}.NS"
        ticker = yf.Ticker(symbol)
        return ticker.history(period=period)
