INVEST TODAY: AI INDIAN MARKET ANALYST
=====================================================

1. INTRODUCTION
---------------
Invest Today is an AI-powered stock analysis platform specifically designed for the Indian market (NSE/BSE). It uses a LangGraph-based multi-agent system to provide comprehensive Technical, Fundamental, Sentiment, and Risk analysis.

2. FEATURES
-----------
- High-fidelity Groww-style UI with Emerald Green theme.
- Multi-analyst reports synthesized by a "Judge" agent.
- Fast performance with 5s timeouts and 24-hour macro data caching.
- Robust validation for Indian stock tickers.
- Dockerized environment for easy deployment.

3. SETTING UP (LOCAL)
---------------------
Requires Python 3.12 and `uv` or `pip`.

Step 1: Create a virtual environment:
    python -m venv .venv
    .venv\Scripts\activate (Windows)

Step 2: Install dependencies:
    pip install .

Step 3: Configure Environment Variables:
    Create a .env file with:
    GOOGLE_API_KEY=your_gemini_key
    GROQ_API_KEY=your_groq_key (Optional fallback)
    GNEWS_API_KEY=your_gnews_key (Optional)

Step 4: Launching the App:
    python run_local.py
    This will start both the FastAPI backend (8000) and Streamlit frontend (8501).

4. DEPLOYING WITH DOCKER
------------------------
Step 1: Ensure Docker and Docker Compose are installed.
Step 2: Run the following command in the project root:
    docker-compose up --build

Access the UI at: http://localhost:8501
Access the API Docs at: http://localhost:8000/docs

5. INTERPRETING REPORTS
-----------
- Technical: RSIs, Moving Averages, and Price Action.
- Fundamental: Key ratios (P/E, Debt/Equity) from NSE data.
- Sentiment: Recent news impact on the stock.
- Risk: Promoter pledge, regulatory issues, and macro headwinds.
- The Verdict: Final "Buy/Hold/Sell" synthesis.

6. DISCLAIMER
-------------
Content shared on or through our digital media channels are for information and education purposes only and should not be treated as investment or trading advice. Investment in securities are subject to market risks, please carry out your due diligence before investing. And last but not the least, past performance is not indicative of future returns.

7. TROUBLESHOOTING
------------------
- If analysis times out: Try a different stock or restart the backend service.
- If "Apple" or "Tesla" returns an error: This is expected as the system strictly validates for the Indian market (NSE/BSE).
- If LLM fails: Ensure your API keys are valid and not rate-limited. The system will automatically attempt to fallback to Groq if configured.
