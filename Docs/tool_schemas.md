# Tool Schemas Documentation

This document outlines the input and output schemas for the tools used by the Invest Today analyst agents.

## 1. Market Data Tool (`market_data.py`)

Provides real-time and historical market data for Indian stocks (NSE/BSE).

### `get_price_info`
- **Input**:
    - `symbol` (str): The stock ticker (e.g., "RELIANCE" or "TCS.NS").
- **Output** (Dict):
    - `symbol` (str): Requested ticker.
    - `current_price` (float): Last traded price.
    - `day_high` (float): High of the day.
    - `day_low` (float): Low of the day.
    - `volume` (int): Trading volume.
    - `market_cap` (int): Total market capitalization.
    - `pe_ratio` (float): Price-to-Earnings ratio.
    - `dividend_yield` (float): Dividend yield percentage.
    - `roe` (float): Return on Equity.
    - `debt_to_equity` (float): Debt to equity ratio.
    - `pb_ratio` (float): Price to Book ratio.
    - `source` (str): Data source (e.g., "yfinance" or "nsepython").

### `get_historical_data`
- **Input**:
    - `symbol` (str): The stock ticker.
    - `period` (str): Time range (e.g., "1mo", "3mo", "1y").
- **Output** (pd.DataFrame):
    - Columns: `Open`, `High`, `Low`, `Close`, `Volume`.

---

## 2. News Tool (`news.py`)

Fetches recent financial news headlines and articles.

### `get_company_news`
- **Input**:
    - `company_name` (str): The name or ticker of the company.
    - `limit` (int): Maximum number of headlines to return (default: 5).
- **Output** (List[Dict]):
    - Each dict contains:
        - `title` (str): Headline title.
        - `link` (str): URL to the news source.
        - `source` (str): Publication name.
        - `content` (str): Snippet or full text (if available).

---

## 3. Economic Tool (`economic.py`)

Retrieves macro-economic indicators for the Indian economy.

### `get_india_macro_data`
- **Input**: None.
- **Output** (Dict):
    - `gdp_growth` (Dict): `{value, year}`.
    - `inflation` (Dict): `{value, year}`.
    - `unemployment` (Dict): `{value, year}`.
    - `usd_inr` (float): Current exchange rate.
    - `repo_rate` (str): Current RBI benchmark rate.
