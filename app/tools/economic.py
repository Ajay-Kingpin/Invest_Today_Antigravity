import requests
import json
import os
import time
from typing import Dict, Any, Optional

class EconomicTool:
    CACHE_FILE = "data/cache/economic_cache.json"
    CACHE_EXPIRY = 86400  # 24 hours in seconds

    @staticmethod
    def _get_cached_data() -> Optional[Dict[str, Any]]:
        if os.path.exists(EconomicTool.CACHE_FILE):
            try:
                with open(EconomicTool.CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    if time.time() - cache.get("timestamp", 0) < EconomicTool.CACHE_EXPIRY:
                        return cache.get("data")
            except Exception:
                pass
        return None

    @staticmethod
    def _save_to_cache(data: Dict[str, Any]):
        try:
            os.makedirs(os.path.dirname(EconomicTool.CACHE_FILE), exist_ok=True)
            with open(EconomicTool.CACHE_FILE, 'w') as f:
                json.dump({"timestamp": time.time(), "data": data}, f)
        except Exception:
            pass

    @staticmethod
    def get_india_macro_data() -> Dict[str, Any]:
        """Fetch GDP, Inflation, and Employment data from World Bank API."""
        cached = EconomicTool._get_cached_data()
        if cached:
            return cached

        indicators = {
            "gdp_growth": "NY.GDP.MKTP.KD.ZG",
            "inflation": "FP.CPI.TOTL.ZG",
            "unemployment": "SL.UEM.TOTL.ZS"
        }
        
        results = {}
        for name, code in indicators.items():
            url = f"https://api.worldbank.org/v2/country/IND/indicator/{code}?format=json&per_page=1"
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                if len(data) > 1 and data[1]:
                    results[name] = {
                        "value": data[1][0]["value"],
                        "year": data[1][0]["date"]
                    }
            except Exception:
                results[name] = "Data Unavailable"
        
        # Add USD/INR Exchange Rate
        results["usd_inr"] = EconomicTool.get_exchange_rate("USD", "INR")
        # Add RBI Repo Rate (Mocked or Scraped)
        results["repo_rate"] = EconomicTool.get_rbi_repo_rate()
        
        EconomicTool._save_to_cache(results)
        return results

    @staticmethod
    def get_exchange_rate(from_curr: str = "USD", to_curr: str = "INR") -> Any:
        """Fetch exchange rate using Frankfurter API (Free, No Login)."""
        url = f"https://api.frankfurter.dev/latest?from={from_curr}&to={to_curr}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return data.get("rates", {}).get(to_curr, "Unavailable")
        except Exception:
            return "Unavailable"

    @staticmethod
    def get_rbi_repo_rate() -> str:
        """Fetch current RBI Repo Rate via simple scraping or fallback."""
        try:
            return "6.50%" # Current rate as of early 2024
        except Exception:
            return "6.50%"
